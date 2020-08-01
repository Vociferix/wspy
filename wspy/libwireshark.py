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

from ctypes.util import find_library
from ctypes import *
from wspy.errors import *
from wspy.libglib2 import *
from wspy.libwsutil import *
import wspy_config as config
import sys

libwireshark = CDLL(config.get_libwireshark())


####################
# wmem/wmem_core.h #
####################

# struct _wmem_allocator_t;
class _wmem_allocator_t(Structure):
    _fields_ = []


# typedef struct _wmem_allocator_t wmem_allocator_t;
wmem_allocator_t = _wmem_allocator_t

# typedef enum _wmem_allocator_type_t {
#     WMEM_ALLOCATOR_SIMPLE,
#     WMEM_ALLOCATOR_BLOCK,
#     WMEM_ALLOCATOR_STRICT,
#     WMEM_ALLOCATOR_BLOCK_FAST
# } wmem_allocator_type_t;
_wmem_allocator_type_t = c_int
wmem_allocator_type_t = _wmem_allocator_type_t
WMEM_ALLOCATOR_SIMPLE = c_int(0)
WMEM_ALLOCATOR_BLOCK = c_int(1)
WMEM_ALLOCATOR_STRICT = c_int(2)
WMEM_ALLOCATOR_BLOCK_FAST = c_int(3)

# void *wmem_alloc(wmem_allocator_t *allocator, const size_t size);
wmem_alloc = libwireshark.wmem_alloc
wmem_alloc.restype = c_void_p
wmem_alloc.argtypes = [POINTER(wmem_allocator_t), c_size_t]


# #define wmem_new(allocator, type) \
#     ((type*)wmem_alloc((allocator), sizeof(type)))
def wmem_new(allocator, type):
    return cast(wmem_alloc(allocator, sizeof(type)), POINTER(type))


# #define wmem_safe_mult(A, B) \
#     ((((A) <= 0) || ((B) <= 0) || ((gsize)(A) > (G_MAXSSIZE / (gsize)(B)))) ? 0 : ((A) * (B)))
def wmem_safe_mult(A, B):
    if A <= 0 or B <= 0 or cast(A, gsize) > ~(gsize(0) / cast(B, gisize)):
        return 0
    else:
        return A * B


# #define wmem_alloc_array(allocator, type, num) \
#     ((type*)wmem_alloc((allocator), wmem_safe_mult(sizeof(type), num)))
def wmem_alloc_array(allocator, type, num):
    return cast(
        wmem_alloc(
            allocator,
            wmem_safe_mult(
                sizeof(type),
                num)),
        POINTER(type))


# void *wmem_alloc0(wmem_allocator_t *allocator, const size_t size);
wmem_alloc0 = libwireshark.wmem_alloc0
wmem_alloc0.restype = c_void_p
wmem_alloc0.argtypes = [POINTER(wmem_allocator_t), c_size_t]


# #define wmem_new0(allocator, type) \
#     ((type*)wmem_alloc0((allocator), sizeof(type)))
def wmem_new0(allocator, type):
    return cast(wmem_alloc0(allocator, sizeof(type)), POINTER(type))


# #define wmem_alloc0_array(allocator, type, num) \
#     ((type*)wmem_alloc0((allocator), wmem_safe_mult(sizeof(type), (num))))
def wmem_alloc0_array(allocator, type, num):
    return cast(
        wmem_alloc0(
            allocator,
            wmem_safe_mult(
                sizeof(type),
                num)),
        POINTER(type))


# void wmem_free(wmem_allocator_t *allocator, void *ptr);
wmem_free = libwireshark.wmem_free
wmem_free.restype = None
wmem_free.argtypes = [POINTER(wmem_allocator_t), c_void_p]

# void *wmem_realloc(wmem_allocator_t *allocator, void *ptr, const size_t
# size);
wmem_realloc = libwireshark.wmem_realloc
wmem_realloc.restype = c_void_p
wmem_realloc.argtypes = [POINTER(wmem_allocator_t), c_void_p, c_size_t]

# void wmem_free_all(wmem_allocator_t *allocator);
wmem_free_all = libwireshark.wmem_free_all
wmem_free_all.restype = None
wmem_free_all.argtypes = [POINTER(wmem_allocator_t)]

# void wmem_gc(wmem_allocator_t *allocator);
wmem_gc = libwireshark.wmem_gc
wmem_gc.restype = None
wmem_gc.argtypes = [POINTER(wmem_allocator_t)]

# void wmem_destroy_allocator(wmem_allocator_t *allocator);
wmem_destroy_allocator = libwireshark.wmem_destroy_allocator
wmem_destroy_allocator.restype = None
wmem_destroy_allocator.argtypes = [POINTER(wmem_allocator_t)]

# wmem_allocator_t *wmem_allocator_new(const wmem_allocator_type_t type);
wmem_allocator_new = libwireshark.wmem_allocator_new
wmem_allocator_new.restype = POINTER(wmem_allocator_t)
wmem_allocator_new.argtypes = [wmem_allocator_type_t]

# void wmem_init(void);
wmem_init = libwireshark.wmem_init
wmem_init.restype = None
wmem_init.argtypes = []

# void wmem_cleanup(void);
wmem_cleanup = libwireshark.wmem_cleanup
wmem_cleanup.restype = None
wmem_cleanup.argtypes = []


#####################
# wmem/wmem_array.h #
#####################

# struct _wmem_array_t;
class _wmem_array_t(Structure):
    _fields_ = []


# typedef struct _wmem_array_t wmem_array_t;
wmem_array_t = _wmem_array_t

# wmem_array_t *
# wmem_array_sized_new(wmem_allocator_t *allocator, gsize elem_size,
#                      guint alloc_count);
wmem_array_sized_new = libwireshark.wmem_array_sized_new
wmem_array_sized_new.restype = POINTER(wmem_array_t)
wmem_array_sized_new.argtypes = [POINTER(wmem_allocator_t),
                                 gsize,
                                 guint]

# wmem_array_t *wmem_array_new(wmem_allocator_t *allocator, const gsize
# elem_size);
wmem_array_new = libwireshark.wmem_array_new
wmem_array_new.restype = POINTER(wmem_array_t)
wmem_array_new.argtypes = [POINTER(wmem_allocator_t), gsize]

# void wmem_array_set_null_terminator(wmem_array_t *array);
wmem_array_set_null_terminator = libwireshark.wmem_array_set_null_terminator
wmem_array_set_null_terminator.restype = None
wmem_array_set_null_terminator.argtypes = [POINTER(wmem_array_t)]

# void wmem_array_bzero(wmem_array_t *array);
wmem_array_bzero = libwireshark.wmem_array_bzero
wmem_array_bzero.restype = None
wmem_array_bzero.argtypes = [POINTER(wmem_array_t)]

# void wmem_array_append(wmem_array_t *array, const void *in, guint count);
wmem_array_append = libwireshark.wmem_array_append
wmem_array_append.restype = None
wmem_array_append.argtypes = [POINTER(wmem_array_t), c_void_p, guint]


# #define wmem_array_append_one(ARRAY, VAL) \
#     wmem_array_append((ARRAY), &(VAL), 1)
def wmem_array_append_one(ARRAY, VAL):
    wmem_array_append(array, byref(VAL), 1)


# void *wmem_array_index(wmem_array_t *array, guint array_index);
wmem_array_index = libwireshark.wmem_array_index
wmem_array_index.restype = c_void_p
wmem_array_index.argtypes = [POINTER(wmem_array_t), guint]

# int wmem_array_try_index(wmem_array_t *array, guint array_index, void *val);
wmem_array_try_index = libwireshark.wmem_array_try_index
wmem_array_try_index.restype = c_int
wmem_array_try_index.argtypes = [POINTER(wmem_array_t), guint, c_void_p]

# void wmem_array_sort(wmem_array_t *array, int (*compar)(const
# void*,const void*));
wmem_array_sort = libwireshark.wmem_array_sort
wmem_array_sort.restype = None
wmem_array_sort.argtypes = [POINTER(wmem_array_t),
                            CFUNCTYPE(c_int, c_void_p, c_void_p)]

# void *wmem_array_get_raw(wmem_array_t *array);
wmem_array_get_raw = libwireshark.wmem_array_get_raw
wmem_array_get_raw.restype = c_void_p
wmem_array_get_raw.argtypes = [POINTER(wmem_array_t)]

# guint wmem_array_get_count(wmem_array_t *array);
wmem_array_get_count = libwireshark.wmem_array_get_count
wmem_array_get_count.restype = guint
wmem_array_get_count.argtypes = [POINTER(wmem_array_t)]

# void wmem_destroy_array(wmem_array_t *array);
#wmem_destroy_array = libwireshark.wmem_destroy_array
#wmem_destroy_array.restype = None
#wmem_destroy_array.argtypes = [POINTER(wmem_array_t)]


####################
# wmem/wmem_list.h #
####################

# struct _wmem_list_t;
class _wmem_list_t(Structure):
    _fields_ = []


# struct _wmem_list_frame_t;
class _wmem_list_frame_t(Structure):
    _fields_ = []


# typedef struct _wmem_list_t       wmem_list_t;
wmem_list_t = _wmem_list_t

# typedef struct _wmem_list_frame_t wmem_list_frame_t;
wmem_list_frame_t = _wmem_list_frame_t

# guint wmem_list_count(const wmem_list_t *list);
wmem_list_count = libwireshark.wmem_list_count
wmem_list_count.restype = guint
wmem_list_count.argtypes = [POINTER(wmem_list_t)]

# wmem_list_frame_t *wmem_list_head(const wmem_list_t *list);
wmem_list_head = libwireshark.wmem_list_head
wmem_list_head.restype = POINTER(wmem_list_frame_t)
wmem_list_head.argtypes = [POINTER(wmem_list_t)]

# wmem_list_frame_t *wmem_list_tail(const wmem_list_t *list);
wmem_list_tail = libwireshark.wmem_list_tail
wmem_list_tail.restype = POINTER(wmem_list_frame_t)
wmem_list_tail.argtypes = [POINTER(wmem_list_t)]

# wmem_list_frame_t *wmem_list_frame_next(const wmem_list_frame_t *frame);
wmem_list_frame_next = libwireshark.wmem_list_frame_next
wmem_list_frame_next.restype = POINTER(wmem_list_frame_t)
wmem_list_frame_next.argtypes = [POINTER(wmem_list_frame_t)]

# wmem_list_frame_t *wmem_list_frame_prev(const wmem_list_frame_t *frame);
wmem_list_frame_prev = libwireshark.wmem_list_frame_prev
wmem_list_frame_prev.restype = POINTER(wmem_list_frame_t)
wmem_list_frame_prev.argtypes = [POINTER(wmem_list_frame_t)]

# void *wmem_list_frame_data(const wmem_list_frame_t *frame);
wmem_list_frame_data = libwireshark.wmem_list_frame_data
wmem_list_frame_data.restype = c_void_p
wmem_list_frame_data.argtypes = [POINTER(wmem_list_frame_t)]

# void wmem_list_remove(wmem_list_t *list, void *data);
wmem_list_remove = libwireshark.wmem_list_remove
wmem_list_remove.restype = None
wmem_list_remove.argtypes = [POINTER(wmem_list_t), c_void_p]

# void wmem_list_remove_frame(wmem_list_t *list, wmem_list_frame_t *frame);
wmem_list_remove_frame = libwireshark.wmem_list_remove_frame
wmem_list_remove_frame.restype = None
wmem_list_remove_frame.argtypes = [
    POINTER(wmem_list_t),
    POINTER(wmem_list_frame_t)]

# wmem_list_frame_t *wmem_list_find(wmem_list_t *list, const void *data);
wmem_list_find = libwireshark.wmem_list_find
wmem_list_find.restype = POINTER(wmem_list_frame_t)
wmem_list_find.argtypes = [POINTER(wmem_list_t), c_void_p]

# wmem_list_frame_t *wmem_list_find_custom(wmem_list_t *list, const void
# *data, GCompareFunc func);
wmem_list_find_custom = libwireshark.wmem_list_find_custom
wmem_list_find_custom.restype = POINTER(wmem_list_frame_t)
wmem_list_find_custom.argtypes = [POINTER(wmem_list_t), c_void_p, GCompareFunc]

# void wmem_list_prepend(wmem_list_t *list, void *data);
wmem_list_prepend = libwireshark.wmem_list_prepend
wmem_list_prepend.restype = None
wmem_list_prepend.argtypes = [POINTER(wmem_list_t), c_void_p]

# void wmem_list_append(wmem_list_t *list, void *data);
wmem_list_append = libwireshark.wmem_list_append
wmem_list_append.restype = None
wmem_list_append.argtypes = [POINTER(wmem_list_t), c_void_p]

# void wmem_list_insert_sorted(wmem_list_t *list, void* data, GCompareFunc
# func);
wmem_list_insert_sorted = libwireshark.wmem_list_insert_sorted
wmem_list_insert_sorted.restype = None
wmem_list_insert_sorted.argtypes = [
    POINTER(wmem_list_t), c_void_p, GCompareFunc]

# wmem_list_t *wmem_list_new(wmem_allocator_t *allocator);
wmem_list_new = libwireshark.wmem_list_new
wmem_list_new.restype = POINTER(wmem_list_t)
wmem_list_new.argtypes = [POINTER(wmem_allocator_t)]

# void wmem_list_foreach(wmem_list_t *list, GFunc foreach_func, gpointer
# user_data);
wmem_list_foreach = libwireshark.wmem_list_foreach
wmem_list_foreach.restype = None
wmem_list_foreach.argtypes = [POINTER(wmem_list_t), GFunc, gpointer]

# void wmem_destroy_list(wmem_list_t *list);
wmem_destroy_list = libwireshark.wmem_destroy_list
wmem_destroy_list.restype = None
wmem_destroy_list.argtypes = [POINTER(wmem_list_t)]


###################
# wmem/wmem_map.h #
###################

# struct _wmem_map_t;
class _wmem_map_t(Structure):
    _fields_ = []


# typedef struct _wmem_map_t wmem_map_t;
wmem_map_t = _wmem_map_t

# wmem_map_t *wmem_map_new(wmem_allocator_t *allocator,
#         GHashFunc hash_func, GEqualFunc eql_func);
wmem_map_new = libwireshark.wmem_map_new
wmem_map_new.restype = POINTER(wmem_map_t)
wmem_map_new.argtypes = [POINTER(wmem_allocator_t),
                         GHashFunc,
                         GEqualFunc]

