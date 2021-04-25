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
import atexit
from ctypes import *
from wspy.errors import *
from wspy.glib import *
from wspy.c_types import *
import wspy.config as config

libwsutil = CDLL(config.get_libwsutil())
libwiretap = CDLL(config.get_libwiretap())
libwireshark = CDLL(config.get_libwireshark())


# void wtap_rec_init(wtap_rec *rec);
wtap_rec_init = libwiretap.wtap_rec_init
wtap_rec_init.restype = None
wtap_rec_init.argtypes = [POINTER(wtap_rec)]

# void wtap_rec_cleanup(wtap_rec *rec);
wtap_rec_cleanup = libwiretap.wtap_rec_cleanup
wtap_rec_cleanup.restype = None
wtap_rec_cleanup.argtypes = [POINTER(wtap_rec)]

# void ws_buffer_init(Buffer* buffer, gsize space);
ws_buffer_init = libwsutil.ws_buffer_init
ws_buffer_init.restype = None
ws_buffer_init.argtypes = [POINTER(Buffer), gsize]

# void ws_buffer_free(Buffer* buffer);
ws_buffer_free = libwsutil.ws_buffer_free
ws_buffer_free.restype = None
ws_buffer_free.argtypes = [POINTER(Buffer)]

# struct wtap* wtap_open_offline(const char *filename, unsigned int type,
#                                int *err, gchar **err_info, gboolean do_random);
wtap_open_offline = libwiretap.wtap_open_offline
wtap_open_offline.restype = POINTER(wtap)
wtap_open_offline.argtypes = [c_char_p,
                              c_uint,
                              POINTER(c_int),
                              POINTER(gchar_p),
                              gboolean]

# void wtap_set_cb_new_ipv4(wtap *wth, wtap_new_ipv4_callback_t add_new_ipv4);
wtap_set_cb_new_ipv4 = libwiretap.wtap_set_cb_new_ipv4
wtap_set_cb_new_ipv4.restype = None
wtap_set_cb_new_ipv4.argtypes = [POINTER(wtap),
                                 wtap_new_ipv4_callback_t]

# void wtap_set_cb_new_ipv6(wtap *wth, wtap_new_ipv6_callback_t add_new_ipv6);
wtap_set_cb_new_ipv6 = libwiretap.wtap_set_cb_new_ipv6
wtap_set_cb_new_ipv6.restype = None
wtap_set_cb_new_ipv6.argtypes = [POINTER(wtap),
                                 wtap_new_ipv6_callback_t]

# void wtap_set_cb_new_secrets(wtap *wth,
#                              wtap_new_secrets_callback_t add_new_secrets);
wtap_set_cb_new_secrets = libwiretap.wtap_set_cb_new_secrets
wtap_set_cb_new_secrets.restype = None
wtap_set_cb_new_secrets.argtypes = [POINTER(wtap),
                                    wtap_new_secrets_callback_t]

# gboolean wtap_read(wtap *wth, wtap_rec *rec, Buffer *buf, int *err,
#     gchar **err_info, gint64 *offset);
wtap_read = libwiretap.wtap_read
wtap_read.restype = gboolean
wtap_read.argtypes = [POINTER(wtap),
                      POINTER(wtap_rec),
                      POINTER(Buffer),
                      POINTER(c_int),
                      POINTER(gchar_p),
                      POINTER(gint64)]

# gboolean wtap_seek_read(wtap *wth, gint64 seek_off, wtap_rec *rec,
#     Buffer *buf, int *err, gchar **err_info);
wtap_seek_read = libwiretap.wtap_seek_read
wtap_seek_read.restype = gboolean
wtap_seek_read.argtypes = [POINTER(wtap),
                           gint64,
                           POINTER(wtap_rec),
                           POINTER(Buffer),
                           POINTER(c_int),
                           POINTER(gchar_p)]

# void wtap_close(wtap *wth);
wtap_close = libwiretap.wtap_close
wtap_close.restype = None
wtap_close.argtypes = [POINTER(wtap)]

# void init_process_policies(void);
init_process_policies = libwsutil.init_process_policies
init_process_policies.restype = None
init_process_policies.argtypes = []

# void relinquish_special_privs_perm(void);
relinquish_special_privs_perm = libwsutil.relinquish_special_privs_perm
relinquish_special_privs_perm.restype = None
relinquish_special_privs_perm.argtypes = []

# char *init_progfile_dir(const char *arg0);
init_progfile_dir = libwsutil.init_progfile_dir
init_progfile_dir.restype = c_char_p
init_progfile_dir.argtypes = [c_char_p]

if os.name == 'nt':
    # gboolean ws_init_dll_search_path();
    ws_init_dll_search_path = libwsutil.ws_init_dll_search_path
    ws_init_dll_search_path.restype = gboolean
    ws_init_dll_search_path.argtypes = []

# void timestamp_set_type(ts_type);
timestamp_set_type = libwireshark.timestamp_set_type
timestamp_set_type.restype = None
timestamp_set_type.argtypes = [ts_type]

# void timestamp_set_precision(int tsp);
timestamp_set_precision = libwireshark.timestamp_set_precision
timestamp_set_precision.restype = None
timestamp_set_precision.argtypes = [c_int]

# void timestamp_set_seconds_type(ts_seconds_type);
timestamp_set_seconds_type = libwireshark.timestamp_set_seconds_type
timestamp_set_seconds_type.restype = None
timestamp_set_seconds_type.argtypes = [ts_seconds_type]

# void wtap_init(gboolean load_wiretap_plugins);
wtap_init = libwiretap.wtap_init
wtap_init.restype = None
wtap_init.argtypes = [gboolean]

# gboolean epan_init(register_cb cb, void *client_data, gboolean load_plugins);
epan_init = libwireshark.epan_init
epan_init.restype = gboolean
epan_init.argtypes = [register_cb, c_void_p, gboolean]

# e_prefs *epan_load_settings(void);
epan_load_settings = libwireshark.epan_load_settings
epan_load_settings.restype = POINTER(e_prefs)
epan_load_settings.argtypes = []

# void register_all_plugin_tap_listeners(void);
register_all_plugin_tap_listeners = libwireshark.register_all_plugin_tap_listeners
register_all_plugin_tap_listeners.restype = None
register_all_plugin_tap_listeners.argtypes = []

# output_fields_t* output_fields_new(void);
output_fields_new = libwireshark.output_fields_new
output_fields_new.restype = POINTER(output_fields_t)
output_fields_new.argtypes = []

