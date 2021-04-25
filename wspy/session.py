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

from wspy.errors import WSError
from wspy.libwireshark import *
from wspy.frame_tvbuff import frame_tvbuff_new_buffer
from wspy.utils import ptr_add, ptraddress
from wspy.columns import ColumnList
from wspy.proto_tree import ProtoNode
from wspy.tap import *

def _get_frame_ts(prov, frame_num):
    if bool(prov[0].ref) and prov[0].ref[0].num == frame_num:
        return cast(pointer(prov[0].ref[0].abs_ts), c_void_p).value
    if bool(prov[0].prev_dis) and prov[0].prev_dis[0].num == frame_num:
        return cast(pointer(prov[0].prev_dis[0].abs_ts), c_void_p).value
    if bool(prov[0].prev_cap) and prov[0].prev_cap[0].num == frame_num:
        return cast(pointer(prov[0].prev_cap[0].abs_ts), c_void_p).value
    if bool(prov[0].frames):
        fd = frame_data_sequence_find(prov[0].frames, frame_num)
        if bool(fd):
            return cast(pointer(fd[0].abs_ts), c_void_p)
    return None

def _get_interface_name(prov, interface_id):
    idb_info = wtap_file_get_idb_info(prov[0].wth)

    wtapng_if_descr = None
    if interface_id < idb_info[0].interface_data[0].len:
        wtapng_if_descr = ptr_add(idb_info[0].interface_data[0].data, interface_id, wtap_block_t)

    g_free(idb_info)

    interface_name = c_char_p(None)
    if bool(wtapng_if_descr):
        if wtap_block_get_string_option_value(wtapng_if_descr,
                                              OPT_IDB_NAME,
                                              byref(interface_name)) == WTAP_OPTTYPE_SUCCESS:
            return interface_name
        if wtap_block_get_string_option_value(wtapng_if_descr,
                                              OPT_IDB_DESCR,
                                              byref(interface_name)) == WTAP_OPTTYPE_SUCCESS:
            return interface_name
        if wtap_block_get_string_option_value(wtapng_if_descr,
                                              OPT_IDB_HARDWARE,
                                              byref(interface_name)) == WTAP_OPTTYPE_SUCCESS:
            return interface_name
    return c_char_p(b'unknown')

def _get_interface_description(prov, interface_id):
    idb_info = wtap_file_get_idb_info(prov[0].wth)

    wtapng_if_descr = None
    if interface_id < idb_info[0].interface_data[0].len:
        wtapng_if_descr = ptr_add(idb_info[0].interface_data[0].data, interface_id, wtap_block_t)

    g_free(idb_info)

    interface_name = c_char_p(None)
    if bool(wtapng_if_descr):
        if wtap_block_get_string_option_value(wtapng_if_descr,
                                              OPT_IDB_DESCR,
                                              byref(interface_name)) == WTAP_OPTTYPE_SUCCESS:
            return interface_name
    return None

__funcs = packet_provider_funcs()
_funcs = packet_provider_funcs(
    type(__funcs.get_frame_ts)(_get_frame_ts),
    type(__funcs.get_interface_name)(0),
    type(__funcs.get_interface_description)(0),
    type(__funcs.get_user_comment)(0))

class Packet:
    def __init__(self, session, record):
        self._session = session
        self._record = record
        self._cinfo = column_info()
        self._fdata = frame_data()

        session._count += 1
        build_column_format_array(byref(self._cinfo), prefs.num_cols, True)
        self._edt = epan_dissect_new(session._epan, True, True)
        frame_data_init(byref(self._fdata), session._count, record._rec,
                        session._sniffer._data_offset, session._cum_bytes)

        prime_epan_dissect_with_postdissector_wanted_hfids(self._edt)
        col_custom_prime_edt(self._edt, byref(self._cinfo))

        frame_data_set_before_dissect(byref(self._fdata), byref(session._elapsed_time),
                                      byref(session._provider.ref),
                                      session._provider.prev_dis)
        if ptraddress(session._provider.ref) == addressof(self._fdata):
            memmove(byref(session._ref_frame), byref(self._fdata), sizeof(frame_data))
            session._provider.ref = pointer(session._ref_frame)

        color_filters_prime_edt(self._edt)
        self._fdata.need_colorize = 1

        self._tvbuff = frame_tvbuff_new_buffer(pointer(session._provider),
                                               pointer(self._fdata),
                                               pointer(record._buf))
        epan_dissect_run_with_taps(self._edt,
                                   session._cd_t,
                                   byref(record._rec),
                                   self._tvbuff,
                                   byref(self._fdata),
                                   byref(self._cinfo))
        frame_data_set_after_dissect(byref(self._fdata), byref(session._cum_bytes))
        epan_dissect_fill_in_columns(self._edt, True, True)

        memmove(byref(session._prev_dis_frame), byref(self._fdata), sizeof(frame_data))
        session._provider.prev_dis = pointer(session._prev_dis_frame)

        memmove(byref(session._prev_cap_frame), byref(self._fdata), sizeof(frame_data))
        session._provider.prev_cap = pointer(session._prev_cap_frame)

    def __del__(self):
        frame_data_destroy(byref(self._fdata))
        epan_dissect_free(self._edt)

    @property
    def columns(self):
        return ColumnList(pointer(self._cinfo))

    @property
    def proto_tree(self):
        if bool(self._edt[0].tree):
            return ProtoNode(self._edt[0].tree)
        return None

class Session:
    def __init__(self, sniffer):
        prefs_apply_all()

        self._sniffer = sniffer
        self._provider = packet_provider_data()
        self._provider.wth = sniffer._wth
        self._provider.ref = None
        self._provider.prev_dis = None
        self._provider.prev_cap = None
        self._provider.frames = new_frame_data_sequence()
        self._provider.frames_user_comments = None

        self._epan = epan_new(byref(self._provider), byref(_funcs))
        self._elapsed_time = nstime_t()
        nstime_set_zero(byref(self._elapsed_time))
        self._cd_t = wtap_file_type_subtype(self._provider.wth)
        self._cum_bytes = guint32(0)
        self._ref_frame = frame_data()
        self._prev_dis_frame = frame_data()
        self._prev_cap_frame = frame_data()
        self._count = 0
    
    def __del__(self):
        epan_free(self._epan)

    def __iter__(self):
        return self

    def __next__(self):
        return Packet(self, next(self._sniffer))

    @property
    def total_bytes(self):
        return self._cum_bytes.value

    @property
    def packet_count(self):
        return self._count