# wmem_map_t *wmem_map_new_autoreset(wmem_allocator_t *master, wmem_allocator_t *slave,
#         GHashFunc hash_func, GEqualFunc eql_func);
wmem_map_new_autoreset = libwireshark.wmem_map_new_autoreset
wmem_map_new_autoreset.restype = POINTER(wmem_map_t)
wmem_map_new_autoreset.argtypes = [POINTER(wmem_allocator_t),
                                   POINTER(wmem_allocator_t),
                                   GHashFunc,
                                   GEqualFunc]

# void *wmem_map_insert(wmem_map_t *map, const void *key, void *value);
wmem_map_insert = libwireshark.wmem_map_insert
wmem_map_insert.restype = c_void_p
wmem_map_insert.argtypes = [POINTER(wmem_map_t), c_void_p, c_void_p]

# gboolean wmem_map_contains(wmem_map_t *map, const void *key);
wmem_map_contains = libwireshark.wmem_map_contains
wmem_map_contains.restype = gboolean
wmem_map_contains.argtypes = [POINTER(wmem_map_t), c_void_p]

# void *wmem_map_lookup(wmem_map_t *map, const void *key);
wmem_map_lookup = libwireshark.wmem_map_lookup
wmem_map_lookup.restype = c_void_p
wmem_map_lookup.argtypes = [POINTER(wmem_map_t), c_void_p]

# gboolean wmem_map_lookup_extended(wmem_map_t *map, const void *key,
# const void **orig_key, void **value);
wmem_map_lookup_extended = libwireshark.wmem_map_lookup_extended
wmem_map_lookup_extended.restype = gboolean
wmem_map_lookup_extended.argtypes = [POINTER(wmem_map_t),
                                     c_void_p,
                                     POINTER(c_void_p),
                                     POINTER(c_void_p)]

# void *wmem_map_remove(wmem_map_t *map, const void *key);
wmem_map_remove = libwireshark.wmem_map_remove
wmem_map_remove.restype = c_void_p
wmem_map_remove.argtypes = [POINTER(wmem_map_t), c_void_p]

# gboolean wmem_map_steal(wmem_map_t *map, const void *key);
wmem_map_steal = libwireshark.wmem_map_steal
wmem_map_steal.restype = gboolean
wmem_map_steal.argtypes = [POINTER(wmem_map_t), c_void_p]

# wmem_list_t* wmem_map_get_keys(wmem_allocator_t *list_allocator, wmem_map_t *map);
wmem_map_get_keys = libwireshark.wmem_map_get_keys
wmem_map_get_keys.restype = POINTER(wmem_list_t)
wmem_map_get_keys.argtypes = [POINTER(wmem_allocator_t), POINTER(wmem_map_t)]

# void wmem_map_foreach(wmem_map_t *map, GHFunc foreach_func, gpointer
# user_data);
wmem_map_foreach = libwireshark.wmem_map_foreach
wmem_map_foreach.restype = None
wmem_map_foreach.argtypes = [POINTER(wmem_map_t), GHFunc, gpointer]

# guint wmem_map_size(wmem_map_t *map);
wmem_map_size = libwireshark.wmem_map_size
wmem_map_size.restype = guint
wmem_map_size.argtypes = [POINTER(wmem_map_t)]

# guint32 wmem_strong_hash(const guint8 *buf, const size_t len);
wmem_strong_hash = libwireshark.wmem_strong_hash
wmem_strong_hash.restype = guint32
wmem_strong_hash.argtypes = [POINTER(guint8), c_size_t]

# guint wmem_str_hash(gconstpointer key);
wmem_str_hash = libwireshark.wmem_str_hash
wmem_str_hash.restype = guint
wmem_str_hash.argtypes = [gconstpointer]

# guint wmem_int64_hash(gconstpointer key);
wmem_int64_hash = libwireshark.wmem_int64_hash
wmem_int64_hash.restype = guint
wmem_int64_hash.argtypes = [gconstpointer]

# guint wmem_double_hash(gconstpointer key);
wmem_double_hash = libwireshark.wmem_double_hash
wmem_double_hash.restype = guint
wmem_double_hash.argtypes = [gconstpointer]


#######################
# wmem/wmem_miscutl.h #
#######################

# void *wmem_memdup(wmem_allocator_t *allocator, const void *source, const
# size_t size);
wmem_memdup = libwireshark.wmem_memdup
wmem_memdup.restype = c_void_p
wmem_memdup.argtypes = [POINTER(wmem_allocator_t), c_void_p, c_size_t]


#####################
# wmem/wmem_stack.h #
#####################

# typedef wmem_list_t wmem_stack_t;
wmem_stack_t = wmem_list_t


# #define wmem_stack_count(X) wmem_list_count(X)
def wmem_stack_count(X):
    wmem_list_count(X)


# void *wmem_stack_peek(const wmem_stack_t *stack);
wmem_stack_peek = libwireshark.wmem_stack_peek
wmem_stack_peek.restype = c_void_p
wmem_stack_peek.argtypes = [POINTER(wmem_stack_t)]

# void *wmem_stack_pop(wmem_stack_t *stack);
wmem_stack_pop = libwireshark.wmem_stack_pop
wmem_stack_pop.restype = c_void_p
wmem_stack_pop.argtypes = [POINTER(wmem_stack_t)]


# #define wmem_stack_push(STACK, DATA) wmem_list_prepend((STACK), (DATA))
def wmem_stack_push(STACK, DATA):
    wmem_list_prepend(STACK, DATA)


# #define wmem_stack_new(ALLOCATOR) wmem_list_new(ALLOCATOR)
def wmem_stack_new(ALLOCATOR):
    return wmem_list_new(ALLOCATOR)


# #define wmem_destroy_stack(STACK) wmem_destroy_list(STACK)
def wmem_destroy_stack(STACK):
    wmem_destroy_list(STACK)


#####################
# wmem/wmem_queue.h #
#####################

# typedef wmem_list_t wmem_queue_t;
wmem_queue_t = wmem_list_t


# #define wmem_queue_count(X) wmem_list_count(X)
def wmem_queue_count(X):
    return wmem_list_count(X)


# #define wmem_queue_peek(QUEUE) wmem_stack_peek(QUEUE)
def wmem_queue_peek(QUEUE):
    return wmem_stack_peek(QUEUE)


# #define wmem_queue_pop(QUEUE) wmem_stack_pop(QUEUE)
def wmem_queue_pop(QUEUE):
    return wmem_stack_pop(QUEUE)


# #define wmem_queue_push(QUEUE, DATA) wmem_list_append((QUEUE), (DATA))
def wmem_queue_push(QUEUE, DATA):
    return wmem_list_append(QUEUE, DATA)


# #define wmem_queue_new(ALLOCATOR) wmem_list_new(ALLOCATOR)
def wmem_queue_new(ALLOCATOR):
    return wmem_list_new(ALLOCATOR)


# #define wmem_destroy_queue(QUEUE) wmem_destroy_list(QUEUE)
def wmem_destroy_queue(QUEUE):
    wmem_destroy_list(QUEUE)


######################
# wmem/wmem_scopes.h #
######################

# wmem_allocator_t *wmem_epan_scope(void);
wmem_epan_scope = libwireshark.wmem_epan_scope
wmem_epan_scope.restype = POINTER(wmem_allocator_t)
wmem_epan_scope.argtypes = []

# wmem_allocator_t *wmem_packet_scope(void);
wmem_packet_scope = libwireshark.wmem_packet_scope
wmem_packet_scope.restype = POINTER(wmem_allocator_t)
wmem_packet_scope.argtypes = []

# wmem_allocator_t *wmem_file_scope(void);
wmem_file_scope = libwireshark.wmem_file_scope
wmem_file_scope.restype = POINTER(wmem_allocator_t)
wmem_file_scope.argtypes = []


######################
# wmem/wmem_strbuf.h #
######################

# struct _wmem_strbuf_t;
class _wmem_strbuf_t(Structure):
    _fields_ = []


# typedef struct _wmem_strbuf_t wmem_strbuf_t;
wmem_strbuf_t = _wmem_strbuf_t


# wmem_strbuf_t *wmem_strbuf_sized_new(wmem_allocator_t *allocator,
#                                      gsize alloc_len, gsize max_len);
wmem_strbuf_sized_new = libwireshark.wmem_strbuf_sized_new
wmem_strbuf_sized_new.restype = POINTER(wmem_strbuf_t)
wmem_strbuf_sized_new.argtypes = [POINTER(wmem_allocator_t), gsize, gsize]


# #define wmem_strbuf_new_label(ALLOCATOR) \
#     wmem_strbuf_sized_new((ALLOCATOR), 0, ITEM_LABEL_LENGTH)
def wmem_strbuf_new_label(ALLOCATOR):
    return wmem_strbuf_sized_new(ALLOCATOR, gsize(0), gsize(ITEM_LABEL_LENGTH))


# wmem_strbuf_t *wmem_strbuf_new(wmem_allocator_t *allocator, const gchar
# *str);
wmem_strbuf_new = libwireshark.wmem_strbuf_new
wmem_strbuf_new.restype = POINTER(wmem_strbuf_t)
wmem_strbuf_new.argtypes = [POINTER(wmem_allocator_t), gchar_p]

# void wmem_strbuf_append(wmem_strbuf_t *strbuf, const gchar *str);
wmem_strbuf_append = libwireshark.wmem_strbuf_append
wmem_strbuf_append.restype = None
wmem_strbuf_append.argtypes = [POINTER(wmem_strbuf_t), gchar_p]


# void wmem_strbuf_append_printf(wmem_strbuf_t *strbuf, const gchar
# *format, ...);
def wmem_strbuf_append_printf(strbuf, format, *argv):
    args, types = c_va_list(*argv)
    _wmem_strbuf_append_printf = libwireshark.wmem_strbuf_append_printf
    _wmem_strbuf_append_printf.restype = None
    _wmem_strbuf_append_printf.argtypes = [
        POINTER(wmem_strbuf_t), gchar_p] + types
    _wmem_strbuf_append_printf(strbuf, format, *args)


# void wmem_strbuf_append_c(wmem_strbuf_t *strbuf, const gchar c);
wmem_strbuf_append_c = libwireshark.wmem_strbuf_append_c
wmem_strbuf_append_c.restype = None
wmem_strbuf_append_c.argtypes = [POINTER(wmem_strbuf_t), gchar]

# void wmem_strbuf_append_unichar(wmem_strbuf_t *strbuf, const gunichar c);
wmem_strbuf_append_unichar = libwireshark.wmem_strbuf_append_unichar
wmem_strbuf_append_unichar.restype = None
wmem_strbuf_append_unichar.argtypes = [POINTER(wmem_strbuf_t), gunichar]

# void wmem_strbuf_truncate(wmem_strbuf_t *strbuf, const gsize len);
wmem_strbuf_truncate = libwireshark.wmem_strbuf_truncate
wmem_strbuf_truncate.restype = None
wmem_strbuf_truncate.argtypes = [POINTER(wmem_strbuf_t), gsize]

# const gchar *wmem_strbuf_get_str(wmem_strbuf_t *strbuf);
wmem_strbuf_get_str = libwireshark.wmem_strbuf_get_str
wmem_strbuf_get_str.restype = gchar_p
wmem_strbuf_get_str.argtypes = [POINTER(wmem_strbuf_t)]

# gsize wmem_strbuf_get_len(wmem_strbuf_t *strbuf);
wmem_strbuf_get_len = libwireshark.wmem_strbuf_get_len
wmem_strbuf_get_len.restype = gsize
wmem_strbuf_get_len.argtypes = [POINTER(wmem_strbuf_t)]

# char *wmem_strbuf_finalize(wmem_strbuf_t *strbuf);
wmem_strbuf_finalize = libwireshark.wmem_strbuf_finalize
wmem_strbuf_finalize.restype = c_char_p
wmem_strbuf_finalize.argtypes = [POINTER(wmem_strbuf_t)]


####################
# wmem/wmem_tree.h #
####################

# struct _wmem_tree_t;
class _wmem_tree_t(Structure):
    _fields_ = []


# typedef struct _wmem_tree_t wmem_tree_t;
wmem_tree_t = _wmem_tree_t

# wmem_tree_t *wmem_tree_new(wmem_allocator_t *allocator);
wmem_tree_new = libwireshark.wmem_tree_new
wmem_tree_new.restype = POINTER(wmem_tree_t)
wmem_tree_new.argtypes = [POINTER(wmem_allocator_t)]

# wmem_tree_t *wmem_tree_new_autoreset(wmem_allocator_t *master, wmem_allocator_t *slave);
wmem_tree_new_autoreset = libwireshark.wmem_tree_new_autoreset
wmem_tree_new_autoreset.restype = POINTER(wmem_tree_t)
wmem_tree_new_autoreset.argtypes = [
    POINTER(wmem_allocator_t),
    POINTER(wmem_allocator_t)]

# void wmem_tree_destroy(wmem_tree_t *tree, gboolean free_keys, gboolean
# free_values);
wmem_tree_destroy = libwireshark.wmem_tree_destroy
wmem_tree_destroy.restype = None
wmem_tree_destroy.argtypes = [POINTER(wmem_tree_t), gboolean, gboolean]

# gboolean wmem_tree_is_empty(wmem_tree_t *tree);
wmem_tree_is_empty = libwireshark.wmem_tree_is_empty
wmem_tree_is_empty.restype = gboolean
wmem_tree_is_empty.argtypes = [POINTER(wmem_tree_t)]

# guint wmem_tree_count(wmem_tree_t* tree);
wmem_tree_count = libwireshark.wmem_tree_count
wmem_tree_count.restype = guint
wmem_tree_count.argtypes = [POINTER(wmem_tree_t)]

# void wmem_tree_insert32(wmem_tree_t *tree, guint32 key, void *data);
wmem_tree_insert32 = libwireshark.wmem_tree_insert32
wmem_tree_insert32.restype = None
wmem_tree_insert32.argtypes = [POINTER(wmem_tree_t), guint32, c_void_p]

# void *wmem_tree_lookup32(wmem_tree_t *tree, guint32 key);
wmem_tree_lookup32 = libwireshark.wmem_tree_lookup32
wmem_tree_lookup32.restype = c_void_p
wmem_tree_lookup32.argtypes = [POINTER(wmem_tree_t), guint32]

