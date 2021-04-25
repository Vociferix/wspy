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

import os
from os import environ
from ctypes.util import find_library
from wspy.errors import LibNotFound


def set_libdir(path):
    environ['WSPY_LIBDIR'] = path


def get_libdir():
    return environ.get('WSPY_LIBDIR')


def _get_lib(name, var=None):
    if var is None:
        var = 'WSPY_LIB{}'.format(name.upper())

    if var not in environ:
        libdir = get_libdir()
        if libdir is not None:
            if os.name == 'nt':
                path = os.path.join(libdir, '{}.dll'.format(name))
                if not os.path.exists(path):
                    path = os.path.join(libdir, 'lib{}.dll'.format(name))
                    if not os.path.exists(path):
                        path = find_library(name)
            else:
                path = os.path.join(libdir, '{}.so'.format(name))
                if not os.path.exists(path):
                    path = os.path.join(libdir, 'lib{}.so'.format(name))
                    if not os.path.exists(path):
                        path = find_library(name)
        else:
            path = find_library(name)
    else:
        path = environ.get(var)

    if path is None:
        raise LibNotFound(name)

    return path


def set_libwireshark(path):
    environ['WSPY_LIBWIRESHARK'] = path


def get_libwireshark():
    return _get_lib('wireshark')


def set_libwiretap(path):
    environ['WSPY_LIBWIRETAP'] = path


def get_libwiretap():
    return _get_lib('wiretap')


def set_libwsutil(path):
    environ['WSPY_LIBWSUTIL'] = path


def get_libwsutil():
    return _get_lib('wsutil')


def set_libglib(path):
    environ['WSPY_LIBGLIB'] = path


def get_libglib():
    try:
        return _get_lib('glib')
    except:
        return _get_lib('glib-2.0', 'WSPY_LIBGLIB')
