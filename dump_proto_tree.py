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

import sys
from wspy import Sniffer, Session

if len(sys.argv) < 2:
    print('Usage: {} <capture-file>'.format(sys.argv[0]))
    exit()

sniffer = Sniffer(sys.argv[1])
session = Session(sniffer)

def print_tree(node, depth=0):
    if node == None:
        return
    tab = '  ' * depth
    if node.value != None:
        _ = node.value.pyvalue
    if node.display != None:
        print('{}{}'.format(tab, node.display))
    elif node.value != None:
        if node.name != None:
            print('{}{}: {}'.format(tab, node.name, node.value))
        elif node.abbrev != None:
            print('{}{}: {}'.format(tab, node.abbrev, node.value))
        else:
            print('{}{}'.format(tab, node.value))
    else:
        depth -= 1
    for child in node.children:
        print_tree(child, depth + 1)

print('##############################################################################################')
for pkt in session:
    print_tree(pkt.proto_tree)
    print('##############################################################################################')