# gboolean color_filters_init(gchar** err_msg, color_filter_add_cb_func add_cb);
color_filters_init = libwireshark.color_filters_init
color_filters_init.restype = gboolean
color_filters_init.argtypes = [POINTER(gchar_p), color_filter_add_cb_func]

# gchar *ws_init_sockets(void);
ws_init_sockets = libwsutil.ws_init_sockets
ws_init_sockets.restype = gchar_p
ws_init_sockets.argtypes = []

# void add_ipv4_name(const guint addr, const gchar *name);
add_ipv4_name = libwireshark.add_ipv4_name
add_ipv4_name.restype = None
add_ipv4_name.argtypes = [guint, gchar_p]

# void add_ipv6_name(const ws_in6_addr *addr, const gchar *name);
add_ipv6_name = libwireshark.add_ipv6_name
add_ipv6_name.restype = None
add_ipv6_name.argtypes = [POINTER(ws_in6_addr), gchar_p]

# void
# secrets_wtap_callback(guint32 secrets_type, const void *secrets, guint size);
secrets_wtap_callback = libwireshark.secrets_wtap_callback
secrets_wtap_callback.restype = None
secrets_wtap_callback.argtypes = [guint32, c_void_p, guint]

# void epan_cleanup(void);
epan_cleanup = libwireshark.epan_cleanup
epan_cleanup.restype = None
epan_cleanup.argtypes = []

# void wtap_cleanup(void);
wtap_cleanup = libwiretap.wtap_cleanup
wtap_cleanup.restype = None
wtap_cleanup.argtypes = []

# void free_progdirs(void);
free_progdirs = libwsutil.free_progdirs
free_progdirs.restype = None
free_progdirs.argtypes = []

# frame_data_sequence *new_frame_data_sequence(void);
new_frame_data_sequence = libwireshark.new_frame_data_sequence
new_frame_data_sequence.restype = POINTER(frame_data_sequence)
new_frame_data_sequence.argtypes = []

# frame_data *frame_data_sequence_find(frame_data_sequence *fds,
#     guint32 num);
frame_data_sequence_find = libwireshark.frame_data_sequence_find
frame_data_sequence_find.restype = POINTER(frame_data)
frame_data_sequence_find.argtypes = [POINTER(frame_data_sequence), guint32]

# void free_frame_data_sequence(frame_data_sequence *fds);
free_frame_data_sequence = libwireshark.free_frame_data_sequence
free_frame_data_sequence.restype = None
free_frame_data_sequence.argtypes = [POINTER(frame_data_sequence)]

# epan_t *epan_new(struct packet_provider_data *prov,
#     const struct packet_provider_funcs *funcs);
epan_new = libwireshark.epan_new
epan_new.restype = POINTER(epan_t)
epan_new.argtypes = [POINTER(packet_provider_data),
                     POINTER(packet_provider_funcs)]

# void nstime_set_zero(nstime_t *nstime);
nstime_set_zero = libwsutil.nstime_set_zero
nstime_set_zero.restype = None
nstime_set_zero.argtypes = [POINTER(nstime_t)]

# int wtap_file_type_subtype(wtap *wth);
wtap_file_type_subtype = libwiretap.wtap_file_type_subtype
wtap_file_type_subtype.restype = c_int
wtap_file_type_subtype.argtypes = [POINTER(wtap)]

# void
# build_column_format_array(column_info *cinfo, const gint num_cols, const gboolean reset_fences);
build_column_format_array = libwireshark.build_column_format_array
build_column_format_array.restype = None
build_column_format_array.argtypes = [POINTER(column_info),
                                      gint,
                                      gboolean]

# e_prefs prefs;
prefs = e_prefs.in_dll(libwireshark, 'prefs')

# epan_dissect_t*
# epan_dissect_new(epan_t *session, const gboolean create_proto_tree, const gboolean proto_tree_visible);
epan_dissect_new = libwireshark.epan_dissect_new
epan_dissect_new.restype = POINTER(epan_dissect_t)
epan_dissect_new.argtypes = [POINTER(epan_t),
                             gboolean,
                             gboolean]

# void frame_data_reset(frame_data *fdata);
frame_data_reset = libwireshark.frame_data_reset
frame_data_reset.restype = None
frame_data_reset.argtypes = [POINTER(frame_data)]

# void frame_data_destroy(frame_data *fdata);
frame_data_destroy = libwireshark.frame_data_destroy
frame_data_destroy.restype = None
frame_data_destroy.argtypes = [POINTER(frame_data)]

# void frame_data_init(frame_data *fdata, guint32 num,
#                 const wtap_rec *rec, gint64 offset,
#                 guint32 cum_bytes);
frame_data_init = libwireshark.frame_data_init
frame_data_init.restype = None
frame_data_init.argtypes = [POINTER(frame_data),
                            guint32,
                            POINTER(wtap_rec),
                            gint64,
                            guint32]

# void frame_data_set_before_dissect(frame_data *fdata,
#                 nstime_t *elapsed_time,
#                 const frame_data **frame_ref,
#                 const frame_data *prev_dis);
frame_data_set_before_dissect = libwireshark.frame_data_set_before_dissect
frame_data_set_before_dissect.restype = None
frame_data_set_before_dissect.argtypes = [POINTER(frame_data),
                                          POINTER(nstime_t),
                                          POINTER(POINTER(frame_data)),
                                          POINTER(frame_data)]

# void frame_data_set_after_dissect(frame_data *fdata,
#                 guint32 *cum_bytes);
frame_data_set_after_dissect = libwireshark.frame_data_set_after_dissect
frame_data_set_after_dissect.restype = None
frame_data_set_after_dissect.argtypes = [POINTER(frame_data),
                                         POINTER(guint32)]

# void
# prime_epan_dissect_with_postdissector_wanted_hfids(epan_dissect_t *edt);
prime_epan_dissect_with_postdissector_wanted_hfids = libwireshark.prime_epan_dissect_with_postdissector_wanted_hfids
prime_epan_dissect_with_postdissector_wanted_hfids.restype = None
prime_epan_dissect_with_postdissector_wanted_hfids.argtypes = [POINTER(epan_dissect_t)]

# void color_filters_prime_edt(struct epan_dissect *edt);
color_filters_prime_edt = libwireshark.color_filters_prime_edt
color_filters_prime_edt.restype = None
color_filters_prime_edt.argtypes = [POINTER(epan_dissect)]

# void
# epan_dissect_free(epan_dissect_t* edt);
epan_dissect_free = libwireshark.epan_dissect_free
epan_dissect_free.restype = None
epan_dissect_free.argtypes = [POINTER(epan_dissect_t)]

