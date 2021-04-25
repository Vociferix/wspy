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
from wspy.utils import make_type_list
from wspy.errors import *

libglib = CDLL(config.get_libglib())

gboolean = c_int
gchar = c_char
gchar_p = c_char_p
guchar = c_uint8
guchar_p = POINTER(guchar)
gushort = c_ushort
guint = c_uint
gulong = c_ulong
guint8 = c_uint8
guint16 = c_uint16
guint32 = c_uint32
guint64 = c_uint64
gshort = c_short
gint = c_int
glong = c_long
gint8 = c_int8
gint16 = c_int16
gint32 = c_int32
gint64 = c_int64
gsize = c_size_t
gssize = c_ssize_t
gfloat = c_float
gdouble = c_double
gunichar = guint32
gunichar_p = POINTER(gunichar)
gunichar2 = guint16
gunichar2_p = POINTER(gunichar2)

gpointer = c_void_p
gconstpointer = c_void_p

GQuark = guint32
GPid = c_int

class GString(Structure):
    _fields_ = [('str', gchar_p),
                ('len', gsize),
                ('allocated_len', gsize)]

class GHashTable(Structure):
    _fields_ = []

class GHashTableIter(Structure):
    _fields_ = []

class GList(Structure):
    pass

GList._fields_ = [('data', gpointer),
                  ('next', POINTER(GList)),
                  ('prev', POINTER(GList))]

class GError(Structure):
    _fields_ = [('domain', GQuark),
                ('code', gint),
                ('message', gchar_p)]

class GPtrArray(Structure):
    _fields_ = [('pdata', POINTER(gpointer)),
                ('len', guint)]

class GArray(Structure):
    _fields_ = [('data', gchar_p),
                ('len', guint)]

class GSList(Structure):
    pass

GSList._fields_ = [('data', gpointer),
                   ('next', POINTER(GSList))]

class GByteArray(Structure):
    _fields_ = [('data', POINTER(guint8)),
                ('len', guint)]

class GRegex(Structure):
    _fields_ = []

class GMatchInfo(Structure):
    _fields_ = []

class GTree(Structure):
    _fields_ = []

class GBytes(Structure):
    _fields_ = []

class GQueue(Structure):
    _fields_ = [('head', POINTER(GList)),
                ('tail', POINTER(GList)),
                ('length', guint)]

class GMemVTable(Structure):
    _fields_ = [('malloc', CFUNCTYPE(gpointer, gsize)),
                ('realloc', CFUNCTYPE(gpointer, gpointer, gsize)),
                ('free', CFUNCTYPE(None, gpointer)),
                ('calloc', CFUNCTYPE(gpointer, gsize, gsize)),
                ('try_malloc', CFUNCTYPE(gpointer, gsize)),
                ('try_realloc', CFUNCTYPE(gpointer, gpointer, gsize))]

class _GIConv(Structure):
    _fields_ = []

GIConv = POINTER(_GIConv)

GCompareFunc = CFUNCTYPE(gint, gconstpointer, gconstpointer)
GCompareDataFunc = CFUNCTYPE(gint, gconstpointer, gconstpointer, gpointer)
GFunc = CFUNCTYPE(None, gpointer, gpointer)
GHFunc = CFUNCTYPE(None, gpointer, gpointer, gpointer)
GHRFunc = CFUNCTYPE(gboolean, gpointer, gpointer, gpointer)
GHashFunc = CFUNCTYPE(guint, gconstpointer)
GEqualFunc = CFUNCTYPE(gboolean, gconstpointer, gconstpointer)
GDestroyNotify = CFUNCTYPE(None, gpointer)
GCopyFunc = CFUNCTYPE(gpointer, gconstpointer, gpointer)
GRegexEvalCallback = CFUNCTYPE(gboolean,
                               POINTER(GMatchInfo),
                               POINTER(GString),
                               gpointer)
GTraverseFunc = CFUNCTYPE(gboolean, gpointer, gpointer, gpointer)

# typedef enum { /* TODO */ } GUnicodeType
GUnicodeType = c_int

# typedef enum { /* TODO */ } GUnicodeBreakType
GUnicodeBreakType = c_int

# typedef enum { /* TODO */ } GUnicodeScript
GUnicodeScript = c_int

# typedef enum { /* TODO */ } GNormalizeMode
GNormalizeMode = c_int

# typedef enum
# {
#   G_LOG_FLAG_RECURSION          = 1 << 0,
#   G_LOG_FLAG_FATAL              = 1 << 1,
#   G_LOG_LEVEL_ERROR             = 1 << 2,
#   G_LOG_LEVEL_CRITICAL          = 1 << 3,
#   G_LOG_LEVEL_WARNING           = 1 << 4,
#   G_LOG_LEVEL_MESSAGE           = 1 << 5,
#   G_LOG_LEVEL_INFO              = 1 << 6,
#   G_LOG_LEVEL_DEBUG             = 1 << 7,
#   G_LOG_LEVEL_MASK              = ~(G_LOG_FLAG_RECURSION | G_LOG_FLAG_FATAL)
# } GLogLevelFlags;
GLogLevelFlags = c_int
G_LOG_FLAG_RECURSION = 1 << 0
G_LOG_FLAG_FATAL = 1 << 1
G_LOG_LEVEL_ERROR = 1 << 2
G_LOG_LEVEL_CRITICAL = 1 << 3
G_LOG_LEVEL_WARNING = 1 << 4
G_LOG_LEVEL_MESSAGE = 1 << 5
G_LOG_LEVEL_INFO = 1 << 6
G_LOG_LEVEL_DEBUG = 1 << 7
G_LOG_LEVEL_MASK = ~(G_LOG_FLAG_RECURSION | G_LOG_FLAG_FATAL)

# typedef enum
# {
#   G_REGEX_ERROR_COMPILE,
#   G_REGEX_ERROR_OPTIMIZE,
#   G_REGEX_ERROR_REPLACE,
#   G_REGEX_ERROR_MATCH,
#   G_REGEX_ERROR_INTERNAL,
#   G_REGEX_ERROR_STRAY_BACKSLASH = 101,
#   G_REGEX_ERROR_MISSING_CONTROL_CHAR = 102,
#   G_REGEX_ERROR_UNRECOGNIZED_ESCAPE = 103,
#   G_REGEX_ERROR_QUANTIFIERS_OUT_OF_ORDER = 104,
#   G_REGEX_ERROR_QUANTIFIER_TOO_BIG = 105,
#   G_REGEX_ERROR_UNTERMINATED_CHARACTER_CLASS = 106,
#   G_REGEX_ERROR_INVALID_ESCAPE_IN_CHARACTER_CLASS = 107,
#   G_REGEX_ERROR_RANGE_OUT_OF_ORDER = 108,
#   G_REGEX_ERROR_NOTHING_TO_REPEAT = 109,
#   G_REGEX_ERROR_UNRECOGNIZED_CHARACTER = 112,
#   G_REGEX_ERROR_POSIX_NAMED_CLASS_OUTSIDE_CLASS = 113,
#   G_REGEX_ERROR_UNMATCHED_PARENTHESIS = 114,
#   G_REGEX_ERROR_INEXISTENT_SUBPATTERN_REFERENCE = 115,
#   G_REGEX_ERROR_UNTERMINATED_COMMENT = 118,
#   G_REGEX_ERROR_EXPRESSION_TOO_LARGE = 120,
#   G_REGEX_ERROR_MEMORY_ERROR = 121,
#   G_REGEX_ERROR_VARIABLE_LENGTH_LOOKBEHIND = 125,
#   G_REGEX_ERROR_MALFORMED_CONDITION = 126,
#   G_REGEX_ERROR_TOO_MANY_CONDITIONAL_BRANCHES = 127,
#   G_REGEX_ERROR_ASSERTION_EXPECTED = 128,
#   G_REGEX_ERROR_UNKNOWN_POSIX_CLASS_NAME = 130,
#   G_REGEX_ERROR_POSIX_COLLATING_ELEMENTS_NOT_SUPPORTED = 131,
#   G_REGEX_ERROR_HEX_CODE_TOO_LARGE = 134,
#   G_REGEX_ERROR_INVALID_CONDITION = 135,
#   G_REGEX_ERROR_SINGLE_BYTE_MATCH_IN_LOOKBEHIND = 136,
#   G_REGEX_ERROR_INFINITE_LOOP = 140,
#   G_REGEX_ERROR_MISSING_SUBPATTERN_NAME_TERMINATOR = 142,
#   G_REGEX_ERROR_DUPLICATE_SUBPATTERN_NAME = 143,
#   G_REGEX_ERROR_MALFORMED_PROPERTY = 146,
#   G_REGEX_ERROR_UNKNOWN_PROPERTY = 147,
#   G_REGEX_ERROR_SUBPATTERN_NAME_TOO_LONG = 148,
#   G_REGEX_ERROR_TOO_MANY_SUBPATTERNS = 149,
#   G_REGEX_ERROR_INVALID_OCTAL_VALUE = 151,
#   G_REGEX_ERROR_TOO_MANY_BRANCHES_IN_DEFINE = 154,
#   G_REGEX_ERROR_DEFINE_REPETION = 155,
#   G_REGEX_ERROR_INCONSISTENT_NEWLINE_OPTIONS = 156,
#   G_REGEX_ERROR_MISSING_BACK_REFERENCE = 157,
#   G_REGEX_ERROR_INVALID_RELATIVE_REFERENCE = 158,
#   G_REGEX_ERROR_BACKTRACKING_CONTROL_VERB_ARGUMENT_FORBIDDEN = 159,
#   G_REGEX_ERROR_UNKNOWN_BACKTRACKING_CONTROL_VERB  = 160,
#   G_REGEX_ERROR_NUMBER_TOO_BIG = 161,
#   G_REGEX_ERROR_MISSING_SUBPATTERN_NAME = 162,
#   G_REGEX_ERROR_MISSING_DIGIT = 163,
#   G_REGEX_ERROR_INVALID_DATA_CHARACTER = 164,
#   G_REGEX_ERROR_EXTRA_SUBPATTERN_NAME = 165,
#   G_REGEX_ERROR_BACKTRACKING_CONTROL_VERB_ARGUMENT_REQUIRED = 166,
#   G_REGEX_ERROR_INVALID_CONTROL_CHAR = 168,
#   G_REGEX_ERROR_MISSING_NAME = 169,
#   G_REGEX_ERROR_NOT_SUPPORTED_IN_CLASS = 171,
#   G_REGEX_ERROR_TOO_MANY_FORWARD_REFERENCES = 172,
#   G_REGEX_ERROR_NAME_TOO_LONG = 175,
#   G_REGEX_ERROR_CHARACTER_VALUE_TOO_LARGE = 176
# } GRegexError;
GRegexError = c_int
G_REGEX_ERROR_COMPILE = 0
G_REGEX_ERROR_OPTIMIZE = 1
G_REGEX_ERROR_REPLACE = 2
G_REGEX_ERROR_MATCH = 3
G_REGEX_ERROR_INTERNAL = 4
G_REGEX_ERROR_STRAY_BACKSLASH = 101
G_REGEX_ERROR_MISSING_CONTROL_CHAR = 102
G_REGEX_ERROR_UNRECOGNIZED_ESCAPE = 103
G_REGEX_ERROR_QUANTIFIERS_OUT_OF_ORDER = 104
G_REGEX_ERROR_QUANTIFIER_TOO_BIG = 105
G_REGEX_ERROR_UNTERMINATED_CHARACTER_CLASS = 106
G_REGEX_ERROR_INVALID_ESCAPE_IN_CHARACTER_CLASS = 107
G_REGEX_ERROR_RANGE_OUT_OF_ORDER = 108
G_REGEX_ERROR_NOTHING_TO_REPEAT = 109
G_REGEX_ERROR_UNRECOGNIZED_CHARACTER = 112
G_REGEX_ERROR_POSIX_NAMED_CLASS_OUTSIDE_CLASS = 113
G_REGEX_ERROR_UNMATCHED_PARENTHESIS = 114
G_REGEX_ERROR_INEXISTENT_SUBPATTERN_REFERENCE = 115
G_REGEX_ERROR_UNTERMINATED_COMMENT = 118
G_REGEX_ERROR_EXPRESSION_TOO_LARGE = 120
G_REGEX_ERROR_MEMORY_ERROR = 121
G_REGEX_ERROR_VARIABLE_LENGTH_LOOKBEHIND = 125
G_REGEX_ERROR_MALFORMED_CONDITION = 126
G_REGEX_ERROR_TOO_MANY_CONDITIONAL_BRANCHES = 127
G_REGEX_ERROR_ASSERTION_EXPECTED = 128
G_REGEX_ERROR_UNKNOWN_POSIX_CLASS_NAME = 130
G_REGEX_ERROR_POSIX_COLLATING_ELEMENTS_NOT_SUPPORTED = 131
G_REGEX_ERROR_HEX_CODE_TOO_LARGE = 134
G_REGEX_ERROR_INVALID_CONDITION = 135
G_REGEX_ERROR_SINGLE_BYTE_MATCH_IN_LOOKBEHIND = 136
G_REGEX_ERROR_INFINITE_LOOP = 140
G_REGEX_ERROR_MISSING_SUBPATTERN_NAME_TERMINATOR = 142
G_REGEX_ERROR_DUPLICATE_SUBPATTERN_NAME = 143
G_REGEX_ERROR_MALFORMED_PROPERTY = 146
G_REGEX_ERROR_UNKNOWN_PROPERTY = 147
G_REGEX_ERROR_SUBPATTERN_NAME_TOO_LONG = 148
G_REGEX_ERROR_TOO_MANY_SUBPATTERNS = 149
G_REGEX_ERROR_INVALID_OCTAL_VALUE = 151
G_REGEX_ERROR_TOO_MANY_BRANCHES_IN_DEFINE = 154
G_REGEX_ERROR_DEFINE_REPETION = 155
G_REGEX_ERROR_INCONSISTENT_NEWLINE_OPTIONS = 156
G_REGEX_ERROR_MISSING_BACK_REFERENCE = 157
G_REGEX_ERROR_INVALID_RELATIVE_REFERENCE = 158
G_REGEX_ERROR_BACKTRACKING_CONTROL_VERB_ARGUMENT_FORBIDDEN = 159
G_REGEX_ERROR_UNKNOWN_BACKTRACKING_CONTROL_VERB  = 160
G_REGEX_ERROR_NUMBER_TOO_BIG = 161
G_REGEX_ERROR_MISSING_SUBPATTERN_NAME = 162
G_REGEX_ERROR_MISSING_DIGIT = 163
G_REGEX_ERROR_INVALID_DATA_CHARACTER = 164
G_REGEX_ERROR_EXTRA_SUBPATTERN_NAME = 165
G_REGEX_ERROR_BACKTRACKING_CONTROL_VERB_ARGUMENT_REQUIRED = 166
G_REGEX_ERROR_INVALID_CONTROL_CHAR = 168
G_REGEX_ERROR_MISSING_NAME = 169
G_REGEX_ERROR_NOT_SUPPORTED_IN_CLASS = 171
G_REGEX_ERROR_TOO_MANY_FORWARD_REFERENCES = 172
G_REGEX_ERROR_NAME_TOO_LONG = 175
G_REGEX_ERROR_CHARACTER_VALUE_TOO_LARGE = 176

# typedef enum
# {
#   G_REGEX_CASELESS          = 1 << 0,
#   G_REGEX_MULTILINE         = 1 << 1,
#   G_REGEX_DOTALL            = 1 << 2,
#   G_REGEX_EXTENDED          = 1 << 3,
#   G_REGEX_ANCHORED          = 1 << 4,
#   G_REGEX_DOLLAR_ENDONLY    = 1 << 5,
#   G_REGEX_UNGREEDY          = 1 << 9,
#   G_REGEX_RAW               = 1 << 11,
#   G_REGEX_NO_AUTO_CAPTURE   = 1 << 12,
#   G_REGEX_OPTIMIZE          = 1 << 13,
#   G_REGEX_FIRSTLINE         = 1 << 18,
#   G_REGEX_DUPNAMES          = 1 << 19,
#   G_REGEX_NEWLINE_CR        = 1 << 20,
#   G_REGEX_NEWLINE_LF        = 1 << 21,
#   G_REGEX_NEWLINE_CRLF      = G_REGEX_NEWLINE_CR | G_REGEX_NEWLINE_LF,
#   G_REGEX_NEWLINE_ANYCRLF   = G_REGEX_NEWLINE_CR | 1 << 22,
#   G_REGEX_BSR_ANYCRLF       = 1 << 23,
#   G_REGEX_JAVASCRIPT_COMPAT = 1 << 25
# } GRegexCompileFlags;
GRegexCompileFlags = c_int
G_REGEX_CASELESS = 1 << 0
G_REGEX_MULTILINE = 1 << 1
G_REGEX_DOTALL = 1 << 2
G_REGEX_EXTENDED = 1 << 3
G_REGEX_ANCHORED = 1 << 4
G_REGEX_DOLLAR_ENDONLY = 1 << 5
G_REGEX_UNGREEDY = 1 << 9
G_REGEX_RAW = 1 << 11
G_REGEX_NO_AUTO_CAPTURE = 1 << 12
G_REGEX_OPTIMIZE = 1 << 13
G_REGEX_FIRSTLINE = 1 << 18
G_REGEX_DUPNAMES = 1 << 19
G_REGEX_NEWLINE_CR = 1 << 20
G_REGEX_NEWLINE_LF = 1 << 21
G_REGEX_NEWLINE_CRLF = G_REGEX_NEWLINE_CR | G_REGEX_NEWLINE_LF
G_REGEX_NEWLINE_ANYCRLF = G_REGEX_NEWLINE_CR | 1 << 22
G_REGEX_BSR_ANYCRLF = 1 << 23
G_REGEX_JAVASCRIPT_COMPAT = 1 << 25

