#!/usr/bin/python3
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

from wspy import Protocol
from tabulate import tabulate

headers = ['ID', 'Name', 'Description', 'Filter Name', 'Enabled', 'Enabled By Default', 'Can Disable']
table = []
for proto in Protocol.all():
    table.append([proto.id,
                  proto.name,
                  proto.description,
                  proto.filter_name,
                  proto.is_enabled,
                  proto.is_enabled_by_default,
                  proto.can_disable])

print(tabulate(table, headers=headers))
