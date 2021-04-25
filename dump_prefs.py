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
from wspy import PrefsModule

visited = {}

not_supported = ['range', 'uat', 'color', 'custom', 'decode_as_uint', 'decode_as_range']

def print_preference(pref, depth):
    tab = '  ' * depth
    header = '{}: '.format(pref.name)
    if pref.type in not_supported:
        print('{}{}PREF_{} preferences are not yet supported'.format(tab,
                                                                     header,
                                                                     pref.type.upper()))
    elif pref.type == 'enum':
        val = pref.value
        vals = pref.enum_values
        if val == vals[0]:
            print('{}{}* {}'.format(tab, header, repr(vals[0])))
        else:
            print('{}{}  {}'.format(tab, header, repr(vals[0])))
        space = ' ' * len(header)
        for opt in vals[1:]:
            if val == opt:
                print('{}{}* {}'.format(tab, space, repr(opt)))
            else:
                print('{}{}  {}'.format(tab, space, repr(opt)))
    elif pref.type != 'static_text':
        print('{}{}{}'.format(tab, header, repr(pref.value)))

def print_module(module, depth=0):
    tab = '  ' * depth
    if module.name in visited:
        return
        print('{}{}: (See reference above)'.format(tab, module.name))
    elif depth != 0 and module.name != None and PrefsModule.from_name(module.name) != None:
        return
        print('{}{}: (See reference below)'.format(tab, module.name))
    else:
        visited[module.name] = True
        print('{}{}:'.format(tab, module.name))
        for submodule in module.submodules:
            print_module(submodule, depth + 1)
        for pref in module.prefs:
            print_preference(pref, depth + 1)

if len(sys.argv) > 1:
    mods = sys.argv[1].split(',')
    if not 'all' in mods:
        for module in mods:
            print_module(PrefsModule.from_name(module))
        exit()

for module in PrefsModule.all():
    print_module(module)