# void *wmem_tree_lookup32_le(wmem_tree_t *tree, guint32 key);
wmem_tree_lookup32_le = libwireshark.wmem_tree_lookup32_le
wmem_tree_lookup32_le.restype = c_void_p
wmem_tree_lookup32_le.argtypes = [POINTER(wmem_tree_t), guint32]

# void *wmem_tree_remove32(wmem_tree_t *tree, guint32 key);
wmem_tree_remove32 = libwireshark.wmem_tree_remove32
wmem_tree_remove32.restype = c_void_p
wmem_tree_remove32.argtypes = [POINTER(wmem_tree_t), guint32]

# #define WMEM_TREE_STRING_NOCASE                 0x00000001
WMEM_TREE_STRING_NOCASE = 0x00000001

# void wmem_tree_insert_string(wmem_tree_t *tree, const gchar* key,
#                              void *data, guint32 flags);
wmem_tree_insert_string = libwireshark.wmem_tree_insert_string
wmem_tree_insert_string.restype = None
wmem_tree_insert_string.argtypes = [POINTER(wmem_tree_t),
                                    gchar_p,
                                    c_void_p,
                                    guint32]

# void *wmem_tree_lookup_string(wmem_tree_t* tree, const gchar* key,
# guint32 flags);
wmem_tree_lookup_string = libwireshark.wmem_tree_lookup_string
wmem_tree_lookup_string.restype = c_void_p
wmem_tree_lookup_string.argtypes = [POINTER(wmem_tree_t), gchar_p, guint32]

# void *wmem_tree_remove_string(wmem_tree_t* tree, const gchar* key,
# guint32 flags);
wmem_tree_remove_string = libwireshark.wmem_tree_remove_string
wmem_tree_remove_string.restype = c_void_p
wmem_tree_remove_string.argtypes = [POINTER(wmem_tree_t), gchar_p, guint32]


# typedef struct _wmem_tree_key_t {
#     guint32 length;
#     guint32 *key;
# } wmem_tree_key_t;
class _wmem_tree_key_t(Structure):
    _fields_ = [('length', guint32),
                ('key', POINTER(guint32))]


wmem_tree_key_t = _wmem_tree_key_t


# void wmem_tree_insert32_array(wmem_tree_t *tree, wmem_tree_key_t *key,
# void *data);
wmem_tree_insert32_array = libwireshark.wmem_tree_insert32_array
wmem_tree_insert32_array.restype = None
wmem_tree_insert32_array.argtypes = [POINTER(wmem_tree_t),
                                     POINTER(wmem_tree_key_t),
                                     c_void_p]

# void *wmem_tree_lookup32_array(wmem_tree_t *tree, wmem_tree_key_t *key);
wmem_tree_lookup32_array = libwireshark.wmem_tree_insert32_array
wmem_tree_lookup32_array.restype = c_void_p
wmem_tree_lookup32_array.argtypes = [
    POINTER(wmem_tree_t),
    POINTER(wmem_tree_key_t)]

# void *wmem_tree_lookup32_array_le(wmem_tree_t *tree, wmem_tree_key_t *key);
wmem_tree_lookup32_array_le = libwireshark.wmem_tree_lookup32_array_le
wmem_tree_lookup32_array_le.restype = c_void_p
wmem_tree_lookup32_array_le.argtypes = [
    POINTER(wmem_tree_t), POINTER(wmem_tree_key_t)]

# typedef gboolean (*wmem_foreach_func)(const void *key, void *value, void
# *userdata);
wmem_foreach_func = CFUNCTYPE(gboolean, c_void_p, c_void_p, c_void_p)

# typedef void (*wmem_printer_func)(const void *data);
wmem_printer_func = CFUNCTYPE(None, c_void_p)

# gboolean wmem_tree_foreach(wmem_tree_t* tree, wmem_foreach_func callback,
#                            void *user_data);
wmem_tree_foreach = libwireshark.wmem_tree_foreach
wmem_tree_foreach.restype = gboolean
wmem_tree_foreach.argtypes = [
    POINTER(wmem_tree_t),
    wmem_foreach_func,
    c_void_p]


#############################
# wmem/wmem_interval_tree.h #
#############################

# typedef struct _wmem_tree_t wmem_itree_t;
wmem_itree_t = _wmem_tree_t


# struct _wmem_range_t {
#     guint64 low;
#     guint64 high;
#     guint64 max_edge;
# };
class _wmem_range_t(Structure):
    _fields_ = [('low', guint64),
                ('high', guint64),
                ('max_edge', guint64)]


# wmem_itree_t *wmem_itree_new(wmem_allocator_t *allocator);
wmem_itree_new = libwireshark.wmem_itree_new
wmem_itree_new.restype = POINTER(wmem_itree_t)
wmem_itree_new.argtypes = [POINTER(wmem_allocator_t)]

# gboolean wmem_itree_is_empty(wmem_itree_t *tree);
wmem_itree_is_empty = libwireshark.wmem_itree_is_empty
wmem_itree_is_empty.restype = gboolean
wmem_itree_is_empty.argtypes = [POINTER(wmem_itree_t)]

# void wmem_itree_insert(wmem_itree_t *tree, const guint64 low,
#                        const guint64 high, void *data);
wmem_itree_insert = libwireshark.wmem_itree_insert
wmem_itree_insert.restype = None
wmem_itree_insert.argtypes = [POINTER(wmem_itree_t),
                              guint64,
                              guint64,
                              c_void_p]

# wmem_list_t *wmem_itree_find_intervals(wmem_itree_t *tree, wmem_allocator_t *allocator,
#                                        guint64 low, guint64 high);
wmem_itree_find_intervals = libwireshark.wmem_itree_find_intervals
wmem_itree_find_intervals.restype = POINTER(wmem_list_t)
wmem_itree_find_intervals.argtypes = [POINTER(wmem_itree_t),
                                      POINTER(wmem_allocator_t),
                                      guint64,
                                      guint64]


#######################
# wmem/wmem_user_cb.h #
#######################

# typedef enum _wmem_cb_event_t {
#     WMEM_CB_FREE_EVENT,
#     WMEM_CB_DESTROY_EVENT
# } wmem_cb_event_t;
_wmem_cb_event_t = c_int
wmem_cb_event_t = c_int
WMEM_CB_FREE_EVENT = c_int(0)
WMEM_CB_DESTROY_EVENT = c_int(1)

# typedef gboolean (*wmem_user_cb_t) (wmem_allocator_t*, wmem_cb_event_t,
# void*);
wmem_user_cb_t = CFUNCTYPE(gboolean,
                           POINTER(wmem_allocator_t),
                           wmem_cb_event_t,
                           c_void_p)

# guint wmem_register_callback(wmem_allocator_t *allocator, wmem_user_cb_t callback,
#                              void *user_data);
wmem_register_callback = libwireshark.wmem_register_callback
wmem_register_callback.restype = guint
wmem_register_callback.argtypes = [POINTER(wmem_allocator_t),
                                   wmem_user_cb_t,
                                   c_void_p]

# void wmem_unregister_callback(wmem_allocator_t *allocator, guint id);
wmem_unregister_callback = libwireshark.wmem_unregister_callback
wmem_unregister_callback.restype = None
wmem_unregister_callback.argtypes = [POINTER(wmem_allocator_t), guint]


################
# guid-utils.h #
################

# #define GUID_LEN	16
GUID_LEN = 16


# typedef struct _e_guid_t {
#     guint32 data1;
#     guint16 data2;
#     guint16 data3;
#     guint8  data4[8];
# } e_guid_t;
class _e_guid_t(Structure):
    _fields_ = [('data1', guint32),
                ('data2', guint16),
                ('data3', guint16),
                ('data4', guint8 * 4)]


e_guid_t = _e_guid_t

# void guids_init(void);
guids_init = libwireshark.guids_init
guids_init.restype = None
guids_init.argtypes = []

# void guids_add_guid(const e_guid_t *guid, const gchar *name);
guids_add_guid = libwireshark.guids_add_guid
guids_add_guid.restype = None
guids_add_guid.argtypes = [POINTER(e_guid_t), gchar_p]

# const gchar *guids_get_guid_name(const e_guid_t *guid);
guids_get_guid_name = libwireshark.guids_get_guid_name
guids_get_guid_name.restype = gchar_p
guids_get_guid_name.argtypes = [POINTER(e_guid_t)]

# const gchar* guids_resolve_guid_to_str(const e_guid_t *guid);
guids_resolve_guid_to_str = libwireshark.guids_resolve_guid_to_str
guids_resolve_guid_to_str.restype = gchar_p
guids_resolve_guid_to_str.argtypes = [POINTER(e_guid_t)]


# #define guids_add_uuid(uuid, name) guids_add_guid((const e_guid_t *) (uuid), (name))
def guids_add_uuid(uuid, name):
    guids_add_guid(cast(uuid, POINTER(e_guid_t)), name)


# #define guids_get_uuid_name(uuid) guids_get_guid_name((e_guid_t *) (uuid))
def guids_get_uuid_name(uuid):
    guids_get_guid_name(cast(uuid, POINTER(e_guid_t)))


# #define guids_resolve_uuid_to_str(uuid) guids_resolve_guid_to_str((e_guid_t *) (uuid))
def guids_reolve_uuid_to_str(uuid):
    guids_resolve_guid_to_str(cast(uuid, POINTER(e_guid_t)))


# int guid_cmp(const e_guid_t *g1, const e_guid_t *g2);
guid_cmp = libwireshark.guid_cmp
guid_cmp.restype = c_int
guid_cmp.argtypes = [POINTER(e_guid_t), POINTER(e_guid_t)]


##########
# ipv6.h #
##########

# typedef struct {
# 	ws_in6_addr addr;
# 	guint32 prefix;
# } ipv6_addr_and_prefix;
class ipv6_addr_and_prefix(Structure):
    _fields_ = [('addr', ws_in6_addr),
                ('prefix', guint32)]


############
# tvbuff.h #
############

# struct tvbuff;
class tvbuff(Structure):
    _fields_ = []


# typedef struct tvbuff tvbuff_t;
tvbuff_t = tvbuff

# typedef void (*tvbuff_free_cb_t)(void*);
tvbuff_free_cb_t = CFUNCTYPE(None, c_void_p)

# tvbuff_t *tvb_new_octet_aligned(tvbuff_t *tvb,
#     guint32 bit_offset, gint32 no_of_bits);
tvb_new_octet_aligned = libwireshark.tvb_new_octet_aligned
tvb_new_octet_aligned.restype = POINTER(tvbuff_t)
tvb_new_octet_aligned.argtypes = [POINTER(tvbuff_t), guint32, guint32]

# tvbuff_t *tvb_new_chain(tvbuff_t *parent, tvbuff_t *backing);
tvb_new_chain = libwireshark.tvb_new_chain
tvb_new_chain.restype = POINTER(tvbuff_t)
tvb_new_chain.argtypes = [POINTER(tvbuff_t), POINTER(tvbuff_t)]

# tvbuff_t *tvb_clone(tvbuff_t *tvb);
tvb_clone = libwireshark.tvb_clone
tvb_clone.restype = POINTER(tvbuff_t)
tvb_clone.argtypes = [POINTER(tvbuff_t)]

# tvbuff_t *tvb_clone_offset_len(tvbuff_t *tvb, guint offset,
#     guint len);
tvb_clone_offset_len = libwireshark.tvb_clone_offset_len
tvb_clone_offset_len.restype = POINTER(tvbuff_t)
tvb_clone_offset_len.argtypes = [POINTER(tvbuff_t), guint, guint]

# void tvb_free(tvbuff_t *tvb);
tvb_free = libwireshark.tvb_free
tvb_free.restype = None
tvb_free.argtypes = [POINTER(tvbuff_t)]

# void tvb_free_chain(tvbuff_t *tvb);
tvb_free_chain = libwireshark.tvb_free_chain
tvb_free_chain.restype = None
tvb_free_chain.argtypes = [POINTER(tvbuff_t)]

# void tvb_set_free_cb(tvbuff_t *tvb, const tvbuff_free_cb_t func);
tvb_set_free_cb = libwireshark.tvb_set_free_cb
tvb_set_free_cb.restype = None
tvb_set_free_cb.argtypes = [POINTER(tvbuff_t), tvbuff_free_cb_t]

# void tvb_set_child_real_data_tvbuff(tvbuff_t *parent,
#     tvbuff_t *child);
tvb_set_child_real_data_tvbuff = libwireshark.tvb_set_child_real_data_tvbuff
tvb_set_child_real_data_tvbuff.restype = None
tvb_set_child_real_data_tvbuff.argtypes = [
    POINTER(tvbuff_t), POINTER(tvbuff_t)]

# tvbuff_t *tvb_new_child_real_data(tvbuff_t *parent,
#     const guint8 *data, const guint length, const gint reported_length);
tvb_new_child_real_data = libwireshark.tvb_new_child_real_data
tvb_new_child_real_data.restype = POINTER(tvbuff_t)
tvb_new_child_real_data.argtypes = [POINTER(tvbuff_t),
                                    POINTER(guint8),
                                    guint,
                                    gint]

# tvbuff_t *tvb_new_real_data(const guint8 *data,
#     const guint length, const gint reported_length);
tvb_new_real_data = libwireshark.tvb_new_real_data
tvb_new_real_data.restype = POINTER(tvbuff_t)
tvb_new_real_data.argtypes = [POINTER(guint8), guint, gint]

# tvbuff_t *tvb_new_subset_length_caplen(tvbuff_t *backing,
#     const gint backing_offset, const gint backing_length,
#     const gint reported_length);
tvb_new_subset_length_caplen = libwireshark.tvb_new_subset_length_caplen
tvb_new_subset_length_caplen.restype = POINTER(tvbuff_t)
tvb_new_subset_length_caplen.argtypes = [POINTER(tvbuff_t),
                                         gint,
                                         gint,
                                         gint]

# tvbuff_t *tvb_new_subset_length(tvbuff_t *backing,
#     const gint backing_offset, const gint reported_length);
tvb_new_subset_length = libwireshark.tvb_new_subset_length
tvb_new_subset_length.restype = POINTER(tvbuff_t)
tvb_new_subset_length.argtypes = [POINTER(tvbuff_t), gint, gint]

# tvbuff_t *tvb_new_subset_remaining(tvbuff_t *backing,
#     const gint backing_offset);
tvb_new_subset_remaining = libwireshark.tvb_new_subset_remaining
tvb_new_subset_remaining.restype = POINTER(tvbuff_t)
tvb_new_subset_remaining.argtypes = [POINTER(tvbuff_t), gint]

