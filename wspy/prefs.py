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

class _PrefsModuleCollector:
    def __init__(self):
        self._lst = []

    def __call__(self, mod_ptr, userdata):
        self._lst.append(PrefsModule(mod_ptr))
        return 0

    def get_prefs(self):
        return self._lst

class PrefsModule:
    def __init__(self, mod_ptr):
        self._mod = mod_ptr

    @staticmethod
    def all():
        foreach = _PrefsModuleCollector()
        prefs_modules_foreach(module_cb(foreach), 0)
        return foreach.get_prefs()

    @staticmethod
    def from_name(name):
        return PrefsModule(prefs_find_module(name.encode('utf-8')))

    @staticmethod
    def apply_all():
        prefs_apply_all()
    
    @property
    def name(self):
        if bool(self._mod[0].name):
            return self._mod[0].name.decode('utf-8')
        return None

    @property
    def title(self):
        if bool(self._mod[0].title):
            return self._mod[0].title.decode('utf-8')
        return None

    @property
    def description(self):
        if bool(self._mod[0].description):
            return self._mod[0].description.decode('utf-8')
        return None

    @property
    def parent(self):
        if bool(self._mod[0].parent):
            return PrefsModule(self._mod[0].parent)
        return None

    @property
    def submodules(self):
        foreach = _PrefsModuleCollector()
        prefs_modules_foreach_submodules(self._mod, module_cb(foreach), 0)
        return foreach.get_prefs()

    @property
    def prefs(self):
        if bool(self._mod[0].prefs):
            lst = []
            entry = g_list_first(self._mod[0].prefs)
            while bool(entry):
                lst.append(Preference(cast(entry[0].data, POINTER(pref_t))))
                entry = entry[0].next
            return lst
        return []

    def apply(self):
        prefs_apply(self._mod)

    def __getitem__(self, pref_name):
        p = c_void_p(prefs_find_preference(self._mod, pref_name.encode('utf-8')))
        if bool(p):
            return Preference(p)
        raise TypeError

    def __getattr__(self, pref_name):
        return self[pref_name]