# typedef enum
# {
#   G_REGEX_MATCH_ANCHORED         = 1 << 4,
#   G_REGEX_MATCH_NOTBOL           = 1 << 7,
#   G_REGEX_MATCH_NOTEOL           = 1 << 8,
#   G_REGEX_MATCH_NOTEMPTY         = 1 << 10,
#   G_REGEX_MATCH_PARTIAL          = 1 << 15,
#   G_REGEX_MATCH_NEWLINE_CR       = 1 << 20,
#   G_REGEX_MATCH_NEWLINE_LF       = 1 << 21,
#   G_REGEX_MATCH_NEWLINE_CRLF     = G_REGEX_MATCH_NEWLINE_CR | G_REGEX_MATCH_NEWLINE_LF,
#   G_REGEX_MATCH_NEWLINE_ANY      = 1 << 22,
#   G_REGEX_MATCH_NEWLINE_ANYCRLF  = G_REGEX_MATCH_NEWLINE_CR | G_REGEX_MATCH_NEWLINE_ANY,
#   G_REGEX_MATCH_BSR_ANYCRLF      = 1 << 23,
#   G_REGEX_MATCH_BSR_ANY          = 1 << 24,
#   G_REGEX_MATCH_PARTIAL_SOFT     = G_REGEX_MATCH_PARTIAL,
#   G_REGEX_MATCH_PARTIAL_HARD     = 1 << 27,
#   G_REGEX_MATCH_NOTEMPTY_ATSTART = 1 << 28
# } GRegexMatchFlags;
GRegexMatchFlags = c_int
G_REGEX_MATCH_ANCHORED = 1 << 4
G_REGEX_MATCH_NOTBOL = 1 << 7
G_REGEX_MATCH_NOTEOL = 1 << 8
G_REGEX_MATCH_NOTEMPTY = 1 << 10
G_REGEX_MATCH_PARTIAL = 1 << 15
G_REGEX_MATCH_NEWLINE_CR = 1 << 20
G_REGEX_MATCH_NEWLINE_LF = 1 << 21
G_REGEX_MATCH_NEWLINE_CRLF = G_REGEX_MATCH_NEWLINE_CR | G_REGEX_MATCH_NEWLINE_LF
G_REGEX_MATCH_NEWLINE_ANY = 1 << 22
G_REGEX_MATCH_NEWLINE_ANYCRLF = G_REGEX_MATCH_NEWLINE_CR | G_REGEX_MATCH_NEWLINE_ANY
G_REGEX_MATCH_BSR_ANYCRLF = 1 << 23
G_REGEX_MATCH_BSR_ANY = 1 << 24
G_REGEX_MATCH_PARTIAL_SOFT = G_REGEX_MATCH_PARTIAL
G_REGEX_MATCH_PARTIAL_HARD = 1 << 27
G_REGEX_MATCH_NOTEMPTY_ATSTART = 1 << 28

# typedef enum
# {
#   G_TRAVERSE_LEAVES     = 1 << 0,
#   G_TRAVERSE_NON_LEAVES = 1 << 1,
#   G_TRAVERSE_ALL        = G_TRAVERSE_LEAVES | G_TRAVERSE_NON_LEAVES,
#   G_TRAVERSE_MASK       = 0x03,
#   G_TRAVERSE_LEAFS      = G_TRAVERSE_LEAVES,
#   G_TRAVERSE_NON_LEAFS  = G_TRAVERSE_NON_LEAVES
# } GTraverseFlags;
GTraverseFlags = c_int
G_TRAVERSE_LEAVES = 1 << 0
G_TRAVERSE_NON_LEAVES = 1 << 1
G_TRAVERSE_ALL = G_TRAVERSE_LEAVES | G_TRAVERSE_NON_LEAVES
G_TRAVERSE_MASK = 0x03
G_TRAVERSE_LEAFS = G_TRAVERSE_LEAVES
G_TRAVERSE_NON_LEAFS = G_TRAVERSE_NON_LEAVES

# typedef enum
# {
#   G_IN_ORDER,
#   G_PRE_ORDER,
#   G_POST_ORDER,
#   G_LEVEL_ORDER
# } GTraverseType;
GTraverseType = c_int
G_IN_ORDER = 0
G_PRE_ORDER = 1
G_POST_ORDER = 2
G_LEVEL_ORDER = 3

# GString* g_string_new(const gchar* init);
g_string_new = libglib.g_string_new
g_string_new.restype = POINTER(GString)
g_string_new.argtypes = [gchar_p]

# GString* g_string_new_len(const gchar* init, gssize len);
g_string_new_len = libglib.g_string_new_len
g_string_new_len.restype = POINTER(GString)
g_string_new_len.argtypes = [gchar_p, gssize]

# GString* g_string_sized_new(gsize dfl_size);
g_string_sized_new = libglib.g_string_sized_new
g_string_sized_new.restype = POINTER(GString)
g_string_sized_new.argtypes = [gsize]

# GString* g_string_assign(GString* string, const gchar* rval);
g_string_assign = libglib.g_string_assign
g_string_assign.restype = POINTER(GString)
g_string_assign.argtypes = [POINTER(GString), gchar_p]

# void g_string_printf(GString* string, const gchar* format, ...);
_g_string_printf = libglib.g_string_printf
_g_string_printf.restype = None

def g_string_printf(string, fmt, *args):
    _g_string_printf.argtypes = [POINTER(GString),
                                      gchar_p] + make_type_list(args)
    _g_string_printf(string, fmt, *args)

# void g_string_append_printf(GString* string, const gchar* format, ...);
_g_string_append_printf = libglib.g_string_append_printf
_g_string_append_printf.restype = None

def g_string_append_printf(string, fmt, *args):
    _g_string_append_printf.argtypes = [POINTER(GString),
                                             gchar_p] + make_type_list(args)
    _g_string_append_printf(string, fmt, *args)

# GString* g_string_append(GString* string, const gchar* val);
g_string_append = libglib.g_string_append
g_string_append.restype = POINTER(GString)
g_string_append.argtypes = [POINTER(GString), gchar_p]

# GString* g_string_append_c(GString* string, gchar c);
g_string_append_c = libglib.g_string_append_c
g_string_append_c.restype = POINTER(GString)
g_string_append_c.argtypes = [POINTER(GString), gchar]

# GString* g_string_append_unichar(GString* string, gunichar wc);
g_string_append_unichar = libglib.g_string_append_unichar
g_string_append_unichar.restype = POINTER(GString)
g_string_append_unichar.argtypes = [POINTER(GString), gunichar]

# GString* g_string_append_len(GString* string, const gchar* val, gssize len);
g_string_append_len = libglib.g_string_append_len
g_string_append_len.restype = POINTER(GString)
g_string_append_len.argtypes = [POINTER(GString), gchar_p, gssize]

# GString* g_string_append_uri_escaped(GString* string,
#                                      const gchar* unescaped,
#                                      const gchar* reserved_chars_allowed,
#                                      gboolean allow_utf8);
g_string_append_uri_escaped = libglib.g_string_append_uri_escaped
g_string_append_uri_escaped.restype = POINTER(GString)
g_string_append_uri_escaped.argtypes = [POINTER(GString),
                                             gchar_p,
                                             gchar_p,
                                             gboolean]

# GString* g_string_prepend(GString* string, const gchar* val);
g_string_prepend = libglib.g_string_prepend
g_string_prepend.restype = POINTER(GString)
g_string_prepend.argtypes = [POINTER(GString), gchar_p]

# GString* g_string_prepend_c(GString* string, gchar c);
g_string_prepend_c = libglib.g_string_prepend_c
g_string_prepend_c.restype = POINTER(GString)
g_string_prepend_c.argtypes = [POINTER(GString), gchar]

# GString* g_string_prepend_unichar(GString* string, gunichar wc);
g_string_prepend_unichar = libglib.g_string_prepend_unichar
g_string_prepend_unichar.restype = POINTER(GString)
g_string_prepend_unichar.argtypes = [POINTER(GString), gunichar]

# GString* g_string_prepend_len(GString* string, const gchar* val, gssize len);
g_string_prepend_len = libglib.g_string_prepend_len
g_string_prepend_len.restype = POINTER(GString)
g_string_prepend_len.argtypes = [POINTER(GString), gchar_p, gssize]

# GString* g_string_insert(GString* string, gssize pos, const gchar* val);
g_string_insert = libglib.g_string_insert
g_string_insert.restype = POINTER(GString)
g_string_insert.argtypes = [POINTER(GString), gssize, gchar_p]

# GString* g_string_insert_c(GString* string, gssize pos, gchar c);
g_string_insert_c = libglib.g_string_insert_c
g_string_insert_c.restype = POINTER(GString)
g_string_insert_c.argtypes = [POINTER(GString), gssize, gchar]

# GString* g_string_insert_unichar(GString* string, gssize pos, gunichar wc);
g_string_insert_unichar = libglib.g_string_insert_unichar
g_string_insert_unichar.restype = POINTER(GString)
g_string_insert_unichar.argtypes = [POINTER(GString), gssize, gunichar]

# GString* g_string_insert_len(GString* string,
#                              gssize pos,
#                              const gchar* val,
#                              gssize len);
g_string_insert_len = libglib.g_string_insert_len
g_string_insert_len.restype = POINTER(GString)
g_string_insert_len.argtypes = [POINTER(GString),
                                     gssize,
                                     gchar_p,
                                     gssize]

# GString* g_string_overwrite(GString* string, gsize pos, const gchar* val);
g_string_overwrite = libglib.g_string_overwrite
g_string_overwrite.restype = POINTER(GString)
g_string_overwrite.argtypes = [POINTER(GString), gsize, gchar_p]

# GString* g_string_overwrite_len(GString* string,
#                                 gsize pos, 
#                                 const gchar* val,
#                                 gssize len);
g_string_overwrite_len = libglib.g_string_overwrite_len
g_string_overwrite_len.restype = POINTER(GString)
g_string_overwrite_len.argtypes = [POINTER(GString),
                                        gsize,
                                        gchar_p,
                                        gssize]

# GString* g_string_erase(GString* string, gssize pos, gssize len);
g_string_erase = libglib.g_string_erase
g_string_erase.restype = POINTER(GString)
g_string_erase.argtypes = [POINTER(GString), gssize, gssize]

# GString* g_string_truncate(GString* string, gsize len);
g_string_truncate = libglib.g_string_truncate
g_string_truncate.restype = POINTER(GString)
g_string_truncate.argtypes = [POINTER(GString), gsize]

# GString* g_string_set_size(GString* string, gsize len);
g_string_set_size = libglib.g_string_set_size
g_string_set_size.restype = POINTER(GString)
g_string_set_size.argtypes = [POINTER(GString), gsize]

# gchar* g_string_free(GString* string, gboolean free_segment);
g_string_free = libglib.g_string_free
g_string_free.restype = gchar_p
g_string_free.argtypes = [POINTER(GString), gboolean]

# GBytes* g_string_free_to_bytes(GString* string);
g_string_free_to_bytes = libglib.g_string_free_to_bytes
g_string_free_to_bytes.restype = POINTER(GBytes)
g_string_free_to_bytes.argtypes = [POINTER(GString)]

# GString* g_string_up(GString* string);
g_string_up = libglib.g_string_up
g_string_up.restype = POINTER(GString)
g_string_up.argtypes = [POINTER(GString)]

# GString* g_string_down(GString* string);
g_string_down = libglib.g_string_down
g_string_down.restype = POINTER(GString)
g_string_down.argtypes = [POINTER(GString)]

# guint g_string_hash(const GString* str);
g_string_hash = libglib.g_string_hash
g_string_hash.restype = guint
g_string_hash.argtypes = [POINTER(GString)]

# gboolean g_string_equal(const GString* v, const GString* v2);
g_string_equal = libglib.g_string_equal
g_string_equal.restype = gboolean
g_string_equal.argtypes = [POINTER(GString), POINTER(GString)]

# GHashTable* g_hash_table_new(GHashFunc hash_func, GEqualFunc key_equal_func);
g_hash_table_new = libglib.g_hash_table_new
g_hash_table_new.restype = POINTER(GHashTable)
g_hash_table_new.argtypes = [GHashFunc, GEqualFunc]

# GHashTable* g_hash_table_new_full(GHashFunc hash_func,
#                                   GEqualFunc key_equal_func,
#                                   GDestroyNotify key_destroy_func,
#                                   GDestroyNotify value_destroy_func);
g_hash_table_new_full = libglib.g_hash_table_new_full
g_hash_table_new_full.restype = POINTER(GHashTable)
g_hash_table_new_full.argtypes = [GHashFunc,
                                       GEqualFunc,
                                       GDestroyNotify,
                                       GDestroyNotify]

# gboolean g_hash_table_insert(GHashTable* hash_table,
#                              gpointer key,
#                              gpointer value);
g_hash_table_insert = libglib.g_hash_table_insert
g_hash_table_insert.restype = gboolean
g_hash_table_insert.argtypes = [POINTER(GHashTable),
                                     gpointer,
                                     gpointer]

# gboolean g_hash_table_replace(GHashTable* hash_table,
#                               gpointer key,
#                               gpointer value);
g_hash_table_replace = libglib.g_hash_table_replace
g_hash_table_replace.restype = gboolean
g_hash_table_replace.argtypes = [POINTER(GHashTable), gpointer, gpointer]

# gboolean g_hash_table_add(GHashTable* hash_table, gpointer key);
g_hash_table_add = libglib.g_hash_table_add
g_hash_table_add.restype = gboolean
g_hash_table_add.argtypes = [POINTER(GHashTable), gpointer]

# gboolean g_hash_table_contains(GHashTable* hash_table, gconstpointer key);
g_hash_table_contains = libglib.g_hash_table_contains
g_hash_table_contains.restype = gboolean
g_hash_table_contains.argtypes = [POINTER(GHashTable), gconstpointer]

# guint g_hash_table_size(GHashTable* hash_table);
g_hash_table_size = libglib.g_hash_table_size
g_hash_table_size.restype = guint
g_hash_table_size.argtypes = [POINTER(GHashTable)]

# gpointer g_hash_table_lookup(GHashTable* hash_table, gconstpointer key);
g_hash_table_lookup = libglib.g_hash_table_lookup
g_hash_table_lookup.restype = gpointer
g_hash_table_lookup.argtypes = [POINTER(GHashTable), gconstpointer]

# gboolean g_hash_table_lookup_extended(GHashTable* hash_table,
#                                       gconstpointer lookup_key,
#                                       gpointer* orig_key,
#                                       gpointer* value);
g_hash_table_lookup_extended = libglib.g_hash_table_lookup_extended
g_hash_table_lookup_extended.restype = gboolean
g_hash_table_lookup_extended.argtypes = [POINTER(GHashTable),
                                              gconstpointer,
                                              POINTER(gpointer),
                                              POINTER(gpointer)]

# void g_hash_table_foreach(GHashTable* hash_table,
#                           GHFunc func,
#                           gpointer user_data);
g_hash_table_foreach = libglib.g_hash_table_foreach
g_hash_table_foreach.restype = None
g_hash_table_foreach.argtypes = [POINTER(GHashTable),
                                      GHFunc,
                                      gpointer]

# gpointer g_hash_table_find(GHashTable* hash_table,
#                            GHRFunc predicate,
#                            gpointer user_data);
g_hash_table_find = libglib.g_hash_table_find
g_hash_table_find.restype = gpointer
g_hash_table_find.argtypes = [POINTER(GHashTable),
                                   GHRFunc,
                                   gpointer]

# gboolean g_hash_table_remove(GHashTable* hash_table, gconstpointer key);
g_hash_table_remove = libglib.g_hash_table_remove
g_hash_table_remove.restype = gboolean
g_hash_table_remove.argtypes = [POINTER(GHashTable), gconstpointer]

# gboolean g_hash_table_steal(GHashTable* hash_table, gconstpointer key);
g_hash_table_steal = libglib.g_hash_table_steal
g_hash_table_steal.restype = gboolean
g_hash_table_steal.argtypes = [POINTER(GHashTable), gconstpointer]

# guint g_hash_table_foreach_remove(GHashTable* hash_table,
#                                   GHRFunc func,
#                                   gpointer user_data);
g_hash_table_foreach_remove = libglib.g_hash_table_foreach_remove
g_hash_table_foreach_remove.restype = guint
g_hash_table_foreach_remove.argtypes = [POINTER(GHashTable),
                                             GHRFunc,
                                             gpointer]

# guint g_hash_table_foreach_steal(GHashTable* hash_table,
#                                  GHRFunc func,
#                                  gpointer user_data);
g_hash_table_foreach_steal = libglib.g_hash_table_foreach_steal
g_hash_table_foreach_steal.restype = guint
g_hash_table_foreach_steal.argtypes = [POINTER(GHashTable),
                                            GHRFunc,
                                            gpointer]

# void g_hash_table_remove_all(GHashTable* hash_table);
g_hash_table_remove_all = libglib.g_hash_table_remove_all
g_hash_table_remove_all.restype = None
g_hash_table_remove_all.argtypes = [POINTER(GHashTable)]

# void g_hash_table_steal_all(GHashTable* hash_table);
g_hash_table_steal_all = libglib.g_hash_table_steal_all
g_hash_table_steal_all.restype = None
g_hash_table_steal_all.argtypes = [POINTER(GHashTable)]

# GList* g_hash_table_get_keys(GHashTable* hash_table);
g_hash_table_get_keys = libglib.g_hash_table_get_keys
g_hash_table_get_keys.restype = POINTER(GList)
g_hash_table_get_keys.argtypes = [POINTER(GHashTable)]

# GList* g_hash_table_get_values(GHashTable* hash_table);
g_hash_table_get_values = libglib.g_hash_table_get_values
g_hash_table_get_values.restype = POINTER(GList)
g_hash_table_get_values.argtypes = [POINTER(GHashTable)]

# gpointer* g_hash_table_get_keys_as_array(GHashTable* hash_table,
#                                          guint* length);
g_hash_table_get_keys_as_array = libglib.g_hash_table_get_keys_as_array
g_hash_table_get_keys_as_array.restype = POINTER(gpointer)
g_hash_table_get_keys_as_array.argtypes = [POINTER(GHashTable),
                                                POINTER(guint)]

# void g_hash_table_destroy(GHashTable* hash_table);
g_hash_table_destroy = libglib.g_hash_table_destroy
g_hash_table_destroy.restype = None
g_hash_table_destroy.argtypes = [POINTER(GHashTable)]

# GHashTable* g_hash_table_ref(GHashTable* hash_table);
g_hash_table_ref = libglib.g_hash_table_ref
g_hash_table_ref.restype = POINTER(GHashTable)
g_hash_table_ref.argtypes = [POINTER(GHashTable)]

# void g_hash_table_unref(GHashTable* hash_table);
g_hash_table_unref = libglib.g_hash_table_unref
g_hash_table_unref.restype = None
g_hash_table_unref.argtypes = [POINTER(GHashTable)]

# void g_hash_table_iter_init(GHashTableIter* iter, GHashTable* hash_table);
g_hash_table_iter_init = libglib.g_hash_table_iter_init
g_hash_table_iter_init.restype = None
g_hash_table_iter_init.argtypes = [POINTER(GHashTableIter),
                                        POINTER(GHashTable)]

# gboolean g_hash_table_iter_next(GHashTableIter* iter,
#                                 gpointer* key,
#                                 gpointer* value);
g_hash_table_iter_next = libglib.g_hash_table_iter_next
g_hash_table_iter_next.restype = gboolean
g_hash_table_iter_next.argtypes = [POINTER(GHashTableIter),
                                        POINTER(gpointer),
                                        POINTER(gpointer)]

# GHashTable* g_hash_table_iter_get_hash_table(GHashTableIter* iter);
g_hash_table_iter_get_hash_table = libglib.g_hash_table_iter_get_hash_table
g_hash_table_iter_get_hash_table.restype = POINTER(GHashTable)
g_hash_table_iter_get_hash_table.argtypes = [POINTER(GHashTableIter)]

# void g_hash_table_iter_replace(GHashTableIter* iter, gpointer value);
g_hash_table_iter_replace = libglib.g_hash_table_iter_replace
g_hash_table_iter_replace.restype = None
g_hash_table_iter_replace.argtypes = [POINTER(GHashTableIter), gpointer]

