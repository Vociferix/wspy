from ctypes import *

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
gdouble = c_double

gpointer = c_void_p
gconstpointer = c_void_p

GQuark = guint32
GPid = c_int

# struct GString {
#     gchar* str;
#     gsize len;
#     gsize allocated_len;
# };


class GString(Structure):
    _fields_ = [('str', gchar),
                ('len', gsize),
                ('allocated_len', gsize)]


# typedef struct _GHashTable GHashTable
GHashTable_p = c_void_p

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
    _fields_ = [('domain', GQuark),
                ('code', gint),
                ('message', gchar_p)]

# struct GPtrArray {
#     gpointer* pdata;
#     guint     len;
# };


class GPtrArray(Structure):
    _fields_ = [('pdata', POINTER(gpointer)), ('len', guint)]