class Preference:
    def __init__(self, pref_ptr):
        self._pref = pref_ptr

    @property
    def name(self):
        n = prefs_get_name(self._pref)
        if bool(n):
            return n.decode('utf-8')
        return None

    @property
    def title(self):
        t = prefs_get_title(self._pref)
        if bool(t):
            return t.decode('utf-8')
        return None

    @property
    def description(self):
        d = prefs_get_description(self._pref)
        if bool(d):
            return d.decode('utf-8')
        return None

    @property
    def is_obsolete(self):
        return (prefs_get_type(self._pref) & PREF_OBSOLETE) == PREF_OBSOLETE

    @property
    def enum_values(self):
        if prefs_get_type(self._pref) != PREF_ENUM:
            return None
        vals = prefs_get_enumvals(self._pref)
        lst = []
        i = 0
        while bool(vals[i].name):
            lst.append(vals[i].name.decode('utf-8'))
            i += 1
        return lst

    @property
    def type(self):
        t = prefs_get_type(self._pref) & ~PREF_OBSOLETE
        if t == PREF_UINT:
            return 'uint'
        elif t == PREF_BOOL:
            return 'bool'
        elif t == PREF_ENUM:
            return 'enum'
        elif t == PREF_STRING:
            return 'string'
        elif t == PREF_RANGE:
            return 'range'
        elif t == PREF_STATIC_TEXT:
            return 'static_text'
        elif t == PREF_UAT:
            return 'uat'
        elif t == PREF_SAVE_FILENAME:
            return 'save_filename'
        elif t == PREF_COLOR:
            return 'color'
        elif t == PREF_CUSTOM:
            return 'custom'
        elif t == PREF_DIRNAME:
            return 'dirname'
        elif t == PREF_DECODE_AS_UINT:
            return 'decode_as_uint'
        elif t == PREF_DECODE_AS_RANGE:
            return 'decode_as_range'
        elif t == PREF_OPEN_FILENAME:
            return 'open_filename'

    @property
    def _uint_value(self):
        return prefs_get_uint_value_real(self._pref, pref_current)

    @property
    def _bool_value(self):
        return prefs_get_bool_value(self._pref, pref_current) != 0

    @property
    def _enum_value(self):
        val = prefs_get_enum_value(self._pref, pref_current)
        vals = prefs_get_enumvals(self._pref)
        i = 0
        while bool(vals[i].name):
            if vals[i].value == val:
                return vals[i].name.decode('utf-8')
            i += 1
        return None

    @property
    def _string_value(self):
        val = prefs_get_string_value(self._pref, pref_current)
        if bool(val):
            return val.decode('utf-8')
        return ''

    @property
    def _range_value(self):
        # TODO
        raise WSError('PREF_RANGE is not yet supported')

    @property
    def _static_text_value(self):
        return None # no value for static text - title only

    @property
    def _uat_value(self):
        # TODO
        raise WSError('PREF_UAT is not yet supported')

    @property
    def _save_filename_value(self):
        return self._string_value
    
    @property
    def _color_value(self):
        # TODO
        raise WSError('PREF_COLOR is not yet supported')

    @property
    def _custom_value(self):
        # TODO
        raise WSError('PREF_CUSTOM is not yet supported')

    @property
    def _dirname_value(self):
        return self._string_value

    @property
    def _decode_as_uint_value(self):
        # TODO
        raise WSError('PREF_DECODE_AS_UINT is not yet supported')

    @property
    def _decode_as_range_value(self):
        # TODO
        raise WSError('PREF_DECODE_AS_RANGE is not yet supported')

    @property
    def _open_filename_value(self):
        return self._string_value

    @_uint_value.setter
    def _uint_value(self, value):
        prefs_set_uint_value(self._pref, value, pref_current)

    @_bool_value.setter
    def _bool_value(self, value):
        prefs_set_bool_value(self._pref, value, pref_current)

    @_enum_value.setter
    def _enum_value(self, value):
        val = c_char_p(value.encode('utf-8'))
        vals = prefs_get_enumvals(self._pref)
        i = 0
        while bool(vals[i].name):
            if g_strcmp0(vals[i].name, val):
                prefs_set_enum_value(self._pref, vals[i].value, pref_current)
                return
            i += 1
        raise WSError('Invalid enum value for preferece "{}": "{}"'.format(self.name, value))

    @_string_value.setter
    def _string_value(self, value):
        prefs_set_string_value(self._pref, value.encode('utf-8'), pref_current)

    @_range_value.setter
    def _range_value(self, value):
        # TODO
        raise WSError('PREF_RANGE is not yet supported')

    @_uat_value.setter
    def _uat_value(self, value):
        # TODO
        raise WSError('PREF_UAT is not yet supported')

    @_save_filename_value.setter
    def _save_filename_value(self, value):
        self._string_value = value
    
    @_color_value.setter
    def _color_value(self, value):
        # TODO
        raise WSError('PREF_COLOR is not yet supported')

    @_custom_value.setter
    def _custom_value(self, value):
        # TODO
        raise WSError('PREF_CUSTOM is not yet supported')

    @_dirname_value.setter
    def _dirname_value(self, value):
        self._string_value = value

    @_decode_as_uint_value.setter
    def _decode_as_uint_value(self, value):
        # TODO
        raise WSError('PREF_DECODE_AS_UINT is not yet supported')

    @_decode_as_range_value.setter
    def _decode_as_range_value(self, value):
        # TODO
        raise WSError('PREF_DECODE_AS_RANGE is not yet supported')

    @_open_filename_value.setter
    def _open_filename_value(self, value):
        self._string_value = value

    @property
    def value(self):
        t = prefs_get_type(self._pref) & ~PREF_OBSOLETE
        if t == PREF_UINT:
            return self._uint_value
        elif t == PREF_BOOL:
            return self._bool_value
        elif t == PREF_ENUM:
            return self._enum_value
        elif t == PREF_STRING:
            return self._string_value
        elif t == PREF_RANGE:
            return self._range_value
        elif t == PREF_STATIC_TEXT:
            return self._static_text_value
        elif t == PREF_UAT:
            return self._uat_value
        elif t == PREF_SAVE_FILENAME:
            return self._save_filename_value
        elif t == PREF_COLOR:
            return self._color_value
        elif t == PREF_CUSTOM:
            return self._custom_value
        elif t == PREF_DIRNAME:
            return self._dirname_value
        elif t == PREF_DECODE_AS_UINT:
            return self._decode_as_uint_value
        elif t == PREF_DECODE_AS_RANGE:
            return self._deocde_as_range_value
        elif t == PREF_OPEN_FILENAME:
            return self._open_filename_value

    @value.setter
    def value(self, value):
        t = prefs_get_type(self._pref) & ~PREF_OBSOLETE
        if t == PREF_UINT:
            self._uint_value = value
        elif t == PREF_BOOL:
            self._bool_value = value
        elif t == PREF_ENUM:
            self._enum_value = value
        elif t == PREF_STRING:
            self._string_value = value
        elif t == PREF_RANGE:
            self._range_value = value
        elif t == PREF_STATIC_TEXT:
            raise WSError('A static text preference has no value to set')
        elif t == PREF_UAT:
            self._uat_value = value
        elif t == PREF_SAVE_FILENAME:
            self._save_filename_value = value
        elif t == PREF_COLOR:
            self._color_value = value
        elif t == PREF_CUSTOM:
            self._custom_value = value
        elif t == PREF_DIRNAME:
            self._dirname_value = value
        elif t == PREF_DECODE_AS_UINT:
            self._decode_as_uint_value = value
        elif t == PREF_DECODE_AS_RANGE:
            self._deocde_as_range_value = value
        elif t == PREF_OPEN_FILENAME:
            self._open_filename_value = value