# void tvb_composite_append(tvbuff_t *tvb, tvbuff_t *member);
tvb_composite_append = libwireshark.tvb_composite_append
tvb_composite_append.restype = None
tvb_composite_append.argtypes = [POINTER(tvbuff_t), POINTER(tvbuff_t)]

# tvbuff_t *tvb_new_composite(void);
tvb_new_composite = libwireshark.tvb_new_composite
tvb_new_composite.restype = POINTER(tvbuff_t)
tvb_new_composite.argtypes = []

# void tvb_composite_finalize(tvbuff_t *tvb);
tvb_composite_finalize = libwireshark.tvb_composite_finalize
tvb_composite_finalize.restype = None
tvb_composite_finalize.argtypes = [POINTER(tvbuff_t)]

# guint tvb_captured_length(const tvbuff_t *tvb);
tvb_captured_length = libwireshark.tvb_captured_length
tvb_captured_length.restype = guint
tvb_captured_length.argtypes = [POINTER(tvbuff_t)]

# gint tvb_captured_length_remaining(const tvbuff_t *tvb, const gint offset);
tvb_captured_length_remaining = libwireshark.tvb_captured_length_remaining
tvb_captured_length_remaining.restype = gint
tvb_captured_length_remaining.argtype = [POINTER(tvbuff_t), gint]

# guint tvb_ensure_captured_length_remaining(const tvbuff_t *tvb,
#     const gint offset);
tvb_ensure_captured_length_remaining = libwireshark.tvb_ensure_captured_length_remaining
tvb_ensure_captured_length_remaining.restype = guint
tvb_ensure_captured_length_remaining.argtypes = [POINTER(tvbuff_t), gint]

# gboolean tvb_bytes_exist(const tvbuff_t *tvb, const gint offset,
#     const gint length);
tvb_bytes_exist = libwireshark.tvb_bytes_exist
tvb_bytes_exist.restype = gboolean
tvb_bytes_exist.argtypes = [POINTER(tvbuff_t), gint, gint]

# void tvb_ensure_bytes_exist64(const tvbuff_t *tvb,
#     const gint offset, const guint64 length);
tvb_ensure_bytes_exist64 = libwireshark.tvb_ensure_bytes_exist64
tvb_ensure_bytes_exist64.restype = None
tvb_ensure_bytes_exist64.argtypes = [POINTER(tvbuff_t), gint, guint64]

# void tvb_ensure_bytes_exist(const tvbuff_t *tvb,
#     const gint offset, const gint length);
tvb_ensure_bytes_exist = libwireshark.tvb_ensure_bytes_exist
tvb_ensure_bytes_exist.restype = None
tvb_ensure_bytes_exist.argtypes = [POINTER(tvbuff_t), gint, gint]

# gboolean tvb_offset_exists(const tvbuff_t *tvb,
#     const gint offset);
tvb_offset_exists = libwireshark.tvb_offset_exists
tvb_offset_exists.restype = gboolean
tvb_offset_exists.argtypes = [POINTER(tvbuff_t), gint]

# guint tvb_reported_length(const tvbuff_t *tvb);
tvb_reported_length = libwireshark.tvb_reported_length
tvb_reported_length.restype = guint
tvb_reported_length.argtypes = [POINTER(tvbuff_t)]

# gint tvb_reported_length_remaining(const tvbuff_t *tvb,
#     const gint offset);
tvb_reported_length_remaining = libwireshark.tvb_reported_length_remaining
tvb_reported_length_remaining.restype = gint
tvb_reported_length_remaining.argtypes = [POINTER(tvbuff_t), gint]

# void tvb_set_reported_length(tvbuff_t *tvb, const guint);
tvb_set_reported_length = libwireshark.tvb_set_reported_length
tvb_set_reported_length.restype = None
tvb_set_reported_length.argtypes = [POINTER(tvbuff_t), guint]

# guint tvb_offset_from_real_beginning(const tvbuff_t *tvb);
tvb_offset_from_real_beginning = libwireshark.tvb_offset_from_real_beginning
tvb_offset_from_real_beginning.restype = guint
tvb_offset_from_real_beginning.argtypes = [POINTER(tvbuff_t)]

# gint tvb_raw_offset(tvbuff_t *tvb);
tvb_raw_offset = libwireshark.tvb_raw_offset
tvb_raw_offset.restype = gint
tvb_raw_offset.argtypes = [POINTER(tvbuff_t)]

# void tvb_set_fragment(tvbuff_t *tvb);
tvb_set_fragment = libwireshark.tvb_set_fragment
tvb_set_fragment.restype = None
tvb_set_fragment.argtypes = [POINTER(tvbuff_t)]

# struct tvbuff *tvb_get_ds_tvb(tvbuff_t *tvb);
tvb_get_ds_tvb = libwireshark.tvb_get_ds_tvb
tvb_get_ds_tvb.restype = POINTER(tvbuff)
tvb_get_ds_tvb.argtypes = [POINTER(tvbuff_t)]

# guint8 tvb_get_guint8(tvbuff_t *tvb, const gint offset);
tvb_get_guint8 = libwireshark.tvb_get_guint8
tvb_get_guint8.restype = guint8
tvb_get_guint8.argtypes = [POINTER(tvbuff_t), gint]

# gint8 tvb_get_gint8(tvbuff_t *tvb, const gint offset);
tvb_get_gint8 = libwireshark.tvb_get_gint8
tvb_get_gint8.restype = gint8
tvb_get_gint8.argtypes = [POINTER(tvbuff_t), gint]

# guint16 tvb_get_ntohs(tvbuff_t *tvb, const gint offset);
tvb_get_ntohs = libwireshark.tvb_get_ntohs
tvb_get_ntohs.restype = guint16
tvb_get_ntohs.argtypes = [POINTER(tvbuff_t), gint]

# gint16 tvb_get_ntohis(tvbuff_t *tvb, const gint offset);
tvb_get_ntohis = libwireshark.tvb_get_ntohis
tvb_get_ntohis.restype = gint16
tvb_get_ntohis.argtypes = [POINTER(tvbuff_t), gint]

# guint32 tvb_get_ntoh24(tvbuff_t *tvb, const gint offset);
tvb_get_ntoh24 = libwireshark.tvb_get_ntoh24
tvb_get_ntoh24.restype = guint32
tvb_get_ntoh24.argtypes = [POINTER(tvbuff_t), gint]

# gint32 tvb_get_ntohi24(tvbuff_t *tvb, const gint offset);
tvb_get_ntohi24 = libwireshark.tvb_get_ntohi24
tvb_get_ntohi24.restype = gint32
tvb_get_ntohi24.argtypes = [POINTER(tvbuff_t), gint]

# guint32 tvb_get_ntohl(tvbuff_t *tvb, const gint offset);
tvb_get_ntohl = libwireshark.tvb_get_ntohl
tvb_get_ntohl.restype = guint32
tvb_get_ntohl.argtypes = [POINTER(tvbuff_t), gint]

# gint32 tvb_get_ntohil(tvbuff_t *tvb, const gint offset);
tvb_get_ntohil = libwireshark.tvb_get_ntohil
tvb_get_ntohil.restype = gint32
tvb_get_ntohil.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_ntoh40(tvbuff_t *tvb, const gint offset);
tvb_get_ntoh40 = libwireshark.tvb_get_ntoh40
tvb_get_ntoh40.restype = guint64
tvb_get_ntoh40.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_ntohi40(tvbuff_t *tvb, const gint offset);
tvb_get_ntohi40 = libwireshark.tvb_get_ntohi40
tvb_get_ntohi40.restype = gint64
tvb_get_ntohi40.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_ntoh48(tvbuff_t *tvb, const gint offset);
tvb_get_ntoh48 = libwireshark.tvb_get_ntoh48
tvb_get_ntoh48.restype = guint64
tvb_get_ntoh48.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_ntohi48(tvbuff_t *tvb, const gint offset);
tvb_get_ntohi48 = libwireshark.tvb_get_ntohi48
tvb_get_ntohi48.restype = gint64
tvb_get_ntohi48.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_ntoh56(tvbuff_t *tvb, const gint offset);
tvb_get_ntoh56 = libwireshark.tvb_get_ntoh56
tvb_get_ntoh56.restype = guint64
tvb_get_ntoh56.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_ntohi56(tvbuff_t *tvb, const gint offset);
tvb_get_ntohi56 = libwireshark.tvb_get_ntohi56
tvb_get_ntohi56.restype = gint64
tvb_get_ntohi56.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_ntoh64(tvbuff_t *tvb, const gint offset);
tvb_get_ntoh64 = libwireshark.tvb_get_ntoh64
tvb_get_ntoh64.restype = guint64
tvb_get_ntoh64.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_ntohi64(tvbuff_t *tvb, const gint offset);
tvb_get_ntohi64 = libwireshark.tvb_get_ntohi64
tvb_get_ntohi64.restype = gint64
tvb_get_ntohi64.argtypes = [POINTER(tvbuff_t), gint]

# gfloat tvb_get_ntohieee_float(tvbuff_t *tvb, const gint offset);
tvb_get_ntohieee_float = libwireshark.tvb_get_ntohieee_float
tvb_get_ntohieee_float.restype = gfloat
tvb_get_ntohieee_float.argtypes = [POINTER(tvbuff_t), gint]

# gdouble tvb_get_ntohieee_double(tvbuff_t *tvb,
#     const gint offset);
tvb_get_ntohieee_double = libwireshark.tvb_get_ntohieee_double
tvb_get_ntohieee_double.restype = gdouble
tvb_get_ntohieee_double.argtypes = [POINTER(tvbuff_t), gint]

# guint16 tvb_get_letohs(tvbuff_t *tvb, const gint offset);
tvb_get_letohs = libwireshark.tvb_get_letohs
tvb_get_letohs.restype = guint16
tvb_get_letohs.argtypes = [POINTER(tvbuff_t), gint]

# gint16 tvb_get_letohis(tvbuff_t *tvb, const gint offset);
tvb_get_letohis = libwireshark.tvb_get_letohis
tvb_get_letohis.restype = gint16
tvb_get_letohis.argtypes = [POINTER(tvbuff_t), gint]

# guint32 tvb_get_letoh24(tvbuff_t *tvb, const gint offset);
tvb_get_letoh24 = libwireshark.tvb_get_letoh24
tvb_get_letoh24.restype = guint32
tvb_get_letoh24.argtypes = [POINTER(tvbuff_t), gint]

# gint32 tvb_get_letohi24(tvbuff_t *tvb, const gint offset);
tvb_get_letohi24 = libwireshark.tvb_get_letohi24
tvb_get_letohi24.restype = gint32
tvb_get_letohi24.argtypes = [POINTER(tvbuff_t), gint]

# guint32 tvb_get_letohl(tvbuff_t *tvb, const gint offset);
tvb_get_letohl = libwireshark.tvb_get_letohl
tvb_get_letohl.restype = guint32
tvb_get_letohl.argtypes = [POINTER(tvbuff_t), gint]

# gint32 tvb_get_letohil(tvbuff_t *tvb, const gint offset);
tvb_get_letohil = libwireshark.tvb_get_letohil
tvb_get_letohil.restype = gint32
tvb_get_letohil.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_letoh40(tvbuff_t *tvb, const gint offset);
tvb_get_letoh40 = libwireshark.tvb_get_letoh40
tvb_get_letoh40.restype = guint64
tvb_get_letoh40.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_letohi40(tvbuff_t *tvb, const gint offset);
tvb_get_letohi40 = libwireshark.tvb_get_letohi40
tvb_get_letohi40.restype = gint64
tvb_get_letohi40.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_letoh48(tvbuff_t *tvb, const gint offset);
tvb_get_letoh48 = libwireshark.tvb_get_letoh48
tvb_get_letoh48.restype = guint64
tvb_get_letoh48.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_letohi48(tvbuff_t *tvb, const gint offset);
tvb_get_letohi48 = libwireshark.tvb_get_letohi48
tvb_get_letohi48.restype = gint64
tvb_get_letohi48.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_letoh56(tvbuff_t *tvb, const gint offset);
tvb_get_letoh56 = libwireshark.tvb_get_letoh56
tvb_get_letoh56.restype = guint64
tvb_get_letoh56.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_letohi56(tvbuff_t *tvb, const gint offset);
tvb_get_letohi56 = libwireshark.tvb_get_letohi56
tvb_get_letohi56.restype = gint64
tvb_get_letohi56.argtypes = [POINTER(tvbuff_t), gint]

# guint64 tvb_get_letoh64(tvbuff_t *tvb, const gint offset);
tvb_get_letoh64 = libwireshark.tvb_get_letoh64
tvb_get_letoh64.restype = guint64
tvb_get_letoh64.argtypes = [POINTER(tvbuff_t), gint]

# gint64 tvb_get_letohi64(tvbuff_t *tvb, const gint offset);
tvb_get_letohi64 = libwireshark.tvb_get_letohi64
tvb_get_letohi64.restype = gint64
tvb_get_letohi64.argtypes = [POINTER(tvbuff_t), gint]

# gfloat tvb_get_letohieee_float(tvbuff_t *tvb, const gint offset);
tvb_get_letohieee_float = libwireshark.tvb_get_letohieee_float
tvb_get_letohieee_float.restype = gfloat
tvb_get_letohieee_float.argtypes = [POINTER(tvbuff_t), gint]

# gdouble tvb_get_letohieee_double(tvbuff_t *tvb,
#     const gint offset);
tvb_get_letohieee_double = libwireshark.tvb_get_letohieee_double
tvb_get_letohieee_double.restype = gdouble
tvb_get_letohieee_double.argtypes = [POINTER(tvbuff_t), gint]

# guint16 tvb_get_guint16(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_guint16 = libwireshark.tvb_get_guint16
tvb_get_guint16.restype = guint16
tvb_get_guint16.argtypes = [POINTER(tvbuff_t), gint, guint]

# gint16 tvb_get_gint16(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_gint16 = libwireshark.tvb_get_gint16
tvb_get_gint16.restype = gint16
tvb_get_gint16.argtypes = [POINTER(tvbuff_t), gint, guint]

# guint32 tvb_get_guint24(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_guint24 = libwireshark.tvb_get_guint24
tvb_get_guint24.restype = guint32
tvb_get_guint24.argtypes = [POINTER(tvbuff_t), gint, guint]