# void g_hash_table_iter_remove(GHashTableIter* iter);
g_hash_table_iter_remove = libglib.g_hash_table_iter_remove
g_hash_table_iter_remove.restype = None
g_hash_table_iter_remove.argtypes = [POINTER(GHashTableIter)]

# void g_hash_table_iter_steal(GHashTableIter* iter);
g_hash_table_iter_steal = libglib.g_hash_table_iter_steal
g_hash_table_iter_steal.restype = None
g_hash_table_iter_steal.argtypes = [POINTER(GHashTableIter)]

# gboolean g_direct_equal(gconstpointer v1, gconstpointer v2);
g_direct_equal = libglib.g_direct_equal
g_direct_equal.restype = gboolean
g_direct_equal.argtypes = [gconstpointer, gconstpointer]

# guint g_direct_hash(gconstpointer v);
g_direct_hash = libglib.g_direct_hash
g_direct_hash.restype = guint
g_direct_hash.argtypes = [gconstpointer]

# gboolean g_int_equal(gconstpointer v1, gconstpointer v2);
g_int_equal = libglib.g_int_equal
g_int_equal.restype = gboolean
g_int_equal.argtypes = [gconstpointer, gconstpointer]

# guint g_int_hash(gconstpointer v);
g_int_hash = libglib.g_int_hash
g_int_hash.restype = guint
g_int_hash.argtypes = [gconstpointer]

# gboolean g_int64_equal(gconstpointer v1, gconstpointer v2);
g_int64_equal = libglib.g_int64_equal
g_int64_equal.restype = gboolean
g_int64_equal.argtypes = [gconstpointer, gconstpointer]

# guint g_int64_hash(gconstpointer v);
g_int64_hash = libglib.g_int64_hash
g_int64_hash.restype = guint
g_int64_hash.argtypes = [gconstpointer]

# gboolean g_double_equal(gconstpointer v1, gconstpointer v2);
g_double_equal = libglib.g_double_equal
g_double_equal.restype = gboolean
g_double_equal.argtypes = [gconstpointer, gconstpointer]

# guint g_double_hash(gconstpointer v);
g_double_hash = libglib.g_double_hash
g_double_hash.restype = guint
g_double_hash.argtypes = [gconstpointer]

# gboolean g_str_equal(gconstpointer v1, gconstpointer v2);
g_str_equal = libglib.g_str_equal
g_str_equal.restype = gboolean
g_str_equal.argtypes = [gconstpointer, gconstpointer]

# guint g_str_hash(gconstpointer v);
g_str_hash = libglib.g_str_hash
g_str_hash.restype = guint
g_str_hash.argtypes = [gconstpointer]

# GList* g_list_append(GList* list, gpointer data);
g_list_append = libglib.g_list_append
g_list_append.restype = POINTER(GList)
g_list_append.argtypes = [POINTER(GList), gpointer]

# GList* g_list_prepend(GList* list, gpointer data);
g_list_prepend = libglib.g_list_prepend
g_list_prepend.restype = POINTER(GList)
g_list_prepend.argtypes = [POINTER(GList), gpointer]

# GList* g_list_insert(GList* list, gpointer data, gint position);
g_list_insert = libglib.g_list_insert
g_list_insert.restype = POINTER(GList)
g_list_insert.argtypes = [POINTER(GList), gpointer, gint]

# GList* g_list_insert_before(GList* list, GList* sibling, gpointer data);
g_list_insert_before = libglib.g_list_insert_before
g_list_insert_before.restype = POINTER(GList)
g_list_insert_before.argtypes = [POINTER(GList), POINTER(GList), gpointer]

# GList* g_list_insert_sorted(GList* list, gpointer data, GCompareFunc func);
g_list_insert_sorted = libglib.g_list_insert_sorted
g_list_insert_sorted.restype = POINTER(GList)
g_list_insert_sorted.argtypes = [POINTER(GList),
                                      gpointer,
                                      GCompareFunc]

# GList* g_list_remove(GList* list, gconstpointer data);
g_list_remove = libglib.g_list_remove
g_list_remove.restype = POINTER(GList)
g_list_remove.argtypes = [POINTER(GList), gconstpointer]

# GList* g_list_remove_link(GList* list, GList* llink);
g_list_remove_link = libglib.g_list_remove_link
g_list_remove_link.restype = POINTER(GList)
g_list_remove_link.argtypes = [POINTER(GList), POINTER(GList)]

# GList* g_list_delete_link(GList* list, GList* link_);
g_list_delete_link = libglib.g_list_delete_link
g_list_delete_link.restype = POINTER(GList)
g_list_delete_link.argtypes = [POINTER(GList), POINTER(GList)]

# GList* g_list_remove_all(GList* list, gconstpointer data);
g_list_remove_all = libglib.g_list_remove_all
g_list_remove_all.restype = POINTER(GList)
g_list_remove_all.argtypes = [POINTER(GList), gconstpointer]

# void g_list_free(GList* list);
g_list_free = libglib.g_list_free
g_list_free.restype = None
g_list_free.argtypes = [POINTER(GList)]

# void g_list_free_full(GList* list, GDestroyNotify free_func);
g_list_free_full = libglib.g_list_free_full
g_list_free_full.restype = None
g_list_free_full.argtypes = [POINTER(GList), GDestroyNotify]

# GList* g_list_alloc(void);
g_list_alloc = libglib.g_list_alloc
g_list_alloc.restype = POINTER(GList)
g_list_alloc.argtypes = []

# void g_list_free_1(GList* list);
g_list_free_1 = libglib.g_list_free_1
g_list_free_1.restype = None
g_list_free_1.argtypes = [POINTER(GList)]

# guint g_list_length(GList* list);
g_list_length = libglib.g_list_length
g_list_length.restype = guint
g_list_length.argtypes = [POINTER(GList)]

# GList* g_list_copy(GList* list);
g_list_copy = libglib.g_list_copy
g_list_copy.restype = POINTER(GList)
g_list_copy.argtypes = [POINTER(GList)]

# GList* g_list_copy_deep(GList* list, GCopyFunc func, gpointer user_data);
g_list_copy_deep = libglib.g_list_copy_deep
g_list_copy_deep.restype = POINTER(GList)
g_list_copy_deep.argtypes = [POINTER(GList), GCopyFunc, gpointer]

# GList* g_list_reverse(GList* list);
g_list_reverse = libglib.g_list_reverse
g_list_reverse.restype = POINTER(GList)
g_list_reverse.argtypes = [POINTER(GList)]

# GList* g_list_sort(GList* list, GCompareFunc compare_func);
g_list_sort = libglib.g_list_sort
g_list_sort.restype = POINTER(GList)
g_list_sort.argtypes = [POINTER(GList), GCompareFunc]

# GList* g_list_insert_sorted_with_data(GList* list,
#                                       gpointer data,
#                                       GCompareDataFunc func,
#                                       gpointer user_data);
g_list_insert_sorted_with_data = libglib.g_list_insert_sorted_with_data
g_list_insert_sorted_with_data.restype = POINTER(GList)
g_list_insert_sorted_with_data.argtypes = [POINTER(GList),
                                                gpointer,
                                                GCompareDataFunc,
                                                gpointer]

# GList* g_list_sort_with_data(GList* list,
#                              GCompareDataFunc compare_func,
#                              gpointer user_data);
g_list_sort_with_data = libglib.g_list_sort_with_data
g_list_sort_with_data.restype = POINTER(GList)
g_list_sort_with_data.argtypes = [POINTER(GList),
                                       GCompareDataFunc,
                                       gpointer]

# GList* g_list_concat(GList* list1, GList* list2);
g_list_concat = libglib.g_list_concat
g_list_concat.restype = POINTER(GList)
g_list_concat.argtypes = [POINTER(GList), POINTER(GList)]

# void g_list_foreach(GList* list, GFunc func, gpointer user_data);
g_list_foreach = libglib.g_list_foreach
g_list_foreach.restype = None
g_list_foreach.argtypes = [POINTER(GList), GFunc, gpointer]

# GList* g_list_first(GList* list);
g_list_first = libglib.g_list_first
g_list_first.restype = POINTER(GList)
g_list_first.argtypes = [POINTER(GList)]

# GList* g_list_last(GList* list);
g_list_last = libglib.g_list_last
g_list_last.restype = POINTER(GList)
g_list_last.argtypes = [POINTER(GList)]

# GList* g_list_nth(GList* list, guint n);
g_list_nth = libglib.g_list_nth
g_list_nth.restype = POINTER(GList)
g_list_nth.argtypes = [POINTER(GList), guint]

# gpointer g_list_nth_data(GList* list, guint n);
g_list_nth_data = libglib.g_list_nth_data
g_list_nth_data.restype = gpointer
g_list_nth_data.argtypes = [POINTER(GList), guint]

# GList* g_list_nth_prev(GList* list, guint n);
g_list_nth_prev = libglib.g_list_nth_prev
g_list_nth_prev.restype = POINTER(GList)
g_list_nth_prev.argtypes = [POINTER(GList), guint]

# GList* g_list_find(GList* list, gconstpointer data);
g_list_find = libglib.g_list_find
g_list_find.restype = POINTER(GList)
g_list_find.argtypes = [POINTER(GList), gconstpointer]

# GList* g_list_find_custom(GList* list, gconstpointer data, GCompareFunc func);
g_list_find_custom = libglib.g_list_find_custom
g_list_find_custom.restype = POINTER(GList)
g_list_find_custom.argtypes = [POINTER(GList),
                                    gconstpointer,
                                    GCompareFunc]

# gint g_list_position(GList* list, GList* llink);
g_list_position = libglib.g_list_position
g_list_position.restype = gint
g_list_position.argtypes = [POINTER(GList), POINTER(GList)]

# gint g_list_index(GList* list, gconstpointer data);
g_list_index = libglib.g_list_index
g_list_index.restype = gint
g_list_index.argtypes = [POINTER(GList), gconstpointer]

# GError* g_error_new(GQuark domain, gint code, const gchar* format, ...);
_g_error_new = libglib.g_error_new
_g_error_new.restype = POINTER(GError)

def g_error_new(domain, code, fmt, *args):
    _g_error_new.argtypes = [GQuark,
                                  gint,
                                  gchar_p] + make_type_list(args)
    return _g_error_new(domain, code, fmt, *args)

# GError* g_error_new_literal(GQuark domain, gint code, const gchar* message);
g_error_new_literal = libglib.g_error_new_literal
g_error_new_literal.restype = POINTER(GError)
g_error_new_literal.argtypes = [GQuark, gint, gchar_p]

# void g_error_free(GError* error);
g_error_free = libglib.g_error_free
g_error_free.restype = None
g_error_free.argtypes = [POINTER(GError)]

# GError* g_error_copy(const GError* error);
g_error_copy = libglib.g_error_copy
g_error_copy.restype = POINTER(GError)
g_error_copy.argtypes = [POINTER(GError)]

# gboolean g_error_matches(const GError* error, GQuark domain, gint code);
g_error_matches = libglib.g_error_matches
g_error_matches.restype = gboolean
g_error_matches.argtypes = [POINTER(GError), GQuark, gint]

# void g_set_error(GError** err,
#                  GQuark domain,
#                  gint code,
#                  const gchar* format,
#                  ...);
_g_set_error = libglib.g_set_error
_g_set_error.restype = None

def g_set_error(err, domain, code, fmt, *args):
    _g_set_error.argtypes = [POINTER(POINTER(GError)),
                                  GQuark,
                                  gint,
                                  gchar_p] + make_type_list(args)
    _g_set_error(err, domain, code, fmt, *args)

# void g_set_error_literal(GError** err,
#                          GQuark domain,
#                          gint code,
#                          const gchar* message);
g_set_error_literal = libglib.g_set_error_literal
g_set_error_literal.restype = None
g_set_error_literal.argtypes = [POINTER(POINTER(GError)),
                                     GQuark,
                                     gint,
                                     gchar_p]

# void g_propagate_error(GError** dest, GError* src);
g_propagate_error = libglib.g_propagate_error
g_propagate_error.restype = None
g_propagate_error.argtypes = [POINTER(POINTER(GError)),
                                   POINTER(GError)]

# void g_clear_error(GError** err);
g_clear_error = libglib.g_clear_error
g_clear_error.restype = None
g_clear_error.argtypes = [POINTER(POINTER(GError))]

# void g_prefix_error(GError** err, const gchar* format, ...);
_g_prefix_error = libglib.g_prefix_error
_g_prefix_error.restype = None

def g_prefix_error(err, fmt, *args):
    _g_prefix_error.argtypes = [POINTER(POINTER(GError)),
                                     gchar_p] + make_type_list(args)
    _g_prefix_error(err, fmt, *args)

# void g_propagate_prefixed_error(GError** dest,
#                                 GError* src,
#                                 const gchar* format,
#                                 ...);
_g_propagate_prefixed_error = libglib.g_propagate_prefixed_error
_g_propagate_prefixed_error.restype = None

def g_propagate_prefixed_error(dest, src, fmt, *args):
    _g_propagate_prefixed_error.argtypes = [POINTER(POINTER(GError)),
                                                 POINTER(GError),
                                                 gchar_p] + make_type_list(args)
    _g_propagate_prefixed_error(dest, src, fmt, *args)

# GPtrArray* g_ptr_array_new(void);
g_ptr_array_new = libglib.g_ptr_array_new
g_ptr_array_new.restype = POINTER(GPtrArray)
g_ptr_array_new.argtypes = []

# GPtrArray* g_ptr_array_sized_new(guint reserved_size);
g_ptr_array_sized_new = libglib.g_ptr_array_sized_new
g_ptr_array_sized_new.restype = POINTER(GPtrArray)
g_ptr_array_sized_new.argtypes = [guint]

# GPtrArray* g_ptr_array_new_with_free_func(GDestroyNotify element_free_func);
g_ptr_array_new_with_free_func = libglib.g_ptr_array_new_with_free_func
g_ptr_array_new_with_free_func.restype = POINTER(GPtrArray)
g_ptr_array_new_with_free_func.argtypes = [GDestroyNotify]

# GPtrArray* g_ptr_array_new_full(guint reserved_size,
#                                 GDestroyNotify element_free_func);
g_ptr_array_new_full = libglib.g_ptr_array_new_full
g_ptr_array_new_full.restype = POINTER(GPtrArray)
g_ptr_array_new_full.argtypes = [guint, GDestroyNotify]

# void g_ptr_array_set_free_func(GPtrArray* array,
#                                GDestroyNotify element_free_func);
g_ptr_array_set_free_func = libglib.g_ptr_array_set_free_func
g_ptr_array_set_free_func.restype = None
g_ptr_array_set_free_func.argtypes = [POINTER(GPtrArray),
                                           GDestroyNotify]

# GPtrArray* g_ptr_array_ref(GPtrArray* array);
g_ptr_array_ref = libglib.g_ptr_array_ref
g_ptr_array_ref.restype = POINTER(GPtrArray)
g_ptr_array_ref.argtypes = [POINTER(GPtrArray)]

# void g_ptr_array_unref(GPtrArray* array);
g_ptr_array_unref = libglib.g_ptr_array_unref
g_ptr_array_unref.restype = None
g_ptr_array_unref.argtypes = [POINTER(GPtrArray)]

# void g_ptr_array_add(GPtrArray* array, gpointer);
g_ptr_array_add = libglib.g_ptr_array_add
g_ptr_array_add.restype = None
g_ptr_array_add.argtypes = [POINTER(GPtrArray), gpointer]

# void g_ptr_array_insert(GPtrArray* array, git index_, gpointer data);
g_ptr_array_insert = libglib.g_ptr_array_insert
g_ptr_array_insert.restype = None
g_ptr_array_insert.argtypes = [POINTER(GPtrArray),
                                    gint,
                                    gpointer]

# gboolean g_ptr_array_remove(GPtrArray* array, gpointer data);
g_ptr_array_remove = libglib.g_ptr_array_remove
g_ptr_array_remove.restype = gboolean
g_ptr_array_remove.argtypes = [POINTER(GPtrArray), gpointer]

# gpointer g_ptr_array_remove_index(GPtrArray* array, guint index_);
g_ptr_array_remove_index = libglib.g_ptr_array_remove_index
g_ptr_array_remove_index.restype = gpointer
g_ptr_array_remove_index.argtypes = [POINTER(GPtrArray), guint]

# gboolean g_ptr_array_remove_fast(GPtrArray* array, gpointer data);
g_ptr_array_remove_fast = libglib.g_ptr_array_remove_fast
g_ptr_array_remove_fast.restype = gboolean
g_ptr_array_remove_fast.argtypes = [POINTER(GPtrArray), gpointer]

# gpointer g_ptr_array_remove_index_fast(GPtrArray* array, guint index_);
g_ptr_array_remove_index_fast = libglib.g_ptr_array_remove_index_fast
g_ptr_array_remove_index_fast.restype = gpointer
g_ptr_array_remove_index_fast.argtypes = [POINTER(GPtrArray), guint]

# GPtrArray* g_ptr_array_remove_range(GPtrArray* array,
#                                     guint index_,
#                                     guint length);
g_ptr_array_remove_range = libglib.g_ptr_array_remove_range
g_ptr_array_remove_range.restype = POINTER(GPtrArray)
g_ptr_array_remove_range.argtypes = [POINTER(GPtrArray), guint, guint]

# void g_ptr_array_sort(GPtrArray* array, GCompareFunc compare_func);
g_ptr_array_sort = libglib.g_ptr_array_sort
g_ptr_array_sort.restype = None
g_ptr_array_sort.argtypes = [POINTER(GPtrArray),
                                  GCompareFunc]

# void g_ptr_array_sort_with_data(GPtrArray* array,
#                                 GCompareDataFunc compare_func,
#                                 gpointer user_data);
g_ptr_array_sort_with_data = libglib.g_ptr_array_sort_with_data
g_ptr_array_sort_with_data.restype = None
g_ptr_array_sort_with_data.argtypes = [POINTER(GPtrArray),
                                            GCompareDataFunc,
                                            gpointer]

# void g_ptr_array_set_size(GPtrArray* array, gint length);
g_ptr_array_set_size = libglib.g_ptr_array_set_size
g_ptr_array_set_size.restype = None
g_ptr_array_set_size.argtypes = [POINTER(GPtrArray), gint]

# gpointer* g_ptr_array_free(GPtrArray* array, gboolean free_seg);
g_ptr_array_free = libglib.g_ptr_array_free
g_ptr_array_free.restype = POINTER(gpointer)
g_ptr_array_free.argtypes = [POINTER(GPtrArray), gboolean]

# void g_ptr_array_foreach(GPtrArray* array, GFunc func, gpointer user_data);
g_ptr_array_foreach = libglib.g_ptr_array_foreach
g_ptr_array_foreach.restype = None
g_ptr_array_foreach.argtypes = [POINTER(GPtrArray),
                                     GFunc,
                                     gpointer]

# gboolean g_ptr_array_find(GPtrArray* haystack,
#                           gconstpointer needle,
#                           guint* index_);
g_ptr_array_find = libglib.g_ptr_array_find
g_ptr_array_find.restype = gboolean
g_ptr_array_find.argtypes = [POINTER(GPtrArray),
                                  gconstpointer,
                                  POINTER(guint)]

