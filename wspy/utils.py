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
import wspy.config as config
from wspy.errors import *

def make_type_list(argv):
    types = []
    for arg in argv:
        types.append(type(arg))
    return types

def ptr_add(ptr, offset, type_=None):
    ptr = cast(ptr, c_void_p)
    if type_ != None:
        offset *= sizeof(type_)
    else:
        type_ = None
    if ptr.value == None:
        ptr = c_void_p(offset)
    else:
        ptr = c_void_p(ptr.value + offset)
    return cast(ptr, POINTER(type_))

def ptraddress(ptr):
    return cast(ptr, c_void_p).value
