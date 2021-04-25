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
from wspy.libwireshark import *
from wspy.errors import *

class Column:
    def __init__(self, col_item):
        self._col_item = col_item

    @property
    def title(self):
        return self._col_item.col_title.decode('utf-8')

    @property
    def data(self):
        return self._col_item.col_data.decode('utf-8')

class ColumnList:
    def __init__(self, cinfo_ptr, begin=None, end=None):
        self._cinfo = cinfo_ptr
        if begin == None:
            self._begin = 0
        else:
            self._begin = begin
        if end == None:
            self._end = self._cinfo[0].num_cols

    def __len__(self):
        return self._end - self._begin

    def __getitem__(self, key):
        if isinstance(key, int):
            l = len(self)
            if key < 0:
                key = l + key
            if key < 0 or key >= l:
                raise IndexError
            return Column(self._cinfo[0].columns[self._begin + key])
        elif isinstance(key, str):
            for i in range(self._begin, self._end):
                if self._cinfo[0].columns[i].col_title.decode('utf-8') == key:
                    return Column(self._cinfo[0].columns[i])
        raise TypeError

    def __getslice__(self, begin, end):
        l = len(self)
        if begin == None:
            begin = self._begin
        elif begin < 0:
            begin = self._end + begin
        else:
            begin = self._begin + begin
        if begin < 0 or begin >= l:
            raise IndexError

        if end == None:
            end = self._end
        elif end < 0:
            end = self._end + end
        else:
            end = self._begin + end
        if end < 0 or begin >= l or end < begin:
            raise IndexError

        return ColumnList(self._cinfo, begin, end)

    def __contains__(self, title):
        for i in range(self._begin, self._end):
            if self._cinfo[0].columns[i].col_title.decode('utf-8') == title:
                return True
        return False
