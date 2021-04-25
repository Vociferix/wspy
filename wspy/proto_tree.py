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

from ctypes import *
from wspy.glib import *
from wspy.c_types import *
from wspy.libwireshark import *
from wspy.errors import *
from datetime import datetime, timedelta

class ProtoNodeIter:
    def __init__(self, node_ptr):
        self._node = node_ptr

    def __iter__(self):
        return self

    def __next__(self):
        if bool(self._node):
            node = self._node
            self._node = node[0].next
            return ProtoNode(node)
        raise StopIteration

class FieldValue:
    def __init__(self, node, value):
        self._node = node
        self._value = value

    @property
    def _finfo(self):
        return self._node[0].finfo

    @property
    def _hfinfo(self):
        if bool(self._finfo):
            return self._finfo[0].hfinfo
        return None

    @property
    def type(self):
        t = fvalue_type_ftenum(byref(self._value))
        if t == FT_PROTOCOL:
            return 'protocol'
        elif t == FT_BOOLEAN:
            return 'boolean'
        elif t == FT_CHAR:
            return 'char'
        elif t == FT_UINT8:
            return 'uint8'
        elif t == FT_UINT16:
            return 'uint16'
        elif t == FT_UINT24:
            return 'uint24'
        elif t == FT_UINT32:
            return 'uint32'
        elif t == FT_UINT40:
            return 'uint40'
        elif t == FT_UINT48:
            return 'uint48'
        elif t == FT_UINT56:
            return 'uint56'
        elif t == FT_UINT64:
            return 'uint64'
        elif t == FT_INT8:
            return 'int8'
        elif t == FT_INT16:
            return 'int16'
        elif t == FT_INT24:
            return 'int24'
        elif t == FT_INT32:
            return 'int32'
        elif t == FT_INT40:
            return 'int40'
        elif t == FT_INT48:
            return 'int48'
        elif t == FT_INT56:
            return 'int56'
        elif t == FT_INT64:
            return 'int64'
        elif t == FT_IEEE_11073_SFLOAT:
            return 'ieee_11037_sfloat'
        elif t == FT_IEEE_11073_FLOAT:
            return 'ieee_11037_float'
        elif t == FT_FLOAT:
            return 'float'
        elif t == FT_DOUBLE:
            return 'double'
        elif t == FT_ABSOLUTE_TIME:
            return 'absolute_time'
        elif t == FT_RELATIVE_TIME:
            return 'relative_time'
        elif t == FT_STRING:
            return 'string'
        elif t == FT_STRINGZ:
            return 'stringz'
        elif t == FT_UINT_STRING:
            return 'uint_string'
        elif t == FT_ETHER:
            return 'ether'
        elif t == FT_BYTES:
            return 'bytes'
        elif t == FT_UINT_BYTES:
            return 'uint_bytes'
        elif t == FT_IPv4:
            return 'ipv4'
        elif t == FT_IPv6:
            return 'ipv6'
        elif t == FT_IPXNET:
            return 'ipxnet'
        elif t == FT_FRAMENUM:
            return 'framenum'
        elif t == FT_PCRE:
            return 'pcre'
        elif t == FT_GUID:
            return 'guid'
        elif t == FT_OID:
            return 'oid'
        elif t == FT_EUI64:
            return 'eui64'
        elif t == FT_AX25:
            return 'ax25'
        elif t == FT_VINES:
            return 'vines'
        elif t == FT_REL_OID:
            return 'rel_oid'
        elif t == FT_SYSTEM_ID:
            return 'system_id'
        elif t == FT_STRINGZPAD:
            return 'stringzpad'
        elif t == FT_FCWWN:
            return 'fcwwn'
        elif t == FT_STRINGZTRUNC:
            return 'stringztrunc'
        else:
            return None

    def bitmask(self):
        if bool(self._hinfo):
            return self._hinfo[0].bitmask
        return None

    def string(self):
        display_type = BASE_NONE
        if bool(self._hfinfo):
            display_type = self._hfinfo[0].display

        c_str = fvalue_to_string_repr(None,
                                      byref(self._value),
                                      FTREPR_DISPLAY,
                                      self._hfinfo[0].display)
        if bool(c_str):
            s = cast(c_str, c_char_p).value.decode('utf-8')
            g_free(c_str)
            return s
        return None

    def __str__(self):
        s = self.string()
        if s == None:
            return ''
        return s
    
    @property
    def pyvalue(self):
        val = self._value
        if val == None:
            return None
        t = fvalue_type_ftenum(byref(self._value))
        if t == FT_NONE:
            return None
        elif t == FT_BYTES or t == FT_UINT_BYTES:
            byte_array = self._value.value.bytes
            return byte_array[0].data[:byte_array[0].len]
        elif t == FT_ABSOLUTE_TIME:
            time = cast(fvalue_get(byref(self._value)),
                        POINTER(nstime_t))
            ts = time[0].secs + (float(time[0].nsecs) / 1000000000.0)
            return datetime.fromtimestamp(ts)
        elif t == FT_RELATIVE_TIME:
            time = cast(fvalue_get(byref(self._value)),
                        POINTER(nstime_t))
            dur = time[0].secs + (float(time[0].nsecs) / 1000000000.0)
            return timedelta(seconds=dur)
        elif t == FT_CHAR:
            return bytes([fvalue_get_uinteger(byref(self._value))])
        elif t == FT_UINT8 or \
             t == FT_UINT16 or \
             t == FT_UINT24 or \
             t == FT_UINT32:
            return fvalue_get_uinteger(byref(self._value))
        elif t == FT_UINT40 or \
             t == FT_UINT48 or \
             t == FT_UINT56 or \
             t == FT_UINT64:
            return fvalue_get_uinteger64(byref(self._value))
        elif t == FT_INT8 or \
             t == FT_INT16 or \
             t == FT_INT24 or \
             t == FT_INT32:
            return fvalue_get_sinteger(byref(self._value))
        elif t == FT_INT40 or \
             t == FT_INT48 or \
             t == FT_INT56 or \
             t == FT_INT64:
            return fvalue_get_sinteger64(byref(self._value))
        elif t == FT_BOOLEAN:
            return bool(fvalue_get_uinteger64(byref(self._value)))
        elif t == FT_FLOAT or t == FT_DOUBLE:
            return fvalue_get_floating(byref(self._value))
        else:
            return self.string()

