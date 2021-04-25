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

def tap_list():
    lst = get_tap_names()
    if not bool(lst):
        return []
    entry = g_list_first(lst)
    out = []
    while bool(entry):
        out.append(cast(entry[0].data, c_char_p).value.decode('utf-8'))
        entry = entry[0].next
    g_list_free(lst)
    return out

def reset_taps():
    reset_tap_listeners()