# gboolean g_ptr_array_find_with_equal_func(GPtrArray* haystack,
#                                           gconstpointer needle,
#                                           GEqualFunc equal_func,
#                                           guint* index_);
g_ptr_array_find_with_equal_func = libglib.g_ptr_array_find_with_equal_func
g_ptr_array_find_with_equal_func.restype = gboolean
g_ptr_array_find_with_equal_func.argtypes = [POINTER(GPtrArray),
                                                  gconstpointer,
                                                  GEqualFunc,
                                                  POINTER(guint)]

# GArray* g_array_new(gboolean zero_terminated,
#                     gboolean clear_,
#                     guint element_size);
g_array_new = libglib.g_array_new
g_array_new.restype = POINTER(GArray)
g_array_new.argtypes = [gboolean, gboolean, guint]

# GArray* g_array_sized_new(gboolean zero_terminated,
#                           gboolean clear_,
#                           guint element_size,
#                           guint reserved_size);
g_array_sized_new = libglib.g_array_sized_new
g_array_sized_new.restype = POINTER(GArray)
g_array_sized_new.argtypes = [gboolean,
                                   gboolean,
                                   guint,
                                   guint]

# GArray* g_array_ref(GArray* array);
g_array_ref = libglib.g_array_ref
g_array_ref.restype = POINTER(GArray)
g_array_ref.argtypes = [POINTER(GArray)]

# void g_array_unref(GArray* array);
g_array_unref = libglib.g_array_unref
g_array_unref.restype = None
g_array_unref.argtypes = [POINTER(GArray)]

# guint g_array_get_element_size(GArray* array);
g_array_get_element_size = libglib.g_array_get_element_size
g_array_get_element_size.restype = guint
g_array_get_element_size.argtypes = [POINTER(GArray)]

# GArray* g_array_append_vals(GArray* array, gconstpointer data, guint len);
g_array_append_vals = libglib.g_array_append_vals
g_array_append_vals.restype = POINTER(GArray)
g_array_append_vals.argtypes = [POINTER(GArray), gconstpointer, guint]

# GArray* g_array_prepend_vals(GArray* array, gconstpointer data, guint len);
g_array_prepend_vals = libglib.g_array_prepend_vals
g_array_prepend_vals.restype = POINTER(GArray)
g_array_prepend_vals.argtypes = [POINTER(GArray), gconstpointer, guint]

# GArray* g_array_insert_vals(GArray* array,
#                             guint index_,
#                             gconstpointer data,
#                             guint len);
g_array_insert_vals = libglib.g_array_insert_vals
g_array_insert_vals.restype = POINTER(GArray)
g_array_insert_vals.argtypes = [POINTER(GArray),
                                     guint,
                                     gconstpointer,
                                     guint]

# GArray* g_array_remove_index(GArray* array, guint index_);
g_array_remove_index = libglib.g_array_remove_index
g_array_remove_index.restype = POINTER(GArray)
g_array_remove_index.argtypes = [POINTER(GArray), guint]

# GArray* g_array_remove_index_fast(GArray* array, guint index_);
g_array_remove_index_fast = libglib.g_array_remove_index_fast
g_array_remove_index_fast.restype = POINTER(GArray)
g_array_remove_index_fast.argtypes = [POINTER(GArray), guint]

# GArray* g_array_remove_range(GArray* array, guint index_, guint length);
g_array_remove_range = libglib.g_array_remove_range
g_array_remove_range.restype = POINTER(GArray)
g_array_remove_range.argtypes = [POINTER(GArray), guint, guint]

# void g_array_sort(GArray* array, GCompareFunc compare_func);
g_array_sort = libglib.g_array_sort
g_array_sort.restype = None
g_array_sort.argtypes = [POINTER(GArray), GCompareFunc]

# void g_array_sort_with_data(GArray* array,
#                             GCompareDataFunc compare_func,
#                             gpointer user_data);
g_array_sort_with_data = libglib.g_array_sort_with_data
g_array_sort_with_data.restype = None
g_array_sort_with_data.argtypes = [POINTER(GArray),
                                        GCompareDataFunc,
                                        gpointer]

# GArray* g_array_set_size(GArray* array, guint length);
g_array_set_size = libglib.g_array_set_size
g_array_set_size.restype = POINTER(GArray)
g_array_set_size.argtypes = [POINTER(GArray), guint]

# void g_array_set_clear_func(GArray* array, GDestroyNotify clear_func);
g_array_set_clear_func = libglib.g_array_set_clear_func
g_array_set_clear_func.restype = None
g_array_set_clear_func.argtypes = [POINTER(GArray), GDestroyNotify]

# gchar* g_array_free(GArray* array, gboolean free_segment);
g_array_free = libglib.g_array_free
g_array_free.restype = gchar_p
g_array_free.argtypes = [POINTER(GArray), gboolean]

def g_array_index_p(data, type, index):
    return POINTER(type)(data.data.value) + index

# GSList* g_slist_alloc(void);
g_slist_alloc = libglib.g_slist_alloc
g_slist_alloc.restype = POINTER(GSList)
g_slist_alloc.argtypes = []

# GSList* g_slist_append(GSList* list, gpointer data);
g_slist_append = libglib.g_slist_append
g_slist_append.restype = POINTER(GSList)
g_slist_append.argtypes = [POINTER(GSList), gpointer]

# GSList* g_slist_prepend(GSList* list, gpointer data);
g_slist_prepend = libglib.g_slist_prepend
g_slist_prepend.restype = POINTER(GSList)
g_slist_prepend.argtypes = [POINTER(GSList), gpointer]

# GSList* g_slist_insert(GSList* list, gpointer data, gint position);
g_slist_insert = libglib.g_slist_insert
g_slist_insert.restype = POINTER(GSList)
g_slist_insert.argtypes = [POINTER(GSList), gpointer, gint]

# GSList* g_slist_insert_before(GSList* slist, GSList* sibling, gpointer data);
g_slist_insert_before = libglib.g_slist_insert_before
g_slist_insert_before.restype = POINTER(GSList)
g_slist_insert_before.argtypes = [POINTER(GSList), POINTER(GSList), gpointer]

# GSList* g_slist_insert_sorted(GSList* list, gpointer data, GCompareFunc func);
g_slist_insert_sorted = libglib.g_slist_insert_sorted
g_slist_insert_sorted.restype = POINTER(GSList)
g_slist_insert_sorted.argtypes = [POINTER(GSList), gpointer, GCompareFunc]

# GSList* g_slist_remove(GSList* list, gconstpointer data);
g_slist_remove = libglib.g_slist_remove
g_slist_remove.restype = POINTER(GSList)
g_slist_remove.argtypes = [POINTER(GSList), gconstpointer]

# GSList* g_slist_remove_link(GSList* list, GSList* link_);
g_slist_remove_link = libglib.g_slist_remove_link
g_slist_remove_link.restype = POINTER(GSList)
g_slist_remove_link.argtypes = [POINTER(GSList), POINTER(GSList)]

# GSList* g_slist_delete_link(GSList* list, GSList* link_);
g_slist_delete_link = libglib.g_slist_delete_link
g_slist_delete_link.restype = POINTER(GSList)
g_slist_delete_link.argtypes = [POINTER(GSList), POINTER(GSList)]

# GSList* g_slist_remove_all(GSList* list, gconstpointer data);
g_slist_remove_all = libglib.g_slist_remove_all
g_slist_remove_all.restype = POINTER(GSList)
g_slist_remove_all.argtypes = [POINTER(GSList), gconstpointer]

# void g_slist_free(GSList* list);
g_slist_free = libglib.g_slist_free
g_slist_free.restype = None
g_slist_free.argtypes = [POINTER(GSList)]

# void g_slist_free_full(GSList* list, GDestroyNotify free_func);
g_slist_free_full = libglib.g_slist_free_full
g_slist_free_full.restype = None
g_slist_free_full.argtypes = [POINTER(GSList), GDestroyNotify]

# void g_slist_free_1(GSList* list);
g_slist_free_1 = libglib.g_slist_free_1
g_slist_free_1.restype = None
g_slist_free_1.argtypes = [POINTER(GSList)]

# guint g_slist_length(GSList* list);
g_slist_length = libglib.g_slist_length
g_slist_length.restype = guint
g_slist_length.argtypes = [POINTER(GSList)]

# GSList* g_slist_copy(GSList* list);
g_slist_copy = libglib.g_slist_copy
g_slist_copy.restype = POINTER(GSList)
g_slist_copy.argtypes = [POINTER(GSList)]

# GSList* g_slist_copy_deep(GSList* list, GCopyFunc func, gpointer user_data);
g_slist_copy_deep = libglib.g_slist_copy_deep
g_slist_copy_deep.restype = POINTER(GSList)
g_slist_copy_deep.argtypes = [POINTER(GSList), GCopyFunc, gpointer]

# GSList* g_slist_reverse(GSList* list);
g_slist_reverse = libglib.g_slist_reverse
g_slist_reverse.restype = POINTER(GSList)
g_slist_reverse.argtypes = [POINTER(GSList)]

# GSList* g_slist_insert_sorted_with_data(GSList* list,
#                                         gpointer data,
#                                         GCompareDataFunc func,
#                                         gpointer user_data);
g_slist_insert_sorted_with_data = libglib.g_slist_insert_sorted_with_data
g_slist_insert_sorted_with_data.restype = POINTER(GSList)
g_slist_insert_sorted_with_data.argtypes = [POINTER(GSList),
                                                 gpointer,
                                                 GCompareDataFunc,
                                                 gpointer]

# GSList* g_slist_sort(GSList* list, GCompareFunc compare_func);
g_slist_sort = libglib.g_slist_sort
g_slist_sort.restype = POINTER(GSList)
g_slist_sort.argtypes = [POINTER(GSList), GCompareFunc]

# GSList* g_slist_sort_with_data(GSList* list,
#                                GCompareDataFunc compare_func,
#                                gpointer user_data);
g_slist_sort_with_data = libglib.g_slist_sort_with_data
g_slist_sort_with_data.restype = POINTER(GSList)
g_slist_sort_with_data.argtypes = [POINTER(GSList),
                                        GCompareDataFunc,
                                        gpointer]

# GSList* g_slist_concat(GSList* list1, GSList* list2);
g_slist_concat = libglib.g_slist_concat
g_slist_concat.restype = POINTER(GSList)
g_slist_concat.argtypes = [POINTER(GSList), POINTER(GSList)]

# void g_slist_foreach(GSList* list, GFunc func, gpointer user_data);
g_slist_foreach = libglib.g_slist_foreach
g_slist_foreach.restype = None
g_slist_foreach.argtypes = [POINTER(GSList), GFunc, gpointer]

# GSList* g_slist_last(GSList* list);
g_slist_last = libglib.g_slist_last
g_slist_last.restype = POINTER(GSList)
g_slist_last.argtypes = [POINTER(GSList)]

# GSList* g_slist_nth(GSList* list, guint n);
g_slist_nth = libglib.g_slist_nth
g_slist_nth.restype = POINTER(GSList)
g_slist_nth.argtypes = [POINTER(GSList), guint]

# gpointer g_slist_nth_data(GSList* list, guint n);
g_slist_nth_data = libglib.g_slist_nth_data
g_slist_nth_data.restype = gpointer
g_slist_nth_data.argtypes = [POINTER(GSList), guint]

# GSList* g_slist_find(GSList* list, gconstpointer data);
g_slist_find = libglib.g_slist_find
g_slist_find.restype = POINTER(GSList)
g_slist_find.argtypes = [POINTER(GSList), gconstpointer]

# GSList* g_slist_find_custom(GSList* list,
#                             gconstpointer data,
#                             GCompareFunc func);
g_slist_find_custom = libglib.g_slist_find_custom
g_slist_find_custom.restype = POINTER(GSList)
g_slist_find_custom.argtypes = [POINTER(GSList),
                                     gconstpointer,
                                     GCompareFunc]

# gint g_slist_position(GSList* list, GSList* llink);
g_slist_position = libglib.g_slist_position
g_slist_position.restype = gint
g_slist_position.argtypes = [POINTER(GSList), POINTER(GSList)]

# gint g_slist_index(GSList* list, gconstpointer data);
g_slist_index = libglib.g_slist_index
g_slist_index.restype = gint
g_slist_index.argtypes = [POINTER(GSList), gconstpointer]

# GByteArray* g_byte_array_new(void);
g_byte_array_new = libglib.g_byte_array_new
g_byte_array_new.restype = POINTER(GByteArray)
g_byte_array_new.argtypes = []

# GByteArray* g_byte_array_new_take(guint8* data, gsize len);
g_byte_array_new_take = libglib.g_byte_array_new_take
g_byte_array_new_take.restype = POINTER(GByteArray)
g_byte_array_new_take.argtypes = [POINTER(guint8), gsize]

# GByteArray* g_byte_array_sized_new(guint reserved_size);
g_byte_array_sized_new = libglib.g_byte_array_sized_new
g_byte_array_sized_new.restype = POINTER(GByteArray)
g_byte_array_sized_new.argtypes = [guint]

# GByteArray* g_byte_array_ref(GByteArray* array);
g_byte_array_ref = libglib.g_byte_array_ref
g_byte_array_ref.restype = POINTER(GByteArray)
g_byte_array_ref.argtypes = [POINTER(GByteArray)]

# void g_byte_array_unref(GByteArray* array);
g_byte_array_unref = libglib.g_byte_array_unref
g_byte_array_unref.restype = None
g_byte_array_unref.argtypes = [POINTER(GByteArray)]

# GByteArray* g_byte_array_append(GByteArray* array,
#                                 const guint8* data,
#                                 guint len);
g_byte_array_append = libglib.g_byte_array_append
g_byte_array_append.restype = POINTER(GByteArray)
g_byte_array_append.argtypes = [POINTER(GByteArray),
                                     POINTER(guint8),
                                     guint]

# GByteArray* g_byte_array_prepend(GByteArray* array,
#                                  const guint8* data,
#                                  guint len);
g_byte_array_prepend = libglib.g_byte_array_prepend
g_byte_array_prepend.restype = POINTER(GByteArray)
g_byte_array_prepend.argtypes = [POINTER(GByteArray),
                                      POINTER(guint8),
                                      guint]

# GByteArray* g_byte_array_remove_index(GByteArray* array, guint index_);
g_byte_array_remove_index = libglib.g_byte_array_remove_index
g_byte_array_remove_index.restype = POINTER(GByteArray)
g_byte_array_remove_index.argtypes = [POINTER(GByteArray), guint]

# GByteArray* g_byte_array_remove_index_fast(GByteArray* array, guint index_);
g_byte_array_remove_index_fast = libglib.g_byte_array_remove_index_fast
g_byte_array_remove_index_fast.restype = POINTER(GByteArray)
g_byte_array_remove_index_fast.argtypes = [POINTER(GByteArray), guint]

# GByteArray* g_byte_array_remove_range(GByteArray* array,
#                                       guint index_,
#                                       guint length);
g_byte_array_remove_range = libglib.g_byte_array_remove_range
g_byte_array_remove_range.restype = POINTER(GByteArray)
g_byte_array_remove_range.argtypes = [POINTER(GByteArray), guint, gint]

# void g_byte_array_sort(GByteArray* array, GCompareFunc compare_func);
g_byte_array_sort = libglib.g_byte_array_sort
g_byte_array_sort.restype = None
g_byte_array_sort.argtypes = [POINTER(GByteArray), GCompareFunc]

# void g_byte_array_sort_with_data(GByteArray* array,
#                                  GCompareDataFunc compare_func,
#                                  gpointer user_data);
g_byte_array_sort_with_data = libglib.g_byte_array_sort_with_data
g_byte_array_sort_with_data.restype = None
g_byte_array_sort_with_data.argtypes = [POINTER(GByteArray),
                                             GCompareDataFunc,
                                             gpointer]

# GByteArray* g_byte_array_set_size(GByteArray* array, guint length);
g_byte_array_set_size = libglib.g_byte_array_set_size
g_byte_array_set_size.restype = POINTER(GByteArray)
g_byte_array_set_size.argtypes = [POINTER(GByteArray), guint]

# guint* g_byte_array_free(GByteArray* array, gboolean free_segment);
g_byte_array_free = libglib.g_byte_array_free
g_byte_array_free.restype = POINTER(guint)
g_byte_array_free.argtypes = [POINTER(GByteArray), gboolean]

# GBytes* g_byte_array_free_to_bytes(GByteArray* array);
g_byte_array_free_to_bytes = libglib.g_byte_array_free_to_bytes
g_byte_array_free_to_bytes.restype = POINTER(GBytes)
g_byte_array_free_to_bytes.argtypes = [POINTER(GByteArray)]

# GBytes* g_bytes_new(gconstpointer data, gsize size);
g_bytes_new = libglib.g_bytes_new
g_bytes_new.restype = POINTER(GBytes)
g_bytes_new.argtypes = [gconstpointer, gsize]

# GBytes* g_bytes_new_take(gpointer data, gsize size);
g_bytes_new_take = libglib.g_bytes_new_take
g_bytes_new_take.restype = POINTER(GBytes)
g_bytes_new_take.argtypes = [gpointer, gsize]

# GBytes* g_bytes_new_static(gconstpointer data, gsize size);
g_bytes_new_static = libglib.g_bytes_new_static
g_bytes_new_static.restype = POINTER(GBytes)
g_bytes_new_static.argtypes = [gconstpointer, gsize]

# GBytes* g_bytes_new_with_free_func(gconstpointer data,
#                                    gsize size,
#                                    GDestroyNotify free_func,
#                                    gpointer user_data);
g_bytes_new_with_free_func = libglib.g_bytes_new_with_free_func
g_bytes_new_with_free_func.restype = POINTER(GBytes)
g_bytes_new_with_free_func.argtypes = [gconstpointer,
                                            gsize,
                                            GDestroyNotify,
                                            gpointer]

# GBytes* g_bytes_new_from_bytes(GBytes* bytes, gsize offset, gsize length);
g_bytes_new_from_bytes = libglib.g_bytes_new_from_bytes
g_bytes_new_from_bytes.restype = POINTER(GBytes)
g_bytes_new_from_bytes.argtypes = [POINTER(GBytes), gsize, gsize]

# gconstpointer g_bytes_get_data(GBytes* bytes, gsize* size);
g_bytes_get_data = libglib.g_bytes_get_data
g_bytes_get_data.restype = gconstpointer
g_bytes_get_data.argtypes = [POINTER(GBytes), POINTER(gsize)]

# gsize g_bytes_get_size(GBytes* bytes);
g_bytes_get_size = libglib.g_bytes_get_size
g_bytes_get_size.restype = gsize
g_bytes_get_size.argtypes = [POINTER(GBytes)]

# guint g_bytes_hash(gconstpointer bytes);
g_bytes_hash = libglib.g_bytes_hash
g_bytes_hash.restype = guint
g_bytes_hash.argtypes = [gconstpointer]