class ProtoNode:
    def __init__(self, node_ptr):
        self._node = node_ptr

    @property
    def parent(self):
        if bool(self._node[0].parent):
            return ProtoNode(self._node[0].parent)
        return None

    @property
    def children(self):
        return ProtoNodeIter(self._node[0].first_child)

    @property
    def _finfo(self):
        return self._node[0].finfo

    @property
    def _hfinfo(self):
        if bool(self._finfo):
            return self._finfo[0].hfinfo
        return None

    @property
    def _name(self):
        if bool(self._hfinfo):
            return self._hfinfo[0].name
        return None

    @property
    def _abbrev(self):
        if bool(self._hfinfo):
            return self._hfinfo[0].abbrev
        return None

    @property
    def _description(self):
        if bool(self._hfinfo):
            return self._hfinfo[0].blurb
        return None

    @property
    def _value(self):
        if bool(self._finfo):
            return self._finfo[0].value
        return None

    @property
    def name(self):
        if bool(self._name):
            return self._name.decode('utf-8')
        return None

    @property
    def abbrev(self):
        if bool(self._abbrev):
            return self._abbrev.decode('utf-8')
        return None

    @property
    def description(self):
        if bool(self._description):
            return self._description.decode('utf-8')
        return None

    @property
    def data(self):
        if bool(self._finfo) and bool(self._finfo[0].ds_tvb):
            ptr = tvb_get_ptr(self._finfo[0].ds_tvb,
                              self._finfo[0].start,
                              self._finfo[0].length)
            if bool(ptr):
                return bytes(ptr[:self._finfo[0].length])
        return None

    @property
    def data_start(self):
        if bool(self._finfo):
            return self._finfo[0].start
        return None

    @property
    def data_end(self):
        if bool(self._finfo):
            return self.data_start + self._finfo[0].length
        return None

    @property
    def appendix(self):
        if bool(self._finfo) and bool(self._finfo[0].ds_tvb):
            if self._finfo[0].appendix_length == 0:
                return []
            ptr = tvb_get_ptr(self._finfo[0].ds_tvb,
                              self._finfo[0].appendix_start,
                              self._finfo[0].appendix_length)
            if bool(ptr):
                return ptr[:self._finfo[0].appendix_length]
        return None

    @property
    def appendix_start(self):
        if bool(self._finfo):
            return self._finfo[0].appendix_start
        return None

    @property
    def appendix_end(self):
        if bool(self._finfo):
            return self.appendix_start + self._finfo[0].appendix_length
        return None

    @property
    def display(self):
        if bool(self._finfo) and bool(self._finfo[0].rep):
            return self._finfo[0].rep[0].representation.decode('utf-8')
        return None

    @property
    def value(self):
        val = self._value
        if val != None:
            return FieldValue(self._node, val)
        return None

    @property
    def next(self):
        if bool(self._node[0].next):
            return ProtoNode(self._node[0].next)
        return None

    @property
    def is_visible(self):
        return bool(self._node[0].tree_data) and self._node[0].tree_data[0].visible != 0
    
    @property
    def is_hidden(self):
        return bool(self._finfo) and (self._finfo[0].flags & FI_HIDDEN) == FI_HIDDEN

    def __iter__(self):
        return ProtoNodeIter(self._node)

    def __getitem__(self, key):
        key = c_char_p(key.encode('utf-8'))
        fallback = None
        for child in self.children:
            if bool(child._abbrev) and g_strcmp0(key, child._abbrev) == 0:
                return child
        for child in self.children:
            if bool(child._name) and g_strcmp0(key, child._name) == 0:
                return child
        raise TypeError

    def __contains__(self, key):
        key = c_char_p(key.encode('utf-8'))
        for child in self.children:
            if bool(child._abbrev) and g_strcmp0(key, child._abbrev) == 0:
                return True
        for child in self.children:
            if bool(child._name) and g_strcmp0(key, child._name) == 0:
                return True
        return False

    def __getattr__(self, name):
        return self[name]

    def _print(self, depth):
        if not self.is_visible or self.is_hidden:
            return
        tab = '  ' * depth
        if self.display != None:
            print('{}{}'.format(tab, self.display))
        elif self.value != None:
            if self.name != None:
                print('{}{}: {}'.format(tab, self.name, self.value))
            elif self.abbrev != None:
                print('{}{}: {}'.format(tab, self.abbrev, self.value))
            else:
                print('{}{}'.format(tab, node.value))
        else:
            depth -= 1
        for child in self.children:
            if child != None:
                child._print(depth + 1)

    def print(self):
        self._print(0)

    def _debug_print(self, depth):
        tab = '  ' * depth
        if self.value != None:
            if self.abbrev != None:
                print('{}{}: {}'.format(tab, self.abbrev, repr(self.value.pyvalue)))
            else:
                print('{}<unamed>: {}'.format(tab, repr(node.value.pyvalue)))
        else:
            depth -= 1
        for child in self.children:
            if child != None:
                child._debug_print(depth + 1)

    def debug_print(self):
        self._debug_print(0)
