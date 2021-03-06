###########################################################################
# wspy: Python wrapper around libwireshark                                #
# Copyright (C) 2020  Jack A Bernard Jr.                                  #
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


class LibGLib2:
    gboolean = c_int
    gchar = c_char
    gchar_p = c_char_p
    guchar = c_uint8
    guchar_p = POINTER(guchar)
    guint = c_uint
    guint8 = c_uint8
    guint16 = c_uint16
    guint32 = c_uint32
    guint64 = c_uint64
    gint = c_int
    gint8 = c_int8
    gint16 = c_int16
    gint32 = c_int32
    gint64 = c_int64
    gsize = c_size_t
    gssize = c_ssize_t
    gfloat = c_float
    gdouble = c_double
    gunichar = guint32

    gpointer = c_void_p
    gconstpointer = c_void_p

    GQuark = guint32
    GPid = c_int

    GCompareFunc = CFUNCTYPE(gint, gconstpointer, gconstpointer)
    GFunc = CFUNCTYPE(None, gpointer, gpointer)
    GHFunc = CFUNCTYPE(None, gpointer, gpointer, gpointer)
    GHashFunc = CFUNCTYPE(guint, gconstpointer)
    GEqualFunc = CFUNCTYPE(gboolean, gconstpointer, gconstpointer)

    # struct GString {
    #     gchar* str;
    #     gsize len;
    #     gsize allocated_len;
    # };

    class GString(Structure):
        pass

    GString._fields_ = [('str', gchar),
                        ('len', gsize),
                        ('allocated_len', gsize)]

    # typedef struct _GHashTable GHashTable

    class _GHashTable(Structure):
        _fields_ = []

    GHashTable = _GHashTable

    # struct GList {
    #     gpointer data;
    #     GList* next;
    #     GList* prev;
    # };

    class GList(Structure):
        pass

    GList._fields_ = [('data', gpointer),
                      ('next', POINTER(GList)),
                      ('prev', POINTER(GList))]

    # struct GError {
    #     GQuark domain;
    #     gint code;
    #     gchar* message;
    # };

    class GError(Structure):
        pass

    GError_fields_ = [('domain', GQuark),
                      ('code', gint),
                      ('message', gchar_p)]

    # struct GPtrArray {
    #     gpointer* pdata;
    #     guint     len;
    # };

    class GPtrArray(Structure):
        pass

    GPtrArray._fields_ = [('pdata', POINTER(gpointer)), ('len', guint)]

    # struct GArray {
    #     gchar* data;
    #     guint  len;
    # };

    class GArray(Structure):
        pass

    GArray._fields_ = [('data', gchar_p), ('len', guint)]

    # struct GSList {
    #     gpointer data;
    #     GSList*  next;
    # };

    class GSList(Structure):
        pass

    GSList._fields_ = [('data', gpointer), ('next', POINTER(GSList))]

    # struct GByteArray {
    #     guint8 *data;
    #     guint   len;
    # };

    class GByteArray(Structure):
        pass

    GByteArray._fields_ = [('data', POINTER(guint8)),
                           ('len', guint)]

    # typedef struct _GRegex GRegex;

    class _GRegex(Structure):
        _fields_ = []

    GRegex = _GRegex

    # typedef struct _GMatchInfo GMatchInfo;

    class _GMatchInfo(Structure):
        _fields_ = []

    GMatchInfo = _GMatchInfo
