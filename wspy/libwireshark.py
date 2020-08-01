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
