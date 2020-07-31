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
import wspy_config as config

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
