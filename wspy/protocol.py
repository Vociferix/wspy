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

class Protocol:
    def __init__(self, protocol_ptr):
        self._proto = protocol_ptr

    @staticmethod
    def from_id(proto_id):
        proto = c_void_p(find_protocol_by_id(proto_id))
        if bool(proto):
            return Protocol(proto)
        return None

    @staticmethod
    def from_name(name):
        return Protocol.from_id(proto_get_id_by_short_name(name.encode('utf-8')))

    @staticmethod
    def from_filter_name(filter_name):
        return Protocol.from_id(proto_get_id_by_filter_name(filter_name.encode('utf-8')))

    @staticmethod
    def all():
        cookie = c_void_p(0)
        proto_id = proto_get_first_protocol(byref(cookie))
        protos = []
        while True:
            proto = Protocol.from_id(proto_id)
            if proto == None:
                break
            protos.append(proto)
            proto_id = proto_get_next_protocol(byref(cookie))
        return protos

    @staticmethod
    def table_by_name():
        cookie = c_void_p(0)
        proto_id = proto_get_first_protocol(byref(cookie))
        protos = {}
        while True:
            proto = Protocol.from_id(proto_id)
            if proto == None:
                break
            protos[proto.name] = proto
            proto_id = proto_get_next_protocol(byref(cookie))
        return protos

    @staticmethod
    def table_by_id():
        cookie = c_void_p(0)
        proto_id = proto_get_first_protocol(byref(cookie))
        protos = {}
        while True:
            proto = Protocol.from_id(proto_id)
            if proto == None:
                break
            protos[proto.id] = proto
            proto_id = proto_get_next_protocol(byref(cookie))
        return protos

    @staticmethod
    def table_by_filter_name():
        cookie = c_void_p(0)
        proto_id = proto_get_first_protocol(byref(cookie))
        protos = {}
        while True:
            proto = Protocol.from_id(proto_id)
            if proto == None:
                break
            protos[proto.filter_name] = proto
            proto_id = proto_get_next_protocol(byref(cookie))
        return protos

    @property
    def id(self):
        return proto_get_id(self._proto)

    @property
    def name(self):
        return proto_get_protocol_short_name(self._proto).decode('utf-8')

    @property
    def filter_name(self):
        return proto_get_protocol_filter_name(self.id).decode('utf-8')

    @property
    def description(self):
        return proto_get_protocol_long_name(self._proto).decode('utf-8')

    @property
    def is_enabled(self):
        return proto_is_protocol_enabled(self._proto) != 0

    @property
    def is_enabled_by_default(self):
        return proto_is_protocol_enabled_by_default(self._proto) != 0

    @property
    def can_disable(self):
        return proto_can_toggle_protocol(self.id) != 0

    def enable(self):
        if not self.is_enabled:
            proto_set_decoding(self.id, True)

    def disable(self):
        if self.is_enabled:
            if not self.can_disable:
                raise WSError('Protocol "{}" cannot be disabled'.format(self.name))
            proto_set_decoding(self.id, False)

    def __repr__(self):
        return 'Protocol(id={}, name={}, description={})'.format(self.id, repr(self.name), repr(self.description))