# gint32 tvb_get_gint24(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_gint24 = libwireshark.tvb_get_gint24
tvb_get_gint24.restype = gint32
tvb_get_gint24.argtypes = [POINTER(tvbuff_t), gint, guint]

# guint32 tvb_get_guint32(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_guint32 = libwireshark.tvb_get_guint32
tvb_get_guint32.restype = guint32
tvb_get_guint32.argtypes = [POINTER(tvbuff_t), gint, guint]

# gint32 tvb_get_gint32(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_gint32 = libwireshark.tvb_get_gint32
tvb_get_gint32.restype = gint32
tvb_get_gint32.argtypes = [POINTER(tvbuff_t), gint, guint]

# guint64 tvb_get_guint40(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_guint40 = libwireshark.tvb_get_guint40
tvb_get_guint40.restype = guint64
tvb_get_guint40.argtypes = [POINTER(tvbuff_t), gint, guint]

# gint64 tvb_get_gint40(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_gint40 = libwireshark.tvb_get_gint40
tvb_get_gint40.restype = gint64
tvb_get_gint40.argtypes = [POINTER(tvbuff_t), gint, guint]

# guint64 tvb_get_guint48(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_guint48 = libwireshark.tvb_get_guint48
tvb_get_guint48.restype = guint64
tvb_get_guint48.argtypes = [POINTER(tvbuff_t), gint, guint]

# gint64 tvb_get_gint48(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_gint48 = libwireshark.tvb_get_gint48
tvb_get_gint48.restype = gint64
tvb_get_gint48.argtypes = [POINTER(tvbuff_t), gint, guint]

# guint64 tvb_get_guint56(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_guint56 = libwireshark.tvb_get_guint56
tvb_get_guint56.restype = guint64
tvb_get_guint56.argtypes = [POINTER(tvbuff_t), gint, guint]

# gint64 tvb_get_gint56(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_gint56 = libwireshark.tvb_get_gint56
tvb_get_gint56.restype = gint64
tvb_get_gint56.argtypes = [POINTER(tvbuff_t), gint, guint]

# guint64 tvb_get_guint64(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_guint64 = libwireshark.tvb_get_guint64
tvb_get_guint64.restype = guint64
tvb_get_guint64.argtypes = [POINTER(tvbuff_t), gint, guint]

# gint64 tvb_get_gint64(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_gint64 = libwireshark.tvb_get_gint64
tvb_get_gint64.restype = gint64
tvb_get_gint64.argtypes = [POINTER(tvbuff_t), gint, guint]

# gfloat tvb_get_ieee_float(tvbuff_t *tvb, const gint offset, const guint
# encoding);
tvb_get_ieee_float = libwireshark.tvb_get_ieee_float
tvb_get_ieee_float.restype = gfloat
tvb_get_ieee_float.argtypes = [POINTER(tvbuff_t), gint, guint]

# gdouble tvb_get_ieee_double(tvbuff_t *tvb, const gint offset, const
# guint encoding);
tvb_get_ieee_double = libwireshark.tvb_get_ieee_double
tvb_get_ieee_double.restype = gdouble
tvb_get_ieee_double.argtypes = [POINTER(tvbuff_t), gint, guint]

# #if G_BYTE_ORDER == G_LITTLE_ENDIAN
if sys.byteorder == 'little':
    # #define tvb_get_h_guint16   tvb_get_letohs
    tvb_get_h_guint16 = tvb_get_letohs

    # #define tvb_get_h_guint32   tvb_get_letohl
    tvb_get_h_guint32 = tvb_get_letohl

# #elif G_BYTE_ORDER == G_BIG_ENDIAN
elif sys.byteorder == 'big':
    # #define tvb_get_h_guint16   tvb_get_ntohs
    tvb_get_h_guint16 = tvb_get_ntohs

    # #define tvb_get_h_guint32   tvb_get_ntohl
    tvb_get_h_guint32 = tvb_get_ntohl


# nstime_t* tvb_get_string_time(tvbuff_t *tvb, const gint offset, const gint length,
# const guint encoding, nstime_t* ns, gint *endoff);
tvb_get_string_time = libwireshark.tvb_get_string_time
tvb_get_string_time.restype = POINTER(nstime_t)
tvb_get_string_time.argtypes = [POINTER(tvbuff_t),
                                gint,
                                gint,
                                guint,
                                POINTER(nstime_t),
                                POINTER(gint)]

# GByteArray* tvb_get_string_bytes(tvbuff_t *tvb, const gint offset, const gint length,
# const guint encoding, GByteArray* bytes, gint *endoff);
tvb_get_string_bytes = libwireshark.tvb_get_string_bytes
tvb_get_string_bytes.restype = POINTER(GByteArray)
tvb_get_string_bytes.argtypes = [POINTER(tvbuff_t),
                                 gint,
                                 gint,
                                 guint,
                                 POINTER(GByteArray),
                                 POINTER(gint)]

# guint32 tvb_get_ipv4(tvbuff_t *tvb, const gint offset);
tvb_get_ipv4 = libwireshark.tvb_get_ipv4
tvb_get_ipv4.restype = guint32
tvb_get_ipv4.argtypes = [POINTER(tvbuff_t), gint]

# void tvb_get_ipv6(tvbuff_t *tvb, const gint offset,
#     ws_in6_addr *addr);
tvb_get_ipv6 = libwireshark.tvb_get_ipv6
tvb_get_ipv6.restype = None
tvb_get_ipv6.argtypes = [POINTER(tvbuff_t), gint, POINTER(ws_in6_addr)]

# void tvb_get_ntohguid(tvbuff_t *tvb, const gint offset,
#     e_guid_t *guid);
tvb_get_ntohguid = libwireshark.tvb_get_ntohguid
tvb_get_ntohguid.restype = None
tvb_get_ntohguid.argtypes = [POINTER(tvbuff_t), gint, POINTER(e_guid_t)]

# void tvb_get_letohguid(tvbuff_t *tvb, const gint offset,
#     e_guid_t *guid);
tvb_get_letohguid = libwireshark.tvb_get_letohguid
tvb_get_letohguid.restype = None
tvb_get_letohguid.argtypes = [POINTER(tvbuff_t), gint, POINTER(e_guid_t)]

# void tvb_get_guid(tvbuff_t *tvb, const gint offset,
#     e_guid_t *guid, const guint encoding);
tvb_get_guid = libwireshark.tvb_get_guid
tvb_get_guid.restype = None
tvb_get_guid.argtypes = [POINTER(tvbuff_t),
                         gint,
                         POINTER(e_guid_t),
                         guint]

# guint8 tvb_get_bits8(tvbuff_t *tvb, guint bit_offset,
#     const gint no_of_bits);
tvb_get_bits8 = libwireshark.tvb_get_bits8
tvb_get_bits8.restype = guint8
tvb_get_bits8.argtypes = [POINTER(tvbuff_t), guint, gint]

# guint16 tvb_get_bits16(tvbuff_t *tvb, guint bit_offset,
#     const gint no_of_bits, const guint encoding);
tvb_get_bits16 = libwireshark.tvb_get_bits16
tvb_get_bits16.restype = guint16
tvb_get_bits16.argtypes = [POINTER(tvbuff_t),
                           guint,
                           gint,
                           guint]

# guint32 tvb_get_bits32(tvbuff_t *tvb, guint bit_offset,
#     const gint no_of_bits, const guint encoding);
tvb_get_bits32 = libwireshark.tvb_get_bits32
tvb_get_bits32.restype = guint32
tvb_get_bits32.argtypes = [POINTER(tvbuff_t),
                           guint,
                           gint,
                           guint]

# guint64 tvb_get_bits64(tvbuff_t *tvb, guint bit_offset,
#     const gint no_of_bits, const guint encoding);
tvb_get_bits64 = libwireshark.tvb_get_bits64
tvb_get_bits64.restype = guint64
tvb_get_bits64.argtypes = [POINTER(tvbuff_t),
                           guint,
                           gint,
                           guint]

# guint32 tvb_get_bits(tvbuff_t *tvb, const guint bit_offset,
#     const gint no_of_bits, const guint encoding);
tvb_get_bits = libwireshark.tvb_get_bits
tvb_get_bits.restype = guint32
tvb_get_bits.argtypes = [POINTER(tvbuff_t), guint, gint, guint]

# void *tvb_memcpy(tvbuff_t *tvb, void *target, const gint offset,
#     size_t length);
tvb_memcpy = libwireshark.tvb_memcpy
tvb_memcpy.restype = c_void_p
tvb_memcpy.argtypes = [POINTER(tvbuff_t), c_void_p, gint, c_size_t]

# void *tvb_memdup(wmem_allocator_t *scope, tvbuff_t *tvb,
#     const gint offset, size_t length);
tvb_memdup = libwireshark.tvb_memdup
tvb_memdup.restype = c_void_p
tvb_memdup.argtypes = [POINTER(wmem_allocator_t),
                       POINTER(tvbuff_t),
                       gint,
                       c_size_t]

# const guint8 *tvb_get_ptr(tvbuff_t *tvb, const gint offset,
#     const gint length);
tvb_get_ptr = libwireshark.tvb_get_ptr
tvb_get_ptr.restype = POINTER(guint8)
tvb_get_ptr.argtypes = [POINTER(tvbuff_t), gint, gint]

# gint tvb_find_guint8(tvbuff_t *tvb, const gint offset,
#     const gint maxlength, const guint8 needle);
tvb_find_guint8 = libwireshark.tvb_find_guint8
tvb_find_guint8.restype = gint
tvb_find_guint8.argtypes = [POINTER(tvbuff_t), gint, gint, guint8]

# gint tvb_find_guint16(tvbuff_t *tvb, const gint offset,
#     const gint maxlength, const guint16 needle);
tvb_find_guint16 = libwireshark.tvb_find_guint16
tvb_find_guint16.restype = gint
tvb_find_guint16.argtypes = [POINTER(tvbuff_t), gint, gint, guint16]

# gint tvb_ws_mempbrk_pattern_guint8(tvbuff_t *tvb, const gint offset,
# const gint maxlength, const ws_mempbrk_pattern* pattern, guchar
# *found_needle);
tvb_ws_mempbrk_pattern_guint8 = libwireshark.tvb_ws_mempbrk_pattern_guint8
tvb_ws_mempbrk_pattern_guint8.restype = gint
tvb_ws_mempbrk_pattern_guint8.argtypes = [POINTER(tvbuff_t),
                                          gint,
                                          gint,
                                          POINTER(ws_mempbrk_pattern),
                                          POINTER(guchar)]

# guint tvb_strsize(tvbuff_t *tvb, const gint offset);
tvb_strsize = libwireshark.tvb_strsize
tvb_strsize.restype = guint
tvb_strsize.argtypes = [POINTER(tvbuff_t), gint]

# guint tvb_unicode_strsize(tvbuff_t *tvb, const gint offset);
tvb_unicode_strsize = libwireshark.tvb_unicode_strsize
tvb_unicode_strsize.restype = guint
tvb_unicode_strsize.argtypes = [POINTER(tvbuff_t), gint]

# gint tvb_strnlen(tvbuff_t *tvb, const gint offset,
#     const guint maxlength);
tvb_strnlen = libwireshark.tvb_strnlen
tvb_strnlen.restype = gint
tvb_strnlen.argtypes = [POINTER(tvbuff_t), gint, guint]

# gchar *tvb_format_text(tvbuff_t *tvb, const gint offset,
#     const gint size);
tvb_format_text = libwireshark.tvb_format_text
tvb_format_text.restype = gchar_p
tvb_format_text.argtypes = [POINTER(tvbuff_t), gint, gint]

# gchar *tvb_format_text_wsp(wmem_allocator_t* allocator, tvbuff_t *tvb, const gint offset,
#     const gint size);
tvb_format_text_wsp = libwireshark.tvb_format_text_wsp
tvb_format_text_wsp.restype = gchar_p
tvb_format_text_wsp.argtypes = [POINTER(wmem_allocator_t),
                                POINTER(tvbuff_t),
                                gint,
                                gint]

# guint8 *tvb_get_string_enc(wmem_allocator_t *scope,
# tvbuff_t *tvb, const gint offset, const gint length, const guint
# encoding);
tvb_get_string_enc = libwireshark.tvb_get_string_enc
tvb_get_string_enc.restype = POINTER(guint8)
tvb_get_string_enc.argtypes = [POINTER(wmem_allocator_t),
                               POINTER(tvbuff_t),
                               gint,
                               gint,
                               guint]

# gchar *tvb_get_ts_23_038_7bits_string(wmem_allocator_t *scope,
#     tvbuff_t *tvb, const gint bit_offset, gint no_of_chars);
tvb_get_ts_23_038_7bits_string = libwireshark.tvb_get_ts_23_038_7bits_string
tvb_get_ts_23_038_7bits_string.restype = gchar_p
tvb_get_ts_23_038_7bits_string.argtypes = [POINTER(wmem_allocator_t),
                                           POINTER(tvbuff_t),
                                           gint,
                                           gint]

# gchar *tvb_get_ascii_7bits_string(wmem_allocator_t *scope,
#     tvbuff_t *tvb, const gint bit_offset, gint no_of_chars);
tvb_get_ascii_7bits_string = libwireshark.tvb_get_ascii_7bits_string
tvb_get_ascii_7bits_string.restype = gchar_p
tvb_get_ascii_7bits_string.argtypes = [POINTER(wmem_allocator_t),
                                       POINTER(tvbuff_t),
                                       gint,
                                       gint]

# guint8 *tvb_get_stringzpad(wmem_allocator_t *scope,
# tvbuff_t *tvb, const gint offset, const gint length, const guint
# encoding);
tvb_get_stringzpad = libwireshark.tvb_get_stringzpad
tvb_get_stringzpad.restype = POINTER(guint8)
tvb_get_stringzpad.argtypes = [POINTER(wmem_allocator_t),
                               POINTER(tvbuff_t),
                               gint,
                               gint,
                               guint]

# guint8 *tvb_get_stringz_enc(wmem_allocator_t *scope,
#     tvbuff_t *tvb, const gint offset, gint *lengthp, const guint encoding);
tvb_get_stringz_enc = libwireshark.tvb_get_stringz_enc
tvb_get_stringz_enc.restype = POINTER(guint8)
tvb_get_stringz_enc.argtypes = [POINTER(wmem_allocator_t),
                                POINTER(tvbuff_t),
                                gint,
                                POINTER(gint),
                                guint]