# gboolean g_bytes_equal(gconstpointer bytes1, gconstpointer bytes2);
g_bytes_equal = libglib.g_bytes_equal
g_bytes_equal.restype = gboolean
g_bytes_equal.argtypes = [gconstpointer, gconstpointer]

# gint g_bytes_compare(gconstpointer bytes1, gconstpointer bytes2);
g_bytes_compare = libglib.g_bytes_compare
g_bytes_compare.restype = gint
g_bytes_compare.argtypes = [gconstpointer, gconstpointer]

# GBytes* g_bytes_ref(GBytes* bytes);
g_bytes_ref = libglib.g_bytes_ref
g_bytes_ref.restype = POINTER(GBytes)
g_bytes_ref.argtypes = [POINTER(GBytes)]

# void g_bytes_unref(GBytes* bytes);
g_bytes_unref = libglib.g_bytes_unref
g_bytes_unref.restype = None
g_bytes_unref.argtypes = [POINTER(GBytes)]

# gpointer g_bytes_unref_to_data(GBytes* bytes, gsize* size);
g_bytes_unref_to_data = libglib.g_bytes_unref_to_data
g_bytes_unref_to_data.restype = gpointer
g_bytes_unref_to_data.argtypes = [POINTER(GBytes), POINTER(gsize)]

# GByteArray* g_bytes_unref_to_array(GBytes* bytes);
g_bytes_unref_to_array = libglib.g_bytes_unref_to_array
g_bytes_unref_to_array.restype = POINTER(GByteArray)
g_bytes_unref_to_array.argtypes = [POINTER(GBytes)]

# GRegex* g_regex_new(const gchar* pattern,
#                     GRegexCompileFlags compile_options,
#                     GRegexMatchFlags match_options,
#                     GError** error);
g_regex_new = libglib.g_regex_new
g_regex_new.restype = POINTER(GRegex)
g_regex_new.argtypes = [gchar_p,
                             GRegexCompileFlags,
                             GRegexMatchFlags,
                             POINTER(POINTER(GError))]

# GRegex* g_regex_ref(GRegex* regex);
g_regex_ref = libglib.g_regex_ref
g_regex_ref.restype = POINTER(GRegex)
g_regex_ref.argtypes = [POINTER(GRegex)]

# void g_regex_unref(GRegex* regex);
g_regex_unref = libglib.g_regex_unref
g_regex_unref.restype = None
g_regex_unref.argtypes = [POINTER(GRegex)]

# const gchar* g_regex_get_pattern(const GRegex* regex);
g_regex_get_pattern = libglib.g_regex_get_pattern
g_regex_get_pattern.restype = gchar_p
g_regex_get_pattern.argtypes = [POINTER(GRegex)]

# gint g_regex_get_max_backref(const GRegex* regex);
g_regex_get_max_backref = libglib.g_regex_get_max_backref
g_regex_get_max_backref.restype = gint
g_regex_get_max_backref.argtypes = [POINTER(GRegex)]

# gint g_regex_get_capture_count(const GRegex* regex);
g_regex_get_capture_count = libglib.g_regex_get_capture_count
g_regex_get_capture_count.restype = gint
g_regex_get_capture_count.argtypes = [POINTER(GRegex)]

# gboolean g_regex_get_has_cr_or_lf(const GRegex* regex);
g_regex_get_has_cr_or_lf = libglib.g_regex_get_has_cr_or_lf
g_regex_get_has_cr_or_lf.restype = gboolean
g_regex_get_has_cr_or_lf.argtypes = [POINTER(GRegex)]

# gint g_regex_get_max_lookbehind(const GRegex* regex);
g_regex_get_max_lookbehind = libglib.g_regex_get_max_lookbehind
g_regex_get_max_lookbehind.restype = gint
g_regex_get_max_lookbehind.argtypes = [POINTER(GRegex)]

# gint g_regex_get_string_number(const GRegex* regex, const gchar* name);
g_regex_get_string_number = libglib.g_regex_get_string_number
g_regex_get_string_number.restype = gint
g_regex_get_string_number.argtypes = [POINTER(GRegex), gchar_p]

# GRegexCompileFlags g_regex_get_compile_flags(const GRegex* regex);
g_regex_get_compile_flags = libglib.g_regex_get_compile_flags
g_regex_get_compile_flags.restype = GRegexCompileFlags
g_regex_get_compile_flags.argtypes = [POINTER(GRegex)]

# GRegexMatchFlags g_regex_get_match_flags(const GRegex* regex);
g_regex_get_match_flags = libglib.g_regex_get_match_flags
g_regex_get_match_flags.restype = GRegexMatchFlags
g_regex_get_match_flags.argtypes = [POINTER(GRegex)]

# gchar* g_regex_escape_string(const gchar* string, gint length);
g_regex_escape_string = libglib.g_regex_escape_string
g_regex_escape_string.restype = gchar_p
g_regex_escape_string.argtypes = [gchar_p, gint]

# gchar* g_regex_escape_nul(const gchar* string, gint length);
g_regex_escape_nul = libglib.g_regex_escape_nul
g_regex_escape_nul.restype = gchar_p
g_regex_escape_nul.argtypes = [gchar_p, gint]

# gboolean g_regex_match_simple(const gchar* pattern,
#                               const gchar* string,
#                               GRegexCompileFlags compile_options,
#                               GRegexMatchFlags match_options);
g_regex_match_simple = libglib.g_regex_match_simple
g_regex_match_simple.restype = gboolean
g_regex_match_simple.argtypes = [gchar_p,
                                      gchar_p,
                                      GRegexCompileFlags,
                                      GRegexMatchFlags]

# gboolean g_regex_match(const GRegex* regex,
#                        const gchar* string,
#                        GRegexMatchFlags match_options,
#                        GMatchInfo** match_info);
g_regex_match = libglib.g_regex_match
g_regex_match.restype = gboolean
g_regex_match.argtypes = [POINTER(GRegex),
                               GRegexMatchFlags,
                               POINTER(POINTER(GMatchInfo))]

# gboolean g_regex_match_full(const GRegex* regex,
#                             const gchar* string,
#                             gssize string_len,
#                             gint start_position,
#                             GRegexMatchFlags match_options,
#                             GMatchInfo** match_info,
#                             GError** error);
g_regex_match_full = libglib.g_regex_match_full
g_regex_match_full.restype = gboolean
g_regex_match_full.argtypes = [POINTER(GRegex),
                                    gchar_p,
                                    gssize,
                                    gint,
                                    GRegexMatchFlags,
                                    POINTER(POINTER(GMatchInfo)),
                                    POINTER(POINTER(GError))]

# gboolean g_regex_match_all(const GRegex* regex,
#                            const gchar* string,
#                            GRegexMatchFlags match_options,
#                            GMatchInfo** match_info);
g_regex_match_all = libglib.g_regex_match_all
g_regex_match_all.restype = gboolean
g_regex_match_all.argtypes = [POINTER(GRegex),
                                   gchar_p,
                                   GRegexMatchFlags,
                                   POINTER(POINTER(GMatchInfo))]

# gboolean g_regex_match_all_full(const GRegex* regex,
#                                 const gchar* string,
#                                 gssize string_len,
#                                 gint start_position,
#                                 GRegexMatchFlags match_options,
#                                 GMatchInfo** match_info,
#                                 GError** error);
g_regex_match_all_full = libglib.g_regex_match_all_full
g_regex_match_all_full.restype = gboolean
g_regex_match_all_full.argtypes = [POINTER(GRegex),
                                        gchar_p,
                                        gssize,
                                        gint,
                                        GRegexMatchFlags,
                                        POINTER(POINTER(GMatchInfo)),
                                        POINTER(POINTER(GError))]

# gchar** g_regex_split_simple(const gchar* pattern,
#                              const gchar* string,
#                              GRegexCompileFlags compile_options,
#                              GRegexMatchFlags match_options);
g_regex_split_simple = libglib.g_regex_split_simple
g_regex_split_simple.restype = POINTER(gchar_p)
g_regex_split_simple.argtypes = [gchar_p,
                                      gchar_p,
                                      GRegexCompileFlags,
                                      GRegexMatchFlags]

# gchar** g_regex_split(const GRegex* regex,
#                       const gchar* string,
#                       GRegexMatchFlags match_options);
g_regex_split = libglib.g_regex_split
g_regex_split.restype = POINTER(gchar_p)
g_regex_split.argtypes = [POINTER(GRegex),
                               gchar_p,
                               GRegexMatchFlags]

# gchar** g_regex_split_full(const GRegex* regex,
#                            const gchar* string,
#                            gssize string_len,
#                            gint start_position,
#                            GRegexMatchFlags match_options,
#                            gint max_tokens,
#                            GError** error);
g_regex_split_full = libglib.g_regex_split_full
g_regex_split_full.restype = POINTER(gchar_p)
g_regex_split_full.argtypes = [POINTER(GRegex),
                                    gchar_p,
                                    gssize,
                                    gint,
                                    GRegexMatchFlags,
                                    gint,
                                    POINTER(POINTER(GError))]

# gchar* g_regex_replace(const GRegex* regex,
#                        const gchar* string,
#                        gssize string_len,
#                        gint start_position,
#                        const gchar* replacement,
#                        GRegexMatchFlags match_options,
#                        GError** error);
g_regex_replace = libglib.g_regex_replace
g_regex_replace.restype = gchar_p
g_regex_replace.argtypes = [POINTER(GRegex),
                                 gchar_p,
                                 gssize,
                                 gint,
                                 gchar_p,
                                 GRegexMatchFlags,
                                 POINTER(POINTER(GError))]

# gchar* g_regex_replace_literal(const GRegex* regex,
#                                const gchar* string,
#                                gssize string_len,
#                                gint start_position,
#                                const gchar* replacement,
#                                GRegexMatchFlags match_options,
#                                GError** error);
g_regex_replace_literal = libglib.g_regex_replace_literal
g_regex_replace_literal.restype = gchar_p
g_regex_replace_literal.argtypes = [POINTER(GRegex),
                                         gchar_p,
                                         gssize,
                                         gint,
                                         gchar_p,
                                         GRegexMatchFlags,
                                         POINTER(POINTER(GError))]

# gchar* g_regex_replace_eval(const GRegex* regex,
#                             const gchar* string,
#                             gssize string_len,
#                             gint start_position,
#                             GRegexMatchFlags match_options,
#                             GRegexEvalCallback eval,
#                             gpointer user_data,
#                             GError** error);
g_regex_replace_eval = libglib.g_regex_replace_eval
g_regex_replace_eval.restype = gchar_p
g_regex_replace_eval.argtypes = [POINTER(GRegex),
                                      gchar_p,
                                      gssize,
                                      gint,
                                      GRegexMatchFlags,
                                      GRegexEvalCallback,
                                      gpointer,
                                      POINTER(POINTER(GError))]

# gboolean g_regex_check_replacement(const gchar* replacement,
#                                    gboolean* has_references,
#                                    GError** error);
g_regex_check_replacement = libglib.g_regex_check_replacement
g_regex_check_replacement.restype = gboolean
g_regex_check_replacement.argtypes = [gchar_p,
                                           POINTER(gboolean),
                                           POINTER(POINTER(GError))]

# GRegex* g_match_info_get_regex(const GMatchInfo* match_info);
g_match_info_get_regex = libglib.g_match_info_get_regex
g_match_info_get_regex.restype = POINTER(GRegex)
g_match_info_get_regex.argtypes = [POINTER(GMatchInfo)]

# const gchar* g_match_info_get_string(const GMatchInfo* match_info);
g_match_info_get_string = libglib.g_match_info_get_string
g_match_info_get_string.restype = gchar_p
g_match_info_get_string.argtypes = [POINTER(GMatchInfo)]

# GMatchInfo* g_match_info_ref(GMatchInfo* match_info);
g_match_info_ref = libglib.g_match_info_ref
g_match_info_ref.restype = POINTER(GMatchInfo)
g_match_info_ref.argtypes = [POINTER(GMatchInfo)]

# void g_match_info_unref(GMatchInfo* match_info);
g_match_info_unref = libglib.g_match_info_unref
g_match_info_unref.restype = None
g_match_info_unref.argtypes = [POINTER(GMatchInfo)]

# void g_match_info_free(GMatchInfo* match_info);
g_match_info_free = libglib.g_match_info_free
g_match_info_free.restype = None
g_match_info_free.argtypes = [POINTER(GMatchInfo)]

# gboolean g_match_info_matches(const GMatchInfo* match_info);
g_match_info_matches = libglib.g_match_info_matches
g_match_info_matches.restype = gboolean
g_match_info_matches.argtypes = [POINTER(GMatchInfo)]

# gboolean g_match_info_next(GMatchInfo* match_info, GError** error);
g_match_info_next = libglib.g_match_info_next
g_match_info_next.restype = gboolean
g_match_info_next.argtypes = [POINTER(GMatchInfo), POINTER(POINTER(GError))]

# gint g_match_info_get_match_count(const GMatchInfo* match_info);
g_match_info_get_match_count = libglib.g_match_info_get_match_count
g_match_info_get_match_count.restype = gint
g_match_info_get_match_count.argtypes = [POINTER(GMatchInfo)]

# gboolean g_match_info_is_partial_match(const GMatchInfo* match_info);
g_match_info_is_partial_match = libglib.g_match_info_is_partial_match
g_match_info_is_partial_match.restype = gboolean
g_match_info_is_partial_match.argtypes = [POINTER(GMatchInfo)]

# gchar* g_match_info_expand_references(const GMatchInfo* match_info,
#                                      const gchar* string_to_expand,
#                                      GError** error);
g_match_info_expand_references = libglib.g_match_info_expand_references
g_match_info_expand_references.restype = gchar_p
g_match_info_expand_references.argtypes = [POINTER(GMatchInfo),
                                                gchar_p,
                                                POINTER(POINTER(GError))]

# gchar* g_match_info_fetch(const GMatchInfo* match_info, gint match_num);
g_match_info_fetch = libglib.g_match_info_fetch
g_match_info_fetch.restype = gchar_p
g_match_info_fetch.argtypes = [POINTER(GMatchInfo), gint]

# gboolean g_match_info_fetch_pos(const GMatchInfo* match_info,
#                                 gint match_num,
#                                 gint* start_pos,
#                                 gint* end_pos);
g_match_info_fetch_pos = libglib.g_match_info_fetch_pos
g_match_info_fetch_pos.restype = gboolean
g_match_info_fetch_pos.argtypes = [POINTER(GMatchInfo),
                                        gint,
                                        POINTER(gint),
                                        POINTER(gint)]

# gchar* g_match_info_fetch_named(const GMatchInfo* match_info,
#                                 const gchar* name);
g_match_info_fetch_named = libglib.g_match_info_fetch_named
g_match_info_fetch_named.restype = gchar_p
g_match_info_fetch_named.argtypes = [POINTER(GMatchInfo), gchar_p]

# gboolean g_match_info_fetch_named_pos(const GMatchInfo* match_info,
#                                       const gchar* name,
#                                       gint* start_pos,
#                                       gint* end_pos);
g_match_info_fetch_named_pos = libglib.g_match_info_fetch_named_pos
g_match_info_fetch_named_pos.restype = gboolean
g_match_info_fetch_named_pos.argtypes = [POINTER(GMatchInfo),
                                              gchar_p,
                                              POINTER(gint),
                                              POINTER(gint)]

# gchar** g_match_info_fetch_all(const GMatchInfo* match_info);
g_match_info_fetch_all = libglib.g_match_info_fetch_all
g_match_info_fetch_all.restype = POINTER(gchar_p)
g_match_info_fetch_all.argtypes = [POINTER(GMatchInfo)]

# GTree* g_tree_new(GCompareFunc key_compare_func);
g_tree_new = libglib.g_tree_new
g_tree_new.restype = POINTER(GTree)
g_tree_new.argtypes = [GCompareFunc]

# GTree* g_tree_ref(GTree* tree);
g_tree_ref = libglib.g_tree_ref
g_tree_ref.restype = POINTER(GTree)
g_tree_ref.argtypes = [POINTER(GTree)]

# void g_tree_unref(GTree* tree);
g_tree_unref = libglib.g_tree_unref
g_tree_unref.restype = None
g_tree_unref.argtypes = [POINTER(GTree)]

# GTree* g_tree_new_with_data(GCompareDataFunc key_compare_func,
#                             gpointer key_compare_data);
g_tree_new_with_data = libglib.g_tree_new_with_data
g_tree_new_with_data.restype = POINTER(GTree)
g_tree_new_with_data.argtypes = [GCompareDataFunc, gpointer]

# GTree* g_tree_new_full(GCompareDataFunc key_compare_func,
#                        gpointer key_compare_data,
#                        GDestroyNotify key_destroy_func,
#                        GDestroyNotify value_destroy_func);
g_tree_new_full = libglib.g_tree_new_full
g_tree_new_full.restype = POINTER(GTree)
g_tree_new_full.argtypes = [GCompareDataFunc,
                                 gpointer,
                                 GDestroyNotify,
                                 GDestroyNotify]

# void g_tree_insert(GTree* tree, gpointer key, gpointer value);
g_tree_insert = libglib.g_tree_insert
g_tree_insert.restype = None
g_tree_insert.argtypes = [POINTER(GTree), gpointer, gpointer]

# void g_tree_replace(GTree* tree, gpointer key, gpointer value);
g_tree_replace = libglib.g_tree_replace
g_tree_replace.restype = None
g_tree_replace.argtypes = [POINTER(GTree), gpointer, gpointer]

# gint g_tree_nnodes(GTree* tree);
g_tree_nnodes = libglib.g_tree_nnodes
g_tree_nnodes.restype = gint
g_tree_nnodes.argtypes = [POINTER(GTree)]

# gint g_tree_height(GTree* tree);
g_tree_height = libglib.g_tree_height
g_tree_height.restype = gint
g_tree_height.argtypes = [POINTER(GTree)]

# gpointer g_tree_lookup(GTree* tree, gconstpointer key);
g_tree_lookup = libglib.g_tree_lookup
g_tree_lookup.restype = gpointer
g_tree_lookup.argtypes = [POINTER(GTree), gconstpointer]

# gboolean g_tree_lookup_extended(GTree* tree,
#                                 gconstpointer lookup_key,
#                                 gpointer* orig_key,
#                                 gpointer* value);
g_tree_lookup_extended = libglib.g_tree_lookup_extended
g_tree_lookup_extended.restype = gboolean
g_tree_lookup_extended.argtypes = [POINTER(GTree),
                                        gconstpointer,
                                        POINTER(gpointer),
                                        POINTER(gpointer)]

# void g_tree_foreach(GTree* tree, GTraverseFunc func, gpointer user_data);
g_tree_foreach = libglib.g_tree_foreach
g_tree_foreach.restype = None
g_tree_foreach.argtypes = [POINTER(GTree), GTraverseFunc, gpointer]

# void g_tree_traverse(GTree* tree,
#                      GTraverseFunc traverse_func,
#                      GTraverseType traverse_type,
#                      gpointer user_data);
g_tree_traverse = libglib.g_tree_traverse
g_tree_traverse.restype = None
g_tree_traverse.argtypes = [POINTER(GTree),
                                 GTraverseFunc,
                                 GTraverseType,
                                 gpointer]

