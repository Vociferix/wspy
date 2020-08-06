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
from wspy.errors import *
from wspy.libglib2 import LibGLib2
from wspy.libwsutil import LibWSUtil
from wspy.libwiretap import LibWiretap
import wspy.config as config
import sys


class LibWireshark:

    #######################
    # TYPES AND CONSTANTS #
    #######################

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

    # struct _wmem_array_t;

    class _wmem_array_t(Structure):
        _fields_ = []

    # typedef struct _wmem_array_t wmem_array_t;
    wmem_array_t = _wmem_array_t

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

    # struct _wmem_map_t;

    class _wmem_map_t(Structure):
        _fields_ = []

    # typedef struct _wmem_map_t wmem_map_t;
    wmem_map_t = _wmem_map_t

    # typedef wmem_list_t wmem_stack_t;
    wmem_stack_t = wmem_list_t

    # typedef wmem_list_t wmem_queue_t;
    wmem_queue_t = wmem_list_t

    # struct _wmem_strbuf_t;

    class _wmem_strbuf_t(Structure):
        _fields_ = []

    # typedef struct _wmem_strbuf_t wmem_strbuf_t;
    wmem_strbuf_t = _wmem_strbuf_t

    # struct _wmem_tree_t;

    class _wmem_tree_t(Structure):
        _fields_ = []

    # typedef struct _wmem_tree_t wmem_tree_t;
    wmem_tree_t = _wmem_tree_t

    # #define WMEM_TREE_STRING_NOCASE                 0x00000001
    WMEM_TREE_STRING_NOCASE = 0x00000001

    # typedef struct _wmem_tree_key_t {
    #     guint32 length;
    #     guint32 *key;
    # } wmem_tree_key_t;

    class _wmem_tree_key_t(Structure):
        _fields_ = [('length', LibGLib2.guint32),
                    ('key', POINTER(LibGLib2.guint32))]

    wmem_tree_key_t = _wmem_tree_key_t

    # typedef gboolean (*wmem_foreach_func)(const void *key, void *value, void
    # *userdata);
    wmem_foreach_func = CFUNCTYPE(
        LibGLib2.gboolean, c_void_p, c_void_p, c_void_p)

    # typedef void (*wmem_printer_func)(const void *data);
    wmem_printer_func = CFUNCTYPE(None, c_void_p)

    # typedef struct _wmem_tree_t wmem_itree_t;
    wmem_itree_t = _wmem_tree_t

    # struct _wmem_range_t {
    #     guint64 low;
    #     guint64 high;
    #     guint64 max_edge;
    # };

    class _wmem_range_t(Structure):
        _fields_ = [('low', LibGLib2.guint64),
                    ('high', LibGLib2.guint64),
                    ('max_edge', LibGLib2.guint64)]

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
    wmem_user_cb_t = CFUNCTYPE(LibGLib2.gboolean,
                               POINTER(wmem_allocator_t),
                               wmem_cb_event_t,
                               c_void_p)

    # #define GUID_LEN	16
    GUID_LEN = 16

    # typedef struct _e_guid_t {
    #     guint32 data1;
    #     guint16 data2;
    #     guint16 data3;
    #     guint8  data4[8];
    # } e_guid_t;

    class _e_guid_t(Structure):
        _fields_ = [('data1', LibGLib2.guint32),
                    ('data2', LibGLib2.guint16),
                    ('data3', LibGLib2.guint16),
                    ('data4', LibGLib2.guint8 * 4)]

    e_guid_t = _e_guid_t

    # typedef struct {
    # 	ws_in6_addr addr;
    # 	guint32 prefix;
    # } ipv6_addr_and_prefix;

    class ipv6_addr_and_prefix(Structure):
        _fields_ = [('addr', LibWSUtil.ws_in6_addr),
                    ('prefix', LibGLib2.guint32)]

    # struct tvbuff;

    class tvbuff(Structure):
        _fields_ = []

    # typedef struct tvbuff tvbuff_t;
    tvbuff_t = tvbuff

    # typedef void (*tvbuff_free_cb_t)(void*);
    tvbuff_free_cb_t = CFUNCTYPE(None, c_void_p)

    # typedef struct dgt_set_t {
    #     const unsigned char out[16];
    # } dgt_set_t;

    class dgt_set_t(Structure):
        _fields_ = [('out', c_char * 16)]

    # typedef struct {
    # 	const char	*name;
    # 	const char	*description;
    # 	gint		value;
    # } enum_val_t;

    class enum_val_t(Structure):
        _fields_ = [('name', c_char_p),
                    ('description', c_char_p),
                    ('value', LibGLib2.gint)]

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
        _fields_ = [('low', LibGLib2.guint32),
                    ('high', LibGLib2.guint32)]

    range_admin_t = range_admin_tag

    # #define RANGE_ADMIN_T_INITIALIZER { 0, 0 }
    RANGE_ADMIN_T_INITIALIZER = range_admin_tag(0, 0)

    # typedef struct epan_range {
    #     guint           nranges;
    #     range_admin_t   ranges[1];
    # } range_t;

    class epan_range(Structure):
        pass

    epan_range._fields_ = [('nranges', LibGLib2.guint),
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
        pass

    _e_prefs._fields_ = [('col_list', POINTER(LibGLib2.GList)),
                         ('num_cols', LibGLib2.gint),
                         ('st_client_fg', LibWSUtil.color_t),
                         ('st_client_bg', LibWSUtil.color_t),
                         ('st_server_fg', LibWSUtil.color_t),
                         ('st_server_bg', LibWSUtil.color_t),
                         ('gui_text_valid', LibWSUtil.color_t),
                         ('gui_text_invalid', LibWSUtil.color_t),
                         ('gui_text_deprecated', LibWSUtil.color_t),
                         ('resotre_filter_after_following_stream', LibGLib2.gboolean),
                         ('gui_toolbar_main_style', LibGLib2.gint),
                         ('gui_qt_font_name', LibGLib2.gchar_p),
                         ('gui_active_fg', LibWSUtil.color_t),
                         ('gui_active_bg', LibWSUtil.color_t),
                         ('gui_active_style', LibGLib2.gint),
                         ('gui_inactive_fg', LibWSUtil.color_t),
                         ('gui_inactive_bg', LibWSUtil.color_t),
                         ('gui_inactive_style', LibGLib2.gint),
                         ('gui_marked_fg', LibWSUtil.color_t),
                         ('gui_marked_bg', LibWSUtil.color_t),
                         ('gui_ignored_fg', LibWSUtil.color_t),
                         ('gui_ignored_bg', LibWSUtil.color_t),
                         ('gui_colorized_fg', LibGLib2.gchar_p),
                         ('gui_colorized_bg', LibGLib2.gchar_p),
                         ('gui_geometry_save_position', LibGLib2.gboolean),
                         ('gui_geometry_save_size', LibGLib2.gboolean),
                         ('gui_geometry_save_maximized', LibGLib2.gboolean),
                         ('gui_console_open', console_open_e),
                         ('gui_recent_df_entries_max', LibGLib2.guint),
                         ('gui_recent_file_count_max', LibGLib2.guint),
                         ('gui_fileopen_style', LibGLib2.guint),
                         ('gui_fileopen_dir', LibGLib2.gchar_p),
                         ('gui_fileopen_preview', LibGLib2.guint),
                         ('gui_ask_unsaved', LibGLib2.gboolean),
                         ('gui_autocomplete_filter', LibGLib2.gboolean),
                         ('gui_find_wrap', LibGLib2.gboolean),
                         ('gui_window_title', LibGLib2.gchar_p),
                         ('gui_prepend_window_title', LibGLib2.gchar_p),
                         ('gui_start_title', LibGLib2.gchar_p),
                         ('gui_layout_type', version_info_e),
                         ('gui_max_export_objects', LibGLib2.guint),
                         ('gui_layout_type', layout_type_e),
                         ('gui_layout_content_1', layout_pane_content_e),
                         ('gui_layout_content_2', layout_pane_content_e),
                         ('gui_layout_content_3', layout_pane_content_e),
                         ('gui_interfaces_hide_types', LibGLib2.gchar_p),
                         ('gui_interfaces_show_hidden', LibGLib2.gboolean),
                         ('gui_interfaces_remote_display', LibGLib2.gboolean),
                         ('console_log_level', LibGLib2.gint),
                         ('caputre_device', LibGLib2.gchar_p),
                         ('capture_devices_linktypes', LibGLib2.gchar_p),
                         ('capture_devices_descr', LibGLib2.gchar_p),
                         ('capture_devices_hide', LibGLib2.gchar_p),
                         ('capture_devices_monitor_mode', LibGLib2.gchar_p),
                         ('capture_devices_buffersize', LibGLib2.gchar_p),
                         ('capture_devices_snaplen', LibGLib2.gchar_p),
                         ('capture_devices_pmode', LibGLib2.gchar_p),
                         ('capture_devices_filter', LibGLib2.gchar_p),
                         ('capture_prom_mode', LibGLib2.gboolean),
                         ('capture_pcap_ng', LibGLib2.gboolean),
                         ('capture_real_time', LibGLib2.gboolean),
                         ('capture_auto_scroll', LibGLib2.gboolean),
                         ('capture_no_interface_load', LibGLib2.gboolean),
                         ('capture_no_extcap', LibGLib2.gboolean),
                         ('caputre_show_info', LibGLib2.gboolean),
                         ('capture_columns', POINTER(LibGLib2.GList)),
                         ('tap_update_interval', LibGLib2.guint),
                         ('display_hidden_proto_items', LibGLib2.gboolean),
                         ('display_byte_fields_with_spaces', LibGLib2.gboolean),
                         ('enable_incomplete_dissectors_check', LibGLib2.gboolean),
                         ('incomplete_dissectors_check_debug', LibGLib2.gboolean),
                         ('strict_conversation_tracking_heuristics', LibGLib2.gboolean),
                         ('filter_expressions_old', LibGLib2.gboolean),
                         ('gui_update_enabled', LibGLib2.gboolean),
                         ('gui_update_channel', software_update_channel_e),
                         ('gui_update_interval', LibGLib2.gint),
                         ('saved_at_version', LibGLib2.gchar_p),
                         ('unknown_prefs', LibGLib2.gboolean),
                         ('unknown_colorfilters', LibGLib2.gboolean),
                         ('gui_qt_packet_list_separator', LibGLib2.gboolean),
                         ('gui_qt_packet_header_column_definition', LibGLib2.gboolean),
                         ('gui_qt_show_selected_packet', LibGLib2.gboolean),
                         ('gui_qt_show_file_load_time', LibGLib2.gboolean),
                         ('gui_packet_editor', LibGLib2.gboolean),
                         ('gui_packet_list_elide_mode', elide_mode_e),
                         ('gui_packet_list_show_related', LibGLib2.gboolean),
                         ('gui_packet_list_show_minimap', LibGLib2.gboolean),
                         ('st_enable_burstinfo', LibGLib2.gboolean),
                         ('st_burst_showcount', LibGLib2.gboolean),
                         ('st_burst_resolution', LibGLib2.gint),
                         ('st_burst_windowlen', LibGLib2.gint),
                         ('st_sort_casesensitve', LibGLib2.gboolean),
                         ('st_sort_rng_fixorder', LibGLib2.gboolean),
                         ('st_sort_rng_nameonly', LibGLib2.gboolean),
                         ('st_sort_defcolflag', LibGLib2.gint),
                         ('st_sort_defdescending', LibGLib2.gboolean),
                         ('st_sort_showfullname', LibGLib2.gboolean),
                         ('extcap_save_on_start', LibGLib2.gboolean)]

    e_prefs = _e_prefs

    # struct pref_module;

    class pref_module(Structure):
        _fields_ = []

    # struct pref_custom_cbs;

    class pref_custom_cbs(Structure):
        _fields_ = []

    # typedef struct pref_module module_t;
    module_t = pref_module

    # typedef guint (*module_cb)(module_t *module, gpointer user_data);
    module_cb = CFUNCTYPE(LibGLib2.guint, POINTER(module_t), LibGLib2.gpointer)

    # struct preference;

    class preference(Structure):
        _fields_ = []

    # typedef struct preference pref_t;
    pref_t = preference

    # typedef guint (*pref_cb)(pref_t *pref, gpointer user_data);
    pref_cb = CFUNCTYPE(LibGLib2.guint, POINTER(pref_t), LibGLib2.gpointer)

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

    # struct _packet_info;

    class _packet_info(Structure):
        _fields_ = []

    # struct epan_session;

    class epan_session(Structure):
        _fields_ = []

    # typedef enum {
    #   PACKET_CHAR_ENC_CHAR_ASCII     = 0,
    #   PACKET_CHAR_ENC_CHAR_EBCDIC    = 1
    # } packet_char_enc;
    packet_char_end = c_int
    PACKET_CHAR_ENC_CHAR_ASCII = c_int(0)
    PACKET_CHAR_END_CHAR_EBCDIC = c_int(1)

    # struct _color_filter;

    class _color_filter(Structure):
        _fields_ = []

    # typedef struct _frame_data {
    #   guint32      num;
    #   guint32      pkt_len;
    #   guint32      cap_len;
    #   guint32      cum_bytes;
    #   gint64       file_off;
    #   GSList      *pfd;
    #   const struct _color_filter *color_filter;
    #   guint16      subnum;
    #   unsigned int passed_dfilter   : 1;
    #   unsigned int dependent_of_displayed : 1;
    #   unsigned int encoding         : 1;
    #   unsigned int visited          : 1;
    #   unsigned int marked           : 1;
    #   unsigned int ref_time         : 1;
    #   unsigned int ignored          : 1;
    #   unsigned int has_ts           : 1;
    #   unsigned int has_phdr_comment : 1;
    #   unsigned int has_user_comment : 1;
    #   unsigned int need_colorize    : 1;
    #   unsigned int tsprec           : 4;
    #   nstime_t     abs_ts;
    #   nstime_t     shift_offset;
    #   guint32      frame_ref_num;
    #   guint32      prev_dis_num;
    # } frame_data;

    class _frame_data(Structure):
        pass

    _frame_data._fields_ = [('num', LibGLib2.guint32),
                            ('pkt_len', LibGLib2.guint32),
                            ('cap_len', LibGLib2.guint32),
                            ('cum_bytes', LibGLib2.guint32),
                            ('file_off', LibGLib2.gint64),
                            ('pfd', POINTER(LibGLib2.GSList)),
                            ('color_filter', POINTER(_color_filter)),
                            ('subnum', LibGLib2.guint16),
                            ('passed_dfilter', c_uint, 1),
                            ('dependent_of_displayed', c_uint, 1),
                            ('encoding', c_uint, 1),
                            ('visited', c_uint, 1),
                            ('marked', c_uint, 1),
                            ('ref_time', c_uint, 1),
                            ('ignored', c_uint, 1),
                            ('has_ts', c_uint, 1),
                            ('has_phdr_comment', c_uint, 1),
                            ('has_user_comment', c_uint, 1),
                            ('need_colorize', c_uint, 1),
                            ('tsprec', c_uint, 4),
                            ('abs_ts', LibWSUtil.nstime_t),
                            ('shift_offset', LibWSUtil.nstime_t),
                            ('frame_ref_num', LibGLib2.guint32),
                            ('prev_dis_num', LibGLib2.guint32)]

    frame_data = _frame_data

    # typedef enum {
    #     RA_NONE,
    #     RA_DISSECTORS,
    #     RA_LISTENERS,
    #     RA_EXTCAP,
    #     RA_REGISTER,
    #     RA_PLUGIN_REGISTER,
    #     RA_HANDOFF,
    #     RA_PLUGIN_HANDOFF,
    #     RA_LUA_PLUGINS,
    #     RA_LUA_DEREGISTER,
    #     RA_PREFERENCES,
    #     RA_INTERFACES
    # } register_action_e;
    register_action_e = c_int
    RA_NONE = c_int(0)
    RA_DISSECTORS = c_int(1)
    RA_LISTENERS = c_int(2)
    RA_EXTCAP = c_int(3)
    RA_REGISTER = c_int(4)
    RA_PLUGIN_REGISTER = c_int(5)
    RA_HANDOFF = c_int(6)
    RA_PLUGIN_HANDOFF = c_int(7)
    RA_LUA_PLUGINS = c_int(8)
    RA_LUA_DEREGISTER = c_int(9)
    RA_PREFERENCES = c_int(10)
    RA_INTERFACES = c_int(11)

    # #define RA_BASE_COUNT (RA_INTERFACES - 3)
    RA_BASE_COUNT = c_int(RA_INTERFACES.value - 3)

    # typedef void (*register_cb)(register_action_e action, const char
    # *message, gpointer client_data);
    register_cb = CFUNCTYPE(
        None,
        register_action_e,
        c_char_p,
        LibGLib2.gpointer)

    # typedef struct epan_dissect epan_dissect_t;

    class epan_dissect(Structure):
        _fields_ = []

    epan_dissect_t = epan_dissect

    # struct epan_dfilter;

    class epan_dfilter(Structure):
        _fields_ = []

    # struct epan_column_info;

    class epan_column_info(Structure):
        _fields_ = []

    # struct packet_provider_data;

    class packet_provider_data(Structure):
        _fields_ = []

    # struct packet_provider_funcs {
    # 	const nstime_t *(*get_frame_ts)(struct packet_provider_data *prov, guint32 frame_num);
    # 	const char *(*get_interface_name)(struct packet_provider_data *prov, guint32 interface_id);
    # 	const char *(*get_interface_description)(struct packet_provider_data *prov, guint32 interface_id);
    # 	const char *(*get_user_comment)(struct packet_provider_data *prov, const frame_data *fd);
    # };

    class packet_provider_funcs(Structure):
        pass

    packet_provider_funcs._fields_ = [
        ('get_frame_ts',
         CFUNCTYPE(
             POINTER(
                 LibWSUtil.nstime_t),
             POINTER(packet_provider_data),
             LibGLib2.guint32)),
        ('get_interface_name',
         CFUNCTYPE(
             c_char_p,
             POINTER(packet_provider_data),
             LibGLib2.guint32)),
        ('get_interface_description',
         CFUNCTYPE(
             c_char_p,
             POINTER(packet_provider_data),
             LibGLib2.guint32)),
        ('get_user_comment',
         CFUNCTYPE(
             c_char_p,
             POINTER(packet_provider_data),
             POINTER(frame_data)))]

    # typedef struct {
    # 	void (*init)(void);
    # 	void (*dissect_init)(epan_dissect_t *);
    # 	void (*dissect_cleanup)(epan_dissect_t *);
    # 	void (*cleanup)(void);
    # 	void (*register_all_protocols)(register_cb, gpointer);
    # 	void (*register_all_handoffs)(register_cb, gpointer);
    # 	void (*register_all_tap_listeners)(void);
    # } epan_plugin;

    class epan_plugin(Structure):
        pass

    epan_plugin._fields_ = [('init', CFUNCTYPE(None)),
                            ('dissect_init', CFUNCTYPE(None, POINTER(epan_dissect_t))),
                            ('dissect_cleanup', CFUNCTYPE(None, POINTER(epan_dissect_t))),
                            ('cleanup', CFUNCTYPE(None)),
                            ('register_all_protocols', CFUNCTYPE(None, register_cb, LibGLib2.gpointer)),
                            ('register_all_handoffs', CFUNCTYPE(None, register_cb, LibGLib2.gpointer)),
                            ('register_all_tap_listeners', CFUNCTYPE(None))]

    # typedef struct epan_session epan_t;
    epan_t = epan_session

    # typedef struct {
    # 	guint32	addr;
    # 	guint32	nmask;
    # } ipv4_addr_and_mask;

    class ipv4_addr_and_mask(Structure):
        _fields_ = [('addr', LibGLib2.guint32),
                    ('nmask', LibGLib2.guint32)]

    # typedef enum {
    # 	TO_STR_TIME_RES_T_SECS,
    # 	TO_STR_TIME_RES_T_DSECS,
    # 	TO_STR_TIME_RES_T_CSECS,
    # 	TO_STR_TIME_RES_T_MSECS,
    # 	TO_STR_TIME_RES_T_USECS,
    # 	TO_STR_TIME_RES_T_NSECS
    # } to_str_time_res_t;
    to_str_time_res_t = c_int
    TO_STR_TIME_RES_T_SECS = c_int(0)
    TO_STR_TIME_RES_T_DSECS = c_int(1)
    TO_STR_TIME_RES_T_CSECS = c_int(2)
    TO_STR_TIME_RES_T_MSECS = c_int(3)
    TO_STR_TIME_RES_T_USECS = c_int(4)
    TO_STR_TIME_RES_T_NSECS = c_int(5)

    # typedef enum {
    # 	ABSOLUTE_TIME_LOCAL = 1000,
    # 	ABSOLUTE_TIME_UTC,
    # 	ABSOLUTE_TIME_DOY_UTC,
    # 	ABSOLUTE_TIME_NTP_UTC
    # } absolute_time_display_e;
    absolute_time_display_e = c_int
    ABSOLUTE_TIME_LOCAL = c_int(1000)
    ABSOLUTE_TIME_UTC = c_int(1001)
    ABSOLUTE_TIME_DOY_UTC = c_int(1002)
    ABSOLUTE_TIME_NTP_UTC = c_int(1003)

    # typedef struct _value_string {
    #     guint32      value;
    #     const gchar *strptr;
    # } value_string;

    class _value_string(Structure):
        _fields_ = [('value', LibGLib2.guint32),
                    ('strptr', LibGLib2.gchar_p)]

    value_string = _value_string

    # typedef struct _val64_string {
    #     guint64      value;
    #     const gchar *strptr;
    # } val64_string;

    class _val64_string(Structure):
        _fields_ = [('value', LibGLib2.guint64),
                    ('strptr', LibGLib2.gchar_p)]

    val64_string = _val64_string

    # typedef struct _value_string_ext value_string_ext;

    class _value_string_ext(Structure):
        pass

    value_string_ext = _value_string_ext

    # typedef const value_string *(*_value_string_match2_t)(const guint32,
    # value_string_ext*);
    _value_string_match2_t = CFUNCTYPE(POINTER(value_string),
                                       LibGLib2.guint32,
                                       POINTER(value_string_ext))

    # struct _value_string_ext {
    #     _value_string_match2_t _vs_match2;
    #     guint32                _vs_first_value;
    #     guint                  _vs_num_entries;
    #     const value_string    *_vs_p;
    #     const gchar           *_vs_name;
    # };
    _value_string_ext._fields_ = [('_vs_match2', _value_string_match2_t),
                                  ('_vs_first_value', LibGLib2.guint32),
                                  ('_vs_num_entries', LibGLib2.guint),
                                  ('_vs_p', POINTER(value_string)),
                                  ('_vs_name', LibGLib2.gchar_p)]

    # typedef struct _val64_string_ext val64_string_ext;

    class _val64_string_ext(Structure):
        pass

    val64_string_ext = _val64_string_ext

    # typedef const val64_string *(*_val64_string_match2_t)(const guint64,
    # val64_string_ext*);
    _val64_string_match2_t = CFUNCTYPE(POINTER(val64_string),
                                       LibGLib2.guint64,
                                       POINTER(val64_string_ext))

    # struct _val64_string_ext {
    #     _val64_string_match2_t _vs_match2;
    #     guint64                _vs_first_value;
    #     guint                  _vs_num_entries;
    #     const val64_string    *_vs_p;
    #     const gchar           *_vs_name;
    # };
    _val64_string_ext._fields_ = [('_vs_match2', _val64_string_match2_t),
                                  ('_vs_first_value', LibGLib2.guint64),
                                  ('_vs_num_entries', LibGLib2.guint),
                                  ('_vs_p', POINTER(val64_string)),
                                  ('_vs_name', LibGLib2.gchar_p)]

    # typedef struct _string_string {
    #     const gchar *value;
    #     const gchar *strptr;
    # } string_string;

    class _string_string(Structure):
        _fields_ = [('value', LibGLib2.gchar_p),
                    ('strptr', LibGLib2.gchar_p)]

    string_string = _string_string

    # typedef struct _range_string {
    #     guint32      value_min;
    #     guint32      value_max;
    #     const gchar *strptr;
    # } range_string;

    class _range_string(Structure):
        _fields_ = [('value_min', LibGLib2.guint32),
                    ('value_max', LibGLib2.guint32),
                    ('strptr', LibGLib2.gchar_p)]

    range_string = _range_string

    # typedef struct _bytes_string {
    #   const guint8 *value;
    #   const size_t  value_length;
    #   const gchar  *strptr;
    # } bytes_string;

    class _bytes_string(Structure):
        _fields_ = [('value', POINTER(LibGLib2.guint8)),
                    ('value_length', c_size_t),
                    ('strptr', LibGLib2.gchar_p)]

    bytes_string = _bytes_string

    # typedef struct true_false_string {
    #         const char      *true_string;
    #         const char      *false_string;
    # } true_false_string;

    class true_false_string(Structure):
        _fields_ = [('true_string', c_char_p),
                    ('false_string', c_char_p)]

    # typedef enum {
    #     AT_NONE,
    #     AT_ETHER,
    #     AT_IPv4,
    #     AT_IPv6,
    #     AT_IPX,
    #     AT_FC,
    #     AT_FCWWN,
    #     AT_STRINGZ,
    #     AT_EUI64,
    #     AT_IB,
    #     AT_AX25,
    #     AT_VINES,
    #     AT_END_OF_LIST
    # } address_type;
    address_type = c_int
    AT_NONE = c_int(0)
    AT_ETHER = c_int(1)
    AT_IPv4 = c_int(2)
    AT_IPv6 = c_int(3)
    AT_IPX = c_int(4)
    AT_FC = c_int(5)
    AT_FCWWN = c_int(6)
    AT_STRINGZ = c_int(7)
    AT_EUI64 = c_int(8)
    AT_IB = c_int(9)
    AT_AX25 = c_int(10)
    AT_VINES = c_int(11)
    AT_END_OF_LIST = c_int(12)

    # typedef struct _address {
    #     int           type;
    #     int           len;
    #     const void   *data;
    #     void         *priv;
    # } address;

    class _address(Structure):
        _fields_ = [('type', c_int),
                    ('len', c_int),
                    ('data', c_void_p),
                    ('priv', c_void_p)]

    address = _address

    # typedef enum {
    #     PT_NONE,
    #     PT_SCTP,
    #     PT_TCP,
    #     PT_UDP,
    #     PT_DCCP,
    #     PT_IPX,
    #     PT_DDP,
    #     PT_IDP,
    #     PT_USB,
    #     PT_I2C,
    #     PT_IBQP,
    #     PT_BLUETOOTH
    # } port_type;
    port_type = c_int
    PT_NONE = c_int(0)
    PT_SCTP = c_int(1)
    PT_TCP = c_int(2)
    PT_UDP = c_int(3)
    PT_DCCP = c_int(4)
    PT_IPX = c_int(5)
    PT_DDP = c_int(6)
    PT_IDP = c_int(7)
    PT_USB = c_int(8)
    PT_I2C = c_int(9)
    PT_IBQP = c_int(10)

    PT_BLUETOOTH = c_int(11)

    class endpoint(Structure):
        _fields_ = []

    # define P2P_DIR_UNKNOWN -1
    P2P_DIR_UNKNOWN = -1

    # define P2P_DIR_SENT    0
    P2P_DIR_SENT = 0

    # define P2P_DIR_RECV    1
    P2P_DIR_RECV = 1

    # define LINK_DIR_UNKNOWN    -1
    LINK_DIR_UNKNOWN = -1

    # define P2P_DIR_UL  0
    P2P_DIR_UL = 0

    # define P2P_DIR_DL  1
    P2P_DIR_DL = 1

    # define PINFO_HAS_TS            0x00000001
    PINFO_HAS_TS = 0x00000001

    # typedef struct _packet_info {
    #   const char *current_proto;
    #   struct epan_column_info *cinfo;
    #   guint32 presence_flags;
    #   guint32 num;
    #   nstime_t abs_ts;
    #   nstime_t rel_ts;
    #   frame_data *fd;
    #   union wtap_pseudo_header *pseudo_header;
    #   wtap_rec *rec;
    #   GSList *data_src;
    #   address dl_src;
    #   address dl_dst;
    #   address net_src;
    #   address net_dst;
    #   address src;
    #   address dst;
    #   guint32 vlan_id;
    #   const char *noreassembly_reason;
    #   gboolean fragmented;
    #   struct {
    #     guint32 in_error_pkt:1;
    #     guint32 in_gre_pkt:1;
    #   } flags;
    #   port_type ptype;
    #   guint32 srcport;
    #   guint32 destport;
    #   guint32 match_uint;
    #   const char *match_string;
    #   gboolean use_endpoint;
    #   struct endpoint* conv_endpoint;
    #   guint16 can_desegment;
    #   guint16 saved_can_desegment;
    #   int desegment_offset;
    # #define DESEGMENT_ONE_MORE_SEGMENT 0x0fffffff
    # #define DESEGMENT_UNTIL_FIN        0x0ffffffe
    #   guint32 desegment_len;
    #   guint16 want_pdu_tracking;
    #   guint32 bytes_until_next_pdu;
    #   int     p2p_dir;
    #   GHashTable *private_table;
    #   wmem_list_t *layers;
    #   guint8 curr_layer_num;
    #   guint16 link_number;
    #   guint16 clnp_srcref;
    #   guint16 clnp_dstref;
    #   int link_dir;
    #   GSList* proto_data;
    #   GSList* dependent_frames;
    #   GSList* frame_end_routines;
    #   wmem_allocator_t *pool;
    #   struct epan_session *epan;
    #   const gchar *heur_list_name;
    # } packet_info;

    class _packet_info_flags(Structure):
        _fields_ = [('in_error_pkt', LibGLib2.guint32, 1),
                    ('in_gre_pkt', LibGLib2.guint32, 1)]

    class _packet_info(Structure):
        pass

    _packet_info._fields_ = [('current_proto', c_char_p),
                             ('cinfo', POINTER(epan_column_info)),
                             ('presence_flags', LibGLib2.guint32),
                             ('num', LibGLib2.guint32),
                             ('abs_ts', LibWSUtil.nstime_t),
                             ('rel_ts', LibWSUtil.nstime_t),
                             ('fd', POINTER(frame_data)),
                             ('pseudo_header', POINTER(LibWiretap.wtap_pseudo_header)),
                             ('rec', POINTER(LibWiretap.wtap_rec)),
                             ('data_src', POINTER(LibGLib2.GSList)),
                             ('dl_src', address),
                             ('dl_dst', address),
                             ('net_src', address),
                             ('net_dst', address),
                             ('src', address),
                             ('dst', address),
                             ('vlan_id', LibGLib2.guint32),
                             ('noreassembly_reason', c_char_p),
                             ('fragmented', LibGLib2.gboolean),
                             ('flags', _packet_info_flags),
                             ('ptype', port_type),
                             ('srcport', LibGLib2.guint32),
                             ('destport', LibGLib2.guint32),
                             ('match_uint', LibGLib2.guint32),
                             ('use_endpoint', LibGLib2.gboolean),
                             ('conv_endpoint', POINTER(endpoint)),
                             ('can_desegment', LibGLib2.guint16),
                             ('saved_can_desgment', LibGLib2.guint16),
                             ('desegment_offset', c_int),
                             ('desegment_len', LibGLib2.guint32),
                             ('want_pdu_tracking', LibGLib2.guint16),
                             ('bytes_unitl_next_pdu', LibGLib2.guint32),
                             ('p2p_dir', c_int),
                             ('private_table', POINTER(LibGLib2.GHashTable)),
                             ('layers', POINTER(wmem_list_t)),
                             ('curr_layer_num', LibGLib2.guint8),
                             ('link_number', LibGLib2.guint16),
                             ('clnp_srcref', LibGLib2.guint16),
                             ('clnp_dstref', LibGLib2.guint16),
                             ('link_dir', c_int),
                             ('proto_data', POINTER(LibGLib2.GSList)),
                             ('dependent_frames', POINTER(LibGLib2.GSList)),
                             ('frame_end_routines', POINTER(LibGLib2.GSList)),
                             ('pool', POINTER(wmem_allocator_t)),
                             ('epan', POINTER(epan_session)),
                             ('heur_list_name', LibGLib2.gchar_p)]

    packet_info = _packet_info

    DESEGMENT_ONE_MORE_SEGMENT = 0x0fffffff
    DESEGMENT_UNTIL_FIN = 0x0ffffffe

    # enum ftenum {
    # 	FT_NONE,
    # 	FT_PROTOCOL,
    # 	FT_BOOLEAN,
    # 	FT_CHAR,
    # 	FT_UINT8,
    # 	FT_UINT16,
    # 	FT_UINT24,
    # 	FT_UINT32,
    # 	FT_UINT40,
    # 	FT_UINT48,
    # 	FT_UINT56,
    # 	FT_UINT64,
    # 	FT_INT8,
    # 	FT_INT16,
    # 	FT_INT24,
    # 	FT_INT32,
    # 	FT_INT40,
    # 	FT_INT48,
    # 	FT_INT56,
    # 	FT_INT64,
    # 	FT_IEEE_11073_SFLOAT,
    # 	FT_IEEE_11073_FLOAT,
    # 	FT_FLOAT,
    # 	FT_DOUBLE,
    # 	FT_ABSOLUTE_TIME,
    # 	FT_RELATIVE_TIME,
    # 	FT_STRING,
    # 	FT_STRINGZ,
    # 	FT_UINT_STRING,
    # 	FT_ETHER,
    # 	FT_BYTES,
    # 	FT_UINT_BYTES,
    # 	FT_IPv4,
    # 	FT_IPv6,
    # 	FT_IPXNET,
    # 	FT_FRAMENUM,
    # 	FT_PCRE,
    # 	FT_GUID,
    # 	FT_OID,
    # 	FT_EUI64,
    # 	FT_AX25,
    # 	FT_VINES,
    # 	FT_REL_OID,
    # 	FT_SYSTEM_ID,
    # 	FT_STRINGZPAD,
    # 	FT_FCWWN,
    # 	FT_NUM_TYPES
    # };
    ftenum = c_int
    FT_NONE = c_int(0)
    FT_PROTOCOL = c_int(1)
    FT_BOOLEAN = c_int(2)
    FT_CHAR = c_int(3)
    FT_UINT8 = c_int(4)
    FT_UINT16 = c_int(5)
    FT_UINT24 = c_int(6)
    FT_UINT32 = c_int(7)
    FT_UINT40 = c_int(8)
    FT_UINT48 = c_int(9)
    FT_UINT56 = c_int(10)
    FT_UINT64 = c_int(11)
    FT_INT8 = c_int(12)
    FT_INT16 = c_int(13)
    FT_INT24 = c_int(14)
    FT_INT32 = c_int(15)
    FT_INT40 = c_int(16)
    FT_INT48 = c_int(17)
    FT_INT56 = c_int(18)
    FT_INT64 = c_int(19)
    FT_IEEE_11073_SFLOAT = c_int(20)
    FT_IEEE_11073_FLOAT = c_int(21)
    FT_FLOAT = c_int(22)
    FT_DOUBLE = c_int(23)
    FT_ABSOLUTE_TIME = c_int(24)
    FT_RELATIVE_TIME = c_int(25)
    FT_STRING = c_int(26)
    FT_STRINGZ = c_int(27)
    FT_UINT_STRING = c_int(28)
    FT_ETHER = c_int(29)
    FT_BYTES = c_int(30)
    FT_UINT_BYTES = c_int(31)
    FT_IPv4 = c_int(32)
    FT_IPv6 = c_int(33)
    FT_IPXNET = c_int(34)
    FT_FRAMENUM = c_int(35)
    FT_PCRE = c_int(36)
    FT_GUID = c_int(37)
    FT_OID = c_int(38)
    FT_EUI64 = c_int(39)
    FT_AX25 = c_int(40)
    FT_VINES = c_int(41)
    FT_REL_OID = c_int(42)
    FT_SYSTEM_ID = c_int(43)
    FT_STRINGZPAD = c_int(44)
    FT_FCWWN = c_int(45)
    FT_NUM_TYPES = c_int(46)

    # #define FT_ETHER_LEN		6
    FT_ETHER_LEN = 6

    # #define FT_GUID_LEN		16
    FT_GUID_LEN = 16

    # #define FT_IPv4_LEN		4
    FT_IPv4_LEN = 4

    # #define FT_IPv6_LEN		16
    FT_IPv6_LEN = 16

    # #define FT_IPXNET_LEN		4
    FT_IPXNET_LEN = 4

    # #define FT_EUI64_LEN		8
    FT_EUI64_LEN = 8

    # #define FT_AX25_ADDR_LEN	7
    FT_AX25_ADDR_LEN = 7

    # #define FT_VINES_ADDR_LEN	6
    FT_VINES_ADDR_LEN = 6

    # #define FT_FCWWN_LEN		8
    FT_FCWWN_LEN = 8

    # #define FT_VARINT_MAX_LEN	10
    FT_VARINT_MAX_LEN = 10

    # typedef enum ftenum ftenum_t;
    ftenum_t = ftenum

    # enum ft_framenum_type {
    # 	FT_FRAMENUM_NONE,
    # 	FT_FRAMENUM_REQUEST,
    # 	FT_FRAMENUM_RESPONSE,
    # 	FT_FRAMENUM_ACK,
    # 	FT_FRAMENUM_DUP_ACK,
    # 	FT_FRAMENUM_RETRANS_PREV,
    # 	FT_FRAMENUM_RETRANS_NEXT,
    # 	FT_FRAMENUM_NUM_TYPES
    # };
    ft_framenum_type = c_int
    FT_FRAMENUM_NONE = c_int(0)
    FT_FRAMENUM_REQUEST = c_int(1)
    FT_FRAMENUM_RESPONSE = c_int(2)
    FT_FRAMENUM_ACK = c_int(3)
    FT_FRAMENUM_DUP_ACK = c_int(4)
    FT_FRAMENUM_RETRANS_PREV = c_int(5)
    FT_FRAMENUM_RETRANS_NEXT = c_int(6)
    FT_FRAMENUM_NUM_TYPES = c_int(7)

    # typedef enum ft_framenum_type ft_framenum_type_t;
    ft_framenum_type_t = ft_framenum_type

    # struct _ftype_t;

    class _ftype_t(Structure):
        _fields_ = []

    # typedef struct _ftype_t ftype_t;
    ftype_t = _ftype_t

    # enum ftrepr {
    # 	FTREPR_DISPLAY,
    # 	FTREPR_DFILTER
    # };
    ftrepr = c_int
    FTREPR_DISPLAY = c_int(0)
    FTREPR_DFILTER = c_int(1)

    # typedef enum ftrepr ftrepr_t;
    ftrepr_t = ftrepr

    # typedef struct _protocol_value_t {
    # 	tvbuff_t	*tvb;
    # 	gchar		*proto_string;
    # } protocol_value_t;

    class _protocol_value_t(Structure):
        pass

    _protocol_value_t._fields_ = [('tvb', POINTER(tvbuff_t)),
                                  ('proto_string', LibGLib2.gchar_p)]

    protocol_value_t = _protocol_value_t

    # typedef struct _fvalue_t {
    # 	ftype_t	*ftype;
    # 	union {
    # 		guint32			uinteger;
    # 		gint32			sinteger;
    # 		guint64			integer64;
    # 		guint64			uinteger64;
    # 		gint64			sinteger64;
    # 		gdouble			floating;
    # 		gchar			*string;
    # 		guchar			*ustring;
    # 		GByteArray		*bytes;
    # 		ipv4_addr_and_mask	ipv4;
    # 		ipv6_addr_and_prefix	ipv6;
    # 		e_guid_t		guid;
    # 		nstime_t		time;
    # 		protocol_value_t 	protocol;
    # 		GRegex			*re;
    # 		guint16			sfloat_ieee_11073;
    # 		guint32			float_ieee_11073;
    # 	} value;
    # 	gboolean	fvalue_gboolean1;
    # } fvalue_t;

    class _fvalue_t_value(Union):
        pass

    _fvalue_t_value._fields_ = [('uinteger', LibGLib2.guint32),
                                ('sinteger', LibGLib2.gint32),
                                ('integer64', LibGLib2.guint64),
                                ('uinteger64', LibGLib2.guint64),
                                ('sinteger64', LibGLib2.gint64),
                                ('floating', LibGLib2.gdouble),
                                ('string', LibGLib2.gchar_p),
                                ('ustring', POINTER(LibGLib2.guchar)),
                                ('bytes', POINTER(LibGLib2.GByteArray)),
                                ('ipv4', ipv4_addr_and_mask),
                                ('ipv6', ipv6_addr_and_prefix),
                                ('guid', e_guid_t),
                                ('time', LibWSUtil.nstime_t),
                                ('protocol', protocol_value_t),
                                ('re', POINTER(LibGLib2.GRegex)),
                                ('sfloat_ieee_11073', LibGLib2.guint16),
                                ('float_ieee_11073', LibGLib2.guint32)]

    class _fvalue_t(Structure):
        pass

    _fvalue_t._fields_ = [('ftype', POINTER(ftype_t)),
                          ('value', _fvalue_t_value),
                          ('fvalue_gboolean1', LibGLib2.gboolean)]

    fvalue_t = _fvalue_t

    # typedef enum {
    #     RA_NONE,
    #     RA_DISSECTORS,
    #     RA_LISTENERS,
    #     RA_EXTCAP,
    #     RA_REGISTER,
    #     RA_PLUGIN_REGISTER,
    #     RA_HANDOFF,
    #     RA_PLUGIN_HANDOFF,
    #     RA_LUA_PLUGINS,
    #     RA_LUA_DEREGISTER,
    #     RA_PREFERENCES,
    #     RA_INTERFACES
    # } register_action_e;
    register_action_e = c_int
    RA_NONE = c_int(0)
    RA_DISSECTORS = c_int(1)
    RA_LISTENERS = c_int(2)
    RA_EXTCAP = c_int(3)
    RA_REGISTER = c_int(4)
    RA_PLUGIN_REGISTER = c_int(5)
    RA_HANDOFF = c_int(6)
    RA_PLUGIN_HANDOFF = c_int(7)
    RA_LUA_PLUGINS = c_int(8)
    RA_LUA_DEREGISTER = c_int(9)
    RA_PREFERENCES = c_int(10)
    RA_INTERFACES = c_int(11)

    # #define RA_BASE_COUNT (RA_INTERFACES - 3)
    RA_BASE_COUNT = c_int(RA_INTERFACES.value - 3)

    # typedef void (*register_cb)(register_action_e action, const char
    # *message, gpointer client_data);
    register_cb = CFUNCTYPE(
        None,
        register_action_e,
        c_char_p,
        LibGLib2.gpointer)

    # #define ITEM_LABEL_LENGTH       240
    ITEM_LABEL_LENGTH = 240

    # #define ITEM_LABEL_UNKNOWN_STR  "Unknown"
    ITEM_LABEL_UNKNOWN_STR = b'Unknown'

    # struct expert_field;

    class expert_field(Structure):
        _fields_ = []

    # typedef void (*custom_fmt_func_t)(gchar *, guint32);
    custom_fmt_func_t = CFUNCTYPE(None, LibGLib2.gchar_p, LibGLib2.guint32)

    # typedef void (*custom_fmt_func_64_t)(gchar *, guint64);
    custom_fmt_func_64_t = CFUNCTYPE(None, LibGLib2.gchar_p, LibGLib2.guint64)

    # struct _protocol;

    class _protocol(Structure):
        _fields_ = []

    # typedef struct _protocol protocol_t;
    protocol_t = _protocol

    # #define ENC_BIG_ENDIAN      0x00000000
    ENC_BIG_ENDIAN = 0x00000000

    # #define ENC_LITTLE_ENDIAN   0x80000000
    ENC_LITTLE_ENDIAN = 0x80000000

    # if G_BYTE_ORDER == G_LITTLE_ENDIAN
    if sys.byteorder == 'little':
        # define ENC_HOST_ENDIAN ENC_LITTLE_ENDIAN
        ENC_HOST_ENDIAN = ENC_LITTLE_ENDIAN
    # else
    else:
        # define ENC_HOST_ENDIAN ENC_BIG_ENDIAN
        ENC_HOST_ENDIAN = ENC_BIG_ENDIAN

    # #define ENC_TIME_SECS_NSECS    0x00000000
    ENC_TIME_SECS_NSECS = 0x00000000

    # #define ENC_TIME_TIMESPEC      0x00000000
    ENC_TIME_TIMESPEC = 0x00000000

    # #define ENC_TIME_NTP           0x00000002
    ENC_TIME_NTP = 0x00000002

    # #define ENC_TIME_TOD           0x00000004
    ENC_TIME_TOD = 0x00000004

    # #define ENC_TIME_RTPS          0x00000008
    ENC_TIME_RTPS = 0x00000008

    # #define ENC_TIME_NTP_BASE_ZERO 0x00000008
    ENC_TIME_NTP_BASE_ZERO = 0x00000008

    # #define ENC_TIME_SECS_USECS    0x00000010
    ENC_TIME_SECS_USECS = 0x00000010

    # #define ENC_TIME_TIMEVAL       0x00000010
    ENC_TIME_TIMEVAL = 0x00000010

    # #define ENC_TIME_SECS          0x00000012
    ENC_TIME_SECS = 0x00000012

    # #define ENC_TIME_MSECS         0x00000014
    ENC_TIME_MSECS = 0x00000014

    # #define ENC_TIME_SECS_NTP      0x00000018
    ENC_TIME_SECS_NTP = 0x00000018

    # #define ENC_TIME_RFC_3971      0x00000020
    ENC_TIME_RFC_3971 = 0x00000020

    # #define ENC_TIME_MSEC_NTP      0x00000022
    ENC_TIME_MSEC_NTP = 0x00000022

    # #define ENC_TIME_MIP6          0x00000024
    ENC_TIME_MIP6 = 0x00000024

    # #define ENC_ZIGBEE               0x40000000
    ENC_ZIGBEE = 0x40000000

    # #define ENC_CHARENCODING_MASK    0x3FFFFFFE
    ENC_CHARENCODING_MASK = 0x3FFFFFFE

    # #define ENC_ASCII                0x00000000
    ENC_ASCII = 0x00000000

    # #define ENC_ISO_646_IRV          ENC_ASCII
    ENC_ISO_646_IRV = ENC_ASCII

    # #define ENC_UTF_8                0x00000002
    ENC_UTF_8 = 0x00000002

    # #define ENC_UTF_16               0x00000004
    ENC_UTF_16 = 0x00000004

    # #define ENC_UCS_2                0x00000006
    ENC_UCS_2 = 0x00000006

    # #define ENC_UCS_4                0x00000008
    ENC_UCS_4 = 0x00000008

    # #define ENC_ISO_8859_1           0x0000000A
    ENC_ISO_8859_1 = 0x0000000A

    # #define ENC_ISO_8859_2           0x0000000C
    ENC_ISO_8859_2 = 0x0000000C

    # #define ENC_ISO_8859_3           0x0000000E
    ENC_ISO_8859_3 = 0x0000000E

    # #define ENC_ISO_8859_4           0x00000010
    ENC_ISO_8859_4 = 0x00000010

    # #define ENC_ISO_8859_5           0x00000012
    ENC_ISO_8859_5 = 0x00000012

    # #define ENC_ISO_8859_6           0x00000014
    ENC_ISO_8859_6 = 0x00000014

    # #define ENC_ISO_8859_7           0x00000016
    ENC_ISO_8859_7 = 0x00000016

    # #define ENC_ISO_8859_8           0x00000018
    ENC_ISO_8859_8 = 0x00000018

    # #define ENC_ISO_8859_9           0x0000001A
    ENC_ISO_8859_9 = 0x0000001A

    # #define ENC_ISO_8859_10          0x0000001C
    ENC_ISO_8859_10 = 0x0000001C

    # #define ENC_ISO_8859_11          0x0000001E
    ENC_ISO_8859_11 = 0x0000001E

    # #define ENC_ISO_8859_13          0x00000022
    ENC_ISO_8859_13 = 0x00000022

    # #define ENC_ISO_8859_14          0x00000024
    ENC_ISO_8859_14 = 0x00000024

    # #define ENC_ISO_8859_15          0x00000026
    ENC_ISO_8859_15 = 0x00000026

    # #define ENC_ISO_8859_16          0x00000028
    ENC_ISO_8859_16 = 0x00000028

    # #define ENC_WINDOWS_1250         0x0000002A
    ENC_WINDOWS_1250 = 0x0000002A

    # #define ENC_3GPP_TS_23_038_7BITS 0x0000002C
    ENC_3GPP_TS_23_038_7BITS = 0x0000002C

    # #define ENC_EBCDIC               0x0000002E
    ENC_EBCDIC = 0x0000002E

    # #define ENC_MAC_ROMAN            0x00000030
    ENC_MAC_ROMAN = 0x00000030

    # #define ENC_CP437                0x00000032
    ENC_CP437 = 0x00000032

    # #define ENC_ASCII_7BITS          0x00000034
    ENC_ASCII_7BITS = 0x00000034

    # #define ENC_T61                  0x00000036
    ENC_T61 = 0x00000036

    # #define ENC_EBCDIC_CP037         0x00000038
    ENC_EBCDIC_CP037 = 0x00000038

    # #define ENC_WINDOWS_1252         0x0000003A
    ENC_WINDOWS_1252 = 0x0000003A

    # #define ENC_WINDOWS_1251         0x0000003C
    ENC_WINDOWS_1251 = 0x0000003C

    # #define ENC_CP855                0x0000003E
    ENC_CP855 = 0x0000003E

    # #define ENC_CP866                0x00000040
    ENC_CP866 = 0x00000040

    # #define ENC_ISO_646_BASIC        0x00000042
    ENC_ISO_646_BASIC = 0x00000042

    # #define ENC_NA          0x00000000
    ENC_NA = 0x00000000

    # #define ENC_STR_NUM     0x01000000
    ENC_STR_NUM = 0x01000000

    # #define ENC_STR_HEX     0x02000000
    ENC_STR_HEX = 0x02000000

    # #define ENC_STRING      0x03000000
    ENC_STRING = 0x03000000

    # #define ENC_STR_MASK    0x0000FFFE
    ENC_STR_MASK = 0x0000FFFE

    # #define ENC_NUM_PREF    0x00200000
    ENC_NUM_PREF = 0x00200000

    # #define ENC_VARINT_PROTOBUF      0x00000002
    ENC_VARINT_PROTOBUF = 0x00000002

    # #define ENC_VARINT_QUIC          0x00000004
    ENC_VARINT_QUIC = 0x00000004

    # #define ENC_VARINT_ZIGZAG        0x00000008
    ENC_VARINT_ZIGZAG = 0x00000008

    # #define ENC_VARIANT_MASK         (ENC_VARINT_PROTOBUF|ENC_VARINT_QUIC|ENC_VARINT_ZIGZAG)
    ENC_VARIANT_MASK = (ENC_VARINT_PROTOBUF |
                        ENC_VARINT_QUIC | ENC_VARINT_ZIGZAG)

    # #define ENC_SEP_NONE    0x00010000
    ENC_SEP_NONE = 0x00010000

    # #define ENC_SEP_COLON   0x00020000
    ENC_SEP_COLON = 0x00020000

    # #define ENC_SEP_DASH    0x00040000
    ENC_SEP_DASH = 0x00040000

    # #define ENC_SEP_DOT     0x00080000
    ENC_SEP_DOT = 0x00080000

    # #define ENC_SEP_SPACE   0x00100000
    ENC_SEP_SPACE = 0x00100000

    # #define ENC_SEP_MASK    0x001F0000
    ENC_SEP_MASK = 0x001F0000

    # #define ENC_ISO_8601_DATE       0x00010000
    ENC_ISO_8601_DATE = 0x00010000

    # #define ENC_ISO_8601_TIME       0x00020000
    ENC_ISO_8601_TIME = 0x00020000

    # #define ENC_ISO_8601_DATE_TIME  0x00030000
    ENC_ISO_8601_DATE_TIME = 0x00030000

    # #define ENC_RFC_822             0x00040000
    ENC_RFC_822 = 0x00040000

    # #define ENC_RFC_1123            0x00080000
    ENC_RFC_1123 = 0x00080000

    # #define ENC_STR_TIME_MASK       0x000F0000
    ENC_STR_TIME_MASK = 0x000F0000

    # #define FIELD_DISPLAY_E_MASK 0xFF
    FIELD_DISPLAY_E_MASK = 0xFF

    # typedef enum {
    #     BASE_NONE    = 0,
    #     BASE_DEC     = 1,
    #     BASE_HEX     = 2,
    #     BASE_OCT     = 3,
    #     BASE_DEC_HEX = 4,
    #     BASE_HEX_DEC = 5,
    #     BASE_CUSTOM  = 6,
    #     BASE_FLOAT   = BASE_NONE,
    #     STR_ASCII    = 0,
    #     STR_UNICODE  = 7,
    #     SEP_DOT      = 8,
    #     SEP_DASH     = 9,
    #     SEP_COLON    = 10,
    #     SEP_SPACE    = 11,
    #     BASE_NETMASK = 12,
    #     BASE_PT_UDP  = 13,
    #     BASE_PT_TCP  = 14,
    #     BASE_PT_DCCP = 15,
    #     BASE_PT_SCTP = 16,
    #     BASE_OUI     = 17
    # } field_display_e;
    field_display_e = c_int
    BASE_NONE = c_int(0)
    BASE_DEC = c_int(1)
    BASE_HEX = c_int(2)
    BASE_OCT = c_int(3)
    BASE_DEC_HEX = c_int(4)
    BASE_HEX_DEC = c_int(5)
    BASE_CUSTOM = c_int(6)
    BASE_FLOAT = BASE_NONE
    STR_ASCII = c_int(0)
    STR_UNICODE = c_int(7)
    SEP_DOT = c_int(8)
    SEP_DASH = c_int(9)
    SEP_COLON = c_int(10)
    SEP_SPACE = c_int(11)
    BASE_NETMASK = c_int(12)
    BASE_PT_UDP = c_int(13)
    BASE_PT_TCP = c_int(14)
    BASE_PT_DCCP = c_int(15)
    BASE_PT_SCTP = c_int(16)
    BASE_OUI = c_int(17)

    # #define BASE_RANGE_STRING         0x00000100
    BASE_RANGE_STRING = 0x00000100

    # #define BASE_EXT_STRING           0x00000200
    BASE_EXT_STRING = 0x00000200

    # #define BASE_VAL64_STRING         0x00000400
    BASE_VAL64_STRING = 0x00000400

    # #define BASE_ALLOW_ZERO           0x00000800
    BASE_ALLOW_ZERO = 0x00000800

    # #define BASE_UNIT_STRING          0x00001000
    BASE_UNIT_STRING = 0x00001000

    # #define BASE_NO_DISPLAY_VALUE     0x00002000
    BASE_NO_DISPLAY_VALUE = 0x00002000

    # #define BASE_PROTOCOL_INFO        0x00004000
    BASE_PROTOCOL_INFO = 0x00004000

    # #define BASE_SPECIAL_VALS         0x00008000
    BASE_SPECIAL_VALS = 0x00008000

    # #define BASE_SHOW_ASCII_PRINTABLE 0x00010000
    BASE_SHOW_ASCII_PRINTABLE = 0x00010000

    # typedef enum {
    #     HF_REF_TYPE_NONE,
    #     HF_REF_TYPE_INDIRECT,
    #     HF_REF_TYPE_DIRECT
    # } hf_ref_type;
    hf_ref_type = c_int
    HF_REF_TYPE_NONE = c_int(0)
    HF_REF_TYPE_INDIRECT = c_int(1)
    HF_REF_TYPE_DIRECT = c_int(2)

    # typedef struct _header_field_info header_field_info;

    class _header_field_info(Structure):
        pass

    header_field_info = _header_field_info

    # struct _header_field_info {
    #     const char        *name;
    #     const char        *abbrev;
    #     enum ftenum        type;
    #     int                display;
    #     const void        *strings;
    #     guint64            bitmask;
    #     const char        *blurb;
    #     int                id;
    #     int                parent;
    #     hf_ref_type        ref_type;
    #     int                same_name_prev_id;
    #     header_field_info *same_name_next;
    # };
    _header_field_info._fields_ = [('name', c_char_p),
                                   ('abbrev', c_char_p),
                                   ('type', ftenum),
                                   ('display', c_int),
                                   ('strings', c_void_p),
                                   ('bitmask', LibGLib2.guint64),
                                   ('blurb', c_char_p),
                                   ('id', c_int),
                                   ('parent', c_int),
                                   ('ref_type', hf_ref_type),
                                   ('same_name_prev_id', c_int),
                                   ('same_name_next', POINTER(header_field_info))]

    # typedef struct hf_register_info {
    #     int               *p_id;
    #     header_field_info  hfinfo;
    # } hf_register_info;

    class hf_register_info(Structure):
        pass

    hf_register_info._fields_ = [('p_id', POINTER(c_int)),
                                 ('hfinfo', header_field_info)]

    # typedef struct _item_label_t {
    #     char representation[ITEM_LABEL_LENGTH];
    # } item_label_t;

    class _item_label_t(Structure):
        pass

    _item_label_t._fields_ = [('representation', c_char * ITEM_LABEL_LENGTH)]

    item_label_t = _item_label_t

    # typedef struct field_info {
    #     header_field_info   *hfinfo;
    #     gint                 start;
    #     gint                 length;
    #     gint                 appendix_start;
    #     gint                 appendix_length;
    #     gint                 tree_type;
    #     guint32              flags;
    #     item_label_t        *rep;
    #     tvbuff_t            *ds_tvb;
    #     fvalue_t             value;
    # } field_info;

    class field_info(Structure):
        pass

    field_info._fields_ = [('hfinfo', POINTER(header_field_info)),
                           ('start', LibGLib2.gint),
                           ('length', LibGLib2.gint),
                           ('appendix_start', LibGLib2.gint),
                           ('appendix_length', LibGLib2.gint),
                           ('tree_type', LibGLib2.gint),
                           ('flags', LibGLib2.guint32),
                           ('rep', POINTER(item_label_t)),
                           ('ds_tvb', POINTER(tvbuff_t)),
                           ('value', fvalue_t)]

    # typedef struct {
    #     guint  crumb_bit_offset;
    #     guint8 crumb_bit_length;
    # } crumb_spec_t;

    class crumb_spec_t(Structure):
        _fields_ = [('crumb_bit_offset', LibGLib2.guint),
                    ('crumb_bit_length', LibGLib2.guint8)]

    # #define FI_HIDDEN               0x00000001
    FI_HIDDEN = 0x00000001

    # #define FI_GENERATED            0x00000002
    FI_GENERATED = 0x00000002

    # #define FI_URL                  0x00000004
    FI_URL = 0x00000004

    # #define FI_LITTLE_ENDIAN        0x00000008
    FI_LITTLE_ENDIAN = 0x00000008

    # #define FI_BIG_ENDIAN           0x00000010
    FI_BIG_ENDIAN = 0x00000010

    # #define FI_VARINT               0x00004000
    FI_VARINT = 0x00004000

    # typedef struct {
    #     GHashTable          *interesting_hfids;
    #     gboolean             visible;
    #     gboolean             fake_protocols;
    #     gint                 count;
    #     struct _packet_info *pinfo;
    # } tree_data_t;

    class tree_data_t(Structure):
        pass

    tree_data_t._fields_ = [
        ('interesting_hfids',
         POINTER(
             LibGLib2.GHashTable)),
        ('visible',
         LibGLib2.gboolean),
        ('fake_protocols',
         LibGLib2.gboolean),
        ('count',
         LibGLib2.gint),
        ('pinfo',
         POINTER(_packet_info))]

    # typedef struct _proto_node {
    #     struct _proto_node *first_child;
    #     struct _proto_node *last_child;
    #     struct _proto_node *next;
    #     struct _proto_node *parent;
    #     field_info         *finfo;
    #     tree_data_t        *tree_data;
    # } proto_node;

    class _proto_node(Structure):
        pass

    _proto_node._fields_ = [('first_child', POINTER(_proto_node)),
                            ('last_child', POINTER(_proto_node)),
                            ('next', POINTER(_proto_node)),
                            ('parent', POINTER(_proto_node)),
                            ('finfo', POINTER(field_info)),
                            ('tree_data', POINTER(tree_data_t))]

    proto_node = _proto_node

    # typedef proto_node proto_tree;
    proto_tree = proto_node

    # typedef proto_node proto_item;
    proto_item = proto_node

    # #define PI_SEVERITY_MASK        0x00F00000
    PI_SEVERITY_MASK = 0x00F00000

    # #define PI_COMMENT              0x00100000
    PI_COMMENT = 0x00100000

    # #define PI_CHAT                 0x00200000
    PI_CHAT = 0x00200000

    # #define PI_NOTE                 0x00400000
    PI_NOTE = 0x00400000

    # #define PI_WARN                 0x00600000
    PI_WARN = 0x00600000

    # #define PI_ERROR                0x00800000
    PI_ERROR = 0x00800000

    # #define PI_GROUP_MASK           0xFF000000
    PI_GROUP_MASK = 0xFF000000

    # #define PI_CHECKSUM             0x01000000
    PI_CHECKSUM = 0x01000000

    # #define PI_SEQUENCE             0x02000000
    PI_SEQUENCE = 0x02000000

    # #define PI_RESPONSE_CODE        0x03000000
    PI_RESPONSE_CODE = 0x03000000

    # #define PI_REQUEST_CODE         0x04000000
    PI_REQUEST_CODE = 0x04000000

    # #define PI_UNDECODED            0x05000000
    PI_UNDECODED = 0x05000000

    # #define PI_REASSEMBLE           0x06000000
    PI_REASSEMBLE = 0x06000000

    # #define PI_MALFORMED            0x07000000
    PI_MALFORMED = 0x07000000

    # #define PI_DEBUG                0x08000000
    PI_DEBUG = 0x08000000

    # #define PI_PROTOCOL             0x09000000
    PI_PROTOCOL = 0x09000000

    # #define PI_SECURITY             0x0a000000
    PI_SECURITY = 0x0a000000

    # #define PI_COMMENTS_GROUP       0x0b000000
    PI_COMMENTS_GROUP = 0x0b000000

    # #define PI_DECRYPTION           0x0c000000
    PI_DECRYPTION = 0x0c000000

    # #define PI_ASSUMPTION           0x0d000000
    PI_ASSUMPTION = 0x0d000000

    # #define PI_DEPRECATED           0x0e000000
    PI_DEPRECATED = 0x0e000000

    # typedef void (*proto_tree_foreach_func)(proto_node *, gpointer);
    proto_tree_foreach_func = CFUNCTYPE(
        None, POINTER(proto_node), LibGLib2.gpointer)

    # typedef gboolean (*proto_tree_traverse_func)(proto_node *, gpointer);
    proto_tree_traverse_func = CFUNCTYPE(
        LibGLib2.gboolean,
        POINTER(proto_node),
        LibGLib2.gpointer)

    # typedef struct {
    #     void (*register_protoinfo)(void);
    #     void (*register_handoff)(void);
    # } proto_plugin;

    class proto_plugin(Structure):
        _fields_ = [('register_protoinfo', CFUNCTYPE(None)),
                    ('register_handoff', CFUNCTYPE(None))]

    # typedef void (*prefix_initializer_t)(const char* match);
    prefix_initializer_t = CFUNCTYPE(None, c_char_p)

    # #define BMT_NO_FLAGS    0x00
    BMT_NO_FLAGS = 0x00

    # #define BMT_NO_APPEND   0x01
    BMT_NO_APPEND = 0x01

    # #define BMT_NO_INT      0x02
    BMT_NO_INT = 0x02

    # #define BMT_NO_FALSE    0x04
    BMT_NO_FALSE = 0x04

    # #define BMT_NO_TFS      0x08
    BMT_NO_TFS = 0x08

    # typedef enum {
    #     PROTO_CHECKSUM_E_BAD = 0,
    #     PROTO_CHECKSUM_E_GOOD,
    #     PROTO_CHECKSUM_E_UNVERIFIED,
    #     PROTO_CHECKSUM_E_NOT_PRESENT
    # } proto_checksum_enum_e;
    proto_checksum_enum_e = c_int
    PROTO_CHECKSUM_E_BAD = c_int(0)
    PROTO_CHECKSUM_E_GOOD = c_int(1)
    PROTO_CHECKSUM_E_UNVERIFIED = c_int(2)
    PROTO_CHECKSUM_E_NOT_PRESENT = c_int(3)

    # #define PROTO_CHECKSUM_NO_FLAGS     0x00
    PROTO_CHECKSUM_NO_FLAGS = 0x00

    # #define PROTO_CHECKSUM_VERIFY       0x01
    PROTO_CHECKSUM_VERIFY = 0x01

    # #define PROTO_CHECKSUM_GENERATED    0x02
    PROTO_CHECKSUM_GENERATED = 0x02

    # #define PROTO_CHECKSUM_IN_CKSUM     0x04
    PROTO_CHECKSUM_IN_CKSUM = 0x04

    # #define PROTO_CHECKSUM_ZERO         0x08
    PROTO_CHECKSUM_ZERO = 0x08

    # #define PROTO_CHECKSUM_NOT_PRESENT  0x10
    PROTO_CHECKSUM_NOT_PRESENT = 0x10

    # struct epan_column_info;

    class epan_column_info(Structure):
        _fields_ = []

    # typedef struct epan_column_info column_info;
    column_info = epan_column_info

    # enum {
    #   COL_8021Q_VLAN_ID,
    #   COL_ABS_YMD_TIME,
    #   COL_ABS_YDOY_TIME,
    #   COL_ABS_TIME,
    #   COL_VSAN,
    #   COL_CUMULATIVE_BYTES,
    #   COL_CUSTOM,
    #   COL_DCE_CALL,
    #   COL_DELTA_TIME,
    #   COL_DELTA_TIME_DIS,
    #   COL_RES_DST,
    #   COL_UNRES_DST,
    #   COL_RES_DST_PORT,
    #   COL_UNRES_DST_PORT,
    #   COL_DEF_DST,
    #   COL_DEF_DST_PORT,
    #   COL_EXPERT,
    #   COL_IF_DIR,
    #   COL_FREQ_CHAN,
    #   COL_DEF_DL_DST,
    #   COL_DEF_DL_SRC,
    #   COL_RES_DL_DST,
    #   COL_UNRES_DL_DST,
    #   COL_RES_DL_SRC,
    #   COL_UNRES_DL_SRC,
    #   COL_RSSI,
    #   COL_TX_RATE,
    #   COL_DSCP_VALUE,
    #   COL_INFO,
    #   COL_RES_NET_DST,
    #   COL_UNRES_NET_DST,
    #   COL_RES_NET_SRC,
    #   COL_UNRES_NET_SRC,
    #   COL_DEF_NET_DST,
    #   COL_DEF_NET_SRC,
    #   COL_NUMBER,
    #   COL_PACKET_LENGTH,
    #   COL_PROTOCOL,
    #   COL_REL_TIME,
    #   COL_DEF_SRC,
    #   COL_DEF_SRC_PORT,
    #   COL_RES_SRC,
    #   COL_UNRES_SRC,
    #   COL_RES_SRC_PORT,
    #   COL_UNRES_SRC_PORT,
    #   COL_TEI,
    #   COL_UTC_YMD_TIME,
    #   COL_UTC_YDOY_TIME,
    #   COL_UTC_TIME,
    #   COL_CLS_TIME,
    #   NUM_COL_FMTS
    # };
    COL_8021Q_VLAN_ID = c_int(0)
    COL_ABS_YMD_TIME = c_int(1)
    COL_ABS_YDOY_TIME = c_int(2)
    COL_ABS_TIME = c_int(3)
    COL_VSAN = c_int(4)
    COL_CUMULATIVE_BYTES = c_int(5)
    COL_CUSTOM = c_int(6)
    COL_DCE_CALL = c_int(7)
    COL_DELTA_TIME = c_int(8)
    COL_DELTA_TIME_DIS = c_int(9)
    COL_RES_DST = c_int(10)
    COL_UNRES_DST = c_int(11)
    COL_RES_DST_PORT = c_int(12)
    COL_UNRES_DST_PORT = c_int(13)
    COL_DEF_DST = c_int(14)
    COL_DEF_DST_PORT = c_int(15)
    COL_EXPERT = c_int(16)
    COL_IF_DIR = c_int(17)
    COL_FREQ_CHAN = c_int(18)
    COL_DEF_DL_DST = c_int(19)
    COL_DEF_DL_SRC = c_int(20)
    COL_RES_DL_DST = c_int(21)
    COL_UNRES_DL_DST = c_int(22)
    COL_RES_DL_SRC = c_int(23)
    COL_UNRES_DL_SRC = c_int(24)
    COL_RSSI = c_int(25)
    COL_TX_RATE = c_int(26)
    COL_DSCP_VALUE = c_int(27)
    COL_INFO = c_int(28)
    COL_RES_NET_DST = c_int(29)
    COL_UNRES_NET_DST = c_int(30)
    COL_RES_NET_SRC = c_int(31)
    COL_UNRES_NET_SRC = c_int(32)
    COL_DEF_NET_DST = c_int(33)
    COL_DEF_NET_SRC = c_int(34)
    COL_NUMBER = c_int(35)
    COL_PACKET_LENGTH = c_int(36)
    COL_PROTOCOL = c_int(37)
    COL_REL_TIME = c_int(38)
    COL_DEF_SRC = c_int(39)
    COL_DEF_SRC_PORT = c_int(40)
    COL_RES_SRC = c_int(41)
    COL_UNRES_SRC = c_int(42)
    COL_RES_SRC_PORT = c_int(43)
    COL_UNRES_SRC_PORT = c_int(44)
    COL_TEI = c_int(45)
    COL_UTC_YMD_TIME = c_int(46)
    COL_UTC_YDOY_TIME = c_int(47)
    COL_UTC_TIME = c_int(48)
    COL_CLS_TIME = c_int(49)
    NUM_COL_FMTS = c_int(50)

    # #define COL_ADD_LSTR_TERMINATOR (const char *) -1
    COL_ADD_LSTR_TERMINATOR = cast(c_void_p(-1), c_char_p)

    # typedef struct unit_name_string {
    #     char *singular;
    #     char *plural;
    # } unit_name_string;

    class unit_name_string(Structure):
        _fields_ = [('singular', c_char_p), ('plural', c_char_p)]

    # struct epan_range;

    class epan_range(Structure):
        _fields_ = []

    # struct dissector_handle;

    class dissector_handle(Structure):
        _fields_ = []

    # typedef struct dissector_handle *dissector_handle_t;
    dissector_handle_t = POINTER(dissector_handle)

    # struct dissector_table;

    class dissector_table(Structure):
        _fields_ = []

    # typedef struct dissector_table *dissector_table_t;
    dissector_table_t = POINTER(dissector_table)

    # typedef int (*dissector_t)(tvbuff_t *, packet_info *, proto_tree *, void
    # *);
    dissector_t = CFUNCTYPE(c_int, POINTER(tvbuff_t),
                            POINTER(packet_info),
                            POINTER(proto_tree),
                            c_void_p)

    # typedef int (*dissector_cb_t)(tvbuff_t *, packet_info *, proto_tree *,
    # void *, void *);
    dissector_cb_t = CFUNCTYPE(c_int, POINTER(tvbuff_t),
                               POINTER(packet_info),
                               POINTER(proto_tree),
                               c_void_p,
                               c_void_p)

    # typedef gboolean (*heur_dissector_t)(tvbuff_t *tvb, packet_info *pinfo,
    # 	proto_tree *tree, void *);
    heur_dissector_t = CFUNCTYPE(LibGLib2.gboolean, POINTER(tvbuff_t),
                                 POINTER(packet_info),
                                 POINTER(proto_tree),
                                 c_void_p)

    # typedef enum {
    #     HEURISTIC_DISABLE,
    #     HEURISTIC_ENABLE
    # } heuristic_enable_e;
    heuristic_enable_e = c_int
    HEURISTIC_DISABLE = c_int(0)
    HEURISTIC_ENABLE = c_int(1)

    # typedef void (*DATFunc) (const gchar *table_name, ftenum_t selector_type,
    #     gpointer key, gpointer value, gpointer user_data);
    DATFunc = CFUNCTYPE(
        None,
        LibGLib2.gchar_p,
        ftenum_t,
        LibGLib2.gpointer,
        LibGLib2.gpointer,
        LibGLib2.gpointer)

    # typedef void (*DATFunc_handle) (const gchar *table_name, gpointer value,
    #     gpointer user_data);
    DATFunc_handle = CFUNCTYPE(
        None,
        LibGLib2.gchar_p,
        LibGLib2.gpointer,
        LibGLib2.gpointer)

    # typedef void (*DATFunc_table) (const gchar *table_name, const gchar *ui_name,
    #     gpointer user_data);
    DATFunc_table = CFUNCTYPE(
        None,
        LibGLib2.gchar_p,
        LibGLib2.gchar_p,
        LibGLib2.gpointer)

    # typedef struct dtbl_entry dtbl_entry_t;

    class dtbl_entry(Structure):
        _fields_ = []

    dtbl_entry_t = dtbl_entry

    # typedef struct _guid_key {
    #     e_guid_t guid;
    #     guint16 ver;
    # } guid_key;

    class _guid_key(Structure):
        pass

    _guid_key._fields_ = [('guid', e_guid_t),
                          ('ver', LibGLib2.guint16)]

    guid_key = _guid_key

    # struct heur_dissector_list;

    class heur_dissector_list(Structure):
        _fields_ = []

    # typedef struct heur_dissector_list *heur_dissector_list_t;
    heur_dissector_list_t = POINTER(heur_dissector_list)

    # typedef struct heur_dtbl_entry {
    # 	heur_dissector_t dissector;
    # 	protocol_t *protocol;
    # 	gchar *list_name;
    # 	const gchar *display_name;
    # 	gchar *short_name;
    # 	gboolean enabled;
    # } heur_dtbl_entry_t;

    class heur_dtbl_entry(Structure):
        pass

    heur_dtbl_entry._fields_ = [('dissector', heur_dissector_t),
                                ('protocol', protocol_t),
                                ('list_name', LibGLib2.gchar_p),
                                ('display_name', LibGLib2.gchar_p),
                                ('short_name', LibGLib2.gchar_p),
                                ('enabled', LibGLib2.gboolean)]

    heur_dtbl_entry_t = heur_dtbl_entry

    # typedef void (*DATFunc_heur) (const gchar *table_name,
    #     struct heur_dtbl_entry *entry, gpointer user_data);
    DATFunc_heur = CFUNCTYPE(
        None,
        LibGLib2.gchar_p,
        POINTER(heur_dtbl_entry),
        LibGLib2.gpointer)

    # typedef void (*DATFunc_heur_table) (const char *table_name,
    #     struct heur_dissector_list *table, gpointer user_data);
    DATFunc_heur_table = CFUNCTYPE(
        None,
        c_char_p,
        POINTER(heur_dissector_list),
        LibGLib2.gpointer)

    # struct depend_dissector_list;

    class depend_dissector_list(Structure):
        _fields_ = []

    # typedef struct depend_dissector_list *depend_dissector_list_t;
    depend_dissector_list_t = POINTER(depend_dissector_list)

    # struct data_source;

    class data_source(Structure):
        _fields_ = []

    # typedef struct frame_data_s {
    #     int file_type_subtype;
    #     const gchar  *pkt_comment;
    #     struct epan_dissect *color_edt;
    # } frame_data_t;

    class frame_data_s(Structure):
        pass

    frame_data_s._fields_ = [('file_type_subtype', c_int),
                             ('pkt_comment', LibGLib2.gchar_p),
                             ('color_edt', POINTER(epan_dissect))]

    frame_data_t = frame_data_s

    # typedef struct file_data_s {
    #     const gchar  *pkt_comment;
    #     struct epan_dissect *color_edt;
    # } file_data_t;

    class file_data_s(Structure):
        pass

    file_data_s._fields_ = [('pkt_comment', LibGLib2.gchar_p),
                            ('color_edt', POINTER(epan_dissect))]

    file_data_t = file_data_s

    # typedef struct ethertype_data_s {
    #     guint16 etype;
    #     int offset_after_ethertype;
    #     proto_tree *fh_tree;
    #     int etype_id;
    #     int trailer_id;
    #     int fcs_len;
    # } ethertype_data_t;

    class ethertype_data_s(Structure):
        pass

    ethertype_data_s._fields_ = [('etype', LibGLib2.guint16),
                                 ('offset_after_ethertype', c_int),
                                 ('fh_tree', POINTER(proto_tree)),
                                 ('etype_id', c_int),
                                 ('trailer_id', c_int),
                                 ('fcs_len', c_int)]

    ethertype_data_t = ethertype_data_s

    # typedef struct _fmt_data {
    #   gchar *title;
    #   int fmt;
    #   gchar *custom_fields;
    #   gint custom_occurrence;
    #   gboolean visible;
    #   gboolean resolved;
    # } fmt_data;

    class _fmt_data(Structure):
        _fields_ = [('title', LibGLib2.gchar_p),
                    ('fmt', c_int),
                    ('custom_fields', LibGLib2.gchar_p),
                    ('custom_occurence', LibGLib2.gint),
                    ('visible', LibGLib2.gboolean),
                    ('resolved', LibGLib2.gboolean)]

    fmt_data = _fmt_data

    # #define GUID_STR_LEN     37
    GUID_STR_LEN = 37

    # #define MAX_ADDR_STR_LEN 256
    MAX_ADDR_STR_LEN = 256

    # #define VINES_ADDR_LEN   6
    VINES_ADDR_LEN = 6

    # #define EUI64_STR_LEN    24
    EUI64_STR_LEN = 24

    # #define AX25_ADDR_LEN    7
    AX25_ADDR_LEN = 7

    # #define FCWWN_ADDR_LEN   8
    FCWWN_ADDR_LEN = 8

    ###########################
    # MACROS/INLINE FUNCTIONS #
    ###########################

    # #define PINFO_FD_VISITED(pinfo)   ((pinfo)->fd->visited)

    def PINFO_FD_VISITED(self, pinfo):
        return pinfo[0].fd[0].visited

    # #define wmem_new(allocator, type) \
    #     ((type*)wmem_alloc((allocator), sizeof(type)))

    def wmem_new(self, allocator, type):
        return cast(self.wmem_alloc(allocator, sizeof(type)), POINTER(type))

    # #define wmem_safe_mult(A, B) \
    #     ((((A) <= 0) || ((B) <= 0) || ((gsize)(A) > (G_MAXSSIZE / (gsize)(B)))) ? 0 : ((A) * (B)))

    def wmem_safe_mult(self, A, B):
        if A.value <= 0 or B.value <= 0 or A.value > LibGLib2.gsize(
                ~(LibGLib2.gsize(0).value)).value / B.value:
            return LibGLib2.gsize(0)
        else:
            return LibGLib2.gsize(A.value * B.value)

    # #define wmem_alloc_array(allocator, type, num) \
    #     ((type*)wmem_alloc((allocator), wmem_safe_mult(sizeof(type), num)))

    def wmem_alloc_array(self, allocator, type, num):
        return cast(
            self.wmem_alloc(
                allocator,
                self.wmem_safe_mult(
                    sizeof(type),
                    num)),
            POINTER(type))

    # #define wmem_new0(allocator, type) \
    #     ((type*)wmem_alloc0((allocator), sizeof(type)))

    def wmem_new0(self, allocator, type):
        return cast(self.wmem_alloc0(allocator, sizeof(type)), POINTER(type))

    # #define wmem_alloc0_array(allocator, type, num) \
    #     ((type*)wmem_alloc0((allocator), wmem_safe_mult(sizeof(type), (num))))

    def wmem_alloc0_array(self, allocator, type, num):
        return cast(
            self.wmem_alloc0(
                allocator,
                self.wmem_safe_mult(
                    sizeof(type),
                    num)),
            POINTER(type))

    # #define wmem_array_append_one(ARRAY, VAL) \
    #     wmem_array_append((ARRAY), &(VAL), 1)

    def wmem_array_append_one(self, ARRAY, VAL):
        self.wmem_array_append(array, byref(VAL), 1)

    # #define wmem_stack_count(X) wmem_list_count(X)

    def wmem_stack_count(self, X):
        self.wmem_list_count(X)

    # #define wmem_stack_push(STACK, DATA) wmem_list_prepend((STACK), (DATA))

    def wmem_stack_push(self, STACK, DATA):
        self.wmem_list_prepend(STACK, DATA)

    # #define wmem_stack_new(ALLOCATOR) wmem_list_new(ALLOCATOR)

    def wmem_stack_new(self, ALLOCATOR):
        return self.wmem_list_new(ALLOCATOR)

    # #define wmem_destroy_stack(STACK) wmem_destroy_list(STACK)

    def wmem_destroy_stack(self, STACK):
        self.wmem_destroy_list(STACK)

    # #define wmem_queue_count(X) wmem_list_count(X)

    def wmem_queue_count(self, X):
        return self.wmem_list_count(X)

    # #define wmem_queue_peek(QUEUE) wmem_stack_peek(QUEUE)

    def wmem_queue_peek(self, QUEUE):
        return self.wmem_stack_peek(QUEUE)

    # #define wmem_queue_pop(QUEUE) wmem_stack_pop(QUEUE)

    def wmem_queue_pop(self, QUEUE):
        return self.wmem_stack_pop(QUEUE)

    # #define wmem_queue_push(QUEUE, DATA) wmem_list_append((QUEUE), (DATA))

    def wmem_queue_push(self, QUEUE, DATA):
        return self.wmem_list_append(QUEUE, DATA)

    # #define wmem_queue_new(ALLOCATOR) wmem_list_new(ALLOCATOR)

    def wmem_queue_new(self, ALLOCATOR):
        return self.wmem_list_new(ALLOCATOR)

    # #define wmem_destroy_queue(QUEUE) wmem_destroy_list(QUEUE)

    def wmem_destroy_queue(self, QUEUE):
        self.wmem_destroy_list(QUEUE)

    # #define wmem_strbuf_new_label(ALLOCATOR) \
    #     wmem_strbuf_sized_new((ALLOCATOR), 0, ITEM_LABEL_LENGTH)

    def wmem_strbuf_new_label(self, ALLOCATOR):
        return self.wmem_strbuf_sized_new(
            ALLOCATOR,
            LibGLib2.gsize(0),
            LibGLib2.gsize(ITEM_LABEL_LENGTH))

    # void wmem_strbuf_append_printf(wmem_strbuf_t *strbuf, const gchar
    # *format, ...);

    def wmem_strbuf_append_printf(self, strbuf, format, *argv):
        args, types = c_va_list(*argv)
        _wmem_strbuf_append_printf = self.dll.wmem_strbuf_append_printf
        _wmem_strbuf_append_printf.restype = None
        _wmem_strbuf_append_printf.argtypes = [
            POINTER(self.wmem_strbuf_t), LibGLib2.gchar_p] + types
        _wmem_strbuf_append_printf(strbuf, format, *args)

    # #define guids_add_uuid(uuid, name) guids_add_guid((const e_guid_t *) (uuid), (name))

    def guids_add_uuid(self, uuid, name):
        self.guids_add_guid(cast(uuid, POINTER(self.e_guid_t)), name)

    # #define guids_get_uuid_name(uuid) guids_get_guid_name((e_guid_t *) (uuid))

    def guids_get_uuid_name(self, uuid):
        self.guids_get_guid_name(cast(uuid, POINTER(self.e_guid_t)))

    # #define guids_resolve_uuid_to_str(uuid) guids_resolve_guid_to_str((e_guid_t *) (uuid))

    def guids_reolve_uuid_to_str(self, uuid):
        self.guids_resolve_guid_to_str(cast(uuid, POINTER(self.e_guid_t)))

    # #define VALUE_STRING_EXT_VS_P(x)           (x)->_vs_p

    def VALUE_STRING_EXT_VS_P(self, x):
        return x[0]._vs_p

    # #define VALUE_STRING_EXT_VS_NUM_ENTRIES(x) (x)->_vs_num_entries

    def VALUE_STRING_EXT_VS_NUM_ENTRIES(self, x):
        return x[0]._vs_num_entries

    # #define VALUE_STRING_EXT_VS_NAME(x)        (x)->_vs_name

    def VALUE_STRING_EXT_VS_NAME(self, x):
        return x[0]._vs_name

    # #define VALUE_STRING_EXT_INIT(x) { _try_val_to_str_ext_init, 0, G_N_ELEMENTS(x)-1, x, #x }

    def VALUE_STRING_EXT_INIT(self, x, name):
        return self.value_string_ext(
            self._try_val_to_str_ext_init, 0, len(x) - 1, x, name)

    # #define VAL64_STRING_EXT_VS_P(x)           (x)->_vs_p

    def VAL64_STRING_EXT_VS_P(self, x):
        return x[0]._vs_p

    # #define VAL64_STRING_EXT_VS_NUM_ENTRIES(x) (x)->_vs_num_entries

    def VAL64_STRING_EXT_VS_NUM_ENTRIES(self, x):
        return x[0]._vs_num_entries

    # #define VAL64_STRING_EXT_VS_NAME(x)        (x)->_vs_name

    def VAL64_STRING_EXT_VS_NAME(self, x):
        return x[0]._vs_name

    # #define VAL64_STRING_EXT_INIT(x) { _try_val64_to_str_ext_init, 0, G_N_ELEMENTS(x)-1, x, #x }

    def VAL64_STRING_EXT_INIT(self, x, name):
        return self.val64_string_ext(
            self._try_val64_to_str_ext_init, 0, len(x) - 1, x, name)

    # #define ADDRESS_INIT(type, len, data) {type, len, data, NULL}

    def ADDRESS_INIT(self, type, len, data):
        return self.address(type, len, cast(data, c_void_p), c_void_p(0))

    # static inline void clear_address(address *addr);

    def clear_address(self, addr):
        addr[0].type = self.AT_NONE
        addr[0].len = c_int(0)
        addr[0].data = c_void_p(0)
        addr[0].priv = c_void_p(0)

    # static inline void set_address(address *addr, int addr_type, int
    # addr_len, const void *addr_data);

    def set_address(self, addr, addr_type, addr_len, addr_data):
        addr[0].type = addr_type
        addr[0].len = addr_len
        addr[0].data = addr_data
        addr[0].priv = c_void_p(0)

    # static inline void set_address_tvb(address *addr, int addr_type, int
    # addr_len, tvbuff_t *tvb, int offset);

    def set_address_tvb(self, addr, addr_type, addr_len, tvb, offset):
        if addr_len.value != 0:
            p = self.tvb_get_ptr(tvb, offset, addr_len)
        else:
            p = c_void_p(0)
        self.set_address(addr, addr_type, addr_len, p)

    # static inline void alloc_address_wmem(wmem_allocator_t *scope, address *addr,
    # int addr_type, int addr_len, const void *addr_data);

    def alloc_address_wmem(self, scope, addr, addr_type, addr_len, addr_data):
        self.clear_address(addr)
        addr[0].type = addr_type
        if addr_len.value != 0:
            addr[0].priv = self.wmem_memdup(scope, addr_data, addr_len)
            addr[0].data = addr[0].priv
            addr[0].len = addr_len

    # static inline void alloc_address_tvb(wmem_allocator_t *scope, address *addr,
    # int addr_type, int addr_len,  tvbuff_t *tvb, int offset);

    def alloc_address_tvb(self, scope, addr, addr_type, addr_len, tvb, offset):
        p = self.tvb_get_ptr(tvb, offset, addr_len)
        self.alloc_address_wmem(scope, addr, addr_type, addr_len, p)

    # static inline int cmp_address(const address *addr1, const address
    # *addr2);

    def cmp_address(self, addr1, addr2):
        if addr1[0].type.value > addr2[0].type:
            return 1
        if addr1[0].type.value < addr2[0].type:
            return -1
        if addr1[0].len.value > addr2[0].len:
            return 1
        if addr1[0].len.value < addr2[0].len:
            return -1
        if addr1[0].len.value == 0:
            return 0
        a1 = cast(addr1[0].data, POINTER(LibGLib2.guint8))
        a2 = cast(addr2[0].data, POINTER(LibGLib2.guint8))
        for i in range(0, addr1[0].len.value):
            if a1[i].value < a2[i].value:
                return -1
            if a1[i].value > a2[i].value:
                return 1
        return 0

    # static inline gboolean addresses_equal(const address *addr1, const
    # address *addr2);

    def addresses_equal(self, addr1, addr2):
        if addr1[0].type.value == addr2[0].type.value and addr1[0].len.value == addr2[0].len.value:
            if addr1[0].len.value == 0:
                return LibGLib2.gboolean(1)
            a1 = cast(addr1[0].data, POINTER(LibGLib2.guint8))
            a2 = cast(addr2[0].data, POINTER(LibGLib2.guint8))
            for i in range(0, addr1[0].len.value):
                if a1[i].value < a2[i].value:
                    return LibGLib2.gboolean(0)
                if a1[i].value > a2[i].value:
                    return LibGLib2.gboolean(0)
            return LibGLib2.gboolean(1)
        return LibGLib2.gboolean(0)

    # static inline gboolean addresses_data_equal(const address *addr1, const
    # address *addr2);

    def addresses_data_equal(self, addr1, addr2):
        if addr1[0].len.value == addr2[0].len.value:
            a1 = cast(addr1[0].data, POINTER(LibGLib2.guint8))
            a2 = cast(addr2[0].data, POINTER(LibGLib2.guint8))
            for i in range(0, addr1[0].len.value):
                if a1[i].value < a2[i].value:
                    return LibGLib2.gboolean(0)
                if a1[i].value > a2[i].value:
                    return LibGLib2.gboolean(0)
            return LibGLib2.gboolean(1)
        return LibGLib2.gboolean(0)

    # static inline void copy_address_shallow(address *to, const address
    # *from);

    def copy_address_shallow(self, to, from_):
        self.set_address(to, from_[0].type, from_[0].len, from_[0].data)

    # static inline void copy_address_wmem(wmem_allocator_t *scope, address
    # *to, const address *from);

    def copy_address_wmem(self, scope, to, from_):
        self.alloc_address_wmem(
            scope,
            to,
            from_[0].type,
            from_[0].len,
            from_[0].data)

    # static inline void copy_address(address *to, const address *from);

    def copy_address(self, to, from_):
        self.copy_address_wmem(POINTER(self.wmem_allocator_t)(0), to, from_)

    # static inline void free_address_wmem(wmem_allocator_t *scope, address
    # *addr);

    def free_address_wmem(self, scope, addr):
        if addr[0].type.value != self.AT_NONE.value and addr[0].len.value > 0 and addr[0].priv.value != c_void_p(
                0):
            self.wmem_free(scope, addr[0].priv)
        self.clear_addresses(addr)

    # static inline void free_address(address *addr);

    def free_address(self, addr):
        self.free_address_wmem(POINTER(self.wmem_allocator_t)(0), addr)

    # static inline guint add_address_to_hash(guint hash_val, const address
    # *addr);

    def add_address_to_hash(self, hash_val, addr):
        hash_data = cast(addr[0].data, POINTER(LibGLib2.guint8))
        for idx in range(0, addr[0].len.value):
            hash_val = LibGLib2.guint(hash_val.value + hash_data[idx].value)
            hash_val = LibGLib2.guint(hash_val.value + (hash_val.value << 10))
            hash_val = LibGLib2.guint(hash_val.value ^ (hash_val.value >> 6))
        return hash_data

    # static inline guint64 add_address_to_hash64(guint64 hash_val, const
    # address *addr);

    def add_address_to_hash64(self, hash_val, addr):
        hash_data = cast(addr[0].data, POINTER(LibGLib2.guint8))
        for idx in range(0, addr[0].len.value):
            hash_val = LibGLib2.guint64(hash_val.value + hash_data[idx].value)
            hash_val = LibGLib2.guint64(
                hash_val.value + (hash_val.value << 10))
            hash_val = LibGLib2.guint64(hash_val.value ^ (hash_val.value >> 6))
        return hash_data

    # #define IS_FT_INT32(ft) \
    # 	((ft) == FT_INT8 ||  \
    # 	 (ft) == FT_INT16 || \
    # 	 (ft) == FT_INT24 || \
    # 	 (ft) == FT_INT32)

    def IS_FT_INT32(self, ft):
        return ft.value == self.FT_INT8.value or ft.value == self.FT_INT16.value or ft.value == self.FT_INT24.value or ft.value == self.FT_INT32.value

    # #define IS_FT_INT64(ft) \
    # 	((ft) == FT_INT40 || \
    # 	 (ft) == FT_INT48 || \
    # 	 (ft) == FT_INT56 || \
    # 	 (ft) == FT_INT64)

    def IS_FT_INT64(self, ft):
        return ft.value == self.FT_INT40.value or ft.value == self.FT_INT48.value or ft.value == self.FT_INT56.value or ft.value == self.FT_INT64.value

    # #define IS_FT_INT(ft) (IS_FT_INT32(ft) || IS_FT_INT64(ft))

    def IS_FT_INT(self, ft):
        return self.IS_FT_INT32(ft) or self.IS_FT_INT64(ft)

    # #define IS_FT_UINT32(ft) \
    # 	((ft) == FT_CHAR ||   \
    # 	 (ft) == FT_UINT8 ||  \
    # 	 (ft) == FT_UINT16 || \
    # 	 (ft) == FT_UINT24 || \
    # 	 (ft) == FT_UINT32 || \
    # 	 (ft) == FT_FRAMENUM)

    def IS_FT_UINT32(self, ft):
        return ft.value == self.FT_CHAR.value or ft.value == self.FT_UINT8.value or ft.value == self.FT_UINT16.value or ft.value == self.FT_UINT24.value or ft.value == self.FT_UINT32.value or ft.value == self.FT_FRAMENUM.value

    # #define IS_FT_UINT64(ft) \
    # 	((ft) == FT_UINT40 || \
    # 	 (ft) == FT_UINT48 || \
    # 	 (ft) == FT_UINT56 || \
    # 	 (ft) == FT_UINT64)

    def IS_FT_UINT64(self, ft):
        return ft.value == self.FT_UINT40.value or ft.value == self.FT_UINT48.value or ft.value == self.FT_UINT56.value or ft.value == self.FT_UINT64.value

    # #define IS_FT_UINT(ft) (IS_FT_UINT32(ft) || IS_FT_UINT64(ft))

    def IS_FT_UINT(self, ft):
        return self.IS_FT_UINT32(ft) or self.IS_FT_UINT64(ft)

    # #define IS_FT_TIME(ft) \
    # 	((ft) == FT_ABSOLUTE_TIME || (ft) == FT_RELATIVE_TIME)

    def IS_FT_TIME(self, ft):
        return ft.value == self.FT_ABSOLUTE_TIME.value or ft.value == self.FT_RELATIVE_TIME.value

    # #define IS_FT_STRING(ft) \
    # 	((ft) == FT_STRING || (ft) == FT_STRINGZ || (ft) == FT_STRINGZPAD)

    def IS_FT_STRING(self, ft):
        return ft.value == self.FT_STRING.value or ft.value == self.FT_STRINGZ.value or ft.value == self.FT_STRINGZPAD.value

    # #define CF_FUNC(x) ((const void *) (gsize) (x))

    def CF_FUNC(self, x):
        return cast(cast(x, LibGLib2.gsize), c_void_p)

    # #define FRAMENUM_TYPE(x) GINT_TO_POINTER(x)

    def FRAMENUM_TYPE(self, x):
        return cast(cast(x, LibGLib2.gsize), LibGLib2.gpointer)

    # void proto_report_dissector_bug(const char *format, ...);

    def proto_report_dissector_bug(self, format, *argv):
        args, types = c_va_list(*argv)
        _proto_report_dissector_bug = self.dll.proto_report_dissector_bug
        _proto_report_dissector_bug.restype = None
        _proto_report_dissector_bug.argtypes = [c_char_p] + types
        _proto_report_dissector_bug(format, *args)

    # #define REPORT_DISSECTOR_BUG(...)  \
    #     proto_report_dissector_bug(__VA_ARGS__)

    def REPORT_DISSECTOR_BUG(self, *args):
        self.proto_report_dissector_bug(*args)

    # #define FIELD_DISPLAY(d) ((d) & FIELD_DISPLAY_E_MASK)

    def FILED_DISPLAY(self, d):
        return type(d)(d.value & self.FILE_DISPLAY_E_MASK)

    # #define IS_BASE_DUAL(b) ((b)==BASE_DEC_HEX||(b)==BASE_HEX_DEC)

    def IS_BASE_DUAL(self, b):
        return b.value == self.BASE_DEC_HEX.value or b.value == self.BASE_HEX_DEC.value

    # #define IS_BASE_PORT(b) (((b)==BASE_PT_UDP||(b)==BASE_PT_TCP||(b)==BASE_PT_DCCP||(b)==BASE_PT_SCTP))

    def IS_BASE_PORT(self, b):
        return b.value == self.BASE_PT_UDP.value or b.value == self.BASE_PT_TCP.value or b.value == self.BASE_PT_DCCP.value or b.value == self.BASE_PT_SCTP.value

    # #define HFILL_INIT(hf)   \
    #     (hf).hfinfo.id                = -1;   \
    #     (hf).hfinfo.parent            = 0;   \
    #     (hf).hfinfo.ref_type          = HF_REF_TYPE_NONE;   \
    #     (hf).hfinfo.same_name_prev_id = -1;   \
    #     (hf).hfinfo.same_name_next    = NULL;

    def HFILL_INIT(self, hf):
        hf.hfinfo.id = c_int(-1)
        hf.hfinfo.parent = c_int(0)
        hf.hfinfo.ref_type = self.HF_REF_TYPE_NONE
        hf.hfinfo.same_name_prev_id = c_int(-1)
        hf.hfinfo.same_name_next = POINTER(self.header_field_info)(0)

    # #define FI_BITS_OFFSET(n)       (((n) & 7) << 5)

    def FI_BITS_OFFSET(self, n):
        return type(n)((n.value & 7) << 5)

    # #define FI_BITS_SIZE(n)         (((n) & 63) << 8)

    def FI_BITS_SIZE(self, n):
        return type(n)((n.value & 63) << 8)

    # #define FI_GET_FLAG(fi, flag)   ((fi) ? ((fi)->flags & (flag)) : 0)

    def FI_GET_FLAG(self, fi, flag):
        if fi.value != 0:
            return type(fi[0].flags)(fi[0].flags & flag.value)
        else:
            return type(fi[0].flags)(0)

    # #define FI_SET_FLAG(fi, flag) \
    #     do { \
    #       if (fi) \
    #         (fi)->flags = (fi)->flags | (flag); \
    #     } while(0)

    def FI_SET_FLAG(self, fi, flag):
        if fi.value != 0:
            fi[0].flags = type(fi[0].flags)(fi[0].flags.value | flag.value)

    # #define FI_RESET_FLAG(fi, flag) \
    #     do { \
    #       if (fi) \
    #         (fi)->flags = (fi)->flags & ~(flag); \
    #     } while(0)

    def FI_RESET_FLAG(self, fi, flag):
        if fi.value != 0:
            fi[0].flags = type(fi[0].flags)(fi[0].flags.value & ~(flag.value))

    # define FI_GET_BITS_OFFSET(fi) (FI_GET_FLAG(fi, FI_BITS_OFFSET(7)) >> 5)

    def FI_GET_BITS_OFFSET(self, fi):
        tmp = self.FI_GET_FLAG(fi, self.FI_BITS_OFFSET(type(fi[0].flags)(7)))
        return type(tmp)(tmp.value >> 5)

    # define FI_GET_BITS_SIZE(fi)   (FI_GET_FLAG(fi, FI_BITS_SIZE(63)) >> 8)

    def FI_GET_BITS_OFFSET(self, fi):
        tmp = self.FI_GET_FLAG(fi, self.FI_BITS_SIZE(type(fi[0].flags)(63)))
        return type(tmp)(tmp.value >> 8)

    # #define PNODE_FINFO(proto_node)  ((proto_node)->finfo)

    def PNODE_FINFO(self, proto_node):
        return proto_node[0].finfo

    # #define PITEM_FINFO(proto_item)  PNODE_FINFO(proto_item)

    def PITEM_FINFO(self, proto_item):
        return self.PNODE_FINFO(proto_item)

    # #define PTREE_FINFO(proto_tree)  PNODE_FINFO(proto_tree)

    def PTREE_FINFO(self, proto_tree):
        return self.PNODE_FINFO(proto_tree)

    # #define PTREE_DATA(proto_tree)   ((proto_tree)->tree_data)

    def PTREE_DATA(self, proto_tree):
        return proto_tree[0].tree_data

    # #define PNODE_POOL(proto_node)   ((proto_node)->tree_data->pinfo->pool)

    def PNODE_POOL(self, proto_node):
        proto_node[0].tree_data[0].pinfo[0].pool

    # static inline gboolean proto_item_is_hidden(proto_item *ti);

    def proto_item_is_hidden(self, ti):
        if ti.value != 0:
            return cast(
                self.FI_GET_FLAG(
                    self.PITEM_FINFO(ti),
                    self.FI_HIDDEN),
                LibGLib2.gboolean)
        return LibGLib2.gboolean(0)

    # #define PROTO_ITEM_IS_HIDDEN(ti) proto_item_is_hidden((ti))

    def PROTO_ITEM_IS_HIDDEN(self, ti):
        return self.proto_item_is_hidden(ti)

    # static inline void proto_item_set_hidden(proto_item *ti);

    def proto_item_set_hidden(self, ti):
        if ti.value != 0:
            self.FI_SET_FLAG(self.PITEM_FINFO(ti), self.FI_HIDDEN)

    # #define PROTO_ITEM_SET_HIDDEN(ti) proto_item_set_hidden((ti))

    def PROTO_ITEM_SET_HIDDEN(self, ti):
        self.proto_item_set_hidden(ti)

    # static inline void proto_item_set_visible(proto_item *ti);

    def proto_item_set_visible(self, ti):
        if ti.value != 0:
            self.FI_RESET_FLAG(self.PITEM_FINFO(ti), self.FI_HIDDEN)

    # #define PROTO_ITEM_SET_VISIBLE(ti) proto_item_set_visible((ti))

    def PROTO_ITEM_SET_VISIBLE(self, ti):
        self.proto_item_set_visible(ti)

    # static inline gboolean proto_item_is_generated(proto_item *ti);

    def proto_item_is_generated(self, ti):
        if ti.value != 0:
            return cast(
                self.FI_GET_FLAG(
                    self.PITEM_FINFO(ti),
                    self.FI_GENERATED),
                LibGLib2.gboolean)
        return LibGLib2.gboolean(0)

    # #define PROTO_ITEM_IS_GENERATED(ti) proto_item_is_generated((ti))

    def PROTO_ITEM_IS_GENERATED(self, ti):
        return self.proto_item_is_generated(ti)

    # static inline void proto_item_set_generated(proto_item *ti);

    def proto_item_set_generated(self, ti):
        if ti.value != 0:
            self.FI_SET_FLAG(self.PITEM_FINFO(ti), self.FI_GENERATED)

    # #define PROTO_ITEM_SET_GENERATED(ti) proto_item_set_generated((ti))

    def PROTO_ITEM_SET_GENERATED(self, ti):
        self.proto_item_set_generated(ti)

    # static inline gboolean proto_item_is_url(proto_item *ti);

    def proto_item_is_url(self, ti):
        if ti.value != 0:
            return cast(
                self.FI_GET_FLAG(
                    self.PITEM_FINFO(ti),
                    self.FI_URL),
                LibGLib2.gboolean)
        return LibGLib2.gboolean(0)

    # #define PROTO_ITEM_IS_URL(ti) proto_item_is_url((ti))

    def PROTO_ITEM_IS_URL(self, ti):
        return self.proto_item_is_url(ti)

    # static inline void proto_item_set_url(proto_item *ti);

    def proto_item_set_url(self, ti):
        if ti.value != 0:
            self.FI_SET_FLAG(self.PITEM_FINFO(ti), self.FI_URL)

    # #define PROTO_ITEM_SET_URL(ti) proto_item_set_url((ti))

    def PROTO_ITEM_SET_URL(self, ti):
        self.proto_item_set_url(ti)

    # void proto_item_set_text(proto_item *ti, const char *format, ...);

    def proto_item_set_text(self, ti, format, *argv):
        args, types = c_va_list(*argv)
        _proto_item_set_text = self.dll.proto_item_set_text
        _proto_item_set_text.restype = None
        _proto_item_set_text.argtypes = [
            POINTER(self.proto_item), c_char_p] + types
        _proto_item_set_text(ti, format, *args)

    # void proto_item_append_text(proto_item *ti, const char *format, ...);

    def proto_item_append_text(self, ti, format, *argv):
        args, types = c_va_list(*argv)
        _proto_item_append_text = self.dll.proto_item_append_text
        _proto_item_append_text.restype = None
        _proto_item_append_text.argtypes = [
            POINTER(self.proto_item), c_char_p] + types
        _proto_item_append_text(ti, format, *args)

    # void proto_item_prepend_text(proto_item *ti, const char *format, ...);

    def proto_item_prepend_text(self, ti, format, *argv):
        args, types = c_va_list(*argv)
        _proto_item_prepend_text = self.dll.proto_item_prepend_text
        _proto_item_prepend_text.restype = None
        _proto_item_prepend_text.argtypes = [
            POINTER(self.proto_item), c_char_p] + types
        _proto_item_prepend_text(ti, format, *args)

    # proto_tree *proto_tree_add_subtree_format(proto_tree *tree, tvbuff_t *tvb, gint start, gint length, gint idx,
    #     proto_item **tree_item, const char *format, ...);

    def proto_tree_add_subtree_format(
            self,
            tree,
            tvb,
            start,
            length,
            idx,
            tree_item,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_subtree_format = self.dll.proto_tree_add_subtree_format
        _proto_tree_add_subtree_format.restype = POINTER(self.proto_tree)
        _proto_tree_add_subtree_format.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.gint, POINTER(
                POINTER(
                    self.proto_item)), c_char_p] + types
        return _proto_tree_add_subtree_format(
            tree, tvb, start, length, idx, tree_item, format, *args)

    # proto_item *proto_tree_add_none_format(proto_tree *tree, const int hfindex, tvbuff_t *tvb, const gint start,
    #     gint length, const char *format, ...);

    def proto_tree_add_none_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_none_format = self.dll.proto_tree_add_none_format
        _proto_tree_add_none_format.restype = POINTER(self.proto_item)
        _proto_tree_add_none_format.argtypes = [POINTER(self.proto_tree),
                                                c_int,
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                c_char_p] + types
        return _proto_tree_add_none_format(
            tree, hfindex, tvb, start, length, format, *args)

    # proto_item *proto_tree_add_protocol_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const char *format, ...);

    def proto_tree_add_protocol_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_protocol_format = self.dll.proto_tree_add_protocol_format
        _proto_tree_add_protocol_format.restype = POINTER(self.proto_item)
        _proto_tree_add_protocol_format.argtypes = [POINTER(self.proto_tree),
                                                    c_int,
                                                    POINTER(self.tvbuff_t),
                                                    LibGLib2.gint,
                                                    LibGLib2.gint,
                                                    c_char_p] + types
        return _proto_tree_add_protocol_format(
            tree, hfindex, tvb, start, length, format, *args)

    # proto_item *proto_tree_add_bytes_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    # gint start, gint length, const guint8* start_ptr, const char *format,
    # ...);

    def proto_tree_add_bytes_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            start_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_bytes_format_value = self.dll.proto_tree_add_bytes_format_value
        _proto_tree_add_bytes_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_bytes_format_value.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, POINTER(
                LibGLib2.guint8), c_char_p] + types
        return _proto_tree_add_bytes_format_value(
            tree, hfindex, tvb, start, length, start_ptr, format, *args)

    # proto_item * proto_tree_add_bytes_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const guint8* start_ptr, const char *format, ...);

    def proto_tree_add_bytes_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            start_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_bytes_format = self.dll.proto_tree_add_bytes_format
        _proto_tree_add_bytes_format.restype = POINTER(self.proto_item)
        _proto_tree_add_bytes_format.argtypes = [POINTER(self.proto_tree),
                                                 c_int,
                                                 POINTER(self.tvbuff_t),
                                                 LibGLib2.gint,
                                                 LibGLib2.gint,
                                                 POINTER(LibGLib2.guint8),
                                                 c_char_p] + types
        return _proto_tree_add_bytes_format(
            tree, hfindex, tvb, start, length, start_ptr, format, *args)

    # proto_item *proto_tree_add_time_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    # gint start, gint length, nstime_t* value_ptr, const char *format, ...);

    def proto_tree_add_time_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_time_format_value = self.dll.proto_tree_add_time_format_value
        _proto_tree_add_time_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_time_format_value.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, POINTER(
                LibWSUtil.nstime_t), c_char_p] + types
        return _proto_tree_add_time_format_value(
            tree, hfindex, tvb, start, length, value_ptr, format, *args)

    # proto_item *proto_tree_add_time_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, nstime_t* value_ptr, const char *format, ...);

    def proto_tree_add_time_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_time_format = self.dll.proto_tree_add_time_format
        _proto_tree_add_time_format.restype = POINTER(self.proto_item)
        _proto_tree_add_time_format.argtypes = [POINTER(self.proto_tree),
                                                c_int,
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                POINTER(LibWSUtil.nstime_t),
                                                c_char_p] + types
        return _proto_tree_add_time_format(
            tree, hfindex, tvb, start, length, value_ptr, format, *args)

    # proto_item *proto_tree_add_ipxnet_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, guint32 value, const char *format, ...);

    def proto_tree_add_ipxnet_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ipxnet_format_value = self.dll.proto_tree_add_ipxnet_format_value
        _proto_tree_add_ipxnet_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_ipxnet_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint32,
            c_char_p] + types
        return _proto_tree_add_ipxnet_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_ipxnet_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, guint32 value, const char *format, ...);

    def proto_tree_add_ipxnet_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ipxnet_format = self.dll.proto_tree_add_ipxnet_format
        _proto_tree_add_ipxnet_format.restype = POINTER(self.proto_item)
        _proto_tree_add_ipxnet_format.argtypes = [POINTER(self.proto_tree),
                                                  c_int,
                                                  POINTER(self.tvbuff_t),
                                                  LibGLib2.gint,
                                                  LibGLib2.gint,
                                                  LibGLib2.guint32,
                                                  c_char_p] + types
        return _proto_tree_add_ipxnet_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_ipv4_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, guint32 value, const char *format, ...);

    def proto_tree_add_ipv4_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ipv4_format_value = self.dll.proto_tree_add_ipv4_format_value
        _proto_tree_add_ipv4_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_ipv4_format_value.argtypes = [POINTER(self.proto_tree),
                                                      c_int,
                                                      POINTER(self.tvbuff_t),
                                                      LibGLib2.gint,
                                                      LibGLib2.gint,
                                                      LibGLib2.guint32,
                                                      c_char_p] + types
        return _proto_tree_add_ipv4_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_ipv4_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, guint32 value, const char *format, ...);

    def proto_tree_add_ipv4_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ipv4_format = self.dll.proto_tree_add_ipv4_format
        _proto_tree_add_ipv4_format.restype = POINTER(self.proto_item)
        _proto_tree_add_ipv4_format.argtypes = [POINTER(self.proto_tree),
                                                c_int,
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                LibGLib2.guint32,
                                                c_char_p] + types
        return _proto_tree_add_ipv4_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_ipv6_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    # gint start, gint length, const ws_in6_addr *value_ptr, const char
    # *format, ...);

    def proto_tree_add_ipv6_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ipv6_format_value = self.dll.proto_tree_add_ipv6_format_value
        _proto_tree_add_ipv6_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_ipv6_format_value.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, POINTER(
                LibWSUtil.ws_in6_addr), c_char_p] + types
        return _proto_tree_add_ipv6_format_value(
            tree, hfindex, tvb, start, length, value_ptr, format, *args)

    # proto_item *proto_tree_add_ipv6_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const ws_in6_addr *value_ptr, const char *format, ...);

    def proto_tree_add_ipv6_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ipv6_format = self.dll.proto_tree_add_ipv6_format
        _proto_tree_add_ipv6_format.restype = POINTER(self.proto_item)
        _proto_tree_add_ipv6_format.argtypes = [POINTER(self.proto_tree),
                                                c_int,
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                POINTER(LibWSUtil.ws_in6_addr),
                                                c_char_p] + types
        return _proto_tree_add_ipv6_format(
            tree, hfindex, tvb, start, length, value_ptr, format, *args)

    # proto_item *proto_tree_add_ether_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    # gint start, gint length, const guint8* value, const char *format, ...);

    def proto_tree_add_ether_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ether_format_value = self.dll.proto_tree_add_ether_format_value
        _proto_tree_add_ether_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_ether_format_value.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, POINTER(
                LibGLib2.guint8), c_char_p] + types
        return _proto_tree_add_ether_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_ether_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const guint8* value, const char *format, ...);

    def proto_tree_add_ether_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_ether_format = self.dll.proto_tree_add_ether_format
        _proto_tree_add_ether_format.restype = POINTER(self.proto_item)
        _proto_tree_add_ether_format.argtypes = [POINTER(self.proto_tree),
                                                 c_int,
                                                 POINTER(self.tvbuff_t),
                                                 LibGLib2.gint,
                                                 LibGLib2.gint,
                                                 POINTER(LibGLib2.guint8),
                                                 c_char_p] + types
        return _proto_tree_add_ether_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_guid_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    # gint start, gint length, const e_guid_t *value_ptr, const char *format,
    # ...);

    def proto_tree_add_guid_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_guid_format_value = self.dll.proto_tree_add_guid_format_value
        _proto_tree_add_guid_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_guid_format_value.argtypes = [POINTER(self.proto_tree),
                                                      c_int,
                                                      POINTER(self.tvbuff_t),
                                                      LibGLib2.gint,
                                                      LibGLib2.gint,
                                                      POINTER(self.e_guid_t),
                                                      c_char_p] + types
        return _proto_tree_add_guid_format_value(
            tree, hfindex, tvb, start, length, value_ptr, format, *args)

    # proto_item *proto_tree_add_guid_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const e_guid_t *value_ptr, const char *format, ...);

    def proto_tree_add_guid_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_guid_format = self.dll.proto_tree_add_guid_format
        _proto_tree_add_guid_format.restype = POINTER(self.proto_item)
        _proto_tree_add_guid_format.argtypes = [POINTER(self.proto_tree),
                                                c_int,
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                POINTER(self.e_guid_t),
                                                c_char_p] + types
        return _proto_tree_add_guid_format(
            tree, hfindex, tvb, start, length, value_ptr, format, *args)

    # proto_item *proto_tree_add_oid_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    # gint start, gint length, const guint8* value_ptr, const char *format,
    # ...);

    def proto_tree_add_oid_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_oid_format_value = self.dll.proto_tree_add_oid_format_value
        _proto_tree_add_oid_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_oid_format_value.argtypes = [POINTER(self.proto_tree),
                                                     c_int,
                                                     POINTER(self.tvbuff_t),
                                                     LibGLib2.gint,
                                                     LibGLib2.gint,
                                                     POINTER(LibGLib2.guint8),
                                                     c_char_p] + types
        return _proto_tree_add_oid_format_value(
            tree, hfindex, tvb, start, length, value_ptr, format, *args)

    # proto_item *proto_tree_add_oid_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const guint8* value_ptr, const char *format, ...);

    def proto_tree_add_oid_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_oid_format = self.dll.proto_tree_add_oid_format
        _proto_tree_add_oid_format.restype = POINTER(self.proto_item)
        _proto_tree_add_oid_format.argtypes = [POINTER(self.proto_tree),
                                               c_int,
                                               POINTER(self.tvbuff_t),
                                               LibGLib2.gint,
                                               LibGLib2.gint,
                                               POINTER(LibGLib2.guint8),
                                               c_char_p] + types
        return _proto_tree_add_oid_format(
            tree,
            hfindex,
            tvb,
            start,
            length,
            value_ptr,
            format,
            *args)

    # proto_item *proto_tree_add_string_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, const char* value, const char *format, ...);

    def proto_tree_add_string_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_string_format_value = self.dll.proto_tree_add_string_format_value
        _proto_tree_add_string_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_string_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            c_char_p,
            c_char_p] + types
        return _proto_tree_add_string_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_string_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const char* value, const char *format, ...);

    def proto_tree_add_string_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_string_format = self.dll.proto_tree_add_string_format
        _proto_tree_add_string_format.restype = POINTER(self.proto_item)
        _proto_tree_add_string_format.argtypes = [POINTER(self.proto_tree),
                                                  c_int,
                                                  POINTER(self.tvbuff_t),
                                                  LibGLib2.gint,
                                                  LibGLib2.gint,
                                                  c_char_p,
                                                  c_char_p] + types
        return _proto_tree_add_string_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_boolean_format_value(proto_tree *tree, int hfindex,
    # tvbuff_t *tvb, gint start, gint length, guint32 value, const char
    # *format, ...);

    def proto_tree_add_boolean_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_boolean_format_value = self.dll.proto_tree_add_boolean_format_value
        _proto_tree_add_boolean_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_boolean_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint32,
            c_char_p] + types
        return _proto_tree_add_boolean_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_boolean_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, guint32 value, const char *format, ...);

    def proto_tree_add_boolean_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_boolean_format = self.dll.proto_tree_add_boolean_format
        _proto_tree_add_boolean_format.restype = POINTER(self.proto_item)
        _proto_tree_add_boolean_format.argtypes = [POINTER(self.proto_tree),
                                                   c_int,
                                                   POINTER(self.tvbuff_t),
                                                   LibGLib2.gint,
                                                   LibGLib2.gint,
                                                   LibGLib2.guint32,
                                                   c_char_p] + types
        return _proto_tree_add_boolean_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_float_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, float value, const char *format, ...);

    def proto_tree_add_float_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_float_format_value = self.dll.proto_tree_add_float_format_value
        _proto_tree_add_float_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_float_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            c_float,
            c_char_p] + types
        return _proto_tree_add_float_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_float_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, float value, const char *format, ...);

    def proto_tree_add_float_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_float_format = self.dll.proto_tree_add_float_format
        _proto_tree_add_float_format.restype = POINTER(self.proto_item)
        _proto_tree_add_float_format.argtypes = [POINTER(self.proto_tree),
                                                 c_int,
                                                 POINTER(self.tvbuff_t),
                                                 LibGLib2.gint,
                                                 LibGLib2.gint,
                                                 c_float,
                                                 c_char_p] + types
        return _proto_tree_add_float_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_double_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, double value, const char *format, ...);

    def proto_tree_add_double_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_double_format_value = self.dll.proto_tree_add_double_format_value
        _proto_tree_add_double_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_double_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            c_double,
            c_char_p] + types
        return _proto_tree_add_double_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_double_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, double value, const char *format, ...);

    def proto_tree_add_double_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_double_format = self.dll.proto_tree_add_double_format
        _proto_tree_add_double_format.restype = POINTER(self.proto_item)
        _proto_tree_add_double_format.argtypes = [POINTER(self.proto_tree),
                                                  c_int,
                                                  POINTER(self.tvbuff_t),
                                                  LibGLib2.gint,
                                                  LibGLib2.gint,
                                                  c_double,
                                                  c_char_p] + types
        return _proto_tree_add_double_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_uint_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, guint32 value, const char *format, ...);

    def proto_tree_add_uint_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_uint_format_value = self.dll.proto_tree_add_uint_format_value
        _proto_tree_add_uint_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_uint_format_value.argtypes = [POINTER(self.proto_tree),
                                                      c_int,
                                                      POINTER(self.tvbuff_t),
                                                      LibGLib2.gint,
                                                      LibGLib2.gint,
                                                      LibGLib2.guint32,
                                                      c_char_p] + types
        return _proto_tree_add_uint_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_uint_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, guint32 value, const char *format, ...);

    def proto_tree_add_uint_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_uint_format = self.dll.proto_tree_add_uint_format
        _proto_tree_add_uint_format.restype = POINTER(self.proto_item)
        _proto_tree_add_uint_format.argtypes = [POINTER(self.proto_tree),
                                                c_int,
                                                POINTER(tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                LibGLib2.guint32,
                                                c_char_p] + types
        return _proto_tree_add_uint_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_uint64_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, guint64 value, const char *format, ...);

    def proto_tree_add_uint64_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_uint64_format_value = self.dll.proto_tree_add_uint64_format_value
        _proto_tree_add_uint64_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_uint64_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint64,
            c_char_p] + types
        return _proto_tree_add_uint64_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_uint64_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, guint64 value, const char *format, ...);

    def proto_tree_add_uint64_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_uint64_format = self.dll.proto_tree_add_uint64_format
        _proto_tree_add_uint64_format.restype = POINTER(self.proto_item)
        _proto_tree_add_uint64_format.argtypes = [POINTER(self.proto_tree),
                                                  c_int,
                                                  POINTER(self.tvbuff_t),
                                                  LibGLib2.gint,
                                                  LibGLib2.gint,
                                                  LibGLib2.guint64,
                                                  c_char_p] + types
        return _proto_tree_add_uint64_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_int_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, gint32 value, const char *format, ...);

    def proto_tree_add_int_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_int_format_value = self.dll.proto_tree_add_int_format_value
        _proto_tree_add_int_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_int_format_value.argtypes = [POINTER(self.proto_tree),
                                                     c_int,
                                                     POINTER(self.tvbuff_t),
                                                     LibGLib2.gint,
                                                     LibGLib2.gint,
                                                     LibGLib2.gint32,
                                                     c_char_p] + types
        return _proto_tree_add_int_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_int_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, gint32 value, const char *format, ...);

    def proto_tree_add_int_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_int_format = self.dll.proto_tree_add_int_format
        _proto_tree_add_int_format.restype = POINTER(self.proto_item)
        _proto_tree_add_int_format.argtypes = [POINTER(self.proto_tree),
                                               c_int,
                                               POINTER(self.tvbuff_t),
                                               LibGLib2.gint,
                                               LibGLib2.gint,
                                               LibGLib2.gint32,
                                               c_char_p] + types
        return _proto_tree_add_int_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_int64_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    #     gint start, gint length, gint64 value, const char *format, ...);

    def proto_tree_add_int64_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_int64_format_value = self.dll.proto_tree_add_int64_format_value
        _proto_tree_add_int64_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_int64_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.gint64,
            c_char_p] + types
        return _proto_tree_add_int64_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_int64_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, gint64 value, const char *format, ...);

    def proto_tree_add_int64_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_int64_format = self.dll.proto_tree_add_int64_format
        _proto_tree_add_int64_format.restype = POINTER(self.proto_item)
        _proto_tree_add_int64_format.argtypes = [POINTER(self.proto_tree),
                                                 c_int,
                                                 POINTER(self.tvbuff_t),
                                                 LibGLib2.gint,
                                                 LibGLib2.gint,
                                                 LibGLib2.gint64,
                                                 c_char_p] + types
        return _proto_tree_add_int64_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_eui64_format_value(proto_tree *tree, int hfindex, tvbuff_t *tvb,
    # gint start, gint length, const guint64 value, const char *format, ...);

    def proto_tree_add_eui64_format_value(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_eui64_format_value = self.dll.proto_tree_add_eui64_format_value
        _proto_tree_add_eui64_format_value.restype = POINTER(self.proto_item)
        _proto_tree_add_eui64_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint64,
            c_char_p] + types
        return _proto_tree_add_eui64_format_value(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_eui64_format(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
    #     gint length, const guint64 value, const char *format, ...);

    def proto_tree_add_eui64_format(
            self,
            tree,
            hfindex,
            tvb,
            start,
            length,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_eui64_format = self.dll.proto_tree_add_eui64_format
        _proto_tree_add_eui64_format.restype = POINTER(self.proto_item)
        _proto_tree_add_eui64_format.argtypes = [POINTER(self.proto_tree),
                                                 c_int,
                                                 POINTER(self.tvbuff_t),
                                                 LibGLib2.gint,
                                                 LibGLib2.gint,
                                                 LibGLib2.guint64,
                                                 c_char_p] + types
        return _proto_tree_add_eui64_format(
            tree, hfindex, tvb, start, length, value, format, *args)

    # proto_item *proto_tree_add_debug_text(proto_tree *tree, const char
    # *format, ...);

    def proto_tree_add_debug_text(self, tree, format, *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_debug_text = self.dll.proto_tree_add_debug_text
        _proto_tree_add_debug_text.restype = POINTER(self.proto_item)
        _proto_tree_add_debug_text.argtypes = [POINTER(self.proto_tree),
                                               c_char_p] + types
        return _proto_tree_add_debug_text(tree, format, *args)

    # proto_item *proto_tree_add_uint_bits_format_value(proto_tree *tree, const int hf_index, tvbuff_t *tvb,
    # const guint bit_offset, const gint no_of_bits, guint32 value, const char
    # *format, ...);

    def proto_tree_add_uint_bits_format_value(
            self,
            tree,
            hf_index,
            tvb,
            bit_offset,
            no_of_bits,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_uint_bits_format_value = self.dll.proto_tree_add_uint_bits_format_value
        _proto_tree_add_uint_bits_format_value.restype = POINTER(
            self.proto_item)
        _proto_tree_add_uint_bits_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.guint,
            LibGLib2.gint,
            LibGLib2.guint32,
            c_char_p] + types
        return _proto_tree_add_uint_bits_format_value(
            tree, hf_inde, tvb, bit_offset, no_of_bits, value, format, *args)

    # proto_item *proto_tree_add_uint64_bits_format_value(proto_tree *tree, const int hf_index, tvbuff_t *tvb,
    # const guint bit_offset, const gint no_of_bits, guint64 value, const char
    # *format, ...);

    def proto_tree_add_uint64_bits_format_value(
            self,
            tree,
            hf_index,
            tvb,
            bit_offset,
            no_of_bits,
            value,
            format,
            *argv):
        args, types = c_va_list(*argv)
        _proto_tree_add_uint64_bits_format_value = self.dll.proto_tree_add_uint64_bits_format_value
        _proto_tree_add_uint64_bits_format_value.restype = POINTER(
            self.proto_item)
        _proto_tree_add_uint64_bits_format_value.argtypes = [
            POINTER(
                self.proto_tree),
            c_int,
            POINTER(
                self.tvbuff_t),
            LibGLib2.guint,
            LibGLib2.gint,
            LibGLib2.guint64,
            c_char_p] + types
        return _proto_tree_add_uint64_bits_format_value(
            tree, hf_index, tvb, bit_offset, no_of_bits, value, format, *args)

    # void col_add_lstr(column_info *cinfo, const gint el, const gchar *str,
    # ...);

    def col_add_lstr(self, cinfo, el, str, *argv):
        args, types = c_va_list(*argv)
        _col_add_lstr = self.dll.col_add_lstr
        _col_add_lstr.restype = None
        _col_add_lstr.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p] + types
        _col_add_lstr(cinfo, el, str * args)

    # void col_add_fstr(column_info *cinfo, const gint col, const gchar
    # *format, ...);

    def col_add_fstr(self, cinfo, col, format, *argv):
        args, types = c_va_list(*argv)
        _col_add_fstr = self.dll.col_add_fstr
        _col_add_fstr.restype = None
        _col_add_fstr.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p] + types
        _col_add_fstr(cinfo, col, format * args)

    # void col_append_lstr(column_info *cinfo, const gint el, const gchar
    # *str, ...);

    def col_append_lstr(self, cinfo, el, str, *argv):
        args, types = c_va_list(*argv)
        _col_append_lstr = self.dll.col_append_lstr
        _col_append_lstr.restype = None
        _col_append_lstr.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p] + types
        _col_append_lstr(cinfo, el, str, *args)

    # void col_append_fstr(column_info *cinfo, const gint col, const gchar
    # *format, ...);

    def col_append_fstr(self, cinfo, col, format, *argv):
        args, types = c_va_list(*argv)
        _col_append_fstr = self.dll.col_append_fstr
        _col_append_fstr.restype = None
        _col_append_fstr.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p] + types
        _col_append_fstr(cinfo, col, format, *args)

    # void col_prepend_fstr(column_info *cinfo, const gint col, const gchar
    # *format, ...);

    def col_prepend_fstr(self, cinfo, col, format, *argv):
        args, types = c_va_list(*argv)
        _col_prepend_fstr = self.dll.col_prepend_fstr
        _col_prepend_fstr.restype = None
        _col_prepend_fstr.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p] + types
        _col_prepend_fstr(cinfo, col, format, *args)

    # void col_prepend_fence_fstr(column_info *cinfo, const gint col, const
    # gchar *format, ...);

    def col_prepend_fence_fstr(self, cinfo, col, format, *argv):
        args, types = c_va_list(*argv)
        _col_prepend_fence_fstr = self.dll.col_prepend_fence_fstr
        _col_prepend_fence_fstr.restype = None
        _col_prepend_fence_fstr.argtypes = [
            POINTER(self.column_info), LibGLib2.gint, LibGLib2.gchar_p] + types
        _col_prepend_fence_fstr(cinfo, col, format, *args)

    # void col_append_sep_fstr(column_info *cinfo, const gint col, const gchar *sep,
    #                          const gchar *format, ...);

    def col_append_sep_fstr(self, cinfo, col, sep, format, *argv):
        args, types = c_va_list(*argv)
        _col_append_sep_fstr = self.dll.col_append_sep_fstr
        _col_append_sep_fstr.restype = None
        _col_append_sep_fstr.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p,
            LibGLib2.gchar_p] + types
        _col_append_sep_fstr(cinfo, col, sep, format, *args)

    # #define hi_nibble(b) (((b) & 0xf0) >> 4)

    def hi_nibble(self, b):
        return type(b)((b.value & 0xF0) >> 4)

    # #define lo_nibble(b) ((b) & 0x0f)

    def lo_nibble(self, b):
        return type(b)(b.value & 0x0F)

    # #define array_length(x)	(sizeof x / sizeof x[0])

    def array_length(self, x):
        return c_size_t(len(x))

    # #define	BYTES_ARE_IN_FRAME(offset, captured_len, len) \
    # 	((guint)(offset) + (guint)(len) > (guint)(offset) && \
    # 	 (guint)(offset) + (guint)(len) <= (guint)(captured_len))

    def BYTES_ARE_IN_FRAME(self, offset, caputred_len, len):
        if offset.value + len.value > offset.value and offset.value + \
                len.value <= caputred_len:
            return LibGLib2.gboolean(1)
        else:
            return LibGLib2.gboolean(0)

    # #define tvb_ether_to_str(tvb, offset) tvb_address_to_str(wmem_packet_scope(), tvb, AT_ETHER, offset)

    def tvb_ether_to_str(self, tvb, offset):
        return self.tvb_address_to_str(
            self.wmem_packet_scope(), tvb, self.AT_ETHER, offset)

    # #define tvb_ip_to_str(tvb, offset) tvb_address_to_str(wmem_packet_scope(), tvb, AT_IPv4, offset)

    def tvb_ip_to_str(self, tvb, offset):
        return self.tvb_address_to_str(
            self.wmem_packet_scope(), tvb, self.AT_IPv4, offset)

    # #define tvb_ip6_to_str(tvb, offset) tvb_address_to_str(wmem_packet_scope(), tvb, AT_IPv6, offset)

    def tvb_ip6_to_str(self, tvb, offset):
        return self.tvb_address_to_str(
            self.wmem_packet_scope(), tvb, self.AT_IPv6, offset)

    # #define tvb_fcwwn_to_str(tvb, offset) tvb_address_to_str(wmem_packet_scope(), tvb, AT_FCWWN, offset)

    def tvb_fcwwn_to_str(self, tvb, offset):
        return self.tvb_address_to_str(
            self.wmem_packet_scope(), tvb, self.AT_FCWWN, offset)

    # #define tvb_fc_to_str(tvb, offset) tvb_address_to_str(wmem_packet_scope(), tvb, AT_FC, offset)

    def tvb_fc_to_str(self, tvb, offset):
        return self.tvb_address_to_str(
            self.wmem_packet_scope(), tvb, self.AT_FC, offset)

    # #define tvb_eui64_to_str(tvb, offset) tvb_address_to_str(wmem_packet_scope(), tvb, AT_EUI64, offset)

    def tvb_eui64_to_str(self, tvb, offset):
        return self.tvb_address_to_str(
            self.wmem_packet_scope(), tvb, self.AT_EUI64, offset)

    def __init__(self, libpath=config.get_libwireshark()):
        libwireshark = CDLL(config.get_libwireshark())

        # void *wmem_alloc(wmem_allocator_t *allocator, const size_t size);
        self.wmem_alloc = libwireshark.wmem_alloc
        self.wmem_alloc.restype = c_void_p
        self.wmem_alloc.argtypes = [POINTER(self.wmem_allocator_t), c_size_t]

        # void *wmem_alloc0(wmem_allocator_t *allocator, const size_t size);
        self.wmem_alloc0 = libwireshark.wmem_alloc0
        self.wmem_alloc0.restype = c_void_p
        self.wmem_alloc0.argtypes = [POINTER(self.wmem_allocator_t), c_size_t]

        # void wmem_free(wmem_allocator_t *allocator, void *ptr);
        self.wmem_free = libwireshark.wmem_free
        self.wmem_free.restype = None
        self.wmem_free.argtypes = [POINTER(self.wmem_allocator_t), c_void_p]

        # void *wmem_realloc(wmem_allocator_t *allocator, void *ptr, const size_t
        # size);
        self.wmem_realloc = libwireshark.wmem_realloc
        self.wmem_realloc.restype = c_void_p
        self.wmem_realloc.argtypes = [
            POINTER(
                self.wmem_allocator_t),
            c_void_p,
            c_size_t]

        # void wmem_free_all(wmem_allocator_t *allocator);
        self.wmem_free_all = libwireshark.wmem_free_all
        self.wmem_free_all.restype = None
        self.wmem_free_all.argtypes = [POINTER(self.wmem_allocator_t)]

        # void wmem_gc(wmem_allocator_t *allocator);
        self.wmem_gc = libwireshark.wmem_gc
        self.wmem_gc.restype = None
        self.wmem_gc.argtypes = [POINTER(self.wmem_allocator_t)]

        # void wmem_destroy_allocator(wmem_allocator_t *allocator);
        self.wmem_destroy_allocator = libwireshark.wmem_destroy_allocator
        self.wmem_destroy_allocator.restype = None
        self.wmem_destroy_allocator.argtypes = [POINTER(self.wmem_allocator_t)]

        # wmem_allocator_t *wmem_allocator_new(const wmem_allocator_type_t
        # type);
        self.wmem_allocator_new = libwireshark.wmem_allocator_new
        self.wmem_allocator_new.restype = POINTER(self.wmem_allocator_t)
        self.wmem_allocator_new.argtypes = [self.wmem_allocator_type_t]

        # void wmem_init(void);
        self.wmem_init = libwireshark.wmem_init
        self.wmem_init.restype = None
        self.wmem_init.argtypes = []

        # void wmem_cleanup(void);
        self.wmem_cleanup = libwireshark.wmem_cleanup
        self.wmem_cleanup.restype = None
        self.wmem_cleanup.argtypes = []

        # wmem_array_t *
        # wmem_array_sized_new(wmem_allocator_t *allocator, gsize elem_size,
        #                      guint alloc_count);
        self.wmem_array_sized_new = libwireshark.wmem_array_sized_new
        self.wmem_array_sized_new.restype = POINTER(self.wmem_array_t)
        self.wmem_array_sized_new.argtypes = [POINTER(self.wmem_allocator_t),
                                              LibGLib2.gsize,
                                              LibGLib2.guint]

        # wmem_array_t *wmem_array_new(wmem_allocator_t *allocator, const gsize
        # elem_size);
        self.wmem_array_new = libwireshark.wmem_array_new
        self.wmem_array_new.restype = POINTER(self.wmem_array_t)
        self.wmem_array_new.argtypes = [
            POINTER(self.wmem_allocator_t), LibGLib2.gsize]

        # void wmem_array_set_null_terminator(wmem_array_t *array);
        self.wmem_array_set_null_terminator = libwireshark.wmem_array_set_null_terminator
        self.wmem_array_set_null_terminator.restype = None
        self.wmem_array_set_null_terminator.argtypes = [
            POINTER(self.wmem_array_t)]

        # void wmem_array_bzero(wmem_array_t *array);
        self.wmem_array_bzero = libwireshark.wmem_array_bzero
        self.wmem_array_bzero.restype = None
        self.wmem_array_bzero.argtypes = [POINTER(self.wmem_array_t)]

        # void wmem_array_append(wmem_array_t *array, const void *in, guint
        # count);
        self.wmem_array_append = libwireshark.wmem_array_append
        self.wmem_array_append.restype = None
        self.wmem_array_append.argtypes = [
            POINTER(self.wmem_array_t), c_void_p, LibGLib2.guint]

        # void *wmem_array_index(wmem_array_t *array, guint array_index);
        self.wmem_array_index = libwireshark.wmem_array_index
        self.wmem_array_index.restype = c_void_p
        self.wmem_array_index.argtypes = [
            POINTER(self.wmem_array_t), LibGLib2.guint]

        # int wmem_array_try_index(wmem_array_t *array, guint array_index, void
        # *val);
        self.wmem_array_try_index = libwireshark.wmem_array_try_index
        self.wmem_array_try_index.restype = c_int
        self.wmem_array_try_index.argtypes = [
            POINTER(self.wmem_array_t), LibGLib2.guint, c_void_p]

        # void wmem_array_sort(wmem_array_t *array, int (*compar)(const
        # void*,const void*));
        self.wmem_array_sort = libwireshark.wmem_array_sort
        self.wmem_array_sort.restype = None
        self.wmem_array_sort.argtypes = [POINTER(self.wmem_array_t),
                                         CFUNCTYPE(c_int, c_void_p, c_void_p)]

        # void *wmem_array_get_raw(wmem_array_t *array);
        self.wmem_array_get_raw = libwireshark.wmem_array_get_raw
        self.wmem_array_get_raw.restype = c_void_p
        self.wmem_array_get_raw.argtypes = [POINTER(self.wmem_array_t)]

        # guint wmem_array_get_count(wmem_array_t *array);
        self.wmem_array_get_count = libwireshark.wmem_array_get_count
        self.wmem_array_get_count.restype = LibGLib2.guint
        self.wmem_array_get_count.argtypes = [POINTER(self.wmem_array_t)]

        # void wmem_destroy_array(wmem_array_t *array);
        #wmem_destroy_array = libwireshark.wmem_destroy_array
        #wmem_destroy_array.restype = None
        #wmem_destroy_array.argtypes = [POINTER(self.wmem_array_t)]

        # guint wmem_list_count(const wmem_list_t *list);
        self.wmem_list_count = libwireshark.wmem_list_count
        self.wmem_list_count.restype = LibGLib2.guint
        self.wmem_list_count.argtypes = [POINTER(self.wmem_list_t)]

        # wmem_list_frame_t *wmem_list_head(const wmem_list_t *list);
        self.wmem_list_head = libwireshark.wmem_list_head
        self.wmem_list_head.restype = POINTER(self.wmem_list_frame_t)
        self.wmem_list_head.argtypes = [POINTER(self.wmem_list_t)]

        # wmem_list_frame_t *wmem_list_tail(const wmem_list_t *list);
        self.wmem_list_tail = libwireshark.wmem_list_tail
        self.wmem_list_tail.restype = POINTER(self.wmem_list_frame_t)
        self.wmem_list_tail.argtypes = [POINTER(self.wmem_list_t)]

        # wmem_list_frame_t *wmem_list_frame_next(const wmem_list_frame_t
        # *frame);
        self.wmem_list_frame_next = libwireshark.wmem_list_frame_next
        self.wmem_list_frame_next.restype = POINTER(self.wmem_list_frame_t)
        self.wmem_list_frame_next.argtypes = [POINTER(self.wmem_list_frame_t)]

        # wmem_list_frame_t *wmem_list_frame_prev(const wmem_list_frame_t
        # *frame);
        self.wmem_list_frame_prev = libwireshark.wmem_list_frame_prev
        self.wmem_list_frame_prev.restype = POINTER(self.wmem_list_frame_t)
        self.wmem_list_frame_prev.argtypes = [POINTER(self.wmem_list_frame_t)]

        # void *wmem_list_frame_data(const wmem_list_frame_t *frame);
        self.wmem_list_frame_data = libwireshark.wmem_list_frame_data
        self.wmem_list_frame_data.restype = c_void_p
        self.wmem_list_frame_data.argtypes = [POINTER(self.wmem_list_frame_t)]

        # void wmem_list_remove(wmem_list_t *list, void *data);
        self.wmem_list_remove = libwireshark.wmem_list_remove
        self.wmem_list_remove.restype = None
        self.wmem_list_remove.argtypes = [POINTER(self.wmem_list_t), c_void_p]

        # void wmem_list_remove_frame(wmem_list_t *list, wmem_list_frame_t
        # *frame);
        self.wmem_list_remove_frame = libwireshark.wmem_list_remove_frame
        self.wmem_list_remove_frame.restype = None
        self.wmem_list_remove_frame.argtypes = [
            POINTER(self.wmem_list_t),
            POINTER(self.wmem_list_frame_t)]

        # wmem_list_frame_t *wmem_list_find(wmem_list_t *list, const void
        # *data);
        self.wmem_list_find = libwireshark.wmem_list_find
        self.wmem_list_find.restype = POINTER(self.wmem_list_frame_t)
        self.wmem_list_find.argtypes = [POINTER(self.wmem_list_t), c_void_p]

        # wmem_list_frame_t *wmem_list_find_custom(wmem_list_t *list, const void
        # *data, GCompareFunc func);
        self.wmem_list_find_custom = libwireshark.wmem_list_find_custom
        self.wmem_list_find_custom.restype = POINTER(self.wmem_list_frame_t)
        self.wmem_list_find_custom.argtypes = [
            POINTER(self.wmem_list_t), c_void_p, LibGLib2.GCompareFunc]

        # void wmem_list_prepend(wmem_list_t *list, void *data);
        self.wmem_list_prepend = libwireshark.wmem_list_prepend
        self.wmem_list_prepend.restype = None
        self.wmem_list_prepend.argtypes = [POINTER(self.wmem_list_t), c_void_p]

        # void wmem_list_append(wmem_list_t *list, void *data);
        self.wmem_list_append = libwireshark.wmem_list_append
        self.wmem_list_append.restype = None
        self.wmem_list_append.argtypes = [POINTER(self.wmem_list_t), c_void_p]

        # void wmem_list_insert_sorted(wmem_list_t *list, void* data, GCompareFunc
        # func);
        self.wmem_list_insert_sorted = libwireshark.wmem_list_insert_sorted
        self.wmem_list_insert_sorted.restype = None
        self.wmem_list_insert_sorted.argtypes = [
            POINTER(self.wmem_list_t), c_void_p, LibGLib2.GCompareFunc]

        # wmem_list_t *wmem_list_new(wmem_allocator_t *allocator);
        self.wmem_list_new = libwireshark.wmem_list_new
        self.wmem_list_new.restype = POINTER(self.wmem_list_t)
        self.wmem_list_new.argtypes = [POINTER(self.wmem_allocator_t)]

        # void wmem_list_foreach(wmem_list_t *list, GFunc foreach_func, gpointer
        # user_data);
        self.wmem_list_foreach = libwireshark.wmem_list_foreach
        self.wmem_list_foreach.restype = None
        self.wmem_list_foreach.argtypes = [
            POINTER(
                self.wmem_list_t),
            LibGLib2.GFunc,
            LibGLib2.gpointer]

        # void wmem_destroy_list(wmem_list_t *list);
        self.wmem_destroy_list = libwireshark.wmem_destroy_list
        self.wmem_destroy_list.restype = None
        self.wmem_destroy_list.argtypes = [POINTER(self.wmem_list_t)]

        # wmem_map_t *wmem_map_new(wmem_allocator_t *allocator,
        #         GHashFunc hash_func, GEqualFunc eql_func);
        self.wmem_map_new = libwireshark.wmem_map_new
        self.wmem_map_new.restype = POINTER(self.wmem_map_t)
        self.wmem_map_new.argtypes = [POINTER(self.wmem_allocator_t),
                                      LibGLib2.GHashFunc,
                                      LibGLib2.GEqualFunc]

        # wmem_map_t *wmem_map_new_autoreset(wmem_allocator_t *master, wmem_allocator_t *slave,
        #         GHashFunc hash_func, GEqualFunc eql_func);
        self.wmem_map_new_autoreset = libwireshark.wmem_map_new_autoreset
        self.wmem_map_new_autoreset.restype = POINTER(self.wmem_map_t)
        self.wmem_map_new_autoreset.argtypes = [POINTER(self.wmem_allocator_t),
                                                POINTER(self.wmem_allocator_t),
                                                LibGLib2.GHashFunc,
                                                LibGLib2.GEqualFunc]

        # void *wmem_map_insert(wmem_map_t *map, const void *key, void *value);
        self.wmem_map_insert = libwireshark.wmem_map_insert
        self.wmem_map_insert.restype = c_void_p
        self.wmem_map_insert.argtypes = [
            POINTER(self.wmem_map_t), c_void_p, c_void_p]

        # gboolean wmem_map_contains(wmem_map_t *map, const void *key);
        self.wmem_map_contains = libwireshark.wmem_map_contains
        self.wmem_map_contains.restype = LibGLib2.gboolean
        self.wmem_map_contains.argtypes = [POINTER(self.wmem_map_t), c_void_p]

        # void *wmem_map_lookup(wmem_map_t *map, const void *key);
        self.wmem_map_lookup = libwireshark.wmem_map_lookup
        self.wmem_map_lookup.restype = c_void_p
        self.wmem_map_lookup.argtypes = [POINTER(self.wmem_map_t), c_void_p]

        # gboolean wmem_map_lookup_extended(wmem_map_t *map, const void *key,
        # const void **orig_key, void **value);
        self.wmem_map_lookup_extended = libwireshark.wmem_map_lookup_extended
        self.wmem_map_lookup_extended.restype = LibGLib2.gboolean
        self.wmem_map_lookup_extended.argtypes = [POINTER(self.wmem_map_t),
                                                  c_void_p,
                                                  POINTER(c_void_p),
                                                  POINTER(c_void_p)]

        # void *wmem_map_remove(wmem_map_t *map, const void *key);
        self.wmem_map_remove = libwireshark.wmem_map_remove
        self.wmem_map_remove.restype = c_void_p
        self.wmem_map_remove.argtypes = [POINTER(self.wmem_map_t), c_void_p]

        # gboolean wmem_map_steal(wmem_map_t *map, const void *key);
        self.wmem_map_steal = libwireshark.wmem_map_steal
        self.wmem_map_steal.restype = LibGLib2.gboolean
        self.wmem_map_steal.argtypes = [POINTER(self.wmem_map_t), c_void_p]

        # wmem_list_t* wmem_map_get_keys(wmem_allocator_t *list_allocator, wmem_map_t *map);
        self.wmem_map_get_keys = libwireshark.wmem_map_get_keys
        self.wmem_map_get_keys.restype = POINTER(self.wmem_list_t)
        self.wmem_map_get_keys.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.wmem_map_t)]

        # void wmem_map_foreach(wmem_map_t *map, GHFunc foreach_func, gpointer
        # user_data);
        self.wmem_map_foreach = libwireshark.wmem_map_foreach
        self.wmem_map_foreach.restype = None
        self.wmem_map_foreach.argtypes = [
            POINTER(
                self.wmem_map_t),
            LibGLib2.GHFunc,
            LibGLib2.gpointer]

        # guint wmem_map_size(wmem_map_t *map);
        self.wmem_map_size = libwireshark.wmem_map_size
        self.wmem_map_size.restype = LibGLib2.guint
        self.wmem_map_size.argtypes = [POINTER(self.wmem_map_t)]

        # guint32 wmem_strong_hash(const guint8 *buf, const size_t len);
        self.wmem_strong_hash = libwireshark.wmem_strong_hash
        self.wmem_strong_hash.restype = LibGLib2.guint32
        self.wmem_strong_hash.argtypes = [POINTER(LibGLib2.guint8), c_size_t]

        # guint wmem_str_hash(gconstpointer key);
        self.wmem_str_hash = libwireshark.wmem_str_hash
        self.wmem_str_hash.restype = LibGLib2.guint
        self.wmem_str_hash.argtypes = [LibGLib2.gconstpointer]

        # guint wmem_int64_hash(gconstpointer key);
        self.wmem_int64_hash = libwireshark.wmem_int64_hash
        self.wmem_int64_hash.restype = LibGLib2.guint
        self.wmem_int64_hash.argtypes = [LibGLib2.gconstpointer]

        # guint wmem_double_hash(gconstpointer key);
        self.wmem_double_hash = libwireshark.wmem_double_hash
        self.wmem_double_hash.restype = LibGLib2.guint
        self.wmem_double_hash.argtypes = [LibGLib2.gconstpointer]

        # void *wmem_memdup(wmem_allocator_t *allocator, const void *source, const
        # size_t size);
        self.wmem_memdup = libwireshark.wmem_memdup
        self.wmem_memdup.restype = c_void_p
        self.wmem_memdup.argtypes = [
            POINTER(
                self.wmem_allocator_t),
            c_void_p,
            c_size_t]

        # void *wmem_stack_peek(const wmem_stack_t *stack);
        self.wmem_stack_peek = libwireshark.wmem_stack_peek
        self.wmem_stack_peek.restype = c_void_p
        self.wmem_stack_peek.argtypes = [POINTER(self.wmem_stack_t)]

        # void *wmem_stack_pop(wmem_stack_t *stack);
        self.wmem_stack_pop = libwireshark.wmem_stack_pop
        self.wmem_stack_pop.restype = c_void_p
        self.wmem_stack_pop.argtypes = [POINTER(self.wmem_stack_t)]

        # wmem_allocator_t *wmem_epan_scope(void);
        self.wmem_epan_scope = libwireshark.wmem_epan_scope
        self.wmem_epan_scope.restype = POINTER(self.wmem_allocator_t)
        self.wmem_epan_scope.argtypes = []

        # wmem_allocator_t *wmem_packet_scope(void);
        self.wmem_packet_scope = libwireshark.wmem_packet_scope
        self.wmem_packet_scope.restype = POINTER(self.wmem_allocator_t)
        self.wmem_packet_scope.argtypes = []

        # wmem_allocator_t *wmem_file_scope(void);
        self.wmem_file_scope = libwireshark.wmem_file_scope
        self.wmem_file_scope.restype = POINTER(self.wmem_allocator_t)
        self.wmem_file_scope.argtypes = []

        # wmem_strbuf_t *wmem_strbuf_sized_new(wmem_allocator_t *allocator,
        #                                      gsize alloc_len, gsize max_len);
        self.wmem_strbuf_sized_new = libwireshark.wmem_strbuf_sized_new
        self.wmem_strbuf_sized_new.restype = POINTER(self.wmem_strbuf_t)
        self.wmem_strbuf_sized_new.argtypes = [
            POINTER(
                self.wmem_allocator_t),
            LibGLib2.gsize,
            LibGLib2.gsize]

        # wmem_strbuf_t *wmem_strbuf_new(wmem_allocator_t *allocator, const gchar
        # *str);
        self.wmem_strbuf_new = libwireshark.wmem_strbuf_new
        self.wmem_strbuf_new.restype = POINTER(self.wmem_strbuf_t)
        self.wmem_strbuf_new.argtypes = [
            POINTER(self.wmem_allocator_t), LibGLib2.gchar_p]

        # void wmem_strbuf_append(wmem_strbuf_t *strbuf, const gchar *str);
        self.wmem_strbuf_append = libwireshark.wmem_strbuf_append
        self.wmem_strbuf_append.restype = None
        self.wmem_strbuf_append.argtypes = [
            POINTER(self.wmem_strbuf_t), LibGLib2.gchar_p]

        # void wmem_strbuf_append_c(wmem_strbuf_t *strbuf, const gchar c);
        self.wmem_strbuf_append_c = libwireshark.wmem_strbuf_append_c
        self.wmem_strbuf_append_c.restype = None
        self.wmem_strbuf_append_c.argtypes = [
            POINTER(self.wmem_strbuf_t), LibGLib2.gchar]

        # void wmem_strbuf_append_unichar(wmem_strbuf_t *strbuf, const gunichar
        # c);
        self.wmem_strbuf_append_unichar = libwireshark.wmem_strbuf_append_unichar
        self.wmem_strbuf_append_unichar.restype = None
        self.wmem_strbuf_append_unichar.argtypes = [
            POINTER(self.wmem_strbuf_t), LibGLib2.gunichar]

        # void wmem_strbuf_truncate(wmem_strbuf_t *strbuf, const gsize len);
        self.wmem_strbuf_truncate = libwireshark.wmem_strbuf_truncate
        self.wmem_strbuf_truncate.restype = None
        self.wmem_strbuf_truncate.argtypes = [
            POINTER(self.wmem_strbuf_t), LibGLib2.gsize]

        # const gchar *wmem_strbuf_get_str(wmem_strbuf_t *strbuf);
        self.wmem_strbuf_get_str = libwireshark.wmem_strbuf_get_str
        self.wmem_strbuf_get_str.restype = LibGLib2.gchar_p
        self.wmem_strbuf_get_str.argtypes = [POINTER(self.wmem_strbuf_t)]

        # gsize wmem_strbuf_get_len(wmem_strbuf_t *strbuf);
        self.wmem_strbuf_get_len = libwireshark.wmem_strbuf_get_len
        self.wmem_strbuf_get_len.restype = LibGLib2.gsize
        self.wmem_strbuf_get_len.argtypes = [POINTER(self.wmem_strbuf_t)]

        # char *wmem_strbuf_finalize(wmem_strbuf_t *strbuf);
        self.wmem_strbuf_finalize = libwireshark.wmem_strbuf_finalize
        self.wmem_strbuf_finalize.restype = c_char_p
        self.wmem_strbuf_finalize.argtypes = [POINTER(self.wmem_strbuf_t)]

        # wmem_tree_t *wmem_tree_new(wmem_allocator_t *allocator);
        self.wmem_tree_new = libwireshark.wmem_tree_new
        self.wmem_tree_new.restype = POINTER(self.wmem_tree_t)
        self.wmem_tree_new.argtypes = [POINTER(self.wmem_allocator_t)]

        # wmem_tree_t *wmem_tree_new_autoreset(wmem_allocator_t *master, wmem_allocator_t *slave);
        self.wmem_tree_new_autoreset = libwireshark.wmem_tree_new_autoreset
        self.wmem_tree_new_autoreset.restype = POINTER(self.wmem_tree_t)
        self.wmem_tree_new_autoreset.argtypes = [
            POINTER(self.wmem_allocator_t),
            POINTER(self.wmem_allocator_t)]

        # void wmem_tree_destroy(wmem_tree_t *tree, gboolean free_keys, gboolean
        # free_values);
        self.wmem_tree_destroy = libwireshark.wmem_tree_destroy
        self.wmem_tree_destroy.restype = None
        self.wmem_tree_destroy.argtypes = [
            POINTER(
                self.wmem_tree_t),
            LibGLib2.gboolean,
            LibGLib2.gboolean]

        # gboolean wmem_tree_is_empty(wmem_tree_t *tree);
        self.wmem_tree_is_empty = libwireshark.wmem_tree_is_empty
        self.wmem_tree_is_empty.restype = LibGLib2.gboolean
        self.wmem_tree_is_empty.argtypes = [POINTER(self.wmem_tree_t)]

        # guint wmem_tree_count(wmem_tree_t* tree);
        self.wmem_tree_count = libwireshark.wmem_tree_count
        self.wmem_tree_count.restype = LibGLib2.guint
        self.wmem_tree_count.argtypes = [POINTER(self.wmem_tree_t)]

        # void wmem_tree_insert32(wmem_tree_t *tree, guint32 key, void *data);
        self.wmem_tree_insert32 = libwireshark.wmem_tree_insert32
        self.wmem_tree_insert32.restype = None
        self.wmem_tree_insert32.argtypes = [
            POINTER(self.wmem_tree_t), LibGLib2.guint32, c_void_p]

        # void *wmem_tree_lookup32(wmem_tree_t *tree, guint32 key);
        self.wmem_tree_lookup32 = libwireshark.wmem_tree_lookup32
        self.wmem_tree_lookup32.restype = c_void_p
        self.wmem_tree_lookup32.argtypes = [
            POINTER(self.wmem_tree_t), LibGLib2.guint32]

        # void *wmem_tree_lookup32_le(wmem_tree_t *tree, guint32 key);
        self.wmem_tree_lookup32_le = libwireshark.wmem_tree_lookup32_le
        self.wmem_tree_lookup32_le.restype = c_void_p
        self.wmem_tree_lookup32_le.argtypes = [
            POINTER(self.wmem_tree_t), LibGLib2.guint32]

        # void *wmem_tree_remove32(wmem_tree_t *tree, guint32 key);
        self.wmem_tree_remove32 = libwireshark.wmem_tree_remove32
        self.wmem_tree_remove32.restype = c_void_p
        self.wmem_tree_remove32.argtypes = [
            POINTER(self.wmem_tree_t), LibGLib2.guint32]

        # void wmem_tree_insert_string(wmem_tree_t *tree, const gchar* key,
        #                              void *data, guint32 flags);
        self.wmem_tree_insert_string = libwireshark.wmem_tree_insert_string
        self.wmem_tree_insert_string.restype = None
        self.wmem_tree_insert_string.argtypes = [POINTER(self.wmem_tree_t),
                                                 LibGLib2.gchar_p,
                                                 c_void_p,
                                                 LibGLib2.guint32]

        # void *wmem_tree_lookup_string(wmem_tree_t* tree, const gchar* key,
        # guint32 flags);
        self.wmem_tree_lookup_string = libwireshark.wmem_tree_lookup_string
        self.wmem_tree_lookup_string.restype = c_void_p
        self.wmem_tree_lookup_string.argtypes = [
            POINTER(self.wmem_tree_t), LibGLib2.gchar_p, LibGLib2.guint32]

        # void *wmem_tree_remove_string(wmem_tree_t* tree, const gchar* key,
        # guint32 flags);
        self.wmem_tree_remove_string = libwireshark.wmem_tree_remove_string
        self.wmem_tree_remove_string.restype = c_void_p
        self.wmem_tree_remove_string.argtypes = [
            POINTER(self.wmem_tree_t), LibGLib2.gchar_p, LibGLib2.guint32]

        # void wmem_tree_insert32_array(wmem_tree_t *tree, wmem_tree_key_t *key,
        # void *data);
        self.wmem_tree_insert32_array = libwireshark.wmem_tree_insert32_array
        self.wmem_tree_insert32_array.restype = None
        self.wmem_tree_insert32_array.argtypes = [
            POINTER(
                self.wmem_tree_t), POINTER(
                self.wmem_tree_key_t), c_void_p]

        # void *wmem_tree_lookup32_array(wmem_tree_t *tree, wmem_tree_key_t *key);
        self.wmem_tree_lookup32_array = libwireshark.wmem_tree_insert32_array
        self.wmem_tree_lookup32_array.restype = c_void_p
        self.wmem_tree_lookup32_array.argtypes = [
            POINTER(self.wmem_tree_t),
            POINTER(self.wmem_tree_key_t)]

        # void *wmem_tree_lookup32_array_le(wmem_tree_t *tree, wmem_tree_key_t *key);
        self.wmem_tree_lookup32_array_le = libwireshark.wmem_tree_lookup32_array_le
        self.wmem_tree_lookup32_array_le.restype = c_void_p
        self.wmem_tree_lookup32_array_le.argtypes = [
            POINTER(self.wmem_tree_t), POINTER(self.wmem_tree_key_t)]

        # gboolean wmem_tree_foreach(wmem_tree_t* tree, wmem_foreach_func callback,
        #                            void *user_data);
        self.wmem_tree_foreach = libwireshark.wmem_tree_foreach
        self.wmem_tree_foreach.restype = LibGLib2.gboolean
        self.wmem_tree_foreach.argtypes = [
            POINTER(self.wmem_tree_t),
            self.wmem_foreach_func,
            c_void_p]

        # wmem_itree_t *wmem_itree_new(wmem_allocator_t *allocator);
        self.wmem_itree_new = libwireshark.wmem_itree_new
        self.wmem_itree_new.restype = POINTER(self.wmem_itree_t)
        self.wmem_itree_new.argtypes = [POINTER(self.wmem_allocator_t)]

        # gboolean wmem_itree_is_empty(wmem_itree_t *tree);
        self.wmem_itree_is_empty = libwireshark.wmem_itree_is_empty
        self.wmem_itree_is_empty.restype = LibGLib2.gboolean
        self.wmem_itree_is_empty.argtypes = [POINTER(self.wmem_itree_t)]

        # void wmem_itree_insert(wmem_itree_t *tree, const guint64 low,
        #                        const guint64 high, void *data);
        self.wmem_itree_insert = libwireshark.wmem_itree_insert
        self.wmem_itree_insert.restype = None
        self.wmem_itree_insert.argtypes = [POINTER(self.wmem_itree_t),
                                           LibGLib2.guint64,
                                           LibGLib2.guint64,
                                           c_void_p]

        # wmem_list_t *wmem_itree_find_intervals(wmem_itree_t *tree, wmem_allocator_t *allocator,
        #                                        guint64 low, guint64 high);
        self.wmem_itree_find_intervals = libwireshark.wmem_itree_find_intervals
        self.wmem_itree_find_intervals.restype = POINTER(self.wmem_list_t)
        self.wmem_itree_find_intervals.argtypes = [
            POINTER(
                self.wmem_itree_t), POINTER(
                self.wmem_allocator_t), LibGLib2.guint64, LibGLib2.guint64]

        # guint wmem_register_callback(wmem_allocator_t *allocator, wmem_user_cb_t callback,
        #                              void *user_data);
        self.wmem_register_callback = libwireshark.wmem_register_callback
        self.wmem_register_callback.restype = LibGLib2.guint
        self.wmem_register_callback.argtypes = [POINTER(self.wmem_allocator_t),
                                                self.wmem_user_cb_t,
                                                c_void_p]

        # void wmem_unregister_callback(wmem_allocator_t *allocator, guint id);
        self.wmem_unregister_callback = libwireshark.wmem_unregister_callback
        self.wmem_unregister_callback.restype = None
        self.wmem_unregister_callback.argtypes = [
            POINTER(self.wmem_allocator_t), LibGLib2.guint]

        # void guids_init(void);
        self.guids_init = libwireshark.guids_init
        self.guids_init.restype = None
        self.guids_init.argtypes = []

        # void guids_add_guid(const e_guid_t *guid, const gchar *name);
        self.guids_add_guid = libwireshark.guids_add_guid
        self.guids_add_guid.restype = None
        self.guids_add_guid.argtypes = [
            POINTER(self.e_guid_t), LibGLib2.gchar_p]

        # const gchar *guids_get_guid_name(const e_guid_t *guid);
        self.guids_get_guid_name = libwireshark.guids_get_guid_name
        self.guids_get_guid_name.restype = LibGLib2.gchar_p
        self.guids_get_guid_name.argtypes = [POINTER(self.e_guid_t)]

        # const gchar* guids_resolve_guid_to_str(const e_guid_t *guid);
        self.guids_resolve_guid_to_str = libwireshark.guids_resolve_guid_to_str
        self.guids_resolve_guid_to_str.restype = LibGLib2.gchar_p
        self.guids_resolve_guid_to_str.argtypes = [POINTER(self.e_guid_t)]

        # int guid_cmp(const e_guid_t *g1, const e_guid_t *g2);
        self.guid_cmp = libwireshark.guid_cmp
        self.guid_cmp.restype = c_int
        self.guid_cmp.argtypes = [
            POINTER(
                self.e_guid_t), POINTER(
                self.e_guid_t)]

        # tvbuff_t *tvb_new_octet_aligned(tvbuff_t *tvb,
        #     guint32 bit_offset, gint32 no_of_bits);
        self.tvb_new_octet_aligned = libwireshark.tvb_new_octet_aligned
        self.tvb_new_octet_aligned.restype = POINTER(self.tvbuff_t)
        self.tvb_new_octet_aligned.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.guint32, LibGLib2.guint32]

        # tvbuff_t *tvb_new_chain(tvbuff_t *parent, tvbuff_t *backing);
        self.tvb_new_chain = libwireshark.tvb_new_chain
        self.tvb_new_chain.restype = POINTER(self.tvbuff_t)
        self.tvb_new_chain.argtypes = [
            POINTER(
                self.tvbuff_t), POINTER(
                self.tvbuff_t)]

        # tvbuff_t *tvb_clone(tvbuff_t *tvb);
        self.tvb_clone = libwireshark.tvb_clone
        self.tvb_clone.restype = POINTER(self.tvbuff_t)
        self.tvb_clone.argtypes = [POINTER(self.tvbuff_t)]

        # tvbuff_t *tvb_clone_offset_len(tvbuff_t *tvb, guint offset,
        #     guint len);
        self.tvb_clone_offset_len = libwireshark.tvb_clone_offset_len
        self.tvb_clone_offset_len.restype = POINTER(self.tvbuff_t)
        self.tvb_clone_offset_len.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.guint, LibGLib2.guint]

        # void tvb_free(tvbuff_t *tvb);
        self.tvb_free = libwireshark.tvb_free
        self.tvb_free.restype = None
        self.tvb_free.argtypes = [POINTER(self.tvbuff_t)]

        # void tvb_free_chain(tvbuff_t *tvb);
        self.tvb_free_chain = libwireshark.tvb_free_chain
        self.tvb_free_chain.restype = None
        self.tvb_free_chain.argtypes = [POINTER(self.tvbuff_t)]

        # void tvb_set_free_cb(tvbuff_t *tvb, const tvbuff_free_cb_t func);
        self.tvb_set_free_cb = libwireshark.tvb_set_free_cb
        self.tvb_set_free_cb.restype = None
        self.tvb_set_free_cb.argtypes = [
            POINTER(self.tvbuff_t), self.tvbuff_free_cb_t]

        # void tvb_set_child_real_data_tvbuff(tvbuff_t *parent,
        #     tvbuff_t *child);
        self.tvb_set_child_real_data_tvbuff = libwireshark.tvb_set_child_real_data_tvbuff
        self.tvb_set_child_real_data_tvbuff.restype = None
        self.tvb_set_child_real_data_tvbuff.argtypes = [
            POINTER(self.tvbuff_t), POINTER(self.tvbuff_t)]

        # tvbuff_t *tvb_new_child_real_data(tvbuff_t *parent,
        # const guint8 *data, const guint length, const gint reported_length);
        self.tvb_new_child_real_data = libwireshark.tvb_new_child_real_data
        self.tvb_new_child_real_data.restype = POINTER(self.tvbuff_t)
        self.tvb_new_child_real_data.argtypes = [POINTER(self.tvbuff_t),
                                                 POINTER(LibGLib2.guint8),
                                                 LibGLib2.guint,
                                                 LibGLib2.gint]

        # tvbuff_t *tvb_new_real_data(const guint8 *data,
        #     const guint length, const gint reported_length);
        self.tvb_new_real_data = libwireshark.tvb_new_real_data
        self.tvb_new_real_data.restype = POINTER(self.tvbuff_t)
        self.tvb_new_real_data.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.gint]

        # tvbuff_t *tvb_new_subset_length_caplen(tvbuff_t *backing,
        #     const gint backing_offset, const gint backing_length,
        #     const gint reported_length);
        self.tvb_new_subset_length_caplen = libwireshark.tvb_new_subset_length_caplen
        self.tvb_new_subset_length_caplen.restype = POINTER(self.tvbuff_t)
        self.tvb_new_subset_length_caplen.argtypes = [POINTER(self.tvbuff_t),
                                                      LibGLib2.gint,
                                                      LibGLib2.gint,
                                                      LibGLib2.gint]

        # tvbuff_t *tvb_new_subset_length(tvbuff_t *backing,
        #     const gint backing_offset, const gint reported_length);
        self.tvb_new_subset_length = libwireshark.tvb_new_subset_length
        self.tvb_new_subset_length.restype = POINTER(self.tvbuff_t)
        self.tvb_new_subset_length.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint, LibGLib2.gint]

        # tvbuff_t *tvb_new_subset_remaining(tvbuff_t *backing,
        #     const gint backing_offset);
        self.tvb_new_subset_remaining = libwireshark.tvb_new_subset_remaining
        self.tvb_new_subset_remaining.restype = POINTER(self.tvbuff_t)
        self.tvb_new_subset_remaining.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # void tvb_composite_append(tvbuff_t *tvb, tvbuff_t *member);
        self.tvb_composite_append = libwireshark.tvb_composite_append
        self.tvb_composite_append.restype = None
        self.tvb_composite_append.argtypes = [
            POINTER(
                self.tvbuff_t), POINTER(
                self.tvbuff_t)]

        # tvbuff_t *tvb_new_composite(void);
        self.tvb_new_composite = libwireshark.tvb_new_composite
        self.tvb_new_composite.restype = POINTER(self.tvbuff_t)
        self.tvb_new_composite.argtypes = []

        # void tvb_composite_finalize(tvbuff_t *tvb);
        self.tvb_composite_finalize = libwireshark.tvb_composite_finalize
        self.tvb_composite_finalize.restype = None
        self.tvb_composite_finalize.argtypes = [POINTER(self.tvbuff_t)]

        # guint tvb_captured_length(const tvbuff_t *tvb);
        self.tvb_captured_length = libwireshark.tvb_captured_length
        self.tvb_captured_length.restype = LibGLib2.guint
        self.tvb_captured_length.argtypes = [POINTER(self.tvbuff_t)]

        # gint tvb_captured_length_remaining(const tvbuff_t *tvb, const gint
        # offset);
        self.tvb_captured_length_remaining = libwireshark.tvb_captured_length_remaining
        self.tvb_captured_length_remaining.restype = LibGLib2.gint
        self.tvb_captured_length_remaining.argtype = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint tvb_ensure_captured_length_remaining(const tvbuff_t *tvb,
        #     const gint offset);
        self.tvb_ensure_captured_length_remaining = libwireshark.tvb_ensure_captured_length_remaining
        self.tvb_ensure_captured_length_remaining.restype = LibGLib2.guint
        self.tvb_ensure_captured_length_remaining.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # gboolean tvb_bytes_exist(const tvbuff_t *tvb, const gint offset,
        #     const gint length);
        self.tvb_bytes_exist = libwireshark.tvb_bytes_exist
        self.tvb_bytes_exist.restype = LibGLib2.gboolean
        self.tvb_bytes_exist.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint]

        # void tvb_ensure_bytes_exist64(const tvbuff_t *tvb,
        #     const gint offset, const guint64 length);
        self.tvb_ensure_bytes_exist64 = libwireshark.tvb_ensure_bytes_exist64
        self.tvb_ensure_bytes_exist64.restype = None
        self.tvb_ensure_bytes_exist64.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint, LibGLib2.guint64]

        # void tvb_ensure_bytes_exist(const tvbuff_t *tvb,
        #     const gint offset, const gint length);
        self.tvb_ensure_bytes_exist = libwireshark.tvb_ensure_bytes_exist
        self.tvb_ensure_bytes_exist.restype = None
        self.tvb_ensure_bytes_exist.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint, LibGLib2.gint]

        # gboolean tvb_offset_exists(const tvbuff_t *tvb,
        #     const gint offset);
        self.tvb_offset_exists = libwireshark.tvb_offset_exists
        self.tvb_offset_exists.restype = LibGLib2.gboolean
        self.tvb_offset_exists.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint tvb_reported_length(const tvbuff_t *tvb);
        self.tvb_reported_length = libwireshark.tvb_reported_length
        self.tvb_reported_length.restype = LibGLib2.guint
        self.tvb_reported_length.argtypes = [POINTER(self.tvbuff_t)]

        # gint tvb_reported_length_remaining(const tvbuff_t *tvb,
        #     const gint offset);
        self.tvb_reported_length_remaining = libwireshark.tvb_reported_length_remaining
        self.tvb_reported_length_remaining.restype = LibGLib2.gint
        self.tvb_reported_length_remaining.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # void tvb_set_reported_length(tvbuff_t *tvb, const guint);
        self.tvb_set_reported_length = libwireshark.tvb_set_reported_length
        self.tvb_set_reported_length.restype = None
        self.tvb_set_reported_length.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.guint]

        # guint tvb_offset_from_real_beginning(const tvbuff_t *tvb);
        self.tvb_offset_from_real_beginning = libwireshark.tvb_offset_from_real_beginning
        self.tvb_offset_from_real_beginning.restype = LibGLib2.guint
        self.tvb_offset_from_real_beginning.argtypes = [POINTER(self.tvbuff_t)]

        # gint tvb_raw_offset(tvbuff_t *tvb);
        self.tvb_raw_offset = libwireshark.tvb_raw_offset
        self.tvb_raw_offset.restype = LibGLib2.gint
        self.tvb_raw_offset.argtypes = [POINTER(self.tvbuff_t)]

        # void tvb_set_fragment(tvbuff_t *tvb);
        self.tvb_set_fragment = libwireshark.tvb_set_fragment
        self.tvb_set_fragment.restype = None
        self.tvb_set_fragment.argtypes = [POINTER(self.tvbuff_t)]

        # struct tvbuff *tvb_get_ds_tvb(tvbuff_t *tvb);
        self.tvb_get_ds_tvb = libwireshark.tvb_get_ds_tvb
        self.tvb_get_ds_tvb.restype = POINTER(self.tvbuff)
        self.tvb_get_ds_tvb.argtypes = [POINTER(self.tvbuff_t)]

        # guint8 tvb_get_guint8(tvbuff_t *tvb, const gint offset);
        self.tvb_get_guint8 = libwireshark.tvb_get_guint8
        self.tvb_get_guint8.restype = LibGLib2.guint8
        self.tvb_get_guint8.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint8 tvb_get_gint8(tvbuff_t *tvb, const gint offset);
        self.tvb_get_gint8 = libwireshark.tvb_get_gint8
        self.tvb_get_gint8.restype = LibGLib2.gint8
        self.tvb_get_gint8.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint16 tvb_get_ntohs(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohs = libwireshark.tvb_get_ntohs
        self.tvb_get_ntohs.restype = LibGLib2.guint16
        self.tvb_get_ntohs.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint16 tvb_get_ntohis(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohis = libwireshark.tvb_get_ntohis
        self.tvb_get_ntohis.restype = LibGLib2.gint16
        self.tvb_get_ntohis.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint32 tvb_get_ntoh24(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntoh24 = libwireshark.tvb_get_ntoh24
        self.tvb_get_ntoh24.restype = LibGLib2.guint32
        self.tvb_get_ntoh24.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint32 tvb_get_ntohi24(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohi24 = libwireshark.tvb_get_ntohi24
        self.tvb_get_ntohi24.restype = LibGLib2.gint32
        self.tvb_get_ntohi24.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint32 tvb_get_ntohl(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohl = libwireshark.tvb_get_ntohl
        self.tvb_get_ntohl.restype = LibGLib2.guint32
        self.tvb_get_ntohl.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint32 tvb_get_ntohil(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohil = libwireshark.tvb_get_ntohil
        self.tvb_get_ntohil.restype = LibGLib2.gint32
        self.tvb_get_ntohil.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_ntoh40(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntoh40 = libwireshark.tvb_get_ntoh40
        self.tvb_get_ntoh40.restype = LibGLib2.guint64
        self.tvb_get_ntoh40.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_ntohi40(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohi40 = libwireshark.tvb_get_ntohi40
        self.tvb_get_ntohi40.restype = LibGLib2.gint64
        self.tvb_get_ntohi40.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_ntoh48(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntoh48 = libwireshark.tvb_get_ntoh48
        self.tvb_get_ntoh48.restype = LibGLib2.guint64
        self.tvb_get_ntoh48.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_ntohi48(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohi48 = libwireshark.tvb_get_ntohi48
        self.tvb_get_ntohi48.restype = LibGLib2.gint64
        self.tvb_get_ntohi48.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_ntoh56(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntoh56 = libwireshark.tvb_get_ntoh56
        self.tvb_get_ntoh56.restype = LibGLib2.guint64
        self.tvb_get_ntoh56.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_ntohi56(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohi56 = libwireshark.tvb_get_ntohi56
        self.tvb_get_ntohi56.restype = LibGLib2.gint64
        self.tvb_get_ntohi56.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_ntoh64(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntoh64 = libwireshark.tvb_get_ntoh64
        self.tvb_get_ntoh64.restype = LibGLib2.guint64
        self.tvb_get_ntoh64.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_ntohi64(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohi64 = libwireshark.tvb_get_ntohi64
        self.tvb_get_ntohi64.restype = LibGLib2.gint64
        self.tvb_get_ntohi64.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gfloat tvb_get_ntohieee_float(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ntohieee_float = libwireshark.tvb_get_ntohieee_float
        self.tvb_get_ntohieee_float.restype = LibGLib2.gfloat
        self.tvb_get_ntohieee_float.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # gdouble tvb_get_ntohieee_double(tvbuff_t *tvb,
        #     const gint offset);
        self.tvb_get_ntohieee_double = libwireshark.tvb_get_ntohieee_double
        self.tvb_get_ntohieee_double.restype = LibGLib2.gdouble
        self.tvb_get_ntohieee_double.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint16 tvb_get_letohs(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohs = libwireshark.tvb_get_letohs
        self.tvb_get_letohs.restype = LibGLib2.guint16
        self.tvb_get_letohs.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint16 tvb_get_letohis(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohis = libwireshark.tvb_get_letohis
        self.tvb_get_letohis.restype = LibGLib2.gint16
        self.tvb_get_letohis.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint32 tvb_get_letoh24(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letoh24 = libwireshark.tvb_get_letoh24
        self.tvb_get_letoh24.restype = LibGLib2.guint32
        self.tvb_get_letoh24.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint32 tvb_get_letohi24(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohi24 = libwireshark.tvb_get_letohi24
        self.tvb_get_letohi24.restype = LibGLib2.gint32
        self.tvb_get_letohi24.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint32 tvb_get_letohl(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohl = libwireshark.tvb_get_letohl
        self.tvb_get_letohl.restype = LibGLib2.guint32
        self.tvb_get_letohl.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint32 tvb_get_letohil(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohil = libwireshark.tvb_get_letohil
        self.tvb_get_letohil.restype = LibGLib2.gint32
        self.tvb_get_letohil.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_letoh40(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letoh40 = libwireshark.tvb_get_letoh40
        self.tvb_get_letoh40.restype = LibGLib2.guint64
        self.tvb_get_letoh40.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_letohi40(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohi40 = libwireshark.tvb_get_letohi40
        self.tvb_get_letohi40.restype = LibGLib2.gint64
        self.tvb_get_letohi40.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_letoh48(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letoh48 = libwireshark.tvb_get_letoh48
        self.tvb_get_letoh48.restype = LibGLib2.guint64
        self.tvb_get_letoh48.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_letohi48(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohi48 = libwireshark.tvb_get_letohi48
        self.tvb_get_letohi48.restype = LibGLib2.gint64
        self.tvb_get_letohi48.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_letoh56(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letoh56 = libwireshark.tvb_get_letoh56
        self.tvb_get_letoh56.restype = LibGLib2.guint64
        self.tvb_get_letoh56.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_letohi56(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohi56 = libwireshark.tvb_get_letohi56
        self.tvb_get_letohi56.restype = LibGLib2.gint64
        self.tvb_get_letohi56.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint64 tvb_get_letoh64(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letoh64 = libwireshark.tvb_get_letoh64
        self.tvb_get_letoh64.restype = LibGLib2.guint64
        self.tvb_get_letoh64.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint64 tvb_get_letohi64(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohi64 = libwireshark.tvb_get_letohi64
        self.tvb_get_letohi64.restype = LibGLib2.gint64
        self.tvb_get_letohi64.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # gfloat tvb_get_letohieee_float(tvbuff_t *tvb, const gint offset);
        self.tvb_get_letohieee_float = libwireshark.tvb_get_letohieee_float
        self.tvb_get_letohieee_float.restype = LibGLib2.gfloat
        self.tvb_get_letohieee_float.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # gdouble tvb_get_letohieee_double(tvbuff_t *tvb,
        #     const gint offset);
        self.tvb_get_letohieee_double = libwireshark.tvb_get_letohieee_double
        self.tvb_get_letohieee_double.restype = LibGLib2.gdouble
        self.tvb_get_letohieee_double.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint16 tvb_get_guint16(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_guint16 = libwireshark.tvb_get_guint16
        self.tvb_get_guint16.restype = LibGLib2.guint16
        self.tvb_get_guint16.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gint16 tvb_get_gint16(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_gint16 = libwireshark.tvb_get_gint16
        self.tvb_get_gint16.restype = LibGLib2.gint16
        self.tvb_get_gint16.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # guint32 tvb_get_guint24(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_guint24 = libwireshark.tvb_get_guint24
        self.tvb_get_guint24.restype = LibGLib2.guint32
        self.tvb_get_guint24.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gint32 tvb_get_gint24(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_gint24 = libwireshark.tvb_get_gint24
        self.tvb_get_gint24.restype = LibGLib2.gint32
        self.tvb_get_gint24.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # guint32 tvb_get_guint32(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_guint32 = libwireshark.tvb_get_guint32
        self.tvb_get_guint32.restype = LibGLib2.guint32
        self.tvb_get_guint32.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gint32 tvb_get_gint32(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_gint32 = libwireshark.tvb_get_gint32
        self.tvb_get_gint32.restype = LibGLib2.gint32
        self.tvb_get_gint32.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # guint64 tvb_get_guint40(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_guint40 = libwireshark.tvb_get_guint40
        self.tvb_get_guint40.restype = LibGLib2.guint64
        self.tvb_get_guint40.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gint64 tvb_get_gint40(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_gint40 = libwireshark.tvb_get_gint40
        self.tvb_get_gint40.restype = LibGLib2.gint64
        self.tvb_get_gint40.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # guint64 tvb_get_guint48(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_guint48 = libwireshark.tvb_get_guint48
        self.tvb_get_guint48.restype = LibGLib2.guint64
        self.tvb_get_guint48.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gint64 tvb_get_gint48(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_gint48 = libwireshark.tvb_get_gint48
        self.tvb_get_gint48.restype = LibGLib2.gint64
        self.tvb_get_gint48.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # guint64 tvb_get_guint56(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_guint56 = libwireshark.tvb_get_guint56
        self.tvb_get_guint56.restype = LibGLib2.guint64
        self.tvb_get_guint56.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gint64 tvb_get_gint56(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_gint56 = libwireshark.tvb_get_gint56
        self.tvb_get_gint56.restype = LibGLib2.gint64
        self.tvb_get_gint56.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # guint64 tvb_get_guint64(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_guint64 = libwireshark.tvb_get_guint64
        self.tvb_get_guint64.restype = LibGLib2.guint64
        self.tvb_get_guint64.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gint64 tvb_get_gint64(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_gint64 = libwireshark.tvb_get_gint64
        self.tvb_get_gint64.restype = LibGLib2.gint64
        self.tvb_get_gint64.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gfloat tvb_get_ieee_float(tvbuff_t *tvb, const gint offset, const guint
        # encoding);
        self.tvb_get_ieee_float = libwireshark.tvb_get_ieee_float
        self.tvb_get_ieee_float.restype = LibGLib2.gfloat
        self.tvb_get_ieee_float.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint, LibGLib2.guint]

        # gdouble tvb_get_ieee_double(tvbuff_t *tvb, const gint offset, const
        # guint encoding);
        self.tvb_get_ieee_double = libwireshark.tvb_get_ieee_double
        self.tvb_get_ieee_double.restype = LibGLib2.gdouble
        self.tvb_get_ieee_double.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint, LibGLib2.guint]

        # #if G_BYTE_ORDER == G_LITTLE_ENDIAN
        if sys.byteorder == 'little':
            # #define tvb_get_h_guint16   tvb_get_letohs
            self.tvb_get_h_guint16 = self.tvb_get_letohs

            # #define tvb_get_h_guint32   tvb_get_letohl
            self.tvb_get_h_guint32 = self.tvb_get_letohl

        # #elif G_BYTE_ORDER == G_BIG_ENDIAN
        elif sys.byteorder == 'big':
            # #define tvb_get_h_guint16   tvb_get_ntohs
            self.tvb_get_h_guint16 = self.tvb_get_ntohs

            # #define tvb_get_h_guint32   tvb_get_ntohl
            self.tvb_get_h_guint32 = self.tvb_get_ntohl

        # nstime_t* tvb_get_string_time(tvbuff_t *tvb, const gint offset, const gint length,
        # const guint encoding, nstime_t* ns, gint *endoff);
        self.tvb_get_string_time = libwireshark.tvb_get_string_time
        self.tvb_get_string_time.restype = POINTER(LibWSUtil.nstime_t)
        self.tvb_get_string_time.argtypes = [POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint,
                                             LibGLib2.guint,
                                             POINTER(LibWSUtil.nstime_t),
                                             POINTER(LibGLib2.gint)]

        # GByteArray* tvb_get_string_bytes(tvbuff_t *tvb, const gint offset, const gint length,
        # const guint encoding, GByteArray* bytes, gint *endoff);
        self.tvb_get_string_bytes = libwireshark.tvb_get_string_bytes
        self.tvb_get_string_bytes.restype = POINTER(LibGLib2.GByteArray)
        self.tvb_get_string_bytes.argtypes = [POINTER(self.tvbuff_t),
                                              LibGLib2.gint,
                                              LibGLib2.gint,
                                              LibGLib2.guint,
                                              POINTER(LibGLib2.GByteArray),
                                              POINTER(LibGLib2.gint)]

        # guint32 tvb_get_ipv4(tvbuff_t *tvb, const gint offset);
        self.tvb_get_ipv4 = libwireshark.tvb_get_ipv4
        self.tvb_get_ipv4.restype = LibGLib2.guint32
        self.tvb_get_ipv4.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # void tvb_get_ipv6(tvbuff_t *tvb, const gint offset,
        #     ws_in6_addr *addr);
        self.tvb_get_ipv6 = libwireshark.tvb_get_ipv6
        self.tvb_get_ipv6.restype = None
        self.tvb_get_ipv6.argtypes = [
            POINTER(
                self.tvbuff_t), LibGLib2.gint, POINTER(
                LibWSUtil.ws_in6_addr)]

        # void tvb_get_ntohguid(tvbuff_t *tvb, const gint offset,
        #     e_guid_t *guid);
        self.tvb_get_ntohguid = libwireshark.tvb_get_ntohguid
        self.tvb_get_ntohguid.restype = None
        self.tvb_get_ntohguid.argtypes = [
            POINTER(
                self.tvbuff_t), LibGLib2.gint, POINTER(
                self.e_guid_t)]

        # void tvb_get_letohguid(tvbuff_t *tvb, const gint offset,
        #     e_guid_t *guid);
        self.tvb_get_letohguid = libwireshark.tvb_get_letohguid
        self.tvb_get_letohguid.restype = None
        self.tvb_get_letohguid.argtypes = [
            POINTER(
                self.tvbuff_t), LibGLib2.gint, POINTER(
                self.e_guid_t)]

        # void tvb_get_guid(tvbuff_t *tvb, const gint offset,
        #     e_guid_t *guid, const guint encoding);
        self.tvb_get_guid = libwireshark.tvb_get_guid
        self.tvb_get_guid.restype = None
        self.tvb_get_guid.argtypes = [POINTER(self.tvbuff_t),
                                      LibGLib2.gint,
                                      POINTER(self.e_guid_t),
                                      LibGLib2.guint]

        # guint8 tvb_get_bits8(tvbuff_t *tvb, guint bit_offset,
        #     const gint no_of_bits);
        self.tvb_get_bits8 = libwireshark.tvb_get_bits8
        self.tvb_get_bits8.restype = LibGLib2.guint8
        self.tvb_get_bits8.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.guint,
            LibGLib2.gint]

        # guint16 tvb_get_bits16(tvbuff_t *tvb, guint bit_offset,
        #     const gint no_of_bits, const guint encoding);
        self.tvb_get_bits16 = libwireshark.tvb_get_bits16
        self.tvb_get_bits16.restype = LibGLib2.guint16
        self.tvb_get_bits16.argtypes = [POINTER(self.tvbuff_t),
                                        LibGLib2.guint,
                                        LibGLib2.gint,
                                        LibGLib2.guint]

        # guint32 tvb_get_bits32(tvbuff_t *tvb, guint bit_offset,
        #     const gint no_of_bits, const guint encoding);
        self.tvb_get_bits32 = libwireshark.tvb_get_bits32
        self.tvb_get_bits32.restype = LibGLib2.guint32
        self.tvb_get_bits32.argtypes = [POINTER(self.tvbuff_t),
                                        LibGLib2.guint,
                                        LibGLib2.gint,
                                        LibGLib2.guint]

        # guint64 tvb_get_bits64(tvbuff_t *tvb, guint bit_offset,
        #     const gint no_of_bits, const guint encoding);
        self.tvb_get_bits64 = libwireshark.tvb_get_bits64
        self.tvb_get_bits64.restype = LibGLib2.guint64
        self.tvb_get_bits64.argtypes = [POINTER(self.tvbuff_t),
                                        LibGLib2.guint,
                                        LibGLib2.gint,
                                        LibGLib2.guint]

        # guint32 tvb_get_bits(tvbuff_t *tvb, const guint bit_offset,
        #     const gint no_of_bits, const guint encoding);
        self.tvb_get_bits = libwireshark.tvb_get_bits
        self.tvb_get_bits.restype = LibGLib2.guint32
        self.tvb_get_bits.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.guint,
            LibGLib2.gint,
            LibGLib2.guint]

        # void *tvb_memcpy(tvbuff_t *tvb, void *target, const gint offset,
        #     size_t length);
        self.tvb_memcpy = libwireshark.tvb_memcpy
        self.tvb_memcpy.restype = c_void_p
        self.tvb_memcpy.argtypes = [
            POINTER(
                self.tvbuff_t),
            c_void_p,
            LibGLib2.gint,
            c_size_t]

        # void *tvb_memdup(wmem_allocator_t *scope, tvbuff_t *tvb,
        #     const gint offset, size_t length);
        self.tvb_memdup = libwireshark.tvb_memdup
        self.tvb_memdup.restype = c_void_p
        self.tvb_memdup.argtypes = [POINTER(self.wmem_allocator_t),
                                    POINTER(self.tvbuff_t),
                                    LibGLib2.gint,
                                    c_size_t]

        # const guint8 *tvb_get_ptr(tvbuff_t *tvb, const gint offset,
        #     const gint length);
        self.tvb_get_ptr = libwireshark.tvb_get_ptr
        self.tvb_get_ptr.restype = POINTER(LibGLib2.guint8)
        self.tvb_get_ptr.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint]

        # gint tvb_find_guint8(tvbuff_t *tvb, const gint offset,
        #     const gint maxlength, const guint8 needle);
        self.tvb_find_guint8 = libwireshark.tvb_find_guint8
        self.tvb_find_guint8.restype = LibGLib2.gint
        self.tvb_find_guint8.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint8]

        # gint tvb_find_guint16(tvbuff_t *tvb, const gint offset,
        #     const gint maxlength, const guint16 needle);
        self.tvb_find_guint16 = libwireshark.tvb_find_guint16
        self.tvb_find_guint16.restype = LibGLib2.gint
        self.tvb_find_guint16.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint16]

        # gint tvb_ws_mempbrk_pattern_guint8(tvbuff_t *tvb, const gint offset,
        # const gint maxlength, const ws_mempbrk_pattern* pattern, guchar
        # *found_needle);
        self.tvb_ws_mempbrk_pattern_guint8 = libwireshark.tvb_ws_mempbrk_pattern_guint8
        self.tvb_ws_mempbrk_pattern_guint8.restype = LibGLib2.gint
        self.tvb_ws_mempbrk_pattern_guint8.argtypes = [
            POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, POINTER(
                LibWSUtil.ws_mempbrk_pattern), POINTER(
                LibGLib2.guchar)]

        # guint tvb_strsize(tvbuff_t *tvb, const gint offset);
        self.tvb_strsize = libwireshark.tvb_strsize
        self.tvb_strsize.restype = LibGLib2.guint
        self.tvb_strsize.argtypes = [POINTER(self.tvbuff_t), LibGLib2.gint]

        # guint tvb_unicode_strsize(tvbuff_t *tvb, const gint offset);
        self.tvb_unicode_strsize = libwireshark.tvb_unicode_strsize
        self.tvb_unicode_strsize.restype = LibGLib2.guint
        self.tvb_unicode_strsize.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # gint tvb_strnlen(tvbuff_t *tvb, const gint offset,
        #     const guint maxlength);
        self.tvb_strnlen = libwireshark.tvb_strnlen
        self.tvb_strnlen.restype = LibGLib2.gint
        self.tvb_strnlen.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.guint]

        # gchar *tvb_format_text(tvbuff_t *tvb, const gint offset,
        #     const gint size);
        self.tvb_format_text = libwireshark.tvb_format_text
        self.tvb_format_text.restype = LibGLib2.gchar_p
        self.tvb_format_text.argtypes = [
            POINTER(
                self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint]

        # gchar *tvb_format_text_wsp(wmem_allocator_t* allocator, tvbuff_t *tvb, const gint offset,
        #     const gint size);
        self.tvb_format_text_wsp = libwireshark.tvb_format_text_wsp
        self.tvb_format_text_wsp.restype = LibGLib2.gchar_p
        self.tvb_format_text_wsp.argtypes = [POINTER(self.wmem_allocator_t),
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint]

        # guint8 *tvb_get_string_enc(wmem_allocator_t *scope,
        # tvbuff_t *tvb, const gint offset, const gint length, const guint
        # encoding);
        self.tvb_get_string_enc = libwireshark.tvb_get_string_enc
        self.tvb_get_string_enc.restype = POINTER(LibGLib2.guint8)
        self.tvb_get_string_enc.argtypes = [POINTER(self.wmem_allocator_t),
                                            POINTER(self.tvbuff_t),
                                            LibGLib2.gint,
                                            LibGLib2.gint,
                                            LibGLib2.guint]

        # gchar *tvb_get_ts_23_038_7bits_string(wmem_allocator_t *scope,
        #     tvbuff_t *tvb, const gint bit_offset, gint no_of_chars);
        self.tvb_get_ts_23_038_7bits_string = libwireshark.tvb_get_ts_23_038_7bits_string
        self.tvb_get_ts_23_038_7bits_string.restype = LibGLib2.gchar_p
        self.tvb_get_ts_23_038_7bits_string.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint]

        # gchar *tvb_get_ascii_7bits_string(wmem_allocator_t *scope,
        #     tvbuff_t *tvb, const gint bit_offset, gint no_of_chars);
        self.tvb_get_ascii_7bits_string = libwireshark.tvb_get_ascii_7bits_string
        self.tvb_get_ascii_7bits_string.restype = LibGLib2.gchar_p
        self.tvb_get_ascii_7bits_string.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint]

        # guint8 *tvb_get_stringzpad(wmem_allocator_t *scope,
        # tvbuff_t *tvb, const gint offset, const gint length, const guint
        # encoding);
        self.tvb_get_stringzpad = libwireshark.tvb_get_stringzpad
        self.tvb_get_stringzpad.restype = POINTER(LibGLib2.guint8)
        self.tvb_get_stringzpad.argtypes = [POINTER(self.wmem_allocator_t),
                                            POINTER(self.tvbuff_t),
                                            LibGLib2.gint,
                                            LibGLib2.gint,
                                            LibGLib2.guint]

        # guint8 *tvb_get_stringz_enc(wmem_allocator_t *scope,
        # tvbuff_t *tvb, const gint offset, gint *lengthp, const guint
        # encoding);
        self.tvb_get_stringz_enc = libwireshark.tvb_get_stringz_enc
        self.tvb_get_stringz_enc.restype = POINTER(LibGLib2.guint8)
        self.tvb_get_stringz_enc.argtypes = [POINTER(self.wmem_allocator_t),
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             POINTER(LibGLib2.gint),
                                             LibGLib2.guint]

        # const guint8 *tvb_get_const_stringz(tvbuff_t *tvb,
        #     const gint offset, gint *lengthp);
        self.tvb_get_const_stringz = libwireshark.tvb_get_const_stringz
        self.tvb_get_const_stringz.restype = POINTER(LibGLib2.guint8)
        self.tvb_get_const_stringz.argtypes = [
            POINTER(
                self.tvbuff_t), LibGLib2.gint, POINTER(
                LibGLib2.gint)]

        # gint tvb_get_nstringz(tvbuff_t *tvb, const gint offset,
        #     const guint bufsize, guint8 *buffer);
        self.tvb_get_nstringz = libwireshark.tvb_get_nstringz
        self.tvb_get_nstringz.restype = LibGLib2.gint
        self.tvb_get_nstringz.argtypes = [
            POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.guint, POINTER(
                LibGLib2.guint8)]

        # gint tvb_get_nstringz0(tvbuff_t *tvb, const gint offset,
        #     const guint bufsize, guint8 *buffer);
        self.tvb_get_nstringz0 = libwireshark.tvb_get_nstringz0
        self.tvb_get_nstringz0.restype = LibGLib2.gint
        self.tvb_get_nstringz0.argtypes = [POINTER(self.tvbuff_t),
                                           LibGLib2.gint,
                                           LibGLib2.guint,
                                           POINTER(LibGLib2.guint8)]

        # gint tvb_get_raw_bytes_as_string(tvbuff_t *tvb, const gint offset, char
        # *buffer, size_t bufsize);
        self.tvb_get_raw_bytes_as_string = libwireshark.tvb_get_raw_bytes_as_string
        self.tvb_get_raw_bytes_as_string.restype = LibGLib2.gint
        self.tvb_get_raw_bytes_as_string.argtypes = [POINTER(self.tvbuff_t),
                                                     LibGLib2.gint,
                                                     c_char_p,
                                                     c_size_t]

        # gboolean tvb_ascii_isprint(tvbuff_t *tvb, const gint offset,
        # 	const gint length);
        self.tvb_ascii_isprint = libwireshark.tvb_ascii_isprint
        self.tvb_ascii_isprint.restype = LibGLib2.gboolean
        self.tvb_ascii_isprint.argtypes = [POINTER(self.tvbuff_t),
                                           LibGLib2.gint,
                                           LibGLib2.gint]

        # gint tvb_find_line_end(tvbuff_t *tvb, const gint offset, int len,
        #     gint *next_offset, const gboolean desegment);
        self.tvb_find_line_end = libwireshark.tvb_find_line_end
        self.tvb_find_line_end.restype = LibGLib2.gint
        self.tvb_find_line_end.argtypes = [POINTER(self.tvbuff_t),
                                           LibGLib2.gint,
                                           c_int,
                                           POINTER(LibGLib2.gint),
                                           LibGLib2.gboolean]

        # gint tvb_find_line_end_unquoted(tvbuff_t *tvb, const gint offset,
        #     int len, gint *next_offset);
        self.tvb_find_line_end_unquoted = libwireshark.tvb_find_line_end_unquoted
        self.tvb_find_line_end_unquoted.restype = LibGLib2.gint
        self.tvb_find_line_end_unquoted.argtypes = [POINTER(self.tvbuff_t),
                                                    LibGLib2.gint,
                                                    c_int,
                                                    POINTER(LibGLib2.gint)]

        # gint tvb_skip_wsp(tvbuff_t *tvb, const gint offset,
        #     const gint maxlength);
        self.tvb_skip_wsp = libwireshark.tvb_skip_wsp
        self.tvb_skip_wsp.restype = LibGLib2.gint
        self.tvb_skip_wsp.argtypes = [POINTER(self.tvbuff_t),
                                      LibGLib2.gint,
                                      LibGLib2.gint]

        # gint tvb_skip_wsp_return(tvbuff_t *tvb, const gint offset);
        self.tvb_skip_wsp_return = libwireshark.tvb_skip_wsp_return
        self.tvb_skip_wsp_return.restype = LibGLib2.gint
        self.tvb_skip_wsp_return.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.gint]

        # int tvb_get_token_len(tvbuff_t *tvb, const gint offset, int len, gint
        # *next_offset, const gboolean desegment);
        self.tvb_get_token_len = libwireshark.tvb_get_token_len
        self.tvb_get_token_len.restype = c_int
        self.tvb_get_token_len.argtypes = [POINTER(self.tvbuff_t),
                                           LibGLib2.gint,
                                           c_int,
                                           POINTER(LibGLib2.gint),
                                           LibGLib2.gboolean]

        # gint tvb_strneql(tvbuff_t *tvb, const gint offset,
        #     const gchar *str, const size_t size);
        self.tvb_strneql = libwireshark.tvb_strneql
        self.tvb_strneql.restype = LibGLib2.gint
        self.tvb_strneql.argtypes = [POINTER(self.tvbuff_t),
                                     LibGLib2.gint,
                                     LibGLib2.gchar_p,
                                     c_size_t]

        # gint tvb_strncaseeql(tvbuff_t *tvb, const gint offset,
        #     const gchar *str, const size_t size);
        self.tvb_strncaseeql = libwireshark.tvb_strncaseeql
        self.tvb_strncaseeql.restype = LibGLib2.gint
        self.tvb_strncaseeql.argtypes = [POINTER(self.tvbuff_t),
                                         LibGLib2.gint,
                                         LibGLib2.gchar_p,
                                         c_size_t]

        # gint tvb_memeql(tvbuff_t *tvb, const gint offset,
        #     const guint8 *str, size_t size);
        self.tvb_memeql = libwireshark.tvb_memeql
        self.tvb_memeql.restype = LibGLib2.gint
        self.tvb_memeql.argtypes = [POINTER(self.tvbuff_t),
                                    LibGLib2.gint,
                                    POINTER(LibGLib2.guint8),
                                    c_size_t]

        # gchar *tvb_bytes_to_str_punct(wmem_allocator_t *scope, tvbuff_t *tvb, const gint offset,
        #     const gint len, const gchar punct);
        self.tvb_bytes_to_str_punct = libwireshark.tvb_bytes_to_str_punct
        self.tvb_bytes_to_str_punct.restype = LibGLib2.gchar_p
        self.tvb_bytes_to_str_punct.argtypes = [POINTER(self.wmem_allocator_t),
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                LibGLib2.gchar]

        # gchar *tvb_bytes_to_str(wmem_allocator_t *allocator, tvbuff_t *tvb,
        #     const gint offset, const gint len);
        self.tvb_bytes_to_str = libwireshark.tvb_bytes_to_str
        self.tvb_bytes_to_str.restype = LibGLib2.gchar_p
        self.tvb_bytes_to_str.argtypes = [POINTER(self.wmem_allocator_t),
                                          POINTER(self.tvbuff_t),
                                          LibGLib2.gint,
                                          LibGLib2.gint]

        # const gchar *tvb_bcd_dig_to_wmem_packet_str(tvbuff_t *tvb,
        #     const gint offset, const gint len, const dgt_set_t *dgt,
        #     gboolean skip_first);
        self.tvb_bcd_dig_to_wmem_packet_str = libwireshark.tvb_bcd_dig_to_wmem_packet_str
        self.tvb_bcd_dig_to_wmem_packet_str.restype = LibGLib2.gchar_p
        self.tvb_bcd_dig_to_wmem_packet_str.argtypes = [
            POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, POINTER(
                self.dgt_set_t), LibGLib2.gboolean]

        # gint tvb_find_tvb(tvbuff_t *haystack_tvb, tvbuff_t *needle_tvb,
        #     const gint haystack_offset);
        self.tvb_find_tvb = libwireshark.tvb_find_tvb
        self.tvb_find_tvb.restype = LibGLib2.gint
        self.tvb_find_tvb.argtypes = [POINTER(self.tvbuff_t),
                                      POINTER(self.tvbuff_t),
                                      LibGLib2.gint]

        # tvbuff_t *tvb_uncompress(tvbuff_t *tvb, const int offset,
        #     int comprlen);
        self.tvb_uncompress = libwireshark.tvb_uncompress
        self.tvb_uncompress.restype = POINTER(self.tvbuff_t)
        self.tvb_uncompress.argtypes = [POINTER(self.tvbuff_t), c_int, c_int]

        # tvbuff_t *tvb_child_uncompress(tvbuff_t *parent, tvbuff_t *tvb,
        #     const int offset, int comprlen);
        self.tvb_child_uncompress = libwireshark.tvb_child_uncompress
        self.tvb_child_uncompress.restype = POINTER(self.tvbuff_t)
        self.tvb_child_uncompress.argtypes = [POINTER(self.tvbuff_t),
                                              POINTER(self.tvbuff_t),
                                              c_int,
                                              c_int]

        # tvbuff_t *tvb_uncompress_brotli(tvbuff_t *tvb, const int offset,
        #     int comprlen);
        self.tvb_uncompress_brotli = libwireshark.tvb_uncompress_brotli
        self.tvb_uncompress_brotli.restype = POINTER(self.tvbuff_t)
        self.tvb_uncompress_brotli.argtypes = [
            POINTER(self.tvbuff_t), c_int, c_int]

        # tvbuff_t *tvb_child_uncompress_brotli(tvbuff_t *parent, tvbuff_t *tvb,
        #     const int offset, int comprlen);
        self.tvb_child_uncompress_brotli = libwireshark.tvb_child_uncompress_brotli
        self.tvb_child_uncompress_brotli.restype = POINTER(self.tvbuff_t)
        self.tvb_child_uncompress_brotli.argtypes = [POINTER(self.tvbuff_t),
                                                     POINTER(self.tvbuff_t),
                                                     c_int,
                                                     c_int]

        # tvbuff_t *tvb_uncompress_lz77(tvbuff_t *tvb,
        #     const int offset, int comprlen);
        self.tvb_uncompress_lz77 = libwireshark.tvb_uncompress_lz77
        self.tvb_uncompress_lz77.restype = POINTER(self.tvbuff_t)
        self.tvb_uncompress_lz77.argtypes = [
            POINTER(self.tvbuff_t), c_int, c_int]

        # tvbuff_t *tvb_child_uncompress_lz77(tvbuff_t *parent,
        #      tvbuff_t *tvb, const int offset, int comprlen);
        self.tvb_child_uncompress_lz77 = libwireshark.tvb_child_uncompress_lz77
        self.tvb_child_uncompress_lz77.restype = POINTER(self.tvbuff_t)
        self.tvb_child_uncompress_lz77.argtypes = [POINTER(self.tvbuff_t),
                                                   POINTER(self.tvbuff_t),
                                                   c_int,
                                                   c_int]

        # tvbuff_t *tvb_uncompress_lz77huff(tvbuff_t *tvb,
        #     const int offset, int comprlen);
        self.tvb_uncompress_lz77huff = libwireshark.tvb_uncompress_lz77huff
        self.tvb_uncompress_lz77huff.restype = POINTER(self.tvbuff_t)
        self.tvb_uncompress_lz77huff.argtypes = [
            POINTER(self.tvbuff_t), c_int, c_int]

        # tvbuff_t *tvb_child_uncompress_lz77huff(tvbuff_t *parent,
        #     tvbuff_t *tvb, const int offset, int comprlen);
        self.tvb_child_uncompress_lz77huff = libwireshark.tvb_child_uncompress_lz77huff
        self.tvb_child_uncompress_lz77huff.restype = POINTER(self.tvbuff_t)
        self.tvb_child_uncompress_lz77huff.argtypes = [POINTER(self.tvbuff_t),
                                                       POINTER(self.tvbuff_t),
                                                       c_int,
                                                       c_int]

        # tvbuff_t *tvb_uncompress_lznt1(tvbuff_t *tvb,
        #     const int offset, int comprlen);
        self.tvb_uncompress_lznt1 = libwireshark.tvb_uncompress_lznt1
        self.tvb_uncompress_lznt1.restype = POINTER(self.tvbuff_t)
        self.tvb_uncompress_lznt1.argtypes = [
            POINTER(self.tvbuff_t), c_int, c_int]

        # tvbuff_t *tvb_child_uncompress_lznt1(tvbuff_t *parent,
        #     tvbuff_t *tvb, const int offset, int comprlen);
        self.tvb_child_uncompress_lznt1 = libwireshark.tvb_child_uncompress_lznt1
        self.tvb_child_uncompress_lznt1.restype = POINTER(self.tvbuff_t)
        self.tvb_child_uncompress_lznt1.argtypes = [POINTER(self.tvbuff_t),
                                                    POINTER(self.tvbuff_t),
                                                    c_int,
                                                    c_int]

        # guint tvb_get_varint(tvbuff_t *tvb, guint offset, guint maxlen, guint64
        # *value, const guint encoding);
        self.tvb_get_varint = libwireshark.tvb_get_varint
        self.tvb_get_varint.restype = LibGLib2.guint
        self.tvb_get_varint.argtypes = [POINTER(self.tvbuff_t),
                                        LibGLib2.guint,
                                        POINTER(LibGLib2.guint64),
                                        LibGLib2.guint]

        # range_t *range_empty(wmem_allocator_t *scope);
        self.range_empty = libwireshark.range_empty
        self.range_empty.restype = POINTER(self.range_t)
        self.range_empty.argtypes = [POINTER(self.wmem_allocator_t)]

        # convert_ret_t range_convert_str(wmem_allocator_t *scope, range_t **range, const gchar *es,
        #     guint32 max_value);
        self.range_convert_str = libwireshark.range_convert_str
        self.range_convert_str.restype = self.convert_ret_t
        self.range_convert_str.argtypes = [POINTER(self.wmem_allocator_t),
                                           POINTER(POINTER(self.range_t)),
                                           LibGLib2.gchar_p,
                                           LibGLib2.guint32]

        # convert_ret_t range_convert_str_work(wmem_allocator_t *scope, range_t **range, const gchar *es,
        #     guint32 max_value, gboolean err_on_max);
        self.range_convert_str_work = libwireshark.range_convert_str_work
        self.range_convert_str_work.restype = self.convert_ret_t
        self.range_convert_str_work.argtypes = [POINTER(self.wmem_allocator_t),
                                                POINTER(POINTER(self.range_t)),
                                                LibGLib2.gchar_p,
                                                LibGLib2.guint32,
                                                LibGLib2.gboolean]

        # gboolean value_is_in_range(range_t *range, guint32 val);
        self.value_is_in_range = libwireshark.value_is_in_range
        self.value_is_in_range.restype = LibGLib2.gboolean
        self.value_is_in_range.argtypes = [
            POINTER(self.range_t), LibGLib2.guint32]

        # gboolean range_add_value(wmem_allocator_t *scope, range_t **range,
        # guint32 val);
        self.range_add_value = libwireshark.range_add_value
        self.range_add_value.restype = LibGLib2.gboolean
        self.range_add_value.argtypes = [POINTER(self.wmem_allocator_t),
                                         POINTER(POINTER(self.range_t)),
                                         LibGLib2.guint32]

        # gboolean range_remove_value(wmem_allocator_t *scope, range_t **range,
        # guint32 val);
        self.range_remove_value = libwireshark.range_remove_value
        self.range_remove_value.restype = LibGLib2.gboolean
        self.range_remove_value.argtypes = [POINTER(self.wmem_allocator_t),
                                            POINTER(POINTER(self.range_t)),
                                            LibGLib2.guint32]

        # gboolean ranges_are_equal(range_t *a, range_t *b);
        self.ranges_are_equal = libwireshark.ranges_are_equal
        self.ranges_are_equal.restype = LibGLib2.gboolean
        self.ranges_are_equal.argtypes = [
            POINTER(
                self.range_t), POINTER(
                self.range_t)]

        # void range_foreach(range_t *range, void (*callback)(guint32 val,
        # gpointer ptr), gpointer ptr);
        self.range_foreach = libwireshark.range_foreach
        self.range_foreach.restype = None
        self.range_foreach.argtypes = [
            POINTER(
                self.range_t),
            CFUNCTYPE(
                None,
                LibGLib2.guint32,
                LibGLib2.gpointer,
                LibGLib2.gpointer),
            LibGLib2.gpointer]

        # char *range_convert_range(wmem_allocator_t *scope, const range_t
        # *range);
        self.range_convert_range = libwireshark.range_convert_range
        self.range_convert_range.restype = c_char_p
        self.range_convert_range.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.range_t)]

        # range_t *range_copy(wmem_allocator_t *scope, range_t *src);
        self.range_copy = libwireshark.range_copy
        self.range_copy.restype = POINTER(self.range_t)
        self.range_copy.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.range_t)]

        # char string_to_name_resolve(const char *string, struct _e_addr_resolve
        # *name_resolve);
        self.string_to_name_resolve = libwireshark.string_to_name_resolve
        self.string_to_name_resolve.restype = c_char
        self.string_to_name_resolve.argtypes = [
            c_char_p, POINTER(self._e_addr_resolve)]

        # e_prefs prefs;
        self.prefs = self.e_prefs.in_dll(libwireshark, 'prefs')

        # void prefs_reset(void);
        self.prefs_reset = libwireshark.prefs_reset
        self.prefs_reset.restype = None
        self.prefs_reset.argtypes = []

        # void prefs_set_gui_theme_is_dark(gboolean is_dark);
        self.prefs_set_gui_theme_is_dark = libwireshark.prefs_set_gui_theme_is_dark
        self.prefs_set_gui_theme_is_dark.restype = None
        self.prefs_set_gui_theme_is_dark.argtypes = [LibGLib2.gboolean]

        # module_t *prefs_register_protocol(int id, void (*apply_cb)(void));
        self.prefs_register_protocol = libwireshark.prefs_register_protocol
        self.prefs_register_protocol.restype = POINTER(self.module_t)
        self.prefs_register_protocol.argtypes = [c_int, CFUNCTYPE(None)]

        # void prefs_register_module_alias(const char *name, module_t *module);
        self.prefs_register_module_alias = libwireshark.prefs_register_module_alias
        self.prefs_register_module_alias.restype = None
        self.prefs_register_module_alias.argtypes = [
            c_char_p, POINTER(self.module_t)]

        # module_t *prefs_register_stat(const char *name, const char *title,
        #     const char *description, void (*apply_cb)(void));
        self.prefs_register_stat = libwireshark.prefs_register_stat
        self.prefs_register_stat.restype = POINTER(self.module_t)
        self.prefs_register_stat.argtypes = [c_char_p,
                                             c_char_p,
                                             c_char_p,
                                             CFUNCTYPE(None)]

        # module_t *prefs_register_codec(const char *name, const char *title,
        #     const char *description, void (*apply_cb)(void));
        self.prefs_register_codec = libwireshark.prefs_register_codec
        self.prefs_register_codec.restype = POINTER(self.module_t)
        self.prefs_register_codec.argtypes = [c_char_p,
                                              c_char_p,
                                              c_char_p,
                                              CFUNCTYPE(None)]

        # module_t *prefs_register_protocol_subtree(const char *subtree, int id,
        #     void (*apply_cb)(void));
        self.prefs_register_protocol_subtree = libwireshark.prefs_register_protocol_subtree
        self.prefs_register_protocol_subtree.restype = POINTER(self.module_t)
        self.prefs_register_protocol_subtree.argtypes = [
            c_char_p, c_int, CFUNCTYPE(None)]

        # gboolean prefs_module_has_submodules(module_t *module);
        self.prefs_module_has_submodules = libwireshark.prefs_module_has_submodules
        self.prefs_module_has_submodules.restype = LibGLib2.gboolean
        self.prefs_module_has_submodules.argtypes = [POINTER(self.module_t)]

        # guint prefs_modules_foreach(module_cb callback, gpointer user_data);
        self.prefs_modules_foreach = libwireshark.prefs_modules_foreach
        self.prefs_modules_foreach.restype = LibGLib2.guint
        self.prefs_modules_foreach.argtypes = [
            self.module_cb, LibGLib2.gpointer]

        # guint prefs_modules_foreach_submodules(module_t *module, module_cb
        # callback, gpointer user_data);
        self.prefs_modules_foreach_submodules = libwireshark.prefs_modules_foreach_submodules
        self.prefs_modules_foreach_submodules.restype = LibGLib2.guint
        self.prefs_modules_foreach_submodules.argtypes = [
            POINTER(self.module_t), self.module_cb, LibGLib2.gpointer]

        # void prefs_apply_all(void);
        self.prefs_apply_all = libwireshark.prefs_apply_all
        self.prefs_apply_all.restype = None
        self.prefs_apply_all.argtypes = []

        # void prefs_apply(module_t *module);
        self.prefs_apply = libwireshark.prefs_apply
        self.prefs_apply.restype = None
        self.prefs_apply.argtypes = [POINTER(self.module_t)]

        # gboolean prefs_is_registered_protocol(const char *name);
        self.prefs_is_registered_protocol = libwireshark.prefs_is_registered_protocol
        self.prefs_is_registered_protocol.restype = LibGLib2.gboolean
        self.prefs_is_registered_protocol.argtypes = [c_char_p]

        # const char *prefs_get_title_by_name(const char *name);
        self.prefs_get_title_by_name = libwireshark.prefs_get_title_by_name
        self.prefs_get_title_by_name.restype = c_char_p
        self.prefs_get_title_by_name.argtypes = [c_char_p]

        # module_t *prefs_find_module(const char *name);
        self.prefs_find_module = libwireshark.prefs_find_module
        self.prefs_find_module.restype = POINTER(self.module_t)
        self.prefs_find_module.argtypes = [c_char_p]

        # pref_t *prefs_find_preference(module_t * module, const char *pref);
        self.prefs_find_preference = libwireshark.prefs_find_preference
        self.prefs_find_preference.restype = POINTER(self.pref_t)
        self.prefs_find_preference.argtypes = [
            POINTER(self.module_t), c_char_p]

        # void prefs_register_uint_preference(module_t *module, const char *name,
        # const char *title, const char *description, guint base, guint *var);
        self.prefs_register_uint_preference = libwireshark.prefs_register_uint_preference
        self.prefs_register_uint_preference.restype = None
        self.prefs_register_uint_preference.argtypes = [
            POINTER(
                self.module_t),
            c_char_p,
            c_char_p,
            c_char_p,
            LibGLib2.guint,
            POINTER(
                LibGLib2.guint)]

        # void prefs_register_bool_preference(module_t *module, const char *name,
        #     const char *title, const char *description, gboolean *var);
        self.prefs_register_bool_preference = libwireshark.prefs_register_bool_preference
        self.prefs_register_bool_preference.restype = None
        self.prefs_register_bool_preference.argtypes = [POINTER(self.module_t),
                                                        c_char_p,
                                                        c_char_p,
                                                        c_char_p,
                                                        LibGLib2.gboolean]

        # void prefs_register_enum_preference(module_t *module, const char *name,
        #     const char *title, const char *description, gint *var,
        #     const enum_val_t *enumvals, gboolean radio_buttons);
        self.prefs_register_enum_preference = libwireshark.prefs_register_enum_preference
        self.prefs_register_enum_preference.restype = None
        self.prefs_register_enum_preference.argtypes = [
            POINTER(
                self.module_t), c_char_p, c_char_p, c_char_p, POINTER(
                LibGLib2.gint), POINTER(
                self.enum_val_t), LibGLib2.gboolean]

        # void prefs_register_string_preference(module_t *module, const char *name,
        #     const char *title, const char *description, const char **var);
        self.prefs_register_string_preference = libwireshark.prefs_register_string_preference
        self.prefs_register_string_preference.restype = None
        self.prefs_register_string_preference.argtypes = [POINTER(self.module_t),
                                                          c_char_p,
                                                          c_char_p,
                                                          c_char_p,
                                                          POINTER(c_char_p)]

        # void prefs_register_filename_preference(module_t *module, const char *name,
        # const char *title, const char *description, const char **var, gboolean
        # for_writing);
        self.prefs_register_filename_preference = libwireshark.prefs_register_filename_preference
        self.prefs_register_filename_preference.restype = None
        self.prefs_register_filename_preference.argtypes = [
            POINTER(
                self.module_t),
            c_char_p,
            c_char_p,
            c_char_p,
            POINTER(c_char_p),
            LibGLib2.gboolean]

        # void prefs_register_directory_preference(module_t *module, const char *name,
        #     const char *title, const char *description, const char **var);
        self.prefs_register_directory_preference = libwireshark.prefs_register_directory_preference
        self.prefs_register_directory_preference.restype = None
        self.prefs_register_directory_preference.argtypes = [
            POINTER(self.module_t), c_char_p, c_char_p, c_char_p, POINTER(c_char_p)]

        # void prefs_register_range_preference(module_t *module, const char *name,
        #     const char *title, const char *description, range_t **var,
        #     guint32 max_value);
        self.prefs_register_range_preference = libwireshark.prefs_register_range_preference
        self.prefs_register_range_preference.restype = None
        self.prefs_register_range_preference.argtypes = [
            POINTER(
                self.module_t), c_char_p, c_char_p, c_char_p, POINTER(
                POINTER(
                    self.range_t)), LibGLib2.guint32]

        # void prefs_register_static_text_preference(module_t *module, const char *name,
        #     const char *title, const char *description);
        self.prefs_register_static_text_preference = libwireshark.prefs_register_static_text_preference
        self.prefs_register_static_text_preference.restype = None
        self.prefs_register_static_text_preference.argtypes = [
            POINTER(self.module_t), c_char_p, c_char_p, c_char_p]

        # void prefs_register_uat_preference(module_t *module,
        # const char *name, const char* title, const char *description,  struct
        # epan_uat* uat);
        self.prefs_register_uat_preference = libwireshark.prefs_register_uat_preference
        self.prefs_register_uat_preference.restype = None
        self.prefs_register_uat_preference.argtypes = [POINTER(self.module_t),
                                                       c_char_p,
                                                       c_char_p,
                                                       c_char_p,
                                                       POINTER(self.epan_uat)]

        # void prefs_register_uat_preference_qt(module_t *module,
        # const char *name, const char* title, const char *description,  struct
        # epan_uat* uat);
        self.prefs_register_uat_preference_qt = libwireshark.prefs_register_uat_preference_qt
        self.prefs_register_uat_preference_qt.restype = None
        self.prefs_register_uat_preference_qt.argtypes = [
            POINTER(
                self.module_t), c_char_p, c_char_p, c_char_p, POINTER(
                self.epan_uat)]

        # void prefs_register_obsolete_preference(module_t *module,
        #     const char *name);
        self.prefs_register_obsolete_preference = libwireshark.prefs_register_obsolete_preference
        self.prefs_register_obsolete_preference.restype = None
        self.prefs_register_obsolete_preference.argtypes = [
            POINTER(self.module_t), c_char_p]

        # guint prefs_pref_foreach(module_t *module, pref_cb callback,
        #     gpointer user_data);
        self.prefs_pref_foreach = libwireshark.prefs_pref_foreach
        self.prefs_pref_foreach.restype = LibGLib2.guint
        self.prefs_pref_foreach.argtypes = [
            POINTER(self.module_t), self.pref_cb, LibGLib2.gpointer]

        # GList *prefs_get_string_list(const gchar *str);
        self.prefs_get_string_list = libwireshark.prefs_get_string_list
        self.prefs_get_string_list.restype = POINTER(LibGLib2.GList)
        self.prefs_get_string_list.argtypes = [LibGLib2.gchar_p]

        # void prefs_clear_string_list(GList *sl);
        self.prefs_clear_string_list = libwireshark.prefs_clear_string_list
        self.prefs_clear_string_list.restype = None
        self.prefs_clear_string_list.argtypes = [POINTER(LibGLib2.GList)]

        # const char *prefs_pref_type_name(pref_t *pref);
        self.prefs_pref_type_name = libwireshark.prefs_pref_type_name
        self.prefs_pref_type_name.restype = c_char_p
        self.prefs_pref_type_name.argtypes = [POINTER(self.pref_t)]

        # char *prefs_pref_type_description(pref_t *pref);
        self.prefs_pref_type_description = libwireshark.prefs_pref_type_description
        self.prefs_pref_type_description.restype = c_char_p
        self.prefs_pref_type_description.argtypes = [POINTER(self.pref_t)]

        # char *prefs_pref_to_str(pref_t *pref, pref_source_t source);
        self.prefs_pref_to_str = libwireshark.prefs_pref_to_str
        self.prefs_pref_to_str.restype = c_char_p
        self.prefs_pref_to_str.argtypes = [
            POINTER(self.pref_t), self.pref_source_t]

        # int write_prefs(char **);
        self.write_prefs = libwireshark.write_prefs
        self.write_prefs.restype = c_int
        self.write_prefs.argtypes = [POINTER(c_char_p)]

        # prefs_set_pref_e prefs_set_pref(char *prefarg, char **errmsg);
        self.prefs_set_pref = libwireshark.prefs_set_pref
        self.prefs_set_pref.restype = self.prefs_set_pref_e
        self.prefs_set_pref.argtypes = [c_char_p, POINTER(c_char_p)]

        # guint prefs_get_uint_value(const char *module_name, const char*
        # pref_name);
        self.prefs_get_uint_value = libwireshark.prefs_get_uint_value
        self.prefs_get_uint_value.restype = LibGLib2.guint
        self.prefs_get_uint_value.argtypes = [c_char_p, c_char_p]

        # range_t* prefs_get_range_value(const char *module_name, const char*
        # pref_name);
        self.prefs_get_range_value = libwireshark.prefs_get_range_value
        self.prefs_get_range_value.restype = POINTER(self.range_t)
        self.prefs_get_range_value.argtypes = [c_char_p, c_char_p]

        # gboolean prefs_is_capture_device_hidden(const char *name);
        self.prefs_is_capture_device_hidden = libwireshark.prefs_is_capture_device_hidden
        self.prefs_is_capture_device_hidden.restype = LibGLib2.gboolean
        self.prefs_is_capture_device_hidden.argtypes = [c_char_p]

        # gboolean prefs_capture_device_monitor_mode(const char *name);
        self.prefs_capture_device_monitor_mode = libwireshark.prefs_capture_device_monitor_mode
        self.prefs_capture_device_monitor_mode.restype = LibGLib2.gboolean
        self.prefs_capture_device_monitor_mode.argtypes = [c_char_p]

        # gboolean prefs_capture_options_dialog_column_is_visible(const gchar
        # *column);
        self.prefs_capture_options_dialog_column_is_visible = libwireshark.prefs_capture_options_dialog_column_is_visible
        self.prefs_capture_options_dialog_column_is_visible.restype = LibGLib2.gboolean
        self.prefs_capture_options_dialog_column_is_visible.argtypes = [
            LibGLib2.gchar_p]

        # gboolean prefs_has_layout_pane_content (layout_pane_content_e
        # layout_pane_content);
        self.prefs_has_layout_pane_content = libwireshark.prefs_has_layout_pane_content
        self.prefs_has_layout_pane_content.restype = LibGLib2.gboolean
        self.prefs_has_layout_pane_content.argtypes = [
            self.layout_pane_content_e]

        # gint frame_data_compare(const struct epan_session *epan, const
        # frame_data *fdata1, const frame_data *fdata2, int field);
        self.frame_data_compare = libwireshark.frame_data_compare
        self.frame_data_compare.restype = LibGLib2.gint
        self.frame_data_compare.argtypes = [POINTER(self.epan_session),
                                            POINTER(self.frame_data),
                                            POINTER(self.frame_data),
                                            c_int]

        # void frame_data_reset(frame_data *fdata);
        self.frame_data_reset = libwireshark.frame_data_reset
        self.frame_data_reset.restype = None
        self.frame_data_reset.argtypes = [POINTER(self.frame_data)]

        # void frame_data_destroy(frame_data *fdata);
        self.frame_data_destroy = libwireshark.frame_data_destroy
        self.frame_data_destroy.restype = None
        self.frame_data_destroy.argtypes = [POINTER(self.frame_data)]

        # void frame_data_init(frame_data *fdata, guint32 num,
        #                 const wtap_rec *rec, gint64 offset,
        #                 guint32 cum_bytes);
        self.frame_data_init = libwireshark.frame_data_init
        self.frame_data_init.restype = None
        self.frame_data_init.argtypes = [POINTER(self.frame_data),
                                         LibGLib2.guint32,
                                         POINTER(LibWiretap.wtap_rec),
                                         LibGLib2.gint64,
                                         LibGLib2.guint32]

        # void frame_data_set_before_dissect(frame_data *fdata,
        #                 nstime_t *elapsed_time,
        #                 const frame_data **frame_ref,
        #                 const frame_data *prev_dis);
        self.frame_data_set_before_dissect = libwireshark.frame_data_set_before_dissect
        self.frame_data_set_before_dissect.restype = None
        self.frame_data_set_before_dissect.argtypes = [
            POINTER(
                self.frame_data), POINTER(
                LibWSUtil.nstime_t), POINTER(
                POINTER(
                    self.frame_data)), POINTER(
                        self.frame_data)]

        # void frame_data_set_after_dissect(frame_data *fdata,
        #                 guint32 *cum_bytes);
        self.frame_data_set_after_dissect = libwireshark.frame_data_set_after_dissect
        self.frame_data_set_after_dissect.restype = None
        self.frame_data_set_after_dissect.argtypes = [
            POINTER(self.frame_data), POINTER(LibGLib2.guint32)]

        # gboolean epan_init(register_cb cb, void *client_data, gboolean
        # load_plugins);
        self.epan_init = libwireshark.epan_init
        self.epan_init.restype = LibGLib2.gboolean
        self.epan_init.argtypes = [
            self.register_cb, c_void_p, LibGLib2.gboolean]

        # e_prefs *epan_load_settings(void);
        self.epan_load_settings = libwireshark.epan_load_settings
        self.epan_load_settings.restype = POINTER(self.e_prefs)
        self.epan_load_settings.argtypes = []

        # void epan_cleanup(void);
        self.epan_cleanup = libwireshark.epan_cleanup
        self.epan_cleanup.restype = None
        self.epan_cleanup.argtypes = []

        # void epan_register_plugin(const epan_plugin *plugin);
        self.epan_register_plugin = libwireshark.epan_register_plugin
        self.epan_register_plugin.restype = None
        self.epan_register_plugin.argtypes = [POINTER(self.epan_plugin)]

        # epan_t *epan_new(struct packet_provider_data *prov,
        #     const struct packet_provider_funcs *funcs);
        self.epan_new = libwireshark.epan_new
        self.epan_new.restype = POINTER(self.epan_t)
        self.epan_new.argtypes = [POINTER(self.packet_provider_data),
                                  POINTER(self.packet_provider_funcs)]

        # const char *epan_get_user_comment(const epan_t *session, const
        # frame_data *fd);
        self.epan_get_user_comment = libwireshark.epan_get_user_comment
        self.epan_get_user_comment.restype = c_char_p
        self.epan_get_user_comment.argtypes = [
            POINTER(
                self.epan_t), POINTER(
                self.frame_data)]

        # const char *epan_get_interface_name(const epan_t *session, guint32
        # interface_id);
        self.epan_get_interface_name = libwireshark.epan_get_interface_name
        self.epan_get_interface_name.restype = c_char_p
        self.epan_get_interface_name.argtypes = [
            POINTER(self.epan_t), LibGLib2.guint32]

        # const char *epan_get_interface_description(const epan_t *session,
        # guint32 interface_id);
        self.epan_get_interface_description = libwireshark.epan_get_interface_description
        self.epan_get_interface_description.restype = c_char_p
        self.epan_get_interface_description.argtypes = [
            POINTER(self.epan_t), LibGLib2.guint32]

        # void epan_free(epan_t *session);
        self.epan_free = libwireshark.epan_free
        self.epan_free.restype = None
        self.epan_free.argtypes = [POINTER(self.epan_t)]

        # const gchar* epan_get_version(void);
        self.epan_get_version = libwireshark.epan_get_version
        self.epan_get_version.restype = LibGLib2.gchar_p
        self.epan_get_version.argtypes = []

        # void epan_get_version_number(int *major, int *minor, int *micro);
        self.epan_get_version_number = libwireshark.epan_get_version_number
        self.epan_get_version_number.restype = None
        self.epan_get_version_number.argtypes = [POINTER(c_int),
                                                 POINTER(c_int),
                                                 POINTER(c_int)]

        # void epan_dissect_init(epan_dissect_t *edt, epan_t *session, const
        # gboolean create_proto_tree, const gboolean proto_tree_visible);
        self.epan_dissect_init = libwireshark.epan_dissect_init
        self.epan_dissect_init.restype = None
        self.epan_dissect_init.argtypes = [POINTER(self.epan_dissect_t),
                                           POINTER(self.epan_t),
                                           LibGLib2.gboolean,
                                           LibGLib2.gboolean]

        # epan_dissect_t* epan_dissect_new(epan_t *session, const gboolean
        # create_proto_tree, const gboolean proto_tree_visible);
        self.epan_dissect_new = libwireshark.epan_dissect_new
        self.epan_dissect_new.restype = POINTER(self.epan_dissect_t)
        self.epan_dissect_new.argtypes = [
            POINTER(
                self.epan_t),
            LibGLib2.gboolean,
            LibGLib2.gboolean]

        # void epan_dissect_reset(epan_dissect_t *edt);
        self.epan_dissect_reset = libwireshark.epan_dissect_reset
        self.epan_dissect_reset.restype = None
        self.epan_dissect_reset.argtypes = [POINTER(self.epan_dissect_t)]

        # void epan_dissect_fake_protocols(epan_dissect_t *edt, const gboolean
        # fake_protocols);
        self.epan_dissect_fake_protocols = libwireshark.epan_dissect_fake_protocols
        self.epan_dissect_fake_protocols.restype = None
        self.epan_dissect_fake_protocols.argtypes = [
            POINTER(self.epan_dissect_t), LibGLib2.gboolean]

        # void epan_dissect_run(epan_dissect_t *edt, int file_type_subtype,
        #         wtap_rec *rec, tvbuff_t *tvb, frame_data *fd,
        #         struct epan_column_info *cinfo);
        self.epan_dissect_run = libwireshark.epan_dissect_run
        self.epan_dissect_run.restype = None
        self.epan_dissect_run.argtypes = [POINTER(self.epan_dissect_t),
                                          c_int,
                                          POINTER(LibWiretap.wtap_rec),
                                          POINTER(self.tvbuff_t),
                                          POINTER(self.frame_data),
                                          POINTER(self.epan_column_info)]

        # void epan_dissect_run_with_taps(epan_dissect_t *edt, int file_type_subtype,
        #         wtap_rec *rec, tvbuff_t *tvb, frame_data *fd,
        #         struct epan_column_info *cinfo);
        self.epan_dissect_run_with_taps = libwireshark.epan_dissect_run_with_taps
        self.epan_dissect_run_with_taps.restype = None
        self.epan_dissect_run_with_taps.argtypes = [
            POINTER(
                self.epan_dissect_t), c_int, POINTER(
                LibWiretap.wtap_rec), POINTER(
                self.tvbuff_t), POINTER(
                    self.frame_data), POINTER(
                        self.epan_column_info)]

        # void epan_dissect_file_run(epan_dissect_t *edt, wtap_rec *rec,
        # tvbuff_t *tvb, frame_data *fd, struct epan_column_info *cinfo);
        self.epan_dissect_file_run = libwireshark.epan_dissect_file_run
        self.epan_dissect_file_run.restype = None
        self.epan_dissect_file_run.argtypes = [POINTER(self.epan_dissect_t),
                                               POINTER(LibWiretap.wtap_rec),
                                               POINTER(self.tvbuff_t),
                                               POINTER(self.frame_data),
                                               POINTER(self.epan_column_info)]

        # void epan_dissect_file_run_with_taps(epan_dissect_t *edt, wtap_rec *rec,
        # tvbuff_t *tvb, frame_data *fd, struct epan_column_info *cinfo);
        self.epan_dissect_file_run_with_taps = libwireshark.epan_dissect_file_run_with_taps
        self.epan_dissect_file_run_with_taps.restype = None
        self.epan_dissect_file_run_with_taps.argtypes = [
            POINTER(
                self.epan_dissect_t), POINTER(
                LibWiretap.wtap_rec), POINTER(
                self.tvbuff_t), POINTER(
                    self.frame_data), POINTER(
                        self.epan_column_info)]

        # void epan_dissect_prime_with_dfilter(epan_dissect_t *edt, const struct
        # epan_dfilter *dfcode);
        self.epan_dissect_prime_with_dfilter = libwireshark.epan_dissect_prime_with_dfilter
        self.epan_dissect_prime_with_dfilter.restype = None
        self.epan_dissect_prime_with_dfilter.argtypes = [
            POINTER(self.epan_dissect_t), POINTER(self.epan_dfilter)]

        # void epan_dissect_prime_with_hfid(epan_dissect_t *edt, int hfid);
        self.epan_dissect_prime_with_hfid = libwireshark.epan_dissect_prime_with_hfid
        self.epan_dissect_prime_with_hfid.restype = None
        self.epan_dissect_prime_with_hfid.argtypes = [
            POINTER(self.epan_dissect_t), c_int]

        # void epan_dissect_prime_with_hfid_array(epan_dissect_t *edt, GArray
        # *hfids);
        self.epan_dissect_prime_with_hfid_array = libwireshark.epan_dissect_prime_with_hfid_array
        self.epan_dissect_prime_with_hfid_array.restype = None
        self.epan_dissect_prime_with_hfid_array.argtypes = [
            POINTER(self.epan_dissect_t), POINTER(LibGLib2.GArray)]

        # void epan_dissect_fill_in_columns(epan_dissect_t *edt, const gboolean
        # fill_col_exprs, const gboolean fill_fd_colums);
        self.epan_dissect_fill_in_columns = libwireshark.epan_dissect_fill_in_columns
        self.epan_dissect_fill_in_columns.restype = None
        self.epan_dissect_fill_in_columns.argtypes = [
            POINTER(self.epan_dissect_t), LibGLib2.gboolean, LibGLib2.gboolean]

        # gboolean epan_dissect_packet_contains_field(epan_dissect_t* edt,
        #                                    const char *field_name);
        self.epan_dissect_packet_contains_field = libwireshark.epan_dissect_packet_contains_field
        self.epan_dissect_packet_contains_field.restype = LibGLib2.gboolean
        self.epan_dissect_packet_contains_field.argtypes = [
            POINTER(self.epan_dissect_t), c_char_p]

        # void epan_dissect_cleanup(epan_dissect_t* edt);
        self.epan_dissect_cleanup = libwireshark.epan_dissect_cleanup
        self.epan_dissect_cleanup.restype = None
        self.epan_dissect_cleanup.argtypes = [POINTER(self.epan_dissect_t)]

        # void epan_dissect_free(epan_dissect_t* edt);
        self.epan_dissect_free = libwireshark.epan_dissect_free
        self.epan_dissect_free.restype = None
        self.epan_dissect_free.argtypes = [POINTER(self.epan_dissect_t)]

        # void epan_get_compiled_version_info(GString *str);
        self.epan_get_compiled_version_info = libwireshark.epan_get_compiled_version_info
        self.epan_get_compiled_version_info.restype = None
        self.epan_get_compiled_version_info.argtypes = [
            POINTER(LibGLib2.GString)]

        # void epan_get_runtime_version_info(GString *str);
        self.epan_get_runtime_version_info = libwireshark.epan_get_runtime_version_info
        self.epan_get_runtime_version_info.restype = None
        self.epan_get_runtime_version_info.argtypes = [
            POINTER(LibGLib2.GString)]

        # const gchar *val_to_str(const guint32 val, const value_string *vs, const
        # char *fmt);
        self.val_to_str = libwireshark.val_to_str
        self.val_to_str.restype = LibGLib2.gchar_p
        self.val_to_str.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string), c_char_p]

        # gchar *val_to_str_wmem(wmem_allocator_t *scope, const guint32 val, const
        # value_string *vs, const char *fmt);
        self.val_to_str_wmem = libwireshark.val_to_str_wmem
        self.val_to_str_wmem.restype = LibGLib2.gchar_p
        self.val_to_str_wmem.argtypes = [POINTER(self.wmem_allocator_t),
                                         LibGLib2.guint32,
                                         POINTER(self.value_string),
                                         c_char_p]

        # const gchar *val_to_str_const(const guint32 val, const value_string *vs,
        # const char *unknown_str);
        self.val_to_str_const = libwireshark.val_to_str_const
        self.val_to_str_const.restype = LibGLib2.gchar_p
        self.val_to_str_const.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string), c_char_p]

        # const gchar *try_val_to_str(const guint32 val, const value_string
        # *vs);
        self.try_val_to_str = libwireshark.try_val_to_str
        self.try_val_to_str.restype = LibGLib2.gchar_p
        self.try_val_to_str.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string)]

        # const gchar *try_val_to_str_idx(const guint32 val, const value_string
        # *vs, gint *idx);
        self.try_val_to_str_idx = libwireshark.try_val_to_str_idx
        self.try_val_to_str_idx.restype = LibGLib2.gchar_p
        self.try_val_to_str_idx.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string), POINTER(
                LibGLib2.gint)]

        # const gchar *val64_to_str(const guint64 val, const val64_string *vs,
        # const char *fmt);
        self.val64_to_str = libwireshark.val64_to_str
        self.val64_to_str.restype = LibGLib2.gchar_p
        self.val64_to_str.argtypes = [
            LibGLib2.guint64, POINTER(
                self.val64_string), c_char_p]

        # const gchar *val64_to_str_const(const guint64 val, const val64_string
        # *vs, const char *unknown_str);
        self.val64_to_str_const = libwireshark.val64_to_str_const
        self.val64_to_str_const.restype = LibGLib2.gchar_p
        self.val64_to_str_const.argtypes = [
            LibGLib2.guint64, POINTER(
                self.val64_string), c_char_p]

        # const gchar *try_val64_to_str(const guint64 val, const val64_string
        # *vs);
        self.try_val64_to_str = libwireshark.try_val64_to_str
        self.try_val64_to_str.restype = LibGLib2.gchar_p
        self.try_val64_to_str.argtypes = [
            LibGLib2.guint64, POINTER(
                self.val64_string)]

        # const gchar *try_val64_to_str_idx(const guint64 val, const val64_string
        # *vs, gint *idx);
        self.try_val64_to_str_idx = libwireshark.try_val64_to_str_idx
        self.try_val64_to_str_idx.restype = LibGLib2.gchar_p
        self.try_val64_to_str_idx.argtypes = [
            LibGLib2.guint64, POINTER(
                self.val64_string), POINTER(
                LibGLib2.gint)]

        # guint32 str_to_val(const gchar *val, const value_string *vs, const
        # guint32 err_val);
        self.str_to_val = libwireshark.str_to_val
        self.str_to_val.restype = LibGLib2.guint32
        self.str_to_val.argtypes = [
            LibGLib2.gchar_p, POINTER(
                self.value_string), LibGLib2.guint32]

        # gint str_to_val_idx(const gchar *val, const value_string *vs);
        self.str_to_val_idx = libwireshark.str_to_val_idx
        self.str_to_val_idx.restype = LibGLib2.gint
        self.str_to_val_idx.argtypes = [
            LibGLib2.gchar_p, POINTER(
                self.value_string)]

        # const value_string *_try_val_to_str_ext_init(const guint32 val,
        # value_string_ext *vse);
        self._try_val_to_str_ext_init = libwireshark._try_val_to_str_ext_init
        self._try_val_to_str_ext_init.restype = POINTER(self.value_string)
        self._try_val_to_str_ext_init.argtypes = [
            LibGLib2.guint32, POINTER(self.value_string_ext)]

        # value_string_ext *value_string_ext_new(const value_string *vs, guint
        # vs_tot_num_entries, const gchar *vs_name);
        self.value_string_ext_new = libwireshark.value_string_ext_new
        self.value_string_ext_new.restype = POINTER(self.value_string_ext)
        self.value_string_ext_new.argtypes = [
            POINTER(
                self.value_string),
            LibGLib2.guint,
            LibGLib2.gchar_p]

        # void value_string_ext_free(value_string_ext *vse);
        self.value_string_ext_free = libwireshark.value_string_ext_free
        self.value_string_ext_free.restype = None
        self.value_string_ext_free.argtypes = [POINTER(self.value_string_ext)]

        # const gchar *val_to_str_ext(const guint32 val, value_string_ext *vse,
        # const char *fmt);
        self.val_to_str_ext = libwireshark.val_to_str_ext
        self.val_to_str_ext.restype = LibGLib2.gchar_p
        self.val_to_str_ext.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string_ext), c_char_p]

        # gchar *val_to_str_ext_wmem(wmem_allocator_t *scope, const guint32 val,
        # value_string_ext *vse, const char *fmt);
        self.val_to_str_ext_wmem = libwireshark.val_to_str_ext_wmem
        self.val_to_str_ext_wmem.restype = LibGLib2.gchar_p
        self.val_to_str_ext_wmem.argtypes = [POINTER(self.wmem_allocator_t),
                                             LibGLib2.guint32,
                                             POINTER(self.value_string_ext),
                                             c_char_p]

        # const gchar *val_to_str_ext_const(const guint32 val, value_string_ext
        # *vs, const char *unknown_str);
        self.val_to_str_ext_const = libwireshark.val_to_str_ext_const
        self.val_to_str_ext_const.restype = LibGLib2.gchar_p
        self.val_to_str_ext_const.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string_ext), c_char_p]

        # const gchar *try_val_to_str_ext(const guint32 val, value_string_ext
        # *vse);
        self.try_val_to_str_ext = libwireshark.try_val_to_str_ext
        self.try_val_to_str_ext.restype = LibGLib2.gchar_p
        self.try_val_to_str_ext.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string_ext)]

        # const gchar *try_val_to_str_idx_ext(const guint32 val, value_string_ext
        # *vse, gint *idx);
        self.try_val_to_str_idx_ext = libwireshark.try_val_to_str_idx_ext
        self.try_val_to_str_idx_ext.restype = LibGLib2.gchar_p
        self.try_val_to_str_idx_ext.argtypes = [
            LibGLib2.guint32, POINTER(
                self.value_string_ext), POINTER(
                LibGLib2.gint)]

        # const val64_string *_try_val64_to_str_ext_init(const guint64 val,
        # val64_string_ext *vse);
        self._try_val64_to_str_ext_init = libwireshark._try_val64_to_str_ext_init
        self._try_val64_to_str_ext_init.restype = POINTER(self.val64_string)
        self._try_val64_to_str_ext_init.argtypes = [
            LibGLib2.guint64, POINTER(self.val64_string_ext)]

        # val64_string_ext *val64_string_ext_new(const val64_string *vs, guint
        # vs_tot_num_entries, const gchar *vs_name);
        self.val64_string_ext_new = libwireshark.val64_string_ext_new
        self.val64_string_ext_new.restype = POINTER(self.val64_string_ext)
        self.val64_string_ext_new.argtypes = [
            POINTER(
                self.val64_string),
            LibGLib2.guint,
            LibGLib2.gchar_p]

        # void val64_string_ext_free(val64_string_ext *vse);
        self.val64_string_ext_free = libwireshark.val64_string_ext_free
        self.val64_string_ext_free.restype = None
        self.val64_string_ext_free.argtypes = [POINTER(self.val64_string_ext)]

        # const gchar *val64_to_str_ext(const guint64 val, val64_string_ext *vse,
        # const char *fmt);
        self.val64_to_str_ext = libwireshark.val64_to_str_ext
        self.val64_to_str_ext.restype = LibGLib2.gchar_p
        self.val64_to_str_ext.argtypes = [
            LibGLib2.guint64, POINTER(
                self.val64_string_ext), c_char_p]

        # gchar *val64_to_str_ext_wmem(wmem_allocator_t *scope, const guint64 val,
        # val64_string_ext *vse, const char *fmt);
        self.val64_to_str_ext_wmem = libwireshark.val64_to_str_ext_wmem
        self.val64_to_str_ext_wmem.restype = LibGLib2.gchar_p
        self.val64_to_str_ext_wmem.argtypes = [POINTER(self.wmem_allocator_t),
                                               LibGLib2.guint64,
                                               POINTER(self.val64_string_ext),
                                               c_char_p]

        # const gchar *val64_to_str_ext_const(const guint64 val, val64_string_ext
        # *vs, const char *unknown_str);
        self.val64_to_str_ext_const = libwireshark.val64_to_str_ext_const
        self.val64_to_str_ext_const.restype = LibGLib2.gchar_p
        self.val64_to_str_ext_const.argtypes = [
            LibGLib2.guint64, POINTER(self.val64_string_ext), c_char_p]

        # const gchar *try_val64_to_str_ext(const guint64 val, val64_string_ext
        # *vse);
        self.try_val64_to_str_ext = libwireshark.try_val64_to_str_ext
        self.try_val64_to_str_ext.restype = LibGLib2.gchar_p
        self.try_val64_to_str_ext.argtypes = [
            LibGLib2.guint64, POINTER(self.val64_string_ext)]

        # const gchar *try_val64_to_str_idx_ext(const guint64 val,
        # val64_string_ext *vse, gint *idx);
        self.try_val64_to_str_idx_ext = libwireshark.try_val64_to_str_idx_ext
        self.try_val64_to_str_idx_ext.restype = LibGLib2.gchar_p
        self.try_val64_to_str_idx_ext.argtypes = [
            LibGLib2.guint64, POINTER(
                self.val64_string_ext), POINTER(
                LibGLib2.gint)]

        # const gchar *str_to_str(const gchar *val, const string_string *vs, const
        # char *fmt);
        self.str_to_str = libwireshark.str_to_str
        self.str_to_str.restype = LibGLib2.gchar_p
        self.str_to_str.argtypes = [
            LibGLib2.gchar_p, POINTER(
                self.string_string), c_char_p]

        # const gchar *try_str_to_str(const gchar *val, const string_string
        # *vs);
        self.try_str_to_str = libwireshark.try_str_to_str
        self.try_str_to_str.restype = LibGLib2.gchar_p
        self.try_str_to_str.argtypes = [
            LibGLib2.gchar_p, POINTER(
                self.string_string)]

        # const gchar *try_str_to_str_idx(const gchar *val, const string_string
        # *vs, gint *idx);
        self.try_str_to_str_idx = libwireshark.try_str_to_str_idx
        self.try_str_to_str_idx.restype = LibGLib2.gchar_p
        self.try_str_to_str_idx.argtypes = [
            LibGLib2.gchar_p, POINTER(
                self.string_string), POINTER(
                LibGLib2.gint)]

        # const gchar *rval_to_str(const guint32 val, const range_string *rs,
        # const char *fmt);
        self.rval_to_str = libwireshark.rval_to_str
        self.rval_to_str.restype = LibGLib2.gchar_p
        self.rval_to_str.argtypes = [
            LibGLib2.guint32, POINTER(
                self.range_string), c_char_p]

        # const gchar *rval_to_str_const(const guint32 val, const range_string
        # *rs, const char *unknown_str);
        self.rval_to_str_const = libwireshark.rval_to_str_const
        self.rval_to_str_const.restype = LibGLib2.gchar_p
        self.rval_to_str_const.argtypes = [
            LibGLib2.guint32, POINTER(
                self.range_string), c_char_p]

        # const gchar *try_rval_to_str(const guint32 val, const range_string
        # *rs);
        self.try_rval_to_str = libwireshark.try_rval_to_str
        self.try_rval_to_str.restype = LibGLib2.gchar_p
        self.try_rval_to_str.argtypes = [
            LibGLib2.guint32, POINTER(
                self.range_string)]

        # const gchar *try_rval_to_str_idx(const guint32 val, const range_string
        # *rs, gint *idx);
        self.try_rval_to_str_idx = libwireshark.try_rval_to_str_idx
        self.try_rval_to_str_idx.restype = LibGLib2.gchar_p
        self.try_rval_to_str_idx.argtypes = [
            LibGLib2.guint32, POINTER(
                self.range_string), POINTER(
                LibGLib2.gint)]

        # const gchar *try_rval64_to_str(const guint64 val, const range_string
        # *rs);
        self.try_rval64_to_str = libwireshark.try_rval64_to_str
        self.try_rval64_to_str.restype = LibGLib2.gchar_p
        self.try_rval64_to_str.argtypes = [
            LibGLib2.guint64, POINTER(self.range_string)]

        # const gchar *try_rval64_to_str_idx(const guint64 val, const range_string
        # *rs, gint *idx);
        self.try_rval64_to_str_idx = libwireshark.try_rval64_to_str_idx
        self.try_rval64_to_str_idx.restype = LibGLib2.gchar_p
        self.try_rval64_to_str_idx.argtypes = [
            LibGLib2.guint64, POINTER(
                self.range_string), POINTER(
                LibGLib2.gint)]

        # const gchar *bytesval_to_str(const guint8 *val, const size_t val_len,
        # const bytes_string *bs, const char *fmt);
        self.bytesval_to_str = libwireshark.bytesval_to_str
        self.bytesval_to_str.restype = LibGLib2.gchar_p
        self.bytesval_to_str.argtypes = [
            POINTER(LibGLib2.guint8),
            c_size_t,
            POINTER(self.bytes_string),
            c_char_p]

        # const gchar *try_bytesval_to_str(const guint8 *val, const size_t
        # val_len, const bytes_string *bs);
        self.try_bytesval_to_str = libwireshark.try_bytesval_to_str
        self.try_bytesval_to_str.restype = LibGLib2.gchar_p
        self.try_bytesval_to_str.argtypes = [
            POINTER(LibGLib2.guint8),
            c_size_t,
            POINTER(self.bytes_string)]

        # const gchar *bytesprefix_to_str(const guint8 *haystack, const size_t
        # haystack_len, const bytes_string *bs, const char *fmt);
        self.bytesprefix_to_str = libwireshark.bytesprefix_to_str
        self.bytesprefix_to_str.restype = LibGLib2.gchar_p
        self.bytesprefix_to_str.argtypes = [
            POINTER(LibGLib2.guint8),
            c_size_t,
            POINTER(self.bytes_string),
            c_char_p]

        # const gchar *try_bytesprefix_to_str(const guint8 *haystack, const size_t
        # haystack_len, const bytes_string *bs);
        self.try_bytesprefix_to_str = libwireshark.try_bytesprefix_to_str
        self.try_bytesprefix_to_str.restype = LibGLib2.gchar_p
        self.try_bytesprefix_to_str.argtypes = [
            POINTER(LibGLib2.guint8), c_size_t, POINTER(self.bytes_string)]

        # const true_false_string tfs_true_false;
        self.tfs_true_false = self.true_false_string.in_dll(
            libwireshark, 'tfs_true_false')

        # const true_false_string tfs_yes_no;
        self.tfs_yes_no = self.true_false_string.in_dll(
            libwireshark, 'tfs_yes_no')

        # const true_false_string tfs_no_yes;
        self.tfs_no_yes = self.true_false_string.in_dll(
            libwireshark, 'tfs_no_yes')

        # const true_false_string tfs_set_notset;
        self.tfs_set_notset = self.true_false_string.in_dll(
            libwireshark, 'tfs_set_notset')

        # const true_false_string tfs_enabled_disabled;
        self.tfs_enabled_disabled = self.true_false_string.in_dll(
            libwireshark, 'tfs_enabled_disabled')

        # const true_false_string tfs_disabled_enabled;
        self.tfs_disabled_enabled = self.true_false_string.in_dll(
            libwireshark, 'tfs_disabled_enabled')

        # const true_false_string tfs_ok_error;
        self.tfs_ok_error = self.true_false_string.in_dll(
            libwireshark, 'tfs_ok_error')

        # const true_false_string tfs_error_ok;
        self.tfs_error_ok = self.true_false_string.in_dll(
            libwireshark, 'tfs_error_ok')

        # const true_false_string tfs_success_fail;
        self.tfs_success_fail = self.true_false_string.in_dll(
            libwireshark, 'tfs_success_fail')

        # const true_false_string tfs_fail_success;
        self.tfs_fail_success = self.true_false_string.in_dll(
            libwireshark, 'tfs_fail_success')

        # const true_false_string tfs_on_off;
        self.tfs_on_off = self.true_false_string.in_dll(
            libwireshark, 'tfs_on_off')

        # const true_false_string tfs_ack_nack;
        self.tfs_ack_nack = self.true_false_string.in_dll(
            libwireshark, 'tfs_ack_nack')

        # const true_false_string tfs_odd_even;
        self.tfs_odd_even = self.true_false_string.in_dll(
            libwireshark, 'tfs_odd_even')

        # const true_false_string tfs_allow_block;
        self.tfs_allow_block = self.true_false_string.in_dll(
            libwireshark, 'tfs_allow_block')

        # const true_false_string tfs_restricted_allowed;
        self.tfs_restricted_allowed = self.true_false_string.in_dll(
            libwireshark, 'tfs_restricted_allowed')

        # const true_false_string tfs_restricted_not_restricted;
        self.tfs_restricted_not_restricted = self.true_false_string.in_dll(
            libwireshark, 'tfs_restricted_not_restricted')

        # const true_false_string tfs_accept_reject;
        self.tfs_accept_reject = self.true_false_string.in_dll(
            libwireshark, 'tfs_accept_reject')

        # const true_false_string tfs_more_nomore;
        self.tfs_more_nomore = self.true_false_string.in_dll(
            libwireshark, 'tfs_more_nomore')

        # const true_false_string tfs_present_absent;
        self.tfs_present_absent = self.true_false_string.in_dll(
            libwireshark, 'tfs_present_absent')

        # const true_false_string tfs_present_not_present;
        self.tfs_present_not_present = self.true_false_string.in_dll(
            libwireshark, 'tfs_present_not_present')

        # const true_false_string tfs_active_inactive;
        self.tfs_active_inactive = self.true_false_string.in_dll(
            libwireshark, 'tfs_active_inactive')

        # const true_false_string tfs_activated_deactivated;
        self.tfs_activated_deactivated = self.true_false_string.in_dll(
            libwireshark, 'tfs_activated_deactivated')

        # const true_false_string tfs_found_not_found;
        self.tfs_found_not_found = self.true_false_string.in_dll(
            libwireshark, 'tfs_found_not_found')

        # const true_false_string tfs_command_response;
        self.tfs_command_response = self.true_false_string.in_dll(
            libwireshark, 'tfs_command_response')

        # const true_false_string tfs_response_command;
        self.tfs_response_command = self.true_false_string.in_dll(
            libwireshark, 'tfs_response_command')

        # const true_false_string tfs_capable_not_capable;
        self.tfs_capable_not_capable = self.true_false_string.in_dll(
            libwireshark, 'tfs_capable_not_capable')

        # const true_false_string tfs_supported_not_supported;
        self.tfs_supported_not_supported = self.true_false_string.in_dll(
            libwireshark, 'tfs_supported_not_supported')

        # const true_false_string tfs_not_supported_supported;
        self.tfs_not_supported_supported = self.true_false_string.in_dll(
            libwireshark, 'tfs_not_supported_supported')

        # const true_false_string tfs_used_notused;
        self.tfs_used_notused = self.true_false_string.in_dll(
            libwireshark, 'tfs_used_notused')

        # const true_false_string tfs_high_low;
        self.tfs_high_low = self.true_false_string.in_dll(
            libwireshark, 'tfs_high_low')

        # const true_false_string tfs_high_normal;
        self.tfs_high_normal = self.true_false_string.in_dll(
            libwireshark, 'tfs_high_normal')

        # const true_false_string tfs_low_normal;
        self.tfs_low_normal = self.true_false_string.in_dll(
            libwireshark, 'tfs_low_normal')

        # const true_false_string tfs_pressed_not_pressed;
        self.tfs_pressed_not_pressed = self.true_false_string.in_dll(
            libwireshark, 'tfs_pressed_not_pressed')

        # const true_false_string tfs_implemented_not_implemented;
        self.tfs_implemented_not_implemented = self.true_false_string.in_dll(
            libwireshark, 'tfs_implemented_not_implemented')

        # const true_false_string tfs_requested_not_requested;
        self.tfs_requested_not_requested = self.true_false_string.in_dll(
            libwireshark, 'tfs_requested_not_requested')

        # const true_false_string tfs_reliable_not_reliable;
        self.tfs_reliable_not_reliable = self.true_false_string.in_dll(
            libwireshark, 'tfs_reliable_not_reliable')

        # const true_false_string tfs_allowed_not_allowed;
        self.tfs_allowed_not_allowed = self.true_false_string.in_dll(
            libwireshark, 'tfs_allowed_not_allowed')

        # const true_false_string tfs_not_allowed_allowed;
        self.tfs_not_allowed_allowed = self.true_false_string.in_dll(
            libwireshark, 'tfs_not_allowed_allowed')

        # const true_false_string tfs_accepted_not_accepted;
        self.tfs_accepted_not_accepted = self.true_false_string.in_dll(
            libwireshark, 'tfs_accepted_not_accepted')

        # const true_false_string tfs_detected_not_detected;
        self.tfs_detected_not_detected = self.true_false_string.in_dll(
            libwireshark, 'tfs_detected_not_detected')

        # const true_false_string tfs_available_not_available;
        self.tfs_available_not_available = self.true_false_string.in_dll(
            libwireshark, 'tfs_available_not_available')

        # const true_false_string tfs_shared_independent;
        self.tfs_shared_independent = self.true_false_string.in_dll(
            libwireshark, 'tfs_shared_independent')

        # const true_false_string tfs_valid_invalid;
        self.tfs_valid_invalid = self.true_false_string.in_dll(
            libwireshark, 'tfs_valid_invalid')

        # const true_false_string tfs_invalid_valid;
        self.tfs_invalid_valid = self.true_false_string.in_dll(
            libwireshark, 'tfs_invalid_valid')

        # const true_false_string tfs_group_unique_name;
        self.tfs_group_unique_name = self.true_false_string.in_dll(
            libwireshark, 'tfs_group_unique_name')

        # const true_false_string tfs_inuse_not_inuse;
        self.tfs_inuse_not_inuse = self.true_false_string.in_dll(
            libwireshark, 'tfs_inuse_not_inuse')

        # const true_false_string tfs_critical_not_critical;
        self.tfs_critical_not_critical = self.true_false_string.in_dll(
            libwireshark, 'tfs_critical_not_critical')

        # const true_false_string tfs_complete_incomplete;
        self.tfs_complete_incomplete = self.true_false_string.in_dll(
            libwireshark, 'tfs_complete_incomplete')

        # const true_false_string tfs_valid_not_valid;
        self.tfs_valid_not_valid = self.true_false_string.in_dll(
            libwireshark, 'tfs_valid_not_valid')

        # const true_false_string tfs_do_not_clear_clear;
        self.tfs_do_not_clear_clear = self.true_false_string.in_dll(
            libwireshark, 'tfs_do_not_clear_clear')

        # const true_false_string tfs_confirmed_unconfirmed;
        self.tfs_confirmed_unconfirmed = self.true_false_string.in_dll(
            libwireshark, 'tfs_confirmed_unconfirmed')

        # const true_false_string tfs_enforced_not_enforced;
        self.tfs_enforced_not_enforced = self.true_false_string.in_dll(
            libwireshark, 'tfs_enforced_not_enforced')

        # const true_false_string tfs_possible_not_possible;
        self.tfs_possible_not_possible = self.true_false_string.in_dll(
            libwireshark, 'tfs_possible_not_possible')

        # const true_false_string tfs_required_not_required;
        self.tfs_required_not_required = self.true_false_string.in_dll(
            libwireshark, 'tfs_required_not_required')

        # const true_false_string tfs_registered_not_registered;
        self.tfs_registered_not_registered = self.true_false_string.in_dll(
            libwireshark, 'tfs_registered_not_registered')

        # const true_false_string tfs_provisioned_not_provisioned;
        self.tfs_provisioned_not_provisioned = self.true_false_string.in_dll(
            libwireshark, 'tfs_provisioned_not_provisioned')

        # const true_false_string tfs_included_not_included;
        self.tfs_included_not_included = self.true_false_string.in_dll(
            libwireshark, 'tfs_included_not_included')

        # const true_false_string tfs_allocated_by_receiver_sender;
        self.tfs_allocated_by_receiver_sender = self.true_false_string.in_dll(
            libwireshark, 'tfs_allocated_by_receiver_sender')

        # const true_false_string tfs_asynchronous_synchronous;
        self.tfs_asynchronous_synchronous = self.true_false_string.in_dll(
            libwireshark, 'tfs_asynchronous_synchronous')

        # const true_false_string tfs_protocol_sensative_bit_transparent;
        self.tfs_protocol_sensative_bit_transparent = self.true_false_string.in_dll(
            libwireshark, 'tfs_protocol_sensative_bit_transparent')

        # const true_false_string tfs_full_half;
        self.tfs_full_half = self.true_false_string.in_dll(
            libwireshark, 'tfs_full_half')

        # const true_false_string tfs_acknowledged_not_acknowledged;
        self.tfs_acknowledged_not_acknowledged = self.true_false_string.in_dll(
            libwireshark, 'tfs_acknowledged_not_acknowledged')

        # const true_false_string tfs_segmentation_no_segmentation;
        self.tfs_segmentation_no_segmentation = self.true_false_string.in_dll(
            libwireshark, 'tfs_segmentation_no_segmentation')

        # const true_false_string tfs_response_request;
        self.tfs_response_request = self.true_false_string.in_dll(
            libwireshark, 'tfs_response_request')

        # const true_false_string tfs_defined_not_defined;
        self.tfs_defined_not_defined = self.true_false_string.in_dll(
            libwireshark, 'tfs_defined_not_defined')

        # const true_false_string tfs_constructed_primitive;
        self.tfs_constructed_primitive = self.true_false_string.in_dll(
            libwireshark, 'tfs_constructed_primitive')

        # const true_false_string tfs_client_server;
        self.tfs_client_server = self.true_false_string.in_dll(
            libwireshark, 'tfs_client_server')

        # const true_false_string tfs_server_client;
        self.tfs_server_client = self.true_false_string.in_dll(
            libwireshark, 'tfs_server_client')

        # const true_false_string tfs_preferred_no_preference;
        self.tfs_preferred_no_preference = self.true_false_string.in_dll(
            libwireshark, 'tfs_preferred_no_preference')

        # const true_false_string tfs_encrypt_do_not_encrypt;
        self.tfs_encrypt_do_not_encrypt = self.true_false_string.in_dll(
            libwireshark, 'tfs_encrypt_do_not_encrypt')

        # const true_false_string tfs_down_up;
        self.tfs_down_up = self.true_false_string.in_dll(
            libwireshark, 'tfs_down_up')

        # const true_false_string tfs_up_down;
        self.tfs_up_down = self.true_false_string.in_dll(
            libwireshark, 'tfs_up_down')

        # const true_false_string tfs_downlink_uplink;
        self.tfs_downlink_uplink = self.true_false_string.in_dll(
            libwireshark, 'tfs_downlink_uplink')

        # const true_false_string tfs_uplink_downlink;
        self.tfs_uplink_downlink = self.true_false_string.in_dll(
            libwireshark, 'tfs_uplink_downlink')

        # const true_false_string tfs_s2c_c2s;
        self.tfs_s2c_c2s = self.true_false_string.in_dll(
            libwireshark, 'tfs_s2c_c2s')

        # const true_false_string tfs_c2s_s2c;
        self.tfs_c2s_s2c = self.true_false_string.in_dll(
            libwireshark, 'tfs_c2s_s2c')

        # const true_false_string tfs_open_closed;
        self.tfs_open_closed = self.true_false_string.in_dll(
            libwireshark, 'tfs_open_closed')

        # const true_false_string tfs_external_internal;
        self.tfs_external_internal = self.true_false_string.in_dll(
            libwireshark, 'tfs_external_internal')

        # const true_false_string tfs_changed_not_changed;
        self.tfs_changed_not_changed = self.true_false_string.in_dll(
            libwireshark, 'tfs_changed_not_changed')

        # const true_false_string tfs_needed_not_needed;
        self.tfs_needed_not_needed = self.true_false_string.in_dll(
            libwireshark, 'tfs_needed_not_needed')

        # const true_false_string tfs_selected_not_selected;
        self.tfs_selected_not_selected = self.true_false_string.in_dll(
            libwireshark, 'tfs_selected_not_selected')

        # guint address_to_bytes(const address *addr, guint8 *buf, guint
        # buf_len);
        self.address_to_bytes = libwireshark.address_to_bytes
        self.address_to_bytes.restype = LibGLib2.guint
        self.address_to_bytes.argtypes = [
            POINTER(
                self.address), POINTER(
                LibGLib2.guint8), LibGLib2.guint]

        # const char* ftype_name(ftenum_t ftype);
        self.ftype_name = libwireshark.ftype_name
        self.ftype_name.restype = c_char_p
        self.ftype_name.argtypes = [self.ftenum_t]

        # const char* ftype_pretty_name(ftenum_t ftype);
        self.ftype_pretty_name = libwireshark.ftype_pretty_name
        self.ftype_pretty_name.restype = c_char_p
        self.ftype_pretty_name.argtypes = [self.ftenum_t]

        # gboolean ftype_can_slice(enum ftenum ftype);
        self.ftype_can_slice = libwireshark.ftype_can_slice
        self.ftype_can_slice.restype = LibGLib2.gboolean
        self.ftype_can_slice.argtypes = [self.ftenum]

        # gboolean ftype_can_eq(enum ftenum ftype);
        self.ftype_can_eq = libwireshark.ftype_can_eq
        self.ftype_can_eq.restype = LibGLib2.gboolean
        self.ftype_can_eq.argtypes = [self.ftenum]

        # gboolean ftype_can_ne(enum ftenum ftype);
        self.ftype_can_ne = libwireshark.ftype_can_ne
        self.ftype_can_ne.restype = LibGLib2.gboolean
        self.ftype_can_ne.argtypes = [self.ftenum]

        # gboolean ftype_can_gt(enum ftenum ftype);
        self.ftype_can_gt = libwireshark.ftype_can_gt
        self.ftype_can_gt.restype = LibGLib2.gboolean
        self.ftype_can_gt.argtypes = [self.ftenum]

        # gboolean ftype_can_ge(enum ftenum ftype);
        self.ftype_can_ge = libwireshark.ftype_can_ge
        self.ftype_can_ge.restype = LibGLib2.gboolean
        self.ftype_can_ge.argtypes = [self.ftenum]

        # gboolean ftype_can_lt(enum ftenum ftype);
        self.ftype_can_lt = libwireshark.ftype_can_lt
        self.ftype_can_lt.restype = LibGLib2.gboolean
        self.ftype_can_lt.argtypes = [self.ftenum]

        # gboolean ftype_can_le(enum ftenum ftype);
        self.ftype_can_le = libwireshark.ftype_can_le
        self.ftype_can_le.restype = LibGLib2.gboolean
        self.ftype_can_le.argtypes = [self.ftenum]

        # gboolean ftype_can_contains(enum ftenum ftype);
        self.ftype_can_contains = libwireshark.ftype_can_contains
        self.ftype_can_contains.restype = LibGLib2.gboolean
        self.ftype_can_contains.argtypes = [self.ftenum]

        # gboolean ftype_can_matches(enum ftenum ftype);
        self.ftype_can_matches = libwireshark.ftype_can_matches
        self.ftype_can_matches.restype = LibGLib2.gboolean
        self.ftype_can_matches.argtypes = [self.ftenum]

        # fvalue_t* fvalue_from_unparsed(ftenum_t ftype, const char *s, gboolean
        # allow_partial_value, gchar **err_msg);
        self.fvalue_from_unparsed = libwireshark.fvalue_from_unparsed
        self.fvalue_from_unparsed.restype = POINTER(self.fvalue_t)
        self.fvalue_from_unparsed.argtypes = [
            self.ftenum_t, c_char_p, LibGLib2.gboolean, POINTER(
                LibGLib2.gchar_p)]

        # int fvalue_string_repr_len(fvalue_t *fv, ftrepr_t rtype, int
        # field_display);
        self.fvalue_string_repr_len = libwireshark.fvalue_string_repr_len
        self.fvalue_string_repr_len.restype = c_int
        self.fvalue_string_repr_len.argtypes = [
            POINTER(self.fvalue_t), self.ftrepr_t, c_int]

        # char *fvalue_to_string_repr(wmem_allocator_t *scope, fvalue_t *fv,
        # ftrepr_t rtype, int field_display);
        self.fvalue_to_string_repr = libwireshark.fvalue_to_string_repr
        self.fvalue_to_string_repr.restype = c_char_p
        self.fvalue_to_string_repr.argtypes = [POINTER(self.wmem_allocator_t),
                                               POINTER(self.fvalue_t),
                                               self.ftrepr_t,
                                               c_int]

        # ftenum_t fvalue_type_ftenum(fvalue_t *fv);
        self.fvalue_type_ftenum = libwireshark.fvalue_type_ftenum
        self.fvalue_type_ftenum.restype = self.ftenum_t
        self.fvalue_type_ftenum.argtypes = [POINTER(self.fvalue_t)]

        # gpointer fvalue_get(fvalue_t *fv);
        self.fvalue_get = libwireshark.fvalue_get
        self.fvalue_get.restype = LibGLib2.gpointer
        self.fvalue_get.argtypes = [POINTER(self.fvalue_t)]

        # guint32 fvalue_get_uinteger(fvalue_t *fv);
        self.fvalue_get_uinteger = libwireshark.fvalue_get_uinteger
        self.fvalue_get_uinteger.restype = LibGLib2.guint32
        self.fvalue_get_uinteger.argtypes = [POINTER(self.fvalue_t)]

        # gint32 fvalue_get_sinteger(fvalue_t *fv);
        self.fvalue_get_sinteger = libwireshark.fvalue_get_sinteger
        self.fvalue_get_sinteger.restype = LibGLib2.gint32
        self.fvalue_get_sinteger.argtypes = [POINTER(self.fvalue_t)]

        # guint64 fvalue_get_uinteger64(fvalue_t *fv);
        self.fvalue_get_uinteger64 = libwireshark.fvalue_get_uinteger64
        self.fvalue_get_uinteger64.restype = LibGLib2.guint64
        self.fvalue_get_uinteger64.argtypes = [POINTER(self.fvalue_t)]

        # gint64 fvalue_get_sinteger64(fvalue_t *fv);
        self.fvalue_get_sinteger64 = libwireshark.fvalue_get_sinteger64
        self.fvalue_get_sinteger64.restype = LibGLib2.gint64
        self.fvalue_get_sinteger64.argtypes = [POINTER(self.fvalue_t)]

        # double fvalue_get_floating(fvalue_t *fv);
        self.fvalue_get_floating = libwireshark.fvalue_get_floating
        self.fvalue_get_floating.restype = c_double
        self.fvalue_get_floating.argtypes = [POINTER(self.fvalue_t)]

        # int hf_text_only;
        self.hf_text_only = c_int.in_dll(libwireshark, 'hf_text_only')

        # void proto_tree_children_foreach(proto_tree *tree,
        #     proto_tree_foreach_func func, gpointer data);
        self.proto_tree_children_foreach = libwireshark.proto_tree_children_foreach
        self.proto_tree_children_foreach.restype = None
        self.proto_tree_children_foreach.argtypes = [
            POINTER(
                self.proto_tree),
            self.proto_tree_foreach_func,
            LibGLib2.gpointer]

        # void proto_register_plugin(const proto_plugin *plugin);
        self.proto_register_plugin = libwireshark.proto_register_plugin
        self.proto_register_plugin.restype = None
        self.proto_register_plugin.argtypes = [POINTER(self.proto_plugin)]

        # gboolean proto_field_is_referenced(proto_tree *tree, int proto_id);
        self.proto_field_is_referenced = libwireshark.proto_field_is_referenced
        self.proto_field_is_referenced.restype = LibGLib2.gboolean
        self.proto_field_is_referenced.argtypes = [
            POINTER(self.proto_tree), c_int]

        # proto_tree* proto_item_add_subtree(proto_item *ti, const gint idx);
        self.proto_item_add_subtree = libwireshark.proto_item_add_subtree
        self.proto_item_add_subtree.restype = POINTER(self.proto_tree)
        self.proto_item_add_subtree.argtypes = [
            POINTER(self.proto_item), LibGLib2.gint]

        # proto_tree* proto_item_get_subtree(proto_item *ti);
        self.proto_item_get_subtree = libwireshark.proto_item_get_subtree
        self.proto_item_get_subtree.restype = POINTER(self.proto_tree)
        self.proto_item_get_subtree.argtypes = [POINTER(self.proto_item)]

        # proto_item* proto_item_get_parent(const proto_item *ti);
        self.proto_item_get_parent = libwireshark.proto_item_get_parent
        self.proto_item_get_parent.restype = POINTER(self.proto_item)
        self.proto_item_get_parent.argtypes = [POINTER(self.proto_item)]

        # proto_item* proto_item_get_parent_nth(proto_item *ti, int gen);
        self.proto_item_get_parent_nth = libwireshark.proto_item_get_parent_nth
        self.proto_item_get_parent_nth.restype = POINTER(self.proto_item)
        self.proto_item_get_parent_nth.argtypes = [
            POINTER(self.proto_item), c_int]

        # void proto_item_set_len(proto_item *ti, const gint length);
        self.proto_item_set_len = libwireshark.proto_item_set_len
        self.proto_item_set_len.restype = None
        self.proto_item_set_len.argtypes = [
            POINTER(self.proto_item), LibGLib2.gint]

        # void proto_item_set_end(proto_item *ti, tvbuff_t *tvb, gint end);
        self.proto_item_set_end = libwireshark.proto_item_set_end
        self.proto_item_set_end.restype = None
        self.proto_item_set_end.argtypes = [
            POINTER(
                self.proto_item), POINTER(
                self.tvbuff_t), LibGLib2.gint]

        # int proto_item_get_len(const proto_item *ti);
        self.proto_item_get_len = libwireshark.proto_item_get_len
        self.proto_item_get_len.restype = c_int
        self.proto_item_get_len.argtypes = [POINTER(self.proto_item)]

        # void proto_tree_free(proto_tree *tree);
        self.proto_tree_free = libwireshark.proto_tree_free
        self.proto_tree_free.restype = None
        self.proto_tree_free.argtypes = [POINTER(self.proto_tree)]

        # gboolean proto_tree_set_visible(proto_tree *tree, gboolean visible);
        self.proto_tree_set_visible = libwireshark.proto_tree_set_visible
        self.proto_tree_set_visible.restype = LibGLib2.gboolean
        self.proto_tree_set_visible.argtypes = [
            POINTER(self.proto_tree), LibGLib2.gboolean]

        # proto_item* proto_tree_get_parent(proto_tree *tree);
        self.proto_tree_get_parent = libwireshark.proto_tree_get_parent
        self.proto_tree_get_parent.restype = POINTER(self.proto_item)
        self.proto_tree_get_parent.argtypes = [POINTER(self.proto_tree)]

        # proto_tree *proto_tree_get_parent_tree(proto_tree *tree);
        self.proto_tree_get_parent_tree = libwireshark.proto_tree_get_parent_tree
        self.proto_tree_get_parent_tree.restype = POINTER(self.proto_tree)
        self.proto_tree_get_parent_tree.argtypes = [POINTER(self.proto_tree)]

        # proto_tree* proto_tree_get_root(proto_tree *tree);
        self.proto_tree_get_root = libwireshark.proto_tree_get_root
        self.proto_tree_get_root.restype = POINTER(self.proto_tree)
        self.proto_tree_get_root.argtypes = [POINTER(self.proto_tree)]

        # void proto_tree_move_item(proto_tree *tree, proto_item *fixed_item,
        # proto_item *item_to_move);
        self.proto_tree_move_item = libwireshark.proto_tree_move_item
        self.proto_tree_move_item.restype = None
        self.proto_tree_move_item.argtypes = [POINTER(self.proto_tree),
                                              POINTER(self.proto_item),
                                              POINTER(self.proto_item)]

        # void proto_tree_set_appendix(proto_tree *tree, tvbuff_t *tvb, gint
        # start, const gint length);
        self.proto_tree_set_appendix = libwireshark.proto_tree_set_appendix
        self.proto_tree_set_appendix.restype = None
        self.proto_tree_set_appendix.argtypes = [POINTER(self.proto_tree),
                                                 POINTER(self.tvbuff_t),
                                                 LibGLib2.gint,
                                                 LibGLib2.gint]

        # proto_item *proto_tree_add_item_new(proto_tree *tree, header_field_info *hfinfo, tvbuff_t *tvb,
        #     const gint start, gint length, const guint encoding);
        self.proto_tree_add_item_new = libwireshark.proto_tree_add_item_new
        self.proto_tree_add_item_new.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_new.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.header_field_info), POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint]

        # proto_item *proto_tree_add_item(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        #     const gint start, gint length, const guint encoding);
        self.proto_tree_add_item = libwireshark.proto_tree_add_item
        self.proto_tree_add_item.restype = POINTER(self.proto_item)
        self.proto_tree_add_item.argtypes = [POINTER(self.proto_tree),
                                             c_int,
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint,
                                             LibGLib2.guint]

        # proto_item *proto_tree_add_item_new_ret_length(proto_tree *tree, header_field_info *hfinfo, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, gint
        # *lenretval);
        self.proto_tree_add_item_new_ret_length = libwireshark.proto_tree_add_item_new_ret_length
        self.proto_tree_add_item_new_ret_length.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_item_new_ret_length.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.header_field_info), POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint, POINTER(
                    LibGLib2.gint)]

        # proto_item *proto_tree_add_item_ret_length(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, gint
        # *lenretval);
        self.proto_tree_add_item_ret_length = libwireshark.proto_tree_add_item_ret_length
        self.proto_tree_add_item_ret_length.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_length.argtypes = [POINTER(self.proto_tree),
                                                        c_int,
                                                        POINTER(self.tvbuff_t),
                                                        LibGLib2.gint,
                                                        LibGLib2.gint,
                                                        LibGLib2.guint,
                                                        POINTER(LibGLib2.gint)]

        # proto_item *proto_tree_add_item_ret_int(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, gint32 *retval);
        self.proto_tree_add_item_ret_int = libwireshark.proto_tree_add_item_ret_int
        self.proto_tree_add_item_ret_int.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_int.argtypes = [POINTER(self.proto_tree),
                                                     c_int,
                                                     POINTER(self.tvbuff_t),
                                                     LibGLib2.gint,
                                                     LibGLib2.gint,
                                                     LibGLib2.guint,
                                                     POINTER(LibGLib2.gint32)]

        # proto_item *proto_tree_add_item_ret_int64(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, gint64 *retval);
        self.proto_tree_add_item_ret_int64 = libwireshark.proto_tree_add_item_ret_int64
        self.proto_tree_add_item_ret_int64.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_int64.argtypes = [POINTER(self.proto_tree),
                                                       c_int,
                                                       POINTER(self.tvbuff_t),
                                                       LibGLib2.gint,
                                                       LibGLib2.gint,
                                                       LibGLib2.guint,
                                                       POINTER(LibGLib2.gint64)]

        # proto_item *proto_tree_add_item_ret_uint(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, guint32
        # *retval);
        self.proto_tree_add_item_ret_uint = libwireshark.proto_tree_add_item_ret_uint
        self.proto_tree_add_item_ret_uint.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_uint.argtypes = [POINTER(self.proto_tree),
                                                      c_int,
                                                      POINTER(self.tvbuff_t),
                                                      LibGLib2.gint,
                                                      LibGLib2.gint,
                                                      LibGLib2.guint,
                                                      POINTER(LibGLib2.guint32)]

        # proto_item *proto_tree_add_item_ret_uint64(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, guint64
        # *retval);
        self.proto_tree_add_item_ret_uint64 = libwireshark.proto_tree_add_item_ret_uint64
        self.proto_tree_add_item_ret_uint64.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_uint64.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint, POINTER(
                LibGLib2.guint64)]

        # proto_item *proto_tree_add_item_ret_varint(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, guint64 *retval,
        # gint *lenretval);
        self.proto_tree_add_item_ret_varint = libwireshark.proto_tree_add_item_ret_varint
        self.proto_tree_add_item_ret_varint.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_varint.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint, POINTER(
                LibGLib2.guint64), POINTER(
                    LibGLib2.gint)]

        # proto_item *proto_tree_add_item_ret_boolean(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        # const gint start, gint length, const guint encoding, gboolean
        # *retval);
        self.proto_tree_add_item_ret_boolean = libwireshark.proto_tree_add_item_ret_boolean
        self.proto_tree_add_item_ret_boolean.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_boolean.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint, POINTER(
                LibGLib2.gboolean)]

        # proto_item *proto_tree_add_item_ret_string_and_length(proto_tree *tree, int hfindex,
        #     tvbuff_t *tvb, const gint start, gint length, const guint encoding,
        #     wmem_allocator_t *scope, const guint8 **retval, gint *lenretval);
        self.proto_tree_add_item_ret_string_and_length = libwireshark.proto_tree_add_item_ret_string_and_length
        self.proto_tree_add_item_ret_string_and_length.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_item_ret_string_and_length.argtypes = [
            POINTER(self.proto_tree),
            c_int,
            POINTER(self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint,
            POINTER(self.wmem_allocator_t),
            POINTER(
                POINTER(LibGLib2.guint8)),
            POINTER(LibGLib2.gint)]

        # proto_item * proto_tree_add_item_ret_string(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        #     const gint start, gint length, const guint encoding,
        #     wmem_allocator_t *scope, const guint8 **retval);
        self.proto_tree_add_item_ret_string = libwireshark.proto_tree_add_item_ret_string
        self.proto_tree_add_item_ret_string.restype = POINTER(self.proto_item)
        self.proto_tree_add_item_ret_string.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint, POINTER(
                self.wmem_allocator_t), POINTER(
                    POINTER(
                        LibGLib2.guint8))]

        # proto_item *proto_tree_add_item_ret_display_string_and_length(proto_tree *tree, int hfindex,
        #     tvbuff_t *tvb,
        #     const gint start, gint length, const guint encoding,
        #     wmem_allocator_t *scope, char **retval, gint *lenretval);
        self.proto_tree_add_item_ret_display_string_and_length = libwireshark.proto_tree_add_item_ret_display_string_and_length
        self.proto_tree_add_item_ret_display_string_and_length.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_item_ret_display_string_and_length.argtypes = [
            POINTER(self.proto_item),
            c_int,
            POINTER(self.tvbuff_t),
            LibGLib2.gint,
            LibGLib2.gint,
            LibGLib2.guint,
            POINTER(self.wmem_allocator_t),
            POINTER(c_char_p),
            POINTER(LibGLib2.gint)]

        # proto_item *proto_tree_add_item_ret_display_string(proto_tree *tree, int hfindex,
        #     tvbuff_t *tvb,
        #     const gint start, gint length, const guint encoding,
        #     wmem_allocator_t *scope, char **retval);
        self.proto_tree_add_item_ret_display_string = libwireshark.proto_tree_add_item_ret_display_string
        self.proto_tree_add_item_ret_display_string.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_item_ret_display_string.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint, POINTER(
                self.wmem_allocator_t), POINTER(c_char_p)]

        # proto_item *proto_tree_add_item_ret_time_string(proto_tree *tree, int hfindex,
        # 	tvbuff_t *tvb,
        # 	const gint start, gint length, const guint encoding,
        # 	wmem_allocator_t *scope, char **retval);
        self.proto_tree_add_item_ret_time_string = libwireshark.proto_tree_add_item_ret_time_string
        self.proto_tree_add_item_ret_time_string.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_item_ret_time_string.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.guint, POINTER(
                self.wmem_allocator_t), POINTER(c_char_p)]

        # proto_tree *proto_tree_add_subtree(proto_tree *tree, tvbuff_t *tvb, gint start, gint length, gint idx,
        #     proto_item **tree_item, const char *text);
        self.proto_tree_add_subtree = libwireshark.proto_tree_add_subtree
        self.proto_tree_add_subtree.restype = POINTER(self.proto_tree)
        self.proto_tree_add_subtree.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, LibGLib2.gint, POINTER(
                POINTER(
                    self.proto_item)), c_char_p]

        # proto_item *proto_tree_add_bytes(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const guint8* start_ptr);
        self.proto_tree_add_bytes = libwireshark.proto_tree_add_bytes
        self.proto_tree_add_bytes.restype = POINTER(self.proto_item)
        self.proto_tree_add_bytes.argtypes = [POINTER(self.proto_tree),
                                              c_int,
                                              POINTER(self.tvbuff_t),
                                              LibGLib2.gint,
                                              LibGLib2.gint,
                                              POINTER(LibGLib2.guint8)]

        # proto_item *proto_tree_add_bytes_with_length(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const guint8 *start_ptr, gint ptr_length);
        self.proto_tree_add_bytes_with_length = libwireshark.proto_tree_add_bytes_with_length
        self.proto_tree_add_bytes_with_length.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_bytes_with_length.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.gint, LibGLib2.gint, POINTER(
                LibGLib2.guint8), LibGLib2.gint]

        # proto_item *proto_tree_add_bytes_item(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        #     const gint start, gint length, const guint encoding,
        #     GByteArray *retval, gint *endoff, gint *err);
        self.proto_tree_add_bytes_item = libwireshark.proto_tree_add_bytes_item
        self.proto_tree_add_bytes_item.restype = POINTER(self.proto_item)
        self.proto_tree_add_bytes_item.argtypes = [POINTER(self.proto_tree),
                                                   c_int,
                                                   POINTER(self.tvbuff_t),
                                                   LibGLib2.gint,
                                                   LibGLib2.gint,
                                                   LibGLib2.guint,
                                                   POINTER(LibGLib2.GByteArray),
                                                   POINTER(LibGLib2.gint),
                                                   POINTER(LibGLib2.gint)]

        # proto_item *proto_tree_add_time(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const nstime_t* value_ptr);
        self.proto_tree_add_time = libwireshark.proto_tree_add_time
        self.proto_tree_add_time.restype = POINTER(self.proto_item)
        self.proto_tree_add_time.argtypes = [POINTER(self.proto_tree),
                                             c_int,
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint,
                                             POINTER(LibWSUtil.nstime_t)]

        # proto_item *proto_tree_add_time_item(proto_tree *tree, int hfindex, tvbuff_t *tvb,
        #     const gint start, gint length, const guint encoding,
        #     nstime_t *retval, gint *endoff, gint *err);
        self.proto_tree_add_time_item = libwireshark.proto_tree_add_time_item
        self.proto_tree_add_time_item.restype = POINTER(self.proto_item)
        self.proto_tree_add_time_item.argtypes = [POINTER(self.proto_tree),
                                                  c_int,
                                                  POINTER(self.tvbuff_t),
                                                  LibGLib2.gint,
                                                  LibGLib2.gint,
                                                  LibGLib2.guint,
                                                  POINTER(LibWSUtil.nstime_t),
                                                  POINTER(LibGLib2.gint),
                                                  POINTER(LibGLib2.gint)]

        # proto_item *proto_tree_add_ipxnet(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, guint32 value);
        self.proto_tree_add_ipxnet = libwireshark.proto_tree_add_ipxnet
        self.proto_tree_add_ipxnet.restype = POINTER(self.proto_item)
        self.proto_tree_add_ipxnet.argtypes = [POINTER(self.proto_tree),
                                               c_int,
                                               POINTER(self.tvbuff_t),
                                               LibGLib2.gint,
                                               LibGLib2.gint,
                                               LibGLib2.guint32]

        # proto_item *proto_tree_add_ipv4(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, guint32 value);
        self.proto_tree_add_ipv4 = libwireshark.proto_tree_add_ipv4
        self.proto_tree_add_ipv4.restype = POINTER(self.proto_item)
        self.proto_tree_add_ipv4.argtypes = [POINTER(self.proto_tree),
                                             c_int,
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint,
                                             LibGLib2.guint32]

        # proto_item *proto_tree_add_ipv6(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const ws_in6_addr *value_ptr);
        self.proto_tree_add_ipv6 = libwireshark.proto_tree_add_ipv6
        self.proto_tree_add_ipv6.restype = POINTER(self.proto_item)
        self.proto_tree_add_ipv6.argtypes = [POINTER(self.proto_tree),
                                             c_int,
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint,
                                             POINTER(LibWSUtil.ws_in6_addr)]

        # proto_item *proto_tree_add_ether(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const guint8* value);
        self.proto_tree_add_ether = libwireshark.proto_tree_add_ether
        self.proto_tree_add_ether.restype = POINTER(self.proto_item)
        self.proto_tree_add_ether.argtypes = [POINTER(self.proto_tree),
                                              c_int,
                                              POINTER(self.tvbuff_t),
                                              LibGLib2.gint,
                                              LibGLib2.gint,
                                              POINTER(LibGLib2.guint8)]

        # proto_item *proto_tree_add_guid(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const e_guid_t *value_ptr);
        self.proto_tree_add_guid = libwireshark.proto_tree_add_guid
        self.proto_tree_add_guid.restype = POINTER(self.proto_item)
        self.proto_tree_add_guid.argtypes = [POINTER(self.proto_tree),
                                             c_int,
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint,
                                             POINTER(self.e_guid_t)]

        # proto_item *proto_tree_add_oid(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const guint8* value_ptr);
        self.proto_tree_add_oid = libwireshark.proto_tree_add_oid
        self.proto_tree_add_oid.restype = POINTER(self.proto_item)
        self.proto_tree_add_oid.argtypes = [POINTER(self.proto_tree),
                                            c_int,
                                            POINTER(self.tvbuff_t),
                                            LibGLib2.gint,
                                            LibGLib2.gint,
                                            POINTER(LibGLib2.guint8)]

        # proto_item *proto_tree_add_string(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const char* value);
        self.proto_tree_add_string = libwireshark.proto_tree_add_string
        self.proto_tree_add_string.restype = POINTER(self.proto_item)
        self.proto_tree_add_string.argtypes = [POINTER(self.proto_tree),
                                               c_int,
                                               POINTER(self.tvbuff_t),
                                               LibGLib2.gint,
                                               LibGLib2.gint,
                                               c_char_p]

        # proto_item *proto_tree_add_boolean(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, guint32 value);
        self.proto_tree_add_boolean = libwireshark.proto_tree_add_boolean
        self.proto_tree_add_boolean.restype = POINTER(self.proto_item)
        self.proto_tree_add_boolean.argtypes = [POINTER(self.proto_tree),
                                                c_int,
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.gint,
                                                LibGLib2.gint,
                                                LibGLib2.guint32]

        # proto_item *proto_tree_add_float(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, float value);
        self.proto_tree_add_float = libwireshark.proto_tree_add_float
        self.proto_tree_add_float.restype = POINTER(self.proto_item)
        self.proto_tree_add_float.argtypes = [POINTER(self.proto_tree),
                                              c_int,
                                              POINTER(self.tvbuff_t),
                                              LibGLib2.gint,
                                              LibGLib2.gint,
                                              c_float]

        # proto_item *proto_tree_add_double(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, double value);
        self.proto_tree_add_double = libwireshark.proto_tree_add_double
        self.proto_tree_add_double.restype = POINTER(self.proto_item)
        self.proto_tree_add_double.argtypes = [POINTER(self.proto_tree),
                                               c_int,
                                               POINTER(self.tvbuff_t),
                                               LibGLib2.gint,
                                               LibGLib2.gint,
                                               c_double]

        # proto_item *proto_tree_add_uint(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, guint32 value);
        self.proto_tree_add_uint = libwireshark.proto_tree_add_uint
        self.proto_tree_add_uint.restype = POINTER(self.proto_item)
        self.proto_tree_add_uint.argtypes = [POINTER(self.proto_tree),
                                             c_int,
                                             POINTER(self.tvbuff_t),
                                             LibGLib2.gint,
                                             LibGLib2.gint,
                                             LibGLib2.guint32]

        # proto_item *proto_tree_add_uint64(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, guint64 value);
        self.proto_tree_add_uint64 = libwireshark.proto_tree_add_uint64
        self.proto_tree_add_uint64.restype = POINTER(self.proto_item)
        self.proto_tree_add_uint64.argtypes = [POINTER(self.proto_tree),
                                               c_int,
                                               POINTER(self.tvbuff_t),
                                               LibGLib2.gint,
                                               LibGLib2.gint,
                                               LibGLib2.guint64]

        # proto_item *proto_tree_add_int(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, gint32 value);
        self.proto_tree_add_int = libwireshark.proto_tree_add_int
        self.proto_tree_add_int.restype = POINTER(self.proto_item)
        self.proto_tree_add_int.argtypes = [POINTER(self.proto_tree),
                                            c_int,
                                            POINTER(self.tvbuff_t),
                                            LibGLib2.gint,
                                            LibGLib2.gint,
                                            LibGLib2.gint32]

        # proto_item *proto_tree_add_int64(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, gint64 value);
        self.proto_tree_add_int64 = libwireshark.proto_tree_add_int64
        self.proto_tree_add_int64.restype = POINTER(self.proto_item)
        self.proto_tree_add_int64.argtypes = [POINTER(self.proto_tree),
                                              c_int,
                                              POINTER(self.tvbuff_t),
                                              LibGLib2.gint,
                                              LibGLib2.gint,
                                              LibGLib2.gint64]

        # proto_item *proto_tree_add_eui64(proto_tree *tree, int hfindex, tvbuff_t *tvb, gint start,
        #     gint length, const guint64 value);
        self.proto_tree_add_eui64 = libwireshark.proto_tree_add_eui64
        self.proto_tree_add_eui64.restype = POINTER(self.proto_item)
        self.proto_tree_add_eui64.argtypes = [POINTER(self.proto_tree),
                                              c_int,
                                              POINTER(self.tvbuff_t),
                                              LibGLib2.gint,
                                              LibGLib2.gint,
                                              LibGLib2.guint64]

        # void proto_item_fill_label(field_info *fi, gchar *label_str);
        self.proto_item_fill_label = libwireshark.proto_item_fill_label
        self.proto_item_fill_label.restype = None
        self.proto_item_fill_label.argtypes = [
            POINTER(self.field_info), LibGLib2.gchar_p]

        # int proto_register_protocol(const char *name, const char *short_name,
        # const char *filter_name);
        self.proto_register_protocol = libwireshark.proto_register_protocol
        self.proto_register_protocol.restype = c_int
        self.proto_register_protocol.argtypes = [c_char_p, c_char_p, c_char_p]

        # int proto_register_protocol_in_name_only(const char *name, const char *short_name, const char *filter_name,
        #     int parent_proto, enum ftenum field_type);
        self.proto_register_protocol_in_name_only = libwireshark.proto_register_protocol_in_name_only
        self.proto_register_protocol_in_name_only.restype = c_int
        self.proto_register_protocol_in_name_only.argtypes = [
            c_char_p, c_char_p, c_char_p, c_int, self.ftenum]

        # void proto_register_alias(const int proto_id, const char
        # *alias_name);
        self.proto_register_alias = libwireshark.proto_register_alias
        self.proto_register_alias.restype = None
        self.proto_register_alias.argtypes = [c_int, c_char_p]

        # void proto_register_prefix(const char *prefix,  prefix_initializer_t
        # initializer);
        self.proto_register_prefix = libwireshark.proto_register_prefix
        self.proto_register_prefix.restype = None
        self.proto_register_prefix.argtypes = [
            c_char_p, self.prefix_initializer_t]

        # void proto_initialize_all_prefixes(void);
        self.proto_initialize_all_prefixes = libwireshark.proto_initialize_all_prefixes
        self.proto_initialize_all_prefixes.restype = None
        self.proto_initialize_all_prefixes.argtypes = []

        # void proto_register_fields_manual(const int parent, header_field_info **hfi,
        #     const int num_records);
        self.proto_register_fields_manual = libwireshark.proto_register_fields_manual
        self.proto_register_fields_manual.restype = None
        self.proto_register_fields_manual.argtypes = [
            c_int, POINTER(POINTER(self.header_field_info)), c_int]

        # void proto_register_fields_section(const int parent, header_field_info *hfi,
        #     const int num_records);
        self.proto_register_fields_section = libwireshark.proto_register_fields_section
        self.proto_register_fields_section.restype = None
        self.proto_register_fields_section.argtypes = [
            c_int, POINTER(self.header_field_info), c_int]

        # void proto_register_field_array(const int parent, hf_register_info *hf,
        # const int num_records);
        self.proto_register_field_array = libwireshark.proto_register_field_array
        self.proto_register_field_array.restype = None
        self.proto_register_field_array.argtypes = [
            c_int, POINTER(self.hf_register_info), c_int]

        # void proto_deregister_field (const int parent, gint hf_id);
        self.proto_deregister_field = libwireshark.proto_deregister_field
        self.proto_deregister_field.restype = None
        self.proto_deregister_field.argtypes = [c_int, LibGLib2.gint]

        # void proto_add_deregistered_data (void *data);
        self.proto_add_deregistered_data = libwireshark.proto_add_deregistered_data
        self.proto_add_deregistered_data.restype = None
        self.proto_add_deregistered_data.argtypes = [c_void_p]

        # void proto_free_field_strings (ftenum_t field_type, unsigned int
        # field_display, const void *field_strings);
        self.proto_free_field_strings = libwireshark.proto_free_field_strings
        self.proto_free_field_strings.restype = None
        self.proto_free_field_strings.argtypes = [
            self.ftenum_t, c_uint, c_void_p]

        # void proto_free_deregistered_fields (void);
        self.proto_free_deregistered_fields = libwireshark.proto_free_deregistered_fields
        self.proto_free_deregistered_fields.restype = None
        self.proto_free_deregistered_fields.argtypes = []

        # void proto_register_subtree_array(gint *const *indices, const int
        # num_indices);
        self.proto_register_subtree_array = libwireshark.proto_register_subtree_array
        self.proto_register_subtree_array.restype = None
        self.proto_register_subtree_array.argtypes = [
            POINTER(LibGLib2.gint), c_int]

        # const char* proto_registrar_get_name(const int n);
        self.proto_registrar_get_name = libwireshark.proto_registrar_get_name
        self.proto_registrar_get_name.restype = c_char_p
        self.proto_registrar_get_name.argtypes = [c_int]

        # const char* proto_registrar_get_abbrev(const int n);
        self.proto_registrar_get_abbrev = libwireshark.proto_registrar_get_abbrev
        self.proto_registrar_get_abbrev.restype = c_char_p
        self.proto_registrar_get_abbrev.argtypes = [c_int]

        # header_field_info* proto_registrar_get_nth(guint hfindex);
        self.proto_registrar_get_nth = libwireshark.proto_registrar_get_nth
        self.proto_registrar_get_nth.restype = POINTER(self.header_field_info)
        self.proto_registrar_get_nth.argtypes = [LibGLib2.guint]

        # header_field_info* proto_registrar_get_byname(const char
        # *field_name);
        self.proto_registrar_get_byname = libwireshark.proto_registrar_get_byname
        self.proto_registrar_get_byname.restype = POINTER(
            self.header_field_info)
        self.proto_registrar_get_byname.argtypes = [c_char_p]

        # header_field_info* proto_registrar_get_byalias(const char
        # *alias_name);
        self.proto_registrar_get_byalias = libwireshark.proto_registrar_get_byalias
        self.proto_registrar_get_byalias.restype = POINTER(
            self.header_field_info)
        self.proto_registrar_get_byalias.argtypes = [c_char_p]

        # int proto_registrar_get_id_byname(const char *field_name);
        self.proto_registrar_get_id_byname = libwireshark.proto_registrar_get_id_byname
        self.proto_registrar_get_id_byname.restype = c_int
        self.proto_registrar_get_id_byname.argtypes = [c_char_p]

        # enum ftenum proto_registrar_get_ftype(const int n);
        self.proto_registrar_get_ftype = libwireshark.proto_registrar_get_ftype
        self.proto_registrar_get_ftype.restype = self.ftenum
        self.proto_registrar_get_ftype.argtypes = [c_int]

        # int proto_registrar_get_parent(const int n);
        self.proto_registrar_get_parent = libwireshark.proto_registrar_get_parent
        self.proto_registrar_get_parent.restype = c_int
        self.proto_registrar_get_parent.argtypes = [c_int]

        # gboolean proto_registrar_is_protocol(const int n);
        self.proto_registrar_is_protocol = libwireshark.proto_registrar_is_protocol
        self.proto_registrar_is_protocol.restype = LibGLib2.gboolean
        self.proto_registrar_is_protocol.argtypes = [c_int]

        # int proto_get_first_protocol(void **cookie);
        self.proto_get_first_protocol = libwireshark.proto_get_first_protocol
        self.proto_get_first_protocol.restype = c_int
        self.proto_get_first_protocol.argtypes = [POINTER(c_void_p)]

        # int proto_get_data_protocol(void *cookie);
        self.proto_get_data_protocol = libwireshark.proto_get_data_protocol
        self.proto_get_data_protocol.restype = c_int
        self.proto_get_data_protocol.argtypes = [c_void_p]

        # int proto_get_next_protocol(void **cookie);
        self.proto_get_next_protocol = libwireshark.proto_get_next_protocol
        self.proto_get_next_protocol.restype = c_int
        self.proto_get_next_protocol.argtypes = [POINTER(c_void_p)]

        # header_field_info *proto_get_first_protocol_field(const int proto_id,
        # void **cookie);
        self.proto_get_first_protocol_field = libwireshark.proto_get_first_protocol_field
        self.proto_get_first_protocol_field.restype = POINTER(
            self.header_field_info)
        self.proto_get_first_protocol_field.argtypes = [
            c_int, POINTER(c_void_p)]

        # header_field_info *proto_get_next_protocol_field(const int proto_id,
        # void **cookie);
        self.proto_get_next_protocol_field = libwireshark.proto_get_next_protocol_field
        self.proto_get_next_protocol_field.restype = POINTER(
            self.header_field_info)
        self.proto_get_next_protocol_field.argtypes = [
            c_int, POINTER(c_void_p)]

        # int proto_name_already_registered(const gchar *name);
        self.proto_name_already_registered = libwireshark.proto_name_already_registered
        self.proto_name_already_registered.restype = c_int
        self.proto_name_already_registered.argtypes = [LibGLib2.gchar_p]

        # int proto_get_id_by_filter_name(const gchar* filter_name);
        self.proto_get_id_by_filter_name = libwireshark.proto_get_id_by_filter_name
        self.proto_get_id_by_filter_name.restype = c_int
        self.proto_get_id_by_filter_name.argtypes = [LibGLib2.gchar_p]

        # int proto_get_id_by_short_name(const gchar* short_name);
        self.proto_get_id_by_short_name = libwireshark.proto_get_id_by_short_name
        self.proto_get_id_by_short_name.restype = c_int
        self.proto_get_id_by_short_name.argtypes = [LibGLib2.gchar_p]

        # gboolean proto_can_toggle_protocol(const int proto_id);
        self.proto_can_toggle_protocol = libwireshark.proto_can_toggle_protocol
        self.proto_can_toggle_protocol.restype = LibGLib2.gboolean
        self.proto_can_toggle_protocol.argtypes = [c_int]

        # protocol_t *find_protocol_by_id(const int proto_id);
        self.find_protocol_by_id = libwireshark.find_protocol_by_id
        self.find_protocol_by_id.restype = POINTER(self.protocol_t)
        self.find_protocol_by_id.argtypes = [c_int]

        # const char *proto_get_protocol_name(const int proto_id);
        self.proto_get_protocol_name = libwireshark.proto_get_protocol_name
        self.proto_get_protocol_name.restype = c_char_p
        self.proto_get_protocol_name.argtypes = [c_int]

        # int proto_get_id(const protocol_t *protocol);
        self.proto_get_id = libwireshark.proto_get_id
        self.proto_get_id.restype = c_int
        self.proto_get_id.argtypes = [POINTER(self.protocol_t)]

        # const char *proto_get_protocol_short_name(const protocol_t
        # *protocol);
        self.proto_get_protocol_short_name = libwireshark.proto_get_protocol_short_name
        self.proto_get_protocol_short_name.restype = c_char_p
        self.proto_get_protocol_short_name.argtypes = [
            POINTER(self.protocol_t)]

        # const char *proto_get_protocol_long_name(const protocol_t *protocol);
        self.proto_get_protocol_long_name = libwireshark.proto_get_protocol_long_name
        self.proto_get_protocol_long_name.restype = c_char_p
        self.proto_get_protocol_long_name.argtypes = [POINTER(self.protocol_t)]

        # gboolean proto_is_protocol_enabled(const protocol_t *protocol);
        self.proto_is_protocol_enabled = libwireshark.proto_is_protocol_enabled
        self.proto_is_protocol_enabled.restype = LibGLib2.gboolean
        self.proto_is_protocol_enabled.argtypes = [POINTER(self.protocol_t)]

        # gboolean proto_is_protocol_enabled_by_default(const protocol_t
        # *protocol);
        self.proto_is_protocol_enabled_by_default = libwireshark.proto_is_protocol_enabled_by_default
        self.proto_is_protocol_enabled_by_default.restype = LibGLib2.gboolean
        self.proto_is_protocol_enabled_by_default.argtypes = [
            POINTER(self.protocol_t)]

        # gboolean proto_is_pino(const protocol_t *protocol);
        self.proto_is_pino = libwireshark.proto_is_pino
        self.proto_is_pino.restype = LibGLib2.gboolean
        self.proto_is_pino.argtypes = [POINTER(self.protocol_t)]

        # const char *proto_get_protocol_filter_name(const int proto_id);
        self.proto_get_protocol_filter_name = libwireshark.proto_get_protocol_filter_name
        self.proto_get_protocol_filter_name.restype = c_char_p
        self.proto_get_protocol_filter_name.argtypes = [c_int]

        # void proto_heuristic_dissector_foreach(const protocol_t *protocol, GFunc func,
        #     gpointer user_data);
        self.proto_heuristic_dissector_foreach = libwireshark.proto_heuristic_dissector_foreach
        self.proto_heuristic_dissector_foreach.restype = None
        self.proto_heuristic_dissector_foreach.argtypes = [
            POINTER(self.protocol_t), LibGLib2.GFunc, LibGLib2.gpointer]

        # void proto_get_frame_protocols(const wmem_list_t *layers,
        #       gboolean *is_ip, gboolean *is_tcp, gboolean *is_udp, gboolean *is_sctp,
        #       gboolean *is_tls, gboolean *is_rtp, gboolean *is_lte_rlc);
        self.proto_get_frame_protocols = libwireshark.proto_get_frame_protocols
        self.proto_get_frame_protocols.restype = None
        self.proto_get_frame_protocols.argtypes = [POINTER(self.wmem_list_t),
                                                   POINTER(LibGLib2.gboolean),
                                                   POINTER(LibGLib2.gboolean),
                                                   POINTER(LibGLib2.gboolean),
                                                   POINTER(LibGLib2.gboolean),
                                                   POINTER(LibGLib2.gboolean),
                                                   POINTER(LibGLib2.gboolean),
                                                   POINTER(LibGLib2.gboolean)]

        # gboolean proto_is_frame_protocol(const wmem_list_t *layers, const char*
        # proto_name);
        self.proto_is_frame_protocol = libwireshark.proto_is_frame_protocol
        self.proto_is_frame_protocol.restype = LibGLib2.gboolean
        self.proto_is_frame_protocol.argtypes = [
            POINTER(self.wmem_list_t), c_char_p]

        # void proto_disable_by_default(const int proto_id);
        self.proto_disable_by_default = libwireshark.proto_disable_by_default
        self.proto_disable_by_default.restype = None
        self.proto_disable_by_default.argtypes = [c_int]

        # void proto_set_decoding(const int proto_id, const gboolean enabled);
        self.proto_set_decoding = libwireshark.proto_set_decoding
        self.proto_set_decoding.restype = None
        self.proto_set_decoding.argtypes = [c_int, LibGLib2.gboolean]

        # void proto_reenable_all(void);
        self.proto_reenable_all = libwireshark.proto_reenable_all
        self.proto_reenable_all.restype = None
        self.proto_reenable_all.argtypes = []

        # void proto_set_cant_toggle(const int proto_id);
        self.proto_set_cant_toggle = libwireshark.proto_set_cant_toggle
        self.proto_set_cant_toggle.restype = None
        self.proto_set_cant_toggle.argtypes = [c_int]

        # GPtrArray* proto_get_finfo_ptr_array(const proto_tree *tree, const int
        # hfindex);
        self.proto_get_finfo_ptr_array = libwireshark.proto_get_finfo_ptr_array
        self.proto_get_finfo_ptr_array.restype = POINTER(LibGLib2.GPtrArray)
        self.proto_get_finfo_ptr_array.argtypes = [
            POINTER(self.proto_tree), c_int]

        # gboolean proto_tracking_interesting_fields(const proto_tree *tree);
        self.proto_tracking_interesting_fields = libwireshark.proto_tracking_interesting_fields
        self.proto_tracking_interesting_fields.restype = LibGLib2.gboolean
        self.proto_tracking_interesting_fields.argtypes = [
            POINTER(self.proto_tree)]

        # GPtrArray* proto_find_finfo(proto_tree *tree, const int hfindex);
        self.proto_find_finfo = libwireshark.proto_find_finfo
        self.proto_find_finfo.restype = POINTER(LibGLib2.GPtrArray)
        self.proto_find_finfo.argtypes = [POINTER(self.proto_tree), c_int]

        # GPtrArray* proto_find_first_finfo(proto_tree *tree, const int
        # hfindex);
        self.proto_find_first_finfo = libwireshark.proto_find_first_finfo
        self.proto_find_first_finfo.restype = POINTER(LibGLib2.GPtrArray)
        self.proto_find_first_finfo.argtypes = [
            POINTER(self.proto_tree), c_int]

        # GPtrArray* proto_all_finfos(proto_tree *tree);
        self.proto_all_finfos = libwireshark.proto_all_finfos
        self.proto_all_finfos.restype = POINTER(LibGLib2.GPtrArray)
        self.proto_all_finfos.argtypes = [POINTER(self.proto_tree)]

        # void proto_registrar_dump_protocols(void);
        self.proto_registrar_dump_protocols = libwireshark.proto_registrar_dump_protocols
        self.proto_registrar_dump_protocols.restype = None
        self.proto_registrar_dump_protocols.argtypes = []

        # void proto_registrar_dump_values(void);
        self.proto_registrar_dump_values = libwireshark.proto_registrar_dump_values
        self.proto_registrar_dump_values.restype = None
        self.proto_registrar_dump_values.argtypes = []

        # void proto_registrar_dump_elastic(const gchar* filter);
        self.proto_registrar_dump_elastic = libwireshark.proto_registrar_dump_elastic
        self.proto_registrar_dump_elastic.restype = None
        self.proto_registrar_dump_elastic.argtypes = [LibGLib2.gchar_p]

        # gboolean proto_registrar_dump_fieldcount(void);
        self.proto_registrar_dump_fieldcount = libwireshark.proto_registrar_dump_fieldcount
        self.proto_registrar_dump_fieldcount.restype = LibGLib2.gboolean
        self.proto_registrar_dump_fieldcount.argtypes = []

        # void proto_registrar_dump_fields(void);
        self.proto_registrar_dump_fields = libwireshark.proto_registrar_dump_fields
        self.proto_registrar_dump_fields.restype = None
        self.proto_registrar_dump_fields.argtypes = []

        # void proto_registrar_dump_ftypes(void);
        self.proto_registrar_dump_ftypes = libwireshark.proto_registrar_dump_ftypes
        self.proto_registrar_dump_ftypes.restype = None
        self.proto_registrar_dump_ftypes.argtypes = []

        # const char* proto_field_display_to_string(int field_display);
        self.proto_field_display_to_string = libwireshark.proto_field_display_to_string
        self.proto_field_display_to_string.restype = c_char_p
        self.proto_field_display_to_string.argtypes = [c_int]

        # int num_tree_types;
        self.num_tree_types = c_int.in_dll(libwireshark, 'num_tree_types')

        # gboolean tree_expanded(int tree_type);
        self.tree_expanded = libwireshark.tree_expanded
        self.tree_expanded.restype = LibGLib2.gboolean
        self.tree_expanded.argtypes = [c_int]

        # void tree_expanded_set(int tree_type, gboolean value);
        self.tree_expanded_set = libwireshark.tree_expanded_set
        self.tree_expanded_set.restype = None
        self.tree_expanded_set.argtypes = [c_int, LibGLib2.gboolean]

        # int hfinfo_bitshift(const header_field_info *hfinfo);
        self.hfinfo_bitshift = libwireshark.hfinfo_bitshift
        self.hfinfo_bitshift.restype = c_int
        self.hfinfo_bitshift.argtypes = [POINTER(self.header_field_info)]

        # gboolean proto_can_match_selected(field_info *finfo, struct epan_dissect
        # *edt);
        self.proto_can_match_selected = libwireshark.proto_can_match_selected
        self.proto_can_match_selected.restype = LibGLib2.gboolean
        self.proto_can_match_selected.argtypes = [POINTER(self.field_info),
                                                  POINTER(self.epan_dissect)]

        # char* proto_construct_match_selected_string(field_info *finfo, struct
        # epan_dissect *edt);
        self.proto_construct_match_selected_string = libwireshark.proto_construct_match_selected_string
        self.proto_construct_match_selected_string.restype = c_char_p
        self.proto_construct_match_selected_string.argtypes = [
            POINTER(self.field_info), POINTER(self.epan_dissect)]

        # field_info* proto_find_field_from_offset(proto_tree *tree, guint offset,
        # tvbuff_t *tvb);
        self.proto_find_field_from_offset = libwireshark.proto_find_field_from_offset
        self.proto_find_field_from_offset.restype = POINTER(self.field_info)
        self.proto_find_field_from_offset.argtypes = [
            POINTER(self.proto_tree), LibGLib2.guint, POINTER(self.tvbuff_t)]

        # gchar* proto_find_undecoded_data(proto_tree *tree, guint length);
        self.proto_find_undecoded_data = libwireshark.proto_find_undecoded_data
        self.proto_find_undecoded_data.restype = LibGLib2.gchar_p
        self.proto_find_undecoded_data.argtypes = [
            POINTER(self.proto_tree), LibGLib2.guint]

        # proto_item *proto_tree_add_bitmask(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        # const int hf_hdr, const gint ett, const int **fields, const guint
        # encoding);
        self.proto_tree_add_bitmask = libwireshark.proto_tree_add_bitmask
        self.proto_tree_add_bitmask.restype = POINTER(self.proto_item)
        self.proto_tree_add_bitmask.argtypes = [POINTER(self.proto_tree),
                                                POINTER(self.tvbuff_t),
                                                LibGLib2.guint,
                                                c_int,
                                                LibGLib2.gint,
                                                POINTER(POINTER(c_int)),
                                                LibGLib2.guint]

        # proto_item *proto_tree_add_bitmask_ret_uint64(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        #         const int hf_hdr, const gint ett, const int **fields,
        #         const guint encoding, guint64 *retval);
        self.proto_tree_add_bitmask_ret_uint64 = libwireshark.proto_tree_add_bitmask_ret_uint64
        self.proto_tree_add_bitmask_ret_uint64.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_bitmask_ret_uint64.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.tvbuff_t), LibGLib2.guint, c_int, LibGLib2.gint, POINTER(
                POINTER(c_int)), LibGLib2.guint, POINTER(
                    LibGLib2.guint64)]

        # proto_item *proto_tree_add_bitmask_with_flags(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        # const int hf_hdr, const gint ett, const int **fields, const guint
        # encoding, const int flags);
        self.proto_tree_add_bitmask_with_flags = libwireshark.proto_tree_add_bitmask_with_flags
        self.proto_tree_add_bitmask_with_flags.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_bitmask_with_flags.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.tvbuff_t), LibGLib2.guint, c_int, LibGLib2.gint, POINTER(
                POINTER(c_int)), LibGLib2.guint, c_int]

        # proto_item *proto_tree_add_bitmask_with_flags_ret_uint64(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        #         const int hf_hdr, const gint ett, const int **fields,
        #         const guint encoding, const int flags, guint64 *retval);
        self.proto_tree_add_bitmask_with_flags_ret_uint64 = libwireshark.proto_tree_add_bitmask_with_flags_ret_uint64
        self.proto_tree_add_bitmask_with_flags_ret_uint64.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_bitmask_with_flags_ret_uint64.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.tvbuff_t), LibGLib2.guint, c_int, LibGLib2.gint, POINTER(
                POINTER(c_int)), LibGLib2.guint, c_int, POINTER(
                    LibGLib2.guint64)]

        # proto_item *proto_tree_add_bitmask_value(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        # const int hf_hdr, const gint ett, const int **fields, const guint64
        # value);
        self.proto_tree_add_bitmask_value = libwireshark.proto_tree_add_bitmask_value
        self.proto_tree_add_bitmask_value.restype = POINTER(self.proto_item)
        self.proto_tree_add_bitmask_value.argtypes = [POINTER(self.proto_tree),
                                                      POINTER(self.tvbuff_t),
                                                      LibGLib2.guint,
                                                      c_int,
                                                      LibGLib2.gint,
                                                      POINTER(POINTER(c_int)),
                                                      LibGLib2.guint64]

        # proto_item *proto_tree_add_bitmask_value_with_flags(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        # const int hf_hdr, const gint ett, const int **fields, const guint64
        # value, const int flags);
        self.proto_tree_add_bitmask_value_with_flags = libwireshark.proto_tree_add_bitmask_value_with_flags
        self.proto_tree_add_bitmask_value_with_flags.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_bitmask_value_with_flags.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.tvbuff_t), LibGLib2.guint, c_int, LibGLib2.gint, POINTER(
                POINTER(c_int)), LibGLib2.guint64, c_int]

        # void proto_tree_add_bitmask_list(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        # const int len, const int **fields, const guint encoding);
        self.proto_tree_add_bitmask_list = libwireshark.proto_tree_add_bitmask_list
        self.proto_tree_add_bitmask_list.restype = None
        self.proto_tree_add_bitmask_list.argtypes = [POINTER(self.proto_tree),
                                                     POINTER(self.tvbuff_t),
                                                     LibGLib2.guint,
                                                     c_int,
                                                     POINTER(POINTER(c_int)),
                                                     LibGLib2.guint]

        # void proto_tree_add_bitmask_list_value(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        # const int len, const int **fields, const guint64 value);
        self.proto_tree_add_bitmask_list_value = libwireshark.proto_tree_add_bitmask_list_value
        self.proto_tree_add_bitmask_list_value.restype = None
        self.proto_tree_add_bitmask_list_value.argtypes = [
            POINTER(
                self.proto_tree), POINTER(
                self.tvbuff_t), LibGLib2.guint, c_int, POINTER(
                POINTER(c_int)), LibGLib2.guint64]

        # proto_item *proto_tree_add_bitmask_len(proto_tree *tree, tvbuff_t *tvb, const guint offset, const guint len,
        # const int hf_hdr, const gint ett, const int **fields, struct
        # expert_field* exp, const guint encoding);
        self.proto_tree_add_bitmask_len = libwireshark.proto_tree_add_bitmask_len
        self.proto_tree_add_bitmask_len.restype = POINTER(self.proto_item)
        self.proto_tree_add_bitmask_len.argtypes = [POINTER(self.proto_tree),
                                                    POINTER(self.tvbuff_t),
                                                    LibGLib2.guint,
                                                    LibGLib2.guint,
                                                    c_int,
                                                    LibGLib2.gint,
                                                    POINTER(POINTER(c_int)),
                                                    POINTER(self.expert_field),
                                                    LibGLib2.guint]

        # proto_item *proto_tree_add_bitmask_text(proto_tree *tree, tvbuff_t *tvb, const guint offset, const guint len,
        #         const char *name, const char *fallback,
        # const gint ett, const int **fields, const guint encoding, const int
        # flags);
        self.proto_tree_add_bitmask_text = libwireshark.proto_tree_add_bitmask_text
        self.proto_tree_add_bitmask_text.restype = POINTER(self.proto_item)
        self.proto_tree_add_bitmask_text.argtypes = [POINTER(self.proto_tree),
                                                     POINTER(self.tvbuff_t),
                                                     LibGLib2.guint,
                                                     LibGLib2.guint,
                                                     c_char_p,
                                                     c_char_p,
                                                     LibGLib2.gint,
                                                     POINTER(POINTER(c_int)),
                                                     LibGLib2.guint,
                                                     c_int]

        # proto_item *proto_tree_add_bits_item(proto_tree *tree, const int hf_index, tvbuff_t *tvb, const guint bit_offset,
        #     const gint no_of_bits, const guint encoding);
        self.proto_tree_add_bits_item = libwireshark.proto_tree_add_bits_item
        self.proto_tree_add_bits_item.restype = POINTER(self.proto_item)
        self.proto_tree_add_bits_item.argtypes = [POINTER(self.proto_tree),
                                                  c_int,
                                                  POINTER(self.tvbuff_t),
                                                  LibGLib2.guint,
                                                  LibGLib2.gint,
                                                  LibGLib2.guint]

        # proto_item *proto_tree_add_split_bits_item_ret_val(proto_tree *tree, const int hf_index, tvbuff_t *tvb,
        # const guint bit_offset, const crumb_spec_t *crumb_spec, guint64
        # *return_value);
        self.proto_tree_add_split_bits_item_ret_val = libwireshark.proto_tree_add_split_bits_item_ret_val
        self.proto_tree_add_split_bits_item_ret_val.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_split_bits_item_ret_val.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.guint, POINTER(
                self.crumb_spec_t), POINTER(
                    LibGLib2.guint64)]

        # proto_item *proto_tree_add_bits_ret_val(proto_tree *tree, const int hf_index, tvbuff_t *tvb,
        # const guint bit_offset, const gint no_of_bits, guint64 *return_value,
        # const guint encoding);
        self.proto_tree_add_bits_ret_val = libwireshark.proto_tree_add_bits_ret_val
        self.proto_tree_add_bits_ret_val.restype = POINTER(self.proto_item)
        self.proto_tree_add_bits_ret_val.argtypes = [POINTER(self.proto_tree),
                                                     c_int,
                                                     POINTER(self.tvbuff_t),
                                                     LibGLib2.guint,
                                                     LibGLib2.gint,
                                                     POINTER(LibGLib2.guint64),
                                                     LibGLib2.guint]

        # proto_item *proto_tree_add_ts_23_038_7bits_item(proto_tree *tree, const int hfindex, tvbuff_t *tvb,
        #     const guint bit_offset, const gint no_of_chars);
        self.proto_tree_add_ts_23_038_7bits_item = libwireshark.proto_tree_add_ts_23_038_7bits_item
        self.proto_tree_add_ts_23_038_7bits_item.restype = POINTER(
            self.proto_item)
        self.proto_tree_add_ts_23_038_7bits_item.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.guint, LibGLib2.gint]

        # proto_item *proto_tree_add_ascii_7bits_item(proto_tree *tree, const int hfindex, tvbuff_t *tvb,
        #     const guint bit_offset, const gint no_of_chars);
        self.proto_tree_add_ascii_7bits_item = libwireshark.proto_tree_add_ascii_7bits_item
        self.proto_tree_add_ascii_7bits_item.restype = POINTER(self.proto_item)
        self.proto_tree_add_ascii_7bits_item.argtypes = [
            POINTER(
                self.proto_tree), c_int, POINTER(
                self.tvbuff_t), LibGLib2.guint, LibGLib2.gint]

        # proto_item *proto_tree_add_checksum(proto_tree *tree, tvbuff_t *tvb, const guint offset,
        #         const int hf_checksum, const int hf_checksum_status, struct expert_field* bad_checksum_expert,
        # packet_info *pinfo, guint32 computed_checksum, const guint encoding,
        # const guint flags);
        self.proto_tree_add_checksum = libwireshark.proto_tree_add_checksum
        self.proto_tree_add_checksum.restype = POINTER(self.proto_item)
        self.proto_tree_add_checksum.argtypes = [POINTER(self.proto_tree),
                                                 POINTER(self.tvbuff_t),
                                                 LibGLib2.guint,
                                                 c_int,
                                                 c_int,
                                                 POINTER(self.expert_field),
                                                 POINTER(self.packet_info),
                                                 LibGLib2.guint32,
                                                 LibGLib2.guint,
                                                 LibGLib2.guint]

        # const value_string proto_checksum_vals[];
        self.proto_checksum_vals = POINTER(self.value_string).in_dll(
            libwireshark, 'proto_checksum_vals')

        # guchar proto_check_field_name(const gchar *field_name);
        self.proto_check_field_name = libwireshark.proto_check_field_name
        self.proto_check_field_name.restype = LibGLib2.guchar
        self.proto_check_field_name.argtypes = [LibGLib2.gchar_p]

        # void col_setup(column_info *cinfo, const gint num_cols);
        self.col_setup = libwireshark.col_setup
        self.col_setup.restype = None
        self.col_setup.argtypes = [POINTER(self.column_info), LibGLib2.gint]

        # void col_cleanup(column_info *cinfo);
        self.col_cleanup = libwireshark.col_cleanup
        self.col_cleanup.restype = None
        self.col_cleanup.argtypes = [POINTER(self.column_info)]

        # void col_fill_in_frame_data(const frame_data *fd, column_info *cinfo,
        # const gint col, gboolean const fill_col_exprs);
        self.col_fill_in_frame_data = libwireshark.col_fill_in_frame_data
        self.col_fill_in_frame_data.restype = None
        self.col_fill_in_frame_data.argtypes = [POINTER(self.frame_data),
                                                POINTER(self.column_info),
                                                LibGLib2.gint,
                                                LibGLib2.gboolean]

        # void col_fill_in(packet_info *pinfo, const gboolean fill_col_exprs,
        # const gboolean fill_fd_colums);
        self.col_fill_in = libwireshark.col_fill_in
        self.col_fill_in.restype = None
        self.col_fill_in.argtypes = [
            POINTER(
                self.packet_info),
            LibGLib2.gboolean,
            LibGLib2.gboolean]

        # void col_fill_in_error(column_info *cinfo, frame_data *fdata, const
        # gboolean fill_col_exprs, const gboolean fill_fd_colums);
        self.col_fill_in_error = libwireshark.col_fill_in_error
        self.col_fill_in_error.restype = None
        self.col_fill_in_error.argtypes = [POINTER(self.column_info),
                                           POINTER(self.frame_data),
                                           LibGLib2.gboolean,
                                           LibGLib2.gboolean]

        # gboolean col_data_changed(void);
        self.col_data_changed = libwireshark.col_data_changed
        self.col_data_changed.restype = LibGLib2.gboolean
        self.col_data_changed.argtypes = []

        # gboolean col_get_writable(column_info *cinfo, const gint col);
        self.col_get_writable = libwireshark.col_get_writable
        self.col_get_writable.restype = LibGLib2.gboolean
        self.col_get_writable.argtypes = [
            POINTER(self.column_info), LibGLib2.gint]

        # void col_set_writable(column_info *cinfo, const gint col, const gboolean
        # writable);
        self.col_set_writable = libwireshark.col_set_writable
        self.col_set_writable.restype = None
        self.col_set_writable.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gboolean]

        # void col_set_fence(column_info *cinfo, const gint col);
        self.col_set_fence = libwireshark.col_set_fence
        self.col_set_fence.restype = None
        self.col_set_fence.argtypes = [
            POINTER(self.column_info), LibGLib2.gint]

        # void col_clear_fence(column_info *cinfo, const gint col);
        self.col_clear_fence = libwireshark.col_clear_fence
        self.col_clear_fence.restype = None
        self.col_clear_fence.argtypes = [
            POINTER(self.column_info), LibGLib2.gint]

        # const gchar *col_get_text(column_info *cinfo, const gint col);
        self.col_get_text = libwireshark.col_get_text
        self.col_get_text.restype = LibGLib2.gchar_p
        self.col_get_text.argtypes = [POINTER(self.column_info), LibGLib2.gint]

        # void col_clear(column_info *cinfo, const gint col);
        self.col_clear = libwireshark.col_clear
        self.col_clear.restype = None
        self.col_clear.argtypes = [POINTER(self.column_info), LibGLib2.gint]

        # void col_set_str(column_info *cinfo, const gint col, const gchar *
        # str);
        self.col_set_str = libwireshark.col_set_str
        self.col_set_str.restype = None
        self.col_set_str.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p]

        # void col_add_str(column_info *cinfo, const gint col, const gchar
        # *str);
        self.col_add_str = libwireshark.col_add_str
        self.col_add_str.restype = None
        self.col_add_str.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p]

        # void col_custom_prime_edt(struct epan_dissect *edt, column_info
        # *cinfo);
        self.col_custom_prime_edt = libwireshark.col_custom_prime_edt
        self.col_custom_prime_edt.restype = None
        self.col_custom_prime_edt.argtypes = [
            POINTER(
                self.epan_dissect), POINTER(
                self.column_info)]

        # gboolean have_custom_cols(column_info *cinfo);
        self.have_custom_cols = libwireshark.have_custom_cols
        self.have_custom_cols.restype = LibGLib2.gboolean
        self.have_custom_cols.argtypes = [POINTER(self.column_info)]

        # gboolean have_field_extractors(void);
        self.have_field_extractors = libwireshark.have_field_extractors
        self.have_field_extractors.restype = LibGLib2.gboolean
        self.have_field_extractors.argtypes = []

        # gboolean col_has_time_fmt(column_info *cinfo, const gint col);
        self.col_has_time_fmt = libwireshark.col_has_time_fmt
        self.col_has_time_fmt.restype = LibGLib2.gboolean
        self.col_has_time_fmt.argtypes = [
            POINTER(self.column_info), LibGLib2.gint]

        # gboolean col_based_on_frame_data(column_info *cinfo, const gint col);
        self.col_based_on_frame_data = libwireshark.col_based_on_frame_data
        self.col_based_on_frame_data.restype = LibGLib2.gboolean
        self.col_based_on_frame_data.argtypes = [
            POINTER(self.column_info), LibGLib2.gint]

        # void col_append_str(column_info *cinfo, const gint col, const gchar
        # *str);
        self.col_append_str = libwireshark.col_append_str
        self.col_append_str.restype = None
        self.col_append_str.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p]

        # void col_append_str_uint(column_info *cinfo, const gint col, const gchar
        # *abbrev, guint32 val, const gchar *sep);
        self.col_append_str_uint = libwireshark.col_append_str_uint
        self.col_append_str_uint.restype = None
        self.col_append_str_uint.argtypes = [
            POINTER(self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p,
            LibGLib2.guint32,
            LibGLib2.gchar_p]

        # void col_append_ports(column_info *cinfo, const gint col, port_type typ,
        # guint16 src, guint16 dst);
        self.col_append_ports = libwireshark.col_append_ports
        self.col_append_ports.restype = None
        self.col_append_ports.argtypes = [
            POINTER(self.column_info),
            LibGLib2.gint,
            self.port_type,
            LibGLib2.guint16,
            LibGLib2.guint16]

        # void col_append_frame_number(packet_info *pinfo, const gint col, const
        # gchar *fmt_str, guint frame_num);
        self.col_append_frame_number = libwireshark.col_append_frame_number
        self.col_append_frame_number.restype = None
        self.col_append_frame_number.argtypes = [
            POINTER(
                self.packet_info),
            LibGLib2.gint,
            LibGLib2.gchar_p,
            LibGLib2.guint]

        # void col_append_sep_str(column_info *cinfo, const gint col, const gchar *sep,
        #                         const gchar *str);
        self.col_append_sep_str = libwireshark.col_append_sep_str
        self.col_append_sep_str.restype = None
        self.col_append_sep_str.argtypes = [
            POINTER(
                self.column_info),
            LibGLib2.gint,
            LibGLib2.gchar_p,
            LibGLib2.gchar_p]

        # void col_set_time(column_info *cinfo, const int col,
        #                   const nstime_t *ts, const char *fieldname);
        self.col_set_time = libwireshark.col_set_time
        self.col_set_time.restype = None
        self.col_set_time.argtypes = [POINTER(self.column_info),
                                      c_int,
                                      POINTER(LibWSUtil.nstime_t),
                                      c_char_p]

        # void set_fd_time(const struct epan_session *epan, frame_data *fd, gchar
        # *buf);
        self.set_fd_time = libwireshark.set_fd_time
        self.set_fd_time.restype = None
        self.set_fd_time.argtypes = [
            POINTER(
                self.epan_session), POINTER(
                self.frame_data), LibGLib2.gchar_p]

        # const char* unit_name_string_get_value(guint32 value, const
        # unit_name_string* units);
        self.unit_name_string_get_value = libwireshark.unit_name_string_get_value
        self.unit_name_string_get_value.restype = c_char_p
        self.unit_name_string_get_value.argtypes = [
            LibGLib2.guint32, POINTER(self.unit_name_string)]

        # const char* unit_name_string_get_value64(guint64 value, const
        # unit_name_string* units);
        self.unit_name_string_get_value64 = libwireshark.unit_name_string_get_value64
        self.unit_name_string_get_value64.restype = c_char_p
        self.unit_name_string_get_value64.argtypes = [
            LibGLib2.guint64, POINTER(self.unit_name_string)]

        # const char* unit_name_string_get_double(double value, const
        # unit_name_string* units);
        self.unit_name_string_get_double = libwireshark.unit_name_string_get_double
        self.unit_name_string_get_double.restype = c_char_p
        self.unit_name_string_get_double.argtypes = [
            c_double, POINTER(self.unit_name_string)]

        # const unit_name_string units_foot_feet;
        self.units_foot_feet = self.unit_name_string.in_dll(
            libwireshark, 'units_foot_feet')

        # const unit_name_string units_bit_bits;
        self.units_bit_bits = self.unit_name_string.in_dll(
            libwireshark, 'units_bit_bits')

        # const unit_name_string units_byte_bytes;
        self.units_byte_bytes = self.unit_name_string.in_dll(
            libwireshark, 'units_byte_bytes')

        # const unit_name_string units_byte_bytespsecond;
        self.units_byte_bytespsecond = self.unit_name_string.in_dll(
            libwireshark, 'units_byte_bytespsecond')

        # const unit_name_string units_octet_octets;
        self.units_octet_octets = self.unit_name_string.in_dll(
            libwireshark, 'units_octet_octets')

        # const unit_name_string units_word_words;
        self.units_word_words = self.unit_name_string.in_dll(
            libwireshark, 'units_word_words')

        # const unit_name_string units_tick_ticks;
        self.units_tick_ticks = self.unit_name_string.in_dll(
            libwireshark, 'units_tick_ticks')

        # const unit_name_string units_meters;
        self.units_meters = self.unit_name_string.in_dll(
            libwireshark, 'units_meters')

        # const unit_name_string units_meter_meters;
        self.units_meter_meters = self.unit_name_string.in_dll(
            libwireshark, 'units_meter_meters')

        # const unit_name_string units_week_weeks;
        self.units_week_weeks = self.unit_name_string.in_dll(
            libwireshark, 'units_week_weeks')

        # const unit_name_string units_day_days;
        self.units_day_days = self.unit_name_string.in_dll(
            libwireshark, 'units_day_days')

        # const unit_name_string units_hour_hours;
        self.units_hour_hours = self.unit_name_string.in_dll(
            libwireshark, 'units_hour_hours')

        # const unit_name_string units_hours;
        self.units_hours = self.unit_name_string.in_dll(
            libwireshark, 'units_hours')

        # const unit_name_string units_minute_minutes;
        self.units_minute_minutes = self.unit_name_string.in_dll(
            libwireshark, 'units_minute_minutes')

        # const unit_name_string units_minutes;
        self.units_minutes = self.unit_name_string.in_dll(
            libwireshark, 'units_minutes')

        # const unit_name_string units_second_seconds;
        self.units_second_seconds = self.unit_name_string.in_dll(
            libwireshark, 'units_second_seconds')

        # const unit_name_string units_seconds;
        self.units_seconds = self.unit_name_string.in_dll(
            libwireshark, 'units_seconds')

        # const unit_name_string units_millisecond_milliseconds;
        self.units_millisecond_milliseconds = self.unit_name_string.in_dll(
            libwireshark, 'units_millisecond_milliseconds')

        # const unit_name_string units_milliseconds;
        self.units_milliseconds = self.unit_name_string.in_dll(
            libwireshark, 'units_milliseconds')

        # const unit_name_string units_microsecond_microseconds;
        self.units_microsecond_microseconds = self.unit_name_string.in_dll(
            libwireshark, 'units_microsecond_microseconds')

        # const unit_name_string units_microseconds;
        self.units_microseconds = self.unit_name_string.in_dll(
            libwireshark, 'units_microseconds')

        # const unit_name_string units_nanosecond_nanoseconds;
        self.units_nanosecond_nanoseconds = self.unit_name_string.in_dll(
            libwireshark, 'units_nanosecond_nanoseconds')

        # const unit_name_string units_nanoseconds;
        self.units_nanoseconds = self.unit_name_string.in_dll(
            libwireshark, 'units_nanoseconds')

        # const unit_name_string units_nanometers;
        self.units_nanometers = self.unit_name_string.in_dll(
            libwireshark, 'units_nanometers')

        # const unit_name_string units_degree_degrees;
        self.units_degree_degrees = self.unit_name_string.in_dll(
            libwireshark, 'units_degree_degrees')

        # const unit_name_string units_degree_celsius;
        self.units_degree_celsius = self.unit_name_string.in_dll(
            libwireshark, 'units_degree_celsius')

        # const unit_name_string units_degree_bearing;
        self.units_degree_bearing = self.unit_name_string.in_dll(
            libwireshark, 'units_degree_bearing')

        # const unit_name_string units_decibels;
        self.units_decibels = self.unit_name_string.in_dll(
            libwireshark, 'units_decibels')

        # const unit_name_string units_dbm;
        self.units_dbm = self.unit_name_string.in_dll(
            libwireshark, 'units_dbm')

        # const unit_name_string units_dbi;
        self.units_dbi = self.unit_name_string.in_dll(
            libwireshark, 'units_dbi')

        # const unit_name_string units_mbm;
        self.units_mbm = self.unit_name_string.in_dll(
            libwireshark, 'units_mbm')

        # const unit_name_string units_percent;
        self.units_percent = self.unit_name_string.in_dll(
            libwireshark, 'units_percent')

        # const unit_name_string units_khz;
        self.units_khz = self.unit_name_string.in_dll(
            libwireshark, 'units_khz')

        # const unit_name_string units_ghz;
        self.units_ghz = self.unit_name_string.in_dll(
            libwireshark, 'units_ghz')

        # const unit_name_string units_mhz;
        self.units_mhz = self.unit_name_string.in_dll(
            libwireshark, 'units_mhz')

        # const unit_name_string units_hz;
        self.units_hz = self.unit_name_string.in_dll(libwireshark, 'units_hz')

        # const unit_name_string units_hz_s;
        self.units_hz_s = self.unit_name_string.in_dll(
            libwireshark, 'units_hz_s')

        # const unit_name_string units_kbit;
        self.units_kbit = self.unit_name_string.in_dll(
            libwireshark, 'units_kbit')

        # const unit_name_string units_kbps;
        self.units_kbps = self.unit_name_string.in_dll(
            libwireshark, 'units_kbps')

        # const unit_name_string units_kibps;
        self.units_kibps = self.unit_name_string.in_dll(
            libwireshark, 'units_kibps')

        # const unit_name_string units_pkts;
        self.units_pkts = self.unit_name_string.in_dll(
            libwireshark, 'units_pkts')

        # const unit_name_string units_pkts_per_sec;
        self.units_pkts_per_sec = self.unit_name_string.in_dll(
            libwireshark, 'units_pkts_per_sec')

        # const unit_name_string units_km;
        self.units_km = self.unit_name_string.in_dll(libwireshark, 'units_km')

        # const unit_name_string units_kmh;
        self.units_kmh = self.unit_name_string.in_dll(
            libwireshark, 'units_kmh')

        # const unit_name_string units_milliamps;
        self.units_milliamps = self.unit_name_string.in_dll(
            libwireshark, 'units_milliamps')

        # const unit_name_string units_microwatts;
        self.units_microwatts = self.unit_name_string.in_dll(
            libwireshark, 'units_microwatts')

        # const unit_name_string units_volt;
        self.units_volt = self.unit_name_string.in_dll(
            libwireshark, 'units_volt')

        # const unit_name_string units_grams_per_second;
        self.units_grams_per_second = self.unit_name_string.in_dll(
            libwireshark, 'units_grams_per_second')

        # const unit_name_string units_meter_sec;
        self.units_meter_sec = self.unit_name_string.in_dll(
            libwireshark, 'units_meter_sec')

        # const unit_name_string units_meter_sec_squared;
        self.units_meter_sec_squared = self.unit_name_string.in_dll(
            libwireshark, 'units_meter_sec_squared')

        # const unit_name_string units_bit_sec;
        self.units_bit_sec = self.unit_name_string.in_dll(
            libwireshark, 'units_bit_sec')

        # const unit_name_string units_segment_remaining;
        self.units_segment_remaining = self.unit_name_string.in_dll(
            libwireshark, 'units_segment_remaining')

        # const unit_name_string units_frame_frames;
        self.units_frame_frames = self.unit_name_string.in_dll(
            libwireshark, 'units_frame_frames')

        # const unit_name_string units_revolutions_per_minute;
        self.units_revolutions_per_minute = self.unit_name_string.in_dll(
            libwireshark, 'units_revolutions_per_minute')

        # const unit_name_string units_kilopascal;
        self.units_kilopascal = self.unit_name_string.in_dll(
            libwireshark, 'units_kilopascal')

        # const unit_name_string units_newton_metre;
        self.units_newton_metre = self.unit_name_string.in_dll(
            libwireshark, 'units_newton_metre')

        # const unit_name_string units_liter_per_hour;
        self.units_liter_per_hour = self.unit_name_string.in_dll(
            libwireshark, 'units_liter_per_hour')

        # const unit_name_string units_amp;
        self.units_amp = self.unit_name_string.in_dll(
            libwireshark, 'units_amp')

        # const unit_name_string units_watthour;
        self.units_watthour = self.unit_name_string.in_dll(
            libwireshark, 'units_watthour')

        # const unit_name_string units_watt;
        self.units_watt = self.unit_name_string.in_dll(
            libwireshark, 'units_watt')

        # const unit_name_string units_bpm;
        self.units_bpm = self.unit_name_string.in_dll(
            libwireshark, 'units_bpm')

        # const unit_name_string units_calorie;
        self.units_calorie = self.unit_name_string.in_dll(
            libwireshark, 'units_calorie')

        # dissector_handle_t dtbl_entry_get_handle (dtbl_entry_t *dtbl_entry);
        self.dtbl_entry_get_handle = libwireshark.dtbl_entry_get_handle
        self.dtbl_entry_get_handle.restype = self.dissector_handle_t
        self.dtbl_entry_get_handle.argtypes = [POINTER(self.dtbl_entry_t)]

        # dissector_handle_t dtbl_entry_get_initial_handle (dtbl_entry_t *
        # entry);
        self.dtbl_entry_get_initial_handle = libwireshark.dtbl_entry_get_initial_handle
        self.dtbl_entry_get_initial_handle.restype = self.dissector_handle_t
        self.dtbl_entry_get_initial_handle.argtypes = [
            POINTER(self.dtbl_entry_t)]

        # void dissector_table_foreach (const char *table_name, DATFunc func,
        #     gpointer user_data);
        self.dissector_table_foreach = libwireshark.dissector_table_foreach
        self.dissector_table_foreach.restype = None
        self.dissector_table_foreach.argtypes = [
            c_char_p, self.DATFunc, LibGLib2.gpointer]

        # void dissector_all_tables_foreach_changed (DATFunc func,
        #     gpointer user_data);
        self.dissector_all_tables_foreach_changed = libwireshark.dissector_all_tables_foreach_changed
        self.dissector_all_tables_foreach_changed.restype = None
        self.dissector_all_tables_foreach_changed.argtypes = [
            self.DATFunc, LibGLib2.gpointer]

        # void dissector_table_foreach_handle(const char *table_name, DATFunc_handle func,
        #     gpointer user_data);
        self.dissector_table_foreach_handle = libwireshark.dissector_table_foreach_handle
        self.dissector_table_foreach_handle.restype = None
        self.dissector_table_foreach_handle.argtypes = [
            c_char_p, self.DATFunc_handle, LibGLib2.gpointer]

        # void dissector_all_tables_foreach_table (DATFunc_table func,
        #     gpointer user_data, GCompareFunc compare_key_func);
        self.dissector_all_tables_foreach_table = libwireshark.dissector_all_tables_foreach_table
        self.dissector_all_tables_foreach_table.restype = None
        self.dissector_all_tables_foreach_table.argtypes = [
            self.DATFunc_table, LibGLib2.gpointer, LibGLib2.GCompareFunc]

        # dissector_table_t register_dissector_table(const char *name,
        # const char *ui_name, const int proto, const ftenum_t type, const int
        # param);
        self.register_dissector_table = libwireshark.register_dissector_table
        self.register_dissector_table.restype = self.dissector_table_t
        self.register_dissector_table.argtypes = [
            c_char_p, c_char_p, c_int, self.ftenum_t, c_int]

        # dissector_table_t register_custom_dissector_table(const char *name,
        # const char *ui_name, const int proto, GHashFunc hash_func, GEqualFunc
        # key_equal_func);
        self.register_custom_dissector_table = libwireshark.register_custom_dissector_table
        self.register_custom_dissector_table.restype = self.dissector_table_t
        self.register_custom_dissector_table.argtypes = [
            c_char_p, c_char_p, c_int, LibGLib2.GHashFunc, LibGLib2.GEqualFunc]

        # void register_dissector_table_alias(dissector_table_t dissector_table,
        #     const char *alias_name);
        self.register_dissector_table_alias = libwireshark.register_dissector_table_alias
        self.register_dissector_table_alias.restype = None
        self.register_dissector_table_alias.argtypes = [
            self.dissector_table_t, c_char_p]

        # dissector_table_t find_dissector_table(const char *name);
        self.find_dissector_table = libwireshark.find_dissector_table
        self.find_dissector_table.restype = self.dissector_table_t
        self.find_dissector_table.argtypes = [c_char_p]

        # const char *get_dissector_table_ui_name(const char *name);
        self.get_dissector_table_ui_name = libwireshark.get_dissector_table_ui_name
        self.get_dissector_table_ui_name.restype = c_char_p
        self.get_dissector_table_ui_name.argtypes = [c_char_p]

        # ftenum_t get_dissector_table_selector_type(const char *name);
        self.get_dissector_table_selector_type = libwireshark.get_dissector_table_selector_type
        self.get_dissector_table_selector_type.restype = self.ftenum_t
        self.get_dissector_table_selector_type.argtypes = [c_char_p]

        # int get_dissector_table_param(const char *name);
        self.get_dissector_table_param = libwireshark.get_dissector_table_param
        self.get_dissector_table_param.restype = c_int
        self.get_dissector_table_param.argtypes = [c_char_p]

        # void dissector_dump_dissector_tables(void);
        self.dissector_dump_dissector_tables = libwireshark.dissector_dump_dissector_tables
        self.dissector_dump_dissector_tables.restype = None
        self.dissector_dump_dissector_tables.argtypes = []

        # void dissector_add_uint(const char *name, const guint32 pattern,
        #     dissector_handle_t handle);
        self.dissector_add_uint = libwireshark.dissector_add_uint
        self.dissector_add_uint.restype = None
        self.dissector_add_uint.argtypes = [
            c_char_p, LibGLib2.guint32, self.dissector_handle_t]

        # void dissector_add_uint_with_preference(const char *name, const guint32 pattern,
        #     dissector_handle_t handle);
        self.dissector_add_uint_with_preference = libwireshark.dissector_add_uint_with_preference
        self.dissector_add_uint_with_preference.restype = None
        self.dissector_add_uint_with_preference.argtypes = [
            c_char_p, LibGLib2.guint32, self.dissector_handle_t]

        # void dissector_add_uint_range(const char *abbrev, struct epan_range *range,
        #     dissector_handle_t handle);
        self.dissector_add_uint_range = libwireshark.dissector_add_uint_range
        self.dissector_add_uint_range.restype = None
        self.dissector_add_uint_range.argtypes = [
            c_char_p, POINTER(self.epan_range), self.dissector_handle_t]

        # void dissector_add_uint_range_with_preference(const char *abbrev, const char* range_str,
        #     dissector_handle_t handle);
        self.dissector_add_uint_range_with_preference = libwireshark.dissector_add_uint_range_with_preference
        self.dissector_add_uint_range_with_preference.restype = None
        self.dissector_add_uint_range_with_preference.argtypes = [
            c_char_p, c_char_p, self.dissector_handle_t]

        # void dissector_delete_uint(const char *name, const guint32 pattern,
        #     dissector_handle_t handle);
        self.dissector_delete_uint = libwireshark.dissector_delete_uint
        self.dissector_delete_uint.restype = None
        self.dissector_delete_uint.argtypes = [
            c_char_p, LibGLib2.guint32, self.dissector_handle_t]

        # void dissector_delete_uint_range(const char *abbrev, struct epan_range *range,
        #     dissector_handle_t handle);
        self.dissector_delete_uint_range = libwireshark.dissector_delete_uint_range
        self.dissector_delete_uint_range.restype = None
        self.dissector_delete_uint_range.argtypes = [
            c_char_p, POINTER(self.epan_range), self.dissector_handle_t]

        # void dissector_delete_all(const char *name, dissector_handle_t
        # handle);
        self.dissector_delete_all = libwireshark.dissector_delete_all
        self.dissector_delete_all.restype = None
        self.dissector_delete_all.argtypes = [
            c_char_p, self.dissector_handle_t]

        # void dissector_change_uint(const char *abbrev, const guint32 pattern,
        #     dissector_handle_t handle);
        self.dissector_change_uint = libwireshark.dissector_change_uint
        self.dissector_change_uint.restype = None
        self.dissector_change_uint.argtypes = [
            c_char_p, LibGLib2.guint32, self.dissector_handle_t]

        # void dissector_reset_uint(const char *name, const guint32 pattern);
        self.dissector_reset_uint = libwireshark.dissector_reset_uint
        self.dissector_reset_uint.restype = None
        self.dissector_reset_uint.argtypes = [c_char_p, LibGLib2.guint32]

        # int dissector_try_uint(dissector_table_t sub_dissectors,
        # const guint32 uint_val, tvbuff_t *tvb, packet_info *pinfo, proto_tree
        # *tree);
        self.dissector_try_uint = libwireshark.dissector_try_uint
        self.dissector_try_uint.restype = c_int
        self.dissector_try_uint.argtypes = [
            self.dissector_table_t,
            LibGLib2.guint32,
            POINTER(self.tvbuff_t),
            POINTER(self.packet_info),
            POINTER(self.proto_tree)]

        # int dissector_try_uint_new(dissector_table_t sub_dissectors,
        # const guint32 uint_val, tvbuff_t *tvb, packet_info *pinfo, proto_tree
        # *tree, const gboolean add_proto_name, void *data);
        self.dissector_try_uint_new = libwireshark.dissector_try_uint_new
        self.dissector_try_uint_new.restype = c_int
        self.dissector_try_uint_new.argtypes = [self.dissector_table_t,
                                                LibGLib2.guint32,
                                                POINTER(self.tvbuff_t),
                                                POINTER(self.packet_info),
                                                POINTER(self.proto_tree),
                                                LibGLib2.gboolean,
                                                c_void_p]

        # dissector_handle_t dissector_get_uint_handle(
        #     dissector_table_t const sub_dissectors, const guint32 uint_val);
        self.dissector_get_uint_handle = libwireshark.dissector_get_uint_handle
        self.dissector_get_uint_handle.restype = self.dissector_handle_t
        self.dissector_get_uint_handle.argtypes = [
            self.dissector_table_t, LibGLib2.guint32]

        # dissector_handle_t dissector_get_default_uint_handle(
        #     const char *name, const guint32 uint_val);
        self.dissector_get_default_uint_handle = libwireshark.dissector_get_default_uint_handle
        self.dissector_get_default_uint_handle.restype = self.dissector_handle_t
        self.dissector_get_default_uint_handle.argtypes = [
            c_char_p, LibGLib2.guint32]

        # void dissector_add_string(const char *name, const gchar *pattern,
        #     dissector_handle_t handle);
        self.dissector_add_string = libwireshark.dissector_add_string
        self.dissector_add_string.restype = None
        self.dissector_add_string.argtypes = [
            c_char_p, LibGLib2.gchar_p, self.dissector_handle_t]

        # void dissector_delete_string(const char *name, const gchar *pattern,
        # 	dissector_handle_t handle);
        self.dissector_delete_string = libwireshark.dissector_delete_string
        self.dissector_delete_string.restype = None
        self.dissector_delete_string.argtypes = [
            c_char_p, LibGLib2.gchar_p, self.dissector_handle_t]

        # void dissector_change_string(const char *name, const gchar *pattern,
        #     dissector_handle_t handle);
        self.dissector_change_string = libwireshark.dissector_change_string
        self.dissector_change_string.restype = None
        self.dissector_change_string.argtypes = [
            c_char_p, LibGLib2.gchar_p, self.dissector_handle_t]

        # void dissector_reset_string(const char *name, const gchar *pattern);
        self.dissector_reset_string = libwireshark.dissector_reset_string
        self.dissector_reset_string.restype = None
        self.dissector_reset_string.argtypes = [c_char_p, LibGLib2.gchar_p]

        # int dissector_try_string(dissector_table_t sub_dissectors,
        # const gchar *string, tvbuff_t *tvb, packet_info *pinfo, proto_tree
        # *tree, void *data);
        self.dissector_try_string = libwireshark.dissector_try_string
        self.dissector_try_string.restype = c_int
        self.dissector_try_string.argtypes = [
            self.dissector_table_t,
            LibGLib2.gchar_p,
            POINTER(self.tvbuff_t),
            POINTER(self.packet_info),
            POINTER(self.proto_tree),
            c_void_p]

        # int dissector_try_string_new(dissector_table_t sub_dissectors,
        # const gchar *string, tvbuff_t *tvb, packet_info *pinfo, proto_tree
        # *tree, const gboolean add_proto_name,void *data);
        self.dissector_try_string_new = libwireshark.dissector_try_string_new
        self.dissector_try_string_new.restype = c_int
        self.dissector_try_string_new.argtypes = [
            self.dissector_table_t,
            LibGLib2.gchar_p,
            POINTER(self.tvbuff_t),
            POINTER(self.packet_info),
            POINTER(self.proto_tree),
            LibGLib2.gboolean,
            c_void_p]

        # dissector_handle_t dissector_get_string_handle(
        #     dissector_table_t sub_dissectors, const gchar *string);
        self.dissector_get_string_handle = libwireshark.dissector_get_string_handle
        self.dissector_get_string_handle.restype = self.dissector_handle_t
        self.dissector_get_string_handle.argtypes = [
            self.dissector_table_t, LibGLib2.gchar_p]

        # dissector_handle_t dissector_get_default_string_handle(
        #     const char *name, const gchar *string);
        self.dissector_get_default_string_handle = libwireshark.dissector_get_default_string_handle
        self.dissector_get_default_string_handle.restype = self.dissector_handle_t
        self.dissector_get_default_string_handle.argtypes = [
            c_char_p, LibGLib2.gchar_p]

        # void dissector_add_custom_table_handle(const char *name, void *pattern,
        #     dissector_handle_t handle);
        self.dissector_add_custom_table_handle = libwireshark.dissector_add_custom_table_handle
        self.dissector_add_custom_table_handle.restype = None
        self.dissector_add_custom_table_handle.argtypes = [
            c_char_p, c_void_p, self.dissector_handle_t]

        # dissector_handle_t dissector_get_custom_table_handle(
        #     dissector_table_t sub_dissectors, void *key);
        self.dissector_get_custom_table_handle = libwireshark.dissector_get_custom_table_handle
        self.dissector_get_custom_table_handle.restype = self.dissector_handle_t
        self.dissector_get_custom_table_handle.argtypes = [
            self.dissector_table_t, c_void_p]

        # void dissector_add_guid(const char *name, guid_key* guid_val,
        #     dissector_handle_t handle);
        self.dissector_add_guid = libwireshark.dissector_add_guid
        self.dissector_add_guid.restype = None
        self.dissector_add_guid.argtypes = [
            c_char_p, POINTER(
                self.guid_key), self.dissector_handle_t]

        # int dissector_try_guid(dissector_table_t sub_dissectors,
        # guid_key* guid_val, tvbuff_t *tvb, packet_info *pinfo, proto_tree
        # *tree);
        self.dissector_try_guid = libwireshark.dissector_try_guid
        self.dissector_try_guid.restype = c_int
        self.dissector_try_guid.argtypes = [
            self.dissector_table_t,
            POINTER(self.guid_key),
            POINTER(self.tvbuff_t),
            POINTER(self.packet_info),
            POINTER(self.proto_tree)]

        # int dissector_try_guid_new(dissector_table_t sub_dissectors,
        # guid_key* guid_val, tvbuff_t *tvb, packet_info *pinfo, proto_tree *tree,
        # const gboolean add_proto_name, void *data);
        self.dissector_try_guid_new = libwireshark.dissector_try_guid_new
        self.dissector_try_guid_new.restype = c_int
        self.dissector_try_guid_new.argtypes = [self.dissector_table_t,
                                                POINTER(self.guid_key),
                                                POINTER(self.tvbuff_t),
                                                POINTER(self.packet_info),
                                                POINTER(self.proto_tree),
                                                LibGLib2.gboolean,
                                                c_void_p]

        # dissector_handle_t dissector_get_guid_handle(
        #     dissector_table_t const sub_dissectors, guid_key* guid_val);
        self.dissector_get_guid_handle = libwireshark.dissector_get_guid_handle
        self.dissector_get_guid_handle.restype = self.dissector_handle_t
        self.dissector_get_guid_handle.argtypes = [
            self.dissector_table_t, POINTER(self.guid_key)]

        # int dissector_try_payload(dissector_table_t sub_dissectors,
        #     tvbuff_t *tvb, packet_info *pinfo, proto_tree *tree);
        self.dissector_try_payload = libwireshark.dissector_try_payload
        self.dissector_try_payload.restype = c_int
        self.dissector_try_payload.argtypes = [
            self.dissector_table_t,
            POINTER(self.tvbuff_t),
            POINTER(self.packet_info),
            POINTER(self.proto_tree)]

        # int dissector_try_payload_new(dissector_table_t sub_dissectors,
        # tvbuff_t *tvb, packet_info *pinfo, proto_tree *tree, const gboolean
        # add_proto_name, void *data);
        self.dissector_try_payload_new = libwireshark.dissector_try_payload_new
        self.dissector_try_payload_new.restype = c_int
        self.dissector_try_payload_new.argtypes = [self.dissector_table_t,
                                                   POINTER(self.tvbuff_t),
                                                   POINTER(self.packet_info),
                                                   POINTER(self.proto_tree),
                                                   LibGLib2.gboolean,
                                                   c_void_p]

        # void dissector_change_payload(const char *abbrev, dissector_handle_t
        # handle);
        self.dissector_change_payload = libwireshark.dissector_change_payload
        self.dissector_change_payload.restype = None
        self.dissector_change_payload.argtypes = [
            c_char_p, self.dissector_handle_t]

        # void dissector_reset_payload(const char *name);
        self.dissector_reset_payload = libwireshark.dissector_reset_payload
        self.dissector_reset_payload.restype = None
        self.dissector_reset_payload.argtypes = [c_char_p]

        # dissector_handle_t dissector_get_payload_handle(
        #         dissector_table_t const dissector_table);
        self.dissector_get_payload_handle = libwireshark.dissector_get_payload_handle
        self.dissector_get_payload_handle.restype = self.dissector_handle_t
        self.dissector_get_payload_handle.argtypes = [self.dissector_table_t]

        # void dissector_add_for_decode_as(const char *name,
        #     dissector_handle_t handle);
        self.dissector_add_for_decode_as = libwireshark.dissector_add_for_decode_as
        self.dissector_add_for_decode_as.restype = None
        self.dissector_add_for_decode_as.argtypes = [
            c_char_p, self.dissector_handle_t]

        # void dissector_add_for_decode_as_with_preference(const char *name,
        #     dissector_handle_t handle);
        self.dissector_add_for_decode_as_with_preference = libwireshark.dissector_add_for_decode_as_with_preference
        self.dissector_add_for_decode_as_with_preference.restype = None
        self.dissector_add_for_decode_as_with_preference.argtypes = [
            c_char_p, self.dissector_handle_t]

        # GSList *dissector_table_get_dissector_handles(dissector_table_t
        # dissector_table);
        self.dissector_table_get_dissector_handles = libwireshark.dissector_table_get_dissector_handles
        self.dissector_table_get_dissector_handles.restype = POINTER(
            LibGLib2.GSList)
        self.dissector_table_get_dissector_handles.argtypes = [
            self.dissector_table_t]

        # dissector_handle_t
        # dissector_table_get_dissector_handle(dissector_table_t dissector_table,
        # const gchar* short_name);
        self.dissector_table_get_dissector_handle = libwireshark.dissector_table_get_dissector_handle
        self.dissector_table_get_dissector_handle.restype = self.dissector_handle_t
        self.dissector_table_get_dissector_handle.argtypes = [
            self.dissector_table_t, LibGLib2.gchar_p]

        # ftenum_t dissector_table_get_type(dissector_table_t dissector_table);
        self.dissector_table_get_type = libwireshark.dissector_table_get_type
        self.dissector_table_get_type.restype = self.ftenum_t
        self.dissector_table_get_type.argtypes = [self.dissector_table_t]

        # void dissector_table_allow_decode_as(dissector_table_t
        # dissector_table);
        self.dissector_table_allow_decode_as = libwireshark.dissector_table_allow_decode_as
        self.dissector_table_allow_decode_as.restype = None
        self.dissector_table_allow_decode_as.argtypes = [
            self.dissector_table_t]

        # heur_dissector_list_t register_heur_dissector_list(const char *name,
        # const int proto);
        self.register_heur_dissector_list = libwireshark.register_heur_dissector_list
        self.register_heur_dissector_list.restype = self.heur_dissector_list_t
        self.register_heur_dissector_list.argtypes = [c_char_p, c_int]

        # void heur_dissector_table_foreach(const char *table_name,
        #     DATFunc_heur func, gpointer user_data);
        self.heur_dissector_table_foreach = libwireshark.heur_dissector_table_foreach
        self.heur_dissector_table_foreach.restype = None
        self.heur_dissector_table_foreach.argtypes = [
            c_char_p, self.DATFunc_heur, LibGLib2.gpointer]

        # void dissector_all_heur_tables_foreach_table (DATFunc_heur_table func,
        #     gpointer user_data, GCompareFunc compare_key_func);
        self.dissector_all_heur_table_foreach_table = libwireshark.dissector_all_heur_tables_foreach_table
        self.dissector_all_heur_table_foreach_table.restype = None
        self.dissector_all_heur_table_foreach_table.argtypes = [
            self.DATFunc_heur_table, LibGLib2.gpointer, LibGLib2.GCompareFunc]

        # gboolean has_heur_dissector_list(const gchar *name);
        self.has_heur_dissector_list = libwireshark.has_heur_dissector_list
        self.has_heur_dissector_list.restype = LibGLib2.gboolean
        self.has_heur_dissector_list.argtypes = [LibGLib2.gchar_p]

        # gboolean dissector_try_heuristic(heur_dissector_list_t sub_dissectors,
        # tvbuff_t *tvb, packet_info *pinfo, proto_tree *tree, heur_dtbl_entry_t
        # **hdtbl_entry, void *data);
        self.dissector_try_heuristic = libwireshark.dissector_try_heuristic
        self.dissector_try_heuristic.restype = LibGLib2.gboolean
        self.dissector_try_heuristic.argtypes = [
            self.heur_dissector_list_t, POINTER(
                self.tvbuff_t), POINTER(
                self.packet_info), POINTER(
                self.proto_tree), POINTER(
                    POINTER(
                        self.heur_dtbl_entry_t)), c_void_p]

        # heur_dissector_list_t find_heur_dissector_list(const char *name);
        self.find_heur_dissector_list = libwireshark.find_heur_dissector_list
        self.find_heur_dissector_list.restype = self.heur_dissector_list_t
        self.find_heur_dissector_list.argtypes = [c_char_p]

        # heur_dtbl_entry_t* find_heur_dissector_by_unique_short_name(const char
        # *short_name);
        self.find_heur_dissector_by_unique_short_name = libwireshark.find_heur_dissector_by_unique_short_name
        self.find_heur_dissector_by_unique_short_name.restype = POINTER(
            self.heur_dtbl_entry_t)
        self.find_heur_dissector_by_unique_short_name.argtypes = [c_char_p]

        # void heur_dissector_add(const char *name, heur_dissector_t dissector,
        # const char *display_name, const char *short_name, const int proto,
        # heuristic_enable_e enable);
        self.heur_dissector_add = libwireshark.heur_dissector_add
        self.heur_dissector_add.restype = None
        self.heur_dissector_add.argtypes = [c_char_p,
                                            self.heur_dissector_t,
                                            c_char_p,
                                            c_char_p,
                                            c_int,
                                            self.heuristic_enable_e]

        # void heur_dissector_delete(const char *name, heur_dissector_t dissector,
        # const int proto);
        self.heur_dissector_delete = libwireshark.heur_dissector_delete
        self.heur_dissector_delete.restype = None
        self.heur_dissector_delete.argtypes = [
            c_char_p, self.heur_dissector_t, c_int]

        # dissector_handle_t register_dissector(const char *name, dissector_t
        # dissector, const int proto);
        self.register_dissector = libwireshark.register_dissector
        self.register_dissector.restype = self.dissector_handle_t
        self.register_dissector.argtypes = [c_char_p, self.dissector_t, c_int]

        # dissector_handle_t register_dissector_with_data(const char *name,
        # dissector_cb_t dissector, const int proto, void *cb_data);
        self.register_dissector_with_data = libwireshark.register_dissector_with_data
        self.register_dissector_with_data.restype = self.dissector_handle_t
        self.register_dissector_with_data.argtypes = [
            c_char_p, self.dissector_cb_t, c_int, c_void_p]

        # const char *dissector_handle_get_short_name(const dissector_handle_t
        # handle);
        self.dissector_handle_get_short_name = libwireshark.dissector_handle_get_short_name
        self.dissector_handle_get_short_name.restype = c_char_p
        self.dissector_handle_get_short_name.argtypes = [
            self.dissector_handle_t]

        # int dissector_handle_get_protocol_index(const dissector_handle_t
        # handle);
        self.dissector_handle_get_protocol_index = libwireshark.dissector_handle_get_protocol_index
        self.dissector_handle_get_protocol_index.restype = c_int
        self.dissector_handle_get_protocol_index.argtypes = [
            self.dissector_handle_t]

        # GList* get_dissector_names(void);
        self.get_dissector_names = libwireshark.get_dissector_names
        self.get_dissector_names.restype = POINTER(LibGLib2.GList)
        self.get_dissector_names.argtypes = []

        # dissector_handle_t find_dissector(const char *name);
        self.find_dissector = libwireshark.find_dissector
        self.find_dissector.restype = self.dissector_handle_t
        self.find_dissector.argtypes = [c_char_p]

        # dissector_handle_t find_dissector_add_dependency(const char *name, const
        # int parent_proto);
        self.find_dissector_add_dependency = libwireshark.find_dissector_add_dependency
        self.find_dissector_add_dependency.restype = self.dissector_handle_t
        self.find_dissector_add_dependency.argtypes = [c_char_p, c_int]

        # const char *dissector_handle_get_dissector_name(const dissector_handle_t
        # handle);
        self.dissector_handle_get_dissector_name = libwireshark.dissector_handle_get_dissector_name
        self.dissector_handle_get_dissector_name.restype = c_char_p
        self.dissector_handle_get_dissector_name.argtypes = [
            self.dissector_handle_t]

        # dissector_handle_t create_dissector_handle(dissector_t dissector,
        #     const int proto);
        self.create_dissector_handle = libwireshark.create_dissector_handle
        self.create_dissector_handle.restype = self.dissector_handle_t
        self.create_dissector_handle.argtypes = [self.dissector_t, c_int]

        # dissector_handle_t create_dissector_handle_with_name(dissector_t dissector,
        #     const int proto, const char* name);
        self.create_dissector_handle_with_name = libwireshark.create_dissector_handle_with_name
        self.create_dissector_handle_with_name.restype = self.dissector_handle_t
        self.create_dissector_handle_with_name.argtypes = [
            self.dissector_t, c_int, c_char_p]

        # int call_dissector_with_data(dissector_handle_t handle, tvbuff_t *tvb,
        #     packet_info *pinfo, proto_tree *tree, void *data);
        self.call_dissector_with_data = libwireshark.call_dissector_with_data
        self.call_dissector_with_data.restype = c_int
        self.call_dissector_with_data.argtypes = [self.dissector_handle_t,
                                                  POINTER(self.tvbuff_t),
                                                  POINTER(self.packet_info),
                                                  POINTER(self.proto_tree),
                                                  c_void_p]

        # int call_dissector(dissector_handle_t handle, tvbuff_t *tvb,
        #     packet_info *pinfo, proto_tree *tree);
        self.call_dissector = libwireshark.call_dissector
        self.call_dissector.restype = c_int
        self.call_dissector.argtypes = [self.dissector_handle_t,
                                        POINTER(self.tvbuff_t),
                                        POINTER(self.packet_info),
                                        POINTER(self.proto_tree)]

        # int call_data_dissector(tvbuff_t *tvb, packet_info *pinfo, proto_tree
        # *tree);
        self.call_data_dissector = libwireshark.call_data_dissector
        self.call_data_dissector.restype = c_int
        self.call_data_dissector.argtypes = [
            POINTER(self.tvbuff_t),
            POINTER(self.packet_info),
            POINTER(self.proto_tree)]

        # int call_dissector_only(dissector_handle_t handle, tvbuff_t *tvb,
        #     packet_info *pinfo, proto_tree *tree, void *data);
        self.call_dissector_only = libwireshark.call_dissector_only
        self.call_dissector_only.restype = c_int
        self.call_dissector_only.argtypes = [self.dissector_handle_t,
                                             POINTER(self.tvbuff_t),
                                             POINTER(self.packet_info),
                                             POINTER(self.proto_tree),
                                             c_void_p]

        # void call_heur_dissector_direct(heur_dtbl_entry_t *heur_dtbl_entry, tvbuff_t *tvb,
        #     packet_info *pinfo, proto_tree *tree, void *data);
        self.call_heur_dissector_direct = libwireshark.call_heur_dissector_direct
        self.call_heur_dissector_direct.restype = None
        self.call_heur_dissector_direct.argtypes = [
            POINTER(
                self.heur_dtbl_entry_t), POINTER(
                self.tvbuff_t), POINTER(
                self.packet_info), POINTER(
                    self.proto_tree), c_void_p]

        # gboolean register_depend_dissector(const char* parent, const char*
        # dependent);
        self.register_depend_dissector = libwireshark.register_depend_dissector
        self.register_depend_dissector.restype = LibGLib2.gboolean
        self.register_depend_dissector.argtypes = [c_char_p, c_char_p]

        # gboolean deregister_depend_dissector(const char* parent, const char*
        # dependent);
        self.deregister_depend_dissector = libwireshark.deregister_depend_dissector
        self.deregister_depend_dissector.restype = LibGLib2.gboolean
        self.deregister_depend_dissector.argtypes = [c_char_p, c_char_p]

        # depend_dissector_list_t find_depend_dissector_list(const char* name);
        self.find_depend_dissector_list = libwireshark.find_depend_dissector_list
        self.find_depend_dissector_list.restype = self.depend_dissector_list_t
        self.find_depend_dissector_list.argtypes = [c_char_p]

        # void set_actual_length(tvbuff_t *tvb, const guint specified_len);
        self.set_actual_length = libwireshark.set_actual_length
        self.set_actual_length.restype = None
        self.set_actual_length.argtypes = [
            POINTER(self.tvbuff_t), LibGLib2.guint]

        # void register_init_routine(void (*func)(void));
        self.register_init_routine = libwireshark.register_init_routine
        self.register_init_routine.restype = None
        self.register_init_routine.argtypes = [CFUNCTYPE(None)]

        # void register_cleanup_routine(void (*func)(void));
        self.register_cleanup_routine = libwireshark.register_cleanup_routine
        self.register_cleanup_routine.restype = None
        self.register_cleanup_routine.argtypes = [CFUNCTYPE(None)]

        # void register_shutdown_routine(void (*func)(void));
        self.register_shutdown_routine = libwireshark.register_shutdown_routine
        self.register_shutdown_routine.restype = None
        self.register_shutdown_routine.argtypes = [CFUNCTYPE(None)]

        # void register_postseq_cleanup_routine(void (*func)(void));
        self.register_postseq_cleanup_routine = libwireshark.register_postseq_cleanup_routine
        self.register_postseq_cleanup_routine.restype = None
        self.register_postseq_cleanup_routine.argtypes = [CFUNCTYPE(None)]

        # void postseq_cleanup_all_protocols(void);
        self.postseq_cleanup_all_protocols = libwireshark.postseq_cleanup_all_protocols
        self.postseq_cleanup_all_protocols.restype = None
        self.postseq_cleanup_all_protocols.argtypes = []

        # void register_final_registration_routine(void (*func)(void));
        self.register_final_registration_routine = libwireshark.register_final_registration_routine
        self.register_final_registration_routine.restype = None
        self.register_final_registration_routine.argtypes = [CFUNCTYPE(None)]

        # void add_new_data_source(packet_info *pinfo, tvbuff_t *tvb,
        #     const char *name);
        self.add_new_data_source = libwireshark.add_new_data_source
        self.add_new_data_source.restype = None
        self.add_new_data_source.argtypes = [
            POINTER(self.packet_info),
            POINTER(self.tvbuff_t),
            c_char_p]

        # void remove_last_data_source(packet_info *pinfo);
        self.remove_last_data_source = libwireshark.remove_last_data_source
        self.remove_last_data_source.restype = None
        self.remove_last_data_source.argtypes = [POINTER(self.packet_info)]

        # char *get_data_source_name(const struct data_source *src);
        self.get_data_source_name = libwireshark.get_data_source_name
        self.get_data_source_name.restype = c_char_p
        self.get_data_source_name.argtypes = [POINTER(self.data_source)]

        # tvbuff_t *get_data_source_tvb(const struct data_source *src);
        self.get_data_source_tvb = libwireshark.get_data_source_tvb
        self.get_data_source_tvb.restype = POINTER(self.tvbuff_t)
        self.get_data_source_tvb.argtypes = [POINTER(self.data_source)]

        # tvbuff_t *get_data_source_tvb_by_name(packet_info *pinfo, const char
        # *name);
        self.get_data_source_tvb_by_name = libwireshark.get_data_source_tvb_by_name
        self.get_data_source_tvb_by_name.restype = POINTER(self.tvbuff_t)
        self.get_data_source_tvb_by_name.argtypes = [
            POINTER(self.packet_info), c_char_p]

        # void mark_frame_as_depended_upon(packet_info *pinfo, guint32
        # frame_num);
        self.mark_frame_as_depended_upon = libwireshark.mark_frame_as_depended_upon
        self.mark_frame_as_depended_upon.restype = None
        self.mark_frame_as_depended_upon.argtypes = [
            POINTER(self.packet_info), LibGLib2.guint32]

        # void dissector_dump_decodes(void);
        self.dissector_dump_decodes = libwireshark.dissector_dump_decodes
        self.dissector_dump_decodes.restype = None
        self.dissector_dump_decodes.argtypes = []

        # void dissector_dump_heur_decodes(void);
        self.dissector_dump_heur_decodes = libwireshark.dissector_dump_heur_decodes
        self.dissector_dump_heur_decodes.restype = None
        self.dissector_dump_heur_decodes.argtypes = []

        # void register_postdissector(dissector_handle_t handle);
        self.register_postdissector = libwireshark.register_postdissector
        self.register_postdissector.restype = None
        self.register_postdissector.argtypes = [self.dissector_handle_t]

        # void set_postdissector_wanted_hfids(dissector_handle_t handle,
        #     GArray *wanted_hfids);
        self.set_postdissector_wanted_hfids = libwireshark.set_postdissector_wanted_hfids
        self.set_postdissector_wanted_hfids.restype = None
        self.set_postdissector_wanted_hfids.argtypes = [
            self.dissector_handle_t, POINTER(LibGLib2.GArray)]

        # gboolean postdissectors_want_hfids(void);
        self.postdissectors_want_hfids = libwireshark.postdissectors_want_hfids
        self.postdissectors_want_hfids.restype = LibGLib2.gboolean
        self.postdissectors_want_hfids.argtypes = []

        # void
        # prime_epan_dissect_with_postdissector_wanted_hfids(epan_dissect_t
        # *edt);
        self.prime_epan_dissect_with_postdissector_wanted_hfids = libwireshark.prime_epan_dissect_with_postdissector_wanted_hfids
        self.prime_epan_dissect_with_postdissector_wanted_hfids.restype = None
        self.prime_epan_dissect_with_postdissector_wanted_hfids.argtypes = [
            POINTER(self.epan_dissect_t)]

        # const gchar         *col_format_to_string(const gint);
        self.col_format_to_string = libwireshark.col_format_to_string
        self.col_format_to_string.restype = LibGLib2.gchar_p
        self.col_format_to_string.argtypes = [LibGLib2.gint]

        # const gchar         *col_format_desc(const gint);
        self.col_format_desc = libwireshark.col_format_desc
        self.col_format_desc.restype = LibGLib2.gchar_p
        self.col_format_desc.argtypes = [LibGLib2.gint]

        # gint                 get_column_format(const gint);
        self.get_column_format = libwireshark.get_column_format
        self.get_column_format.restype = LibGLib2.gint
        self.get_column_format.argtypes = [LibGLib2.gint]

        # void                 set_column_format(const gint, const gint);
        self.set_column_format = libwireshark.set_column_format
        self.set_column_format.restype = None
        self.set_column_format.argtypes = [LibGLib2.gint, LibGLib2.gint]

        # void                 get_column_format_matches(gboolean *, const
        # gint);
        self.get_column_format_matches = libwireshark.get_column_format_matches
        self.get_column_format_matches.restype = None
        self.get_column_format_matches.argtypes = [
            POINTER(LibGLib2.gboolean), LibGLib2.gint]

        # gint                 get_column_format_from_str(const gchar *);
        self.get_column_format_from_str = libwireshark.get_column_format_from_str
        self.get_column_format_from_str.restype = LibGLib2.gint
        self.get_column_format_from_str.argtypes = [LibGLib2.gchar_p]

        # gchar               *get_column_title(const gint);
        self.get_column_title = libwireshark.get_column_title
        self.get_column_title.restype = LibGLib2.gchar_p
        self.get_column_title.argtypes = [LibGLib2.gint]

        # void                 set_column_title(const gint, const gchar *);
        self.set_column_title = libwireshark.set_column_title
        self.set_column_title.restype = None
        self.set_column_title.argtypes = [LibGLib2.gint, LibGLib2.gchar_p]

        # gboolean             get_column_visible(const gint);
        self.get_column_visible = libwireshark.get_column_visible
        self.get_column_visible.restype = LibGLib2.gboolean
        self.get_column_visible.argtypes = [LibGLib2.gint]

        # void                 set_column_visible(const gint, gboolean);
        self.set_column_visible = libwireshark.set_column_visible
        self.set_column_visible.restype = None
        self.set_column_visible.argtypes = [LibGLib2.gint, LibGLib2.gboolean]

        # gboolean             get_column_resolved(const gint);
        self.get_column_resolved = libwireshark.get_column_resolved
        self.get_column_resolved.restype = LibGLib2.gboolean
        self.get_column_resolved.argtypes = [LibGLib2.gint]

        # void                 set_column_resolved(const gint, gboolean);
        self.set_column_resolved = libwireshark.set_column_resolved
        self.set_column_resolved.restype = None
        self.set_column_resolved.argtypes = [LibGLib2.gint, LibGLib2.gboolean]

        # const gchar         *get_column_custom_fields(const gint);
        self.get_column_custom_fields = libwireshark.get_column_custom_fields
        self.get_column_custom_fields.restype = LibGLib2.gchar_p
        self.get_column_custom_fields.argtypes = [LibGLib2.gint]

        # void                 set_column_custom_fields(const gint, const char
        # *);
        self.set_column_custom_fields = libwireshark.set_column_custom_fields
        self.set_column_custom_fields.restype = None
        self.set_column_custom_fields.argtypes = [LibGLib2.gint, c_char_p]

        # gint                 get_column_custom_occurrence(const gint);
        self.get_column_custom_occurrence = libwireshark.get_column_custom_occurrence
        self.get_column_custom_occurrence.restype = LibGLib2.gint
        self.get_column_custom_occurrence.argtypes = [LibGLib2.gint]

        # void                 set_column_custom_occurrence(const gint, const
        # gint);
        self.set_column_custom_occurrence = libwireshark.set_column_custom_occurrence
        self.set_column_custom_occurrence.restype = None
        self.set_column_custom_occurrence.argtypes = [
            LibGLib2.gint, LibGLib2.gint]

        # const gchar         *get_column_width_string(const gint, const gint);
        self.get_column_width_string = libwireshark.get_column_width_string
        self.get_column_width_string.restype = LibGLib2.gchar_p
        self.get_column_width_string.argtypes = [LibGLib2.gint, LibGLib2.gint]

        # gint                 get_column_char_width(const gint format);
        self.get_column_char_width = libwireshark.get_column_char_width
        self.get_column_char_width.restype = LibGLib2.gint
        self.get_column_char_width.argtypes = [LibGLib2.gint]

        # gchar               *get_column_tooltip(const gint col);
        self.get_column_tooltip = libwireshark.get_column_tooltip
        self.get_column_tooltip.restype = LibGLib2.gchar_p
        self.get_column_tooltip.argtypes = [LibGLib2.gint]

        # void col_finalize(column_info *cinfo);
        self.col_finalize = libwireshark.col_finalize
        self.col_finalize.restype = None
        self.col_finalize.argtypes = [POINTER(self.column_info)]

        # void build_column_format_array(column_info *cinfo, const gint num_cols,
        # const gboolean reset_fences);
        self.build_column_format_array = libwireshark.build_column_format_array
        self.build_column_format_array.restype = None
        self.build_column_format_array.argtypes = [
            POINTER(self.column_info), LibGLib2.gint, LibGLib2.gboolean]

        # void                 column_dump_column_formats(void);
        self.column_dump_column_formats = libwireshark.column_dump_column_formats
        self.column_dump_column_formats.restype = None
        self.column_dump_column_formats.argtypes = []

        # #define ADDRESS_INIT_NONE ADDRESS_INIT(AT_NONE, 0, NULL)
        self.ADDRESS_INIT_NONE = self.ADDRESS_INIT(
            self.AT_NONE, c_int(0), c_void_p(0))

        # gchar* address_to_str(wmem_allocator_t *scope, const address *addr);
        self.address_to_str = libwireshark.address_to_str
        self.address_to_str.restype = LibGLib2.gchar_p
        self.address_to_str.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.address)]

        # gchar* address_with_resolution_to_str(wmem_allocator_t *scope, const
        # address *addr);
        self.address_with_resolution_to_str = libwireshark.address_with_resolution_to_str
        self.address_with_resolution_to_str.restype = LibGLib2.gchar_p
        self.address_with_resolution_to_str.argtypes = [
            POINTER(self.wmem_allocator_t), POINTER(self.address)]

        # gchar* tvb_address_with_resolution_to_str(wmem_allocator_t *scope,
        # tvbuff_t *tvb, int type, const gint offset);
        self.tvb_address_with_resolution_to_str = libwireshark.tvb_address_with_resolution_to_str
        self.tvb_address_with_resolution_to_str.restype = LibGLib2.gchar_p
        self.tvb_address_with_resolution_to_str.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.tvbuff_t), c_int, LibGLib2.gint]

        # const gchar *address_to_name(const address *addr);
        self.address_to_name = libwireshark.address_to_name
        self.address_to_name.restype = LibGLib2.gchar_p
        self.address_to_name.argtypes = [POINTER(self.address)]

        # gchar *address_to_display(wmem_allocator_t *allocator, const address
        # *addr);
        self.address_to_display = libwireshark.address_to_display
        self.address_to_display.restype = LibGLib2.gchar_p
        self.address_to_display.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.address)]

        # void     address_to_str_buf(const address *addr, gchar *buf, int
        # buf_len);
        self.address_to_str_buf = libwireshark.address_to_str_buf
        self.address_to_str_buf.restype = None
        self.address_to_str_buf.argtypes = [
            POINTER(self.address), LibGLib2.gchar_p, c_int]

        # gchar*	eui64_to_str(wmem_allocator_t *scope, const guint64 ad);
        self.eui64_to_str = libwireshark.eui64_to_str
        self.eui64_to_str.restype = LibGLib2.gchar_p
        self.eui64_to_str.argtypes = [
            POINTER(
                self.wmem_allocator_t),
            LibGLib2.guint64]

        # gchar*	abs_time_to_str(wmem_allocator_t *scope, const nstime_t*, const absolute_time_display_e fmt,
        #     gboolean show_zone);
        self.abs_time_to_str = libwireshark.abs_time_to_str
        self.abs_time_to_str.restype = LibGLib2.gchar_p
        self.abs_time_to_str.argtypes = [
            POINTER(self.wmem_allocator_t),
            POINTER(LibWSUtil.nstime_t),
            self.absolute_time_display_e,
            LibGLib2.gboolean]

        # gchar*	abs_time_secs_to_str(wmem_allocator_t *scope, const time_t, const absolute_time_display_e fmt,
        #     gboolean show_zone);
        self.abs_time_secs_to_str = libwireshark.abs_time_secs_to_str
        self.abs_time_secs_to_str.restype = LibGLib2.gchar_p
        self.abs_time_secs_to_str.argtypes = [
            POINTER(self.wmem_allocator_t),
            c_int64,
            self.absolute_time_display_e,
            LibGLib2.gboolean]

        # void    display_epoch_time(gchar *, int, const time_t,  gint32, const
        # to_str_time_res_t);
        self.display_epoch_time = libwireshark.display_epoch_time
        self.display_epoch_time.restype = None
        self.display_epoch_time.argtypes = [
            LibGLib2.gchar_p,
            c_int,
            c_int64,
            LibGLib2.gint32,
            self.to_str_time_res_t]

        # void    display_signed_time(gchar *, int, const gint32, gint32, const
        # to_str_time_res_t);
        self.display_signed_time = libwireshark.display_signed_time
        self.display_signed_time.restype = None
        self.display_signed_time.argtypes = [
            LibGLib2.gchar_p,
            c_int,
            LibGLib2.gint32,
            LibGLib2.gint32,
            self.to_str_time_res_t]

        # gchar*  signed_time_secs_to_str(wmem_allocator_t *scope, const gint32
        # time_val);
        self.signed_time_secs_to_str = libwireshark.signed_time_secs_to_str
        self.signed_time_secs_to_str.restype = LibGLib2.gchar_p
        self.signed_time_secs_to_str.argtypes = [
            POINTER(self.wmem_allocator_t), LibGLib2.gint32]

        # gchar*  unsigned_time_secs_to_str(wmem_allocator_t *scope, const
        # guint32);
        self.unsigned_time_secs_to_str = libwireshark.unsigned_time_secs_to_str
        self.unsigned_time_secs_to_str.restype = LibGLib2.gchar_p
        self.unsigned_time_secs_to_str.argtypes = [
            POINTER(self.wmem_allocator_t), LibGLib2.guint32]

        # gchar*  signed_time_msecs_to_str(wmem_allocator_t *scope, gint32
        # time_val);
        self.signed_time_msecs_to_str = libwireshark.signed_time_msecs_to_str
        self.signed_time_msecs_to_str.restype = LibGLib2.gchar_p
        self.signed_time_msecs_to_str.argtypes = [
            POINTER(self.wmem_allocator_t), LibGLib2.gint32]

        # void guint32_to_str_buf(guint32 u, gchar *buf, int buf_len);
        self.guint32_to_str_buf = libwireshark.guint32_to_str_buf
        self.guint32_to_str_buf.restype = None
        self.guint32_to_str_buf.argtypes = [
            LibGLib2.guint32, LibGLib2.gchar_p, c_int]

        # void guint64_to_str_buf(guint64 u, gchar *buf, int buf_len);
        self.guint64_to_str_buf = libwireshark.guint64_to_str_buf
        self.guint64_to_str_buf.restype = None
        self.guint64_to_str_buf.argtypes = [
            LibGLib2.guint64, LibGLib2.gchar_p, c_int]

        # gchar*	rel_time_to_str(wmem_allocator_t *scope, const nstime_t*);
        self.rel_time_to_str = libwireshark.rel_time_to_str
        self.rel_time_to_str.restype = LibGLib2.gchar_p
        self.rel_time_to_str.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                LibWSUtil.nstime_t)]

        # gchar*  rel_time_to_secs_str(wmem_allocator_t *scope, const
        # nstime_t*);
        self.rel_time_to_secs_str = libwireshark.rel_time_to_secs_str
        self.rel_time_to_secs_str.restype = LibGLib2.gchar_p
        self.rel_time_to_secs_str.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                LibWSUtil.nstime_t)]

        # gchar*	guid_to_str(wmem_allocator_t *scope, const e_guid_t*);
        self.guid_to_str = libwireshark.guid_to_str
        self.guid_to_str.restype = LibGLib2.gchar_p
        self.guid_to_str.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                self.e_guid_t)]

        # char *decode_bits_in_field(const guint bit_offset, const gint
        # no_of_bits, const guint64 value);
        self.decode_bits_in_field = libwireshark.decode_bits_in_field
        self.decode_bits_in_field.restype = c_char_p
        self.decode_bits_in_field.argtypes = [
            LibGLib2.guint, LibGLib2.gint, LibGLib2.guint64]

        # const gchar* port_type_to_str (port_type type);
        self.port_type_to_str = libwireshark.port_type_to_str
        self.port_type_to_str.restype = LibGLib2.gchar_p
        self.port_type_to_str.argtypes = [self.port_type]

        # gchar* tvb_address_to_str(wmem_allocator_t *scope, tvbuff_t *tvb, int
        # type, const gint offset);
        self.tvb_address_to_str = libwireshark.tvb_address_to_str
        self.tvb_address_to_str.restype = LibGLib2.gchar_p
        self.tvb_address_to_str.argtypes = [
            POINTER(self.wmem_allocator_t),
            POINTER(self.tvbuff_t),
            c_int,
            LibGLib2.gint]

        # gchar* tvb_address_var_to_str(wmem_allocator_t *scope, tvbuff_t *tvb,
        # address_type type, const gint offset, int length);
        self.tvb_address_var_to_str = libwireshark.tvb_address_var_to_str
        self.tvb_address_var_to_str.restype = LibGLib2.gchar_p
        self.tvb_address_var_to_str.argtypes = [
            POINTER(self.wmem_allocator_t),
            POINTER(self.tvbuff_t),
            self.address_type,
            LibGLib2.gint,
            c_int]

        # char *guint8_to_hex(char *out, guint8 val);
        self.guint8_to_hex = libwireshark.guint8_to_hex
        self.guint8_to_hex.restype = c_char_p
        self.guint8_to_hex.argtypes = [c_char_p, LibGLib2.guint8]

        # char *word_to_hex(char *out, guint16 word);
        self.word_to_hex = libwireshark.word_to_hex
        self.word_to_hex.restype = c_char_p
        self.word_to_hex.argtypes = [c_char_p, LibGLib2.guint16]

        # char *dword_to_hex(char *out, guint32 dword);
        self.dword_to_hex = libwireshark.dword_to_hex
        self.dword_to_hex.restype = c_char_p
        self.dword_to_hex.argtypes = [c_char_p, LibGLib2.guint32]

        # char *bytes_to_str(wmem_allocator_t *scope, const guint8 *bd, int
        # bd_len);
        self.bytes_to_str = libwireshark.bytes_to_str
        self.bytes_to_str.restype = c_char_p
        self.bytes_to_str.argtypes = [
            POINTER(
                self.wmem_allocator_t), POINTER(
                LibGLib2.guint8), c_int]

        # gchar *bytestring_to_str(wmem_allocator_t *scope, const guint8 *ad,
        # const guint32 len, const char punct);
        self.bytestring_to_str = libwireshark.bytestring_to_str
        self.bytestring_to_str.restype = LibGLib2.gchar_p
        self.bytestring_to_str.argtypes = [
            POINTER(self.wmem_allocator_t),
            POINTER(LibGLib2.guint8),
            LibGLib2.guint32,
            c_char]

        # char *bytes_to_hexstr(char *out, const guint8 *ad, guint32 len);
        self.bytes_to_hexstr = libwireshark.bytes_to_hexstr
        self.bytes_to_hexstr.restype = c_char_p
        self.bytes_to_hexstr.argtypes = [
            c_char_p, POINTER(
                LibGLib2.guint8), LibGLib2.guint32]

        # char *uint_to_str_back(char *ptr, guint32 value);
        self.uint_to_str_back = libwireshark.uint_to_str_back
        self.uint_to_str_back.restype = c_char_p
        self.uint_to_str_back.argtypes = [c_char_p, LibGLib2.guint32]