# const guint8 *tvb_get_const_stringz(tvbuff_t *tvb,
#     const gint offset, gint *lengthp);
tvb_get_const_stringz = libwireshark.tvb_get_const_stringz
tvb_get_const_stringz.restype = POINTER(guint8)
tvb_get_const_stringz.argtypes = [POINTER(tvbuff_t), gint, POINTER(gint)]

# gint tvb_get_nstringz(tvbuff_t *tvb, const gint offset,
#     const guint bufsize, guint8 *buffer);
tvb_get_nstringz = libwireshark.tvb_get_nstringz
tvb_get_nstringz.restype = gint
tvb_get_nstringz.argtypes = [POINTER(tvbuff_t), gint, guint, POINTER(guint8)]

# gint tvb_get_nstringz0(tvbuff_t *tvb, const gint offset,
#     const guint bufsize, guint8 *buffer);
tvb_get_nstringz0 = libwireshark.tvb_get_nstringz0
tvb_get_nstringz0.restype = gint
tvb_get_nstringz0.argtypes = [POINTER(tvbuff_t),
                              gint,
                              guint,
                              POINTER(guint8)]

# gint tvb_get_raw_bytes_as_string(tvbuff_t *tvb, const gint offset, char
# *buffer, size_t bufsize);
tvb_get_raw_bytes_as_string = libwireshark.tvb_get_raw_bytes_as_string
tvb_get_raw_bytes_as_string.restype = gint
tvb_get_raw_bytes_as_string.argtypes = [POINTER(tvbuff_t),
                                        gint,
                                        c_char_p,
                                        c_size_t]

# gboolean tvb_ascii_isprint(tvbuff_t *tvb, const gint offset,
# 	const gint length);
tvb_ascii_isprint = libwireshark.tvb_ascii_isprint
tvb_ascii_isprint.restype = gboolean
tvb_ascii_isprint.argtypes = [POINTER(tvbuff_t),
                              gint,
                              gint]

# gint tvb_find_line_end(tvbuff_t *tvb, const gint offset, int len,
#     gint *next_offset, const gboolean desegment);
tvb_find_line_end = libwireshark.tvb_find_line_end
tvb_find_line_end.restype = gint
tvb_find_line_end.argtypes = [POINTER(tvbuff_t),
                              gint,
                              c_int,
                              POINTER(gint),
                              gboolean]

# gint tvb_find_line_end_unquoted(tvbuff_t *tvb, const gint offset,
#     int len, gint *next_offset);
tvb_find_line_end_unquoted = libwireshark.tvb_find_line_end_unquoted
tvb_find_line_end_unquoted.restype = gint
tvb_find_line_end_unquoted.argtypes = [POINTER(tvbuff_t),
                                       gint,
                                       c_int,
                                       POINTER(gint)]

# gint tvb_skip_wsp(tvbuff_t *tvb, const gint offset,
#     const gint maxlength);
tvb_skip_wsp = libwireshark.tvb_skip_wsp
tvb_skip_wsp.restype = gint
tvb_skip_wsp.argtypes = [POINTER(tvbuff_t),
                         gint,
                         gint]

# gint tvb_skip_wsp_return(tvbuff_t *tvb, const gint offset);
tvb_skip_wsp_return = libwireshark.tvb_skip_wsp_return
tvb_skip_wsp_return.restype = gint
tvb_skip_wsp_return.argtypes = [POINTER(tvbuff_t), gint]

# int tvb_get_token_len(tvbuff_t *tvb, const gint offset, int len, gint
# *next_offset, const gboolean desegment);
tvb_get_token_len = libwireshark.tvb_get_token_len
tvb_get_token_len.restype = c_int
tvb_get_token_len.argtypes = [POINTER(tvbuff_t),
                              gint,
                              c_int,
                              POINTER(gint),
                              gboolean]

# gint tvb_strneql(tvbuff_t *tvb, const gint offset,
#     const gchar *str, const size_t size);
tvb_strneql = libwireshark.tvb_strneql
tvb_strneql.restype = gint
tvb_strneql.argtypes = [POINTER(tvbuff_t),
                        gint,
                        gchar_p,
                        c_size_t]

# gint tvb_strncaseeql(tvbuff_t *tvb, const gint offset,
#     const gchar *str, const size_t size);
tvb_strncaseeql = libwireshark.tvb_strncaseeql
tvb_strncaseeql.restype = gint
tvb_strncaseeql.argtypes = [POINTER(tvbuff_t),
                            gint,
                            gchar_p,
                            c_size_t]

# gint tvb_memeql(tvbuff_t *tvb, const gint offset,
#     const guint8 *str, size_t size);
tvb_memeql = libwireshark.tvb_memeql
tvb_memeql.restype = gint
tvb_memeql.argtypes = [POINTER(tvbuff_t),
                       gint,
                       POINTER(guint8),
                       c_size_t]

# gchar *tvb_bytes_to_str_punct(wmem_allocator_t *scope, tvbuff_t *tvb, const gint offset,
#     const gint len, const gchar punct);
tvb_bytes_to_str_punct = libwireshark.tvb_bytes_to_str_punct
tvb_bytes_to_str_punct.restype = gchar_p
tvb_bytes_to_str_punct.argtypes = [POINTER(wmem_allocator_t),
                                   POINTER(tvbuff_t),
                                   gint,
                                   gint,
                                   gchar]

# gchar *tvb_bytes_to_str(wmem_allocator_t *allocator, tvbuff_t *tvb,
#     const gint offset, const gint len);
tvb_bytes_to_str = libwireshark.tvb_bytes_to_str
tvb_bytes_to_str.restype = gchar_p
tvb_bytes_to_str.argtypes = [POINTER(wmem_allocator_t),
                             POINTER(tvbuff_t),
                             gint,
                             gint]


# typedef struct dgt_set_t {
#     const unsigned char out[16];
# } dgt_set_t;
class dgt_set_t(Structure):
    _fields_ = [('out', c_char * 16)]


# const gchar *tvb_bcd_dig_to_wmem_packet_str(tvbuff_t *tvb,
#     const gint offset, const gint len, const dgt_set_t *dgt,
#     gboolean skip_first);
tvb_bcd_dig_to_wmem_packet_str = libwireshark.tvb_bcd_dig_to_wmem_packet_str
tvb_bcd_dig_to_wmem_packet_str.restype = gchar_p
tvb_bcd_dig_to_wmem_packet_str.argtypes = [POINTER(tvbuff_t),
                                           gint,
                                           gint,
                                           POINTER(dgt_set_t),
                                           gboolean]

# gint tvb_find_tvb(tvbuff_t *haystack_tvb, tvbuff_t *needle_tvb,
#     const gint haystack_offset);
tvb_find_tvb = libwireshark.tvb_find_tvb
tvb_find_tvb.restype = gint
tvb_find_tvb.argtypes = [POINTER(tvbuff_t),
                         POINTER(tvbuff_t),
                         gint]

# tvbuff_t *tvb_uncompress(tvbuff_t *tvb, const int offset,
#     int comprlen);
tvb_uncompress = libwireshark.tvb_uncompress
tvb_uncompress.restype = POINTER(tvbuff_t)
tvb_uncompress.argtypes = [POINTER(tvbuff_t), c_int, c_int]

# tvbuff_t *tvb_child_uncompress(tvbuff_t *parent, tvbuff_t *tvb,
#     const int offset, int comprlen);
tvb_child_uncompress = libwireshark.tvb_child_uncompress
tvb_child_uncompress.restype = POINTER(tvbuff_t)
tvb_child_uncompress.argtypes = [POINTER(tvbuff_t),
                                 POINTER(tvbuff_t),
                                 c_int,
                                 c_int]

# tvbuff_t *tvb_uncompress_brotli(tvbuff_t *tvb, const int offset,
#     int comprlen);
tvb_uncompress_brotli = libwireshark.tvb_uncompress_brotli
tvb_uncompress_brotli.restype = POINTER(tvbuff_t)
tvb_uncompress_brotli.argtypes = [POINTER(tvbuff_t), c_int, c_int]

# tvbuff_t *tvb_child_uncompress_brotli(tvbuff_t *parent, tvbuff_t *tvb,
#     const int offset, int comprlen);
tvb_child_uncompress_brotli = libwireshark.tvb_child_uncompress_brotli
tvb_child_uncompress_brotli.restype = POINTER(tvbuff_t)
tvb_child_uncompress_brotli.argtypes = [POINTER(tvbuff_t),
                                        POINTER(tvbuff_t),
                                        c_int,
                                        c_int]

# tvbuff_t *tvb_uncompress_lz77(tvbuff_t *tvb,
#     const int offset, int comprlen);
tvb_uncompress_lz77 = libwireshark.tvb_uncompress_lz77
tvb_uncompress_lz77.restype = POINTER(tvbuff_t)
tvb_uncompress_lz77.argtypes = [POINTER(tvbuff_t), c_int, c_int]

# tvbuff_t *tvb_child_uncompress_lz77(tvbuff_t *parent,
#      tvbuff_t *tvb, const int offset, int comprlen);
tvb_child_uncompress_lz77 = libwireshark.tvb_child_uncompress_lz77
tvb_child_uncompress_lz77.restype = POINTER(tvbuff_t)
tvb_child_uncompress_lz77.argtypes = [POINTER(tvbuff_t),
                                      POINTER(tvbuff_t),
                                      c_int,
                                      c_int]

# tvbuff_t *tvb_uncompress_lz77huff(tvbuff_t *tvb,
#     const int offset, int comprlen);
tvb_uncompress_lz77huff = libwireshark.tvb_uncompress_lz77huff
tvb_uncompress_lz77huff.restype = POINTER(tvbuff_t)
tvb_uncompress_lz77huff.argtypes = [POINTER(tvbuff_t), c_int, c_int]

# tvbuff_t *tvb_child_uncompress_lz77huff(tvbuff_t *parent,
#     tvbuff_t *tvb, const int offset, int comprlen);
tvb_child_uncompress_lz77huff = libwireshark.tvb_child_uncompress_lz77huff
tvb_child_uncompress_lz77huff.restype = POINTER(tvbuff_t)
tvb_child_uncompress_lz77huff.argtypes = [POINTER(tvbuff_t),
                                          POINTER(tvbuff_t),
                                          c_int,
                                          c_int]

# tvbuff_t *tvb_uncompress_lznt1(tvbuff_t *tvb,
#     const int offset, int comprlen);
tvb_uncompress_lznt1 = libwireshark.tvb_uncompress_lznt1
tvb_uncompress_lznt1.restype = POINTER(tvbuff_t)
tvb_uncompress_lznt1.argtypes = [POINTER(tvbuff_t), c_int, c_int]

# tvbuff_t *tvb_child_uncompress_lznt1(tvbuff_t *parent,
#     tvbuff_t *tvb, const int offset, int comprlen);
tvb_child_uncompress_lznt1 = libwireshark.tvb_child_uncompress_lznt1
tvb_child_uncompress_lznt1.restype = POINTER(tvbuff_t)
tvb_child_uncompress_lznt1.argtypes = [POINTER(tvbuff_t),
                                       POINTER(tvbuff_t),
                                       c_int,
                                       c_int]

# guint tvb_get_varint(tvbuff_t *tvb, guint offset, guint maxlen, guint64
# *value, const guint encoding);
tvb_get_varint = libwireshark.tvb_get_varint
tvb_get_varint.restype = guint
tvb_get_varint.argtypes = [POINTER(tvbuff_t),
                           guint,
                           POINTER(guint64),
                           guint]


############
# params.h #
############

# typedef struct {
# 	const char	*name;
# 	const char	*description;
# 	gint		value;
# } enum_val_t;
class enum_val_t(Structure):
    _fields_ = [('name', c_char_p),
                ('description', c_char_p),
                ('value', gint)]


###########
# range.h #
###########

# #define MAX_SCTP_PORT 65535
MAX_SCTP_PORT = 65535

# #define MAX_TCP_PORT 65535
MAX_TCP_PORT = 65535

# #define MAX_UDP_PORT 65535
MAX_UDP_PORT = 65535

# #define MAX_DCCP_PORT 65535
MAX_DCCP_PORT = 65535


# typedef struct range_admin_tag {
#     guint32 low;
#     guint32 high;
# } range_admin_t;
class range_admin_tag(Structure):
    _fields_ = [('low', guint32),
                ('high', guint32)]


range_admin_t = range_admin_tag


# #define RANGE_ADMIN_T_INITIALIZER { 0, 0 }
RANGE_ADMIN_T_INITIALIZER = range_admin_tag(0, 0)

# typedef struct epan_range {
#     guint           nranges;
#     range_admin_t   ranges[1];
# } range_t;


class epan_range(Structure):
    _fields_ = [('nranges', guint),
                ('ranges', range_admin_t * 1)]


range_t = epan_range


# typedef enum {
#     CVT_NO_ERROR,
#     CVT_SYNTAX_ERROR,
#     CVT_NUMBER_TOO_BIG
# } convert_ret_t;
convert_ret_t = c_int
CVT_NO_ERROR = c_int(0)
CVT_SYNTAX_ERROR = c_int(1)
CVT_NUMBER_TOO_BIG = c_int(2)

# range_t *range_empty(wmem_allocator_t *scope);
range_empty = libwireshark.range_empty
range_empty.restype = POINTER(range_t)
range_empty.argtypes = [POINTER(wmem_allocator_t)]

# convert_ret_t range_convert_str(wmem_allocator_t *scope, range_t **range, const gchar *es,
#     guint32 max_value);
range_convert_str = libwireshark.range_convert_str
range_convert_str.restype = convert_ret_t
range_convert_str.argtypes = [POINTER(wmem_allocator_t),
                              POINTER(POINTER(range_t)),
                              gchar_p,
                              guint32]

# convert_ret_t range_convert_str_work(wmem_allocator_t *scope, range_t **range, const gchar *es,
#     guint32 max_value, gboolean err_on_max);
range_convert_str_work = libwireshark.range_convert_str_work
range_convert_str_work.restype = convert_ret_t
range_convert_str_work.argtypes = [POINTER(wmem_allocator_t),
                                   POINTER(POINTER(range_t)),
                                   gchar_p,
                                   guint32,
                                   gboolean]

# gboolean value_is_in_range(range_t *range, guint32 val);
value_is_in_range = libwireshark.value_is_in_range
value_is_in_range.restype = gboolean
value_is_in_range.argtypes = [POINTER(range_t), guint32]

