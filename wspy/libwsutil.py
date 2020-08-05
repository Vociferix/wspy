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
from wspy.libglib2 import LibGLib2
from wspy.utils import *
import wspy.config as config
import sys
import os


class LibWSUtil:
    #########
    # TYPES #
    #########

    # typedef guint32 ws_in4_addr;
    ws_in4_addr = LibGLib2.guint32

    # typedef struct e_in6_addr {
    #     guint8 bytes[16];
    # } ws_in6_addr;

    class e_in6_addr(Structure):
        _fields_ = [('bytes', LibGLib2.guint8 * 16)]

    ws_in6_addr = e_in6_addr

    # struct ws_ip6_hdr {
    #     guint32 ip6h_vc_flow;
    #     guint16 ip6h_plen;
    #     guint8 ip6h_nxt;
    #     guint8 ip6h_hlim;
    #     ws_in6_addr ip6h_src;
    #     ws_in6_addr ip6h_dst;
    # };

    class ws_ip6_hdr(Structure):
        pass

    ws_ip6_hdr._fields_ = [('ip6h_vc_flow', LibGLib2.guint32),
                           ('ip6h_plen', LibGLib2.guint16),
                           ('ip6h_nxt', LibGLib2.guint8),
                           ('ip6h_hlim', LibGLib2.guint8),
                           ('ip6h_src', ws_in6_addr),
                           ('ip6h_dst', ws_in6_addr)]

    # struct ip6_ext {
    #     guchar ip6e_nxt;
    #     guchar ip6e_len;
    # };

    class ip6_ext(Structure):
        _fields_ = [('ip6e_nxt', LibGLib2.guchar),
                    ('ip6e_len', LibGLib2.guchar)]

    # struct ip6_rthdr {
    #     guint8 ip6r_nxt;
    #     guint8 ip6r_len;
    #     guint8 ip6r_type;
    #     guint8 ip6r_segleft;
    # };

    class ip6_rthdr(Structure):
        _fields_ = [('ip6r_nxt', LibGLib2.guint8),
                    ('ip6r_len', LibGLib2.guint8),
                    ('ip6r_type', LibGLib2.guint8),
                    ('ip6r_segleft', LibGLib2.guint8)]

    # struct ip6_rthdr0 {
    #     guint8 ip6r0_nxt;
    #     guint8 ip6r0_len;
    #     guint8 ip6r0_type;
    #     guint8 ip6r0_segleft;
    #     guint8 ip6r0_reserved;
    #     guint8 ip6r0_slmap[3];
    #     ws_in6_addr ip6r0_addr[1];
    # };

    class ip6_rthdr0(Structure):
        pass

    ip6_rthdr0._fields_ = [('ip6r0_nxt', LibGLib2.guint8),
                           ('ip6r0_len', LibGLib2.guint8),
                           ('ip6r0_type', LibGLib2.guint8),
                           ('ip6r0_segleft', LibGLib2.guint8),
                           ('ip6r0_reserved', LibGLib2.guint8),
                           ('ip6r0_slmap', LibGLib2.guint8 * 3),
                           ('ip6r0_addr', ws_in6_addr * 1)]

    # struct ip6_frag {
    #     guint8 ip6f_nxt;
    #     guint8 ip6f_reserved;
    #     guint16 ip6f_offlg;
    #     guint32 ip6f_ident;
    # };

    class ip6_frag(Structure):
        _fields_ = [('ip6f_nxt', LibGLib2.guint8),
                    ('ip6f_reserved', LibGLib2.guint8),
                    ('ip6f_offlg', LibGLib2.guint16),
                    ('ip6f_ident', LibGLib2.guint32)]

    # typedef struct {
    #     gchar patt[256];
    # #ifdef HAVE_SSE4_2
    #     gboolean use_sse42;
    #     __m128i mask;
    # #endif
    # } ws_mempbrk_pattern;

    class ws_mempbrk_pattern(Structure):
        _fields_ = [('patt', LibGLib2.gchar * 256),
                    ('use_sse42', LibGLib2.gboolean),
                    ('mask', c_uint8 * 16)]

    # typedef struct Buffer {
    #     guint8* data;
    #     gsize allocated;
    #     gsize start;
    #     gsize first_free;
    # } Buffer;

    class Buffer(Structure):
        _fields_ = [('data', POINTER(LibGLib2.guint8)),
                    ('allocated', LibGLib2.gsize),
                    ('start', LibGLib2.gsize),
                    ('first_free', LibGLib2.gsize)]

    # typedef struct {
    #     void (*register_codec_module)(void);
    # } codecs_plugin;

    class codecs_plugin(Structure):
        _fields_ = [('register_codec_module', CFUNCTYPE(None))]

    # struct codec_handle;
    # typedef struct codec_handle* codec_handle_t;

    class codec_handle(Structure):
        _fields_ = []

    codec_handle_t = POINTER(codec_handle)

    # typedef void* (*codec_init_fn)(void);
    codec_init_fn = CFUNCTYPE(c_void_p)

    # typedef void (*codec_release_fn)(void* context);
    codec_release_fn = CFUNCTYPE(None, c_void_p)

    # typedef unsigned (*codec_get_channels_fn)(void* context);
    codec_get_channels_fn = CFUNCTYPE(c_uint, c_void_p)

    # typedef unsigned (*codec_get_frequency_fn)(void* context);
    codec_get_frequency_fn = CFUNCTYPE(c_uint, c_void_p)

    # typedef size_t (*codec_decode_fn)(void* context,
    #                                   const void* inputBytes,
    #                                   size_t inputBytesSize,
    #                                   void* outputSamples,
    #                                   size_t* outputSamplesSize);
    codec_decode_fn = CFUNCTYPE(c_size_t,
                                c_void_p,
                                c_void_p,
                                c_size_t,
                                c_void_p,
                                POINTER(c_size_t))

    # typedef struct {
    #     guint16 red;
    #     guint16 green;
    #     guint16 blue;
    # } color_t;

    class color_t(Structure):
        _fields_ = [('red', LibGLib2.guint16),
                    ('green', LibGLib2.guint16),
                    ('blue', LibGLib2.guint16)]

    # typedef guint16 crc16_plain_t;
    crc16_plain_t = LibGLib2.guint16

    # typedef struct tagMAC_T {
    #     guint8 Mac[4];
    # } MAC_T;

    class tagMAC_T(Structure):
        _fields_ = [('Mac', LibGLib2.guint8 * 4)]

    MAC_T = tagMAC_T

    if os.name == 'nt':
        # #define ws_statb64 struct _stat64
        class _stat64(Structure):
            _fields_ = []

        ws_statb64 = _stat64
    else:
        # #define ws_statb64 struct stat
        class stat(Structure):
            _fields_ = []

        ws_statb64 = stat

    # typedef enum {
    #     JSMN_UNDEFINED = 0,
    #     JSMN_OBJECT = 1,
    #     JSMN_ARRAY = 2,
    #     JSMN_STRING = 3,
    #     JSMN_PRIMITIVE = 4
    # } jsmntype_t;
    jsmntype_t = c_int
    JSMN_UNDEFINED = c_int(0)
    JSMN_OBJECT = c_int(1)
    JSMN_ARRAY = c_int(2)
    JSMN_STRING = c_int(3)
    JSMN_PRIMITIVE = c_int(4)

    # enum jsmnerr {
    #     JSMN_ERROR_NOMEM = -1,
    #     JSMN_ERROR_INVAL = -2,
    #     JSMN_ERROR_PART = -3
    # };
    jsmnerr = c_int
    JSMN_ERROR_NOMEM = -1
    JSMN_ERROR_INVAL = -2
    JSMN_ERROR_PART = -3

    # typedef struct {
    #     jsmntype_t type;
    #     int start;
    #     int end;
    #     int size;
    #     int parent;
    # } jsmntok_t;

    class jsmntok_t(Structure):
        pass

    jsmntok_t._fields_ = [('type', jsmntype_t),
                          ('start', c_int),
                          ('end', c_int),
                          ('size', c_int),
                          ('parent', c_int)]

    # typedef struct {
    #     unsigned int pos;
    #     unsigned int toknext;
    #     int toksuper;
    # } jsmn_parser;

    class jsmn_parser(Structure):
        _fields_ = [('pos', c_uint),
                    ('toknext', c_uint),
                    ('toksuper', c_int)]

    # typedef struct json_dumper {
    #     FILE* output_file;
    #     int flags;
    #     int current_depth;
    #     gint base64_state;
    #     gint base64_save;
    #     guint8 state[JSON_DUMPER_MAX_DEPTH];
    # } json_dumper;

    class json_dumper(Structure):
        _fields_ = [('output_file', POINTER(c_void_p)),
                    ('flags', c_int),
                    ('current_depth', c_int),
                    ('base64_state', LibGLib2.gint),
                    ('base64_save', LibGLib2.gint),
                    ('state', LibGLib2.guint8 * 1100)]

    # struct mpa {
    #     unsigned int emphasis   :2;
    #     unsigned int original   :1;
    #     unsigned int copyright  :1;
    #     unsigned int modeext    :2;
    #     unsigned int mode       :2;
    #     unsigned int priv       :1;
    #     unsigned int padding    :1;
    #     unsigned int frequency  :2;
    #     unsigned int bitrate    :4;
    #     unsigned int protection :1;
    #     unsigned int layer      :2;
    #     unsigned int version    :2;
    #     unsigned int sync       :11;
    # };

    class mpa(Structure):
        _fields_ = [('emphasis', c_uint, 2),
                    ('original', c_uint, 1),
                    ('copyright', c_uint, 1),
                    ('modeext', c_uint, 2),
                    ('mode', c_uint, 2),
                    ('priv', c_uint, 1),
                    ('padding', c_uint, 1),
                    ('frequency', c_uint, 2),
                    ('bitrate', c_uint, 4),
                    ('protection', c_uint, 1),
                    ('layer', c_uint, 2),
                    ('version', c_uint, 2),
                    ('sync', c_uint, 11)]

    # #define MPA_UNMARSHAL(mpa, n) do { \
    #         (mpa)->sync       = MPA_UNMARSHAL_SYNC(n);       \
    #         (mpa)->version    = MPA_UNMARSHAL_VERSION(n);    \
    #         (mpa)->layer      = MPA_UNMARSHAL_LAYER(n);      \
    #         (mpa)->protection = MPA_UNMARSHAL_PROTECTION(n); \
    #         (mpa)->bitrate    = MPA_UNMARSHAL_BITRATE(n);    \
    #         (mpa)->frequency  = MPA_UNMARSHAL_FREQUENCY(n);  \
    #         (mpa)->padding    = MPA_UNMARSHAL_PADDING(n);    \
    #         (mpa)->priv       = MPA_UNMARSHAL_PRIVATE(n);    \
    #         (mpa)->mode       = MPA_UNMARSHAL_MODE(n);       \
    #         (mpa)->modeext    = MPA_UNMARSHAL_MODEEXT(n);    \
    #         (mpa)->copyright  = MPA_UNMARSHAL_COPYRIGHT(n);  \
    #         (mpa)->original   = MPA_UNMARSHAL_ORIGINAL(n);   \
    #         (mpa)->emphasis   = MPA_UNMARSHAL_EMPHASIS(n);   \
    #         } while (0)

    def MPA_UNMARSHAL(mpa, n):
        mpa[0].sync = MPA_UNMARSHAL_SYNC(n)
        mpa[0].version = MPA_UNMARSHAL_VERSION(n)
        mpa[0].layer = MPA_UNMARSHAL_LAYER(n)
        mpa[0].protection = MPA_UNMARSHAL_PROTECTION(n)
        mpa[0].bitrate = MPA_UNMARSHAL_BITRATE(n)
        mpa[0].frequency = MPA_UNMARSHAL_FREQUENCY(n)
        mpa[0].padding = MPA_UNMARSHAL_PADDING(n)
        mpa[0].priv = MPA_UNMARSHAL_PRIVATE(n)
        mpa[0].mode = MPA_UNMARSHAL_MODE(n)
        mpa[0].modeext = MPA_UNMARSHAL_MODEEXT(n)
        mpa[0].copyright = MPA_UNMARSHAL_COPYRIGHT(n)
        mpa[0].original = MPA_UNMARSHAL_ORIGINAL(n)
        mpa[0].emphasis = MPA_UNMARSHAL_EMPHASIS(n)

    # typedef struct {
    #     time_t secs;
    #     int nsecs;
    # } nstime_t;

    class nstime_t(Structure):
        _fields_ = [('secs', c_long), ('nsecs', c_int)]

    # typedef void (*plugin_register_func)(void);
    plugin_register_func = CFUNCTYPE(None)

    # typedef void plugins_t;
    plugins_t = None

    # typedef enum {
    #     WS_PLUGIN_EPAN,
    #     WS_PLUGIN_WIRETAP,
    #     WS_PLUGIN_CODEC
    # } plugin_type_e;
    plugin_type_e = c_int
    WS_PLUGIN_EPAN = c_int(0)
    WS_PLUGIN_WIRETAP = c_int(1)
    WS_PLUGIN_CODEC = c_int(2)

    # typedef void (*plugin_description_callback)(const char* name, const char* version,
    #                                             const char* types, const char* filename,
    #                                             void* user_data);
    plugin_description_callback = CFUNCTYPE(
        None, c_char_p, c_char_p, c_char_p, c_char_p, c_void_p)

    if os.name == 'nt':
        # typedef HANDLE ws_process_id
        ws_process_id = c_void_p
    else:
        # typedef pid_t ws_process_id
        ws_process_id = c_int32

    # (from gpg-error.h)
    # typedef unsigned int gpg_error_t;
    # (from gcrypt.h)
    # typedef gpg_error_t gcry_error_t;
    gcry_error_t = c_uint

    # (from gcrypt.h)
    # struct gcry_sexp;
    # typedef struct gcry_sexp* gcry_sexp_t;

    class gcry_sexp(Structure):
        _fields_ = []

    gcry_sexp_t = POINTER(gcry_sexp)

    # (from gnutls.h)
    # struct gnutls_x509_privkey_int;
    # typedef gnutls_x509_privkey_int* gnutls_x509_privkey_t;

    class gnutls_x509_privkey_int(Structure):
        _fields_ = []

    gnutls_x509_privkey_t = POINTER(gnutls_x509_privkey_int)

    # typedef struct _sober128_prng {
    #     unsigned long R[17];
    #     unsigned long initR[17];
    #     unsigned long konst;
    #     unsigned long sbuf;
    #     int nbuf;
    #     int flag;
    #     int set;
    # } sober128_prng;

    class sober128_prng(Structure):
        _fields_ = [('R', c_ulong * 17),
                    ('initR', c_ulong * 17),
                    ('konst', c_ulong),
                    ('sbuf', c_ulong),
                    ('nbuf', c_int),
                    ('flag', c_int),
                    ('set', c_int)]

    # typedef char nat_char
    nat_char = c_char

    class tm(Structure):
        _fields_ = []

    # typedef enum {
    #     format_size_unit_none = 0,
    #     format_size_unit_bytes = 1,
    #     format_size_unit_bits = 2,
    #     format_size_unit_bits_s = 3,
    #     format_size_unit_bytes_s = 4,
    #     format_size_unit_packets = 5,
    #     format_size_unit_packets_s = 6,
    #     format_size_prefix_si = 0 << 8,
    #     format_size_prefix_iec = 1 << 8,
    #     format_size_suffix_no_space = 1 << 16
    # } format_size_flags_e;
    format_size_flags_e = c_int
    format_size_unit_none = c_int(0)
    format_size_unit_bytes = c_int(1)
    format_size_unit_bits = c_int(2)
    format_size_uint_bits_s = c_int(3)
    format_size_unit_bytes_s = c_int(4)
    format_size_unit_packets = c_int(5)
    format_size_unit_packets_s = c_int(6)
    format_size_prefix_si = c_int(0)
    format_size_prefix_iec = c_int(0x100)
    format_size_suffix_no_space = c_int(0x10000)

    # struct option {
    #     const char* name;
    #     int has_arg;
    #     int* flag;
    #     int val;
    # };

    class option(Structure):
        _fields_ = [('name', c_char_p),
                    ('has_arg', c_int),
                    ('flag', POINTER(c_int)),
                    ('val', c_int)]

    if os.name == 'nt':
        # #define ws_pipe_handle HANDLE
        ws_pipe_handle = c_void_p
    else:
        # #define ws_pipe_handle int
        ws_pipe_handle = c_int

    # typedef struct _ws_pipe_t {
    #     GPid pid;
    #     gchar* stderr_msg;
    #     gint exitcode;
    #     gint stdin_fd;
    #     gint stdout_fd;
    #     gint stderr_fd;
    # #ifdef _WIN32
    #     HANDLE threadId;
    # #endif
    # } ws_pipe_t;
    if os.name == 'nt':
        class _ws_pipe_t(Structure):
            _fields_ = [('pid', LibGLib2.GPid),
                        ('stderr_msg', LibGLib2.gchar_p),
                        ('exitcode', LibGLib2.gint),
                        ('stdin_fd', LibGLib2.gint),
                        ('stdout_fd', LibGLib2.gint),
                        ('stderr_fd', LibGLib2.gint),
                        ('threadId', c_void_p)]
    else:
        class _ws_pipe_t(Structure):
            _fields_ = [('pid', LibGLib2.GPid),
                        ('stderr_msg', LibGLib2.gchar_p),
                        ('exitcode', LibGLib2.gint),
                        ('stdin_fd', LibGLib2.gint),
                        ('stdout_fd', LibGLib2.gint),
                        ('stderr_fd', LibGLib2.gint)]
    ws_pipe_t = _ws_pipe_t

    #######################
    # MACROS/INLINE FUNCS #
    #######################

    # #define in4_addr_is_local_network_control_block(addr) \
    #   ((addr & 0xffffff00) == 0xe0000000)

    def in4_addr_is_local_network_control_block(self, addr):
        return (addr.value & 0xffffff00) == 0xe0000000

    # #define in4_addr_is_multicast(addr) \
    #   ((addr & 0xf0000000) == 0xe0000000)

    def in4_addr_is_multicast(self, addr):
        return (addr.value & 0xf0000000) == 0xe0000000

    # static inline gboolean in6_addr_is_linklocal(const ws_in6_addr* a);

    def in6_addr_is_linklocal(self, a):
        if a[0].bytes[0].value == 0xfe and (
                a[0].bytes[1].value & 0xc0) == 0x80:
            return LibGLib2.gboolean(1)
        else:
            return LibGLib2.gboolean(0)

    # static inline gboolean in6_addr_is_sitelocal(const ws_in6_addr* a);

    def in6_addr_is_sitelocal(self, a):
        if a[0].bytes[0].value == 0xfe and (
                a[0].bytes[1].value & 0xc0) == 0xc0:
            return LibGLib2.gboolean(1)
        else:
            return LibGLib2.gboolean(0)

    # static inline gboolean in6_addr_is_multicast(const ws_in6_addr* a);

    def in6_addr_is_multicast(self, a):
        if a[0].bytes[0].value == 0xff:
            return LibGLib2.gboolean(1)
        else:
            return LibGLib2.gboolean(0)

    # static inline int ws_count_ones(const guint64 x);

    def ws_count_ones(self, x):
        bits = x.value - ((x.value >> 1) & 0x5555555555555555)
        bits = (bits & 0x3333333333333333) + \
            ((bits >> 2) & 0x3333333333333333)
        bits = (bits + (bits >> 4)) & 0x0F0F0F0F0F0F0F0F
        return c_int((bits * 0x0101010101010101) >> 56)

    # static inline int __ws_ctz32(guint32 x);
    __ws_ctz32_table = [
        0,
        1,
        28,
        2,
        29,
        14,
        24,
        3,
        30,
        22,
        20,
        15,
        25,
        17,
        4,
        8,
        31,
        27,
        13,
        23,
        21,
        19,
        16,
        7,
        26,
        12,
        18,
        6,
        11,
        5,
        10,
        9]

    def __ws_ctz32(self, x):
        return c_int(
            __ws_ctz32_table[(x.value & -(x.value & 0xFFFFFFFF)) >> 27])

    # static inline int ws_ctz(guint64 x);

    def ws_ctz(self, x):
        hi = (x.value >> 32) & 0xFFFFFFFF
        lo = x.value & 0xFFFFFFFF
        if lo == 0:
            return c_int(32 + self.__ws_ctz32(LibGLib2.guint32(hi)).value)
        else:
            return self.__ws_ctz32(LibGLib2.guint32(lo))

    # static inline int __ws_ilog2_32(guint32 x);
    __ws_ilog2_32_table = [
        0,
        9,
        1,
        10,
        13,
        21,
        2,
        29,
        11,
        14,
        16,
        18,
        22,
        25,
        3,
        30,
        8,
        12,
        20,
        28,
        15,
        17,
        24,
        7,
        19,
        27,
        23,
        6,
        26,
        5,
        4,
        31]

    def __ws_ilog2_32(self, x):
        x = x.value
        x |= x >> 1
        x |= x >> 2
        x |= x >> 4
        x |= x >> 8
        x |= x >> 16
        return c_int(__ws_ilog2_32_table[(x * 0x07C4ACDD) >> 27])

    # static inline int ws_ilog2(guint64 x);

    def ws_ilog2(self, x):
        hi = (x.value >> 32) & 0xFFFFFFFF
        lo = x.value & 0xFFFFFFFF
        if hi == 0:
            return self.__ws_ilog2_32(LibGLib2.guint32(lo))
        else:
            return c_int(32 + self.__ws_ilog2_32(LibGLib2.guint32(hi)).value)

    # #define ws_buffer_length(buffer) ((buffer)->first_free - (buffer)->start)

    def ws_buffer_length(self, buffer):
        return type(
            buffer[0].first_free)(
            buffer[0].first_free.value -
            buffer[0].start.value)

    # #define ws_buffer_clean(buffer) ws_buffer_remove_start((buffer), ws_buffer_length(buffer))

    def ws_buffer_clean(self, buffer):
        self.ws_buffer_remove_start(buffer, self.ws_buffer_length(buffer))

    # #define ws_buffer_increase_length(buffer,bytes) (buffer)->first_free += (bytes)

    def ws_buffer_increase_length(self, buffer, bytes):
        buffer[0].first_free = type(
            buffer[0].first_free)(
            buffer[0].first_free.value +
            bytes.value)

    # #define ws_buffer_start_ptr(buffer) ((buffer)->data + (buffer)->start)

    def ws_buffer_start_ptr(self, buffer):
        return type(
            buffer[0].data)(
            buffer[0].data.value +
            buffer[0].start.value)

    # #define ws_buffer_end_ptr(buffer) ((buffer)->data + (buffer)->first_free)

    def ws_buffer_end_ptr(self, buffer):
        return type(
            buffer[0].data)(
            buffer[0].data.value +
            buffer[0].first_free.value)

    # #define ws_buffer_append_buffer(buffer,src_buffer) ws_buffer_append((buffer), ws_buffer_start_ptr(src_buffer), ws_buffer_length(src_buffer))

    def ws_buffer_append_buffer(self, buffer, src_buffer):
        self.ws_buffer_append(buffer, self.ws_buffer_start_ptr(
            src_buffer), self.ws_buffer_length(src_buffer))

    # inline static unsigned int color_t_to_rgb(const color_t* color);

    def color_t_to_rgb(self, color):
        return (
            c_uint(
                color[0].red.value >> 8) << 16) | (
            c_uint(
                color[0].green.value >> 8) << 8) | c_uint(
            color[0].blue.value >> 8)

    # void ws_add_crash_info(const char* fmt, ...);

    def ws_add_crash_info(self, fmt, *argv):
        args, types = c_va_list(*argv)
        _ws_add_crash_info = self.dll.ws_add_crash_info
        _ws_add_crash_info.restype = None
        _ws_add_crash_info.argtypes = [c_char_p] + types
        _ws_add_crash_info(fmt, *args)

    # static inline crc16_plain_t crc16_plain_init(void);

    def crc16_plain_init(self):
        return crc16_plain_t(0)

    # static inline crc16_plain_t crc16_plain_finalize(crc16_plain_t crc);

    def crc16_plain_finalize(self, crc):
        return crc

    # #define CRC32C_SWAP(crc32c_value)                       \
    #         (((crc32c_value & 0xff000000) >> 24)    |       \
    #          ((crc32c_value & 0x00ff0000) >>  8)    |       \
    #          ((crc32c_value & 0x0000ff00) <<  8)    |       \
    #          ((crc32c_value & 0x000000ff) << 24))

    def CRC32C_SWAP(self, crc32c_value):
        return type(crc32c_value)(
            ((crc32c_value.value & 0xFF000000) >> 24) | (
                (crc32c_value.value & 0x00FF0000) >> 8) | (
                (crc32c_value.value & 0x0000FF00) << 8) | (
                    (crc32c_value.value & 0x000000FF) << 24))

    # static inline guint8 crc7init(void)

    def crc7init(self):
        return LibGLib2.guint8(0)

    # static inline guint8 crc7finalize(guint8 crc);

    def crc7finalize(self, crc):
        return type(crc)(crc.value >> 1)

    # #define FREQ_IS_BG(freq) (freq <= 2484)

    def FREQ_IS_BG(self, freq):
        return freq.value <= 2484

    # #define MPA_UNMARSHAL_SYNC(n)       ((n) >> 21 & 0x7ff)

    def MPA_UNMARHAL_SYNC(self, n):
        return c_uint((n.value >> 21) & 0x7ff)

    # #define MPA_UNMARSHAL_VERSION(n)    ((n) >> 19 & 0x3)

    def MPA_UNMARSHAL_VERSION(self, n):
        return c_uint((n.value >> 19) & 0x3)

    # #define MPA_UNMARSHAL_LAYER(n)      ((n) >> 17 & 0x3)

    def MPA_UNMARSHAL_LAYER(self, n):
        return c_uint((n.value >> 17) & 0x3)

    # #define MPA_UNMARSHAL_PROTECTION(n) ((n) >> 16 & 0x1)

    def MPA_UNMARSHAL_PROTECTION(self, n):
        return c_uint((n.value >> 16) & 0x1)

    # #define MPA_UNMARSHAL_BITRATE(n)    ((n) >> 12 & 0xf)

    def MPA_UNMARSHAL_BITRATE(self, n):
        return c_uint((n.value >> 12) & 0xf)

    # #define MPA_UNMARSHAL_FREQUENCY(n)  ((n) >> 10 & 0x3)

    def MPA_UNMARSHAL_FREQUENCY(self, n):
        return c_uint((n.value >> 10) & 0x3)

    # #define MPA_UNMARSHAL_PADDING(n)    ((n) >>  9 & 0x1)

    def MPA_UNMARSHAL_PADDING(self, n):
        return c_uint((n.value >> 9) & 0x1)

    # #define MPA_UNMARSHAL_PRIVATE(n)    ((n) >>  8 & 0x1)

    def MPA_UNMARSHAL_PRIVATE(self, n):
        return c_uint((n.value >> 8) & 0x1)

    # #define MPA_UNMARSHAL_MODE(n)       ((n) >>  6 & 0x3)

    def MPA_UNMARSHAL_MODE(self, n):
        return c_uint((n.value >> 6) & 0x3)

    # #define MPA_UNMARSHAL_MODEEXT(n)    ((n) >>  4 & 0x3)

    def MPA_UNMARSHAL_MODEEXT(self, n):
        return c_uint((n.value >> 4) & 0x3)

    # #define MPA_UNMARSHAL_COPYRIGHT(n)  ((n) >>  3 & 0x1)

    def MPA_UNMARSHAL_COPYRIGHT(self, n):
        return c_uint((n.value >> 3) & 0x1)

    # #define MPA_UNMARSHAL_ORIGINAL(n)   ((n) >>  2 & 0x1)

    def MPA_UNMARSHAL_ORIGINAL(self, n):
        return c_uint((n.value >> 2) & 0x1)

    # #define MPA_UNMARSHAL_EMPHASIS(n)   ((n) >>  0 & 0x3)

    def MPA_UNMARSHAL_EMPHASIS(self, n):
        return c_uint(n.value & 0x3)

    # #define MPA_DATA_BYTES(mpa) (mpa_bitrate(mpa) * mpa_samples(mpa) \
    #                 / mpa_frequency(mpa) / 8)

    def MPA_DATA_BYTES(self, mpa):
        return c_uint(
            self.mpa_bitrate(mpa).value *
            self.mpa_samples(mpa).value /
            self.mpa_frequency(mpa).value /
            8)

    # #define MPA_BYTES(mpa) (MPA_DATA_BYTES(mpa) + mpa_padding(mpa))

    def MPA_BYTES(self, mpa):
        return c_uint(
            self.MPA_DATA_BYTES(mpa).value +
            self.mpa_padding(mpa).value)

    # #define MPA_DURATION_NS(mpa) \
    #         (1000000000 / mpa_frequency(mpa) * mpa_samples(mpa))

    def MPA_DURATION_NS(self, mpa):
        return c_uint(
            1000000000 /
            self.mpa_frequency(mpa).value *
            self.mpa_samples(mpa).value)

    # #define MPA_SYNC_VALID(mpa)      ((mpa)->sync == MPA_SYNC)

    def MPA_SYNC_VALID(self, mpa):
        return mpa[0].sync.value == MPA_SYNC

    # #define MPA_VERSION_VALID(mpa)   (mpa_version(mpa) >= 0)

    def MPA_VERSION_VALID(self, mpa):
        return self.mpa_version(mpa).value >= 0

    # #define MPA_LAYER_VALID(mpa)     (mpa_layer(mpa) >= 0)

    def MPA_LAYER_VALID(self, mpa):
        return self.mpa_layer(mpa).value >= 0

    # #define MPA_BITRATE_VALID(mpa)   (mpa_bitrate(mpa) > 0)

    def MPA_BITRATE_VALID(self, mpa):
        return self.mpa_bitrate(mpa).value > 0

    # #define MPA_FREQUENCY_VALID(mpa) (mpa_frequency(mpa) > 0)

    def MPA_FREQUENCY_VALID(self, mpa):
        return self.mpa_frequency(mpa).value > 0

    # #define MPA_VALID(mpa) (MPA_SYNC_VALID(mpa) \
    #                 && MPA_VERSION_VALID(mpa) && MPA_LAYER_VALID(mpa) \
    #                 && MPA_BITRATE_VALID(mpa) && MPA_FREQUENCY_VALID(mpa))

    def MPA_VALID(self, mpa):
        return self.MPA_SYNC_VALID(mpa) and self.MPA_VERSION_VALID(mpa) and self.MPA_LAYER_VALID(
            mpa) and self.MPA_BITRATE_VALID(mpa) and self.MPA_FREQUENCY_VALID(mpa)

    # #define NSTIME_INIT_SECS_NSECS(secs, nsecs)     {secs, nsecs}

    def NSTIME_INIT_SECS_NSECS(self, secs, nsecs):
        return nstime_t(secs, nsecs)

    # #define NSTIME_INIT_SECS_USECS(secs, usecs)     {secs, usecs*1000}

    def NSTIME_INIT_SECS_USECS(self, secs, usecs):
        return nstime_t(secs, usecs.value * 1000)

    # #define NSTIME_INIT_SECS_MSECS(secs, msecs)     {secs, msecs*1000000}

    def NSTIME_INIT_SECS_MSECS(self, secs, msecs):
        return nstime_t(secs, msecs.value * 1000000)

    # #define NSTIME_INIT_SECS(secs)                  {secs, 0}

    def NSTIME_INIT_SECS(self, secs):
        return nstime_t(secs, 0)

    # #define nstime_add(sum, a) nstime_sum(sum, sum, a)

    def nstime_add(self, sum, a):
        self.nstime_sum(sum, sum, a)

    # #define nstime_subtract(sum, a) nstime_delta(sum, sum, a)

    def nstime_subtract(self, sum, a):
        self.nstime_delta(sum, sum, a)

    # static inline guint16 pntoh16(const void *p)

    def pntoh16(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint16((tmp[0].value << 8) | tmp[1].value)

    # static inline guint32 pntoh24(const void *p)

    def pntoh24(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint32((tmp[0].value << 16) | (
            tmp[1].value << 8) | tmp[2].value)

    # static inline guint32 pntoh32(const void *p)

    def pntoh32(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint32((
            tmp[0].value << 24) | (
            tmp[1].value << 16) | (
            tmp[2].value << 8) | tmp[3].value)

    # static inline guint64 pntoh40(const void *p)

    def pntoh40(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[0].value << 32) | (
            tmp[1].value << 24) | (
            tmp[2].value << 16) | (
            tmp[3].value << 8) | tmp[4].value)

    # static inline guint64 pntoh48(const void *p)

    def pntoh48(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[0].value << 40) | (
            tmp[1].value << 32) | (
            tmp[2].value << 24) | (
            tmp[3].value << 16) | (
            tmp[4].value << 8) | tmp[5].value)

    # static inline guint64 pntoh56(const void *p)

    def pntoh56(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[0].value << 48) | (
            tmp[1].value << 40) | (
            tmp[2].value << 32) | (
            tmp[3].value << 24) | (
            tmp[4].value << 16) | (
            tmp[5].value << 8) | tmp[6].value)

    # static inline guint64 pntoh64(const void *p)

    def pntoh64(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[0].value << 56) | (
            tmp[1].value << 48) | (
            tmp[2].value << 40) | (
            tmp[3].value << 32) | (
            tmp[4].value << 24) | (
            tmp[5].value << 16) | (
            tmp[6].value << 8) | tmp[7].value)

    # static inline guint16 pletoh16(const void *p)

    def pletoh16(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint16((tmp[1].value << 8) | tmp[0].value)

    # static inline guint32 pletoh24(const void *p)

    def pletoh24(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint32((tmp[2].value << 16) | (
            tmp[1].value << 8) | tmp[0].value)

    # static inline guint32 pletoh32(const void *p)

    def pletoh32(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint32((
            tmp[3].value << 24) | (
            tmp[2].value << 16) | (
            tmp[1].value << 8) | tmp[0].value)

    # static inline guint64 pletoh40(const void *p)

    def pletoh40(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[4].value << 32) | (
            tmp[3].value << 24) | (
            tmp[2].value << 16) | (
            tmp[1].value << 8) | tmp[0].value)

    # static inline guint64 pletoh48(const void *p)

    def pletoh48(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[5].value << 40) | (
            tmp[4].value << 32) | (
            tmp[3].value << 24) | (
            tmp[2].value << 16) | (
            tmp[1].value << 8) | tmp[0].value)

    # static inline guint64 pletoh56(const void *p)

    def pletoh56(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[6].value << 48) | (
            tmp[5].value << 40) | (
            tmp[4].value << 32) | (
            tmp[3].value << 24) | (
            tmp[2].value << 16) | (
            tmp[1].value << 8) | tmp[0].value)

    # static inline guint64 pletoh64(const void *p)

    def pntoh64(self, p):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        return LibGLib2.guint64((
            tmp[7].value << 56) | (
            tmp[6].value << 48) | (
            tmp[5].value << 40) | (
            tmp[4].value << 32) | (
            tmp[3].value << 24) | (
            tmp[2].value << 16) | (
            tmp[1].value << 8) | tmp[0].value)

    # static inline void phton16(guint8 *p, guint16 v)

    def phton16(self, p, v):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        tmp[0] = LibGLib2.guint8(v.value >> 8)
        tmp[1] = LibGLib2.guint8(v.value & 0xFF)

    # static inline void phton32(guint8 *p, guint32 v)

    def phton32(self, p, v):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        tmp[0] = LibGLib2.guint8((v.value >> 24) & 0xFF)
        tmp[1] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        tmp[2] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        tmp[3] = LibGLib2.guint8(v.value & 0xFF)

    # static inline void phton64(guint8 *p, guint64 v) {

    def phton64(self, p, v):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        tmp[0] = LibGLib2.guint8((v.value >> 56) & 0xFF)
        tmp[1] = LibGLib2.guint8((v.value >> 48) & 0xFF)
        tmp[2] = LibGLib2.guint8((v.value >> 40) & 0xFF)
        tmp[3] = LibGLib2.guint8((v.value >> 32) & 0xFF)
        tmp[4] = LibGLib2.guint8((v.value >> 24) & 0xFF)
        tmp[5] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        tmp[6] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        tmp[7] = LibGLib2.guint8(v.value & 0xFF)

    # static inline void phtole32(guint8 *p, guint32 v) {

    def phtole32(self, p, v):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        tmp[0] = LibGLib2.guint8(v.value & 0xFF)
        tmp[1] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        tmp[2] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        tmp[3] = LibGLib2.guint8((v.value >> 24) & 0xFF)

    # static inline void phtole64(guint8 *p, guint64 v) {

    def phtole64(self, p, v):
        tmp = cast(p, POINTER(LibGLib2.guint8))
        tmp[0] = LibGLib2.guint8(v.value & 0xFF)
        tmp[1] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        tmp[2] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        tmp[3] = LibGLib2.guint8((v.value >> 24) & 0xFF)
        tmp[4] = LibGLib2.guint8((v.value >> 32) & 0xFF)
        tmp[5] = LibGLib2.guint8((v.value >> 40) & 0xFF)
        tmp[6] = LibGLib2.guint8((v.value >> 48) & 0xFF)
        tmp[7] = LibGLib2.guint8((v.value >> 56) & 0xFF)

    # #define guint32_wraparound_diff(higher, lower) ((higher>lower)?(higher-lower):(higher+0xffffffff-lower+1))

    def guint32_wraparound_diff(self, higher, lower):
        if higher.value > lower.value:
            return LibGLib2.guint32(higher.value - lower.value)
        else:
            return LibGLib2.guint32(
                higher.value + 0xffffffff - lower.value + 1)

    # #define pow2(type, m)     (((type)1U) << (m))

    def pow2(self, type_, m):
        return type_(1 << m.value)

    # #define pow4(type, m)     (((type)1U) << (2*(m)))

    def pow4(self, type_, m):
        return type_(1 << (2 * m.value))

    # #define pow8(type, m)     (((type)1U) << (3*(m)))

    def pow8(self, type_, m):
        return type_(1 << (3 * m.value))

    # #define pow16(type, m)    (((type)1U) << (4*(m)))

    def pow16(self, type_, m):
        return type_(1 << (4 * m.value))

    # #define pow32(type, m)    (((type)1U) << (5*(m)))

    def pow32(self, type_, m):
        return type_(1 << (5 * m.value))

    # #define pow64(type, m)    (((type)1U) << (6*(m)))

    def pow64(self, type_, m):
        return type_(1 << (6 * m.value))

    # #define pow128(type, m)   (((type)1U) << (7*(m)))

    def pow128(self, type_, m):
        return type_(1 << (7 * m.value))

    # #define pow256(type, m)   (((type)1U) << (8*(m)))

    def pow256(self, type_, m):
        return type_(1 << (8 * m.value))

    # static inline gcry_error_t hkdf_extract(int hashalgo, const guint8*
    # salt, size_t salt_len, const guint8* ikm, size_t ikm_len, guint8* prk);

    def hkdf_extract(self, hashalgo, salt, salt_len, ikm, ikm_len, prk):
        return self.ws_hmac_buffer(hashalgo, prk, ikm, ikm_len, salt, salt_len)

    # void report_failure(const char* msg_format, ...);

    def report_failure(self, msg_format, *argv):
        args, types = c_va_list(*argv)
        _report_failure = self.dll.report_failure
        _report_failure.restype = None
        _report_failure.argtypes = [c_char_p] + types
        _report_failure(msg_format, *argv)

    # void report_warning(const char* msg_format, ...);

    def report_warning(self, msg_format, *argv):
        args, types = c_va_list(*argv)
        _report_warning = self.dll.report_warning
        _report_warning.restype = None
        _report_warning.argtypes = [c_char_p] + types
        _report_warning(msg_format, *argv)

    # static inline guint32 ws_sign_ext32(guint32 val, int no_of_bits);

    def ws_sign_ext32(self, val, no_of_bits):
        if no_of_bits.value == 0 or no_of_bits.value == 32:
            return val
        if val.value & (1 << (no_of_bits.value - 1)):
            val = type(val)(val.value | (0xFFFFFFFF << no_of_bits.value))
        return val

    # static inline guint64 ws_sign_ext64(guint64 val, int no_of_bits);

    def ws_sign_ext64(self, val, no_of_bits):
        if no_of_bits.value == 0 or no_of_bits.value == 64:
            return val
        if val.value & (1 << (no_of_bits.value - 1)):
            val = type(val)(
                val.value | (
                    0xFFFFFFFFFFFFFFFF << no_of_bits.value))
        return val

    # #define plurality(d,s,p) ((d) == 1 ? (s) : (p))

    def plurality(self, d, s, p):
        if d.value == 1:
            return s
        else:
            return p

    # void log_resource_usage(gboolean reset_delta, const char* format, ...);

    def log_resource_usage(self, reset_delta, format, *argv):
        args, types = c_va_list(*argv)
        _log_resource_usage = self.dll.log_resource_usage
        _log_resource_usage.restype = None
        _log_resource_usage.argtypes = [LibGLib2.gboolean, c_char_p] + types
        _log_resource_usage(reset_delta, format, *args)

    # #define         gdouble_to_guint64(value)   type_util_gdouble_to_guint64(value)

    def gdouble_to_guint64(self, value):
        return self.type_util_gdouble_to_guint64(value)

    # #define         guint64_to_gdouble(value)   type_util_guint64_to_gdouble(value)

    def guint64_to_gdouble(self, value):
        return self.type_util_guint64_to_gdouble(value)

    # static inline gboolean ws_pipe_valid(ws_pipe_t* ws_pipe);

    def ws_pipe_valid(self, ws_pipe):
        return ws_pipe.value != 0 and ws_pipe[0].pid.value != 0 and ws_pipe.pid.value != self.WS_INVALID_PID

    #############
    # CONSTANTS #
    #############

    # #define WS_IN4_LOOPBACK ((ws_in4_addr)GUINT32_TO_BE(0x7f000001))
    WS_IN4_LOOPBACK = ws_in4_addr(0x7f000001)

    # #define IPv6_ADDR_SIZE  16
    IPv6_ADDR_SIZE = 16

    # #define IPv6_HDR_SIZE           40
    IPv6_HDR_SIZE = 40

    # #define IPv6_FRAGMENT_HDR_SIZE  8
    IPv6_FRAGMENT_HDR_SIZE = 8

    # #define IP6F_OFF_MASK           0xfff8
    IP6F_OFF_MASK = 0xfff8

    # #define IP6F_RESERVED_MASK      0x0006
    IP6F_RESERVED_MASK = 0x0006

    # #define IP6F_MORE_FRAG          0x0001
    IP6F_MORE_FRAG = 0x0001

    # #define WS_INET_ADDRSTRLEN      16
    WS_INET_ADDRSTRLEN = 16

    # #define WS_INET6_ADDRSTRLEN     46
    WS_INET6_ADDRSTRLEN = 46

    # #define Base32_BAD_INPUT -1
    Base32_BAD_INPUT = -1

    # #define Base32_TOO_BIG -2
    Base32_TOO_BIG = -2

    # #define CRC_ALGO_TABLE_DRIVEN 1
    CRC_ALGO_TABLE_DRIVEN = 1

    # #define CRC32_CCITT_SEED 0xFFFFFFFF
    CRC32_CCITT_SEED = 0xFFFFFFFF

    # #define CRC32C_PRELOAD 0xFFFFFFFF
    CRC32C_PRELOAD = 0xFFFFFFFF

    # #define CRC32_MPEG2_SEED 0xFFFFFFFF
    CRC32_MPEG2_SEED = 0xFFFFFFFF

    # #define EAX_MODE_CLEARTEXT_AUTH     1
    EAX_MODE_CLEARTEXT_AUTH = 1

    # #define EAX_MODE_CIPHERTEXT_AUTH    2
    EAX_MODE_CIPHERTEXT_AUTH = 2

    # #define EAX_SIZEOF_KEY              16
    EAX_SIZEOF_KEY = 16

    # #define EPOCH_DELTA_1900_01_01_00_00_00_UTC 2208988800U
    EPOCH_DELTA_1900_01_01_00_00_00_UTC = 2208988800

    # #define EPOCH_DELTA_1904_01_01_00_00_00_UTC  2082844800U
    EPOCH_DELTA_1904_01_01_00_00_00_UTC = 2082844800

    # #define EPOCH_DELTA_1601_01_01_00_00_00_UTC G_GUINT64_CONSTANT(11644473600)
    EPOCH_DELTA_1601_01_01_00_00_00_UTC = 11644473600

    # #define DEFAULT_PROFILE      "Default"
    DEFAULT_PROFILE = b'Default'

    # #define JSON_DUMPER_MAX_DEPTH   1100
    JSON_DUMPER_MAX_DEPTH = 1100

    # #define JSON_DUMPER_FLAGS_PRETTY_PRINT  (1 << 0)
    JSON_DUMPER_FLAGS_PRETTY_PRINT = 1

    # #define JSON_DUMPER_DOT_TO_UNDERSCORE   (1 << 1)
    JSON_DUMPER_DOT_TO_UNDERSCORE = 2

    # enum { MPA_SYNC = 0x7ff };
    MPA_SYNC = 0x7ff

    # #define NSTIME_INIT_ZERO {0, 0}
    NSTIME_INIT_ZERO = nstime_t(0, 0)

    # #define NSTIME_INIT_UNSET {0, G_MAXINT}
    NSTIME_INIT_UNSET = nstime_t(0, 0x7FFFFFFF)

    # #define NSTIME_INIT_MAX {sizeof(time_t) > sizeof(int) ? LONG_MAX : INT_MAX, INT_MAX}
    NSTIME_INIT_MAX = nstime_t(0x7FFFFFFFFFFFFFFF, 0x7FFFFFFF)

    if os.name == 'nt':
        # #define WS_INVALID_PID INVALID_HANDLE_VALUE
        WS_INVALID_PID = cast(c_int(-1), ws_process_id)
    else:
        WS_INVALID_PID = ws_process_id(-1)

    # #define HASH_MD5_LENGTH      16
    HASH_MD5_LENGTH = 16

    # #define HASH_SHA1_LENGTH     20
    HASH_SHA1_LENGTH = 20

    # #define HASH_SHA2_224_LENGTH 28
    HASH_SHA2_244_LENGTH = 28

    # #define HASH_SHA2_256_LENGTH 32
    HASH_SHA2_256_LENGTH = 32

    # #define HASH_SHA2_384_LENGTH 48
    HASH_SHA2_384_LENGTH = 48

    # #define HASH_SHA2_512_LENGTH 64
    HASH_SHA2_512_LENGTH = 64

    # # define no_argument            0
    no_argument = 0

    # # define required_argument      1
    required_argument = 1

    # # define optional_argument      2
    optional_argument = 2

    ############
    # LOAD DLL #
    ############

    def __init__(self, libpath=config.get_libwsutil()):
        libwsutil = CDLL(libpath)
        self.dll = libwsutil

        # plugins_t* plugins_init(plugin_type_e type);
        self.plugins_init = libwsutil.plugins_init
        self.plugins_init.restype = c_void_p
        self.plugins_init.argtypes = [self.plugin_type_e]

        # const char* get_copyright_info(void);
        self.get_copyright_info = libwsutil.get_copyright_info
        self.get_copyright_info.restype = c_char_p
        self.get_copyright_info.argtypes = []

        # gchar* ws_init_sockets(void);
        self.ws_init_sockets = libwsutil.ws_init_sockets
        self.ws_init_sockets.restype = LibGLib2.gchar_p
        self.ws_init_sockets.argtypes = []

        # void ws_cleanup_sockets(void);
        self.ws_cleanup_sockets = libwsutil.ws_cleanup_sockets
        self.ws_init_sockets.restype = None
        self.ws_init_sockets.argtypes = []

        # int ws_socket_ptoa(struct sockaddr_storage* dst, const gchar* src,
        # guint16 def_port);
        self.ws_socket_ptoa = libwsutil.ws_socket_ptoa
        self.ws_socket_ptoa.restype = c_int
        self.ws_socket_ptoa.argtypes = [
            c_void_p, LibGLib2.gchar_p, LibGLib2.guint16]

        # const gchar* ws_inet_ntop4(gconstpointer src, gchar* dst, guint
        # dst_size);
        self.ws_inet_ntop4 = libwsutil.ws_inet_ntop4
        self.ws_inet_ntop4.restype = LibGLib2.gchar_p
        self.ws_inet_ntop4.argtypes = [
            LibGLib2.gconstpointer,
            LibGLib2.gchar_p,
            LibGLib2.guint]

        # const gchar* ws_inet_ntop6(gconstpointer src, gchar* dst, guint
        # dst_size);
        self.ws_inet_ntop6 = libwsutil.ws_inet_ntop6
        self.ws_inet_ntop6.restype = LibGLib2.gchar_p
        self.ws_inet_ntop6.argtypes = [
            LibGLib2.gconstpointer,
            LibGLib2.gchar_p,
            LibGLib2.guint]

        # gboolean ws_inet_pton4(const gchar* src, ws_in4_addr* dst);
        self.ws_inet_pton4 = libwsutil.ws_inet_pton4
        self.ws_inet_pton4.restype = LibGLib2.gboolean
        self.ws_inet_pton4argtypes = [
            LibGLib2.gchar_p, POINTER(
                self.ws_in4_addr)]

        # gboolean ws_inet_pton6(const gchar* src, ws_in6_addr* dst);
        self.ws_inet_pton6 = libwsutil.ws_inet_pton4
        self.ws_inet_pton6.restype = LibGLib2.gboolean
        self.ws_inet_pton6argtypes = [
            LibGLib2.gchar_p, POINTER(
                self.ws_in6_addr)]

        # void ws_mempbrk_compile(ws_mempbrk_pattern* pattern, const gchar*
        # needles);
        self.ws_mempbrk_compile = libwsutil.ws_mempbrk_compile
        self.ws_mempbrk_compile.restype = None
        self.ws_mempbrk_compile.argtypes = [
            POINTER(self.ws_mempbrk_pattern), LibGLib2.gchar_p]

        # const guint8* ws_mempbrk_exec(const guint8* haystack,
        #                               size_t haystacklen,
        #                               const ws_mempbrk_pattern* pattern,
        #                               guchar* found_needle);
        self.ws_mempbrk_exec = libwsutil.ws_mempbrk_exec
        self.ws_mempbrk_exec.restype = POINTER(LibGLib2.guint8)
        self.ws_mempbrk_exec.argtypes = [POINTER(LibGLib2.guint8),
                                         c_size_t,
                                         POINTER(self.ws_mempbrk_pattern),
                                         LibGLib2.guchar_p]

        # guint32 update_adler32(guint32 adler, const guint8* buf, size_t len);
        self.update_adler32 = libwsutil.update_adler32
        self.update_adler32.restype = LibGLib2.guint32
        self.update_adler32.argtypes = [
            LibGLib2.guint32, POINTER(
                LibGLib2.guint8), c_size_t]

        # guint32 adler32_bytes(const guint8* buf, size_t len);
        self.adler32_bytes = libwsutil.adler32_bytes
        self.adler32_bytes.restype = LibGLib2.guint32
        self.adler32_bytes.argtypes = [POINTER(LibGLib2.guint8), c_size_t]

        # guint32 adler32_str(const char* buf);
        self.adler32_str = libwsutil.adler32_str
        self.adler32_str.restype = LibGLib2.guint32
        self.adler32_str.argtypes = [c_char_p]

        # int ws_base32_decode(guint8* output,
        #                      const guint32 outputLength,
        #                      const guint8* in,
        #                      const guint32 inputLength);
        self.ws_base32_decode = libwsutil.ws_base32_decode
        self.ws_base32_decode.restype = c_int
        self.ws_base32_decode.argtypes = [POINTER(LibGLib2.guint8),
                                          LibGLib2.guint32,
                                          POINTER(LibGLib2.guint8),
                                          LibGLib2.guint32]

        # void bitswap_buf_inplace(guint8* buf, size_t len);
        self.bitswap_buf_inplace = libwsutil.bitswap_buf_inplace
        self.bitswap_buf_inplace.restype = None
        self.bitswap_buf_inplace.argtypes = [
            POINTER(LibGLib2.guint8), c_size_t]

        # void ws_buffer_init(Buffer* buffer, gsize space);
        self.ws_buffer_init = libwsutil.ws_buffer_init
        self.ws_buffer_init.restype = None
        self.ws_buffer_init.argtypes = [POINTER(self.Buffer), LibGLib2.gsize]

        # void ws_buffer_free(Buffer* buffer);
        self.ws_buffer_free = libwsutil.ws_buffer_free
        self.ws_buffer_free.restype = None
        self.ws_buffer_free.argtypes = [POINTER(self.Buffer)]

        # void ws_buffer_assure_space(Buffer* buffer, gsize space);
        self.ws_buffer_assure_space = libwsutil.ws_buffer_assure_space
        self.ws_buffer_assure_space.restype = None
        self.ws_buffer_assure_space.argtypes = [
            POINTER(self.Buffer), LibGLib2.gsize]

        # void ws_buffer_append(Buffer* buffer, guint8* from, gsize bytes);
        self.ws_buffer_append = libwsutil.ws_buffer_append
        self.ws_buffer_append.restype = None
        self.ws_buffer_append.argtypes = [
            POINTER(
                self.Buffer), POINTER(
                LibGLib2.guint8), LibGLib2.gsize]

        # void ws_buffer_remove_start(Buffer* buffer, gsize bytes);
        self.ws_buffer_remove_start = libwsutil.ws_buffer_remove_start
        self.ws_buffer_remove_start.restype = None
        self.ws_buffer_remove_start.argtypes = [
            POINTER(self.Buffer), LibGLib2.gsize]

        # void ws_buffer_cleanup(void);
        self.ws_buffer_cleanup = libwsutil.ws_buffer_cleanup
        self.ws_buffer_cleanup.restype = None
        self.ws_buffer_cleanup.argtypes = []

        # void codecs_register_plugin(const codecs_plugin* plug);
        self.codecs_register_plugin = libwsutil.codecs_register_plugin
        self.codecs_register_plugin.restype = None
        self.codecs_register_plugin.argtypes = [POINTER(self.codecs_plugin)]

        # void codecs_init(void);
        self.codecs_init = libwsutil.codecs_init
        self.codecs_init.restype = None
        self.codecs_init.argtypes = []

        # void codecs_cleanup(void);
        self.codecs_cleanup = libwsutil.codecs_cleanup
        self.codecs_cleanup.restype = None
        self.codecs_cleanup.argtypes = []

        # void codec_get_compiled_version_info(GString* str);
        #self.codec_get_compiled_version_info = libwsutil.codec_get_compiled_version_info
        #self.codec_get_compiled_version_info.restype = None
        #self.codec_get_compiled_version_info.argtypes = [POINTER(LibGLib2.GString)]

        # gboolean register_codec(const char* name,
        #                         codec_init_fn init_fn,
        #                         codec_release_fn release_fn,
        #                         codec_get_channels_fn channels_fn,
        #                         codec_get_frequency_fn frequency_fn,
        #                         codec_decode_fn decode_fn);
        self.register_codec = libwsutil.register_codec
        self.register_codec.restype = LibGLib2.gboolean
        self.register_codec.argtypes = [c_char_p,
                                        self.codec_init_fn,
                                        self.codec_release_fn,
                                        self.codec_get_channels_fn,
                                        self.codec_get_frequency_fn,
                                        self.codec_decode_fn]

        # gboolean deregister_codec(const char* name);
        self.deregister_codec = libwsutil.deregister_codec
        self.deregister_codec.restype = LibGLib2.gboolean
        self.deregister_codec.argtypes = [c_char_p]

        # codec_handle_t find_codec(const char* name);
        self.find_codec = libwsutil.find_codec
        self.find_codec.restype = self.codec_handle_t
        self.find_codec.argtypes = [c_char_p]

        # void* codec_init(codec_handle_t codec);
        self.codec_init = libwsutil.codec_init
        self.codec_init.restype = c_void_p
        self.codec_init.argtypes = [self.codec_handle_t]

        # void codec_release(codec_handle_t codec, void* context);
        self.codec_release = libwsutil.codec_release
        self.codec_release.restype = None
        self.codec_release.argtypes = [self.codec_handle_t, c_void_p]

        # unsigned codec_get_channels(codec_handle_t codec, void* context);
        self.codec_get_channels = libwsutil.codec_get_channels
        self.codec_get_channels.restype = c_uint
        self.codec_get_channels.argtypes = [self.codec_handle_t, c_void_p]

        # unsigned codec_get_frequency(codec_handle_t codec, void* context);
        self.codec_get_frequency = libwsutil.codec_get_frequency
        self.codec_get_frequency.restype = c_uint
        self.codec_get_frequency.argtypes = [self.codec_handle_t, c_void_p]

        # size_t codec_decode(codec_handle_t codec,
        #                     void* context,
        #                     const void* inputBytes,
        #                     size_t inputBytesSize,
        #                     void* outputSamples,
        #                     size_t* outputSamplesSize);
        self.codec_decode = libwsutil.codec_decode
        self.codec_decode.restype = c_size_t
        self.codec_decode.argtypes = [self.codec_handle_t,
                                      c_void_p,
                                      c_void_p,
                                      c_size_t,
                                      c_void_p,
                                      POINTER(c_size_t)]

        # void get_cpu_info(GString* str);
        self.get_cpu_info = libwsutil.get_cpu_info
        self.get_cpu_info.restype = None
        self.get_cpu_info.argtypes = [POINTER(LibGLib2.GString)]

        # guint16 update_crc10_by_bytes(guint16 crc10, const guint8* data_blk_ptr,
        # int data_blk_size);
        self.update_crc10_by_bytes = libwsutil.update_crc10_by_bytes
        self.update_crc10_by_bytes.restype = LibGLib2.guint16
        self.update_crc10_by_bytes.argtypes = [
            LibGLib2.guint16, POINTER(LibGLib2.guint8), c_int]

        # guint16 crc11_307_noreflect_noxor(const guint8* data, guint64
        # data_len);
        self.crc11_307_noreflect_noxor = libwsutil.crc11_307_noreflect_noxor
        self.crc11_307_noreflect_noxor.restype = LibGLib2.guint16
        self.crc11_307_noreflect_noxor.argtypes = [
            POINTER(LibGLib2.guint8), LibGLib2.guint64]

        # guint16 crc16_ccitt(const guint8* buf, guint len);
        self.crc16_ccitt = libwsutil.crc16_ccitt
        self.crc16_ccitt.restype = LibGLib2.guint16
        self.crc16_ccitt.argtypes = [POINTER(LibGLib2.guint8), LibGLib2.guint]

        # guint16 crc16_x25_ccitt_seed(const guint8* buf, guint len, guint16
        # seed);
        self.crc16_x25_ccitt_seed = libwsutil.crc16_x25_ccitt_seed
        self.crc16_x25_ccitt_seed.restype = LibGLib2.guint16
        self.crc16_x25_ccitt_seed.argtypes = [
            POINTER(LibGLib2.guint8), LibGLib2.guint, LibGLib2.guint16]

        # guint16 crc16_ccitt_seed(const guint8* buf, guint len, guint16 seed);
        self.crc16_ccitt_seed = libwsutil.crc16_ccitt_seed
        self.crc16_ccitt_seed.restype = LibGLib2.guint16
        self.crc16_ccitt_seed.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint16]

        # guint16 crc16_iso14443a(const guint8* buf, guint len);
        self.crc16_iso14443a = libwsutil.crc16_iso14443a
        self.crc16_iso14443a.restype = LibGLib2.guint16
        self.crc16_iso14443a.argtypes = [
            POINTER(LibGLib2.guint8), LibGLib2.guint]

        # guint16 crc16_usb(const guint8* buf, guint len);
        self.crc16_usb = libwsutil.crc16_usb
        self.crc16_usb.restype = LibGLib2.guint16
        self.crc16_usb.argtypes = [POINTER(LibGLib2.guint8), LibGLib2.guint]

        # guint16 crc16_0x5935(const guint8* buf, guint len, guint16 seed);
        self.crc16_0x5935 = libwsutil.crc16_0x5935
        self.crc16_0x5935.restype = LibGLib2.guint16
        self.crc16_0x5935.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint16]

        # guint16 crc16_0x755B(const guint8* buf, guint len, guint16 seed);
        self.crc16_0x755B = libwsutil.crc16_0x755B
        self.crc16_0x755B.restype = LibGLib2.guint16
        self.crc16_0x755B.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint16]

        # guint16 crc16_0x9949_seed(const guint8* buf, guint len, guint16
        # seed);
        self.crc16_0x9949_seed = libwsutil.crc16_0x9949_seed
        self.crc16_0x9949_seed.restype = LibGLib2.guint16
        self.crc16_0x9949_seed.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint16]

        # guint16 crc16_0x3D65_seed(const guint8* buf, guint len, guint16
        # seed);
        self.crc16_0x3D65_seed = libwsutil.crc16_0x3D65_seed
        self.crc16_0x3D65_seed.restype = LibGLib2.guint16
        self.crc16_0x3D65_seed.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint16]

        # guint16 crc16_0x080F_seed(const guint8* buf, guint len, guint16
        # seed);
        self.crc16_0x080F_seed = libwsutil.crc16_0x080F_seed
        self.crc16_0x080F_seed.restype = LibGLib2.guint16
        self.crc16_0x080F_seed.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint16]

        # crc16_plain_t crc16_plain_update(crc16_plain_t crc, const unsigned char*
        # data, size_t data_len);
        self.crc16_plain_update = libwsutil.crc16_plain_update
        self.crc16_plain_update.restype = self.crc16_plain_t
        self.crc16_plain_update.argtypes = [
            self.crc16_plain_t, POINTER(c_ubyte), c_size_t]

        # guint16 crc16_8005_noreflect_noxor(const guint8* data, guint64
        # data_len);
        self.crc16_8005_noreflect_noxor = libwsutil.crc16_8005_noreflect_noxor
        self.crc16_8005_noreflect_noxor.restype = LibGLib2.guint16
        self.crc16_8005_noreflect_noxor.argtypes = [
            POINTER(LibGLib2.guint8), LibGLib2.guint64]

        # guint32 crc32_ccitt_table_lookup(guchar pos);
        self.crc32_ccitt_table_lookup = libwsutil.crc32_ccitt_table_lookup
        self.crc32_ccitt_table_lookup.restype = LibGLib2.guint32
        self.crc32_ccitt_table_lookup.argtypes = [LibGLib2.guchar]

        # guint32 crc32c_table_lookup(guchar pos);
        self.crc32c_table_lookup = libwsutil.crc32c_table_lookup
        self.crc32c_table_lookup.restype = LibGLib2.guint32
        self.crc32c_table_lookup.argtypes = [LibGLib2.guchar]

        # guint32 crc32c_calculate(const void* buf, int len, guint32 crc);
        self.crc32c_calculate = libwsutil.crc32c_calculate
        self.crc32c_calculate.restype = LibGLib2.guint32
        self.crc32c_calculate.argtypes = [c_void_p, c_int, LibGLib2.guint32]

        # guint32 crc32c_calculate_no_swap(const void* buf, int len, guint32
        # crc);
        self.crc32c_calculate_no_swap = libwsutil.crc32c_calculate_no_swap
        self.crc32c_calculate_no_swap.restype = LibGLib2.guint32
        self.crc32c_calculate_no_swap.argtypes = [
            c_void_p, c_int, LibGLib2.guint32]

        # guint32 crc32_ccitt(const guint8* buf, guint len);
        self.crc32_ccitt = libwsutil.crc32_ccitt
        self.crc32_ccitt.restype = LibGLib2.guint32
        self.crc32_ccitt.argtypes = [POINTER(LibGLib2.guint8), LibGLib2.guint]

        # guint32 crc32_ccitt_seed(const guint8* buf, guint len, guint32 seed);
        self.crc32_ccitt_seed = libwsutil.crc32_ccitt_seed
        self.crc32_ccitt_seed.restype = LibGLib2.guint32
        self.crc32_ccitt_seed.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint32]

        # guint32 crc32_mpeg2_seed(const guint8* buf, guint len, guint32 seed);
        self.crc32_mpeg2_seed = libwsutil.crc32_mpeg2_seed
        self.crc32_mpeg2_seed.restype = LibGLib2.guint32
        self.crc32_mpeg2_seed.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint32]

        # guint32 crc32_0x0AA725CF_seed(const guint8* buf, guint len, guint32
        # seed);
        self.crc32_0x0AA725CF_seed = libwsutil.crc32_0x0AA725CF_seed
        self.crc32_0x0AA725CF_seed.restype = LibGLib2.guint32
        self.crc32_0x0AA725CF_seed.argtypes = [
            POINTER(LibGLib2.guint8), LibGLib2.guint, LibGLib2.guint32]

        # guint32 crc32_0x5D6DCB_seed(const guint8* buf, guint len, guint32
        # seed);
        self.crc32_0x5D6DCB_seed = libwsutil.crc32_0x5D6DCB_seed
        self.crc32_0x5D6DCB_seed.restype = LibGLib2.guint32
        self.crc32_0x5D6DCB_seed.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint,
            LibGLib2.guint32]

        # int Dot11DecryptWepDecrypt(const guchar* seed, const size_t seed_len,
        # guchar* cypher_text, const size_t data_len);
        self.Dot11DecryptWepDecrypt = libwsutil.Dot11DecryptWepDecrypt
        self.Dot11DecryptWepDecrypt.restype = c_int
        self.Dot11DecryptWepDecrypt.argtypes = [
            POINTER(LibGLib2.guchar),
            c_size_t,
            POINTER(LibGLib2.guchar),
            c_size_t]

        # guint8 crc5_usb_11bit_input(guint16 input);
        self.crc5_usb_11bit_input = libwsutil.crc5_usb_11bit_input
        self.crc5_usb_11bit_input.restype = LibGLib2.guint8
        self.crc5_usb_11bit_input.argtypes = [LibGLib2.guint16]

        # guint8 crc5_usb_19bit_input(guint32 input);
        self.crc5_usb_19bit_input = libwsutil.crc5_usb_19bit_input
        self.crc5_usb_19bit_input.restype = LibGLib2.guint8
        self.crc5_usb_19bit_input.argtypes = [LibGLib2.guint32]

        # guint16 crc6_0X6F(guint16 crc6, const guint8* data_blk_ptr, int
        # data_blk_size);
        self.crc6_0X6F = libwsutil.crc6_0X6F
        self.crc6_0X6F.restype = LibGLib2.guint16
        self.crc6_0X6F.argtypes = [
            LibGLib2.guint16, POINTER(
                LibGLib2.guint8), c_int]

        # guint8 crc7update(guint8 crc, const unsigned char* data, int
        # data_len);
        self.crc7update = libwsutil.crc7update
        self.crc7update.restype = LibGLib2.guint8
        self.crc7update.argtypes = [LibGLib2.guint8, POINTER(c_ubyte), c_int]

        # guint8 crc8_0x2F(const guint8* buf, guint32 len, guint8 seed);
        self.crc8_0x2F = libwsutil.crc8_0x2F
        self.crc8_0x2F.restype = LibGLib2.guint8
        self.crc8_0x2F.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint32,
            LibGLib2.guint8]

        # guint8 crc8_0x37(const guint8* buf, guint32 len, guint8 seed);
        self.crc8_0x37 = libwsutil.crc8_0x37
        self.crc8_0x37.restype = LibGLib2.guint8
        self.crc8_0x37.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint32,
            LibGLib2.guint8]

        # guint8 crc8_0x3B(const guint8* buf, guint32 len, guint8 seed);
        self.crc8_0x3B = libwsutil.crc8_0x3B
        self.crc8_0x3B.restype = LibGLib2.guint8
        self.crc8_0x3B.argtypes = [
            POINTER(
                LibGLib2.guint8),
            LibGLib2.guint32,
            LibGLib2.guint8]

        # int crypto_scalarmult_curve25519(unsigned char* q, const unsigned char*
        # n, const unsigned char* p);
        self.crypto_scalarmult_curve25519 = libwsutil.crypto_scalarmult_curve25519
        self.crypto_scalarmult_curve25519.restype = c_int
        self.crypto_scalarmult_curve25519.argtypes = [
            POINTER(c_ubyte), POINTER(c_ubyte), POINTER(c_ubyte)]

        # int crypto_scalarmult_curve25519_base(const unsigned char* n, const
        # unsigned char* p);
        self.crypto_scalarmult_curve25519_base = libwsutil.crypto_scalarmult_curve25519_base
        self.crypto_scalarmult_curve25519_base.restype = c_int
        self.crypto_scalarmult_curve25519_base.argtypes = [
            POINTER(c_ubyte), POINTER(c_ubyte)]

        # gboolean Eax_Decrypt(guint8* pN, guint8* pK, guint8* pC,
        #                      guint32 SizeN, guint32 SizeK, guint32 SizeC,
        #                      MAC_T* pMac, guint8 Mode);
        self.Eax_Decrypt = libwsutil.Eax_Decrypt
        self.Eax_Decrypt.restype = LibGLib2.gboolean
        self.Eax_Decrypt.argtypes = [
            POINTER(
                LibGLib2.guint8), POINTER(
                LibGLib2.guint8), POINTER(
                LibGLib2.guint8), LibGLib2.guint32, LibGLib2.guint32, LibGLib2.guint32, POINTER(
                    self.MAC_T), LibGLib2.guint8]

        # char* init_progfile_dir(const char* arg0);
        self.init_progfile_dir = libwsutil.init_progfile_dir
        self.init_progfile_dir.restype = c_char_p
        self.init_progfile_dir.argtypes = [c_char_p]

        # const char* get_progfile_dir(void);
        self.get_progfile_dir = libwsutil.get_progfile_dir
        self.get_progfile_dir.restype = c_char_p
        self.get_progfile_dir.argtypes = []

        # const char* get_plugins_dir(void);
        self.get_plugins_dir = libwsutil.get_plugins_dir
        self.get_plugins_dir.restype = c_char_p
        self.get_plugins_dir.argtypes = []

        # const char* get_plugins_dir_with_version(void);
        self.get_plugins_dir_with_version = libwsutil.get_plugins_dir_with_version
        self.get_plugins_dir_with_version.restype = c_char_p
        self.get_plugins_dir_with_version.argtypes = []

        # const char* get_plugins_pers_dir(void);
        self.get_plugins_pers_dir = libwsutil.get_plugins_pers_dir
        self.get_plugins_pers_dir.restype = c_char_p
        self.get_plugins_pers_dir.argtypes = []

        # const char* get_plugins_pers_dir_with_version(void);
        self.get_plugins_pers_dir_with_version = libwsutil.get_plugins_pers_dir_with_version
        self.get_plugins_pers_dir_with_version.restype = c_char_p
        self.get_plugins_pers_dir_with_version.argtypes = []

        # const char* get_extcap_dir(void);
        self.get_extcap_dir = libwsutil.get_extcap_dir
        self.get_extcap_dir.restype = c_char_p
        self.get_extcap_dir.argtypes = []

        # gboolean running_in_build_directory(void);
        self.running_in_build_directory = libwsutil.running_in_build_directory
        self.running_in_build_directory.restype = LibGLib2.gboolean
        self.running_in_build_directory.argtypes = []

        # const char* get_datafile_dir(void);
        self.get_datafile_dir = libwsutil.get_datafile_dir
        self.get_datafile_dir.restype = c_char_p
        self.get_datafile_dir.argtypes = []

        # const char* get_datafile_path(const char* filename);
        self.get_datafile_path = libwsutil.get_datafile_path
        self.get_datafile_path.restype = c_char_p
        self.get_datafile_path.argtypes = [c_char_p]

        # const char* get_systemfile_dir(void);
        self.get_systemfile_dir = libwsutil.get_systemfile_dir
        self.get_systemfile_dir.restype = c_char_p
        self.get_systemfile_dir.argtypes = []

        # void set_profile_name(const gchar* profilename);
        self.set_profile_name = libwsutil.set_profile_name
        self.set_profile_name.restype = None
        self.set_profile_name.argtypes = [LibGLib2.gchar_p]

        # const char* get_profile_name(void);
        self.get_profile_name = libwsutil.get_profile_name
        self.get_profile_name.restype = c_char_p
        self.get_profile_name.argtypes = []

        # gboolean is_default_profile(void);
        self.is_default_profile = libwsutil.is_default_profile
        self.is_default_profile.restype = LibGLib2.gboolean
        self.is_default_profile.argtypes = []

        # gboolean has_global_profiles(void);
        self.has_global_profiles = libwsutil.has_global_profiles
        self.has_global_profiles.restype = LibGLib2.gboolean
        self.has_global_profiles.argtypes = []

        # const char* get_profiles_dir(void);
        self.get_profiles_dir = libwsutil.get_profiles_dir
        self.get_profiles_dir.restype = c_char_p
        self.get_profiles_dir.argtypes = []

        # const char* get_profile_dir(const char* profilename, gboolean
        # is_global);
        self.get_profile_dir = libwsutil.get_profile_dir
        self.get_profile_dir.restype = c_char_p
        self.get_profile_dir.argtypes = [c_char_p, LibGLib2.gboolean]

        # int create_profiles_dir(char** pf_dir_path_return);
        self.create_profiles_dir = libwsutil.create_profiles_dir
        self.create_profiles_dir.restype = c_int
        self.create_profiles_dir.argtypes = [POINTER(c_char_p)]

        # const char* get_global_profiles_dir(void);
        self.get_global_profiles_dir = libwsutil.get_global_profiles_dir
        self.get_global_profiles_dir.restype = c_char_p
        self.get_global_profiles_dir.argtypes = []

        # void profile_store_persconffiles(gboolean store);
        self.profile_store_persconffiles = libwsutil.profile_store_persconffiles
        self.profile_store_persconffiles.restype = None
        self.profile_store_persconffiles.argtypes = [LibGLib2.gboolean]

        # gboolean profile_exists(const gchar* profilename, gboolean global);
        self.profile_exists = libwsutil.profile_exists
        self.profile_exists.restype = LibGLib2.gboolean
        self.profile_exists.argtypes = [LibGLib2.gchar_p, LibGLib2.gboolean]

        # int create_persconffile_profile(const char* profilename, char**
        # pf_dir_path_return);
        self.create_persconffile_profile = libwsutil.create_persconffile_profile
        self.create_persconffile_profile.restype = c_int
        self.create_persconffile_profile.argtypes = [
            c_char_p, POINTER(c_char_p)]

        # const GHashTable* allowed_profile_filenames(void);
        self.allowed_profile_filenames = libwsutil.allowed_profile_filenames
        self.allowed_profile_filenames.restype = POINTER(LibGLib2.GHashTable)
        self.allowed_profile_filenames.argtypes = []

        # int delete_perconffile_profile(const char* profilename, char**
        # pf_dir_path_return);
        self.delete_persconffile_profile = libwsutil.delete_persconffile_profile
        self.delete_persconffile_profile.restype = c_int
        self.delete_persconffile_profile.argtypes = [
            c_char_p, POINTER(c_char_p)]

        # int rename_persconffile_profile(const char* fromname, const char* toname,
        #                                 char** pf_from_dir_path_return,
        #                                 char** pf_to_dir_path_return);
        self.rename_persconffile_profile = libwsutil.rename_persconffile_profile
        self.rename_persconffile_profile.restype = c_int
        self.rename_persconffile_profile.argtypes = [
            c_char_p, c_char_p, POINTER(c_char_p), POINTER(c_char_p)]

        # int copy_persconffile_profile(const char* toname, const char* fromname,
        #                               gboolean from_global,
        #                               char** pf_filename_return,
        #                               char** pf_to_dir_path_return,
        #                               char** pf_from_dir_path_return);
        self.copy_persconffile_profile = libwsutil.copy_persconffile_profile
        self.copy_persconffile_profile.restype = c_int
        self.copy_persconffile_profile.argtypes = [c_char_p,
                                                   c_char_p,
                                                   LibGLib2.gboolean,
                                                   POINTER(c_char_p),
                                                   POINTER(c_char_p),
                                                   POINTER(c_char_p)]

        # int create_persconffile_dir(char** pf_dir_path_return);
        self.create_persconffile_dir = libwsutil.create_persconffile_dir
        self.create_persconffile_dir.restype = c_int
        self.create_persconffile_dir.argtypes = [POINTER(c_char_p)]

        # char* get_persconffile_path(const char* filename, gboolean
        # from_profile);
        self.get_persconffile_path = libwsutil.get_persconffile_path
        self.get_persconffile_path.restype = c_char_p
        self.get_persconffile_path.argtypes = [c_char_p, LibGLib2.gboolean]

        # void set_persconffile_dir(const char* p);
        self.set_persconffile_dir = libwsutil.set_persconffile_dir
        self.set_persconffile_dir.restype = None
        self.set_persconffile_dir.argtypes = [c_char_p]

        # const char* get_persdatafile_dir(void);
        self.get_persdatafile_dir = libwsutil.get_persdatafile_dir
        self.get_persdatafile_dir.restype = c_char_p
        self.get_persdatafile_dir.argtypes = []

        # void set_persdatafile_dir(const char* p);
        self.set_persdatafile_dir = libwsutil.set_persdatafile_dir
        self.set_persdatafile_dir.restype = None
        self.set_persdatafile_dir.argtypes = [c_char_p]

        # const char* file_open_error_message(int err, LibGLib2.gboolean
        # for_writing);
        self.file_open_error_message = libwsutil.file_open_error_message
        self.file_open_error_message.restype = c_char_p
        self.file_open_error_message.argtypes = [c_int, LibGLib2.gboolean]

        # const char* file_write_error_message(int err);
        self.file_write_error_message = libwsutil.file_write_error_message
        self.file_write_error_message.restype = c_char_p
        self.file_write_error_message.argtypes = [c_int]

        # const char* get_basename(const char*);
        self.get_basename = libwsutil.get_basename
        self.get_basename.restype = c_char_p
        self.get_basename.argtypes = [c_char_p]

        # const char* find_last_pathname_separator(const char* path);
        self.find_last_pathname_separator = libwsutil.find_last_pathname_separator
        self.find_last_pathname_separator.restype = c_char_p
        self.find_last_pathname_separator.argtypes = [c_char_p]

        # char* get_dirname(char*);
        self.get_dirname = libwsutil.get_dirname
        self.get_dirname.restype = c_char_p
        self.get_dirname.argtypes = [c_char_p]

        # int test_for_directory(const char*);
        self.test_for_directory = libwsutil.test_for_directory
        self.test_for_directory.restype = c_int
        self.test_for_directory.argtypes = [c_char_p]

        # int test_for_fifo(const char*);
        self.test_for_fifo = libwsutil.test_for_fifo
        self.test_for_fifo.restype = c_int
        self.test_for_fifo.argtypes = [c_char_p]

        # gboolean file_exists(const char* fname);
        self.file_exists = libwsutil.file_exists
        self.file_exists.restype = LibGLib2.gboolean
        self.file_exists.argtypes = [c_char_p]

        # gboolean config_file_exists_with_entries(const char* fname, char
        # comment_char);
        self.config_file_exists_with_entries = libwsutil.config_file_exists_with_entries
        self.config_file_exists_with_entries.restype = LibGLib2.gboolean
        self.config_file_exists_with_entries.argtypes = [c_char_p, c_char]

        # gboolean files_identical(const char* fname1, const char* fname2);
        self.files_identical = libwsutil.files_identical
        self.files_identical.restype = LibGLib2.gboolean
        self.files_identical.argtypes = [c_char_p, c_char_p]

        # gboolean file_needs_reopen(int fd, const char* filename);
        self.file_needs_reopen = libwsutil.file_needs_reopen
        self.file_needs_reopen.restype = LibGLib2.gboolean
        self.file_needs_reopen.argtypes = [c_int, c_char_p]

        # gboolean copy_file_binary_mode(const char* from_filename, const char*
        # to_filename);
        self.copy_file_binary_mode = libwsutil.copy_file_binary_mode
        self.copy_file_binary_mode.restype = LibGLib2.gboolean
        self.copy_file_binary_mode.argtypes = [c_char_p, c_char_p]

        # gchar* data_file_url(const gchar* filename);
        self.data_file_url = libwsutil.data_file_url
        self.data_file_url.restype = LibGLib2.gchar_p
        self.data_file_url.argtypes = [LibGLib2.gchar_p]

        # void free_progdirs(void)
        self.free_progdirs = libwsutil.free_progdirs
        self.free_progdirs.restype = None
        self.free_progdirs.argtypes = []

        # gint ieee80211_mhz_to_chan(guint freq);
        self.ieee80211_mhz_to_chan = libwsutil.ieee80211_mhz_to_chan
        self.ieee80211_mhz_to_chan.restype = LibGLib2.gint
        self.ieee80211_mhz_to_chan.argtypes = [LibGLib2.guint]

        # guint ieee80211_chan_to_mhz(gint chan, gboolean is_bg)
        self.ieee80211_chan_to_mhz = libwsutil.ieee80211_chan_to_mhz
        self.ieee80211_chan_to_mhz.restype = LibGLib2.guint
        self.ieee80211_chan_to_mhz.argtypes = [
            LibGLib2.gint, LibGLib2.gboolean]

        # gchar* ieee80211_mhz_to_str(guint freq);
        self.ieee80211_mhz_to_str = libwsutil.ieee80211_mhz_to_str
        self.ieee80211_mhz_to_str.restype = LibGLib2.gchar_p
        self.ieee80211_mhz_to_str.argtypes = [LibGLib2.guint]

        # unsigned char linear2alaw(int);
        self.linear2alaw = libwsutil.linear2alaw
        self.linear2alaw.restype = c_ubyte
        self.linear2alaw.argtypes = [c_int]

        # int alaw2linear(unsigned char);
        self.alaw2linear = libwsutil.alaw2linear
        self.alaw2linear.restype = c_int
        self.alaw2linear.argtypes = [c_ubyte]

        # unsigned char linear2ulaw(int);
        self.linear2ulaw = libwsutil.linear2ulaw
        self.linear2ulaw.restype = c_ubyte
        self.linear2ulaw.argtypes = [c_int]

        # int ulaw2linear(unsigned char);
        self.ulaw2linear = libwsutil.ulaw2linear
        self.ulaw2linear.restype = c_int
        self.ulaw2linear.argtypes = [c_ubyte]

        # GList* local_interfaces_to_list(void);
        self.local_interfaces_to_list = libwsutil.local_interfaces_to_list
        self.local_interfaces_to_list.restype = POINTER(LibGLib2.GList)
        self.local_interfaces_to_list.argtypes = []

        # void json_dumper_begin_object(json_dumper* dumper);
        self.json_dumper_begin_object = libwsutil.json_dumper_begin_object
        self.json_dumper_begin_object.restype = None
        self.json_dumper_begin_object.argtypes = [POINTER(self.json_dumper)]

        # void json_dumper_set_member_name(json_dumper* dumper, const char*
        # name);
        self.json_dumper_set_member_name = libwsutil.json_dumper_set_member_name
        self.json_dumper_set_member_name.restype = None
        self.json_dumper_set_member_name.argtypes = [
            POINTER(self.json_dumper), c_char_p]

        # void json_dumper_end_object(json_dumper* dumper);
        self.json_dumper_end_object = libwsutil.json_dumper_end_object
        self.json_dumper_end_object.restype = None
        self.json_dumper_end_object.argtypes = [POINTER(self.json_dumper)]

        # void json_dumper_begin_array(json_dumper* dumper);
        self.json_dumper_begin_array = libwsutil.json_dumper_begin_array
        self.json_dumper_begin_array.restype = None
        self.json_dumper_begin_array.argtypes = [POINTER(self.json_dumper)]

        # void json_dumper_end_array(json_dumper* dumper);
        self.json_dumper_end_array = libwsutil.json_dumper_end_array
        self.json_dumper_end_array.restype = None
        self.json_dumper_end_array.argtypes = [POINTER(self.json_dumper)]

        # void json_dumper_value_string(json_dumper* dumper, const char*
        # value);
        self.json_dumper_value_string = libwsutil.json_dumper_value_string
        self.json_dumper_value_string.restype = None
        self.json_dumper_value_string.argtypes = [
            POINTER(self.json_dumper), c_char_p]

        # void json_dumper_value_double(json_dumper* dumper, double value);
        self.json_dumper_value_double = libwsutil.json_dumper_value_double
        self.json_dumper_value_double.restype = None
        self.json_dumper_value_double.argtypes = [
            POINTER(self.json_dumper), c_double]

        # void json_dumper_begin_base64(json_dumper* dumper);
        self.json_dumper_begin_base64 = libwsutil.json_dumper_begin_base64
        self.json_dumper_begin_base64.restype = None
        self.json_dumper_begin_base64.argtypes = [POINTER(self.json_dumper)]

        # void json_dumper_end_base64(json_dumper* dumper);
        self.json_dumper_end_base64 = libwsutil.json_dumper_end_base64
        self.json_dumper_end_base64.restype = None
        self.json_dumper_end_base64.argtypes = [POINTER(self.json_dumper)]

        # void json_dumper_write_base64(json_dumper* dumper, const guchar* data,
        # size_t len);
        self.json_dumper_write_base64 = libwsutil.json_dumper_write_base64
        self.json_dumper_write_base64.restype = None
        self.json_dumper_write_base64.argtypes = [
            POINTER(self.json_dumper), POINTER(LibGLib2.guchar), c_size_t]

        # gboolean json_dumper_finish(json_dumper* dumper);
        self.json_dumper_finish = libwsutil.json_dumper_finish
        self.json_dumper_finish.restype = LibGLib2.gboolean
        self.json_dumper_finish.argtypes = [POINTER(self.json_dumper)]

        # int mpa_version(const struct mpa*);
        self.mpa_version = libwsutil.mpa_version
        self.mpa_version.restype = c_int
        self.mpa_version.argtypes = [POINTER(self.mpa)]

        # int mpa_layer(const struct mpa*);
        self.mpa_layer = libwsutil.mpa_layer
        self.mpa_layer.restype = c_int
        self.mpa_layer.argtypes = [POINTER(self.mpa)]

        # unsigned int mpa_samples(const struct mpa*);
        self.mpa_samples = libwsutil.mpa_samples
        self.mpa_samples.restype = c_uint
        self.mpa_samples.argtypes = [POINTER(self.mpa)]

        # unsigned int mpa_bitrate(const struct mpa*);
        self.mpa_bitrate = libwsutil.mpa_bitrate
        self.mpa_bitrate.restype = c_uint
        self.mpa_bitrate.argtypes = [POINTER(self.mpa)]

        # unsigned int mpa_frequency(const struct mpa*);
        self.mpa_frequency = libwsutil.mpa_frequency
        self.mpa_frequency.restype = c_uint
        self.mpa_frequency.argtypes = [POINTER(self.mpa)]

        # unsigned int mpa_padding(const struct mpa*);
        self.mpa_padding = libwsutil.mpa_padding
        self.mpa_padding.restype = c_uint
        self.mpa_padding.argtypes = [POINTER(self.mpa)]

        # void nstime_set_zero(nstime_t* nstime);
        self.nstime_set_zero = libwsutil.nstime_set_zero
        self.nstime_set_zero.restype = None
        self.nstime_set_zero.argtypes = [POINTER(self.nstime_t)]

        # gboolean nstime_is_zero(nstime_t* nstime);
        self.nstime_is_zero = libwsutil.nstime_is_zero
        self.nstime_is_zero.restype = LibGLib2.gboolean
        self.nstime_is_zero.argtypes = [POINTER(self.nstime_t)]

        # void nstime_set_unset(nstime_t* nstime);
        self.nstime_set_unset = libwsutil.nstime_set_unset
        self.nstime_set_unset.restype = None
        self.nstime_set_unset.argtypes = [POINTER(self.nstime_t)]

        # gboolean nstime_copy(nstime_t* a, const nstime_t* b);
        self.nstime_copy = libwsutil.nstime_copy
        self.nstime_copy.restype = LibGLib2.gboolean
        self.nstime_copy.argtypes = [
            POINTER(
                self.nstime_t), POINTER(
                self.nstime_t)]

        # void nstime_delta(nstime_t* delta, const nstime_t* b, const nstime_t*
        # a);
        self.nstime_delta = libwsutil.nstime_delta
        self.nstime_delta.restype = None
        self.nstime_delta.argtypes = [
            POINTER(self.nstime_t),
            POINTER(self.nstime_t),
            POINTER(self.nstime_t)]

        # void nstime_sum(nstime_t* sum, const nstime_t* a, const nstime_t* b);
        self.nstime_sum = libwsutil.nstime_sum
        self.nstime_sum.restype = None
        self.nstime_sum.argtypes = [
            POINTER(
                self.nstime_t), POINTER(
                self.nstime_t), POINTER(
                self.nstime_t)]

        # int nstime_cmp(const nstime_t* a, const nstime_t* b);
        self.nstime_cmp = libwsutil.nstime_cmp
        self.nstime_cmp.restype = c_int
        self.nstime_cmp.argtypes = [
            POINTER(
                self.nstime_t), POINTER(
                self.nstime_t)]

        # double nstime_to_msec(const nstime_t* nstime);
        self.nstime_to_msec = libwsutil.nstime_to_msec
        self.nstime_to_msec.restype = c_double
        self.nstime_to_msec.argtypes = [POINTER(self.nstime_t)]

        # double nstime_to_sec(const nstime_t* nstime);
        self.nstime_to_sec = libwsutil.nstime_to_sec
        self.nstime_to_sec.restype = c_double
        self.nstime_to_sec.argtypes = [POINTER(self.nstime_t)]

        # gboolean filetime_to_nstime(nstime_t* nstime, guint64 filetime);
        self.filetime_to_nstime = libwsutil.filetime_to_nstime
        self.filetime_to_nstime.restype = LibGLib2.gboolean
        self.filetime_to_nstime.argtypes = [
            POINTER(self.nstime_t), LibGLib2.guint64]

        # gboolean nsfiletime_to_nstime(nstime_t* nstime, guint64 nsfiletime);
        self.nsfiletime_to_nstime = libwsutil.nsfiletime_to_nstime
        self.nsfiletime_to_nstime.restype = LibGLib2.gboolean
        self.nsfiletime_to_nstime.argtypes = [
            POINTER(self.nstime_t), LibGLib2.guint64]

        # void get_os_version_info(GString* str);
        self.get_os_version_info = libwsutil.get_os_version_info
        self.get_os_version_info.restype = None
        self.get_os_version_info.argtypes = [POINTER(LibGLib2.GString)]

        # const char* please_report_bug(void);
        self.please_report_bug = libwsutil.please_report_bug
        self.please_report_bug.restype = c_char_p
        self.please_report_bug.argtypes = []

        # const char* please_report_bug_short(void);
        self.please_report_bug_short = libwsutil.please_report_bug_short
        self.please_report_bug_short.restype = c_char_p
        self.please_report_bug_short.argtypes = []

        # void plugins_get_descriptions(plugin_description_callback callback,
        # void* user_data);
        self.plugins_get_descriptions = libwsutil.plugins_get_descriptions
        self.plugins_get_descriptions.restype = None
        self.plugins_get_descriptions.argtypes = [
            self.plugin_description_callback, c_void_p]

        # void plugins_dump_all(void);
        self.plugins_dump_all = libwsutil.plugins_dump_all
        self.plugins_dump_all.restype = None
        self.plugins_dump_all.argtypes = []

        # int plugins_get_count(void);
        self.plugins_get_count = libwsutil.plugins_get_count
        self.plugins_get_count.restype = c_int
        self.plugins_get_count.argtypes = []

        # void plugins_cleanup(plugins_t* plugins);
        self.plugins_cleanup = libwsutil.plugins_cleanup
        self.plugins_cleanup.restype = None
        self.plugins_cleanup.argtypes = [c_void_p]

        # void init_process_policies(void);
        self.init_process_policies = libwsutil.init_process_policies
        self.init_process_policies.restype = None
        self.init_process_policies.argtypes = []

        # gboolean started_with_special_privs(void);
        self.started_with_special_privs = libwsutil.started_with_special_privs
        self.started_with_special_privs.restype = LibGLib2.gboolean
        self.started_with_special_privs.argtypes = []

        # gboolean running_with_special_privs(void);
        self.running_with_special_privs = libwsutil.running_with_special_privs
        self.running_with_special_privs.restype = LibGLib2.gboolean
        self.running_with_special_privs.argtypes = []

        # void relinquish_special_privs_perm(void);
        self.relinquish_special_privs_perm = libwsutil.relinquish_special_privs_perm
        self.relinquish_special_privs_perm.restype = None
        self.relinquish_special_privs_perm.argtypes = []

        # gchar* get_cur_username(void);
        self.get_cur_username = libwsutil.get_cur_username
        self.get_cur_username.restype = LibGLib2.gchar_p
        self.get_cur_username.argtypes = []

        # gchar* get_cur_groupname(void);
        self.get_cur_groupname = libwsutil.get_cur_groupname
        self.get_cur_groupname.restype = LibGLib2.gchar_p
        self.get_cur_groupname.argtypes = []

        # gcry_error_t ws_hmac_buffer(int algo, void* digest, const void* buffer,
        # size_t length, const void *key, size_t keylen);
        self.ws_hmac_buffer = libwsutil.ws_hmac_buffer
        self.ws_hmac_buffer.restype = self.gcry_error_t
        self.ws_hmac_buffer.argtypes = [
            c_int,
            c_void_p,
            c_void_p,
            c_size_t,
            c_void_p,
            c_size_t]

        # gcry_error_t ws_cmac_buffer(int algo, void* digest, const void* buffer,
        # size_t length, const void* key, size_t keylen);
        self.ws_cmac_buffer = libwsutil.ws_cmac_buffer
        self.ws_cmac_buffer.restype = self.gcry_error_t
        self.ws_cmac_buffer.argtypes = [
            c_int,
            c_void_p,
            c_void_p,
            c_size_t,
            c_void_p,
            c_size_t]

        # void crypt_des_ecb(guint8* output, const guint8* buffer, const guint8*
        # key56);
        self.crypt_des_ecb = libwsutil.crypt_des_ecb
        self.crypt_des_ecb.restype = None
        self.crypt_des_ecb.argtypes = [
            POINTER(
                LibGLib2.guint8), POINTER(
                LibGLib2.guint8), POINTER(
                LibGLib2.guint8)]

        # size_t rsa_decrypt_inplace(const guint len, guchar* data, gcry_sexp_t
        # pk, gboolean pkcs1_padding, char** err);
        self.rsa_decrypt_inplace = libwsutil.rsa_decrypt_inplace
        self.rsa_decrypt_inplace.restype = c_size_t
        self.rsa_decrypt_inplace.argtypes = [
            LibGLib2.guint,
            POINTER(LibGLib2.guchar),
            self.gcry_sexp_t,
            LibGLib2.gboolean,
            POINTER(c_char_p)]

        # gcry_error_t hkdf_expand(int hashalgo, const guint8* prk, guint prk_len,
        # const guint8* info, guint info_len, guint8* out, guint out_len);
        self.hkdf_expand = libwsutil.hkdf_expand
        self.hkdf_expand.restype = self.gcry_error_t
        self.hkdf_expand.argtypes = [
            c_int,
            POINTER(LibGLib2.guint8),
            LibGLib2.guint,
            POINTER(LibGLib2.guint8),
            LibGLib2.guint,
            POINTER(LibGLib2.guint8),
            LibGLib2.guint]

        # void report_open_failure(const char* filename, int err, gboolean
        # for_writing);
        self.report_open_failure = libwsutil.report_open_failure
        self.report_open_failure.restype = None
        self.report_open_failure.argtypes = [
            c_char_p, c_int, LibGLib2.gboolean]

        # void report_read_failure(const char* filename, int err);
        self.report_read_failure = libwsutil.report_read_failure
        self.report_read_failure.restype = None
        self.report_read_failure.argtypes = [c_char_p, c_int]

        # void report_write_failure(const char* filename, int err);
        self.report_write_failure = libwsutil.report_write_failure
        self.report_write_failure.restype = None
        self.report_write_failure.argtypes = [c_char_p, c_int]

        # gcry_sexp_t rsa_privkey_to_sexp(gnutls_x509_privkey_t priv_key,
        # char** err);
        self.rsa_privkey_to_sexp = libwsutil.rsa_privkey_to_sexp
        self.rsa_privkey_to_sexp.restype = self.gcry_sexp_t
        self.rsa_privkey_to_sexp.argtypes = [
            self.gnutls_x509_privkey_t, POINTER(c_char_p)]

        # gnutls_x509_privkey_t rsa_load_pem_key(FILE* fp, char** err);
        self.rsa_load_pem_key = libwsutil.rsa_load_pem_key
        self.rsa_load_pem_key.restype = self.gnutls_x509_privkey_t
        self.rsa_load_pem_key.argtypes = [c_void_p, POINTER(c_char_p)]

        # gnutls_x509_privkey_t rsa_load_pkcs12(FILE* fp, const char* cert_passwd,
        # char** err);
        self.rsa_load_pkcs12 = libwsutil.rsa_load_pkcs12
        self.rsa_load_pkcs12.restype = self.gnutls_x509_privkey_t
        self.rsa_load_pkcs12.argtypes = [c_void_p, c_char_p, POINTER(c_char_p)]

        # void rsa_private_key_free(gpointer key);
        self.rsa_private_key_free = libwsutil.rsa_private_key_free
        self.rsa_private_key_free.restype = None
        self.rsa_private_key_free.argtypes = [LibGLib2.gpointer]

        # int sober128_start(sober128_prng* prng);
        self.sober128_start = libwsutil.sober128_start
        self.sober128_start.restype = c_int
        self.sober128_start.argtypes = [POINTER(self.sober128_prng)]

        # int sober128_add_entropy(const unsigned char* buf, unsigned long len,
        # sober128_prng* prng);
        self.sober128_add_entropy = libwsutil.sober128_add_entropy
        self.sober128_add_entropy.restype = c_int
        self.sober128_add_entropy.argtypes = [
            POINTER(c_ubyte),
            c_ulong,
            POINTER(self.sober128_prng)]

        # unsigned long sober128_read(unsigned char* buf, unsigned long len,
        # sober128_prng* prng);
        self.sober128_read = libwsutil.sober128_read
        self.sober128_read.restype = c_ulong
        self.sober128_read.argtypes = [
            POINTER(c_ubyte), c_ulong, POINTER(
                self.sober128_prng)]

        # int ws_ascii_strnatcmp(nat_char const* a, nat_char const* b);
        self.ws_ascii_strnatcmp = libwsutil.ws_ascii_strnatcmp
        self.ws_ascii_strnatcmp.restype = c_int
        self.ws_ascii_strnatcmp.argtypes = [
            POINTER(
                self.nat_char), POINTER(
                self.nat_char)]

        # int ws_ascii_strnatcasecmp(nat_char const* a, nat_char const* b);
        self.ws_ascii_strnatcasecmp = libwsutil.ws_ascii_strnatcasecmp
        self.ws_ascii_strnatcasecmp.restype = c_int
        self.ws_ascii_strnatcasecmp.argtypes = [
            POINTER(
                self.nat_char), POINTER(
                self.nat_char)]

        # char* strptime(const char*, const char*, struct tm*);
        self.strptime = libwsutil.strptime
        self.strptime.restype = c_char_p
        self.strptime.argtypes = [c_char_p, c_char_p, POINTER(self.tm)]

        # gboolean ws_strtoi64(const gchar* str, const gchar** endptr, gint64*
        # cint);
        self.ws_strtoi64 = libwsutil.ws_strtoi64
        self.ws_strtoi64.restype = LibGLib2.gboolean
        self.ws_strtoi64.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.gint64)]

        # gboolean ws_strtoi32(const gchar* str, const gchar** endptr, gint32*
        # cint);
        self.ws_strtoi32 = libwsutil.ws_strtoi32
        self.ws_strtoi32.restype = LibGLib2.gboolean
        self.ws_strtoi32.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.gint32)]

        # gboolean ws_strtoi16(const gchar* str, const gchar** endptr, gint16*
        # cint);
        self.ws_strtoi16 = libwsutil.ws_strtoi16
        self.ws_strtoi16.restype = LibGLib2.gboolean
        self.ws_strtoi16.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.gint16)]

        # gboolean ws_strtoi8(const gchar* str, const gchar** endptr, gint8*
        # cint);
        self.ws_strtoi8 = libwsutil.ws_strtoi8
        self.ws_strtoi8.restype = LibGLib2.gboolean
        self.ws_strtoi8.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.gint8)]

        # gboolean ws_strtou64(const gchar* str, const gchar** endptr, guint64*
        # cint);
        self.ws_strtou64 = libwsutil.ws_strtou64
        self.ws_strtou64.restype = LibGLib2.gboolean
        self.ws_strtou64.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint64)]

        # gboolean ws_strtou32(const gchar* str, const gchar** endptr, guint32*
        # cint);
        self.ws_strtou32 = libwsutil.ws_strtou32
        self.ws_strtou32.restype = LibGLib2.gboolean
        self.ws_strtou32.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint32)]

        # gboolean ws_strtou16(const gchar* str, const gchar** endptr, guint16*
        # cint);
        self.ws_strtou16 = libwsutil.ws_strtou16
        self.ws_strtou16.restype = LibGLib2.gboolean
        self.ws_strtou16.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint16)]

        # gboolean ws_strtou8(const gchar* str, const gchar** endptr, guint8*
        # cint);
        self.ws_strtou8 = libwsutil.ws_strtou8
        self.ws_strtou8.restype = LibGLib2.gboolean
        self.ws_strtou8.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint8)]

        # gboolean ws_hexstrtou64(const gchar* str, const gchar** endptr, guint64*
        # cint);
        self.ws_hexstrtou64 = libwsutil.ws_hexstrtou64
        self.ws_hexstrtou64.restype = LibGLib2.gboolean
        self.ws_hexstrtou64.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint64)]

        # gboolean ws_hexstrtou32(const gchar* str, const gchar** endptr, guint32*
        # cint);
        self.ws_hexstrtou32 = libwsutil.ws_hexstrtou32
        self.ws_hexstrtou32.restype = LibGLib2.gboolean
        self.ws_hexstrtou32.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint32)]

        # gboolean ws_hexstrtou16(const gchar* str, const gchar** endptr, guint16*
        # cint);
        self.ws_hexstrtou16 = libwsutil.ws_hexstrtou16
        self.ws_hexstrtou16.restype = LibGLib2.gboolean
        self.ws_hexstrtou16.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint16)]

        # gboolean ws_hexstrtou8(const gchar* str, const gchar** endptr,
        # guint8* cint);
        self.ws_hexstrtou8 = libwsutil.ws_hexstrtou8
        self.ws_hexstrtou8.restype = LibGLib2.gboolean
        self.ws_hexstrtou8.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint8)]

        # gboolean ws_basestrtou64(const gchar* str, const gchar** endptr,
        # guint64* cint, int base);
        self.ws_basestrtou64 = libwsutil.ws_basestrtou64
        self.ws_basestrtou64.restype = LibGLib2.gboolean
        self.ws_basestrtou64.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint64), c_int]

        # gboolean ws_basestrtou32(const gchar* str, const gchar** endptr,
        # guint32* cint, int base);
        self.ws_basestrtou32 = libwsutil.ws_basestrtou32
        self.ws_basestrtou32.restype = LibGLib2.gboolean
        self.ws_basestrtou32.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint32), c_int]

        # gboolean ws_basestrtou16(const gchar* str, const gchar** endptr,
        # guint16* cint, int base);
        self.ws_basestrtou16 = libwsutil.ws_basestrtou16
        self.ws_basestrtou16.restype = LibGLib2.gboolean
        self.ws_basestrtou16.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint16), c_int]

        # gboolean ws_basestrtou8(const gchar* str, const gchar** endptr, guint8*
        # cint, int base);
        self.ws_basestrtou8 = libwsutil.ws_basestrtou8
        self.ws_basestrtou8.restype = LibGLib2.gboolean
        self.ws_basestrtou8.argtypes = [
            LibGLib2.gchar_p, POINTER(
                LibGLib2.gchar_p), POINTER(
                LibGLib2.guint8), c_int]

        # char* ascii_strdown_inplace(gchar* str);
        self.ascii_strdown_inplace = libwsutil.ascii_strdown_inplace
        self.ascii_strdown_inplace.restype = c_char_p
        self.ascii_strdown_inplace.argtypes = [LibGLib2.gchar_p]

        # gchar* ascii_strup_inplace(gchar* str);
        self.ascii_strup_inplace = libwsutil.ascii_strup_inplace
        self.ascii_strup_inplace.restype = LibGLib2.gchar_p
        self.ascii_strup_inplace.argtypes = [LibGLib2.gchar_p]

        # gboolean isprint_string(const gchar* str);
        self.isprint_string = libwsutil.isprint_string
        self.isprint_string.restype = LibGLib2.gboolean
        self.isprint_string.argtypes = [LibGLib2.gchar_p]

        # gboolean isprint_utf8_string(const gchar* str, guint length);
        self.isprint_utf8_string = libwsutil.isprint_utf8_string
        self.isprint_utf8_string.restype = LibGLib2.gboolean
        self.isprint_utf8_string.argtypes = [LibGLib2.gchar_p, LibGLib2.guint]

        # gboolean isdigit_string(const guchar* str);
        self.isdigit_string = libwsutil.isdigit_string
        self.isdigit_string.restype = LibGLib2.gboolean
        self.isdigit_string.argtypes = [POINTER(LibGLib2.guchar)]

        # int ws_xton(char ch)
        self.ws_xton = libwsutil.ws_xton
        self.ws_xton.restype = c_int
        self.ws_xton.argtypes = [c_char]

        # gchar* format_size(gint64 size, format_size_flags_e flags);
        self.format_size = libwsutil.format_size
        self.format_size.restype = LibGLib2.gchar_p
        self.format_size.argtypes = [LibGLib2.gint64, self.format_size_flags_e]

        # gchar printable_char_or_period(gchar c);
        self.printable_char_or_period = libwsutil.printable_char_or_period
        self.printable_char_or_period.restype = LibGLib2.gchar
        self.printable_char_or_period.argtypes = [LibGLib2.gchar]

        # int create_tempfile(gchar** namebuf, const char* pfx, const char* sfx,
        # GError** err);
        self.create_tempfile = libwsutil.create_tempfile
        self.create_tempfile.restype = c_int
        self.create_tempfile.argtypes = [
            POINTER(LibGLib2.gchar_p),
            c_char_p,
            c_char_p,
            POINTER(
                POINTER(LibGLib2.GError))]

        # time_t mktime_utc(struct tm* tm);
        self.mktime_utc = libwsutil.mktime_utc
        self.mktime_utc.restype = c_ulong
        self.mktime_utc.argtypes = [POINTER(self.tm)]

        # void get_resource_usage(double* user_time, double* sys_time);
        self.get_resource_usage = libwsutil.get_resource_usage
        self.get_resource_usage.restype = None
        self.get_resource_usage.argtypes = [
            POINTER(c_double), POINTER(c_double)]

        # guint64 create_timestamp(void);
        self.create_timestamp = libwsutil.create_timestamp
        self.create_timestamp.restype = LibGLib2.guint64
        self.create_timestamp.argtypes = []

        # guint64 type_util_gdouble_to_guint64(gdouble value);
        self.type_util_gdouble_to_guint64 = libwsutil.type_util_gdouble_to_guint64
        self.type_util_gdouble_to_guint64.restype = LibGLib2.guint64
        self.type_util_gdouble_to_guint64.argtypes = [LibGLib2.gdouble]

        # gdouble type_util_guint64_to_gdouble(guint64 value);
        self.type_util_guint64_to_gdouble = libwsutil.type_util_guint64_to_gdouble
        self.type_util_guint64_to_gdouble.restype = LibGLib2.gdouble
        self.type_util_guint64_to_gdouble.argtypes = [LibGLib2.guint64]

        self.optarg = c_char_p.in_dll(libwsutil, 'optarg')

        self.optind = c_int.in_dll(libwsutil, 'optind')

        self.opterr = c_int.in_dll(libwsutil, 'opterr')

        self.optopt = c_int.in_dll(libwsutil, 'optopt')

        # int getopt(int ___argc, char* const* ___argv, const char*
        # __shortopts);
        self.getopt = libwsutil.getopt
        self.getopt.restype = c_int
        self.getopt.argtypes = [c_int, c_char_p, c_char_p]

        # int getopt_long(int ___argc, char* const* ___argv, const char*
        # __shortopts, const struct option* __longopts, int* __longind);
        self.getopt_long = libwsutil.getopt_long
        self.getopt_long.restype = c_int
        self.getopt_long.argtypes = [
            c_int,
            c_char_p,
            c_char_p,
            POINTER(self.option),
            POINTER(c_int)]

        # gboolean json_validate(const guint8* buf, const size_t len);
        self.json_validate = libwsutil.json_validate
        self.json_validate.restype = LibGLib2.gboolean
        self.json_validate.argtypes = [POINTER(LibGLib2.guint8), c_size_t]

        # int json_parse(const char* buf, jsmntok_t* tokens, unsigned int
        # max_tokens);
        self.json_parse = libwsutil.json_parse
        self.json_parse.restype = c_int
        self.json_parse.argtypes = [c_char_p, POINTER(self.jsmntok_t), c_uint]

        # jsmntok_t* json_get_object(const char* buf, jsmntok_t* parent, const
        # gchar* name);
        self.json_get_object = libwsutil.json_get_object
        self.json_get_object.restype = POINTER(self.jsmntok_t)
        self.json_get_object.argtypes = [
            c_char_p, POINTER(
                self.jsmntok_t), LibGLib2.gchar_p]

        # char* json_get_string(char* buf, jsmntok_t* parent, const gchar*
        # name);
        self.json_get_string = libwsutil.json_get_string
        self.json_get_string.restype = c_char_p
        self.json_get_string.argtypes = [
            c_char_p, POINTER(
                self.jsmntok_t), LibGLib2.gchar_p]

        # gboolean json_get_double(char* buf, jsmntok_t* parent, const gchar*
        # name, gdouble* val);
        self.json_get_double = libwsutil.json_get_double
        self.json_get_double.restype = LibGLib2.gboolean
        self.json_get_double.argtypes = [
            c_char_p,
            POINTER(self.jsmntok_t),
            LibGLib2.gchar_p,
            POINTER(LibGLib2.gdouble)]

        # gboolean json_decode_string_inplace(char* text);
        self.json_decode_string_inplace = libwsutil.json_decode_string_inplace
        self.json_decode_string_inplace.restype = LibGLib2.gboolean
        self.json_decode_string_inplace.argtypes = [c_char_p]

        # gboolean ws_pipe_spawn_sync(const gchar* working_directory, const gchar*
        # command, gint argc, gchar** args, gchar** command_output);
        self.ws_pipe_spawn_sync = libwsutil.ws_pipe_spawn_sync
        self.ws_pipe_spawn_sync.restype = LibGLib2.gboolean
        self.ws_pipe_spawn_sync.argtypes = [
            LibGLib2.gchar_p,
            LibGLib2.gchar_p,
            LibGLib2.gint,
            POINTER(LibGLib2.gchar_p),
            POINTER(LibGLib2.gchar_p)]

        # void ws_pipe_init(ws_pipe_t* ws_pipe);
        self.ws_pipe_init = libwsutil.ws_pipe_init
        self.ws_pipe_init.restype = None
        self.ws_pipe_init.argtypes = [POINTER(self.ws_pipe_t)]

        # GPid ws_pipe_spawn_async(ws_pipe_t* ws_pipe, GPtrArray* args);
        self.ws_pipe_spawn_async = libwsutil.ws_pipe_spawn_async
        self.ws_pipe_spawn_async.restype = LibGLib2.GPid
        self.ws_pipe_spawn_async.argtypes = [
            POINTER(
                self.ws_pipe_t), POINTER(
                LibGLib2.GPtrArray)]

        # void ws_pipe_close(ws_pipe_t* ws_pipe);
        self.ws_pipe_close = libwsutil.ws_pipe_close
        self.ws_pipe_close.restype = None
        self.ws_pipe_close.argtypes = [POINTER(self.ws_pipe_t)]

        # gboolean ws_pipe_data_available(int pipe_fd);
        self.ws_pipe_data_available = libwsutil.ws_pipe_data_available
        self.ws_pipe_data_available.restype = LibGLib2.gboolean
        self.ws_pipe_data_available.argtypes = [c_int]

        # gboolean ws_read_string_from_pipe(ws_pipe_handle read_pipe, gchar*
        # buffer, size_t buffer);
        self.ws_read_string_from_pipe = libwsutil.ws_read_string_from_pipe
        self.ws_read_string_from_pipe.restype = LibGLib2.gboolean
        self.ws_read_string_from_pipe.argtypes = [
            self.ws_pipe_handle, LibGLib2.gchar_p, c_size_t]

        # void decrypt_xtea_ecb(guint8 plaintext[8], const guint8 ciphertext[8],
        # const guint32 key[4], guint num_rounds);
        self.decrypt_xtea_ecb = libwsutil.decrypt_xtea_ecb
        self.decrypt_xtea_ecb.restype = None
        self.decrypt_xtea_ecb.argtypes = [
            LibGLib2.guint8 * 8,
            LibGLib2.guint8 * 8,
            LibGLib2.guint32 * 4,
            LibGLib2.guint]

        # void decrypt_xtea_le_ecb(guint8 plaintext[8], const guint8
        # ciphertext[8], const guint32 key[4], guint num_rounds);
        self.decrypt_xtea_le_ecb = libwsutil.decrypt_xtea_le_ecb
        self.decrypt_xtea_le_ecb.restype = None
        self.decrypt_xtea_le_ecb.argtypes = [
            LibGLib2.guint8 * 8,
            LibGLib2.guint8 * 8,
            LibGLib2.guint32 * 4,
            LibGLib2.guint]
