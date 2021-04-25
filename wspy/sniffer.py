###########################################################################
# wspy: Python wrapper around libwireshark                                #
# Copyright (C) 2021  Jack A Bernard Jr.                                  #
#                                                                         #
# This program is free software; you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation; either version 2 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# This program is distributed in the hope that it will be useful,         #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License along #
# with this program; if not, write to the Free Software Foundation, Inc., #
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.             #
###########################################################################

from wspy.glib import *
from wspy.c_types import *
from wspy.libwireshark import *
from wspy.errors import WSError
from ctypes import *
import errno
from datetime import datetime
import os

def _wtap_error(err, err_info):
    msg = None
    if err.value != 0:
        if bool(err_info):
            msg = '{}: {} - {}'.format(errno.errorcode[-err.value], os.strerror(err.value), err_info.value.decode('utf-8'))
            g_free(err_info)
        else:
            msg = '{}: {}'.format(errno.errorcode[-err.value], os.strerror(err.value))
    elif bool(err_info):
        msg = err_info.value.decode('utf-8')
        g_free(err_info)
    else:
        raise WSError('unknown error!')
    raise WSError(msg)



class Record:
    def __init__(self):
        self._rec = wtap_rec()
        self._buf = Buffer()
        wtap_rec_init(byref(self._rec))
        ws_buffer_init(byref(self._buf), 1514)

    def __del__(self):
        ws_buffer_free(byref(self._buf))
        wtap_rec_cleanup(byref(self._rec))

    @property
    def type(self):
        if self._rec.rec_type == REC_TYPE_PACKET:
            return 'packet'
        elif self._rec.rec_type == REC_TYPE_FT_SPECIFIC_EVENT:
            return 'file-type-specific-event'
        elif self._rec.rec_type == REC_TYPE_FT_SPECIFIC_REPORT:
            return 'file-type-specific-report'
        elif self._rec.rec_type == REC_TYPE_SYSCALL:
            return 'syscall'
        elif self._rec.rec_type == REC_TYPE_SYSTEMD_JOURNAL:
            return 'systemd-journal'
        else:
            return None

    @property
    def data(self):
        if self._rec.rec_type == REC_TYPE_PACKET:
            return self._buf.data[:self._rec.rec_header.packet_header.caplen]
        elif self._rec.rec_type == REC_TYPE_FT_SPECIFIC_EVENT:
            return self._buf.data[:self._rec.rec_header.ft_specific_header.record_len]
        elif self._rec.rec_type == REC_TYPE_FT_SPECIFIC_REPORT:
            return self._buf.data[:self._rec.rec_header.ft_specific_header.record_len]
        elif self._rec.rec_type == REC_TYPE_SYSCALL:
            return self._buf.data[:self._rec.rec_header.syscall_header.event_len]
        elif self._rec.rec_type == REC_TYPE_SYSTEMD_JOURNAL:
            return self._buf.data[:self._rec.rec_header.systemd_journal_header.record_len]
        else:
            return None

    @property
    def timestamp(self):
        if (self._rec.presence_flags & WTAP_HAS_TS) == 0:
            return None
        ts = self._rec.ts.secs + (float(self._rec.ts.nsecs) / 1000000000.0)
        return datetime.fromtimestamp(ts)



class Sniffer:
    _exists = False

    def __init__(self, capfile=None, interface=None):
        self._dead = True
        if Sniffer._exists:
            raise WSError('only one WSPY session can exist at a time')
        Sniffer._exists = True
        self._dead = False

        if interface == None and capfile == None:
            raise WSError('wspy.Sniffer requires a capture file or an interface')

        if interface != None and capfile != None:
            raise WSError('wspy.Sniffer requires a capture file or an interface, not both')

        if interface != None:
            raise WSError('wspy does not yet support live interface sniffing')

        err = c_int(0)
        err_info = gchar_p(None)
        filename = capfile.encode('utf-8')
        self._wth = wtap_open_offline(filename,
                                      WTAP_TYPE_AUTO,
                                      byref(err),
                                      byref(err_info),
                                      True)
        if not bool(self._wth):
            _wtap_error(err, err_info)
        wtap_set_cb_new_ipv4(self._wth, wtap_new_ipv4_callback_t(add_ipv4_name))
        wtap_set_cb_new_ipv6(self._wth, cast(add_ipv6_name, wtap_new_ipv6_callback_t))
        wtap_set_cb_new_secrets(self._wth, wtap_new_secrets_callback_t(secrets_wtap_callback))

        self._data_offset = gint64(0)

    def __del__(self):
        if not self._dead:
            wtap_close(self._wth)
            Sniffer._exists = False

    @property
    def data_offset(self):
        return self._data_offset

    def __iter__(self):
        return self

    def __next__(self):
        err = c_int(0)
        err_info = gchar_p(None)
        record = Record()
        if bool(wtap_read(self._wth,
                          byref(record._rec),
                          byref(record._buf),
                          byref(err),
                          byref(err_info),
                          byref(self._data_offset))):
            return record
        else:
            if err.value != 0:
                _wtap_error(err, err_info)
            raise StopIteration