# void col_custom_prime_edt(struct epan_dissect *edt, column_info *cinfo);
col_custom_prime_edt = libwireshark.col_custom_prime_edt
col_custom_prime_edt.restype = None
col_custom_prime_edt.argtypes = [POINTER(epan_dissect),
                                 POINTER(column_info)]

# tvbuff_t *tvb_new(const struct tvb_ops *ops);
tvb_new = libwireshark.tvb_new
tvb_new.restype = POINTER(tvbuff_t)
tvb_new.argtypes = [POINTER(tvb_ops)]

# void
# epan_dissect_run(epan_dissect_t *edt, int file_type_subtype,
#         wtap_rec *rec, tvbuff_t *tvb, frame_data *fd,
#         struct epan_column_info *cinfo);
epan_dissect_run = libwireshark.epan_dissect_run
epan_dissect_run.restype = None
epan_dissect_run.argtypes = [POINTER(epan_dissect_t),
                             c_int,
                             POINTER(wtap_rec),
                             POINTER(tvbuff_t),
                             POINTER(frame_data),
                             POINTER(epan_column_info)]

# void
# epan_dissect_run_with_taps(epan_dissect_t *edt, int file_type_subtype,
#         wtap_rec *rec, tvbuff_t *tvb, frame_data *fd,
#         struct epan_column_info *cinfo);
epan_dissect_run_with_taps = libwireshark.epan_dissect_run_with_taps
epan_dissect_run_with_taps.restype = None
epan_dissect_run_with_taps.argtypes = [POINTER(epan_dissect_t),
                                       c_int,
                                       POINTER(wtap_rec),
                                       POINTER(tvbuff_t),
                                       POINTER(frame_data),
                                       POINTER(epan_column_info)]

# wtapng_iface_descriptions_t *wtap_file_get_idb_info(wtap *wth);
wtap_file_get_idb_info = libwiretap.wtap_file_get_idb_info
wtap_file_get_idb_info.restype = POINTER(wtapng_iface_descriptions_t)
wtap_file_get_idb_info.argtypes = [POINTER(wtap)]

# wtap_opttype_return_val
# wtap_block_get_string_option_value(wtap_block_t block, guint option_id,
#                                    char** value);
wtap_block_get_string_option_value = libwiretap.wtap_block_get_string_option_value
wtap_block_get_string_option_value.restype = wtap_opttype_return_val
wtap_block_get_string_option_value.argtypes = [wtap_block_t,
                                               guint,
                                               POINTER(c_char_p)]

# void prefs_apply_all(void);
prefs_apply_all = libwireshark.prefs_apply_all
prefs_apply_all.restype = None
prefs_apply_all.argtypes = []

# void
# epan_dissect_fill_in_columns(epan_dissect_t *edt, const gboolean fill_col_exprs, const gboolean fill_fd_colums);
epan_dissect_fill_in_columns = libwireshark.epan_dissect_fill_in_columns
epan_dissect_fill_in_columns.restype = None
epan_dissect_fill_in_columns.argtypes = [POINTER(epan_dissect_t),
                                         gboolean,
                                         gboolean]

# void epan_free(epan_t *session);
epan_free = libwireshark.epan_free
epan_free.restype = None
epan_free.argtypes = [POINTER(epan_t)]

# ftenum_t
# fvalue_type_ftenum(fvalue_t *fv);
fvalue_type_ftenum = libwireshark.fvalue_type_ftenum
fvalue_type_ftenum.restype = ftenum_t
fvalue_type_ftenum.argtypes = [POINTER(fvalue_t)]

# char *
# fvalue_to_string_repr(wmem_allocator_t *scope, fvalue_t *fv, ftrepr_t rtype, int field_display);
fvalue_to_string_repr = libwireshark.fvalue_to_string_repr
fvalue_to_string_repr.restype = c_void_p
fvalue_to_string_repr.argtyeps = [POINTER(wmem_allocator_t),
                                  POINTER(fvalue_t),
                                  ftrepr_t,
                                  c_int]

# gpointer
# fvalue_get(fvalue_t *fv);
fvalue_get = libwireshark.fvalue_get
fvalue_get.restype = gpointer
fvalue_get.argtypes = [POINTER(fvalue_t)]

# guint32
# fvalue_get_uinteger(fvalue_t *fv);
fvalue_get_uinteger = libwireshark.fvalue_get_uinteger
fvalue_get_uinteger.restype = guint32
fvalue_get_uinteger.argtypes = [POINTER(fvalue_t)]

# gint32
# fvalue_get_sinteger(fvalue_t *fv);
fvalue_get_sinteger = libwireshark.fvalue_get_sinteger
fvalue_get_sinteger.restype = gint32
fvalue_get_sinteger.argtypes = [POINTER(fvalue_t)]

# guint64
# fvalue_get_uinteger64(fvalue_t *fv);
fvalue_get_uinteger64 = libwireshark.fvalue_get_uinteger64
fvalue_get_uinteger64.restype = guint64
fvalue_get_uinteger64.argtypes = [POINTER(fvalue_t)]

# gint64
# fvalue_get_sinteger64(fvalue_t *fv);
fvalue_get_sinteger64 = libwireshark.fvalue_get_sinteger64
fvalue_get_sinteger64.restype = gint64
fvalue_get_sinteger64.argtypes = [POINTER(fvalue_t)]

# double
# fvalue_get_floating(fvalue_t *fv);
fvalue_get_floating = libwireshark.fvalue_get_floating
fvalue_get_floating.restype = c_double
fvalue_get_floating.argtypes = [POINTER(fvalue_t)]

# guint tvb_captured_length(const tvbuff_t *tvb);
tvb_captured_length = libwireshark.tvb_captured_length
tvb_captured_length.restype = guint
tvb_captured_length.argtypes = [POINTER(tvbuff_t)]

# guint tvb_reported_length(const tvbuff_t *tvb);
tvb_reported_length = libwireshark.tvb_reported_length
tvb_reported_length.restype = guint
tvb_reported_length.argtypes = [POINTER(tvbuff_t)]

# gboolean tvb_bytes_exist(const tvbuff_t *tvb, const gint offset,
#     const gint length);
tvb_bytes_exist = libwireshark.tvb_bytes_exist
tvb_bytes_exist.restype = gboolean
tvb_bytes_exist.argtypes = [POINTER(tvbuff_t), gint, gint]

# const guint8 *tvb_get_ptr(tvbuff_t *tvb, const gint offset,
#     const gint length);
tvb_get_ptr = libwireshark.tvb_get_ptr
tvb_get_ptr.restype = POINTER(guint8)
tvb_get_ptr.argtypes = [POINTER(tvbuff_t), gint, gint]