# gboolean range_add_value(wmem_allocator_t *scope, range_t **range,
# guint32 val);
range_add_value = libwireshark.range_add_value
range_add_value.restype = gboolean
range_add_value.argtypes = [POINTER(wmem_allocator_t),
                            POINTER(POINTER(range_t)),
                            guint32]

# gboolean range_remove_value(wmem_allocator_t *scope, range_t **range,
# guint32 val);
range_remove_value = libwireshark.range_remove_value
range_remove_value.restype = gboolean
range_remove_value.argtypes = [POINTER(wmem_allocator_t),
                               POINTER(POINTER(range_t)),
                               guint32]

# gboolean ranges_are_equal(range_t *a, range_t *b);
ranges_are_equal = libwireshark.ranges_are_equal
ranges_are_equal.restype = gboolean
ranges_are_equal.argtypes = [POINTER(range_t), POINTER(range_t)]

# void range_foreach(range_t *range, void (*callback)(guint32 val,
# gpointer ptr), gpointer ptr);
range_foreach = libwireshark.range_foreach
range_foreach.restype = None
range_foreach.argtypes = [POINTER(range_t),
                          CFUNCTYPE(None, guint32, gpointer, gpointer),
                          gpointer]

# char *range_convert_range(wmem_allocator_t *scope, const range_t *range);
range_convert_range = libwireshark.range_convert_range
range_convert_range.restype = c_char_p
range_convert_range.argtypes = [POINTER(wmem_allocator_t), POINTER(range_t)]

# range_t *range_copy(wmem_allocator_t *scope, range_t *src);
range_copy = libwireshark.range_copy
range_copy.restype = POINTER(range_t)
range_copy.argtypes = [POINTER(wmem_allocator_t), POINTER(range_t)]


###########
# prefs.h #
###########

# #define DEF_WIDTH 750
DEF_WIDTH = 750

# #define DEF_HEIGHT 550
DEF_HEIGHT = 550

# #define MAX_VAL_LEN  1024
MAX_VAL_LEN = 1024

# #define TAP_UPDATE_DEFAULT_INTERVAL 3000
TAP_UPDATE_DEFAULT_INTERVAL = 3000

# #define ST_DEF_BURSTRES 5
ST_DEF_BURSTRES = 5

# #define ST_DEF_BURSTLEN 100
ST_DEF_BURSTLEN = 100

# #define ST_MAX_BURSTRES 600000
ST_MAX_BURSTRES = 600000

# #define ST_MAX_BURSTBUCKETS 100
ST_MAX_BURSTBUCKETS = 100


# struct epan_uat;
class epan_uat(Structure):
    _fields_ = []


# struct _e_addr_resolve;
class _e_addr_resolve(Structure):
    _fields_ = []


# char string_to_name_resolve(const char *string, struct _e_addr_resolve
# *name_resolve);
string_to_name_resolve = libwireshark.string_to_name_resolve
string_to_name_resolve.restype = c_char
string_to_name_resolve.argtypes = [c_char_p, POINTER(_e_addr_resolve)]

# #define FO_STYLE_LAST_OPENED    0
FO_STYLE_LAST_OPENED = 0

# #define FO_STYLE_SPECIFIED      1
FO_STYLE_SPECIFIED = 1

# #define TB_STYLE_ICONS          0
TB_STYLE_ICONS = 0

# #define TB_STYLE_TEXT           1
TB_STYLE_TEXT = 1

# #define TB_STYLE_BOTH           2
TB_STYLE_BOTH = 2

# #define COLOR_STYLE_DEFAULT     0
COLOR_STYLE_DEFAULT = 0

# #define COLOR_STYLE_FLAT        1
COLOR_STYLE_FLAT = 1

# #define COLOR_STYLE_GRADIENT    2
COLOR_STYLE_GRADIENT = 2

# #define COLOR_STYLE_ALPHA       0.25
COLOR_STYLE_ALPHA = 0.25

# typedef enum {
#     layout_unused,
#     layout_type_5,
#     layout_type_2,
#     layout_type_1,
#     layout_type_4,
#     layout_type_3,
#     layout_type_6,
#     layout_type_max
# } layout_type_e;
layout_type_e = c_int
layout_unused = c_int(0)
layout_type_5 = c_int(1)
layout_type_2 = c_int(2)
layout_type_1 = c_int(3)
layout_type_4 = c_int(4)
layout_type_3 = c_int(5)
layout_type_6 = c_int(6)
layout_type_max = c_int(7)

# typedef enum {
#     layout_pane_content_none,
#     layout_pane_content_plist,
#     layout_pane_content_pdetails,
#     layout_pane_content_pbytes
# } layout_pane_content_e;
layout_pane_content_e = c_int
layout_pane_content_none = c_int(0)
layout_pane_content_plist = c_int(1)
layout_pane_content_pdetails = c_int(2)
layout_pane_content_pbytes = c_int(3)

# typedef enum {
#     console_open_never,
#     console_open_auto,
#     console_open_always
# } console_open_e;
console_open_e = c_int
console_open_never = c_int(0)
console_open_auto = c_int(1)
console_open_always = c_int(2)

# typedef enum {
#     version_welcome_only,
#     version_title_only,
#     version_both,
#     version_neither
# } version_info_e;
version_info_e = c_int
version_welcome_only = c_int(0)
version_title_only = c_int(1)
version_both = c_int(2)
version_neither = c_int(3)

# typedef enum {
#     pref_default,
#     pref_stashed,
#     pref_current
# } pref_source_t;
pref_source_t = c_int
pref_default = c_int(0)
pref_stashed = c_int(1)
pref_current = c_int(2)

# typedef enum {
#     ELIDE_LEFT,
#     ELIDE_RIGHT,
#     ELIDE_MIDDLE,
#     ELIDE_NONE
# } elide_mode_e;
elide_mode_e = c_int
ELIDE_LEFT = c_int(0)
ELIDE_RIGHT = c_int(1)
ELIDE_MIDDLE = c_int(2)
ELIDE_NONE = c_int(3)

# typedef enum {
#     UPDATE_CHANNEL_DEVELOPMENT,
#     UPDATE_CHANNEL_STABLE
# } software_update_channel_e;
software_update_channel_e = c_int
UPDATE_CHANNEL_DEVELOPMENT = c_int(0)
UPDATE_CHANNEL_STABLE = c_int(1)

# typedef struct _e_prefs {
#   GList       *col_list;
#   gint         num_cols;
#   color_t      st_client_fg, st_client_bg, st_server_fg, st_server_bg;
#   color_t      gui_text_valid, gui_text_invalid, gui_text_deprecated;
#   gboolean     restore_filter_after_following_stream;
#   gint         gui_toolbar_main_style;
#   gchar       *gui_qt_font_name;
#   color_t      gui_active_fg;
#   color_t      gui_active_bg;
#   gint         gui_active_style;
#   color_t      gui_inactive_fg;
#   color_t      gui_inactive_bg;
#   gint         gui_inactive_style;
#   color_t      gui_marked_fg;
#   color_t      gui_marked_bg;
#   color_t      gui_ignored_fg;
#   color_t      gui_ignored_bg;
#   gchar       *gui_colorized_fg;
#   gchar       *gui_colorized_bg;
#   gboolean     gui_geometry_save_position;
#   gboolean     gui_geometry_save_size;
#   gboolean     gui_geometry_save_maximized;
#   console_open_e gui_console_open;
#   guint        gui_recent_df_entries_max;
#   guint        gui_recent_files_count_max;
#   guint        gui_fileopen_style;
#   gchar       *gui_fileopen_dir;
#   guint        gui_fileopen_preview;
#   gboolean     gui_ask_unsaved;
#   gboolean     gui_autocomplete_filter;
#   gboolean     gui_find_wrap;
#   gchar       *gui_window_title;
#   gchar       *gui_prepend_window_title;
#   gchar       *gui_start_title;
#   version_info_e gui_version_placement;
#   guint        gui_max_export_objects;
#   layout_type_e gui_layout_type;
#   layout_pane_content_e gui_layout_content_1;
#   layout_pane_content_e gui_layout_content_2;
#   layout_pane_content_e gui_layout_content_3;
#   gchar       *gui_interfaces_hide_types;
#   gboolean     gui_interfaces_show_hidden;
#   gboolean     gui_interfaces_remote_display;
#   gint         console_log_level;
#   gchar       *capture_device;
#   gchar       *capture_devices_linktypes;
#   gchar       *capture_devices_descr;
#   gchar       *capture_devices_hide;
#   gchar       *capture_devices_monitor_mode;
#   gchar       *capture_devices_buffersize;
#   gchar       *capture_devices_snaplen;
#   gchar       *capture_devices_pmode;
#   gchar       *capture_devices_filter;
#   gboolean     capture_prom_mode;
#   gboolean     capture_pcap_ng;
#   gboolean     capture_real_time;
#   gboolean     capture_auto_scroll;
#   gboolean     capture_no_interface_load;
#   gboolean     capture_no_extcap;
#   gboolean     capture_show_info;
#   GList       *capture_columns;
#   guint        tap_update_interval;
#   gboolean     display_hidden_proto_items;
#   gboolean     display_byte_fields_with_spaces;
#   gboolean     enable_incomplete_dissectors_check;
#   gboolean     incomplete_dissectors_check_debug;
#   gboolean     strict_conversation_tracking_heuristics;
#   gboolean     filter_expressions_old;
#   gboolean     gui_update_enabled;
#   software_update_channel_e gui_update_channel;
#   gint         gui_update_interval;
#   gchar       *saved_at_version;
#   gboolean     unknown_prefs;
#   gboolean     unknown_colorfilters;
#   gboolean     gui_qt_packet_list_separator;
#   gboolean     gui_qt_packet_header_column_definition;
#   gboolean     gui_qt_show_selected_packet;
#   gboolean     gui_qt_show_file_load_time;
#   gboolean     gui_packet_editor;
#   elide_mode_e gui_packet_list_elide_mode;
#   gboolean     gui_packet_list_show_related;
#   gboolean     gui_packet_list_show_minimap;
#   gboolean     st_enable_burstinfo;
#   gboolean     st_burst_showcount;
#   gint         st_burst_resolution;
#   gint         st_burst_windowlen;
#   gboolean     st_sort_casesensitve;
#   gboolean     st_sort_rng_fixorder;
#   gboolean     st_sort_rng_nameonly;
#   gint         st_sort_defcolflag;
#   gboolean     st_sort_defdescending;
#   gboolean     st_sort_showfullname;
#   gboolean     extcap_save_on_start;
# } e_prefs;


class _e_prefs(Structure):
    _fields_ = [('col_list', POINTER(GList)),
                ('num_cols', gint),
                ('st_client_fg', color_t),
                ('st_client_bg', color_t),
                ('st_server_fg', color_t),
                ('st_server_bg', color_t),
                ('gui_text_valid', color_t),
                ('gui_text_invalid', color_t),
                ('gui_text_deprecated', color_t),
                ('resotre_filter_after_following_stream', gboolean),
                ('gui_toolbar_main_style', gint),
                ('gui_qt_font_name', gchar_p),
                ('gui_active_fg', color_t),
                ('gui_active_bg', color_t),
                ('gui_active_style', gint),
                ('gui_inactive_fg', color_t),
                ('gui_inactive_bg', color_t),
                ('gui_inactive_style', gint),
                ('gui_marked_fg', color_t),
                ('gui_marked_bg', color_t),
                ('gui_ignored_fg', color_t),
                ('gui_ignored_bg', color_t),
                ('gui_colorized_fg', gchar_p),
                ('gui_colorized_bg', gchar_p),
                ('gui_geometry_save_position', gboolean),
                ('gui_geometry_save_size', gboolean),
                ('gui_geometry_save_maximized', gboolean),
                ('gui_console_open', console_open_e),
                ('gui_recent_df_entries_max', guint),
                ('gui_recent_file_count_max', guint),
                ('gui_fileopen_style', guint),
                ('gui_fileopen_dir', gchar_p),
                ('gui_fileopen_preview', guint),
                ('gui_ask_unsaved', gboolean),
                ('gui_autocomplete_filter', gboolean),
                ('gui_find_wrap', gboolean),
                ('gui_window_title', gchar_p),
                ('gui_prepend_window_title', gchar_p),
                ('gui_start_title', gchar_p),
                ('gui_layout_type', version_info_e),
                ('gui_max_export_objects', guint),
                ('gui_layout_type', layout_type_e),
                ('gui_layout_content_1', layout_pane_content_e),
                ('gui_layout_content_2', layout_pane_content_e),
                ('gui_layout_content_3', layout_pane_content_e),
                ('gui_interfaces_hide_types', gchar_p),
                ('gui_interfaces_show_hidden', gboolean),
                ('gui_interfaces_remote_display', gboolean),
                ('console_log_level', gint),
                ('caputre_device', gchar_p),
                ('capture_devices_linktypes', gchar_p),
                ('capture_devices_descr', gchar_p),
                ('capture_devices_hide', gchar_p),
                ('capture_devices_monitor_mode', gchar_p),
                ('capture_devices_buffersize', gchar_p),
                ('capture_devices_snaplen', gchar_p),
                ('capture_devices_pmode', gchar_p),
                ('capture_devices_filter', gchar_p),
                ('capture_prom_mode', gboolean),
                ('capture_pcap_ng', gboolean),
                ('capture_real_time', gboolean),
                ('capture_auto_scroll', gboolean),
                ('capture_no_interface_load', gboolean),
                ('capture_no_extcap', gboolean),
                ('caputre_show_info', gboolean),
                ('capture_columns', POINTER(GList)),
                ('tap_update_interval', guint),
                ('display_hidden_proto_items', gboolean),
                ('display_byte_fields_with_spaces', gboolean),
                ('enable_incomplete_dissectors_check', gboolean),
                ('incomplete_dissectors_check_debug', gboolean),
                ('strict_conversation_tracking_heuristics', gboolean),
                ('filter_expressions_old', gboolean),
                ('gui_update_enabled', gboolean),
                ('gui_update_channel', software_update_channel_e),
                ('gui_update_interval', gint),
                ('saved_at_version', gchar_p),
                ('unknown_prefs', gboolean),
                ('unknown_colorfilters', gboolean),
                ('gui_qt_packet_list_separator', gboolean),
                ('gui_qt_packet_header_column_definition', gboolean),
                ('gui_qt_show_selected_packet', gboolean),
                ('gui_qt_show_file_load_time', gboolean),
                ('gui_packet_editor', gboolean),
                ('gui_packet_list_elide_mode', elide_mode_e),
                ('gui_packet_list_show_related', gboolean),
                ('gui_packet_list_show_minimap', gboolean),
                ('st_enable_burstinfo', gboolean),
                ('st_burst_showcount', gboolean),
                ('st_burst_resolution', gint),
                ('st_burst_windowlen', gint),
                ('st_sort_casesensitve', gboolean),
                ('st_sort_rng_fixorder', gboolean),
                ('st_sort_rng_nameonly', gboolean),
                ('st_sort_defcolflag', gint),
                ('st_sort_defdescending', gboolean),
                ('st_sort_showfullname', gboolean),
                ('extcap_save_on_start', gboolean)]


