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
import os
from wspy import PrefsModule, Sniffer, Session

if len(sys.argv) < 3:
    print('Usage: {} <capture-file> <premaster-sercrets-log>'.format(sys.argv[0]))
    exit()

PrefsModule.from_name('tls').keylog_file.value = sys.argv[2]

sniffer = Sniffer(sys.argv[1])
session = Session(sniffer)

def print_data(data):
    data = data.decode('utf-8', 'backslashreplace').replace('\r', '')
    for line in data.splitlines():
        print('  {}'.format(line))

width = 80
try:
    width = os.get_terminal_size().columns
except:
    pass

first = True
for pkt in session:
    if 'tls' in pkt.proto_tree and ('http' in pkt.proto_tree or 'http2' in pkt.proto_tree):
        if first:
            first = False
            print('#' * width)
        print('Frame {}: {}->{}'.format(session.packet_count,
                                        pkt.proto_tree.ip['ip.src'].value.pyvalue,
                                        pkt.proto_tree.ip['ip.dst'].value.pyvalue))

        for node in pkt.proto_tree.tls.next:
            node.print()

        #if 'http' in pkt.proto_tree:
        #    print_data(pkt.proto_tree.http.data)
        #if 'http2' in pkt.proto_tree:
        #    pkt.proto_tree.http2.print()

        print('#' * width)
            