# gint tvb_raw_offset(tvbuff_t *tvb);
tvb_raw_offset = libwireshark.tvb_raw_offset
tvb_raw_offset.restype = gint
tvb_raw_offset.argtypes = [POINTER(tvbuff_t)]

# struct tvbuff *tvb_get_ds_tvb(tvbuff_t *tvb);
tvb_get_ds_tvb = libwireshark.tvb_get_ds_tvb
tvb_get_ds_tvb.restype = POINTER(tvbuff)
tvb_get_ds_tvb.argtypes = [POINTER(tvbuff_t)]

# void tap_register_plugin(const tap_plugin *plug);
tap_register_plugin = libwireshark.tap_register_plugin
tap_register_plugin.restype = None
tap_register_plugin.argtypes = [POINTER(tap_plugin)]

# int register_tap(const char *name);
register_tap = libwireshark.register_tap
register_tap.restype = c_int
register_tap.argtypes = [c_char_p]

# GList* get_tap_names(void);
get_tap_names = libwireshark.get_tap_names
get_tap_names.restype = POINTER(GList)
get_tap_names.argtypes = []

# int find_tap_id(const char *name);
find_tap_id = libwireshark.find_tap_id
find_tap_id.restype = c_int
find_tap_id.argtypes = [c_char_p]

# void tap_queue_packet(int tap_id, packet_info *pinfo, const void *tap_specific_data);
tap_queue_packet = libwireshark.tap_queue_packet
tap_queue_packet.restype = None
tap_queue_packet.argtypes = [c_int, POINTER(packet_info), c_void_p]

# void tap_build_interesting(epan_dissect_t *edt);
tap_build_interesting = libwireshark.tap_build_interesting
tap_build_interesting.restype = None
tap_build_interesting.argtypes = [POINTER(epan_dissect_t)]

# void reset_tap_listeners(void);
reset_tap_listeners = libwireshark.reset_tap_listeners
reset_tap_listeners.restype = None
reset_tap_listeners.argtypes = []

# void draw_tap_listeners(gboolean draw_all);
draw_tap_listeners = libwireshark.draw_tap_listeners
draw_tap_listeners.restype = None
draw_tap_listeners.argtypes = [gboolean]

# GString *register_tap_listener(const char *tapname, void *tapdata,
#     const char *fstring, guint flags, tap_reset_cb tap_reset,
#     tap_packet_cb tap_packet, tap_draw_cb tap_draw,
#     tap_finish_cb tap_finish);
register_tap_listener = libwireshark.register_tap_listener
register_tap_listener.restype = POINTER(GString)
register_tap_listener.argtypes = [c_char_p,
                                       c_void_p,
                                       c_char_p,
                                       guint,
                                       tap_reset_cb,
                                       tap_packet_cb,
                                       tap_draw_cb,
                                       tap_finish_cb]

# GString *set_tap_dfilter(void *tapdata, const char *fstring);
set_tap_dfilter = libwireshark.set_tap_dfilter
set_tap_dfilter.restype = POINTER(GString)
set_tap_dfilter.argtypes = [c_void_p, c_char_p]

# void tap_listeners_dfilter_recompile(void);
tap_listeners_dfilter_recompile = libwireshark.tap_listeners_dfilter_recompile
tap_listeners_dfilter_recompile.restype = None
tap_listeners_dfilter_recompile.argtypes = []

# void remove_tap_listener(void *tapdata);
remove_tap_listener = libwireshark.remove_tap_listener
remove_tap_listener.restype = None
remove_tap_listener.argtypes = [c_void_p]

# gboolean tap_listeners_require_dissection(void);
tap_listeners_require_dissection = libwireshark.tap_listeners_require_dissection
tap_listeners_require_dissection.restype = gboolean
tap_listeners_require_dissection.argtypes = []

# gboolean have_tap_listener(int tap_id);
have_tap_listener = libwireshark.have_tap_listener
have_tap_listener.restype = gboolean
have_tap_listener.argtypes = [c_int]

# gboolean have_filtering_tap_listeners(void);
have_filtering_tap_listeners = libwireshark.have_filtering_tap_listeners
have_filtering_tap_listeners.restype = gboolean
have_filtering_tap_listeners.argtypes = []

# guint union_of_tap_listener_flags(void);
union_of_tap_listener_flags = libwireshark.union_of_tap_listener_flags
union_of_tap_listener_flags.restype = guint
union_of_tap_listener_flags.argtypes = []

# const void *fetch_tapped_data(int tap_id, int idx);
fetch_tapped_data = libwireshark.fetch_tapped_data
fetch_tapped_data.restype = c_void_p
fetch_tapped_data.argtypes = [c_int, c_int]

# void register_follow_stream(const int proto_id, const char* tap_listener,
#                             follow_conv_filter_func conv_filter, follow_index_filter_func index_filter, follow_address_filter_func address_filter,
#                             follow_port_to_display_func port_to_display, tap_packet_cb tap_handler);
register_follow_stream = libwireshark.register_follow_stream
register_follow_stream.restype = None
register_follow_stream.argtypes = [c_int,
                                        c_char_p,
                                        follow_conv_filter_func,
                                        follow_index_filter_func,
                                        follow_address_filter_func,
                                        follow_port_to_display_func,
                                        tap_packet_cb]

# int get_follow_proto_id(register_follow_t* follower);
get_follow_proto_id = libwireshark.get_follow_proto_id
get_follow_proto_id.restype = c_int
get_follow_proto_id.argtypes = [POINTER(register_follow_t)]

# const char* get_follow_tap_string(register_follow_t* follower);
get_follow_tap_string = libwireshark.get_follow_tap_string
get_follow_tap_string.restype = c_char_p
get_follow_tap_string.argtypes = [POINTER(register_follow_t)]

# register_follow_t* get_follow_by_name(const char* proto_short_name);
get_follow_by_name = libwireshark.get_follow_by_name
get_follow_by_name.restype = POINTER(register_follow_t)
get_follow_by_name.argtypes = [c_char_p]

# follow_conv_filter_func get_follow_conv_func(register_follow_t* follower);
get_follow_conv_func = libwireshark.get_follow_conv_func
get_follow_conv_func.restype = follow_conv_filter_func
get_follow_conv_func.argtypes = [POINTER(register_follow_t)]

# follow_index_filter_func get_follow_index_func(register_follow_t* follower);
get_follow_index_func = libwireshark.get_follow_index_func
get_follow_index_func.restype = follow_index_filter_func
get_follow_index_func.argtypes = [POINTER(register_follow_t)]