# gpointer g_tree_search(GTree* tree,
#                        GCompareFunc search_func,
#                        gconstpointer user_data);
g_tree_search = libglib.g_tree_search
g_tree_search.restype = gpointer
g_tree_search.argtypes = [POINTER(GTree),
                               GCompareFunc,
                               gconstpointer]

# gboolean g_tree_remove(GTree* tree, gconstpointer key);
g_tree_remove = libglib.g_tree_remove
g_tree_remove.restype = gboolean
g_tree_remove.argtypes = [POINTER(GTree), gconstpointer]

# gboolean g_tree_steal(GTree* tree, gconstpointer key);
g_tree_steal = libglib.g_tree_steal
g_tree_steal.restype = gboolean
g_tree_steal.argtypes = [POINTER(GTree), gconstpointer]

# void g_tree_destroy(GTree* tree);
g_tree_destroy = libglib.g_tree_destroy
g_tree_destroy.restype = None
g_tree_destroy.argtypes = [POINTER(GTree)]

# GQueue* g_queue_new(void);
g_queue_new = libglib.g_queue_new
g_queue_new.restype = POINTER(GQueue)
g_queue_new.argtypes = []

# void g_queue_free(GQueue* queue);
g_queue_free = libglib.g_queue_free
g_queue_free.restype = None
g_queue_free.argtypes = [POINTER(GQueue)]

# void g_queue_free_full(GQueue* queue, GDestroyNotify free_func);
g_queue_free_full = libglib.g_queue_free_full
g_queue_free_full.restype = None
g_queue_free_full.argtypes = [POINTER(GQueue), GDestroyNotify]

# void g_queue_init(GQueue* queue);
g_queue_init = libglib.g_queue_init
g_queue_init.restype = None
g_queue_init.argtypes = [POINTER(GQueue)]

# void g_queue_clear(GQueue* queue);
g_queue_clear = libglib.g_queue_clear
g_queue_clear.restype = None
g_queue_clear.argtypes = [POINTER(GQueue)]

# gboolean g_queue_is_empty(GQueue* queue);
g_queue_is_empty = libglib.g_queue_is_empty
g_queue_is_empty.restype = gboolean
g_queue_is_empty.argtypes = [POINTER(GQueue)]

# guint g_queue_get_length(GQueue* queue);
g_queue_get_length = libglib.g_queue_get_length
g_queue_get_length.restype = guint
g_queue_get_length.argtypes = [POINTER(GQueue)]

# void g_queue_reverse(GQueue* queue);
g_queue_reverse = libglib.g_queue_reverse
g_queue_reverse.restype = None
g_queue_reverse.argtypes = [POINTER(GQueue)]

# GQueue* g_queue_copy(GQueue* queue);
g_queue_copy = libglib.g_queue_copy
g_queue_copy.restype = POINTER(GQueue)
g_queue_copy.argtypes = [POINTER(GQueue)]

# void g_queue_foreach(GQueue* queue, GFunc func, gpointer user_data);
g_queue_foreach = libglib.g_queue_foreach
g_queue_foreach.restype = None
g_queue_foreach.argtypes = [POINTER(GQueue), GFunc, gpointer]

# GList* g_queue_find(GQueue* queue, gconstpointer data);
g_queue_find = libglib.g_queue_find
g_queue_find.restype = POINTER(GList)
g_queue_find.argtypes = [POINTER(GQueue), gconstpointer]

# GList* g_queue_find_custom(GQueue* queue,
#                            gconstpointer data,
#                            GCompareFunc func);
g_queue_find_custom = libglib.g_queue_find_custom
g_queue_find_custom.restype = POINTER(GList)
g_queue_find_custom.argtypes = [POINTER(GQueue),
                                     gconstpointer,
                                     GCompareFunc]

# void g_queue_sort(GQueue* queue,
#                   GCompareDataFunc compare_func,
#                   gpointer user_data);
g_queue_sort = libglib.g_queue_sort
g_queue_sort.restype = None
g_queue_sort.argtypes = [POINTER(GQueue), GCompareDataFunc, gpointer]

# void g_queue_push_head(GQueue* queue, gpointer data);
g_queue_push_head = libglib.g_queue_push_head
g_queue_push_head.restype = None
g_queue_push_head.argtypes = [POINTER(GQueue), gpointer]

# void g_queue_push_tail(GQueue* queue, gpointer data);
g_queue_push_tail = libglib.g_queue_push_tail
g_queue_push_tail.restype = None
g_queue_push_tail.argtypes = [POINTER(GQueue), gpointer]

# void g_queue_push_nth(GQueue* queue, gpointer data, gint n);
g_queue_push_nth = libglib.g_queue_push_nth
g_queue_push_nth.restype = None
g_queue_push_nth.argtypes = [POINTER(GQueue), gpointer, gint]

# gpointer g_queue_pop_head(GQueue* queue);
g_queue_pop_head = libglib.g_queue_pop_head
g_queue_pop_head.restype = gpointer
g_queue_pop_head.argtypes = [POINTER(GQueue)]

# gpointer g_queue_pop_tail(GQueue* queue);
g_queue_pop_tail = libglib.g_queue_pop_tail
g_queue_pop_tail.restype = gpointer
g_queue_pop_tail.argtypes = [POINTER(GQueue)]

# gpointer g_queue_pop_nth(GQueue* queue, guint n);
g_queue_pop_nth = libglib.g_queue_pop_nth
g_queue_pop_nth.restype = gpointer
g_queue_pop_nth.argtypes = [POINTER(GQueue), guint]

# gpointer g_queue_peek_head(GQueue* queue);
g_queue_peek_head = libglib.g_queue_peek_head
g_queue_peek_head.restype = gpointer
g_queue_peek_head.argtypes = [POINTER(GQueue)]

# gpointer g_queue_peek_tail(GQueue* queue);
g_queue_peek_tail = libglib.g_queue_peek_tail
g_queue_peek_tail.restype = gpointer
g_queue_peek_tail.argtypes = [POINTER(GQueue)]

# gpointer g_queue_peek_nth(GQueue* queue, guint n);
g_queue_peek_nth = libglib.g_queue_peek_nth
g_queue_peek_nth.restype = gpointer
g_queue_peek_nth.argtypes = [POINTER(GQueue), guint]

# gint g_queue_index(GQueue* queue, gconstpointer data);
g_queue_index = libglib.g_queue_index
g_queue_index.restype = gint
g_queue_index.argtypes = [POINTER(GQueue), gconstpointer]

# gboolean g_queue_remove(GQueue* queue, gconstpointer data);
g_queue_remove = libglib.g_queue_remove
g_queue_remove.restype = gboolean
g_queue_remove.argtypes = [POINTER(GQueue), gconstpointer]

# guint g_queue_remove_all(GQueue* queue, gconstpointer data);
g_queue_remove_all = libglib.g_queue_remove_all
g_queue_remove_all.restype = guint
g_queue_remove_all.argtypes = [POINTER(GQueue), gconstpointer]

# void g_queue_insert_before(GQueue* queue, GList* sibling, gpointer data);
g_queue_insert_before = libglib.g_queue_insert_before
g_queue_insert_before.restype = None
g_queue_insert_before.argtypes = [POINTER(GQueue), POINTER(GList), gpointer]

# void g_queue_insert_after(GQueue* queue, GList* sibling, gpointer data);
g_queue_insert_after = libglib.g_queue_insert_after
g_queue_insert_after.restype = None
g_queue_insert_after.argtypes = [POINTER(GQueue), POINTER(GList), gpointer]

# void g_queue_insert_sorted(GQueue* queue,
#                            gpointer data,
#                            GCompareDataFunc func,
#                            gpointer user_data);
g_queue_insert_sorted = libglib.g_queue_insert_sorted
g_queue_insert_sorted.restype = None
g_queue_insert_sorted.argtypes = [POINTER(GQueue),
                                       gpointer,
                                       GCompareDataFunc,
                                       gpointer]

# void g_queue_push_head_link(GQueue* queue, GList* link_);
g_queue_push_head_link = libglib.g_queue_push_head_link
g_queue_push_head_link.restype = None
g_queue_push_head_link.argtypes = [POINTER(GQueue), POINTER(GList)]

# void g_queue_push_tail_link(GQueue* queue, GList* link_);
g_queue_push_tail_link = libglib.g_queue_push_tail_link
g_queue_push_tail_link.restype = None
g_queue_push_tail_link.argtypes = [POINTER(GQueue), POINTER(GList)]

# void g_queue_push_nth_link(GQueue* queue, gint n, GList* link_);
g_queue_push_nth_link = libglib.g_queue_push_nth_link
g_queue_push_nth_link.restype = None
g_queue_push_nth_link.argtypes = [POINTER(GQueue), gint, POINTER(GList)]

# GList* g_queue_pop_head_link(GQueue* queue);
g_queue_pop_head_link = libglib.g_queue_pop_head_link
g_queue_pop_head_link.restype = POINTER(GList)
g_queue_pop_head_link.argtypes = [POINTER(GQueue)]

# GList* g_queue_pop_tail_link(GQueue* queue);
g_queue_pop_tail_link = libglib.g_queue_pop_tail_link
g_queue_pop_tail_link.restype = POINTER(GList)
g_queue_pop_tail_link.argtypes = [POINTER(GQueue)]

# GList* g_queue_pop_nth_link(GQueue* queue, guint n);
g_queue_pop_nth_link = libglib.g_queue_pop_nth_link
g_queue_pop_nth_link.restype = POINTER(GList)
g_queue_pop_nth_link.argtypes = [POINTER(GQueue), guint]

# GList* g_queue_peek_head_link(GQueue* queue);
g_queue_peek_head_link = libglib.g_queue_peek_head_link
g_queue_peek_head_link.restype = POINTER(GList)
g_queue_peek_head_link.argtypes = [POINTER(GQueue)]

# GList* g_queue_peek_tail_link(GQueue* queue);
g_queue_peek_tail_link = libglib.g_queue_peek_tail_link
g_queue_peek_tail_link.restype = POINTER(GList)
g_queue_peek_tail_link.argtypes = [POINTER(GQueue)]

# GList* g_queue_peek_nth_link(GQueue* queue, guint n);
g_queue_peek_nth_link = libglib.g_queue_peek_nth_link
g_queue_peek_nth_link.restype = POINTER(GList)
g_queue_peek_nth_link.argtypes = [POINTER(GQueue), guint]

# gint g_queue_link_index(GQueue* queue, GList* link_);
g_queue_link_index = libglib.g_queue_link_index
g_queue_link_index.restype = gint
g_queue_link_index.argtypes = [POINTER(GQueue), POINTER(GList)]

# void g_queue_unlink(GQueue* queue, GList* link_);
g_queue_unlink = libglib.g_queue_unlink
g_queue_unlink.restype = None
g_queue_unlink.argtypes = [POINTER(GQueue), POINTER(GList)]

# void g_queue_delete_link(GQueue* queue, GList* link_);
g_queue_delete_link = libglib.g_queue_delete_link
g_queue_delete_link.restype = None
g_queue_delete_link.argtypes = [POINTER(GQueue), POINTER(GList)]

# #define g_new(struct_type, n_structs)
def g_new(struct_type, n_structs):
    return cast(g_malloc_n(n_structs, sizeof(struct_type)), struct_type)

# #define g_new0(struct_type, n_structs)
def g_new0(struct_type, n_structs):
    return cast(g_malloc0_n(n_structs, sizeof(struct_type)), struct_type)

# #define g_renew(struct_type, mem, n_structs)
def g_renew(struct_type, mem, n_structs):
    return cast(g_realloc_n(mem, n_structs, sizeof(struct_type)), struct_type)

# #define g_try_new(struct_type, n_structs)
def g_try_new(struct_type, n_structs):
    return cast(g_try_malloc_n(n_structs, sizeof(struct_type)), struct_type)

# #define g_try_new0(struct_type, n_structs)
def g_try_new0(struct_type, n_structs):
    return cast(g_try_malloc0_n(n_structs, sizeof(struct_type)), struct_type)

# #define g_try_renew(struct_type, mem, n_structs)
def g_try_renew(struct_type, mem, n_structs):
    return cast(g_try_realloc_n(mem, n_structs, sizeof(struct_type)), struct_type)

# gpointer g_malloc(gsize n_bytes);
g_malloc = libglib.g_malloc
g_malloc.restype = gpointer
g_malloc.argtypes = [gsize]

# gpointer g_malloc0(gsize n_bytes);
g_malloc0 = libglib.g_malloc0
g_malloc0.restype = gpointer
g_malloc0.argtypes = [gsize]

# gpointer g_realloc(gpointer mem, gsize n_bytes);
g_realloc = libglib.g_realloc
g_realloc.restype = gpointer
g_realloc.argtypes = [gpointer, gsize]

# gpointer g_try_malloc(gsize n_bytes);
g_try_malloc = libglib.g_try_malloc
g_try_malloc.restype = gpointer
g_try_malloc.argtypes = [gsize]

# gpointer g_try_malloc0(gsize n_bytes);
g_try_malloc0 = libglib.g_try_malloc0
g_try_malloc0.restype = gpointer
g_try_malloc0.argtypes = [gsize]

# gpointer g_try_realloc(gpointer mem, gsize n_bytes);
g_try_realloc = libglib.g_try_realloc
g_try_realloc.restype = gpointer
g_try_realloc.argtypes = [gpointer, gsize]

# gpointer g_malloc_n(gsize n_block, gsize n_block_bytes);
g_malloc_n = libglib.g_malloc_n
g_malloc_n.restype = gpointer
g_malloc_n.argtypes = [gsize, gsize]

# gpointer g_malloc0_n(gsize n_blocks, gsize n_block_bytes);
g_malloc0_n = libglib.g_malloc0_n
g_malloc0_n.restype = gpointer
g_malloc0_n.argtypes = [gsize, gsize]

# gpointer g_realloc_n(gpointer mem, gsize n_blocks, gsize n_block_bytes);
g_realloc_n = libglib.g_realloc_n
g_realloc_n.restype = gpointer
g_realloc_n.argtypes = [gpointer, gsize, gsize]

# gpointer g_try_malloc_n(gsize n_blocks, gsize n_block_bytes);
g_try_malloc_n = libglib.g_try_malloc_n
g_try_malloc_n.restype = gpointer
g_try_malloc_n.argtypes = [gsize, gsize]

# gpointer g_try_malloc0_n(gsize n_blocks, gsize n_block_bytes);
g_try_malloc0_n = libglib.g_try_malloc0_n
g_try_malloc0_n.restype = gpointer
g_try_malloc0_n.argtypes = [gsize, gsize]

# gpointer g_try_realloc_n(gpointer mem, gsize n_blocks, gsize n_block_bytes);
g_try_realloc_n = libglib.g_try_realloc_n
g_try_realloc_n.restype = gpointer
g_try_realloc_n.argtypes = [gpointer, gsize, gsize]

# void g_free(gpointer mem);
g_free = libglib.g_free
g_free.restype = None
g_free.argtypes = [gpointer]

# void g_clear_pointer(gpointer* pp, GDestroyNotify destroy);
g_clear_pointer = libglib.g_clear_pointer
g_clear_pointer.restype = None
g_clear_pointer.argtypes = [POINTER(gpointer), GDestroyNotify]

# gpointer g_memdup(gconstpointer mem, guint byte_size);
g_memdup = libglib.g_memdup
g_memdup.restype = gpointer
g_memdup.argtypes = [gconstpointer, guint]

# void g_mem_set_vtable(GMemVTable* vtable);
g_mem_set_vtable = libglib.g_mem_set_vtable
g_mem_set_vtable.restype = None
g_mem_set_vtable.argtypes = [POINTER(GMemVTable)]

# gboolean g_mem_is_system_malloc(void);
g_mem_is_system_malloc = libglib.g_mem_is_system_malloc
g_mem_is_system_malloc.restype = gboolean
g_mem_is_system_malloc.argtypes = []

# gboolean g_mem_gc_friendly;
g_mem_gc_friendly = gboolean.in_dll(libglib, 'g_mem_gc_friendly')

# gchar* g_strdup(const gchar* str);
g_strdup = libglib.g_strdup
g_strdup.restype = gchar_p
g_strdup.argtypes = [gchar_p]

# gchar* g_strndup(const gchar* str, gsize n);
g_strndup = libglib.g_strndup
g_strndup.restype = gchar_p
g_strndup.argtypes = [gchar_p, gsize]

# gchar** g_strdupvy(gchar** str_array);
g_strdupv = libglib.g_strdupv
g_strdupv.restype = POINTER(gchar_p)
g_strdupv.argtypes = [POINTER(gchar_p)]

# gchar* g_strnfill(gsize length, gchar fill_char);
g_strnfill = libglib.g_strnfill
g_strnfill.restype = gchar_p
g_strnfill.argtypes = [gsize, gchar]

# gchar* g_strstr_len(const gchar* haystack,
#                     gssize haystack_len,
#                     const gchar* needle);
g_strstr_len = libglib.g_strstr_len
g_strstr_len.restype = gchar_p
g_strstr_len.argtypes = [gchar_p, gssize, gchar_p]

# gchar* g_strrstr(const gchar* haystack,
#                  gssize haystack_len,
#                  const gchar* needle);
g_strrstr = libglib.g_strrstr
g_strrstr.restype = gchar_p
g_strrstr.argtypes = [gchar_p, gssize, gchar_p]

# gboolean g_str_has_prefix(const gchar* str, const gchar* prefix);
g_str_has_prefix = libglib.g_str_has_prefix
g_str_has_prefix.restype = gboolean
g_str_has_prefix.argtypes = [gchar_p, gchar_p]

# gboolean g_str_has_suffix(const gchar* str, const gchar* suffix);
g_str_has_suffix = libglib.g_str_has_suffix
g_str_has_suffix.restype = gboolean
g_str_has_suffix.argtypes = [gchar_p, gchar_p]

# int g_strcmp0(const char* str1, const char* str2);
g_strcmp0 = libglib.g_strcmp0
g_strcmp0.restype = c_int
g_strcmp0.argtypes = [c_char_p, c_char_p]

# gchar* g_str_to_ascii(const gchar* str, const gchar* from_locale);
g_str_to_ascii = libglib.g_str_to_ascii
g_str_to_ascii.restype = gchar_p
g_str_to_ascii.argtypes = [gchar_p, gchar_p]

# gchar** g_str_tokenize_and_fold(const gchar* string,
#                                 const gchar* translit_locale,
#                                 gchar*** ascii_alternates);
g_str_tokenize_and_fold = libglib.g_str_tokenize_and_fold
g_str_tokenize_and_fold.restype = POINTER(gchar_p)
g_str_tokenize_and_fold.argtypes = [gchar_p,
                                         gchar_p,
                                         POINTER(POINTER(gchar_p))]

# gboolean g_str_match_string(const gchar* search_term,
#                             const gchar* potential_hit,
#                             gboolean accept_alternates);
g_str_match_string = libglib.g_str_match_string
g_str_match_string.restype = gboolean
g_str_match_string.argtypes = [gchar_p, gchar_p, gboolean]

