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
from wspy.utils import ptr_add
from wspy.errors import *
from ctypes import *

class _tvb_frame(Structure):
    _fields_ = [('tvb', tvbuff),
                ('buf', POINTER(Buffer)),
                ('prov', POINTER(packet_provider_data)),
                ('file_off', gint64),
                ('offset', guint)]

_buffer_cache = cast(c_void_p(0), POINTER(GPtrArray))

def _frame_read(frame_tvb, rec, buf):
    err = c_int(0)
    err_info = gchar_p(None)

    if not bool(wtap_seek_read(frame_tvb[0].prov[0].wth, frame_tvb[0].file_off, rec, buf, byref(err), byref(err_info))):
        if err.value == WTAP_ERR_BAD_FILE:
            g_free(err_info)
        return False
    return True

class _FrameCache:
    def __init__(self):
        self._buffer_cache = cast(c_void_p(0), POINTER(GPtrArray))

    def __call__(self, frame_tvb):
        rec = wtap_rec()
        wtap_rec_init(byref(rec))

        if not bool(frame_tvb[0].buf):
            if not bool(self._buffer_cache):
                self._buffer_cache = g_ptr_array_sized_new(1024)
            if self._buffer_cache[0].len > 0:
                frame_tvb[0].buf = cast(g_ptr_array_remove_index(self._buffer_cache, self._buffer_cache[0].len - 1), POINTER(Buffer))
            else:
                frame_tvb[0].buf = cast(g_malloc(sizeof(Buffer)), POINTER(Buffer))
            ws_buffer_init(frame_tvb[0].buf, frame_tvb[0].tvb.length + frame_tvb[0].offset)
            _frame_read(frame_tvb, byref(rec), frame_tvb[0].buf)

        frame_tvb[0].tvb.real_data = ptr_add(frame_tvb[0].buf[0].data, frame_tvb[0].buf[0].start + frame_tvb[0].offset, guint8)

        wtap_rec_cleanup(byref(rec))

_frame_cache = _FrameCache()

def _frame_free(tvb):
    frame_tvb = cast(tvb, POINTER(_tvb_frame))
    if bool(frame_tvb[0].buf):
        ws_buffer_free(frame_tvb[0].buf)
        g_ptr_array_add(_frame_cache._buffer_cache, frame_tvb[0].buf)

def _frame_offset(tvb, counter):
    return counter

def _frame_get_ptr(tvb, abs_offset, abs_length):
    frame_tvb = cast(tvb, POINTER(_tvb_frame))
    _frame_cache(frame_tvb)
    return ptr_add(tvb[0].real_data, abs_offset).value

def _frame_memcpy(tvb, target, abs_offset, abs_length):
    frame_tvb = cast(tvb, POINTER(_tvb_frame))
    _frame_cache(frame_tvb)
    target[:abs_length] = tvb[0].real_data[abs_offset:abs_offset+abs_length]
    return target

def _frame_find_guint8(tvb, abs_offset, limit, needle):
    frame_tvb = cast(tvb, POINTER(_tvb_frame))
    _frame_cache(frame_tvb)
    return tvb[0].real_data[abs_offset:abs_offset+limit].find(bytes([needle]))

def _frame_pbrk_guint8(tvb, abs_offset, limit, patter, found_needle):
    frame_tvb = cast(tvb, POINTER(_tvb_frame))
    _frame_cache(frame_tvb)
    return tvb_ws_mempbrk_pattern_guint(tvb, abs_offset, limit, pattern, found_needle)

_tvb_frame_ops = tvb_ops()

def _frame_clone(tvb, abs_offset, abs_length):
    frame_tvb = cast(tvb, POINTER(_tvb_frame))
    if not bool(frame_tvb[0].prov):
        return None

    abs_offset += frame_tvb[0].offset

    cloned_tvb = tvb_new(byref(_tvb_frame_ops))

    cloned_tvb[0].real_data = None
    cloned_tvb[0].length = abs_length
    cloned_tvb[0].reported_length = abs_length
    cloned_tvb[0].contiained_length = cloned_tvb[0].reported_length
    cloned_tvb[0].initialized = True
    cloned_tvb[0].ds_tvb = cloned_tvb

    cloned_frame_tvb = cast(cloned_tvb, POINTER(_tvb_frame))
    cloned_frame_tvb[0].prov = frame_tvb[0].prov
    cloned_frame_tvb[0].file_offset = frame_tvb[0].file_off
    cloned_frame_tvb[0].offset = abs_offset
    cloned_frame_tvb[0].buf = None

    return cast(cloned_tvb, c_void_p).value

_tvb_frame_ops.tvb_size = sizeof(_tvb_frame)
_tvb_frame_ops.tvb_free = type(_tvb_frame_ops.tvb_free)(_frame_free)
_tvb_frame_ops.tvb_offset = type(_tvb_frame_ops.tvb_offset)(_frame_offset)
_tvb_frame_ops.tvb_get_ptr = type(_tvb_frame_ops.tvb_get_ptr)(_frame_get_ptr)
_tvb_frame_ops.tvb_memcpy = type(_tvb_frame_ops.tvb_memcpy)(_frame_memcpy)
_tvb_frame_ops.tvb_find_guint8 = type(_tvb_frame_ops.tvb_find_guint8)(_frame_find_guint8)
_tvb_frame_ops.tvb_ws_mempbrk_pattern_guint8 = type(_tvb_frame_ops.tvb_ws_mempbrk_pattern_guint8)(_frame_pbrk_guint8)
_tvb_frame_ops.tvb_clone = type(_tvb_frame_ops.tvb_clone)(_frame_clone)

def frame_tvbuff_new(prov, fd, buf):
    tvb = tvb_new(byref(_tvb_frame_ops))
    tvb[0].real_data = buf
    tvb[0].length = fd[0].cap_len
    if fd[0].pkt_len > 0x7FFFFFFF:
        tvb[0].reported_length = 0x7FFFFFFF
    else:
        tvb[0].reported_length = fd[0].pkt_len
    tvb[0].contained_length = tvb[0].reported_length
    tvb[0].initialized = 1
    tvb[0].ds_tvb = tvb

    frame_tvb = cast(tvb, POINTER(_tvb_frame))

    if bool(prov[0].wth) and bool(prov[0].wth[0].random_fh):
        frame_tvb[0].prov = prov
        frame_tvb[0].file_off = fd[0].file_off
        frame_tvb[0].offset = 0
    else:
        frame_tvb[0].prov = None

    frame_tvb[0].buf = None

    return tvb

def frame_tvbuff_new_buffer(prov, fd, buf):
    return frame_tvbuff_new(prov, fd, ptr_add(buf[0].data, buf[0].start, guint8))