# follow_address_filter_func get_follow_address_func(register_follow_t* follower);
get_follow_address_func = libwireshark.get_follow_address_func
get_follow_address_func.restype = follow_address_filter_func
get_follow_address_func.argtypes = [POINTER(register_follow_t)]

# follow_port_to_display_func get_follow_port_to_display(register_follow_t* follower);
get_follow_port_to_display = libwireshark.get_follow_port_to_display
get_follow_port_to_display.restype = follow_port_to_display_func
get_follow_port_to_display.argtypes = [POINTER(register_follow_t)]

# tap_packet_cb get_follow_tap_handler(register_follow_t* follower);
get_follow_tap_handler = libwireshark.get_follow_tap_handler
get_follow_tap_handler.restype = tap_packet_cb
get_follow_tap_handler.argtypes = [POINTER(register_follow_t)]

# tap_packet_status
# follow_tvb_tap_listener(void *tapdata, packet_info *pinfo, epan_dissect_t *edt _U_, const void *data);
follow_tvb_tap_listener = libwireshark.follow_tvb_tap_listener
follow_tvb_tap_listener.restype = tap_packet_status
follow_tvb_tap_listener.argtypes = [c_void_p,
                                         POINTER(packet_info),
                                         POINTER(epan_dissect_t),
                                         c_void_p]

# void follow_iterate_followers(wmem_foreach_func func, gpointer user_data);
follow_iterate_followers = libwireshark.follow_iterate_followers
follow_iterate_followers.restype = None
follow_iterate_followers.argtypes = [wmem_foreach_func, gpointer]

# gchar* follow_get_stat_tap_string(register_follow_t* follower);
follow_get_stat_tap_string = libwireshark.follow_get_stat_tap_string
follow_get_stat_tap_string.restype = gchar_p
follow_get_stat_tap_string.argtypes = [POINTER(register_follow_t)]

# void follow_reset_stream(follow_info_t* info);
follow_reset_stream = libwireshark.follow_reset_stream
follow_reset_stream.restype = None
follow_reset_stream.argtypes = [POINTER(follow_info_t)]

# void follow_info_free(follow_info_t* follow_info);
follow_info_free = libwireshark.follow_info_free
follow_info_free.restype = None
follow_info_free.argtypes = [POINTER(follow_info_t)]

# const char* proto_registrar_get_name(const int n);
proto_registrar_get_name = libwireshark.proto_registrar_get_name
proto_registrar_get_name.restype = c_char_p
proto_registrar_get_name.argtypes = [c_int]

# const char* proto_registrar_get_abbrev(const int n);
proto_registrar_get_abbrev = libwireshark.proto_registrar_get_abbrev
proto_registrar_get_abbrev.restype = c_char_p
proto_registrar_get_abbrev.argtypes = [c_int]

# header_field_info* proto_registrar_get_nth(guint hfindex);
proto_registrar_get_nth = libwireshark.proto_registrar_get_nth
proto_registrar_get_nth.restype = POINTER(header_field_info)
proto_registrar_get_nth.argtypes = [guint]

# header_field_info* proto_registrar_get_byname(const char *field_name);
proto_registrar_get_byname = libwireshark.proto_registrar_get_byname
proto_registrar_get_byname.restype = POINTER(header_field_info)
proto_registrar_get_byname.argtypes = [c_char_p]

# header_field_info* proto_registrar_get_byalias(const char *alias_name);
proto_registrar_get_byalias = libwireshark.proto_registrar_get_byalias
proto_registrar_get_byalias.restype = POINTER(header_field_info)
proto_registrar_get_byalias.argtypes = [c_char_p]

# int proto_registrar_get_id_byname(const char *field_name);
proto_registrar_get_id_byname = libwireshark.proto_registrar_get_id_byname
proto_registrar_get_id_byname.restype = c_int
proto_registrar_get_id_byname.argtypes = [c_char_p]

# enum ftenum proto_registrar_get_ftype(const int n);
proto_registrar_get_ftype = libwireshark.proto_registrar_get_ftype
proto_registrar_get_ftype.restype = ftenum
proto_registrar_get_ftype.argtypes = [c_int]

# int proto_registrar_get_parent(const int n);
proto_registrar_get_parent = libwireshark.proto_registrar_get_parent
proto_registrar_get_parent.restype = c_int
proto_registrar_get_parent.argtypes = [c_int]

# gboolean proto_registrar_is_protocol(const int n);
proto_registrar_is_protocol = libwireshark.proto_registrar_is_protocol
proto_registrar_is_protocol.restype = gboolean
proto_registrar_is_protocol.argtypes = [c_int]

# int proto_get_first_protocol(void **cookie);
proto_get_first_protocol = libwireshark.proto_get_first_protocol
proto_get_first_protocol.restype = c_int
proto_get_first_protocol.argtypes = [POINTER(c_void_p)]

# int proto_get_data_protocol(void *cookie);
proto_get_data_protocol = libwireshark.proto_get_data_protocol
proto_get_data_protocol.restype = c_int
proto_get_data_protocol.argtypes = [c_void_p]

# int proto_get_next_protocol(void **cookie);
proto_get_next_protocol = libwireshark.proto_get_next_protocol
proto_get_next_protocol.restype = c_int
proto_get_next_protocol.argtypes = [POINTER(c_void_p)]

# header_field_info *proto_get_first_protocol_field(const int proto_id, void **cookie);
proto_get_first_protocol_field = libwireshark.proto_get_first_protocol_field
proto_get_first_protocol_field.restype = POINTER(header_field_info)
proto_get_first_protocol_field.argtypes = [c_int, POINTER(c_void_p)]

# header_field_info *proto_get_next_protocol_field(const int proto_id, void **cookie);
proto_get_next_protocol_field = libwireshark.proto_get_next_protocol_field
proto_get_next_protocol_field.restype = POINTER(header_field_info)
proto_get_next_protocol_field.argtypes = [c_int, POINTER(c_void_p)]

# int proto_name_already_registered(const gchar *name);
proto_name_already_registered = libwireshark.proto_name_already_registered
proto_name_already_registered.restype = c_int
proto_name_already_registered.argtypes = [gchar_p]

# int proto_get_id_by_filter_name(const gchar* filter_name);
proto_get_id_by_filter_name = libwireshark.proto_get_id_by_filter_name
proto_get_id_by_filter_name.restype = c_int
proto_get_id_by_filter_name.argtypes = [gchar_p]

# int proto_get_id_by_short_name(const gchar* short_name);
proto_get_id_by_short_name = libwireshark.proto_get_id_by_short_name
proto_get_id_by_short_name.restype = c_int
proto_get_id_by_short_name.argtypes = [gchar_p]