# gsize g_strlcpy(gchar* dest, const gchar* src, gsize dest_size);
g_strlcpy = libglib.g_strlcpy
g_strlcpy.restype = gsize
g_strlcpy.argtypes = [gchar_p, gchar_p, gsize]

# gsize g_strlcat(gchar* dest, const gchar* src, gsize dest_size);
g_strlcat = libglib.g_strlcat
g_strlcat.restype = gsize
g_strlcat.argtypes = [gchar_p, gchar_p, gsize]

# gchar* g_strdup_printf(const gchar* format, ...);
_g_strdup_printf = libglib.g_strdup_printf
_g_strdup_printf.restype = gchar_p

def g_strdup_printf(fmt, *args):
    _g_strdup_printf.argtypes = [gchar_p] + make_type_list(args)
    return _g_strdup_printf(fmt, *args)

# gint g_printf(const gchar* format, ...);
_g_printf = libglib.g_printf
_g_printf.restype = gint

def g_printf(fmt, *args):
    _g_printf.argtypes = [g_char_p] + make_type_list(args)
    return _g_printf(fmt, *args)

# gint g_fprintf(FILE* file, const gchar* format, ...);
_g_fprintf = libglib.g_fprintf
_g_fprintf.restype = gint

def g_fprintf(file, fmt, *args):
    _g_fprintf.argtypes = [c_void_p, gchar_p] + make_type_list(args)
    return _g_fprintf(file, fmt, *args)

# gint g_sprintf(gchar* string, const gchar* format, ...);
_g_sprintf = libglib.g_sprintf
_g_sprintf.restype = gint

def g_sprintf(string, fmt, *args):
    _g_sprintf.argtypes = [gchar_p, gchar_p] + make_type_list(args)
    return _g_sprintf(string, fmt, *args)

# gint g_snprintf(gchar* string, gulong n, const gchar* format, ...);
_g_snprintf = libglib.g_snprintf
_g_snprintf.restype = gint

def g_snprintf(string, n, fmt, *args):
    _g_snprintf.argtypes = [gchar_p, gulong, gchar_p] + make_type_list(args)
    return _g_snprintf(string, n, fmt, *args)

# gboolean g_str_is_ascii(const gchar* str);
g_str_is_ascii = libglib.g_str_is_ascii
g_str_is_ascii.restype = gboolean
g_str_is_ascii.argtypes = [gchar_p]

# gboolean g_ascii_isalnum(gchar c);
#g_ascii_isalnum = libglib.g_ascii_isalnum
#g_ascii_isalnum.restype = gboolean
#g_ascii_isalnum.argtypes = [gchar]

# gboolean g_ascii_isalpha(gchar c);
#g_ascii_isalpha = libglib.g_ascii_isalpha
#g_ascii_isalpha.restype = gboolean
#g_ascii_isalpha.argtypes = [gchar]

# gboolean g_ascii_iscntrl(gchar c);
#g_ascii_iscntrl = libglib.g_ascii_iscntrl
#g_ascii_iscntrl.restype = gboolean
#g_ascii_iscntrl.argtypes = [gchar]

# gboolean g_ascii_isdigit(gchar c);
#g_ascii_isdigit = libglib.g_ascii_isdigit
#g_ascii_isdigit.restype = gboolean
#g_ascii_isdigit.argtypes = [gchar]

# gboolean g_ascii_isgraph(gchar c);
#g_ascii_isgraph = libglib.g_ascii_isgraph
#g_ascii_isgraph.restype = gboolean
#g_ascii_isgraph.argtypes = [gchar]

# gboolean g_ascii_islower(gchar c);
#g_ascii_islower = libglib.g_ascii_islower
#g_ascii_islower.restype = gboolean
#g_ascii_islower.argtypes = [gchar]

# gboolean g_ascii_isprint(gchar c);
#g_ascii_isprint = libglib.g_ascii_isprint
#g_ascii_isprint.restype = gboolean
#g_ascii_isprint.argtypes = [gchar]

# gboolean g_ascii_ispunct(gchar c);
#g_ascii_ispunct = libglib.g_ascii_ispunct
#g_ascii_ispunct.restype = gboolean
#g_ascii_ispunct.argtypes = [gchar]

# gboolean g_ascii_isspace(gchar c);
#g_ascii_isspace = libglib.g_ascii_isspace
#g_ascii_isspace.restype = gboolean
#g_ascii_isspace.argtypes = [gchar]

# gboolean g_ascii_isupper(gchar c);
#g_ascii_isupper = libglib.g_ascii_isupper
#g_ascii_isupper.restype = gboolean
#g_ascii_isupper.argtypes = [gchar]

# gboolean g_ascii_isxdigit(gchar c);
#g_ascii_isxdigit = libglib.g_ascii_isxdigit
#g_ascii_isxdigit.restype = gboolean
#g_ascii_isxdigit.argtypes = [gchar]

# gint g_ascii_digit_value(gchar c);
#g_ascii_digit_value = libglib.g_ascii_digit_value
#g_ascii_digit_value.restype = gint
#g_ascii_digit_value.argtypes = [gchar]

# gint g_ascii_xdigit_value(gchar c);
#g_ascii_xdigit_value = libglib.g_ascii_xdigit_value
#g_ascii_xdigit_value.restype = gint
#g_ascii_xdigit_value.argtypes = [gchar]

# gint g_ascii_strcasecmp(const gchar* s1, const gchar* s2);
g_ascii_strcasecmp = libglib.g_ascii_strcasecmp
g_ascii_strcasecmp.restype = gint
g_ascii_strcasecmp.argtypes = [gchar_p, gchar_p]

# gint g_ascii_strncasecmp(const gchar* s1, const gchar* s2, gsize n);
g_ascii_strncasecmp = libglib.g_ascii_strncasecmp
g_ascii_strncasecmp.restype = gint
g_ascii_strncasecmp.argtypes = [gchar_p, gchar_p, gsize]

# gchar* g_ascii_strup(const gchar* str, gssize len);
g_ascii_strup = libglib.g_ascii_strup
g_ascii_strup.restype = gchar_p
g_ascii_strup.argtypes = [gchar_p, gssize]

# gchar* g_ascii_strdown(const gchar* str, gssize len);
g_ascii_strdown = libglib.g_ascii_strdown
g_ascii_strdown.restype = gchar_p
g_ascii_strdown.argtypes = [gchar_p, gssize];

# gchar g_ascii_tolower(gchar c);
g_ascii_tolower = libglib.g_ascii_tolower
g_ascii_tolower.restype = gchar
g_ascii_tolower.argtypes = [gchar]

# gchar g_ascii_toupper(gchar c);
g_ascii_toupper = libglib.g_ascii_toupper
g_ascii_toupper.restype = gchar
g_ascii_toupper.argtypes = [gchar]

# GString* g_string_ascii_up(GString* string);
g_string_ascii_up = libglib.g_string_ascii_up
g_string_ascii_up.restype = POINTER(GString)
g_string_ascii_up.argtypes = [POINTER(GString)]

# GString* g_string_ascii_down(GString* string);
g_string_ascii_down = libglib.g_string_ascii_down
g_string_ascii_down.restype = POINTER(GString)
g_string_ascii_down.argtypes = [POINTER(GString)]

# gchar* g_strup(gchar* string);
g_strup = libglib.g_strup
g_strup.restype = gchar_p
g_strup.argtypes = [gchar_p]

# gchar* g_strdown(gchar* string);
g_strdown = libglib.g_strdown
g_strdown.restype = gchar_p
g_strdown.argtypes = [gchar_p]

# gint g_strcasecmp(const gchar* s1, const gchar* s2);
g_strcasecmp = libglib.g_strcasecmp
g_strcasecmp.restype = gint
g_strcasecmp.argtypes = [gchar_p, gchar_p]

# gint g_strncasecmp(const gchar* s1, const gchar* s2, guint n);
g_strncasecmp = libglib.g_strncasecmp
g_strncasecmp.restype = gint
g_strncasecmp.argtypes = [gchar_p, gchar_p, guint]

# gchar* g_strreverse(gchar* string);
g_strreverse = libglib.g_strreverse
g_strreverse.restype = gchar_p
g_strreverse.argtypes = [gchar_p]

# gint64 g_ascii_strtoll(const gchar* nptr, gchar** endptr, guint base);
g_ascii_strtoll = libglib.g_ascii_strtoll
g_ascii_strtoll.restype = gint64
g_ascii_strtoll.argtypes = [gchar_p, POINTER(gchar_p), guint]

# guint64 g_ascii_strtoull(const gchar* nptr, ghcar** endptr, guint base);
g_ascii_strtoull = libglib.g_ascii_strtoull
g_ascii_strtoull.restype = guint64
g_ascii_strtoull.argtypes = [gchar_p, POINTER(gchar_p), guint]

# gdouble g_ascii_strtod(const gchar* nptr, gchar** endptr);
g_ascii_strtod = libglib.g_ascii_strtod
g_ascii_strtod.restype = gdouble
g_ascii_strtod.argtypes = [gchar_p, POINTER(gchar_p)]

# gchar* g_ascii_dtostr(gchar* buffer, gint buf_len, gdouble d);
g_ascii_dtostr = libglib.g_ascii_dtostr
g_ascii_dtostr.restype = gchar_p
g_ascii_dtostr.argtypes = [gchar_p, gint, gdouble]

# gchar* g_ascii_formatd(gchar* buffer,
#                        gint buf_len,
#                        const gchar* format,
#                        gdouble d);
g_ascii_formatd = libglib.g_ascii_formatd
g_ascii_formatd.restype = gchar_p
g_ascii_formatd.argtypes = [gchar_p, gint, gchar_p, gdouble]

# gdouble g_strtod(const gchar* nptr, gchar** endptr);
g_strtod = libglib.g_strtod
g_strtod.restype = gdouble
g_strtod.argtypes = [gchar_p, POINTER(gchar_p)]

# gboolean g_ascii_string_to_signed(const gchar* str,
#                                   guint base,
#                                   gint64 min,
#                                   gint64 max,
#                                   gint64* out_num,
#                                   GError** error);
g_ascii_string_to_signed = libglib.g_ascii_string_to_signed
g_ascii_string_to_signed.restype = gboolean
g_ascii_string_to_signed.argtypes = [gchar_p,
                                          guint,
                                          gint64,
                                          gint64,
                                          POINTER(gint64),
                                          POINTER(POINTER(GError))]

# gboolean g_ascii_string_to_unsigned(const gchar* str,
#                                     guint base,
#                                     guint64 min,
#                                     guint64 max,
#                                     guint64* out_num,
#                                     GError** error);
g_ascii_string_to_unsigned = libglib.g_ascii_string_to_unsigned
g_ascii_string_to_unsigned.restype = gboolean
g_ascii_string_to_unsigned.argtypes = [gchar_p,
                                            guint,
                                            guint64,
                                            guint64,
                                            POINTER(guint64),
                                            POINTER(POINTER(GError))]

# gchar* g_strchug(gchar* string);
g_strchug = libglib.g_strchug
g_strchug.restype = gchar_p
g_strchug.argtypes = [gchar_p]

# gchar* g_strchomp(gchar* string);
g_strchomp = libglib.g_strchomp
g_strchomp.restype = gchar_p
g_strchomp.argtypes = [gchar_p]

# #define g_strstrip(string)
def g_strstrip(string):
    return g_strchug(g_strchomp(string))

# gchar* g_strdelimit(gchar* string,
#                     const gchar* delimiters,
#                     gchar new_delimiter);
g_strdelimit = libglib.g_strdelimit
g_strdelimit.restype = gchar_p
g_strdelimit.argtypes = [gchar_p, gchar_p, gchar]

# gchar* g_escape(const gchar* source, const gchar* exceptions);
#g_escape = libglib.g_escape
#g_escape.restype = gchar_p
#g_escape.argtypes = [gchar_p, gchar_p]

# gchar* g_strcompress(const gchar* source);
g_strcompress = libglib.g_strcompress
g_strcompress.restype = gchar_p
g_strcompress.argtypes = [gchar_p]

# gchar* g_strcanon(gchar* string, const gchar* valid_chrs, gchar substitutor);
g_strcanon = libglib.g_strcanon
g_strcanon.restype = gchar_p
g_strcanon.argtypes = [gchar_p, gchar_p, gchar]

# gchar** g_strsplit(const gchar* string,
#                    const gchar* delimiter,
#                    gint max_tokens);
g_strsplit = libglib.g_strsplit
g_strsplit.restype = POINTER(gchar_p)
g_strsplit.argtypes = [gchar_p, gchar_p, gint]

# gchar** g_strsplit_set(const gchar* string,
#                        const gchar* delimiters,
#                        gint max_tokens);
g_strsplit_set = libglib.g_strsplit_set
g_strsplit_set.restype = POINTER(gchar_p)
g_strsplit_set.argtypes = [gchar_p, gchar_p, gint]

# void g_strfreev(gchar** str_array);
g_strfreev = libglib.g_strfreev
g_strfreev.restype = None
g_strfreev.argtypes = [POINTER(gchar_p)]

# gchar* g_strconcat(const gchar* string1, ...);
_g_strconcat = libglib.g_strconcat
_g_strconcat.restype = gchar_p

def g_strconcat(string1, *args):
    _g_strconcat.argtypes = [gchar_p] * (len(args) + 1)
    return _g_strconcat(string1, *args)

# gchar* g_strjoin(const gchar* separator, ...);
_g_strjoin = libglib.g_strjoin
_g_strjoin.restype = gchar_p

def g_strjoin(separator, *args):
    _g_strjoin.argtypes = [gchar_p] * (len(args) + 1)
    return _g_strjoin(separator, *args)

# gchar* g_strjoinv(const gchar* separator, gchar** str_array);
g_strjoinv = libglib.g_strjoinv
g_strjoinv.restype = gchar_p
g_strjoinv.argtypes = [gchar_p, POINTER(gchar_p)]

# guint g_strv_length(gchar** str_array);
g_strv_length = libglib.g_strv_length
g_strv_length.restype = guint
g_strv_length.argtypes = [POINTER(gchar_p)]

# gboolean g_strv_contains(const gchar* const* strv, const gchar* str);
g_strv_contains = libglib.g_strv_contains
g_strv_contains.restype = gboolean
g_strv_contains.argtypes = [POINTER(gchar_p), gchar_p]

# const gchar* g_strerror(gint errnum);
g_strerror = libglib.g_strerror
g_strerror.restype = gchar_p
g_strerror.argtypes = [gint]

# const gchar* g_strsignal(gint signum);
g_strsignal = libglib.g_strsignal
g_strsignal.restype = gchar_p
g_strsignal.argtypes = [gint]

# #define G_ASCII_DTOSTR_BUF_SIZE (29 + 10)
G_ASCII_DTOSTR_BUF_SIZE = 29 + 10

# #define G_STR_DELIMITERS "_-|> <."
G_STR_DELIMITERS = b'_-|> <.'

# #define FALSE (0)
FALSE = gboolean(0)
FALSE = FALSE

# #define TRUE (!FALSE)
TRUE = gboolean(1)
TRUE = gboolean(1)

# gchar* g_convert(const gchar* str,
#                  gssize len,
#                  const gchar* to_codeset,
#                  const gchar* from_codeset,
#                  gsize* bytes_read,
#                  gsize* bytes_written,
#                  GError** error);
g_convert = libglib.g_convert
g_convert.restype = gchar_p
g_convert.argtypes = [gchar_p,
                           gssize,
                           gchar_p,
                           gchar_p,
                           POINTER(gsize),
                           POINTER(gsize),
                           POINTER(POINTER(GError))]

# gchar* g_convert_with_fallback(const gchar* str,
#                                gssize len,
#                                const gchar* to_codeset,
#                                const gchar* from_codeset,
#                                const gchar* fallback,
#                                gsize* bytes_read,
#                                gsize* bytes_written,
#                                GError** error);
g_convert_with_fallback = libglib.g_convert_with_fallback
g_convert_with_fallback.restype = gchar_p
g_convert_with_fallback.argtypes = [gchar_p,
                                         gssize,
                                         gchar_p,
                                         gchar_p,
                                         gchar_p,
                                         POINTER(gsize),
                                         POINTER(gsize),
                                         POINTER(POINTER(GError))]

# gchar* g_convert_with_iconv(const gchar* str,
#                             gssize len,
#                             GIConv converter,
#                             gsize* bytes_read,
#                             gsize* bytes_written,
#                             GError** error);
g_convert_with_iconv = libglib.g_convert_with_iconv
g_convert_with_iconv.restype = gchar_p
g_convert_with_iconv.argtypes = [gchar_p,
                                      gssize,
                                      GIConv,
                                      POINTER(gsize),
                                      POINTER(gsize),
                                      POINTER(POINTER(GError))]

# GIConv g_iconv_open(const gchar* to_codeset, const gchar* from_codeset);
g_iconv_open = libglib.g_iconv_open
g_iconv_open.restype = GIConv
g_iconv_open.argtypes = [gchar_p, gchar_p]

# gsize g_iconv(GIConv converter,
#               gchar** inbuf,
#               gsize* inbytes_left,
#               gchar** outbuf,
#               gsize* outbytes_left);
g_iconv = libglib.g_iconv
g_iconv.restype = gsize
g_iconv.argtypes = [GIConv,
                         POINTER(gchar_p),
                         POINTER(gsize),
                         POINTER(gchar_p),
                         POINTER(gsize)]

# gint g_iconv_close(GIConv converter);
g_iconv_close = libglib.g_iconv_close
g_iconv_close.restype = gint
g_iconv_close.argtypes = [GIConv]

# gchar* g_locale_to_utf8(const gchar* opsysstring,
#                         gssize len,
#                         gsize* bytes_read,
#                         gsize* bytes_written,
#                         GError** error);
g_locale_to_utf8 = libglib.g_locale_to_utf8
g_locale_to_utf8.restype = gchar_p
g_locale_to_utf8.argtypes = [gchar_p,
                                  gssize,
                                  POINTER(gsize),
                                  POINTER(gsize),
                                  POINTER(POINTER(GError))]

# gchar* g_filename_to_utf8(const gchar* opsysstring,
#                           gssize len,
#                           gsize* bytes_read,
#                           gsize* bytes_written,
#                           GError** error);
g_filename_to_utf8 = libglib.g_filename_to_utf8
g_filename_to_utf8.restype = gchar_p
g_filename_to_utf8.argtypes = [gchar_p,
                                    gssize,
                                    POINTER(gsize),
                                    POINTER(gsize),
                                    POINTER(POINTER(GError))]

# gchar* g_filename_from_utf8(const gchar* utf8string,
#                             gssize len,
#                             gsize* bytes_read,
#                             gsize* bytes_written,
#                             GError** error);
g_filename_from_utf8 = libglib.g_filename_from_utf8
g_filename_from_utf8.restype = gchar_p
g_filename_from_utf8.argtypes = [gchar_p,
                                      gssize,
                                      POINTER(gsize),
                                      POINTER(gsize),
                                      POINTER(POINTER(GError))]