e_prefs = _e_prefs


# e_prefs prefs;
prefs = e_prefs.in_dll(libwireshark, 'prefs')


# struct pref_module;
class pref_module(Structure):
    _fields_ = []


# struct pref_custom_cbs;
class pref_custom_cbs(Structure):
    _fields_ = []


# typedef struct pref_module module_t;
module_t = pref_module

# void prefs_reset(void);
prefs_reset = libwireshark.prefs_reset
prefs_reset.restype = None
prefs_reset.argtypes = []

# void prefs_set_gui_theme_is_dark(gboolean is_dark);
prefs_set_gui_theme_is_dark = libwireshark.prefs_set_gui_theme_is_dark
prefs_set_gui_theme_is_dark.restype = None
prefs_set_gui_theme_is_dark.argtypes = [gboolean]

# module_t *prefs_register_protocol(int id, void (*apply_cb)(void));
prefs_register_protocol = libwireshark.prefs_register_protocol
prefs_register_protocol.restype = POINTER(module_t)
prefs_register_protocol.argtypes = [c_int, CFUNCTYPE(None)]

# void prefs_register_module_alias(const char *name, module_t *module);
prefs_register_module_alias = libwireshark.prefs_register_module_alias
prefs_register_module_alias.restype = None
prefs_register_module_alias.argtypes = [c_char_p, POINTER(module_t)]

# module_t *prefs_register_stat(const char *name, const char *title,
#     const char *description, void (*apply_cb)(void));
prefs_register_stat = libwireshark.prefs_register_stat
prefs_register_stat.restype = POINTER(module_t)
prefs_register_stat.argtypes = [c_char_p,
                                c_char_p,
                                c_char_p,
                                CFUNCTYPE(None)]

# module_t *prefs_register_codec(const char *name, const char *title,
#     const char *description, void (*apply_cb)(void));
prefs_register_codec = libwireshark.prefs_register_codec
prefs_register_codec.restype = POINTER(module_t)
prefs_register_codec.argtypes = [c_char_p,
                                 c_char_p,
                                 c_char_p,
                                 CFUNCTYPE(None)]

# module_t *prefs_register_protocol_subtree(const char *subtree, int id,
#     void (*apply_cb)(void));
prefs_register_protocol_subtree = libwireshark.prefs_register_protocol_subtree
prefs_register_protocol_subtree.restype = POINTER(module_t)
prefs_register_protocol_subtree.argtypes = [c_char_p, c_int, CFUNCTYPE(None)]

# typedef guint (*module_cb)(module_t *module, gpointer user_data);
module_cb = CFUNCTYPE(guint, POINTER(module_t), gpointer)

# gboolean prefs_module_has_submodules(module_t *module);
prefs_module_has_submodules = libwireshark.prefs_module_has_submodules
prefs_module_has_submodules.restype = gboolean
prefs_module_has_submodules.argtypes = [POINTER(module_t)]

# guint prefs_modules_foreach(module_cb callback, gpointer user_data);
prefs_modules_foreach = libwireshark.prefs_modules_foreach
prefs_modules_foreach.restype = guint
prefs_modules_foreach.argtypes = [module_cb, gpointer]

# guint prefs_modules_foreach_submodules(module_t *module, module_cb
# callback, gpointer user_data);
prefs_modules_foreach_submodules = libwireshark.prefs_modules_foreach_submodules
prefs_modules_foreach_submodules.restype = guint
prefs_modules_foreach_submodules.argtypes = [
    POINTER(module_t), module_cb, gpointer]

# void prefs_apply_all(void);
prefs_apply_all = libwireshark.prefs_apply_all
prefs_apply_all.restype = None
prefs_apply_all.argtypes = []

# void prefs_apply(module_t *module);
prefs_apply = libwireshark.prefs_apply
prefs_apply.restype = None
prefs_apply.argtypes = [POINTER(module_t)]


# struct preference;
class preference(Structure):
    _fields_ = []


# typedef struct preference pref_t;
pref_t = preference

# gboolean prefs_is_registered_protocol(const char *name);
prefs_is_registered_protocol = libwireshark.prefs_is_registered_protocol
prefs_is_registered_protocol.restype = gboolean
prefs_is_registered_protocol.argtypes = [c_char_p]

# const char *prefs_get_title_by_name(const char *name);
prefs_get_title_by_name = libwireshark.prefs_get_title_by_name
prefs_get_title_by_name.restype = c_char_p
prefs_get_title_by_name.argtypes = [c_char_p]

# module_t *prefs_find_module(const char *name);
prefs_find_module = libwireshark.prefs_find_module
prefs_find_module.restype = POINTER(module_t)
prefs_find_module.argtypes = [c_char_p]

# pref_t *prefs_find_preference(module_t * module, const char *pref);
prefs_find_preference = libwireshark.prefs_find_preference
prefs_find_preference.restype = POINTER(pref_t)
prefs_find_preference.argtypes = [POINTER(module_t), c_char_p]

# void prefs_register_uint_preference(module_t *module, const char *name,
#     const char *title, const char *description, guint base, guint *var);
prefs_register_uint_preference = libwireshark.prefs_register_uint_preference
prefs_register_uint_preference.restype = None
prefs_register_uint_preference.argtypes = [POINTER(module_t),
                                           c_char_p,
                                           c_char_p,
                                           c_char_p,
                                           guint,
                                           POINTER(guint)]

# void prefs_register_bool_preference(module_t *module, const char *name,
#     const char *title, const char *description, gboolean *var);
prefs_register_bool_preference = libwireshark.prefs_register_bool_preference
prefs_register_bool_preference.restype = None
prefs_register_bool_preference.argtypes = [POINTER(module_t),
                                           c_char_p,
                                           c_char_p,
                                           c_char_p,
                                           gboolean]

# void prefs_register_enum_preference(module_t *module, const char *name,
#     const char *title, const char *description, gint *var,
#     const enum_val_t *enumvals, gboolean radio_buttons);
prefs_register_enum_preference = libwireshark.prefs_register_enum_preference
prefs_register_enum_preference.restype = None
prefs_register_enum_preference.argtypes = [POINTER(module_t),
                                           c_char_p,
                                           c_char_p,
                                           c_char_p,
                                           POINTER(gint),
                                           POINTER(enum_val_t),
                                           gboolean]

# void prefs_register_string_preference(module_t *module, const char *name,
#     const char *title, const char *description, const char **var);
prefs_register_string_preference = libwireshark.prefs_register_string_preference
prefs_register_string_preference.restype = None
prefs_register_string_preference.argtypes = [POINTER(module_t),
                                             c_char_p,
                                             c_char_p,
                                             c_char_p,
                                             POINTER(c_char_p)]

# void prefs_register_filename_preference(module_t *module, const char *name,
# const char *title, const char *description, const char **var, gboolean
# for_writing);
prefs_register_filename_preference = libwireshark.prefs_register_filename_preference
prefs_register_filename_preference.restype = None
prefs_register_filename_preference.argtypes = [POINTER(module_t),
                                               c_char_p,
                                               c_char_p,
                                               c_char_p,
                                               POINTER(c_char_p),
                                               gboolean]

# void prefs_register_directory_preference(module_t *module, const char *name,
#     const char *title, const char *description, const char **var);
prefs_register_directory_preference = libwireshark.prefs_register_directory_preference
prefs_register_directory_preference.restype = None
prefs_register_directory_preference.argtypes = [POINTER(module_t),
                                                c_char_p,
                                                c_char_p,
                                                c_char_p,
                                                POINTER(c_char_p)]

# void prefs_register_range_preference(module_t *module, const char *name,
#     const char *title, const char *description, range_t **var,
#     guint32 max_value);
prefs_register_range_preference = libwireshark.prefs_register_range_preference
prefs_register_range_preference.restype = None
prefs_register_range_preference.argtypes = [POINTER(module_t),
                                            c_char_p,
                                            c_char_p,
                                            c_char_p,
                                            POINTER(POINTER(range_t)),
                                            guint32]

# void prefs_register_static_text_preference(module_t *module, const char *name,
#     const char *title, const char *description);
prefs_register_static_text_preference = libwireshark.prefs_register_static_text_preference
prefs_register_static_text_preference.restype = None
prefs_register_static_text_preference.argtypes = [POINTER(module_t),
                                                  c_char_p,
                                                  c_char_p,
                                                  c_char_p]

# void prefs_register_uat_preference(module_t *module,
# const char *name, const char* title, const char *description,  struct
# epan_uat* uat);
prefs_register_uat_preference = libwireshark.prefs_register_uat_preference
prefs_register_uat_preference.restype = None
prefs_register_uat_preference.argtypes = [POINTER(module_t),
                                          c_char_p,
                                          c_char_p,
                                          c_char_p,
                                          POINTER(epan_uat)]

# void prefs_register_uat_preference_qt(module_t *module,
# const char *name, const char* title, const char *description,  struct
# epan_uat* uat);
prefs_register_uat_preference_qt = libwireshark.prefs_register_uat_preference_qt
prefs_register_uat_preference_qt.restype = None
prefs_register_uat_preference_qt.argtypes = [POINTER(module_t),
                                             c_char_p,
                                             c_char_p,
                                             c_char_p,
                                             POINTER(epan_uat)]

# void prefs_register_obsolete_preference(module_t *module,
#     const char *name);
prefs_register_obsolete_preference = libwireshark.prefs_register_obsolete_preference
prefs_register_obsolete_preference.restype = None
prefs_register_obsolete_preference.argtypes = [POINTER(module_t), c_char_p]

# typedef guint (*pref_cb)(pref_t *pref, gpointer user_data);
pref_cb = CFUNCTYPE(guint, POINTER(pref_t), gpointer)

# guint prefs_pref_foreach(module_t *module, pref_cb callback,
#     gpointer user_data);
prefs_pref_foreach = libwireshark.prefs_pref_foreach
prefs_pref_foreach.restype = guint
prefs_pref_foreach.argtypes = [POINTER(module_t), pref_cb, gpointer]

# GList *prefs_get_string_list(const gchar *str);
prefs_get_string_list = libwireshark.prefs_get_string_list
prefs_get_string_list.restype = POINTER(GList)
prefs_get_string_list.argtypes = [gchar_p]

# void prefs_clear_string_list(GList *sl);
prefs_clear_string_list = libwireshark.prefs_clear_string_list
prefs_clear_string_list.restype = None
prefs_clear_string_list.argtypes = [POINTER(GList)]

# const char *prefs_pref_type_name(pref_t *pref);
prefs_pref_type_name = libwireshark.prefs_pref_type_name
prefs_pref_type_name.restype = c_char_p
prefs_pref_type_name.argtypes = [POINTER(pref_t)]

# char *prefs_pref_type_description(pref_t *pref);
prefs_pref_type_description = libwireshark.prefs_pref_type_description
prefs_pref_type_description.restype = c_char_p
prefs_pref_type_description.argtypes = [POINTER(pref_t)]

# char *prefs_pref_to_str(pref_t *pref, pref_source_t source);
prefs_pref_to_str = libwireshark.prefs_pref_to_str
prefs_pref_to_str.restype = c_char_p
prefs_pref_to_str.argtypes = [POINTER(pref_t), pref_source_t]

# int write_prefs(char **);
write_prefs = libwireshark.write_prefs
write_prefs.restype = c_int
write_prefs.argtypes = [POINTER(c_char_p)]

# typedef enum {
#     PREFS_SET_OK,
#     PREFS_SET_SYNTAX_ERR,
#     PREFS_SET_NO_SUCH_PREF,
#     PREFS_SET_OBSOLETE
# } prefs_set_pref_e;
prefs_set_pref_e = c_int
PREFS_SET_OK = c_int(0)
PREFS_SET_SYNTAX_ERR = c_int(1)
PREFS_SET_NO_SUCH_PREF = c_int(2)
PREFS_SET_OBSOLETE = c_int(3)

# prefs_set_pref_e prefs_set_pref(char *prefarg, char **errmsg);
prefs_set_pref = libwireshark.prefs_set_pref
prefs_set_pref.restype = prefs_set_pref_e
prefs_set_pref.argtypes = [c_char_p, POINTER(c_char_p)]

# guint prefs_get_uint_value(const char *module_name, const char* pref_name);
prefs_get_uint_value = libwireshark.prefs_get_uint_value
prefs_get_uint_value.restype = guint
prefs_get_uint_value.argtypes = [c_char_p, c_char_p]

# range_t* prefs_get_range_value(const char *module_name, const char*
# pref_name);
prefs_get_range_value = libwireshark.prefs_get_range_value
prefs_get_range_value.restype = POINTER(range_t)
prefs_get_range_value.argtypes = [c_char_p, c_char_p]

# gboolean prefs_is_capture_device_hidden(const char *name);
prefs_is_capture_device_hidden = libwireshark.prefs_is_capture_device_hidden
prefs_is_capture_device_hidden.restype = gboolean
prefs_is_capture_device_hidden.argtypes = [c_char_p]

# gboolean prefs_capture_device_monitor_mode(const char *name);
prefs_capture_device_monitor_mode = libwireshark.prefs_capture_device_monitor_mode
prefs_capture_device_monitor_mode.restype = gboolean
prefs_capture_device_monitor_mode.argtypes = [c_char_p]

# gboolean prefs_capture_options_dialog_column_is_visible(const gchar *column);
prefs_capture_options_dialog_column_is_visible = libwireshark.prefs_capture_options_dialog_column_is_visible
prefs_capture_options_dialog_column_is_visible.restype = gboolean
prefs_capture_options_dialog_column_is_visible.argtypes = [gchar_p]

# gboolean prefs_has_layout_pane_content (layout_pane_content_e
# layout_pane_content);
prefs_has_layout_pane_content = libwireshark.prefs_has_layout_pane_content
prefs_has_layout_pane_content.restype = gboolean
prefs_has_layout_pane_content.argtypes = [layout_pane_content_e]