# gboolean proto_can_toggle_protocol(const int proto_id);
proto_can_toggle_protocol = libwireshark.proto_can_toggle_protocol
proto_can_toggle_protocol.restype = gboolean
proto_can_toggle_protocol.argtypes = [c_int]

# protocol_t *find_protocol_by_id(const int proto_id);
find_protocol_by_id = libwireshark.find_protocol_by_id
find_protocol_by_id.restype = POINTER(protocol_t)
find_protocol_by_id.argtypes = [c_int]

# const char *proto_get_protocol_name(const int proto_id);
proto_get_protocol_name = libwireshark.proto_get_protocol_name
proto_get_protocol_name.restype = c_char_p
proto_get_protocol_name.argtypes = [c_int]

# int proto_get_id(const protocol_t *protocol);
proto_get_id = libwireshark.proto_get_id
proto_get_id.restype = c_int
proto_get_id.argtypes = [POINTER(protocol_t)]

# const char *proto_get_protocol_short_name(const protocol_t *protocol);
proto_get_protocol_short_name = libwireshark.proto_get_protocol_short_name
proto_get_protocol_short_name.restype = c_char_p
proto_get_protocol_short_name.argtypes = [POINTER(protocol_t)]

# const char *proto_get_protocol_long_name(const protocol_t *protocol);
proto_get_protocol_long_name = libwireshark.proto_get_protocol_long_name
proto_get_protocol_long_name.restype = c_char_p
proto_get_protocol_long_name.argtypes = [POINTER(protocol_t)]

# gboolean proto_is_protocol_enabled(const protocol_t *protocol);
proto_is_protocol_enabled = libwireshark.proto_is_protocol_enabled
proto_is_protocol_enabled.restype = gboolean
proto_is_protocol_enabled.argtypes = [POINTER(protocol_t)]

# gboolean proto_is_protocol_enabled_by_default(const protocol_t *protocol);
proto_is_protocol_enabled_by_default = libwireshark.proto_is_protocol_enabled_by_default
proto_is_protocol_enabled_by_default.restype = gboolean
proto_is_protocol_enabled_by_default.argtypes = [POINTER(protocol_t)]

# const char *proto_get_protocol_filter_name(const int proto_id);
proto_get_protocol_filter_name = libwireshark.proto_get_protocol_filter_name
proto_get_protocol_filter_name.restype = c_char_p
proto_get_protocol_filter_name.argtypes = [c_int]

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
prefs_register_protocol_subtree.argtypes = [c_char_p,
                                                 c_int,
                                                 CFUNCTYPE(None)]

# gboolean prefs_module_has_submodules(module_t *module);
prefs_module_has_submodules = libwireshark.prefs_module_has_submodules
prefs_module_has_submodules.restype = gboolean
prefs_module_has_submodules.argtypes = [POINTER(module_t)]

# guint prefs_modules_foreach(module_cb callback, gpointer user_data);
prefs_modules_foreach = libwireshark.prefs_modules_foreach
prefs_modules_foreach.restype = guint
prefs_modules_foreach.argtypes = [module_cb, gpointer]

# guint prefs_modules_foreach_submodules(module_t *module, module_cb callback, gpointer user_data);
prefs_modules_foreach_submodules = libwireshark.prefs_modules_foreach_submodules
prefs_modules_foreach_submodules.restype = guint
prefs_modules_foreach_submodules.argtypes = [POINTER(module_t),
                                                  module_cb,
                                                  gpointer]

# void prefs_apply_all(void);
prefs_apply_all = libwireshark.prefs_apply_all
prefs_apply_all.restype = None
prefs_apply_all.argtypes = []

# void prefs_apply(module_t *module);
prefs_apply = libwireshark.prefs_apply
prefs_apply.restype = None
prefs_apply.argtypes = [POINTER(module_t)]

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
                                                POINTER(gboolean)]

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
#     const char *title, const char *description, const char **var, gboolean for_writing);
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
#     const char *name, const char* title, const char *description,  struct epan_uat* uat);
prefs_register_uat_preference = libwireshark.prefs_register_uat_preference
prefs_register_uat_preference.restype = None
prefs_register_uat_preference.argtypes = [POINTER(module_t),
                                               c_char_p,
                                               c_char_p,
                                               c_char_p,
                                               POINTER(epan_uat)]

# void prefs_register_uat_preference_qt(module_t *module,
#     const char *name, const char* title, const char *description,  struct epan_uat* uat);
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
prefs_register_obsolete_preference.argtypes = [POINTER(module_t),
                                                    c_char_p]

# void prefs_set_preference_effect_fields(module_t *module,
#     const char *name);
prefs_set_preference_effect_fields = libwireshark.prefs_set_preference_effect_fields
prefs_set_preference_effect_fields.restype = None
prefs_set_preference_effect_fields.argtypes = [POINTER(module_t), c_char_p]

# typedef guint (*pref_cb)(pref_t *pref, gpointer user_data);
pref_cb = CFUNCTYPE(guint, POINTER(pref_t), gpointer)
pref_cb = pref_cb

# guint prefs_pref_foreach(module_t *module, pref_cb callback,
#     gpointer user_data);
prefs_pref_foreach = libwireshark.prefs_pref_foreach
prefs_pref_foreach.restype = guint
prefs_pref_foreach.argtypes = [POINTER(module_t),
                                    pref_cb,
                                    gpointer]

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

# prefs_set_pref_e prefs_set_pref(char *prefarg, char **errmsg);
prefs_set_pref = libwireshark.prefs_set_pref
prefs_set_pref.restype = prefs_set_pref_e
prefs_set_pref.argtypes = [c_char_p, POINTER(c_char_p)]

# guint prefs_get_uint_value(const char *module_name, const char* pref_name);
prefs_get_uint_value = libwireshark.prefs_get_uint_value
prefs_get_uint_value.restype = guint
prefs_get_uint_value.argtypes = [c_char_p, c_char_p]

# range_t* prefs_get_range_value(const char *module_name, const char* pref_name);
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

# gboolean prefs_has_layout_pane_content (layout_pane_content_e layout_pane_content);
prefs_has_layout_pane_content = libwireshark.prefs_has_layout_pane_content
prefs_has_layout_pane_content.restype = gboolean
prefs_has_layout_pane_content.argtypes = [layout_pane_content_e]

# module_t *protocols_module;
protocols_module = POINTER(module_t).in_dll(libwireshark, 'protocols_module')

# const char* prefs_get_description(pref_t *pref);
prefs_get_description = libwireshark.prefs_get_description
prefs_get_description.restype = c_char_p
prefs_get_description.argtypes = [POINTER(pref_t)]

