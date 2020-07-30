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