# gboolean g_get_filename_charsets(const gchar*** charsets);
g_get_filename_charsets = libglib.g_get_filename_charsets
g_get_filename_charsets.restype = gboolean
g_get_filename_charsets.argtypes = [POINTER(POINTER(gchar_p))]

# gchar* g_filename_display_name(const gchar* filename);
g_filename_display_name = libglib.g_filename_display_name
g_filename_display_name.restype = gchar_p
g_filename_display_name.argtypes = [gchar_p]

# gchar* g_filename_display_basename(const gchar* filename);
g_filename_display_basename = libglib.g_filename_display_basename
g_filename_display_basename.restype = gchar_p
g_filename_display_basename.argtypes = [gchar_p]

# gchar* g_locale_from_utf8(const gchar* utf8string,
#                           gssize len,
#                           gsize* bytes_read,
#                           gsize* bytes_written,
#                           GError** error);
g_locale_from_utf8 = libglib.g_locale_from_utf8
g_locale_from_utf8.restype = gchar_p
g_locale_from_utf8.argtypes = [gchar_p,
                                    gssize,
                                    POINTER(gsize),
                                    POINTER(gsize),
                                    POINTER(POINTER(GError))]

# gboolean g_get_charset(const char** charset);
g_get_charset = libglib.g_get_charset
g_get_charset.restype = gboolean
g_get_charset.argtypes = [POINTER(c_char_p)]

# gchar* g_get_codeset(void);
g_get_codeset = libglib.g_get_codeset
g_get_codeset.restype = gchar_p
g_get_codeset.argtypes = []

# gboolean g_unichar_validate(gunichar ch);
g_unichar_validate = libglib.g_unichar_validate
g_unichar_validate.restype = gboolean
g_unichar_validate.argtypes = [gunichar]

# gboolean g_unichar_isalnum(gunichar c);
g_unichar_isalnum = libglib.g_unichar_isalnum
g_unichar_isalnum.restype = gboolean
g_unichar_isalnum.argtypes = [gunichar]

# gboolean g_unichar_isalpha(gunichar c);
g_unichar_isalpha = libglib.g_unichar_isalpha
g_unichar_isalpha.restype = gboolean
g_unichar_isalpha.argtypes = [gunichar]

# gboolean g_unichar_iscntrl(gunichar c);
g_unichar_iscntrl = libglib.g_unichar_iscntrl
g_unichar_iscntrl.restype = gboolean
g_unichar_iscntrl.argtypes = [gunichar]

# gboolean g_unichar_isdefined(gunichar c);
g_unichar_isdefined = libglib.g_unichar_isdefined
g_unichar_isdefined.restype = gboolean
g_unichar_isdefined.argtypes = [gunichar]

# gboolean g_unichar_isdigit(gunichar c);
g_unichar_isdigit = libglib.g_unichar_isdigit
g_unichar_isdigit.restype = gboolean
g_unichar_isdigit.argtypes = [gunichar]

# gboolean g_unichar_isgraph(gunichar c);
g_unichar_isgraph = libglib.g_unichar_isgraph
g_unichar_isgraph.restype = gboolean
g_unichar_isgraph.argtypes = [gunichar]

# gboolean g_unichar_islower(gunichar c);
g_unichar_islower = libglib.g_unichar_islower
g_unichar_islower.restype = gboolean
g_unichar_islower.argtypes = [gunichar]

# gboolean g_unichar_ismark(gunichar c);
g_unichar_ismark = libglib.g_unichar_ismark
g_unichar_ismark.restype = gboolean
g_unichar_ismark.argtypes = [gunichar]

# gboolean g_unichar_isprint(gunichar c);
g_unichar_isprint = libglib.g_unichar_isprint
g_unichar_isprint.restype = gboolean
g_unichar_isprint.argtypes = [gunichar]

# gboolean g_unichar_ispunct(gunichar c);
g_unichar_ispunct = libglib.g_unichar_ispunct
g_unichar_ispunct.restype = gboolean
g_unichar_ispunct.argtypes = [gunichar]

# gboolean g_unichar_isspace(gunichar c);
g_unichar_isspace = libglib.g_unichar_isspace
g_unichar_isspace.restype = gboolean
g_unichar_isspace.argtypes = [gunichar]

# gboolean g_unichar_istitle(gunichar c);
g_unichar_istitle = libglib.g_unichar_istitle
g_unichar_istitle.restype = gboolean
g_unichar_istitle.argtypes = [gunichar]

# gboolean g_unichar_isupper(gunichar c);
g_unichar_isupper = libglib.g_unichar_isupper
g_unichar_isupper.restype = gboolean
g_unichar_isupper.argtypes = [gunichar]

# gboolean g_unichar_isxdigit(gunichar c);
g_unichar_isxdigit = libglib.g_unichar_isxdigit
g_unichar_isxdigit.restype = gboolean
g_unichar_isxdigit.argtypes = [gunichar]

# gboolean g_unichar_iswide(gunichar c);
g_unichar_iswide = libglib.g_unichar_iswide
g_unichar_iswide.restype = gboolean
g_unichar_iswide.argtypes = [gunichar]

# gboolean g_unichar_iswide_cjk(gunichar c);
g_unichar_iswide_cjk = libglib.g_unichar_iswide_cjk
g_unichar_iswide_cjk.restype = gboolean
g_unichar_iswide_cjk.argtypes = [gunichar]

# gboolean g_unichar_iszerowidth(gunichar c);
g_unichar_iszerowidth = libglib.g_unichar_iszerowidth
g_unichar_iszerowidth.restype = gboolean
g_unichar_iszerowidth.argtypes = [gunichar]

# gunichar g_unichar_toupper(gunichar c);
g_unichar_toupper = libglib.g_unichar_toupper
g_unichar_toupper.restype = gunichar
g_unichar_toupper.argtypes = [gunichar]

# gunichar g_unichar_tolower(gunichar c);
g_unichar_tolower = libglib.g_unichar_tolower
g_unichar_tolower.restype = gunichar
g_unichar_tolower.argtypes = [gunichar]

# gunichar g_unichar_totitle(gunichar c);
g_unichar_totitle = libglib.g_unichar_totitle
g_unichar_totitle.restype = gunichar
g_unichar_totitle.argtypes = [gunichar]

# gint g_unichar_digit_value(gunichar c);
g_unichar_digit_value = libglib.g_unichar_digit_value
g_unichar_digit_value.restype = gint
g_unichar_digit_value.argtypes = [gunichar]

# gint g_unichar_xdigit_value(gunichar c);
g_unichar_xdigit_value = libglib.g_unichar_xdigit_value
g_unichar_xdigit_value.restype = gint
g_unichar_xdigit_value.argtypes = [gunichar]

# gboolean g_unichar_compose(gunichar a, gunichar b, gunichar* ch);
g_unichar_compose = libglib.g_unichar_compose
g_unichar_compose.restype = gboolean
g_unichar_compose.argtypes = [gunichar, gunichar, gunichar_p]

# gboolean g_unichar_decompose(gunichar ch, gunichar* a, gunichar* b);
g_unichar_decompose = libglib.g_unichar_decompose
g_unichar_decompose.restype = gboolean
g_unichar_decompose.argtypes = [gunichar, gunichar_p, gunichar_p]

# gsize g_unichar_fully_decompose(gunichar ch,
#                                 gboolean compat,
#                                 gunichar* result,
#                                 gsize result_len);
g_unichar_fully_decompose = libglib.g_unichar_fully_decompose
g_unichar_fully_decompose.restype = gsize
g_unichar_fully_decompose.argtypes = [gunichar,
                                           gboolean,
                                           gunichar_p,
                                           gsize]

# GUnicodeType g_unichar_type(gunichar c);
g_unichar_type = libglib.g_unichar_type
g_unichar_type.restype = GUnicodeType
g_unichar_type.argtypes = [gunichar]

# GUnicodeBreakType g_unichar_break_type(gunichar c);
g_unichar_break_type = libglib.g_unichar_break_type
g_unichar_break_type.restype = GUnicodeBreakType
g_unichar_break_type.argtypes = [gunichar]

# gint g_unichar_combining_class(gunichar uc);
g_unichar_combining_class = libglib.g_unichar_combining_class
g_unichar_combining_class.restype = gint
g_unichar_combining_class.argtypes = [gunichar]

# void g_unicode_canonical_ordering(gunichar* string, gsize len);
g_unicode_canonical_ordering = libglib.g_unicode_canonical_ordering
g_unicode_canonical_ordering.restype = None
g_unicode_canonical_ordering.argtypes = [gunichar_p, gsize]

# gunichar* g_unicode_canonical_decomposition(gunichar ch, gsize* result_len);
g_unicode_canonical_decomposition = libglib.g_unicode_canonical_decomposition
g_unicode_canonical_decomposition.restype = gunichar_p
g_unicode_canonical_decomposition.argtypes = [gunichar, POINTER(gsize)]

# gboolean g_unichar_get_mirror_char(gunichar ch, gunichar* mirrored_ch);
g_unichar_get_mirror_char = libglib.g_unichar_get_mirror_char
g_unichar_get_mirror_char.restype = gboolean
g_unichar_get_mirror_char.argtypes = [gunichar, gunichar_p]

# GUnicodeScript g_unichar_get_script(gunichar ch);
g_unichar_get_script = libglib.g_unichar_get_script
g_unichar_get_script.restype = GUnicodeScript
g_unichar_get_script.argtypes = [gunichar]

# GUnicodeScript g_unichar_script_from_iso15924(guint32 iso15924);
#g_unichar_script_from_iso15924 = libglib.g_unichar_script_from_iso15924
#g_unichar_script_from_iso15924.restype = GUnicodeScript
#g_unichar_script_from_iso15924.argtypes = [guint32]

# guint32 g_unicode_script_to_iso15924(GUnicodeScript script);
#g_unicode_script_to_iso15924 = libglib.g_unicode_script_to_iso15924
#g_unicode_script_to_iso15924.restype = guint32
#g_unicode_script_to_iso15924.argtypes = [GUnicodeScript]

# gunichar g_utf8_get_char(const gchar* p);
g_utf8_get_char = libglib.g_utf8_get_char
g_utf8_get_char.restype = gunichar
g_utf8_get_char.argtypes = [gchar_p]

# gunichar g_utf8_get_char_validated(const gchar* p, gssize max_len);
g_utf8_get_char_validated = libglib.g_utf8_get_char_validated
g_utf8_get_char_validated.restype = gunichar
g_utf8_get_char_validated.argtypes = [gchar_p, gssize]

# gchar* g_utf8_offset_to_pointer(const gchar* str, glong offset);
g_utf8_offset_to_pointer = libglib.g_utf8_offset_to_pointer
g_utf8_offset_to_pointer.restype = gchar_p
g_utf8_offset_to_pointer.argtypes = [gchar_p, glong]

# glong g_utf8_pointer_to_offset(cosnt gchar* str, const gchar* pos);
g_utf8_pointer_to_offset = libglib.g_utf8_pointer_to_offset
g_utf8_pointer_to_offset.restype = glong
g_utf8_pointer_to_offset.argtypes = [gchar_p, gchar_p]

# gchar* g_utf8_prev_char(const gchar* p);
g_utf8_prev_char = libglib.g_utf8_prev_char
g_utf8_prev_char.restype = gchar_p
g_utf8_prev_char.argtypes = [gchar_p]

# gchar* g_utf8_find_next_char(const gchar* p, const gchar* end);
g_utf8_find_next_char = libglib.g_utf8_find_next_char
g_utf8_find_next_char.restype = gchar_p
g_utf8_find_next_char.argtypes = [gchar_p, gchar_p]

# gchar* g_utf8_find_prev_char(const gchar* str, const gchar* p);
g_utf8_find_prev_char = libglib.g_utf8_find_prev_char
g_utf8_find_prev_char.restype = gchar_p
g_utf8_find_prev_char.argtypes = [gchar_p, gchar_p]

# glong g_utf8_strlen(const gchar* p, gssize max);
g_utf8_strlen = libglib.g_utf8_strlen
g_utf8_strlen.restype = glong
g_utf8_strlen.argtypes = [gchar_p, gssize]

# gchar* g_utf8_strncpy(gchar* dest, const gchar* src, gsize n);
g_utf8_strncpy = libglib.g_utf8_strncpy
g_utf8_strncpy.restype = gchar_p
g_utf8_strncpy.argtypes = [gchar_p, gchar_p, gsize]

# gchar* g_utf8_strchr(const gchar* p, gssize len, gunichar c);
g_utf8_strchr = libglib.g_utf8_strchr
g_utf8_strchr.restype = gchar_p
g_utf8_strchr.argtypes = [gchar_p, gssize, gunichar]

# gchar* g_utf8_strrchr(const gchar* p, gssize len, gunichar c);
g_utf8_strrchr = libglib.g_utf8_strrchr
g_utf8_strrchr.restype = gchar_p
g_utf8_strrchr.argtypes = [gchar_p, gssize, gunichar]

# gchar* g_utf8_strreverse(const gchar* str, gssize len);
g_utf8_strreverse = libglib.g_utf8_strreverse
g_utf8_strreverse.restype = gchar_p
g_utf8_strreverse.argtypes = [gchar_p, gssize]

# gchar* g_utf8_substring(const gchar* str, glong start_pos, glong end_pos);
g_utf8_substring = libglib.g_utf8_substring
g_utf8_substring.restype = gchar_p
g_utf8_substring.argtypes = [gchar_p, glong, glong]

# gboolean g_utf8_validate(const gchar* str, gssize max_len, const gchar** end);
g_utf8_validate = libglib.g_utf8_validate
g_utf8_validate.restype = gboolean
g_utf8_validate.argtypes = [gchar_p, gssize, POINTER(gchar_p)]

# gchar* g_utf8_make_valid(const gchar* str, gssize len);
g_utf8_make_valid = libglib.g_utf8_make_valid
g_utf8_make_valid.restype = gchar_p
g_utf8_make_valid.argtypes = [gchar_p, gssize]

# gchar* g_utf8_strup(const gchar* str, gssize len);
g_utf8_strup = libglib.g_utf8_strup
g_utf8_strup.restype = gchar_p
g_utf8_strup.argtypes = [gchar_p, gssize]

# gchar* g_utf8_strdown(const gchar* str, gssize len);
g_utf8_strdown = libglib.g_utf8_strdown
g_utf8_strdown.restype = gchar_p
g_utf8_strdown.argtypes = [gchar_p, gssize]

# gchar* g_utf8_casefold(const gchar* str, gssize len);
g_utf8_casefold = libglib.g_utf8_casefold
g_utf8_casefold.restype = gchar_p
g_utf8_casefold.argtypes = [gchar_p, gssize]

# gchar* g_utf8_normalize(const gchar* str, gssize len, GNormalizeMode mode);
g_utf8_normalize = libglib.g_utf8_normalize
g_utf8_normalize.restype = gchar_p
g_utf8_normalize.argtypes = [gchar_p, gssize, GNormalizeMode]

# gint g_utf8_collate(const gchar* str1, const gchar* str2);
g_utf8_collate = libglib.g_utf8_collate
g_utf8_collate.restype = gint
g_utf8_collate.argtypes = [gchar_p, gchar_p]

# gchar* g_utf8_collate_key(const gchar* str, gssize len);
g_utf8_collate_key = libglib.g_utf8_collate_key
g_utf8_collate_key.restype = gchar_p
g_utf8_collate_key.argtypes = [gchar_p, gssize]

# gchar* g_utf8_collate_key_for_filename(const gchar* str, gssize len);
g_utf8_collate_key_for_filename = libglib.g_utf8_collate_key_for_filename
g_utf8_collate_key_for_filename.restype = gchar_p
g_utf8_collate_key_for_filename.argtypes = [gchar_p, gssize]

# gunichar2* g_utf8_to_utf16(const gchar* str,
#                            glong len,
#                            glong* items_read,
#                            glong* items_written,
#                            GError** error);
g_utf8_to_utf16 = libglib.g_utf8_to_utf16
g_utf8_to_utf16.restype = gunichar2_p
g_utf8_to_utf16.argtypes = [gchar_p,
                                 glong,
                                 POINTER(glong),
                                 POINTER(glong),
                                 POINTER(POINTER(GError))]

# gunichar* g_utf8_to_ucs4(const gchar* str,
#                          glong len,
#                          glong* items_read,
#                          glong* items_written,
#                          GError** error);
g_utf8_to_ucs4 = libglib.g_utf8_to_ucs4
g_utf8_to_ucs4.restype = gunichar_p
g_utf8_to_ucs4.argtypes = [gchar_p,
                                glong,
                                POINTER(glong),
                                POINTER(glong),
                                POINTER(POINTER(GError))]

# gunichar* g_utf8_to_ucs4_fast(const gchar* str,
#                               glong len,
#                               glong* items_written);
g_utf8_to_ucs4_fast = libglib.g_utf8_to_ucs4_fast
g_utf8_to_ucs4_fast.restype = gunichar_p
g_utf8_to_ucs4_fast.argtypes = [gchar_p, glong, POINTER(glong)]

# gunichar* g_utf16_to_ucs4(const gunichar2* str,
#                           glong len,
#                           glong* items_read,
#                           glong* items_written,
#                           GError** error);
g_utf16_to_ucs4 = libglib.g_utf16_to_ucs4
g_utf16_to_ucs4.restype = gunichar_p
g_utf16_to_ucs4.argtypes = [gunichar2_p,
                                 glong,
                                 POINTER(glong),
                                 POINTER(glong),
                                 POINTER(POINTER(GError))]

# gchar* g_utf16_to_utf8(const gunichar2* str,
#                        glong len,
#                        glong* items_read,
#                        glong* items_written,
#                        GError** error);
g_utf16_to_utf8 = libglib.g_utf16_to_utf8
g_utf16_to_utf8.restype = gchar_p
g_utf16_to_utf8.argtypes = [gunichar2_p,
                                 glong,
                                 POINTER(glong),
                                 POINTER(glong),
                                 POINTER(POINTER(GError))]

# gunichar2* g_ucs4_to_utf16(const gunichar* str,
#                            glong len,
#                            glong* items_read,
#                            glong* items_written,
#                            GError** error);
g_ucs4_to_utf16 = libglib.g_ucs4_to_utf16
g_ucs4_to_utf16.restype = gunichar2_p
g_ucs4_to_utf16.argtypes = [gunichar_p,
                                 glong,
                                 POINTER(glong),
                                 POINTER(glong),
                                 POINTER(POINTER(GError))]

# gchar* g_ucs4_to_utf8(const gunichar* str,
#                       glong len,
#                       glong* items_read,
#                       glong* items_written,
#                       GError** error);
g_ucs4_to_utf8 = libglib.g_ucs4_to_utf8
g_ucs4_to_utf8.restype = gchar_p
g_ucs4_to_utf8.argtypes = [gunichar_p,
                                glong,
                                POINTER(glong),
                                POINTER(glong),
                                POINTER(POINTER(GError))]

# gint g_unichar_to_utf8(gunichar c, gchar* outbuf);
g_unichar_to_utf8 = libglib.g_unichar_to_utf8
g_unichar_to_utf8.restype = gint
g_unichar_to_utf8.argtypes = [gunichar, gchar_p]