# const char* prefs_get_title(pref_t *pref);
prefs_get_title = libwireshark.prefs_get_title
prefs_get_title.restype = c_char_p
prefs_get_title.argtypes = [POINTER(pref_t)]

# const char* prefs_get_name(pref_t *pref);
prefs_get_name = libwireshark.prefs_get_name
prefs_get_name.restype = c_char_p
prefs_get_name.argtypes = [POINTER(pref_t)]

# int prefs_get_type(pref_t *pref);
prefs_get_type = libwireshark.prefs_get_type
prefs_get_type.restype = c_int
prefs_get_type.argtypes = [POINTER(pref_t)]

# gui_type_t prefs_get_gui_type(pref_t *pref);
prefs_get_gui_type = libwireshark.prefs_get_gui_type
prefs_get_gui_type.restype = gui_type_t
prefs_get_gui_type.argtypes = [POINTER(pref_t)]

# guint32 prefs_get_max_value(pref_t *pref);
prefs_get_max_value = libwireshark.prefs_get_max_value
prefs_get_max_value.restype = guint32
prefs_get_max_value.argtypes = [POINTER(pref_t)]

# unsigned int prefs_get_effect_flags(pref_t *pref);
prefs_get_effect_flags = libwireshark.prefs_get_effect_flags
prefs_get_effect_flags.restype = c_uint
prefs_get_effect_flags.argtypes = [POINTER(pref_t)]

# void prefs_set_effect_flags(pref_t *pref, unsigned int flags);
prefs_set_effect_flags = libwireshark.prefs_set_effect_flags
prefs_set_effect_flags.restype = None
prefs_set_effect_flags.argtypes = [POINTER(pref_t), c_uint]

# void prefs_set_effect_flags_by_name(module_t * module, const char *pref, unsigned int flags);
prefs_set_effect_flags_by_name = libwireshark.prefs_set_effect_flags_by_name
prefs_set_effect_flags_by_name.restype = None
prefs_set_effect_flags_by_name.argtypes = [POINTER(module_t),
                                                c_char_p,
                                                c_uint]

# unsigned int prefs_get_module_effect_flags(module_t * module);
prefs_get_module_effect_flags = libwireshark.prefs_get_module_effect_flags
prefs_get_module_effect_flags.restype = c_uint
prefs_get_module_effect_flags.argtypes = [POINTER(module_t)]

# void prefs_set_module_effect_flags(module_t * module, unsigned int flags);
prefs_set_module_effect_flags = libwireshark.prefs_set_module_effect_flags
prefs_set_module_effect_flags.restype = None
prefs_set_module_effect_flags.argtypes = [POINTER(module_t), c_uint]

# gboolean prefs_set_range_value_work(pref_t *pref, const gchar *value,
#                            gboolean return_range_errors, unsigned int *changed_flags);
prefs_set_range_value_work = libwireshark.prefs_set_range_value_work
prefs_set_range_value_work.restype = gboolean
prefs_set_range_value_work.argtypes = [POINTER(pref_t),
                                            gchar_p,
                                            gboolean,
                                            POINTER(c_uint)]

# unsigned int
# prefs_set_stashed_range_value(pref_t *pref, const gchar *value);
prefs_set_stashed_range_value = libwireshark.prefs_set_stashed_range_value
prefs_set_stashed_range_value.restype = c_uint
prefs_set_stashed_range_value.argtypes = [POINTER(pref_t), gchar_p]

# void
# prefs_range_add_value(pref_t *pref, guint32 val);
prefs_range_add_value = libwireshark.prefs_range_add_value
prefs_range_add_value.restype = None
prefs_range_add_value.argtypes = [POINTER(pref_t), guint32]

# void
# prefs_range_remove_value(pref_t *pref, guint32 val);
prefs_range_remove_value = libwireshark.prefs_range_remove_value
prefs_range_remove_value.restype = None
prefs_range_remove_value.argtypes = [POINTER(pref_t), guint32]

# unsigned int prefs_set_bool_value(pref_t *pref, gboolean value, pref_source_t source);
prefs_set_bool_value = libwireshark.prefs_set_bool_value
prefs_set_bool_value.restype = c_uint
prefs_set_bool_value.argtypes = [POINTER(pref_t),
                                      gboolean,
                                      pref_source_t]

# gboolean prefs_get_bool_value(pref_t *pref, pref_source_t source);
prefs_get_bool_value = libwireshark.prefs_get_bool_value
prefs_get_bool_value.restype = gboolean
prefs_get_bool_value.argtypes = [POINTER(pref_t), pref_source_t]

# void prefs_invert_bool_value(pref_t *pref, pref_source_t source);
prefs_invert_bool_value = libwireshark.prefs_invert_bool_value
prefs_invert_bool_value.restype = None
prefs_invert_bool_value.argtypes = [POINTER(pref_t), pref_source_t]

# unsigned int prefs_set_uint_value(pref_t *pref, guint value, pref_source_t source);
prefs_set_uint_value = libwireshark.prefs_set_uint_value
prefs_set_uint_value.restype = c_uint
prefs_set_uint_value.argtypes = [POINTER(pref_t), guint, pref_source_t]

# guint prefs_get_uint_base(pref_t *pref);
prefs_get_uint_base = libwireshark.prefs_get_uint_base
prefs_get_uint_base.restype = guint
prefs_get_uint_base.argtypes = [POINTER(pref_t)]

# guint prefs_get_uint_value_real(pref_t *pref, pref_source_t source);
prefs_get_uint_value_real = libwireshark.prefs_get_uint_value_real
prefs_get_uint_value_real.restype = guint
prefs_get_uint_value_real.argtypes = [POINTER(pref_t), pref_source_t]

# unsigned int prefs_set_enum_value(pref_t *pref, gint value, pref_source_t source);
prefs_set_enum_value = libwireshark.prefs_set_enum_value
prefs_set_enum_value.restype = c_uint
prefs_set_enum_value.argtypes = [POINTER(pref_t), gint, pref_source_t]

# gint prefs_get_enum_value(pref_t *pref, pref_source_t source);
prefs_get_enum_value = libwireshark.prefs_get_enum_value
prefs_get_enum_value.restype = gint
prefs_get_enum_value.argtypes = [POINTER(pref_t), pref_source_t]

# const enum_val_t* prefs_get_enumvals(pref_t *pref);
prefs_get_enumvals = libwireshark.prefs_get_enumvals
prefs_get_enumvals.restype = POINTER(enum_val_t)
prefs_get_enumvals.argtypes = [POINTER(pref_t)]

# gboolean prefs_get_enum_radiobuttons(pref_t *pref);
prefs_get_enum_radiobuttons = libwireshark.prefs_get_enum_radiobuttons
prefs_get_enum_radiobuttons.restype = gboolean
prefs_get_enum_radiobuttons.argtypes = [POINTER(pref_t)]

# gboolean prefs_set_color_value(pref_t *pref, color_t value, pref_source_t source);
prefs_set_color_value = libwireshark.prefs_set_color_value
prefs_set_color_value.restype = gboolean
prefs_set_color_value.argtypes = [POINTER(pref_t), color_t, pref_source_t]

# color_t* prefs_get_color_value(pref_t *pref, pref_source_t source);
prefs_get_color_value = libwireshark.prefs_get_color_value
prefs_get_color_value.restype = POINTER(color_t)
prefs_get_color_value.argtypes = [POINTER(pref_t), pref_source_t]

# unsigned int prefs_set_custom_value(pref_t *pref, const char *value, pref_source_t source);
prefs_set_custom_value = libwireshark.prefs_set_custom_value
prefs_set_custom_value.restype = c_uint
prefs_set_custom_value.argtypes = [POINTER(pref_t), c_char_p, pref_source_t]

# unsigned int prefs_set_string_value(pref_t *pref, const char* value, pref_source_t source);
prefs_set_string_value = libwireshark.prefs_set_string_value
prefs_set_string_value.restype = c_uint
prefs_set_string_value.argtypes = [POINTER(pref_t), c_char_p, pref_source_t]

# char* prefs_get_string_value(pref_t *pref, pref_source_t source);
prefs_get_string_value = libwireshark.prefs_get_string_value
prefs_get_string_value.restype = c_char_p
prefs_get_string_value.argtypes = [POINTER(pref_t), pref_source_t]

# struct epan_uat* prefs_get_uat_value(pref_t *pref);
prefs_get_uat_value = libwireshark.prefs_get_uat_value
prefs_get_uat_value.restype = POINTER(epan_uat)
prefs_get_uat_value.argtypes = [POINTER(pref_t)]

# gboolean prefs_set_range_value(pref_t *pref, range_t *value, pref_source_t source);
prefs_set_range_value = libwireshark.prefs_set_range_value
prefs_set_range_value.restype = gboolean
prefs_set_range_value.argtypes = [POINTER(pref_t),
                                       POINTER(range_t),
                                       pref_source_t]

# range_t* prefs_get_range_value_real(pref_t *pref, pref_source_t source);
prefs_get_range_value_real = libwireshark.prefs_get_range_value_real
prefs_get_range_value_real.restype = POINTER(range_t)
prefs_get_range_value_real.argtypes = [POINTER(pref_t), pref_source_t]

# gboolean prefs_add_decode_as_value(pref_t *pref, guint value, gboolean replace);
prefs_add_decode_as_value = libwireshark.prefs_add_decode_as_value
prefs_add_decode_as_value.restype = gboolean
prefs_add_decode_as_value.argtypes = [POINTER(pref_t), guint, gboolean]

# gboolean prefs_remove_decode_as_value(pref_t *pref, guint value, gboolean set_default);
prefs_remove_decode_as_value = libwireshark.prefs_remove_decode_as_value
prefs_remove_decode_as_value.restype = gboolean
prefs_remove_decode_as_value.argtypes = [POINTER(pref_t), guint, gboolean]

# void reset_pref(pref_t *pref);
reset_pref = libwireshark.reset_pref
reset_pref.restype = None
reset_pref.argtypes = [POINTER(pref_t)]

# int
# read_prefs_file(const char *pf_path, FILE *pf, pref_set_pair_cb pref_set_pair_fct, void *private_data);
read_prefs_file = libwireshark.read_prefs_file
read_prefs_file.restype = c_int
read_prefs_file.argtypes = [c_char_p,
                                 c_void_p,
                                 pref_set_pair_cb,
                                 c_void_p]

# gboolean
# prefs_pref_is_default(pref_t *pref);
prefs_pref_is_default = libwireshark.prefs_pref_is_default
prefs_pref_is_default.restype = gboolean
prefs_pref_is_default.argtypes = [POINTER(pref_t)]

# guint pref_stash(pref_t *pref, gpointer unused);
pref_stash = libwireshark.pref_stash
pref_stash.restype = guint
pref_stash.argtypes = [POINTER(pref_t), gpointer]

# guint pref_unstash(pref_t *pref, gpointer unstash_data_p);
pref_unstash = libwireshark.pref_unstash
pref_unstash.restype = guint
pref_unstash.argtypes = [POINTER(pref_t), gpointer]

# guint pref_clean_stash(pref_t *pref, gpointer unused);
pref_clean_stash = libwireshark.pref_clean_stash
pref_clean_stash.restype = guint
pref_clean_stash.argtypes = [POINTER(pref_t), gpointer]

# void reset_stashed_pref(pref_t *pref);
reset_stashed_pref = libwireshark.reset_stashed_pref
reset_stashed_pref.restype = None
reset_stashed_pref.argtypes = [POINTER(pref_t)]

# char *
# join_string_list(GList *sl);
join_string_list = libwireshark.join_string_list
join_string_list.restype = c_char_p
join_string_list.argtypes = [POINTER(GList)]

def _initialize():
    init_process_policies()
    relinquish_special_privs_perm()
    
    argv0 = sys.argv[0].encode('utf-8')
    err_msg = init_progfile_dir(argv0)
    if bool(err_msg):
        msg = err_msg.decode('utf-8')
        g_free(err_msg)
        raise WSError(msg)
    
    #initialize_funnel_ops()
    
    if os.name == 'nt':
        ws_init_dll_search_path()
        #load_wpcap()
    
    timestamp_set_type(TS_RELATIVE)
    timestamp_set_precision(TS_PREC_AUTO)
    timestamp_set_seconds_type(TS_SECONDS_DEFAULT)

    wtap_init(True)
    if not bool(epan_init(register_cb(0), None, True)):
        raise WSError('epan initialization failed')
    
    register_all_plugin_tap_listeners()
    epan_load_settings()
    output_fields = output_fields_new()
    
    err_msg = c_char_p(None)
    if not bool(color_filters_init(byref(err_msg), color_filter_add_cb_func(0))):
        msg = err_msg.value.decode('utf-8')
        g_free(err_msg)
        raise WSError(msg)
    
    err_msg = ws_init_sockets()
    if bool(err_msg):
        msg = err_msg.decode('utf-8')
        g_free(err_msg)
        raise WSError(msg)

def _cleanup():
    epan_cleanup()
    wtap_cleanup()
    free_progdirs()

_initialize()
#atexit.register(_cleanup)
