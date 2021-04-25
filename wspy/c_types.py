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
import os
from wspy.glib import *
from wspy.errors import *

# #define WS_INET_ADDRSTRLEN      16
WS_INET_ADDRSTRLEN = 16

# #define WS_INET6_ADDRSTRLEN     46
WS_INET6_ADDRSTRLEN = 46

# typedef struct Buffer {
# 	guint8	*data;
# 	gsize	allocated;
# 	gsize	start;
# 	gsize	first_free;
# } Buffer;
class Buffer(Structure):
    _fields_ = [('data', POINTER(guint8)),
                ('allocated', gsize),
                ('start', gsize),
                ('first_free', gsize)]

# typedef struct {
# 	time_t	secs;
# 	int	nsecs;
# } nstime_t;
class nstime_t(Structure):
    _fields_ = [('secs', c_long),
                ('nsecs', c_int)]

# #define NSTIME_INIT_ZERO {0, 0}
NSTIME_INIT_ZERO = nstime_t(0, 0)

# #define NSTIME_INIT_UNSET {0, G_MAXINT}
NSTIME_INIT_UNSET = nstime_t(0, 0x7FFFFFFF)

# #define NSTIME_INIT_MAX	{sizeof(time_t) > sizeof(int) ? LONG_MAX : INT_MAX, INT_MAX}
if os.name == 'nt':
    NSTIME_INIT_MAX = nstime_t(0x7FFFFFFF, 0x7FFFFFFF)
else:
    NSTIME_INIT_MAX = nstime_t(0x7FFFFFFFFFFFFFFF, 0x7FFFFFFF)

# #define WTAP_ENCAP_PER_PACKET                   -1
WTAP_ENCAP_PER_PACKET = -1

# #define WTAP_ENCAP_UNKNOWN                        0
WTAP_ENCAP_UNKNOWN = 0

# #define WTAP_ENCAP_ETHERNET                       1
WTAP_ENCAP_ETHERNET = 1

# #define WTAP_ENCAP_TOKEN_RING                     2
WTAP_ENCAP_TOKEN_RING = 2

# #define WTAP_ENCAP_SLIP                           3
WTAP_ENCAP_SLIP = 3

# #define WTAP_ENCAP_PPP                            4
WTAP_ENCAP_PPP = 4

# #define WTAP_ENCAP_FDDI                           5
WTAP_ENCAP_FDDI = 5

# #define WTAP_ENCAP_FDDI_BITSWAPPED                6
WTAP_ENCAP_FDDI_BITSWAPPED = 6

# #define WTAP_ENCAP_RAW_IP                         7
WTAP_ENCAP_RAW_IP = 7

# #define WTAP_ENCAP_ARCNET                         8
WTAP_ENCAP_ARCNET = 8

# #define WTAP_ENCAP_ARCNET_LINUX                   9
WTAP_ENCAP_ARCNET_LINUX = 9

# #define WTAP_ENCAP_ATM_RFC1483                   10
WTAP_ENCAP_ATM_RFC1483 = 10

# #define WTAP_ENCAP_LINUX_ATM_CLIP                11
WTAP_ENCAP_LINUX_ATM_CLIP = 11

# #define WTAP_ENCAP_LAPB                          12
WTAP_ENCAP_LAPB = 12

# #define WTAP_ENCAP_ATM_PDUS                      13
WTAP_ENCAP_ATM_PDUS = 13

# #define WTAP_ENCAP_ATM_PDUS_UNTRUNCATED          14
WTAP_ENCAP_ATM_PDUS_UNTRUNCATED = 14

# #define WTAP_ENCAP_NULL                          15
WTAP_ENCAP_NULL = 15

# #define WTAP_ENCAP_ASCEND                        16
WTAP_ENCAP_ASCEND = 16

# #define WTAP_ENCAP_ISDN                          17
WTAP_ENCAP_ISDN = 17

# #define WTAP_ENCAP_IP_OVER_FC                    18
WTAP_ENCAP_IP_OVER_FC = 18

# #define WTAP_ENCAP_PPP_WITH_PHDR                 19
WTAP_ENCAP_PPP_WITH_PHDR = 19

# #define WTAP_ENCAP_IEEE_802_11                   20
WTAP_ENCAP_IEEE_802_11 = 20

# #define WTAP_ENCAP_IEEE_802_11_PRISM             21
WTAP_ENCAP_IEEE_802_11_PRISM = 21

# #define WTAP_ENCAP_IEEE_802_11_WITH_RADIO        22
WTAP_ENCAP_IEEE_802_11_WITH_RADIO = 22

# #define WTAP_ENCAP_IEEE_802_11_RADIOTAP          23
WTAP_ENCAP_IEEE_802_11_RADIOTAP = 23

# #define WTAP_ENCAP_IEEE_802_11_AVS               24
WTAP_ENCAP_IEEE_802_11_AVS = 24

# #define WTAP_ENCAP_SLL                           25
WTAP_ENCAP_SLL = 25

# #define WTAP_ENCAP_FRELAY                        26
WTAP_ENCAP_FRELAY = 26

# #define WTAP_ENCAP_FRELAY_WITH_PHDR              27
WTAP_ENCAP_FRELAY_WITH_PHDR = 27

# #define WTAP_ENCAP_CHDLC                         28
WTAP_ENCAP_CHDLC = 28

# #define WTAP_ENCAP_CISCO_IOS                     29
WTAP_ENCAP_CISCO_IOS = 29

# #define WTAP_ENCAP_LOCALTALK                     30
WTAP_ENCAP_LOCALTALK = 30

# #define WTAP_ENCAP_OLD_PFLOG                     31
WTAP_ENCAP_OLD_PFLOG = 31

# #define WTAP_ENCAP_HHDLC                         32
WTAP_ENCAP_HHDLC = 32

# #define WTAP_ENCAP_DOCSIS                        33
WTAP_ENCAP_DOCSIS = 33

# #define WTAP_ENCAP_COSINE                        34
WTAP_ENCAP_COSINE = 34

# #define WTAP_ENCAP_WFLEET_HDLC                   35
WTAP_ENCAP_WFLEET_HDLC = 35

# #define WTAP_ENCAP_SDLC                          36
WTAP_ENCAP_SDLC = 36

# #define WTAP_ENCAP_TZSP                          37
WTAP_ENCAP_TZSP = 37

# #define WTAP_ENCAP_ENC                           38
WTAP_ENCAP_ENC = 38

# #define WTAP_ENCAP_PFLOG                         39
WTAP_ENCAP_PFLOG = 39

# #define WTAP_ENCAP_CHDLC_WITH_PHDR               40
WTAP_ENCAP_CHDLC_WITH_PHDR = 40

# #define WTAP_ENCAP_BLUETOOTH_H4                  41
WTAP_ENCAP_BLUETOOTH_H4 = 41

# #define WTAP_ENCAP_MTP2                          42
WTAP_ENCAP_MTP2 = 42

# #define WTAP_ENCAP_MTP3                          43
WTAP_ENCAP_MTP3 = 43

# #define WTAP_ENCAP_IRDA                          44
WTAP_ENCAP_IRDA = 44

# #define WTAP_ENCAP_USER0                         45
WTAP_ENCAP_USER0 = 45

# #define WTAP_ENCAP_USER1                         46
WTAP_ENCAP_USER1 = 46

# #define WTAP_ENCAP_USER2                         47
WTAP_ENCAP_USER2 = 47

# #define WTAP_ENCAP_USER3                         48
WTAP_ENCAP_USER3 = 48

# #define WTAP_ENCAP_USER4                         49
WTAP_ENCAP_USER4 = 49

# #define WTAP_ENCAP_USER5                         50
WTAP_ENCAP_USER5 = 50

# #define WTAP_ENCAP_USER6                         51
WTAP_ENCAP_USER6 = 51

# #define WTAP_ENCAP_USER7                         52
WTAP_ENCAP_USER7 = 52

# #define WTAP_ENCAP_USER8                         53
WTAP_ENCAP_USER8 = 53

# #define WTAP_ENCAP_USER9                         54
WTAP_ENCAP_USER9 = 54

# #define WTAP_ENCAP_USER10                        55
WTAP_ENCAP_USER10 = 55

# #define WTAP_ENCAP_USER11                        56
WTAP_ENCAP_USER11 = 56

# #define WTAP_ENCAP_USER12                        57
WTAP_ENCAP_USER12 = 57

# #define WTAP_ENCAP_USER13                        58
WTAP_ENCAP_USER13 = 58

# #define WTAP_ENCAP_USER14                        59
WTAP_ENCAP_USER14 = 59

# #define WTAP_ENCAP_USER15                        60
WTAP_ENCAP_USER15 = 60

# #define WTAP_ENCAP_SYMANTEC                      61
WTAP_ENCAP_SYMANTEC = 61

# #define WTAP_ENCAP_APPLE_IP_OVER_IEEE1394        62
WTAP_ENCAP_APPLE_IP_OVER_IEEE1394 = 62

# #define WTAP_ENCAP_BACNET_MS_TP                  63
WTAP_ENCAP_BACNET_MS_TP = 63

# #define WTAP_ENCAP_NETTL_RAW_ICMP                64
WTAP_ENCAP_NETTL_RAW_ICMP = 64

# #define WTAP_ENCAP_NETTL_RAW_ICMPV6              65
WTAP_ENCAP_NETTL_RAW_ICMPV6 = 65

# #define WTAP_ENCAP_GPRS_LLC                      66
WTAP_ENCAP_GPRS_LLC = 66

# #define WTAP_ENCAP_JUNIPER_ATM1                  67
WTAP_ENCAP_JUNIPER_ATM1 = 67

# #define WTAP_ENCAP_JUNIPER_ATM2                  68
WTAP_ENCAP_JUNIPER_ATM2 = 68

# #define WTAP_ENCAP_REDBACK                       69
WTAP_ENCAP_REDBACK = 69

# #define WTAP_ENCAP_NETTL_RAW_IP                  70
WTAP_ENCAP_NETTL_RAW_IP = 70

# #define WTAP_ENCAP_NETTL_ETHERNET                71
WTAP_ENCAP_NETTL_ETHERNET = 71

# #define WTAP_ENCAP_NETTL_TOKEN_RING              72
WTAP_ENCAP_NETTL_TOKEN_RING = 72

# #define WTAP_ENCAP_NETTL_FDDI                    73
WTAP_ENCAP_NETTL_FDDI = 73

# #define WTAP_ENCAP_NETTL_UNKNOWN                 74
WTAP_ENCAP_NETTL_UNKNOWN = 74

# #define WTAP_ENCAP_MTP2_WITH_PHDR                75
WTAP_ENCAP_MTP2_WITH_PHDR = 75

# #define WTAP_ENCAP_JUNIPER_PPPOE                 76
WTAP_ENCAP_JUNIPER_PPPOE = 76

# #define WTAP_ENCAP_GCOM_TIE1                     77
WTAP_ENCAP_GCOM_TIE1 = 77

# #define WTAP_ENCAP_GCOM_SERIAL                   78
WTAP_ENCAP_GCOM_SERIAL = 78

# #define WTAP_ENCAP_NETTL_X25                     79
WTAP_ENCAP_NETTL_X25 = 79

# #define WTAP_ENCAP_K12                           80
WTAP_ENCAP_K12 = 80

# #define WTAP_ENCAP_JUNIPER_MLPPP                 81
WTAP_ENCAP_JUNIPER_MLPPP = 81

# #define WTAP_ENCAP_JUNIPER_MLFR                  82
WTAP_ENCAP_JUNIPER_MLFR = 82

# #define WTAP_ENCAP_JUNIPER_ETHER                 83
WTAP_ENCAP_JUNIPER_ETHER = 83

# #define WTAP_ENCAP_JUNIPER_PPP                   84
WTAP_ENCAP_JUNIPER_PPP = 84

# #define WTAP_ENCAP_JUNIPER_FRELAY                85
WTAP_ENCAP_JUNIPER_FRELAY = 85

# #define WTAP_ENCAP_JUNIPER_CHDLC                 86
WTAP_ENCAP_JUNIPER_CHDLC = 86

# #define WTAP_ENCAP_JUNIPER_GGSN                  87
WTAP_ENCAP_JUNIPER_GGSN = 87

# #define WTAP_ENCAP_LINUX_LAPD                    88
WTAP_ENCAP_LINUX_LAPD = 88

# #define WTAP_ENCAP_CATAPULT_DCT2000              89
WTAP_ENCAP_CATAPULT_DCT2000 = 89

# #define WTAP_ENCAP_BER                           90
WTAP_ENCAP_BER = 90

# #define WTAP_ENCAP_JUNIPER_VP                    91
WTAP_ENCAP_JUNIPER_VP = 91

# #define WTAP_ENCAP_USB_FREEBSD                   92
WTAP_ENCAP_USB_FREEBSD = 92

# #define WTAP_ENCAP_IEEE802_16_MAC_CPS            93
WTAP_ENCAP_IEEE802_16_MAC_CPS = 93

# #define WTAP_ENCAP_NETTL_RAW_TELNET              94
WTAP_ENCAP_NETTL_RAW_TELNET = 94

# #define WTAP_ENCAP_USB_LINUX                     95
WTAP_ENCAP_USB_LINUX = 95

# #define WTAP_ENCAP_MPEG                          96
WTAP_ENCAP_MPEG = 96

# #define WTAP_ENCAP_PPI                           97
WTAP_ENCAP_PPI = 97

# #define WTAP_ENCAP_ERF                           98
WTAP_ENCAP_ERF = 98

# #define WTAP_ENCAP_BLUETOOTH_H4_WITH_PHDR        99
WTAP_ENCAP_BLUETOOTH_H4_WITH_PHDR = 99

# #define WTAP_ENCAP_SITA                         100
WTAP_ENCAP_SITA = 100

# #define WTAP_ENCAP_SCCP                         101
WTAP_ENCAP_SCCP = 101

# #define WTAP_ENCAP_BLUETOOTH_HCI                102
WTAP_ENCAP_BLUETOOTH_HCI = 102

# #define WTAP_ENCAP_IPMB_KONTRON                 103
WTAP_ENCAP_IPMB_KONTRON = 103

# #define WTAP_ENCAP_IEEE802_15_4                 104
WTAP_ENCAP_IEEE802_15_4 = 104

# #define WTAP_ENCAP_X2E_XORAYA                   105
WTAP_ENCAP_X2E_XORAYA = 105

# #define WTAP_ENCAP_FLEXRAY                      106
WTAP_ENCAP_FLEXRAY = 106

# #define WTAP_ENCAP_LIN                          107
WTAP_ENCAP_LIN = 107

# #define WTAP_ENCAP_MOST                         108
WTAP_ENCAP_MOST = 108

# #define WTAP_ENCAP_CAN20B                       109
WTAP_ENCAP_CAN20B = 109

# #define WTAP_ENCAP_LAYER1_EVENT                 110
WTAP_ENCAP_LAYER1_EVENT = 110

# #define WTAP_ENCAP_X2E_SERIAL                   111
WTAP_ENCAP_X2E_SERIAL = 111

# #define WTAP_ENCAP_I2C_LINUX                    112
WTAP_ENCAP_I2C_LINUX = 112

# #define WTAP_ENCAP_IEEE802_15_4_NONASK_PHY      113
WTAP_ENCAP_IEEE802_15_4_NONASK_PHY = 113

# #define WTAP_ENCAP_TNEF                         114
WTAP_ENCAP_TNEF = 114

# #define WTAP_ENCAP_USB_LINUX_MMAPPED            115
WTAP_ENCAP_USB_LINUX_MMAPPED = 115

# #define WTAP_ENCAP_GSM_UM                       116
WTAP_ENCAP_GSM_UM = 116

# #define WTAP_ENCAP_DPNSS                        117
WTAP_ENCAP_DPNSS = 117

# #define WTAP_ENCAP_PACKETLOGGER                 118
WTAP_ENCAP_PACKETLOGGER = 118

# #define WTAP_ENCAP_NSTRACE_1_0                  119
WTAP_ENCAP_NSTRACE_1_0 = 119

# #define WTAP_ENCAP_NSTRACE_2_0                  120
WTAP_ENCAP_NSTRACE_2_0 = 120

# #define WTAP_ENCAP_FIBRE_CHANNEL_FC2            121
WTAP_ENCAP_FIBRE_CHANNEL_FC2 = 121

# #define WTAP_ENCAP_FIBRE_CHANNEL_FC2_WITH_FRAME_DELIMS 122
WTAP_ENCAP_FIBRE_CHANNEL_FC2_WITH_FRAME_DELIMS = 122

# #define WTAP_ENCAP_JPEG_JFIF                    123
WTAP_ENCAP_JPEG_JFIF = 123

# #define WTAP_ENCAP_IPNET                        124
WTAP_ENCAP_IPNET = 124

# #define WTAP_ENCAP_SOCKETCAN                    125
WTAP_ENCAP_SOCKETCAN = 125

# #define WTAP_ENCAP_IEEE_802_11_NETMON           126
WTAP_ENCAP_IEEE_802_11_NETMON = 126

# #define WTAP_ENCAP_IEEE802_15_4_NOFCS           127
WTAP_ENCAP_IEEE802_15_4_NOFCS = 127

# #define WTAP_ENCAP_RAW_IPFIX                    128
WTAP_ENCAP_RAW_IPFIX = 128

# #define WTAP_ENCAP_RAW_IP4                      129
WTAP_ENCAP_RAW_IP4 = 129

# #define WTAP_ENCAP_RAW_IP6                      130
WTAP_ENCAP_RAW_IP6 = 130

# #define WTAP_ENCAP_LAPD                         131
WTAP_ENCAP_LAPD = 131

# #define WTAP_ENCAP_DVBCI                        132
WTAP_ENCAP_DVBCI = 132

# #define WTAP_ENCAP_MUX27010                     133
WTAP_ENCAP_MUX27010 = 133

# #define WTAP_ENCAP_MIME                         134
WTAP_ENCAP_MIME = 134

# #define WTAP_ENCAP_NETANALYZER                  135
WTAP_ENCAP_NETANALYZER = 135

# #define WTAP_ENCAP_NETANALYZER_TRANSPARENT      136
WTAP_ENCAP_NETANALYZER_TRANSPARENT = 136

# #define WTAP_ENCAP_IP_OVER_IB_SNOOP             137
WTAP_ENCAP_IP_OVER_IB_SNOOP = 137

# #define WTAP_ENCAP_MPEG_2_TS                    138
WTAP_ENCAP_MPEG_2_TS = 138

# #define WTAP_ENCAP_PPP_ETHER                    139
WTAP_ENCAP_PPP_ETHER = 139

# #define WTAP_ENCAP_NFC_LLCP                     140
WTAP_ENCAP_NFC_LLCP = 140

# #define WTAP_ENCAP_NFLOG                        141
WTAP_ENCAP_NFLOG = 141

# #define WTAP_ENCAP_V5_EF                        142
WTAP_ENCAP_V5_EF = 142

# #define WTAP_ENCAP_BACNET_MS_TP_WITH_PHDR       143
WTAP_ENCAP_BACNET_MS_TP_WITH_PHDR = 143

# #define WTAP_ENCAP_IXVERIWAVE                   144
WTAP_ENCAP_IXVERIWAVE = 144

# #define WTAP_ENCAP_SDH                          145
WTAP_ENCAP_SDH = 145

# #define WTAP_ENCAP_DBUS                         146
WTAP_ENCAP_DBUS = 146

# #define WTAP_ENCAP_AX25_KISS                    147
WTAP_ENCAP_AX25_KISS = 147

# #define WTAP_ENCAP_AX25                         148
WTAP_ENCAP_AX25 = 148

# #define WTAP_ENCAP_SCTP                         149
WTAP_ENCAP_SCTP = 149

# #define WTAP_ENCAP_INFINIBAND                   150
WTAP_ENCAP_INFINIBAND = 150

# #define WTAP_ENCAP_JUNIPER_SVCS                 151
WTAP_ENCAP_JUNIPER_SVCS = 151

# #define WTAP_ENCAP_USBPCAP                      152
WTAP_ENCAP_USBPCAP = 152

# #define WTAP_ENCAP_RTAC_SERIAL                  153
WTAP_ENCAP_RTAC_SERIAL = 153

# #define WTAP_ENCAP_BLUETOOTH_LE_LL              154
WTAP_ENCAP_BLUETOOTH_LE_LL = 154

# #define WTAP_ENCAP_WIRESHARK_UPPER_PDU          155
WTAP_ENCAP_WIRESHARK_UPPER_PDU = 155

# #define WTAP_ENCAP_STANAG_4607                  156
WTAP_ENCAP_STANAG_4607 = 156

# #define WTAP_ENCAP_STANAG_5066_D_PDU            157
WTAP_ENCAP_STANAG_5066_D_PDU = 157

# #define WTAP_ENCAP_NETLINK                      158
WTAP_ENCAP_NETLINK = 158

# #define WTAP_ENCAP_BLUETOOTH_LINUX_MONITOR      159
WTAP_ENCAP_BLUETOOTH_LINUX_MONITOR = 159

# #define WTAP_ENCAP_BLUETOOTH_BREDR_BB           160
WTAP_ENCAP_BLUETOOTH_BREDR_BB = 160

# #define WTAP_ENCAP_BLUETOOTH_LE_LL_WITH_PHDR    161
WTAP_ENCAP_BLUETOOTH_LE_LL_WITH_PHDR = 161

# #define WTAP_ENCAP_NSTRACE_3_0                  162
WTAP_ENCAP_NSTRACE_3_0 = 162

# #define WTAP_ENCAP_LOGCAT                       163
WTAP_ENCAP_LOGCAT = 163

# #define WTAP_ENCAP_LOGCAT_BRIEF                 164
WTAP_ENCAP_LOGCAT_BRIEF = 164

# #define WTAP_ENCAP_LOGCAT_PROCESS               165
WTAP_ENCAP_LOGCAT_PROCESS = 165

# #define WTAP_ENCAP_LOGCAT_TAG                   166
WTAP_ENCAP_LOGCAT_TAG = 166

# #define WTAP_ENCAP_LOGCAT_THREAD                167
WTAP_ENCAP_LOGCAT_THREAD = 167

# #define WTAP_ENCAP_LOGCAT_TIME                  168
WTAP_ENCAP_LOGCAT_TIME = 168

# #define WTAP_ENCAP_LOGCAT_THREADTIME            169
WTAP_ENCAP_LOGCAT_THREADTIME = 169

# #define WTAP_ENCAP_LOGCAT_LONG                  170
WTAP_ENCAP_LOGCAT_LONG = 170

# #define WTAP_ENCAP_PKTAP                        171
WTAP_ENCAP_PKTAP = 171

# #define WTAP_ENCAP_EPON                         172
WTAP_ENCAP_EPON = 172

# #define WTAP_ENCAP_IPMI_TRACE                   173
WTAP_ENCAP_IPMI_TRACE = 173

# #define WTAP_ENCAP_LOOP                         174
WTAP_ENCAP_LOOP = 174

# #define WTAP_ENCAP_JSON                         175
WTAP_ENCAP_JSON = 175

# #define WTAP_ENCAP_NSTRACE_3_5                  176
WTAP_ENCAP_NSTRACE_3_5 = 176

# #define WTAP_ENCAP_ISO14443                     177
WTAP_ENCAP_ISO14443 = 177

# #define WTAP_ENCAP_GFP_T                        178
WTAP_ENCAP_GFP_T = 178

# #define WTAP_ENCAP_GFP_F                        179
WTAP_ENCAP_GFP_F = 179

# #define WTAP_ENCAP_IP_OVER_IB_PCAP              180
WTAP_ENCAP_IP_OVER_IB_PCAP = 180

# #define WTAP_ENCAP_JUNIPER_VN                   181
WTAP_ENCAP_JUNIPER_VN = 181

# #define WTAP_ENCAP_USB_DARWIN                   182
WTAP_ENCAP_USB_DARWIN = 182

# #define WTAP_ENCAP_LORATAP                      183
WTAP_ENCAP_LORATAP = 183

# #define WTAP_ENCAP_3MB_ETHERNET                 184
WTAP_ENCAP_3MB_ETHERNET = 184

# #define WTAP_ENCAP_VSOCK                        185
WTAP_ENCAP_VSOCK = 185

# #define WTAP_ENCAP_NORDIC_BLE                   186
WTAP_ENCAP_NORDIC_BLE = 186

# #define WTAP_ENCAP_NETMON_NET_NETEVENT          187
WTAP_ENCAP_NETMON_NET_NETEVENT = 187

# #define WTAP_ENCAP_NETMON_HEADER                188
WTAP_ENCAP_NETMON_HEADER = 188

# #define WTAP_ENCAP_NETMON_NET_FILTER            189
WTAP_ENCAP_NETMON_NET_FILTER = 189

# #define WTAP_ENCAP_NETMON_NETWORK_INFO_EX       190
WTAP_ENCAP_NETMON_NETWORK_INFO_EX = 190

# #define WTAP_ENCAP_MA_WFP_CAPTURE_V4            191
WTAP_ENCAP_MA_WFP_CAPTURE_V4 = 191

# #define WTAP_ENCAP_MA_WFP_CAPTURE_V6            192
WTAP_ENCAP_MA_WFP_CAPTURE_V6 = 192

# #define WTAP_ENCAP_MA_WFP_CAPTURE_2V4           193
WTAP_ENCAP_MA_WFP_CAPTURE_2V4 = 193

# #define WTAP_ENCAP_MA_WFP_CAPTURE_2V6           194
WTAP_ENCAP_MA_WFP_CAPTURE_2V6 = 194

# #define WTAP_ENCAP_MA_WFP_CAPTURE_AUTH_V4       195
WTAP_ENCAP_MA_WFP_CAPTURE_AUTH_V4 = 195

# #define WTAP_ENCAP_MA_WFP_CAPTURE_AUTH_V6       196
WTAP_ENCAP_MA_WFP_CAPTURE_AUTH_V6 = 196

# #define WTAP_ENCAP_JUNIPER_ST                   197
WTAP_ENCAP_JUNIPER_ST = 197

# #define WTAP_ENCAP_ETHERNET_MPACKET             198
WTAP_ENCAP_ETHERNET_MPACKET = 198

# #define WTAP_ENCAP_DOCSIS31_XRA31               199
WTAP_ENCAP_DOCSIS31_XRA31 = 199

# #define WTAP_ENCAP_DPAUXMON                     200
WTAP_ENCAP_DPAUXMON = 200

# #define WTAP_ENCAP_RUBY_MARSHAL                 201
WTAP_ENCAP_RUBY_MARSHAL = 201

# #define WTAP_ENCAP_RFC7468                      202
WTAP_ENCAP_RFC7468 = 202

# #define WTAP_ENCAP_SYSTEMD_JOURNAL              203
WTAP_ENCAP_SYSTEMD_JOURNAL = 203

# #define WTAP_ENCAP_EBHSCR                       204
WTAP_ENCAP_EBHSCR = 204

# #define WTAP_ENCAP_VPP                          205
WTAP_ENCAP_VPP = 205

# #define WTAP_ENCAP_IEEE802_15_4_TAP             206
WTAP_ENCAP_IEEE802_15_4_TAP = 206

# #define WTAP_ENCAP_LOG_3GPP                     207
WTAP_ENCAP_LOG_3GPP = 207

# #define WTAP_ENCAP_USB_2_0                      208
WTAP_ENCAP_USB_2_0 = 208

# #define WTAP_ENCAP_MP4                          209
WTAP_ENCAP_MP4 = 209

# #define WTAP_ENCAP_SLL2                         210
WTAP_ENCAP_SLL2 = 210

# #define WTAP_ENCAP_ZWAVE_SERIAL                 211
WTAP_ENCAP_ZWAVE_SERIAL = 211

# #define WTAP_FILE_TYPE_SUBTYPE_UNKNOWN                        0
WTAP_FILE_TYPE_SUBTYPE_UNKNOWN = 0

# #define WTAP_FILE_TYPE_SUBTYPE_PCAP                           1
WTAP_FILE_TYPE_SUBTYPE_PCAP = 1

# #define WTAP_FILE_TYPE_SUBTYPE_PCAPNG                         2
WTAP_FILE_TYPE_SUBTYPE_PCAPNG = 2

# #define WTAP_FILE_TYPE_SUBTYPE_PCAP_NSEC                      3
WTAP_FILE_TYPE_SUBTYPE_PCAP_NSEC = 3

# #define WTAP_FILE_TYPE_SUBTYPE_PCAP_AIX                       4
WTAP_FILE_TYPE_SUBTYPE_PCAP_AIX = 4

# #define WTAP_FILE_TYPE_SUBTYPE_PCAP_SS991029                  5
WTAP_FILE_TYPE_SUBTYPE_PCAP_SS991029 = 5

# #define WTAP_FILE_TYPE_SUBTYPE_PCAP_NOKIA                     6
WTAP_FILE_TYPE_SUBTYPE_PCAP_NOKIA = 6

# #define WTAP_FILE_TYPE_SUBTYPE_PCAP_SS990417                  7
WTAP_FILE_TYPE_SUBTYPE_PCAP_SS990417 = 7

# #define WTAP_FILE_TYPE_SUBTYPE_PCAP_SS990915                  8
WTAP_FILE_TYPE_SUBTYPE_PCAP_SS990915 = 8

# #define WTAP_FILE_TYPE_SUBTYPE_5VIEWS                         9
WTAP_FILE_TYPE_SUBTYPE_5VIEWS = 9

# #define WTAP_FILE_TYPE_SUBTYPE_IPTRACE_1_0                   10
WTAP_FILE_TYPE_SUBTYPE_IPTRACE_1_0 = 10

# #define WTAP_FILE_TYPE_SUBTYPE_IPTRACE_2_0                   11
WTAP_FILE_TYPE_SUBTYPE_IPTRACE_2_0 = 11

# #define WTAP_FILE_TYPE_SUBTYPE_BER                           12
WTAP_FILE_TYPE_SUBTYPE_BER = 12

# #define WTAP_FILE_TYPE_SUBTYPE_HCIDUMP                       13
WTAP_FILE_TYPE_SUBTYPE_HCIDUMP = 13

# #define WTAP_FILE_TYPE_SUBTYPE_CATAPULT_DCT2000              14
WTAP_FILE_TYPE_SUBTYPE_CATAPULT_DCT2000 = 14

# #define WTAP_FILE_TYPE_SUBTYPE_NETXRAY_OLD                   15
WTAP_FILE_TYPE_SUBTYPE_NETXRAY_OLD = 15

# #define WTAP_FILE_TYPE_SUBTYPE_NETXRAY_1_0                   16
WTAP_FILE_TYPE_SUBTYPE_NETXRAY_1_0 = 16

# #define WTAP_FILE_TYPE_SUBTYPE_COSINE                        17
WTAP_FILE_TYPE_SUBTYPE_COSINE = 17

# #define WTAP_FILE_TYPE_SUBTYPE_CSIDS                         18
WTAP_FILE_TYPE_SUBTYPE_CSIDS = 18

# #define WTAP_FILE_TYPE_SUBTYPE_DBS_ETHERWATCH                19
WTAP_FILE_TYPE_SUBTYPE_DBS_ETHERWATCH = 19

# #define WTAP_FILE_TYPE_SUBTYPE_ERF                           20
WTAP_FILE_TYPE_SUBTYPE_ERF = 20

# #define WTAP_FILE_TYPE_SUBTYPE_EYESDN                        21
WTAP_FILE_TYPE_SUBTYPE_EYESDN = 21

# #define WTAP_FILE_TYPE_SUBTYPE_NETTL                         22
WTAP_FILE_TYPE_SUBTYPE_NETTL = 22

# #define WTAP_FILE_TYPE_SUBTYPE_ISERIES                       23
WTAP_FILE_TYPE_SUBTYPE_ISERIES = 23

# #define WTAP_FILE_TYPE_SUBTYPE_ISERIES_UNICODE               24
WTAP_FILE_TYPE_SUBTYPE_ISERIES_UNICODE = 24

# #define WTAP_FILE_TYPE_SUBTYPE_I4BTRACE                      25
WTAP_FILE_TYPE_SUBTYPE_I4BTRACE = 25

# #define WTAP_FILE_TYPE_SUBTYPE_ASCEND                        26
WTAP_FILE_TYPE_SUBTYPE_ASCEND = 26

# #define WTAP_FILE_TYPE_SUBTYPE_NETMON_1_x                    27
WTAP_FILE_TYPE_SUBTYPE_NETMON_1_x = 27

# #define WTAP_FILE_TYPE_SUBTYPE_NETMON_2_x                    28
WTAP_FILE_TYPE_SUBTYPE_NETMON_2_x = 28

# #define WTAP_FILE_TYPE_SUBTYPE_NGSNIFFER_UNCOMPRESSED        29
WTAP_FILE_TYPE_SUBTYPE_NGSNIFFER_UNCOMPRESSED = 29

# #define WTAP_FILE_TYPE_SUBTYPE_NGSNIFFER_COMPRESSED          30
WTAP_FILE_TYPE_SUBTYPE_NGSNIFFER_COMPRESSED = 30

# #define WTAP_FILE_TYPE_SUBTYPE_NETXRAY_1_1                   31
WTAP_FILE_TYPE_SUBTYPE_NETXRAY_1_1 = 31

# #define WTAP_FILE_TYPE_SUBTYPE_NETXRAY_2_00x                 32
WTAP_FILE_TYPE_SUBTYPE_NETXRAY_2_00x = 32

# #define WTAP_FILE_TYPE_SUBTYPE_NETWORK_INSTRUMENTS           33
WTAP_FILE_TYPE_SUBTYPE_NETWORK_INSTRUMENTS = 33

# #define WTAP_FILE_TYPE_SUBTYPE_LANALYZER                     34
WTAP_FILE_TYPE_SUBTYPE_LANALYZER = 34

# #define WTAP_FILE_TYPE_SUBTYPE_PPPDUMP                       35
WTAP_FILE_TYPE_SUBTYPE_PPPDUMP = 35

# #define WTAP_FILE_TYPE_SUBTYPE_RADCOM                        36
WTAP_FILE_TYPE_SUBTYPE_RADCOM = 36

# #define WTAP_FILE_TYPE_SUBTYPE_SNOOP                         37
WTAP_FILE_TYPE_SUBTYPE_SNOOP = 37

# #define WTAP_FILE_TYPE_SUBTYPE_SHOMITI                       38
WTAP_FILE_TYPE_SUBTYPE_SHOMITI = 38

# #define WTAP_FILE_TYPE_SUBTYPE_VMS                           39
WTAP_FILE_TYPE_SUBTYPE_VMS = 39

# #define WTAP_FILE_TYPE_SUBTYPE_K12                           40
WTAP_FILE_TYPE_SUBTYPE_K12 = 40

# #define WTAP_FILE_TYPE_SUBTYPE_TOSHIBA                       41
WTAP_FILE_TYPE_SUBTYPE_TOSHIBA = 41

# #define WTAP_FILE_TYPE_SUBTYPE_VISUAL_NETWORKS               42
WTAP_FILE_TYPE_SUBTYPE_VISUAL_NETWORKS = 42

# #define WTAP_FILE_TYPE_SUBTYPE_PEEKCLASSIC_V56               43
WTAP_FILE_TYPE_SUBTYPE_PEEKCLASSIC_V56 = 43

# #define WTAP_FILE_TYPE_SUBTYPE_PEEKCLASSIC_V7                44
WTAP_FILE_TYPE_SUBTYPE_PEEKCLASSIC_V7 = 44

# #define WTAP_FILE_TYPE_SUBTYPE_PEEKTAGGED                    45
WTAP_FILE_TYPE_SUBTYPE_PEEKTAGGED = 45

# #define WTAP_FILE_TYPE_SUBTYPE_MPEG                          46
WTAP_FILE_TYPE_SUBTYPE_MPEG = 46

# #define WTAP_FILE_TYPE_SUBTYPE_K12TEXT                       47
WTAP_FILE_TYPE_SUBTYPE_K12TEXT = 47

# #define WTAP_FILE_TYPE_SUBTYPE_NETSCREEN                     48
WTAP_FILE_TYPE_SUBTYPE_NETSCREEN = 48

# #define WTAP_FILE_TYPE_SUBTYPE_COMMVIEW                      49
WTAP_FILE_TYPE_SUBTYPE_COMMVIEW = 49

# #define WTAP_FILE_TYPE_SUBTYPE_BTSNOOP                       50
WTAP_FILE_TYPE_SUBTYPE_BTSNOOP = 50

# #define WTAP_FILE_TYPE_SUBTYPE_TNEF                          51
WTAP_FILE_TYPE_SUBTYPE_TNEF = 51

# #define WTAP_FILE_TYPE_SUBTYPE_DCT3TRACE                     52
WTAP_FILE_TYPE_SUBTYPE_DCT3TRACE = 52

# #define WTAP_FILE_TYPE_SUBTYPE_PACKETLOGGER                  53
WTAP_FILE_TYPE_SUBTYPE_PACKETLOGGER = 53

# #define WTAP_FILE_TYPE_SUBTYPE_DAINTREE_SNA                  54
WTAP_FILE_TYPE_SUBTYPE_DAINTREE_SNA = 54

# #define WTAP_FILE_TYPE_SUBTYPE_NETSCALER_1_0                 55
WTAP_FILE_TYPE_SUBTYPE_NETSCALER_1_0 = 55

# #define WTAP_FILE_TYPE_SUBTYPE_NETSCALER_2_0                 56
WTAP_FILE_TYPE_SUBTYPE_NETSCALER_2_0 = 56

# #define WTAP_FILE_TYPE_SUBTYPE_JPEG_JFIF                     57
WTAP_FILE_TYPE_SUBTYPE_JPEG_JFIF = 57

# #define WTAP_FILE_TYPE_SUBTYPE_IPFIX                         58
WTAP_FILE_TYPE_SUBTYPE_IPFIX = 58

# #define WTAP_FILE_TYPE_SUBTYPE_MIME                          59
WTAP_FILE_TYPE_SUBTYPE_MIME = 59

# #define WTAP_FILE_TYPE_SUBTYPE_AETHRA                        60
WTAP_FILE_TYPE_SUBTYPE_AETHRA = 60

# #define WTAP_FILE_TYPE_SUBTYPE_MPEG_2_TS                     61
WTAP_FILE_TYPE_SUBTYPE_MPEG_2_TS = 61

# #define WTAP_FILE_TYPE_SUBTYPE_VWR_80211                     62
WTAP_FILE_TYPE_SUBTYPE_VWR_80211 = 62

# #define WTAP_FILE_TYPE_SUBTYPE_VWR_ETH                       63
WTAP_FILE_TYPE_SUBTYPE_VWR_ETH = 63

# #define WTAP_FILE_TYPE_SUBTYPE_CAMINS                        64
WTAP_FILE_TYPE_SUBTYPE_CAMINS = 64

# #define WTAP_FILE_TYPE_SUBTYPE_STANAG_4607                   65
WTAP_FILE_TYPE_SUBTYPE_STANAG_4607 = 65

# #define WTAP_FILE_TYPE_SUBTYPE_NETSCALER_3_0                 66
WTAP_FILE_TYPE_SUBTYPE_NETSCALER_3_0 = 66

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT                        67
WTAP_FILE_TYPE_SUBTYPE_LOGCAT = 67

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT_BRIEF                  68
WTAP_FILE_TYPE_SUBTYPE_LOGCAT_BRIEF = 68

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT_PROCESS                69
WTAP_FILE_TYPE_SUBTYPE_LOGCAT_PROCESS = 69

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT_TAG                    70
WTAP_FILE_TYPE_SUBTYPE_LOGCAT_TAG = 70

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT_THREAD                 71
WTAP_FILE_TYPE_SUBTYPE_LOGCAT_THREAD = 71

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT_TIME                   72
WTAP_FILE_TYPE_SUBTYPE_LOGCAT_TIME = 72

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT_THREADTIME             73
WTAP_FILE_TYPE_SUBTYPE_LOGCAT_THREADTIME = 73

# #define WTAP_FILE_TYPE_SUBTYPE_LOGCAT_LONG                   74
WTAP_FILE_TYPE_SUBTYPE_LOGCAT_LONG = 74

# #define WTAP_FILE_TYPE_SUBTYPE_COLASOFT_CAPSA                75
WTAP_FILE_TYPE_SUBTYPE_COLASOFT_CAPSA = 75

# #define WTAP_FILE_TYPE_SUBTYPE_COLASOFT_PACKET_BUILDER       76
WTAP_FILE_TYPE_SUBTYPE_COLASOFT_PACKET_BUILDER = 76

# #define WTAP_FILE_TYPE_SUBTYPE_JSON                          77
WTAP_FILE_TYPE_SUBTYPE_JSON = 77

# #define WTAP_FILE_TYPE_SUBTYPE_NETSCALER_3_5                 78
WTAP_FILE_TYPE_SUBTYPE_NETSCALER_3_5 = 78

# #define WTAP_FILE_TYPE_SUBTYPE_NETTRACE_3GPP_32_423          79
WTAP_FILE_TYPE_SUBTYPE_NETTRACE_3GPP_32_423 = 79

# #define WTAP_FILE_TYPE_SUBTYPE_MPLOG                         80
WTAP_FILE_TYPE_SUBTYPE_MPLOG = 80

# #define WTAP_FILE_TYPE_SUBTYPE_DPA400                        81
WTAP_FILE_TYPE_SUBTYPE_DPA400 = 81

# #define WTAP_FILE_TYPE_SUBTYPE_RFC7468                       82
WTAP_FILE_TYPE_SUBTYPE_RFC7468 = 82

# #define WTAP_FILE_TYPE_SUBTYPE_RUBY_MARSHAL                  83
WTAP_FILE_TYPE_SUBTYPE_RUBY_MARSHAL = 83

# #define WTAP_FILE_TYPE_SUBTYPE_SYSTEMD_JOURNAL               84
WTAP_FILE_TYPE_SUBTYPE_SYSTEMD_JOURNAL = 84

# #define WTAP_FILE_TYPE_SUBTYPE_LOG_3GPP                      85
WTAP_FILE_TYPE_SUBTYPE_LOG_3GPP = 85

# #define WTAP_FILE_TYPE_SUBTYPE_MP4                           86
WTAP_FILE_TYPE_SUBTYPE_MP4 = 86

# #define WTAP_TSPREC_UNKNOWN    -2
WTAP_TSPREC_UNKNOWN = -2

# #define WTAP_TSPREC_PER_PACKET -1
WTAP_TSPREC_PER_PACKET = -1

# #define WTAP_TSPREC_SEC         0
WTAP_TSPREC_SEC = 0

# #define WTAP_TSPREC_DSEC        1
WTAP_TSPREC_DSEC = 1

# #define WTAP_TSPREC_CSEC        2
WTAP_TSPREC_CSEC = 2

# #define WTAP_TSPREC_MSEC        3
WTAP_TSPREC_MSEC = 3

# #define WTAP_TSPREC_USEC        6
WTAP_TSPREC_USEC = 6

# #define WTAP_TSPREC_NSEC        9
WTAP_TSPREC_NSEC = 9

# #define WTAP_MAX_PACKET_SIZE_STANDARD    262144
WTAP_MAX_PACKET_SIZE_STANDARD = 262144

# #define WTAP_MAX_PACKET_SIZE_USBPCAP     (128*1024*1024)
WTAP_MAX_PACKET_SIZE_USBPCAP = (128*1024*1024)

# #define WTAP_MAX_PACKET_SIZE_EBHSCR      (8*1024*1024)
WTAP_MAX_PACKET_SIZE_EBHSCR = (8*1024*1024)

# #define WTAP_MAX_PACKET_SIZE_DBUS        (128*1024*1024)
WTAP_MAX_PACKET_SIZE_DBUS = (128*1024*1024)

# struct eth_phdr {
#     gint   fcs_len;
# };
class eth_phdr(Structure):
    _fields_ = [('fcs_len', gint)]

# struct dte_dce_phdr {
#     guint8  flags;
# };
class dte_dce_phdr(Structure):
    _fields_ = [('flags', guint8)]

# struct isdn_phdr {
#     gboolean uton;
#     guint8   channel;
# };
class isdn_phdr(Structure):
    _fields_ = [('uton', gboolean),
                ('channel', guint8)]

# #define ATM_RAW_CELL         0x01
ATM_RAW_CELL = 0x01

# #define ATM_NO_HEC           0x02
ATM_NO_HEC = 0x02

# #define ATM_AAL2_NOPHDR      0x04
ATM_AAL2_NOPHDR = 0x04

# #define ATM_REASSEMBLY_ERROR 0x08
ATM_REASSEMBLY_ERROR = 0x08

# #define AAL_UNKNOWN     0
AAL_UNKNOWN = 0

# #define AAL_1           1
AAL_1 = 1

# #define AAL_2           2
AAL_2 = 2

# #define AAL_3_4         3
AAL_3_4 = 3

# #define AAL_5           4
AAL_5 = 4

# #define AAL_USER        5
AAL_USER = 5

# #define AAL_SIGNALLING  6
AAL_SIGNALLING = 6

# #define AAL_OAMCELL     7
AAL_OAMCELL = 7

# #define TRAF_UNKNOWN    0
TRAF_UNKNOWN = 0

# #define TRAF_LLCMX      1
TRAF_LLCMX = 1

# #define TRAF_VCMX       2
TRAF_VCMX = 2

# #define TRAF_LANE       3
TRAF_LANE = 3

# #define TRAF_ILMI       4
TRAF_ILMI = 4

# #define TRAF_FR         5
TRAF_FR = 5

# #define TRAF_SPANS      6
TRAF_SPANS = 6

# #define TRAF_IPSILON    7
TRAF_IPSILON = 7

# #define TRAF_UMTS_FP    8
TRAF_UMTS_FP = 8

# #define TRAF_GPRS_NS    9
TRAF_GPRS_NS = 9

# #define TRAF_SSCOP     10
TRAF_SSCOP = 10

# #define TRAF_ST_UNKNOWN     0
TRAF_ST_UNKNOWN = 0

# #define TRAF_ST_VCMX_802_3_FCS   1
TRAF_ST_VCMX_802_3_FCS = 1

# #define TRAF_ST_VCMX_802_4_FCS   2
TRAF_ST_VCMX_802_4_FCS = 2

# #define TRAF_ST_VCMX_802_5_FCS   3
TRAF_ST_VCMX_802_5_FCS = 3

# #define TRAF_ST_VCMX_FDDI_FCS    4
TRAF_ST_VCMX_FDDI_FCS = 4

# #define TRAF_ST_VCMX_802_6_FCS   5
TRAF_ST_VCMX_802_6_FCS = 5

# #define TRAF_ST_VCMX_802_3       7
TRAF_ST_VCMX_802_3 = 7

# #define TRAF_ST_VCMX_802_4       8
TRAF_ST_VCMX_802_4 = 8

# #define TRAF_ST_VCMX_802_5       9
TRAF_ST_VCMX_802_5 = 9

# #define TRAF_ST_VCMX_FDDI       10
TRAF_ST_VCMX_FDDI = 10

# #define TRAF_ST_VCMX_802_6      11
TRAF_ST_VCMX_802_6 = 11

# #define TRAF_ST_VCMX_FRAGMENTS  12
TRAF_ST_VCMX_FRAGMENTS = 12

# #define TRAF_ST_VCMX_BPDU       13
TRAF_ST_VCMX_BPDU = 13

# #define TRAF_ST_LANE_LE_CTRL     1
TRAF_ST_LANE_LE_CTRL = 1

# #define TRAF_ST_LANE_802_3       2
TRAF_ST_LANE_802_3 = 2

# #define TRAF_ST_LANE_802_5       3
TRAF_ST_LANE_802_5 = 3

# #define TRAF_ST_LANE_802_3_MC    4
TRAF_ST_LANE_802_3_MC = 4

# #define TRAF_ST_LANE_802_5_MC    5
TRAF_ST_LANE_802_5_MC = 5

# #define TRAF_ST_IPSILON_FT0      1
TRAF_ST_IPSILON_FT0 = 1

# #define TRAF_ST_IPSILON_FT1      2
TRAF_ST_IPSILON_FT1 = 2

# #define TRAF_ST_IPSILON_FT2      3
TRAF_ST_IPSILON_FT2 = 3

# struct atm_phdr {
#     guint32 flags;
#     guint8  aal;
#     guint8  type;
#     guint8  subtype;
#     guint16 vpi;
#     guint16 vci;
#     guint8  aal2_cid;
#     guint16 channel;
#     guint16 cells;
#     guint16 aal5t_u2u;
#     guint16 aal5t_len;
#     guint32 aal5t_chksum;
# };
class atm_phdr(Structure):
    _fields_ = [('flags', guint32),
                ('aal', guint8),
                ('type', guint8),
                ('subtype', guint8),
                ('vpi', guint16),
                ('vci', guint16),
                ('aal2_cid', guint8),
                ('channel', guint16),
                ('cells', guint16),
                ('aal5t_u2u', guint16),
                ('aal5t_len', guint16),
                ('aal5t_chksum', guint32)]

# #define ASCEND_MAX_STR_LEN 64
ASCEND_MAX_STR_LEN = 64

# #define ASCEND_PFX_WDS_X    1
ASCEND_PFX_WDS_X = 1

# #define ASCEND_PFX_WDS_R    2
ASCEND_PFX_WDS_R = 2

# #define ASCEND_PFX_WDD      3
ASCEND_PFX_WDD = 3

# #define ASCEND_PFX_ISDN_X   4
ASCEND_PFX_ISDN_X = 4

# #define ASCEND_PFX_ISDN_R   5
ASCEND_PFX_ISDN_R = 5

# #define ASCEND_PFX_ETHER    6
ASCEND_PFX_ETHER = 6

# struct ascend_phdr {
#     guint16 type;
#     char    user[ASCEND_MAX_STR_LEN];
#     guint32 sess;
#     char    call_num[ASCEND_MAX_STR_LEN];
#     guint32 chunk;
#     guint32 task;
# };
class ascend_phdr(Structure):
    _fields_ = [('type', guint16),
                ('user', c_char * ASCEND_MAX_STR_LEN),
                ('sess', guint32),
                ('call_num', c_char * ASCEND_MAX_STR_LEN),
                ('chunk', guint32),
                ('task', guint32)]

# struct p2p_phdr {
#     gboolean sent;
# };
class p2p_phdr(Structure):
    _fields_ = [('sent', gboolean)]

# #define PHDR_802_11_PHY_UNKNOWN        0
PHDR_802_11_PHY_UNKNOWN = 0

# #define PHDR_802_11_PHY_11_FHSS        1
PHDR_802_11_PHY_11_FHSS = 1

# #define PHDR_802_11_PHY_11_IR          2
PHDR_802_11_PHY_11_IR = 2

# #define PHDR_802_11_PHY_11_DSSS        3
PHDR_802_11_PHY_11_DSSS = 3

# #define PHDR_802_11_PHY_11B            4
PHDR_802_11_PHY_11B = 4

# #define PHDR_802_11_PHY_11A            5
PHDR_802_11_PHY_11A = 5

# #define PHDR_802_11_PHY_11G            6
PHDR_802_11_PHY_11G = 6

# #define PHDR_802_11_PHY_11N            7
PHDR_802_11_PHY_11N = 7

# #define PHDR_802_11_PHY_11AC           8
PHDR_802_11_PHY_11AC = 8

# #define PHDR_802_11_PHY_11AD           9
PHDR_802_11_PHY_11AD = 9

# #define PHDR_802_11_PHY_11AH          10
PHDR_802_11_PHY_11AH = 10

# #define PHDR_802_11_PHY_11AX          11
PHDR_802_11_PHY_11AX = 11

# struct ieee_802_11_fhss {
#     guint    has_hop_set:1;
#     guint    has_hop_pattern:1;
#     guint    has_hop_index:1;
#     guint8   hop_set;
#     guint8   hop_pattern;
#     guint8   hop_index;
# };
class ieee_802_11_fhss(Structure):
    _fields_ = [('has_hop_set', guint, 1),
                ('has_hop_pattern', guint, 1),
                ('has_hop_index', guint, 1),
                ('hop_set', guint8),
                ('hop_pattern', guint8),
                ('hop_index', guint8)]

# struct ieee_802_11b {
#     guint    has_short_preamble:1;
#     gboolean short_preamble;
# };
class ieee_802_11b(Structure):
    _fields_ = [('has_short_preamble', guint, 1),
                ('short_preamble', gboolean)]

# struct ieee_802_11a {
#     guint    has_channel_type:1;
#     guint    has_turbo_type:1;
#     guint    channel_type:2;
#     guint    turbo_type:2;
# };
class ieee_802_11a(Structure):
    _fields_ = [('has_channel_type', guint, 1),
                ('has_turbo_type', guint, 1),
                ('channel_type', guint, 2),
                ('turbo_type', guint, 2)]

# #define PHDR_802_11A_CHANNEL_TYPE_NORMAL           0
PHDR_802_11A_CHANNEL_TYPE_NORMAL = 0

# #define PHDR_802_11A_CHANNEL_TYPE_HALF_CLOCKED     1
PHDR_802_11A_CHANNEL_TYPE_HALF_CLOCKED = 1

# #define PHDR_802_11A_CHANNEL_TYPE_QUARTER_CLOCKED  2
PHDR_802_11A_CHANNEL_TYPE_QUARTER_CLOCKED = 2

# #define PHDR_802_11A_TURBO_TYPE_NORMAL           0
PHDR_802_11A_TURBO_TYPE_NORMAL = 0

# #define PHDR_802_11A_TURBO_TYPE_TURBO            1
PHDR_802_11A_TURBO_TYPE_TURBO = 1

# #define PHDR_802_11A_TURBO_TYPE_DYNAMIC_TURBO    2
PHDR_802_11A_TURBO_TYPE_DYNAMIC_TURBO = 2

# #define PHDR_802_11A_TURBO_TYPE_STATIC_TURBO     3
PHDR_802_11A_TURBO_TYPE_STATIC_TURBO = 3

# struct ieee_802_11g {
#     guint    has_short_preamble:1;
#     guint    has_mode:1;
#     gboolean short_preamble;
#     guint32  mode;
# };
class ieee_802_11g(Structure):
    _fields_ = [('has_short_preamble', guint, 1),
                ('has_mode', guint, 1),
                ('short_preamble', gboolean),
                ('mode', guint32)]

# #define PHDR_802_11G_MODE_NORMAL    0
PHDR_802_11G_MODE_NORMAL = 0

# #define PHDR_802_11G_MODE_SUPER_G   1
PHDR_802_11G_MODE_SUPER_G = 1

# struct ieee_802_11n {
#     guint    has_mcs_index:1;
#     guint    has_bandwidth:1;
#     guint    has_short_gi:1;
#     guint    has_greenfield:1;
#     guint    has_fec:1;
#     guint    has_stbc_streams:1;
#     guint    has_ness:1;
#     guint16  mcs_index;
#     guint    bandwidth;
#     guint    short_gi:1;
#     guint    greenfield:1;
#     guint    fec:1;
#     guint    stbc_streams:2;
#     guint    ness;
# };
class ieee_802_11n(Structure):
    _fields_ = [('has_mcs_index', guint, 1),
                ('has_bandwidth', guint, 1),
                ('has_short_gi', guint, 1),
                ('has_greenfield', guint, 1),
                ('has_fec', guint, 1),
                ('has_stbc_steams', guint, 1),
                ('has_ness', guint, 1),
                ('mcs_index', guint16),
                ('bandwidth', guint),
                ('short_gi', guint, 1),
                ('greenfield', guint, 1),
                ('fec', guint, 1),
                ('stbc_streams', guint, 2),
                ('ness', guint)]

# #define PHDR_802_11_BANDWIDTH_20_MHZ   0
PHDR_802_11_BANDWIDTH_20_MHZ = 0

# #define PHDR_802_11_BANDWIDTH_40_MHZ   1
PHDR_802_11_BANDWIDTH_40_MHZ = 1

# #define PHDR_802_11_BANDWIDTH_20_20L   2
PHDR_802_11_BANDWIDTH_20_20L = 2

# #define PHDR_802_11_BANDWIDTH_20_20U   3
PHDR_802_11_BANDWIDTH_20_20U = 3

# #define PHDR_802_11_BANDWIDTH_80_MHZ   4
PHDR_802_11_BANDWIDTH_80_MHZ = 4

# #define PHDR_802_11_BANDWIDTH_40_40L   5
PHDR_802_11_BANDWIDTH_40_40L = 5

# #define PHDR_802_11_BANDWIDTH_40_40U   6
PHDR_802_11_BANDWIDTH_40_40U = 6

# #define PHDR_802_11_BANDWIDTH_20LL     7
PHDR_802_11_BANDWIDTH_20LL = 7

# #define PHDR_802_11_BANDWIDTH_20LU     8
PHDR_802_11_BANDWIDTH_20LU = 8

# #define PHDR_802_11_BANDWIDTH_20UL     9
PHDR_802_11_BANDWIDTH_20UL = 9

# #define PHDR_802_11_BANDWIDTH_20UU     10
PHDR_802_11_BANDWIDTH_20UU = 10

# #define PHDR_802_11_BANDWIDTH_160_MHZ  11
PHDR_802_11_BANDWIDTH_160_MHZ = 11

# #define PHDR_802_11_BANDWIDTH_80_80L   12
PHDR_802_11_BANDWIDTH_80_80L = 12

# #define PHDR_802_11_BANDWIDTH_80_80U   13
PHDR_802_11_BANDWIDTH_80_80U = 13

# #define PHDR_802_11_BANDWIDTH_40LL     14
PHDR_802_11_BANDWIDTH_40LL = 14

# #define PHDR_802_11_BANDWIDTH_40LU     15
PHDR_802_11_BANDWIDTH_40LU = 15

# #define PHDR_802_11_BANDWIDTH_40UL     16
PHDR_802_11_BANDWIDTH_40UL = 16

# #define PHDR_802_11_BANDWIDTH_40UU     17
PHDR_802_11_BANDWIDTH_40UU = 17

# #define PHDR_802_11_BANDWIDTH_20LLL    18
PHDR_802_11_BANDWIDTH_20LLL = 18

# #define PHDR_802_11_BANDWIDTH_20LLU    19
PHDR_802_11_BANDWIDTH_20LLU = 19

# #define PHDR_802_11_BANDWIDTH_20LUL    20
PHDR_802_11_BANDWIDTH_20LUL = 20

# #define PHDR_802_11_BANDWIDTH_20LUU    21
PHDR_802_11_BANDWIDTH_20LUU = 21

# #define PHDR_802_11_BANDWIDTH_20ULL    22
PHDR_802_11_BANDWIDTH_20ULL = 22

# #define PHDR_802_11_BANDWIDTH_20ULU    23
PHDR_802_11_BANDWIDTH_20ULU = 23

# #define PHDR_802_11_BANDWIDTH_20UUL    24
PHDR_802_11_BANDWIDTH_20UUL = 24

# #define PHDR_802_11_BANDWIDTH_20UUU    25
PHDR_802_11_BANDWIDTH_20UUU = 25

# struct ieee_802_11ac {
#     guint    has_stbc:1;
#     guint    has_txop_ps_not_allowed:1;
#     guint    has_short_gi:1;
#     guint    has_short_gi_nsym_disambig:1;
#     guint    has_ldpc_extra_ofdm_symbol:1;
#     guint    has_beamformed:1;
#     guint    has_bandwidth:1;
#     guint    has_fec:1;
#     guint    has_group_id:1;
#     guint    has_partial_aid:1;
#     guint    stbc:1;
#     guint    txop_ps_not_allowed:1;
#     guint    short_gi:1;
#     guint    short_gi_nsym_disambig:1;
#     guint    ldpc_extra_ofdm_symbol:1;
#     guint    beamformed:1;
#     guint8   bandwidth;
#     guint8   mcs[4];
#     guint8   nss[4];
#     guint8   fec;
#     guint8   group_id;
#     guint16  partial_aid;
# };
class ieee_802_11ac(Structure):
    _fields_ = [('has_stbc', guint, 1),
                ('has_txop_ps_not_allowed', guint, 1),
                ('has_short_gi', guint, 1),
                ('has_short_gi_nsym_disambig', guint, 1),
                ('has_ldpc_extra_ofdm_symbol', guint, 1),
                ('has_beamformed', guint, 1),
                ('has_bandwidth', guint, 1),
                ('has_fec', guint, 1),
                ('has_group_id', guint, 1),
                ('has_partial_aid', guint, 1),
                ('stbc', guint, 1),
                ('txop_ps_not_allowed', guint, 1),
                ('short_gi', guint, 1),
                ('short_gi_nsym_disambig', guint, 1),
                ('ldpc_extra_ofdm_symbol', guint, 1),
                ('beamformed', guint, 1),
                ('bandwidth', guint8),
                ('mcs', guint8 * 4),
                ('nss', guint8 * 4),
                ('fec', guint8),
                ('group_id', guint8),
                ('partial_aid', guint16)]

# #define PHDR_802_11AD_MIN_FREQUENCY    57000
PHDR_802_11AD_MIN_FREQUENCY = 57000

# #define PHDR_802_11AD_MAX_FREQUENCY    71000
PHDR_802_11AD_MAX_FREQUENCY = 71000

# struct ieee_802_11ad {
#     guint    has_mcs_index:1;
#     guint8   mcs;
# };
class ieee_802_11ad(Structure):
    _fields_ = [('has_mcs_index', guint8, 1),
                ('mcs', guint8)]

# struct ieee_802_11ax {
#     guint    has_mcs_index:1;
#     guint    has_bwru:1;
#     guint    has_gi:1;
#     guint8   nsts:4;
#     guint8   mcs:4;
#     guint8   bwru:4;
#     guint8   gi:2;
# };
class ieee_802_11ax(Structure):
    _fields_ = [('has_mcs_index', guint, 1),
                ('has_bwru', guint, 1),
                ('has_gi', guint, 1),
                ('nsts', guint8, 4),
                ('mcs', guint8, 4),
                ('bwru', guint8, 4),
                ('gi', guint8, 2)]

# union ieee_802_11_phy_info {
#     struct ieee_802_11_fhss info_11_fhss;
#     struct ieee_802_11b info_11b;
#     struct ieee_802_11a info_11a;
#     struct ieee_802_11g info_11g;
#     struct ieee_802_11n info_11n;
#     struct ieee_802_11ac info_11ac;
#     struct ieee_802_11ad info_11ad;
#     struct ieee_802_11ax info_11ax;
# };
class ieee_802_11_phy_info(Union):
    _fields_ = [('info_11_fhss', ieee_802_11_fhss),
                ('info_11b', ieee_802_11b),
                ('info_11a', ieee_802_11a),
                ('info_11g', ieee_802_11g),
                ('info_11n', ieee_802_11n),
                ('info_11ac', ieee_802_11ac),
                ('info_11ad', ieee_802_11ad),
                ('info_11ax', ieee_802_11ax)]

# struct ieee_802_11_phdr {
#     gint     fcs_len;
#     guint    decrypted:1;
#     guint    datapad:1;
#     guint    no_a_msdus:1;
#     guint    phy;
#     union ieee_802_11_phy_info phy_info;
#     guint    has_channel:1;
#     guint    has_frequency:1;
#     guint    has_data_rate:1;
#     guint    has_signal_percent:1;
#     guint    has_noise_percent:1;
#     guint    has_signal_dbm:1;
#     guint    has_noise_dbm:1;
#     guint    has_signal_db:1;
#     guint    has_noise_db:1;
#     guint    has_tsf_timestamp:1;
#     guint    has_aggregate_info:1;
#     guint    has_zero_length_psdu_type:1;
#     guint16  channel;
#     guint32  frequency;
#     guint16  data_rate;
#     guint8   signal_percent;
#     guint8   noise_percent;
#     gint8    signal_dbm;
#     gint8    noise_dbm;
#     guint8   signal_db;
#     guint8   noise_db;
#     guint64  tsf_timestamp;
#     guint32  aggregate_flags;
#     guint32  aggregate_id;
#     guint8   zero_length_psdu_type;
# };
class ieee_802_11_phdr(Structure):
    _fields_ = [('fcs_len', gint),
                ('decrypted', guint, 1),
                ('datapad', guint, 1),
                ('no_a_msdus', guint, 1),
                ('phy', guint),
                ('phy_info', ieee_802_11_phy_info),
                ('has_channel', guint, 1),
                ('has_frequency', guint, 1),
                ('has_data_rate', guint, 1),
                ('has_signal_percent', guint, 1),
                ('has_noise_percent', guint, 1),
                ('has_signal_dbm', guint, 1),
                ('has_noise_dbm', guint, 1),
                ('has_signal_db', guint, 1),
                ('has_noise_db', guint, 1),
                ('has_tsf_timestamp', guint, 1),
                ('has_aggregate_info', guint, 1),
                ('has_zero_length_psdu_type', guint, 1),
                ('channel', guint16),
                ('frequency', guint32),
                ('data_rate', guint16),
                ('signal_percent', guint8),
                ('noise_percent', guint8),
                ('signal_dbm', gint8),
                ('noise_dbm', gint8),
                ('signal_db', guint8),
                ('noise_db', guint8),
                ('tsf_timestamp', guint64),
                ('aggregate_flags', guint32),
                ('aggregate_id', guint32),
                ('zero_length_psdu_type', guint8)]

# #define PHDR_802_11_LAST_PART_OF_A_MPDU    0x00000001
PHDR_802_11_LAST_PART_OF_A_MPDU = 0x00000001

# #define PHDR_802_11_A_MPDU_DELIM_CRC_ERROR 0x00000002
PHDR_802_11_A_MPDU_DELIM_CRC_ERROR = 0x00000002

# #define PHDR_802_11_SOUNDING_PSDU                 0
PHDR_802_11_SOUNDING_PSDU = 0

# #define PHDR_802_11_DATA_NOT_CAPTURED             1
PHDR_802_11_DATA_NOT_CAPTURED = 1

# #define PHDR_802_11_0_LENGTH_PSDU_VENDOR_SPECIFIC 0xff
PHDR_802_11_0_LENGTH_PSDU_VENDOR_SPECIFIC = 0xff

# #define COSINE_MAX_IF_NAME_LEN  128
COSINE_MAX_IF_NAME_LEN = 128

# #define COSINE_ENCAP_TEST      1
COSINE_ENCAP_TEST = 1

# #define COSINE_ENCAP_PPoATM    2
COSINE_ENCAP_PPoATM = 2

# #define COSINE_ENCAP_PPoFR     3
COSINE_ENCAP_PPoFR = 3

# #define COSINE_ENCAP_ATM       4
COSINE_ENCAP_ATM = 4

# #define COSINE_ENCAP_FR        5
COSINE_ENCAP_FR = 5

# #define COSINE_ENCAP_HDLC      6
COSINE_ENCAP_HDLC = 6

# #define COSINE_ENCAP_PPP       7
COSINE_ENCAP_PPP = 7

# #define COSINE_ENCAP_ETH       8
COSINE_ENCAP_ETH = 8

# #define COSINE_ENCAP_UNKNOWN  99
COSINE_ENCAP_UNKNOWN = 99

# #define COSINE_DIR_TX 1
COSINE_DIR_TX = 1

# #define COSINE_DIR_RX 2
COSINE_DIR_RX = 2

# struct cosine_phdr {
#     guint8  encap;
#     guint8  direction;
#     char    if_name[COSINE_MAX_IF_NAME_LEN];
#     guint16 pro;
#     guint16 off;
#     guint16 pri;
#     guint16 rm;
#     guint16 err;
# };
class cosine_phdr(Structure):
    _fields_ = [('encap', guint8),
                ('direction', guint8),
                ('if_name', c_char * COSINE_MAX_IF_NAME_LEN),
                ('pro', guint16),
                ('off', guint16),
                ('pri', guint16),
                ('rm', guint16),
                ('err', guint16)]

# #define IRDA_INCOMING       0x0000
IRDA_INCOMING = 0x0000

# #define IRDA_OUTGOING       0x0004
IRDA_OUTGOING = 0x0004

# #define IRDA_LOG_MESSAGE    0x0100
IRDA_LOG_MESSAGE = 0x0100

# #define IRDA_MISSED_MSG     0x0101
IRDA_MISSED_MSG = 0x0101

# #define IRDA_CLASS_FRAME    0x0000
IRDA_CLASS_FRAME = 0x0000

# #define IRDA_CLASS_LOG      0x0100
IRDA_CLASS_LOG = 0x0100

# #define IRDA_CLASS_MASK     0xFF00
IRDA_CLASS_MASK = 0xFF00

# struct irda_phdr {
#     guint16 pkttype;
# };
class irda_phdr(Structure):
    _fields_ = [('pkttype', guint16)]

# struct nettl_phdr {
#     guint16 subsys;
#     guint32 devid;
#     guint32 kind;
#     gint32  pid;
#     guint32 uid;
# };
class nettl_phdr(Structure):
    _fields_ = [('subsys', guint16),
                ('devid', guint32),
                ('kind', guint32),
                ('pid', gint32),
                ('uid', guint32)]

# #define MTP2_ANNEX_A_NOT_USED      0
MTP2_ANNEX_A_NOT_USED = 0

# #define MTP2_ANNEX_A_USED          1
MTP2_ANNEX_A_USED = 1

# #define MTP2_ANNEX_A_USED_UNKNOWN  2
MTP2_ANNEX_A_USED_UNKNOWN = 2

# struct mtp2_phdr {
#     guint8  sent;
#     guint8  annex_a_used;
#     guint16 link_number;
# };
class mtp2_phdr(Structure):
    _fields_ = [('sent', guint8),
                ('annex_a_used', guint8),
                ('link_number', guint16)]

# typedef union {
#     struct {
#         guint16 vp;
#         guint16 vc;
#         guint16 cid;
#     } atm;
#     guint32 ds0mask;
# } k12_input_info_t;
class k12_input_info_t_atm(Structure):
    _fields_ = [('vp', guint16),
                ('vc', guint16),
                ('cid', guint16)]

class k12_input_info_t(Union):
    _fields_ = [('atm', k12_input_info_t_atm),
                ('ds0mask', guint32)]

# struct k12_phdr {
#     guint32           input;
#     const gchar      *input_name;
#     const gchar      *stack_file;
#     guint32           input_type;
#     k12_input_info_t  input_info;
#     guint8           *extra_info;
#     guint32           extra_length;
#     void*             stuff;
# };
class k12_phdr(Structure):
    _fields_ = [('input', guint32),
                ('input_name', gchar_p),
                ('stack_file', gchar_p),
                ('input_type', guint32),
                ('input_info', k12_input_info_t),
                ('extra_info', POINTER(guint8)),
                ('extra_length', guint32),
                ('stuff', c_void_p)]

# #define K12_PORT_DS0S      0x00010008
K12_PORT_DS0S = 0x00010008

# #define K12_PORT_DS1       0x00100008
K12_PORT_DS1 = 0x00100008

# #define K12_PORT_ATMPVC    0x01020000
K12_PORT_ATMPVC = 0x01020000

# struct lapd_phdr {
#     guint16 pkttype;
#     guint8 we_network;
# };
class lapd_phdr(Structure):
    _fields_ = [('pkttype', guint16),
                ('we_network', guint8)]

# struct wtap;
class wtap(Structure):
    pass

# struct catapult_dct2000_phdr
# {
#     union
#     {
#         struct isdn_phdr isdn;
#         struct atm_phdr  atm;
#         struct p2p_phdr  p2p;
#     } inner_pseudo_header;
#     gint64       seek_off;
#     struct wtap *wth;
# };
class catapult_dct2000_phdr_inner_psuedo_header(Union):
    _fields_ = [('isdn', isdn_phdr),
                ('atm', atm_phdr),
                ('p2p', p2p_phdr)]

class catapult_dct2000_phdr(Structure):
    _fields_ = [('inner_pseudo_header', catapult_dct2000_phdr_inner_psuedo_header),
                ('seek_off', gint64),
                ('wth', POINTER(wtap))]

# struct erf_phdr {
#     guint64 ts;
#     guint8  type;
#     guint8  flags;
#     guint16 rlen;
#     guint16 lctr;
#     guint16 wlen;
# };
class erf_phdr(Structure):
    _fields_ = [('ts', guint64),
                ('type', guint8),
                ('flags', guint8),
                ('rlen', guint16),
                ('lctr', guint16),
                ('wlen', guint16)]

# struct erf_ehdr {
#   guint64 ehdr;
# };
class erf_ehdr(Structure):
    _feilds_ = [('ehdr', guint64)]

# #define MAX_ERF_EHDR 16
MAX_ERF_EHDR = 16

# struct wtap_erf_eth_hdr {
#     guint8 offset;
#     guint8 pad;
# };
class wtap_erf_eth_hdr(Structure):
    _fields_ = [('offset', guint8),
                ('pad', guint8)]

# struct erf_mc_phdr {
#     struct erf_phdr phdr;
#     struct erf_ehdr ehdr_list[MAX_ERF_EHDR];
#     union
#     {
#         struct wtap_erf_eth_hdr eth_hdr;
#         guint32 mc_hdr;
#         guint32 aal2_hdr;
#     } subhdr;
# };
class erf_mc_phdr_subhdr(Union):
    _fields_ = [('eth_hdr', wtap_erf_eth_hdr),
                ('mc_hdr', guint32),
                ('aal2_hdr', guint32)]

class erf_mc_phdr(Structure):
    _fields_ = [('phdr', erf_phdr),
                ('ehdr_list', erf_ehdr * MAX_ERF_EHDR),
                ('subhdr', erf_mc_phdr_subhdr)]

# #define SITA_FRAME_DIR_TXED            (0x00)
SITA_FRAME_DIR_TXED = (0x00)

# #define SITA_FRAME_DIR_RXED            (0x01)
SITA_FRAME_DIR_RXED = (0x01)

# #define SITA_FRAME_DIR                 (0x01)
SITA_FRAME_DIR = (0x01)

# #define SITA_ERROR_NO_BUFFER           (0x80)
SITA_ERROR_NO_BUFFER = (0x80)

# #define SITA_SIG_DSR                   (0x01)
SITA_SIG_DSR = (0x01)

# #define SITA_SIG_DTR                   (0x02)
SITA_SIG_DTR = (0x02)

# #define SITA_SIG_CTS                   (0x04)
SITA_SIG_CTS = (0x04)

# #define SITA_SIG_RTS                   (0x08)
SITA_SIG_RTS = (0x08)

# #define SITA_SIG_DCD                   (0x10)
SITA_SIG_DCD = (0x10)

# #define SITA_SIG_UNDEF1                (0x20)
SITA_SIG_UNDEF1 = (0x20)

# #define SITA_SIG_UNDEF2                (0x40)
SITA_SIG_UNDEF2 = (0x40)

# #define SITA_SIG_UNDEF3                (0x80)
SITA_SIG_UNDEF3 = (0x80)

# #define SITA_ERROR_TX_UNDERRUN         (0x01)
SITA_ERROR_TX_UNDERRUN = (0x01)

# #define SITA_ERROR_TX_CTS_LOST         (0x02)
SITA_ERROR_TX_CTS_LOST = (0x02)

# #define SITA_ERROR_TX_UART_ERROR       (0x04)
SITA_ERROR_TX_UART_ERROR = (0x04)

# #define SITA_ERROR_TX_RETX_LIMIT       (0x08)
SITA_ERROR_TX_RETX_LIMIT = (0x08)

# #define SITA_ERROR_TX_UNDEF1           (0x10)
SITA_ERROR_TX_UNDEF1 = (0x10)

# #define SITA_ERROR_TX_UNDEF2           (0x20)
SITA_ERROR_TX_UNDEF2 = (0x20)

# #define SITA_ERROR_TX_UNDEF3           (0x40)
SITA_ERROR_TX_UNDEF3 = (0x40)

# #define SITA_ERROR_TX_UNDEF4           (0x80)
SITA_ERROR_TX_UNDEF4 = (0x80)

# #define SITA_ERROR_RX_FRAMING          (0x01)
SITA_ERROR_RX_FRAMING = (0x01)

# #define SITA_ERROR_RX_PARITY           (0x02)
SITA_ERROR_RX_PARITY = (0x02)

# #define SITA_ERROR_RX_COLLISION        (0x04)
SITA_ERROR_RX_COLLISION = (0x04)

# #define SITA_ERROR_RX_FRAME_LONG       (0x08)
SITA_ERROR_RX_FRAME_LONG = (0x08)

# #define SITA_ERROR_RX_FRAME_SHORT      (0x10)
SITA_ERROR_RX_FRAME_SHORT = (0x10)

# #define SITA_ERROR_RX_UNDEF1           (0x20)
SITA_ERROR_RX_UNDEF1 = (0x20)

# #define SITA_ERROR_RX_UNDEF2           (0x40)
SITA_ERROR_RX_UNDEF2 = (0x40)

# #define SITA_ERROR_RX_UNDEF3           (0x80)
SITA_ERROR_RX_UNDEF3 = (0x80)

# #define SITA_ERROR_RX_NONOCTET_ALIGNED (0x01)
SITA_ERROR_RX_NONOCTET_ALIGNED = (0x01)

# #define SITA_ERROR_RX_ABORT            (0x02)
SITA_ERROR_RX_ABORT = (0x02)

# #define SITA_ERROR_RX_CD_LOST          (0x04)
SITA_ERROR_RX_CD_LOST = (0x04)

# #define SITA_ERROR_RX_DPLL             (0x08)
SITA_ERROR_RX_DPLL = (0x08)

# #define SITA_ERROR_RX_OVERRUN          (0x10)
SITA_ERROR_RX_OVERRUN = (0x10)

# #define SITA_ERROR_RX_FRAME_LEN_VIOL   (0x20)
SITA_ERROR_RX_FRAME_LEN_VIOL = (0x20)

# #define SITA_ERROR_RX_CRC              (0x40)
SITA_ERROR_RX_CRC = (0x40)

# #define SITA_ERROR_RX_BREAK            (0x80)
SITA_ERROR_RX_BREAK = (0x80)

# #define SITA_PROTO_UNUSED              (0x00)
SITA_PROTO_UNUSED = (0x00)

# #define SITA_PROTO_BOP_LAPB            (0x01)
SITA_PROTO_BOP_LAPB = (0x01)

# #define SITA_PROTO_ETHERNET            (0x02)
SITA_PROTO_ETHERNET = (0x02)

# #define SITA_PROTO_ASYNC_INTIO         (0x03)
SITA_PROTO_ASYNC_INTIO = (0x03)

# #define SITA_PROTO_ASYNC_BLKIO         (0x04)
SITA_PROTO_ASYNC_BLKIO = (0x04)

# #define SITA_PROTO_ALC                 (0x05)
SITA_PROTO_ALC = (0x05)

# #define SITA_PROTO_UTS                 (0x06)
SITA_PROTO_UTS = (0x06)

# #define SITA_PROTO_PPP_HDLC            (0x07)
SITA_PROTO_PPP_HDLC = (0x07)

# #define SITA_PROTO_SDLC                (0x08)
SITA_PROTO_SDLC = (0x08)

# #define SITA_PROTO_TOKENRING           (0x09)
SITA_PROTO_TOKENRING = (0x09)

# #define SITA_PROTO_I2C                 (0x10)
SITA_PROTO_I2C = (0x10)

# #define SITA_PROTO_DPM_LINK            (0x11)
SITA_PROTO_DPM_LINK = (0x11)

# #define SITA_PROTO_BOP_FRL             (0x12)
SITA_PROTO_BOP_FRL = (0x12)

# struct sita_phdr {
#     guint8  sita_flags;
#     guint8  sita_signals;
#     guint8  sita_errors1;
#     guint8  sita_errors2;
#     guint8  sita_proto;
# };
class sita_phdr(Structure):
    _fields_ = [('sita_flags', guint8),
                ('sita_signals', guint8),
                ('sita_errors1', guint8),
                ('sita_errors2', guint8),
                ('sita_proto', guint8)]

# struct bthci_phdr {
#     gboolean  sent;
#     guint32   channel;
# };
class bthci_phdr(Structure):
    _fields_ = [('sent', gboolean),
                ('channel', guint32)]

# #define BTHCI_CHANNEL_COMMAND  1
BTHCI_CHANNEL_COMMAND = 1

# #define BTHCI_CHANNEL_ACL      2
BTHCI_CHANNEL_ACL = 2

# #define BTHCI_CHANNEL_SCO      3
BTHCI_CHANNEL_SCO = 3

# #define BTHCI_CHANNEL_EVENT    4
BTHCI_CHANNEL_EVENT = 4

# #define BTHCI_CHANNEL_ISO      5
BTHCI_CHANNEL_ISO = 5

# struct btmon_phdr {
#     guint16   adapter_id;
#     guint16   opcode;
# };
class btmon_phdr(Structure):
    _fields_ = [('adapter_id', guint16),
                ('opcode', guint16)]

# struct l1event_phdr {
#     gboolean uton;
# };
class l1event_phdr(Structure):
    _fields_ = [('uton', gboolean)]

# struct i2c_phdr {
#     guint8  is_event;
#     guint8  bus;
#     guint32 flags;
# };
class i2c_phdr(Structure):
    _fields_  = [('is_event', guint8),
                 ('bus', guint8),
                 ('flags', guint32)]

# struct gsm_um_phdr {
#     gboolean uplink;
#     guint8   channel;
#     guint8   bsic;
#     guint16  arfcn;
#     guint32  tdma_frame;
#     guint8   error;
#     guint16  timeshift;
# };
class gsm_um_phdr(Structure):
    _fields_ = [('uplink', gboolean),
                ('channel', guint8),
                ('bsic', guint8),
                ('arfcn', guint16),
                ('tdma_frame', guint32),
                ('error', guint8),
                ('timeshift', guint16)]

# #define GSM_UM_CHANNEL_UNKNOWN  0
GSM_UM_CHANNEL_UNKNOWN = 0

# #define GSM_UM_CHANNEL_BCCH     1
GSM_UM_CHANNEL_BCCH = 1

# #define GSM_UM_CHANNEL_SDCCH    2
GSM_UM_CHANNEL_SDCCH = 2

# #define GSM_UM_CHANNEL_SACCH    3
GSM_UM_CHANNEL_SACCH = 3

# #define GSM_UM_CHANNEL_FACCH    4
GSM_UM_CHANNEL_FACCH = 4

# #define GSM_UM_CHANNEL_CCCH     5
GSM_UM_CHANNEL_CCCH = 5

# #define GSM_UM_CHANNEL_RACH     6
GSM_UM_CHANNEL_RACH = 6

# #define GSM_UM_CHANNEL_AGCH     7
GSM_UM_CHANNEL_AGCH = 7

# #define GSM_UM_CHANNEL_PCH      8
GSM_UM_CHANNEL_PCH = 8

# struct nstr_phdr {
#     gint64 rec_offset;
#     gint32 rec_len;
#     guint8 nicno_offset;
#     guint8 nicno_len;
#     guint8 dir_offset;
#     guint8 dir_len;
#     guint16 eth_offset;
#     guint8 pcb_offset;
#     guint8 l_pcb_offset;
#     guint8 rec_type;
#     guint8 vlantag_offset;
#     guint8 coreid_offset;
#     guint8 srcnodeid_offset;
#     guint8 destnodeid_offset;
#     guint8 clflags_offset;
#     guint8 src_vmname_len_offset;
#     guint8 dst_vmname_len_offset;
#     guint8 ns_activity_offset;
#     guint8 data_offset;
# };
class nstr_phdr(Structure):
    _fields_ = [('rec_offset', gint64),
                ('rec_len', gint32),
                ('nicno_offset', guint8),
                ('nicno_len', guint8),
                ('dir_offset', guint8),
                ('dir_len', guint8),
                ('eth_offset', guint16),
                ('pcb_offset', guint8),
                ('l_pcb_offset', guint8),
                ('rec_type', guint8),
                ('vlantag_offset', guint8),
                ('coreid_offset', guint8),
                ('srcnodeid_offset', guint8),
                ('destnodeid_offset', guint8),
                ('clflags_offset', guint8),
                ('src_vmname_len_offset', guint8),
                ('dst_vmname_len_offset', guint8),
                ('ns_activity_offset', guint8),
                ('data_offset', guint8)]

# struct nokia_phdr {
#     struct eth_phdr eth;
#     guint8 stuff[4];
# };
class nokia_phdr(Structure):
    _fields_ = [('eth', eth_phdr),
                ('stuff', guint8 * 4)]

# #define LLCP_PHDR_FLAG_SENT 0
LLCP_PHDR_FLAG_SENT = 0

# struct llcp_phdr {
#     guint8 adapter;
#     guint8 flags;
# };
class llcp_phdr(Structure):
    _fields_ = [('adapter', guint8),
                ('flags', guint8)]

# struct logcat_phdr {
#     gint version;
# };
class logcat_phdr(Structure):
    _fields_ = [('version', gint)]

# struct netmon_phdr {
#     guint8* title;
#     guint32 descLength;
#     guint8* description;
#     guint sub_encap;
#     union sub_wtap_pseudo_header {
#         struct eth_phdr     eth;
#         struct atm_phdr     atm;
#         struct ieee_802_11_phdr ieee_802_11;
#     } subheader;
# };
class sub_wtap_pseudo_header(Union):
    _fields_ = [('eth', eth_phdr),
                ('atm', atm_phdr),
                ('ieee_802_11', ieee_802_11_phdr)]

class netmon_phdr(Structure):
    _fields_ = [('title', POINTER(guint8)),
                ('descLength', guint32),
                ('description', POINTER(guint8)),
                ('sub_encap', guint),
                ('subheader', sub_wtap_pseudo_header)]

# union wtap_pseudo_header {
#     struct eth_phdr     eth;
#     struct dte_dce_phdr dte_dce;
#     struct isdn_phdr    isdn;
#     struct atm_phdr     atm;
#     struct ascend_phdr  ascend;
#     struct p2p_phdr     p2p;
#     struct ieee_802_11_phdr ieee_802_11;
#     struct cosine_phdr  cosine;
#     struct irda_phdr    irda;
#     struct nettl_phdr   nettl;
#     struct mtp2_phdr    mtp2;
#     struct k12_phdr     k12;
#     struct lapd_phdr    lapd;
#     struct catapult_dct2000_phdr dct2000;
#     struct erf_mc_phdr  erf;
#     struct sita_phdr    sita;
#     struct bthci_phdr   bthci;
#     struct btmon_phdr   btmon;
#     struct l1event_phdr l1event;
#     struct i2c_phdr     i2c;
#     struct gsm_um_phdr  gsm_um;
#     struct nstr_phdr    nstr;
#     struct nokia_phdr   nokia;
#     struct llcp_phdr    llcp;
#     struct logcat_phdr  logcat;
#     struct netmon_phdr  netmon;
# };
class wtap_pseudo_header(Union):
    _fields_ = [('eth', eth_phdr),
                ('dte_dce', dte_dce_phdr),
                ('isdn', isdn_phdr),
                ('atm', atm_phdr),
                ('ascend', ascend_phdr),
                ('p2p', p2p_phdr),
                ('ieee_802_11', ieee_802_11_phdr),
                ('cosine', cosine_phdr),
                ('irda', irda_phdr),
                ('nettl', nettl_phdr),
                ('mtp2', mtp2_phdr),
                ('k12', k12_phdr),
                ('lapd', lapd_phdr),
                ('dct2000', catapult_dct2000_phdr),
                ('erf', erf_mc_phdr),
                ('sita', sita_phdr),
                ('bthci', bthci_phdr),
                ('btmon', btmon_phdr),
                ('l1event', l1event_phdr),
                ('i2c', i2c_phdr),
                ('gsm_um', gsm_um_phdr),
                ('nstr', nstr_phdr),
                ('nokia', nokia_phdr),
                ('llcp', llcp_phdr),
                ('logcat', logcat_phdr),
                ('netmon', netmon_phdr)]

# #define REC_TYPE_PACKET               0
REC_TYPE_PACKET = 0

# #define REC_TYPE_FT_SPECIFIC_EVENT    1
REC_TYPE_FT_SPECIFIC_EVENT = 1

# #define REC_TYPE_FT_SPECIFIC_REPORT   2
REC_TYPE_FT_SPECIFIC_REPORT = 2

# #define REC_TYPE_SYSCALL              3
REC_TYPE_SYSCALL = 3

# #define REC_TYPE_SYSTEMD_JOURNAL      4
REC_TYPE_SYSTEMD_JOURNAL = 4

# typedef struct {
#     guint32   caplen;
#     guint32   len;
#     int       pkt_encap;
#     guint32   interface_id;
#     guint64   drop_count;
#     guint32   pack_flags;
#     guint32   interface_queue;
#     guint64   packet_id;
#     union wtap_pseudo_header  pseudo_header;
# } wtap_packet_header;
class wtap_packet_header(Structure):
    _fields_ = [('caplen', guint32),
                ('len', guint32),
                ('pkt_encap', c_int),
                ('interface_id', guint32),
                ('drop_count', guint64),
                ('pack_flags', guint32),
                ('interface_queue', guint32),
                ('packet_id', guint64),
                ('pseudo_header', wtap_pseudo_header)]

# #define PACK_FLAGS_DIRECTION_MASK     0x00000003
PACK_FLAGS_DIRECTION_MASK = 0x00000003

# #define PACK_FLAGS_DIRECTION_SHIFT    0
PACK_FLAGS_DIRECTION_SHIFT = 0

# #define PACK_FLAGS_DIRECTION_UNKNOWN  0
PACK_FLAGS_DIRECTION_UNKNOWN = 0

# #define PACK_FLAGS_DIRECTION_INBOUND  1
PACK_FLAGS_DIRECTION_INBOUND = 1

# #define PACK_FLAGS_DIRECTION_OUTBOUND 2
PACK_FLAGS_DIRECTION_OUTBOUND = 2

# #define PACK_FLAGS_RECEPTION_TYPE_MASK        0x0000001C
PACK_FLAGS_RECEPTION_TYPE_MASK = 0x0000001C

# #define PACK_FLAGS_RECEPTION_TYPE_SHIFT       2
PACK_FLAGS_RECEPTION_TYPE_SHIFT = 2

# #define PACK_FLAGS_RECEPTION_TYPE_UNSPECIFIED 0
PACK_FLAGS_RECEPTION_TYPE_UNSPECIFIED = 0

# #define PACK_FLAGS_RECEPTION_TYPE_UNICAST     1
PACK_FLAGS_RECEPTION_TYPE_UNICAST = 1

# #define PACK_FLAGS_RECEPTION_TYPE_MULTICAST   2
PACK_FLAGS_RECEPTION_TYPE_MULTICAST = 2

# #define PACK_FLAGS_RECEPTION_TYPE_BROADCAST   3
PACK_FLAGS_RECEPTION_TYPE_BROADCAST = 3

# #define PACK_FLAGS_RECEPTION_TYPE_PROMISCUOUS 4
PACK_FLAGS_RECEPTION_TYPE_PROMISCUOUS = 4

# #define PACK_FLAGS_FCS_LENGTH_MASK                        0x000001E0
PACK_FLAGS_FCS_LENGTH_MASK = 0x000001E0

# #define PACK_FLAGS_FCS_LENGTH_SHIFT                       5
PACK_FLAGS_FCS_LENGTH_SHIFT = 5

# #define PACK_FLAGS_RESERVED_MASK                          0x0000FE00
PACK_FLAGS_RESERVED_MASK = 0x0000FE00

# #define PACK_FLAGS_CRC_ERROR                   0x01000000
PACK_FLAGS_CRC_ERROR = 0x01000000

# #define PACK_FLAGS_PACKET_TOO_LONG             0x02000000
PACK_FLAGS_PACKET_TOO_LONG = 0x02000000

# #define PACK_FLAGS_PACKET_TOO_SHORT            0x04000000
PACK_FLAGS_PACKET_TOO_SHORT = 0x04000000

# #define PACK_FLAGS_WRONG_INTER_FRAME_GAP       0x08000000
PACK_FLAGS_WRONG_INTER_FRAME_GAP = 0x08000000

# #define PACK_FLAGS_UNALIGNED_FRAME             0x10000000
PACK_FLAGS_UNALIGNED_FRAME = 0x10000000

# #define PACK_FLAGS_START_FRAME_DELIMITER_ERROR 0x20000000
PACK_FLAGS_START_FRAME_DELIMITER_ERROR = 0x20000000

# #define PACK_FLAGS_PREAMBLE_ERROR              0x40000000
PACK_FLAGS_PREAMBLE_ERROR = 0x40000000

# #define PACK_FLAGS_SYMBOL_ERROR                0x80000000
PACK_FLAGS_SYMBOL_ERROR = 0x80000000

# typedef struct {
#     guint     record_type;
#     guint32   record_len;
# } wtap_ft_specific_header;
class wtap_ft_specific_header(Structure):
    _fields_ = [('record_type', guint),
                ('record_len', guint32)]

# typedef struct {
#     guint     record_type;
#     int       byte_order;
#     guint64   timestamp;
#     guint64   thread_id;
#     guint32   event_len;
#     guint32   event_filelen;
#     guint16   event_type;
#     guint16   cpu_id;
# } wtap_syscall_header;
class wtap_syscall_header(Structure):
    _fields_ = [('record_type', guint),
                ('byte_order', c_int),
                ('timestamp', guint64),
                ('thread_id', guint64),
                ('event_len', guint32),
                ('event_filelen', guint32),
                ('event_type', guint16),
                ('cpu_id', guint16)]

# typedef struct {
#     guint32   record_len;
# } wtap_systemd_journal_header;
class wtap_systemd_journal_header(Structure):
    _fields_ = [('record_len', guint32)]

# typedef struct {
#     guint     rec_type;
#     guint32   presence_flags;
#     nstime_t  ts;
#     int       tsprec;
#     union {
#         wtap_packet_header packet_header;
#         wtap_ft_specific_header ft_specific_header;
#         wtap_syscall_header syscall_header;
#         wtap_systemd_journal_header systemd_journal_header;
#     } rec_header;
#     gchar     *opt_comment;
#     gboolean  has_comment_changed;
#     GPtrArray *packet_verdict;
#     Buffer    options_buf;
# } wtap_rec;
class wtap_rec_rec_header(Union):
    _fields_ = [('packet_header', wtap_packet_header),
                ('ft_specific_header', wtap_ft_specific_header),
                ('syscall_header', wtap_syscall_header),
                ('systemd_journal_header', wtap_systemd_journal_header)]

class wtap_rec(Structure):
    _fields_ = [('rec_type', guint),
                ('presence_flags', guint32),
                ('ts', nstime_t),
                ('tsprec', c_int),
                ('rec_header', wtap_rec_rec_header),
                ('opt_comment', gchar_p),
                ('has_comment_changed', gboolean),
                ('packet_verdict', POINTER(GPtrArray)),
                ('options_buf', Buffer)]

# #define WTAP_HAS_TS            0x00000001
WTAP_HAS_TS = 0x00000001

# #define WTAP_HAS_CAP_LEN       0x00000002
WTAP_HAS_CAP_LEN = 0x00000002

# #define WTAP_HAS_INTERFACE_ID  0x00000004
WTAP_HAS_INTERFACE_ID = 0x00000004

# #define WTAP_HAS_COMMENTS      0x00000008
WTAP_HAS_COMMENTS = 0x00000008

# #define WTAP_HAS_DROP_COUNT    0x00000010
WTAP_HAS_DROP_COUNT = 0x00000010

# #define WTAP_HAS_PACK_FLAGS    0x00000020
WTAP_HAS_PACK_FLAGS = 0x00000020

# #define WTAP_HAS_PACKET_ID     0x00000040
WTAP_HAS_PACKET_ID = 0x00000040

# #define WTAP_HAS_INT_QUEUE     0x00000080
WTAP_HAS_INT_QUEUE = 0x00000080

# #define WTAP_HAS_VERDICT       0x00000100
WTAP_HAS_VERDICT = 0x00000100

# typedef struct wtapng_section_mandatory_s {
#     guint64             section_length;
# } wtapng_mandatory_section_t;
class wtapng_section_mandatory_s(Structure):
    _fields_ = [('section_length', guint64)]

wtapng_mandatory_section_t = wtapng_section_mandatory_s

# typedef struct wtapng_iface_descriptions_s {
#     GArray *interface_data;
# } wtapng_iface_descriptions_t;
class wtapng_iface_descriptions_s(Structure):
    _fields_ = [('interface_data', POINTER(GArray))]

wtapng_iface_descriptions_t = wtapng_iface_descriptions_s

# typedef struct wtapng_if_descr_mandatory_s {
#     int                    wtap_encap;
#     guint64                time_units_per_second;
#     int                    tsprecision;
#     guint32                snap_len;
#     guint8                 num_stat_entries;
#     GArray                *interface_statistics;
# } wtapng_if_descr_mandatory_t;
class wtapng_if_descr_mandatory_s(Structure):
    _fields_ = [('wtap_encap', c_int),
                ('time_units_per_second', guint64),
                ('tsprecision', c_int),
                ('snap_len', guint32),
                ('num_stat_entries', guint8),
                ('interface_statistics', POINTER(GArray))]

wtapng_if_descr_mandatory_t = wtapng_if_descr_mandatory_s

# typedef struct wtapng_dsb_mandatory_s {
#     guint32                secrets_type;
#     guint32                secrets_len;
#     guint8                *secrets_data;
# } wtapng_dsb_mandatory_t;
class wtapng_dsb_mandatory_s(Structure):
    _fields_ = [('secrets_type', guint32),
                ('secrets_len', guint32),
                ('secrets_data', POINTER(guint8))]

wtapng_dsb_mandatory_t = wtapng_dsb_mandatory_s

# typedef struct wtapng_if_descr_filter_s {
#     gchar                 *if_filter_str;
#     guint16                bpf_filter_len;
#     guint8                *if_filter_bpf_bytes;
# } wtapng_if_descr_filter_t;
class wtapng_if_descr_filter_s(Structure):
    _fields_ = [('if_filter_str', gchar_p),
                ('bpf_filter_len', guint16),
                ('if_filter_bpf_bytes', POINTER(guint8))]

wtapng_if_descr_filter_t = wtapng_if_descr_filter_s

# typedef struct wtapng_if_stats_mandatory_s {
#     guint32  interface_id;
#     guint32  ts_high;
#     guint32  ts_low;
# } wtapng_if_stats_mandatory_t;
class wtapng_if_stats_mandatory_s(Structure):
    _fields_ = [('interface_id', guint32),
                ('ts_high', guint32),
                ('ts_low', guint32)]

wtapng_if_stats_mandatory_t = wtapng_if_stats_mandatory_s

# #ifndef MAXNAMELEN
# #define MAXNAMELEN  	64
MAXNAMELEN = 64
# #endif

# typedef struct hashipv4 {
#     guint             addr;
#     guint8            flags;
#     gchar             ip[WS_INET_ADDRSTRLEN];
#     gchar             name[MAXNAMELEN];
# } hashipv4_t;
class hashipv4(Structure):
    _fields_ = [('addr', guint),
                ('flags', guint8),
                ('ip', gchar * WS_INET_ADDRSTRLEN),
                ('name', gchar * MAXNAMELEN)]

hashipv4_t = hashipv4

# typedef struct hashipv6 {
#     guint8            addr[16];
#     guint8            flags;
#     gchar             ip6[WS_INET6_ADDRSTRLEN];
#     gchar             name[MAXNAMELEN];
# } hashipv6_t;
class hashipv6(Structure):
    _fields_ = [('addr', guint8 * 16),
                ('flags', guint8),
                ('ip6', gchar * WS_INET6_ADDRSTRLEN),
                ('name', gchar * MAXNAMELEN)]

hashipv6_t = hashipv6

# typedef struct addrinfo_lists {
#     GList      *ipv4_addr_list;
#     GList      *ipv6_addr_list;
# } addrinfo_lists_t;
class addrinfo_lists(Structure):
    _fields_ = [('ipv4_addr_list', POINTER(GList)),
                ('ipv6_addr_list', POINTER(GList))]

addrinfo_lists_t = addrinfo_lists

# typedef struct wtap_dump_params {
#     int         encap;
#     int         snaplen;
#     int         tsprec;
#     GArray     *shb_hdrs;
#     wtapng_iface_descriptions_t *idb_inf;
#     GArray     *nrb_hdrs;
#     GArray     *dsbs_initial;
#     const GArray *dsbs_growing;
#     gboolean    dont_copy_idbs;
# } wtap_dump_params;
class wtap_dump_params(Structure):
    _fields_ = [('encap', c_int),
                ('snaplen', c_int),
                ('tsprec', c_int),
                ('shb_hdrs', POINTER(GArray)),
                ('idb_inf', POINTER(wtapng_iface_descriptions_t)),
                ('nrb_hdrs', POINTER(GArray)),
                ('dsbs_initial', POINTER(GArray)),
                ('dsbs_growing', POINTER(GArray)),
                ('dont_copy_idbs', gboolean)]

# #define WTAP_DUMP_PARAMS_INIT {.snaplen=0}
WTAP_DUMP_PARAMS_INIT = wtap_dump_params(snaplen=0)

# struct wtap_dumper;
wtap_dumper = None

# typedef struct wtap_reader *FILE_T;
wtap_reader = None
FILE_T = c_void_p

# typedef struct wtap_wslua_file_info {
#     int (*wslua_can_write_encap)(int, void*);
#     void* wslua_data;
# } wtap_wslua_file_info_t;
class wtap_wslua_file_info(Structure):
    _fields_ = [('wslua_can_write_encap', CFUNCTYPE(c_int, c_int, c_void_p)),
                ('wslua_data', c_void_p)]

wtap_wslua_file_info_t = wtap_wslua_file_info

# struct file_extension_info {
#     const char *name;
#     gboolean is_capture_file;
#     const char *extensions;
# };
class file_extension_info(Structure):
    _fields_ = [('name', c_char_p),
                ('is_capture_file', gboolean),
                ('extensions', c_char_p)]

# typedef enum {
#     WTAP_OPEN_NOT_MINE = 0,
#     WTAP_OPEN_MINE = 1,
#     WTAP_OPEN_ERROR = -1
# } wtap_open_return_val;
wtap_open_return_val = c_int
WTAP_OPEN_NOT_MINE = 0
WTAP_OPEN_MINE = 1
WTAP_OPEN_ERROR = -1

# typedef wtap_open_return_val (*wtap_open_routine_t)(struct wtap*, int *, char **);
wtap_open_routine_t = CFUNCTYPE(wtap_open_return_val,
                                POINTER(wtap),
                                POINTER(c_int),
                                POINTER(c_char_p))

# typedef enum {
#     OPEN_INFO_MAGIC = 0,
#     OPEN_INFO_HEURISTIC = 1
# } wtap_open_type;
wtap_open_type = c_int
OPEN_INFO_MAGIC = 0
OPEN_INFO_HEURISTIC = 1

# struct open_info {
#     const char *name;
#     wtap_open_type type;
#     wtap_open_routine_t open_routine;
#     const char *extensions;
#     gchar **extensions_set;
#     void* wslua_data;
# };
class open_info(Structure):
    _fields_ = [('name', c_char_p),
                ('type', wtap_open_type),
                ('open_routine', wtap_open_routine_t),
                ('extensions', c_char_p),
                ('extensions_set', POINTER(gchar_p)),
                ('wslua_data', c_void_p)]

# #define WTAP_COMMENT_PER_SECTION        0x00000001
WTAP_COMMENT_PER_SECTION = 0x00000001

# #define WTAP_COMMENT_PER_INTERFACE      0x00000002
WTAP_COMMENT_PER_INTERFACE = 0x00000002

# #define WTAP_COMMENT_PER_PACKET         0x00000004
WTAP_COMMENT_PER_PACKET = 0x00000004

# struct file_type_subtype_info {
#     const char *name;
#     const char *short_name;
#     const char *default_file_extension;
#     const char *additional_file_extensions;
#     gboolean writing_must_seek;
#     gboolean has_name_resolution;
#     guint32 supported_comment_types;
#     int (*can_write_encap)(int);
#     int (*dump_open)(wtap_dumper *, int *, gchar **);
#     wtap_wslua_file_info_t *wslua_info;
# };
class file_type_subtype_info(Structure):
    _fields_ = [('name', c_char_p),
                ('short_name', c_char_p),
                ('default_file_extension', c_char_p),
                ('additional_file_extensions', c_char_p),
                ('writing_must_seek', gboolean),
                ('has_name_resolution', gboolean),
                ('supported_comment_types', guint32),
                ('can_write_encap', CFUNCTYPE(c_int, c_int)),
                ('dump_open', CFUNCTYPE(c_int,
                                        POINTER(wtap_dumper),
                                        POINTER(c_int),
                                        POINTER(gchar_p))),
                ('wslua_info', POINTER(wtap_wslua_file_info_t))]

# #define WTAP_TYPE_AUTO 0
WTAP_TYPE_AUTO = 0

# typedef void (*wtap_new_ipv4_callback_t) (const guint addr, const gchar *name);
wtap_new_ipv4_callback_t = CFUNCTYPE(None, guint, gchar_p)

# typedef void (*wtap_new_ipv6_callback_t) (const void *addrp, const gchar *name);
wtap_new_ipv6_callback_t = CFUNCTYPE(None, c_void_p, gchar_p)

# typedef void (*wtap_new_secrets_callback_t)(guint32 secrets_type,
#                                             const void *secrets, guint size);
wtap_new_secrets_callback_t = CFUNCTYPE(None, guint32, c_void_p, guint)

# typedef enum {
# 	TS_RELATIVE,
# 	TS_ABSOLUTE,
# 	TS_ABSOLUTE_WITH_YMD,
# 	TS_ABSOLUTE_WITH_YDOY,
# 	TS_DELTA,
# 	TS_DELTA_DIS,
# 	TS_EPOCH,
# 	TS_UTC,
# 	TS_UTC_WITH_YMD,
# 	TS_UTC_WITH_YDOY,
# 	TS_NOT_SET
# } ts_type;
ts_type = c_int
TS_RELATIVE = 0
TS_ABSOLUTE = 1
TS_ABSOLUTE_WITH_YMD = 2
TS_ABSOLUTE_WITH_YDOY = 3
TS_DELTA = 4
TS_DELTA_DIS = 5
TS_EPOCH = 6
TS_UTC = 7
TS_UTC_WITH_YMD = 8
TS_UTC_WITH_YDOY = 9
TS_NOT_SET = 10

# typedef enum {
# 	TS_PREC_AUTO,
# 	TS_PREC_FIXED_SEC,
# 	TS_PREC_FIXED_DSEC,
# 	TS_PREC_FIXED_CSEC,
# 	TS_PREC_FIXED_MSEC,
# 	TS_PREC_FIXED_USEC,
# 	TS_PREC_FIXED_NSEC
# } ts_precision;
ts_precision = c_int
TS_PREC_AUTO = 0
TS_PREC_FIXED_SEC = 1
TS_PREC_FIXED_DSEC = 2
TS_PREC_FIXED_CSEC = 3
TS_PREC_FIXED_MSEC = 4
TS_PREC_FIXED_USEC = 5
TS_PREC_FIXED_NSEC = 6

# typedef enum {
# 	TS_SECONDS_DEFAULT,
# 	TS_SECONDS_HOUR_MIN_SEC,
# 	TS_SECONDS_NOT_SET
# } ts_seconds_type;
ts_seconds_type = c_int
TS_SECONDS_DEFAULT = 0
TS_SECONDS_HOUR_MIN_SEC = 1
TS_SECONDS_NOT_SET = 2

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
RA_NONE = 0
RA_DISSECTORS = 1
RA_LISTENERS = 2
RA_EXTCAP = 3
RA_REGISTER = 4
RA_PLUGIN_REGISTER = 5
RA_HANDOFF = 6
RA_PLUGIN_HANDOFF = 7
RA_LUA_PLUGINS = 8
RA_LUA_DEREGISTER = 9
RA_PREFERENCES = 10
RA_INTERFACES = 11

# #define RA_BASE_COUNT (RA_INTERFACES - 3)
RA_BASE_COUNT = RA_INTERFACES - 3

# typedef void (*register_cb)(register_action_e action, const char *message, gpointer client_data);
register_cb = CFUNCTYPE(None, register_action_e, c_char_p, gpointer)

# typedef struct {
#     guint16 red;
#     guint16 green;
#     guint16 blue;
# } color_t;
class color_t(Structure):
    _fields_ = [('red', guint16),
                ('green', guint16),
                ('blue', guint16)]

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
layout_unused = 0
layout_type_5 = 1
layout_type_2 = 2
layout_type_1 = 3
layout_type_4 = 4
layout_type_3 = 5
layout_type_6 = 6
layout_type_max = 7

# typedef enum {
#     layout_pane_content_none,
#     layout_pane_content_plist,
#     layout_pane_content_pdetails,
#     layout_pane_content_pbytes,
#     layout_pane_content_pdiagram,
# } layout_pane_content_e;
layout_pane_content_e = c_int
layout_pane_content_none = 0
layout_pane_content_plist = 1
layout_pane_content_pdetails = 2
layout_pane_content_pbytes = 3
layout_pane_content_pdiagram = 4

# typedef enum {
#     console_open_never,
#     console_open_auto,
#     console_open_always
# } console_open_e;
console_open_e = c_int
console_open_never = 0
console_open_auto = 1
console_open_always = 2

# typedef enum {
#     version_welcome_only,
#     version_title_only,
#     version_both,
#     version_neither
# } version_info_e;
version_info_e = c_int
version_welcome_only = 0
version_title_only = 1
version_both = 2
version_neither = 3

# typedef enum {
#     pref_default,
#     pref_stashed,
#     pref_current
# } pref_source_t;
pref_source_t = c_int
pref_default = 0
pref_stashed = 1
pref_current = 2

# typedef enum {
#     ELIDE_LEFT,
#     ELIDE_RIGHT,
#     ELIDE_MIDDLE,
#     ELIDE_NONE
# } elide_mode_e;
elide_mode_e = c_int
ELIDE_LEFT = 0
ELIDE_RIGHT = 1
ELIDE_MIDDLE = 2
ELIDE_NONE = 3

# typedef enum {
#     UPDATE_CHANNEL_DEVELOPMENT,
#     UPDATE_CHANNEL_STABLE
# } software_update_channel_e;
software_update_channel_e = c_int
UPDATE_CHANNEL_DEVELOPEMENT = 0
UPDATE_CHANNEL_STABLE = 1

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
                ('gui_colorized_fg', color_t),
                ('gui_colorized_bg', color_t),
                ('gui_geometry_save_position', gboolean),
                ('gui_geometry_save_size', gboolean),
                ('gui_geometry_save_maximized', gboolean),
                ('gui_console_open', console_open_e),
                ('gui_recent_df_entries_max', guint),
                ('gui_recent_files_count_max', guint),
                ('gui_fileopen_style', guint),
                ('gui_fileopen_dir', gchar_p),
                ('gui_fileopen_preview', guint),
                ('gui_ask_unsaved', gboolean),
                ('gui_autocomplete_filter', gboolean),
                ('gui_find_wrap', gboolean),
                ('gui_window_title', gchar_p),
                ('gui_prepend_window_title', gchar_p),
                ('gui_start_title', gchar_p),
                ('gui_version_placement', version_info_e),
                ('gui_max_export_objects', guint),
                ('gui_layout_type', layout_type_e),
                ('gui_layout_content_1', layout_pane_content_e),
                ('gui_layout_content_2', layout_pane_content_e),
                ('gui_layout_content_3', layout_pane_content_e),
                ('gui_interfaces_hide_types', gchar_p),
                ('gui_interfaces_show_hidden', gboolean),
                ('gui_interfaces_remote_display', gboolean),
                ('console_log_level', gint),
                ('capture_device', gchar_p),
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
                ('capture_show_info', gboolean),
                ('capture_columns', POINTER(GList)),
                ('tap_update_interval', guint),
                ('display_hidden_proto_items', gboolean),
                ('display_byte_fileds_with_spaces', gboolean),
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

# struct _output_fields;
# typedef struct _output_fields output_fields_t;
_output_fields = None
output_fields_t = None

# struct epan_dfilter;
epan_dfilter = None

# typedef struct _color_filter {
#     gchar     *filter_name;
#     gchar     *filter_text;
#     color_t    bg_color;
#     color_t    fg_color;
#     gboolean   disabled;
#     struct epan_dfilter *c_colorfilter;
# } color_filter_t;
class _color_filter(Structure):
    _fields_ = [('filter_name', gchar_p),
                ('filter_text', gchar_p),
                ('bg_color', color_t),
                ('fg_color', color_t),
                ('disabled', gboolean),
                ('c_colorfilter', POINTER(epan_dfilter))]

color_filter_t = _color_filter

# typedef void (*color_filter_add_cb_func)(color_filter_t *colorf, gpointer user_data);
color_filter_add_cb_func = CFUNCTYPE(None, POINTER(color_filter_t), gpointer)

# typedef struct e_in6_addr {
#     guint8 bytes[16];
# } ws_in6_addr;
class e_in6_addr(Structure):
    _fields_ = [('bytes', guint8 * 16)]

ws_in6_addr = e_in6_addr

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
    _fields_ = [('num', guint32),
                ('pkt_len', guint32),
                ('cap_len', guint32),
                ('cum_bytes', guint32),
                ('file_off', gint64),
                ('pfd', POINTER(GSList)),
                ('color_filter', POINTER(_color_filter)),
                ('subnum', guint16),
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
                ('abs_ts', nstime_t),
                ('shift_offset', nstime_t),
                ('frame_ref_num', guint32),
                ('prev_dis_num', guint32)]

frame_data = _frame_data

# typedef struct _frame_data_sequence frame_data_sequence;
_frame_data_sequence = None
frame_data_sequence = None

# struct packet_provider_data {
#   wtap        *wth;
#   const frame_data *ref;
#   frame_data  *prev_dis;
#   frame_data  *prev_cap;
#   frame_data_sequence *frames;
#   GTree       *frames_user_comments;
# };
class packet_provider_data(Structure):
    _fields_ = [('wth', POINTER(wtap)),
                ('ref', POINTER(frame_data)),
                ('prev_dis', POINTER(frame_data)),
                ('prev_cap', POINTER(frame_data)),
                ('frames', POINTER(frame_data_sequence)),
                ('frames_user_comments', POINTER(GTree))]

# struct packet_provider_funcs {
# 	const nstime_t *(*get_frame_ts)(struct packet_provider_data *prov, guint32 frame_num);
# 	const char *(*get_interface_name)(struct packet_provider_data *prov, guint32 interface_id);
# 	const char *(*get_interface_description)(struct packet_provider_data *prov, guint32 interface_id);
# 	const char *(*get_user_comment)(struct packet_provider_data *prov, const frame_data *fd);
# };
class packet_provider_funcs(Structure):
    _fields_ = [('get_frame_ts', CFUNCTYPE(c_void_p,
                                           POINTER(packet_provider_data),
                                           guint32)),
                ('get_interface_name', CFUNCTYPE(c_char_p,
                                                 POINTER(packet_provider_data),
                                                 guint32)),
                ('get_interface_description', CFUNCTYPE(c_char_p,
                                                        POINTER(packet_provider_data),
                                                        guint32)),
                ('get_user_comment', CFUNCTYPE(c_char_p,
                                               POINTER(packet_provider_data),
                                               POINTER(frame_data)))]

# struct epan_session;
epan_session = None

# typedef struct epan_session epan_t;
epan_t = None

# #define COL_MAX_LEN 256
COL_MAX_LEN = 256

# #define COL_MAX_INFO_LEN 4096
COL_MAX_INFO_LEN = 4096

# #define COL_CUSTOM_PRIME_REGEX " *([^ \\|]+) *(?:(?:\\|\\|)|(?:or)| *$){1}"
COL_CUSTOM_PRIME_REGEX = b" *([^ \\|]+) *(?:(?:\\|\\|)|(?:or)| *$){1}"

# typedef struct {
#   const gchar **col_expr;
#   gchar      **col_expr_val;
# } col_expr_t;
class col_expr_t(Structure):
    _fields_ = [('col_expr', POINTER(gchar_p)),
                ('col_expr_val', POINTER(gchar_p))]

# typedef struct {
#   gint                col_fmt;
#   gboolean           *fmt_matx;
#   gchar              *col_title;
#   gchar              *col_custom_fields;
#   gint                col_custom_occurrence;
#   GSList             *col_custom_fields_ids;
#   struct epan_dfilter *col_custom_dfilter;
#   const gchar        *col_data;
#   gchar              *col_buf;
#   int                 col_fence;
#   gboolean            writable;
# } col_item_t;
class col_item_t(Structure):
    _fields_ = [('col_fmt', gint),
                ('fmt_matx', POINTER(gboolean)),
                ('col_title', gchar_p),
                ('col_custom_fields', gchar_p),
                ('col_custom_occurrence', gint),
                ('col_custom_fields_ids', POINTER(GSList)),
                ('col_custom_dfilter', POINTER(epan_dfilter)),
                ('col_data', gchar_p),
                ('col_buf', gchar_p),
                ('col_fence', c_int),
                ('writble', gboolean)]

# struct epan_column_info {
#   const struct epan_session *epan;
#   gint                num_cols;
#   col_item_t         *columns;
#   gint               *col_first;
#   gint               *col_last;
#   col_expr_t          col_expr;
#   gboolean            writable;
#   GRegex             *prime_regex;
# };
class epan_column_info(Structure):
    _fields_ = [('epan', POINTER(epan_session)),
                ('num_cols', gint),
                ('columns', POINTER(col_item_t)),
                ('col_first', POINTER(gint)),
                ('col_last', POINTER(gint)),
                ('col_expr', col_expr_t),
                ('wrtable', gboolean),
                ('prime_regex', POINTER(GRegex))]

# typedef struct epan_column_info column_info;
column_info = epan_column_info

# typedef struct {
#     gchar patt[256];
# #ifdef HAVE_SSE4_2
#     gboolean use_sse42;
#     __m128i mask;
# #endif
# } ws_mempbrk_pattern;
class ws_mempbrk_pattern(Structure):
    _fields_ = [('patt', gchar * 256),
                ('use_sse42', gboolean),
                ('mask', c_char * 16)]

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
AT_NONE = 0
AT_ETHER = 1
AT_IPv4 = 2
AT_IPv6 = 3
AT_IPX = 4
AT_FC = 5
AT_FCWWN = 6
AT_STRINGZ = 7
AT_EUI64 = 8
AT_IB = 9
AT_AX25 = 10
AT_VINES = 11
AT_END_OF_LIST = 12

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
PT_NONE = 0
PT_SCTP = 1
PT_TCP = 2
PT_UDP = 3
PT_DCCP = 4
PT_IPX = 5
PT_DDP = 6
PT_IDP = 7
PT_USB = 8
PT_I2C = 9
PT_IBQP = 10
PT_BLUETOOTH = 11

# typedef struct endpoint* endpoint_t;
endpoint = None
endpoint_t = c_void_p

# typedef struct _wmem_allocator_t wmem_allocator_t;
_wmem_allocator_t = None
wmem_allocator_t = None

# typedef enum _wmem_allocator_type_t {
#     WMEM_ALLOCATOR_SIMPLE,
#     WMEM_ALLOCATOR_BLOCK,
#     WMEM_ALLOCATOR_STRICT,
#     WMEM_ALLOCATOR_BLOCK_FAST
# } wmem_allocator_type_t;
_wmem_allocator_type_t = c_int
wmem_allocator_type_t = _wmem_allocator_type_t
WMEM_ALLOCATOR_SIMPLE = 0
WMEM_ALLOCATOR_BLOCK = 1
WMEM_ALLOCATOR_STRICT = 2
WMEM_ALLOCATOR_BLOCK_FAST = 3

# typedef struct _wmem_list_t       wmem_list_t;
_wmem_list_t = None
wmem_list_t = None

# typedef struct _wmem_list_frame_t wmem_list_frame_t;
_wmem_list_frame_t = None
wmem_list_frame_t = None

# typedef struct {
# 	guint32	addr;
# 	guint32	nmask;
# } ipv4_addr_and_mask;
class ipv4_addr_and_mask(Structure):
    _fields_ = [('addr', guint32),
                ('nmask', guint32)]

# typedef struct {
# 	ws_in6_addr addr;
# 	guint32 prefix;
# } ipv6_addr_and_prefix;
class ipv6_addr_and_prefix(Structure):
    _fields_ = [('addr', ws_in6_addr),
                ('prefix', guint32)]

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
                ('data4', guint8 * 8)]

e_guid_t = _e_guid_t

# typedef struct _ftype_t ftype_t;
_ftype_t = None
ftype_t = None

# typedef struct tvbuff tvbuff_t;
class tvbuff(Structure):
    pass

tvbuff_t = tvbuff

# enum ftenum {
#         FT_NONE,        
#         FT_PROTOCOL,
#         FT_BOOLEAN,        
#         FT_CHAR,        
#         FT_UINT8,
#         FT_UINT16,
#         FT_UINT24,        
#         FT_UINT32,
#         FT_UINT40,        
#         FT_UINT48,        
#         FT_UINT56,        
#         FT_UINT64,
#         FT_INT8,
#         FT_INT16,
#         FT_INT24,        
#         FT_INT32,
#         FT_INT40, 
#         FT_INT48, 
#         FT_INT56, 
#         FT_INT64,
#         FT_IEEE_11073_SFLOAT,
#         FT_IEEE_11073_FLOAT,
#         FT_FLOAT,
#         FT_DOUBLE,
#         FT_ABSOLUTE_TIME,
#         FT_RELATIVE_TIME,
#         FT_STRING,        
#         FT_STRINGZ,        
#         FT_UINT_STRING,        
#         FT_ETHER,
#         FT_BYTES,
#         FT_UINT_BYTES,
#         FT_IPv4,
#         FT_IPv6,
#         FT_IPXNET,
#         FT_FRAMENUM,        
#         FT_PCRE,        
#         FT_GUID,        
#         FT_OID,                
#         FT_EUI64,
#         FT_AX25,
#         FT_VINES,
#         FT_REL_OID,        
#         FT_SYSTEM_ID,
#         FT_STRINGZPAD,        
#         FT_FCWWN,
#         FT_STRINGZTRUNC,        
#         FT_NUM_TYPES 
# };
ftenum = c_int
FT_NONE = 0
FT_PROTOCOL = 1
FT_BOOLEAN = 2
FT_CHAR = 3
FT_UINT8 = 4
FT_UINT16 = 5
FT_UINT24 = 6
FT_UINT32 = 7
FT_UINT40 = 8
FT_UINT48 = 9
FT_UINT56 = 10
FT_UINT64 = 11
FT_INT8 = 12
FT_INT16 = 13
FT_INT24 = 14
FT_INT32 = 15
FT_INT40 = 16
FT_INT48 = 17
FT_INT56 = 18
FT_INT64 = 19
FT_IEEE_11073_SFLOAT = 20
FT_IEEE_11073_FLOAT = 21
FT_FLOAT = 22
FT_DOUBLE = 23
FT_ABSOLUTE_TIME = 24
FT_RELATIVE_TIME = 25
FT_STRING = 26
FT_STRINGZ = 27
FT_UINT_STRING = 28
FT_ETHER = 29
FT_BYTES = 30
FT_UINT_BYTES = 31
FT_IPv4 = 32
FT_IPv6 = 33
FT_IPXNET = 34
FT_FRAMENUM = 35
FT_PCRE = 36
FT_GUID = 37
FT_OID = 38
FT_EUI64 = 39
FT_AX25 = 40
FT_VINES = 41
FT_REL_OID = 42
FT_SYSTEM_ID = 43
FT_STRINGZPAD = 44
FT_FCWWN = 45
FT_STRINGZTRUNC = 46
FT_NUM_TYPES = 47

# typedef enum ftenum ftenum_t;
ftenum_t = ftenum

# typedef struct _protocol_value_t
# {
#         tvbuff_t        *tvb;
#         gchar                *proto_string;
# } protocol_value_t;
class _protocol_value_t(Structure):
    _fields_ = [('tvb', POINTER(tvbuff_t)),
                ('proto_string', gchar_p)]

protocol_value_t = _protocol_value_t

# typedef struct _fvalue_t {
#         ftype_t        *ftype;
#         union {
#                 guint32                        uinteger;
#                 gint32                        sinteger;
#                 guint64                        integer64;
#                 guint64                        uinteger64;
#                 gint64                        sinteger64;
#                 gdouble                        floating;
#                 gchar                        *string;
#                 guchar                        *ustring;
#                 GByteArray                *bytes;
#                 ipv4_addr_and_mask        ipv4;
#                 ipv6_addr_and_prefix        ipv6;
#                 e_guid_t                guid;
#                 nstime_t                time;
#                 protocol_value_t         protocol;
#                 GRegex                        *re;
#                 guint16                        sfloat_ieee_11073;
#                 guint32                        float_ieee_11073;
#         } value;
#         gboolean        fvalue_gboolean1;
# } fvalue_t;
class _fvalue_t_value(Union):
    _fields_ = [('uinteger', guint32),
                ('sinteger', gint32),
                ('integer64', guint64),
                ('uinteger64', guint64),
                ('sinteger64', gint64),
                ('floating', gdouble),
                ('string', gchar_p),
                ('ustring', POINTER(guchar)),
                ('bytes', POINTER(GByteArray)),
                ('ipv4', ipv4_addr_and_mask),
                ('ipv6', ipv6_addr_and_prefix),
                ('guid', e_guid_t),
                ('time', nstime_t),
                ('protocol', protocol_value_t),
                ('re', POINTER(GRegex)),
                ('sfloat_ieee_11073', guint16),
                ('float_ieee_11073', guint32)]

class _fvalue_t(Structure):
    _fields_ = [('ftype', POINTER(ftype_t)),
                ('value', _fvalue_t_value),
                ('fvalue_gboolean1', gboolean)]

fvalue_t = _fvalue_t

# typedef enum {
#     HF_REF_TYPE_NONE,
#     HF_REF_TYPE_INDIRECT,
#     HF_REF_TYPE_DIRECT
# } hf_ref_type;
hf_ref_type = c_int
HF_REF_TYPE_NONE = 0
HF_REF_TYPE_INDIRECT = 1
HF_REF_TYPE_DIRECT = 2

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
                               ('bitmask', guint64),
                               ('blurb', c_char_p),
                               ('id', c_int),
                               ('parent', c_int),
                               ('ref_type', hf_ref_type),
                               ('same_name_prev_id', c_int),
                               ('same_name_next', POINTER(header_field_info))]

# #define ITEM_LABEL_LENGTH       240
ITEM_LABEL_LENGTH = 240

# typedef struct _item_label_t {
#     char representation[ITEM_LABEL_LENGTH];
# } item_label_t;
class _item_label_t(Structure):
    _fields_ = [('representation', c_char * ITEM_LABEL_LENGTH)]

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
    _fields_ = [('hfinfo', POINTER(header_field_info)),
                ('start', gint),
                ('length', gint),
                ('appendix_start', gint),
                ('appendix_length', gint),
                ('tree_type', gint),
                ('flags', guint32),
                ('rep', POINTER(item_label_t)),
                ('ds_tvb', POINTER(tvbuff_t)),
                ('value', fvalue_t)]

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
    _fields_ = [('in_error_pkt', guint32, 1),
                ('in_gre_pkt', guint32, 1)]

class _packet_info(Structure):
    _fields_ = [('current_proto', c_char_p),
                ('cinfo', POINTER(epan_column_info)),
                ('presence_flags', guint32),
                ('num', guint32),
                ('abs_ts', nstime_t),
                ('rel_ts', nstime_t),
                ('fd', POINTER(frame_data)),
                ('pseudo_header', POINTER(wtap_pseudo_header)),
                ('rec', POINTER(wtap_rec)),
                ('data_src', POINTER(GSList)),
                ('dl_src', address),
                ('dl_dst', address),
                ('net_src', address),
                ('net_dst', address),
                ('src', address),
                ('dst', address),
                ('vlan_id', guint32),
                ('noreassembly_reason', c_char_p),
                ('fragmented', gboolean),
                ('flags', _packet_info_flags),
                ('ptype', port_type),
                ('srcport', guint32),
                ('destport', guint32),
                ('match_uint', guint32),
                ('use_endpoint', gboolean),
                ('conv_endpoint', POINTER(endpoint)),
                ('can_desegment', guint16),
                ('saved_can_desegment', guint16),
                ('desegment_offset', c_int),
                ('desegment_len', guint32),
                ('want_pdu_tracking', guint16),
                ('bytes_until_next_pdu', guint32),
                ('p2p_dir', c_int),
                ('private_table', POINTER(GHashTable)),
                ('layers', POINTER(wmem_list_t)),
                ('curr_layer_num', guint8),
                ('link_number', guint16),
                ('clnp_srcref', guint16),
                ('clnp_dstref', guint16),
                ('link_dir', c_int),
                ('proto_data', POINTER(GSList)),
                ('dependent_frames', POINTER(GSList)),
                ('frame_end_routines', POINTER(GSList)),
                ('pool', POINTER(wmem_allocator_t)),
                ('epan', POINTER(epan_session)),
                ('heur_list_name', gchar_p)]

packet_info = _packet_info

# #define FI_HIDDEN               0x00000001
FI_HIDDEN = 0x00000001

# #define FI_URL                  0x00000004
FI_URL = 0x00000004

# #define FI_LITTLE_ENDIAN        0x00000008
FI_LITTLE_ENDIAN = 0x00000008

# #define FI_BIG_ENDIAN           0x00000010
FI_BIG_ENDIAN = 0x00000010

# #define FI_BITS_OFFSET(n)       (((n) & 7) << 5)
def FI_BITS_OFFSET(n):
    return (n & 7) << 5

# #define FI_BITS_SIZE(n)         (((n) & 63) << 8)
def FI_BITS_SIZE(n):
    return (n & 63) << 8

# #define FI_VARINT               0x00004000
FI_VARINT = 0x00004000

# #define FI_GET_FLAG(fi, flag)   ((fi) ? ((fi)->flags & (flag)) : 0)
def FI_GET_FLAG(fi, flag):
    if fi.value == 0:
        return 0
    else:
        return fi[0].flags & flag

# #define FI_SET_FLAG(fi, flag) \
#     do { \
#       if (fi) \
#         (fi)->flags = (fi)->flags | (flag); \
#     } while(0)
def FI_SET_FLAG(fi, flag):
    if fi.value != 0:
        fi[0].flags = fi[0].flags | flag

# #define FI_RESET_FLAG(fi, flag) \
#     do { \
#       if (fi) \
#         (fi)->flags = (fi)->flags & ~(flag); \
#     } while(0)
def FI_RESET_FLAG(fi, flag):
    if fi.value == 0:
        fi[0].flags = fi[0].flags & ~flag

# #define FI_GET_BITS_OFFSET(fi) (FI_GET_FLAG(fi, FI_BITS_OFFSET(7)) >> 5)
def FI_GET_BITS_OFFSET(fi):
    return FI_GET_FLAG(fi, FI_BITS_OFFSET(7)) >> 5

# #define FI_GET_BITS_SIZE(fi)   (FI_GET_FLAG(fi, FI_BITS_SIZE(63)) >> 8)
def FI_GET_BITS_SIZE(fi):
    return FI_GET_FLAG(fi, FI_BITS_SIZE(63)) >> 8

# typedef struct {
#     GHashTable          *interesting_hfids;
#     gboolean             visible;
#     gboolean             fake_protocols;
#     gint                 count;
#     struct _packet_info *pinfo;
# } tree_data_t;
class tree_data_t(Structure):
    _fields_ = [('interesting_hfids', POINTER(GHashTable)),
                ('visible', gboolean),
                ('fake_protocols', gboolean),
                ('count', gint),
                ('pinfo', POINTER(_packet_info))]

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

# struct tvb_ops {
#         gsize tvb_size;
#         void (*tvb_free)(struct tvbuff *tvb);
#         guint (*tvb_offset)(const struct tvbuff *tvb, guint counter);
#         const guint8 *(*tvb_get_ptr)(struct tvbuff *tvb, guint abs_offset, guint abs_length);
#         void *(*tvb_memcpy)(struct tvbuff *tvb, void *target, guint offset, guint length);

#         gint (*tvb_find_guint8)(tvbuff_t *tvb, guint abs_offset, guint limit, guint8 needle);
#         gint (*tvb_ws_mempbrk_pattern_guint8)(tvbuff_t *tvb, guint abs_offset, guint limit, const ws_mempbrk_pattern* pattern, guchar *found_needle);

#         tvbuff_t *(*tvb_clone)(tvbuff_t *tvb, guint abs_offset, guint abs_length);
# };
class tvb_ops(Structure):
    _fields_ = [('tvb_size', gsize),
                ('tvb_free', CFUNCTYPE(None, POINTER(tvbuff))),
                ('tvb_offset', CFUNCTYPE(guint, POINTER(tvbuff), guint)),
                ('tvb_get_ptr', CFUNCTYPE(c_void_p,
                                          POINTER(tvbuff),
                                          guint,
                                          guint)),
                ('tvb_memcpy', CFUNCTYPE(c_void_p,
                                         POINTER(tvbuff),
                                         c_void_p,
                                         guint,
                                         guint)),
                ('tvb_find_guint8', CFUNCTYPE(gint,
                                              POINTER(tvbuff_t),
                                              guint,
                                              guint,
                                              guint8)),
                ('tvb_ws_mempbrk_pattern_guint8', CFUNCTYPE(gint,
                                                            POINTER(tvbuff_t),
                                                            guint,
                                                            guint,
                                                            POINTER(ws_mempbrk_pattern),
                                                            POINTER(guchar))),
                ('tvb_clone', CFUNCTYPE(c_void_p,
                                        POINTER(tvbuff_t),
                                        guint,
                                        guint))]


# struct tvbuff {
#         tvbuff_t                *next;
#         const struct tvb_ops   *ops;
#         gboolean                initialized;
#         guint                        flags;
#         struct tvbuff                *ds_tvb;
#         const guint8                *real_data;
#         guint                        length;
#         guint                        reported_length;
#         guint                        contained_length;
#         gint                        raw_offset;
# };
tvbuff._fields_ = [('next', POINTER(tvbuff_t)),
                   ('ops', POINTER(tvb_ops)),
                   ('initialized', gboolean),
                   ('flags', guint),
                   ('ds_tvb', POINTER(tvbuff)),
                   ('real_data', POINTER(guint8)),
                   ('length', guint),
                   ('reported_length', guint),
                   ('contained_length', guint),
                   ('raw_offset', gint)]

# struct epan_dissect {
#         struct epan_session *session;
#         tvbuff_t        *tvb;
#         proto_tree        *tree;
#         packet_info        pi;
# };
class epan_dissect(Structure):
    _fields_ = [('session', POINTER(epan_session)),
                ('tvb', POINTER(tvbuff_t)),
                ('tree', POINTER(proto_tree)),
                ('pi', packet_info)]

# typedef struct epan_dissect epan_dissect_t;
epan_dissect_t = epan_dissect

# typedef gboolean (*subtype_read_func)(struct wtap*, wtap_rec *,
#                                       Buffer *, int *, char **, gint64 *);
subtype_read_func = CFUNCTYPE(gboolean, POINTER(wtap),
                                        POINTER(wtap_rec),
                                        POINTER(Buffer),
                                        POINTER(c_int),
                                        POINTER(c_char_p),
                                        POINTER(gint64))

# typedef gboolean (*subtype_seek_read_func)(struct wtap*, gint64, wtap_rec *,
#                                            Buffer *, int *, char **);
subtype_seek_read_func = CFUNCTYPE(gboolean, POINTER(wtap),
                                             gint64,
                                             POINTER(wtap_rec),
                                             POINTER(Buffer),
                                             POINTER(c_int),
                                             POINTER(c_char_p))

# struct wtap {
#     FILE_T                      fh;
#     FILE_T                      random_fh;
#     gboolean                    ispipe;
#     int                         file_type_subtype;
#     guint                       snapshot_length;
#     GArray                      *shb_hdrs;
#     GArray                      *interface_data;
#     guint                       next_interface_data;
#     GArray                      *nrb_hdrs;
#     GArray                      *dsbs;
#     void                        *priv;
#     void                        *wslua_data;
#     subtype_read_func           subtype_read;
#     subtype_seek_read_func      subtype_seek_read;
#     void                        (*subtype_sequential_close)(struct wtap*);
#     void                        (*subtype_close)(struct wtap*);
#     int                         file_encap;
#     int                         file_tsprec;
#     wtap_new_ipv4_callback_t    add_new_ipv4;
#     wtap_new_ipv6_callback_t    add_new_ipv6;
#     wtap_new_secrets_callback_t add_new_secrets;
#     GPtrArray                   *fast_seek;
# };
wtap._fields_ = [('fh', FILE_T),
                 ('random_fh', FILE_T),
                 ('ispipe', gboolean),
                 ('file_type_subtype', c_int),
                 ('snapshot_length', guint),
                 ('shb_hdrs', POINTER(GArray)),
                 ('interface_data', POINTER(GArray)),
                 ('net_interface_data', guint),
                 ('nrb_hdrs', POINTER(GArray)),
                 ('dsbs', POINTER(GArray)),
                 ('priv', c_void_p),
                 ('wslua_data', c_void_p),
                 ('subtype_read', subtype_read_func),
                 ('subtype_seek_read', subtype_seek_read_func),
                 ('subtype_sequential_close', CFUNCTYPE(None, POINTER(wtap))),
                 ('subtype_close', CFUNCTYPE(None, POINTER(wtap))),
                 ('file_encap', c_int),
                 ('file_tsprec', c_int),
                 ('add_new_ipv4', wtap_new_ipv4_callback_t),
                 ('add_new_ipv6', wtap_new_ipv6_callback_t),
                 ('add_new_secrets', wtap_new_secrets_callback_t),
                 ('fast_seek', POINTER(GPtrArray))]

# typedef struct wtap_block *wtap_block_t;
wtap_block = None
wtap_block_t = c_void_p

# typedef enum {
#     WTAP_BLOCK_NG_SECTION = 0,
#     WTAP_BLOCK_IF_DESCR,
#     WTAP_BLOCK_NG_NRB,
#     WTAP_BLOCK_IF_STATS,
#     WTAP_BLOCK_DSB,
#     WTAP_BLOCK_END_OF_LIST
# } wtap_block_type_t;
wtap_block_type_t = c_int
WTAP_BLOCK_NG_SECTION = 0
WTAP_BLOCK_IF_DESCR = 1
WTAP_BLOCK_NG_NRB = 2
WTAP_BLOCK_IF_STATS = 3
WTAP_BLOCK_DSB = 4
WTAP_BLOCK_END_OF_LIST = 5

# typedef enum {
#     WTAP_OPTTYPE_UINT8,
#     WTAP_OPTTYPE_UINT64,
#     WTAP_OPTTYPE_STRING,
#     WTAP_OPTTYPE_IPv4,
#     WTAP_OPTTYPE_IPv6,
#     WTAP_OPTTYPE_CUSTOM
# } wtap_opttype_e;
wtap_opttype_e = c_int
WTAP_OPTTYPE_UINT8 = 0
WTAP_OPTTYPE_UINT64 = 1
WTAP_OPTTYPE_STRING = 2
WTAP_OPTTYPE_IPv4 = 3
WTAP_OPTTYPE_IPv6 = 4
WTAP_OPTTYPE_CUSTOM = 5

# typedef enum {
#     WTAP_OPTTYPE_SUCCESS = 0,
#     WTAP_OPTTYPE_NO_SUCH_OPTION = -1,
#     WTAP_OPTTYPE_NOT_FOUND = -2,
#     WTAP_OPTTYPE_TYPE_MISMATCH = -3,
#     WTAP_OPTTYPE_NUMBER_MISMATCH = -4,
#     WTAP_OPTTYPE_ALREADY_EXISTS = -5
# } wtap_opttype_return_val;
wtap_opttype_return_val = c_int
WTAP_OPTTYPE_SUCCESS = 0
WTAP_OPTTYPE_NO_SUCH_OPTION = -1
WTAP_OPTTYPE_NOT_FOUND = -2
WTAP_OPTTYPE_TYPE_MISMATCH = -3
WTAP_OPTTYPE_NUMBER_MISMATCH = -4
WTAP_OPTTYPE_ALREADY_EXISTS = -5

# #define OPT_EOFOPT           0
OPT_EOFOPT = 0

# #define OPT_COMMENT          1
OPT_COMMENT = 1

# #define OPT_SHB_HARDWARE     2
OPT_SHB_HARDWARE = 2

# #define OPT_SHB_OS           3
OPT_SHB_OS = 3

# #define OPT_SHB_USERAPPL     4
OPT_SHB_USERAPPL = 4

# #define OPT_IDB_NAME         2
OPT_IDB_NAME = 2

# #define OPT_IDB_DESCR        3
OPT_IDB_DESCR = 3

# #define OPT_IDB_IP4ADDR      4
OPT_IDB_IP4ADDR = 4

# #define OPT_IDB_IP6ADDR      5
OPT_IDB_IP6ADDR = 5

# #define OPT_IDB_MACADDR      6
OPT_IDB_MACADDR = 6

# #define OPT_IDB_EUIADDR      7
OPT_IDB_EUIADDR = 7

# #define OPT_IDB_SPEED        8
OPT_IDB_SPEED = 8

# #define OPT_IDB_TSRESOL      9
OPT_IDB_TSRESOL = 9

# #define OPT_IDB_TZONE        10
OPT_IDB_TZONE = 10

# #define OPT_IDB_FILTER       11
OPT_IDB_FILTER = 11

# #define OPT_IDB_OS           12
OPT_IDB_OS = 12

# #define OPT_IDB_FCSLEN       13
OPT_IDB_FCSLEN = 13

# #define OPT_IDB_TSOFFSET     14
OPT_IDB_TSOFFSET = 14

# #define OPT_IDB_HARDWARE     15
OPT_IDB_HARDWARE = 15

# #define OPT_NS_DNSNAME       2
OPT_NS_DNSNAME = 2

# #define OPT_NS_DNSIP4ADDR    3
OPT_NS_DNSIP4ADDR = 3

# #define OPT_NS_DNSIP6ADDR    4
OPT_NS_DNSIP6ADDR = 4

# #define OPT_ISB_STARTTIME    2
OPT_ISB_STARTTIME = 2

# #define OPT_ISB_ENDTIME      3
OPT_ISB_ENDTIME = 3

# #define OPT_ISB_IFRECV       4
OPT_ISB_IFRECV = 4

# #define OPT_ISB_IFDROP       5
OPT_ISB_IFDROP = 5

# #define OPT_ISB_FILTERACCEPT 6
OPT_ISB_FILTERACCEPT = 6

# #define OPT_ISB_OSDROP       7
OPT_ISB_OSDROP = 7

# #define OPT_ISB_USRDELIV     8
OPT_ISB_USRDELIV = 8

# enum ftrepr {
# 	FTREPR_DISPLAY,
# 	FTREPR_DFILTER
# };
ftrepr = c_int
FTREPR_DISPLAY = 0
FTREPR_DFILTER = 1

# typedef enum ftrepr ftrepr_t;
ftrepr_t = c_int

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
BASE_NONE = 0
BASE_DEC = 1
BASE_HEX = 2
BASE_OCT = 3
BASE_DEC_HEX = 4
BASE_HEX_DEC = 5
BASE_CUSTOM = 6
BASE_FLOAT = BASE_NONE
STR_ASCII = 0
STR_UNICODE = 7
SEP_DOT = 8
SEP_DASH = 9
SEP_COLON = 10
SEP_SPACE = 11
BASE_NETMASK = 12
BASE_PT_UDP = 13
BASE_PT_TCP = 14
BASE_PT_DCCP = 15
BASE_PT_SCTP = 16
BASE_OUI = 17

# typedef enum {
# 	TAP_PACKET_DONT_REDRAW,
# 	TAP_PACKET_REDRAW,
# 	TAP_PACKET_FAILED
# } tap_packet_status;
tap_packet_status = c_int
TAP_PACKET_DONT_REDRAW = 0
TAP_PACKET_REDRAW = 1
TAP_PACKET_FAILED = 2

# typedef void (*tap_reset_cb)(void *tapdata);
tap_reset_cb = CFUNCTYPE(None, c_void_p)

# typedef tap_packet_status (*tap_packet_cb)(void *tapdata, packet_info *pinfo, epan_dissect_t *edt, const void *data);
tap_packet_cb = CFUNCTYPE(tap_packet_status,
                          c_void_p,
                          POINTER(packet_info),
                          POINTER(epan_dissect_t),
                          c_void_p)

# typedef void (*tap_draw_cb)(void *tapdata);
tap_draw_cb = CFUNCTYPE(None, c_void_p)

# typedef void (*tap_finish_cb)(void *tapdata);
tap_finish_cb = CFUNCTYPE(None, c_void_p)

# #define TL_REQUIRES_NOTHING	0x00000000
TL_REQUIRES_NOTHING = 0x00000000

# #define TL_REQUIRES_PROTO_TREE	0x00000001
TL_REQUIRES_PROTO_TREE = 0x00000001

# #define TL_REQUIRES_COLUMNS	0x00000002
TL_REQUIRES_COLUMNS = 0x00000002

# #define TL_REQUIRES_ERROR_PACKETS	0x00000004
TL_REQUIRES_ERROR_PACKETS = 0x00000004

# #define TL_IS_DISSECTOR_HELPER	0x00000008
TL_IS_DISSECTOR_HELPER = 0x00000008

# typedef struct {
# 	void (*register_tap_listener)(void);
# } tap_plugin;
class tap_plugin(Structure):
    _fields_ = [('register_tap_listener', CFUNCTYPE(None))]

# typedef enum {
#   TCP_STREAM = 0,
#   UDP_STREAM,
#   MAX_STREAM
# } stream_type;
stream_type = c_int
TCP_STREAM = 0
UDP_STREAM = 1
MAX_STREAM = 2

# typedef enum {
#     FRS_OK,
#     FRS_OPEN_ERROR,
#     FRS_READ_ERROR,
#     FRS_PRINT_ERROR
# } frs_return_t;
frs_return_t = c_int
FRS_OK = 0
FRS_OPEN_ERROR = 1
FRS_READ_ERROR = 2
FRS_PRINT_ERROR = 3

# typedef enum {
#     FOLLOW_TCP,
#     FOLLOW_TLS,
#     FOLLOW_UDP,
#     FOLLOW_HTTP,
#     FOLLOW_HTTP2,
#     FOLLOW_QUIC,
# } follow_type_t;
follow_type_t = c_int
FOLLOW_TCP = 0
FOLLOW_TLS = 1
FOLLOW_UDP = 2
FOLLOW_HTTP = 3
FOLLOW_HTTP2 = 4
FOLLOW_QUIC = 5

# typedef enum {
#     SHOW_ASCII,
#     SHOW_CARRAY,
#     SHOW_EBCDIC,
#     SHOW_HEXDUMP,
#     SHOW_RAW,
#     SHOW_CODEC, 
#     SHOW_YAML
# } show_type_t;
show_type_t = c_int
SHOW_ASCII = 0
SHOW_CARRAY = 1
SHOW_EBCDIC = 2
SHOW_HEXDUMP = 3
SHOW_RAW = 4
SHOW_CODEC = 5
SHOW_YAML = 6

# typedef enum {
#     FROM_CLIENT,
#     FROM_SERVER,
#     BOTH_HOSTS
# } show_stream_t;
show_stream_t = c_int
FROM_CLIENT = 0
FROM_SERVER = 1
BOTH_HOSTS = 2

# typedef union _stream_addr {
#   guint32 ipv4;
#   ws_in6_addr ipv6;
# } stream_addr;
class _stream_addr(Union):
    _fields_ = [('ipv4', guint32),
                ('ipv6', ws_in6_addr)]

stream_addr = _stream_addr

# struct _follow_info;
class _follow_info(Structure):
    pass


# typedef gboolean (*follow_print_line_func)(char *, size_t, gboolean, void *);
follow_print_line_func = CFUNCTYPE(gboolean,
                                   c_char_p,
                                   c_size_t,
                                   gboolean,
                                   c_void_p)

# typedef frs_return_t (*follow_read_stream_func)(struct _follow_info *follow_info, follow_print_line_func follow_print, void *arg);
follow_read_stream_func = CFUNCTYPE(frs_return_t,
                                    POINTER(_follow_info),
                                    follow_print_line_func,
                                    c_void_p)

# typedef struct {
#     gboolean is_server;
#     guint32 packet_num;
#     guint32 seq;
#     GByteArray *data;
# } follow_record_t;
class follow_record_t(Structure):
    _fields_ = [('is_server', gboolean),
                ('packet_num', guint32),
                ('seq', guint32),
                ('data', POINTER(GByteArray))]


# typedef struct _follow_info {
#     show_stream_t   show_stream;
#     char            *filter_out_filter;
#     GList           *payload;
#     guint           bytes_written[2];
#     guint32         seq[2];
#     GList           *fragments[2];
#     guint           client_port;
#     guint           server_port;
#     address         client_ip;
#     address         server_ip;
#     void*           gui_data;
# } follow_info_t;
_follow_info._fields_ = [('show_stream', show_stream_t),
                         ('filter_out_filter', c_char_p),
                         ('payload', POINTER(GList)),
                         ('bytes_written', guint * 2),
                         ('seq', guint32 * 2),
                         ('fragments', POINTER(GList) * 2),
                         ('client_port', guint),
                         ('server_port', guint),
                         ('client_ip', address),
                         ('server_ip', address),
                         ('gui_data', c_void_p)]

follow_info_t = _follow_info

# struct register_follow;
# typedef struct register_follow register_follow_t;
class register_follow(Structure):
    _fields_ = []

register_follow_t = register_follow

# typedef gchar* (*follow_conv_filter_func)(packet_info *pinfo, guint *stream, guint *sub_stream);
follow_conv_filter_func = CFUNCTYPE(gchar_p,
                                    POINTER(packet_info),
                                    POINTER(guint),
                                    POINTER(guint))

# typedef gchar* (*follow_index_filter_func)(guint stream, guint sub_stream);
follow_index_filter_func = CFUNCTYPE(gchar_p, guint, guint)

# typedef gchar* (*follow_address_filter_func)(address* src_addr, address* dst_addr, int src_port, int dst_port);
follow_address_filter_func = CFUNCTYPE(gchar_p,
                                       POINTER(address),
                                       POINTER(address),
                                       c_int,
                                       c_int)

# typedef gchar* (*follow_port_to_display_func)(wmem_allocator_t *allocator, guint port);
follow_port_to_display_func = CFUNCTYPE(gchar_p,
                                        POINTER(wmem_allocator_t),
                                        guint)

# typedef gboolean (*wmem_foreach_func)(const void *key, void *value,
#                                       void *userdata);
wmem_foreach_func = CFUNCTYPE(gboolean, c_void_p, c_void_p, c_void_p)

# typedef struct _protocol protocol_t;
_protocol = None
protocol_t = None

# #define WTAP_ERR_NOT_REGULAR_FILE              -1
WTAP_ERR_NOT_REGULAR_FILE = -1

# #define WTAP_ERR_RANDOM_OPEN_PIPE              -2
WTAP_ERR_RANDOM_OPEN_PIPE = -2

# #define WTAP_ERR_FILE_UNKNOWN_FORMAT           -3
WTAP_ERR_FILE_UNKNOWN_FORMAT = -3

# #define WTAP_ERR_UNSUPPORTED                   -4
WTAP_ERR_UNSUPPORTED = -4

# #define WTAP_ERR_CANT_WRITE_TO_PIPE            -5
WTAP_ERR_CANT_WRITE_TO_PIPE = -5

# #define WTAP_ERR_CANT_OPEN                     -6
WTAP_ERR_CANT_OPEN = -6

# #define WTAP_ERR_UNWRITABLE_FILE_TYPE          -7
WTAP_ERR_UNWRITABLE_FILE_TYPE = -7

# #define WTAP_ERR_UNWRITABLE_ENCAP              -8
WTAP_ERR_UNWRITABLE_ENCAP = -8

# #define WTAP_ERR_ENCAP_PER_PACKET_UNSUPPORTED  -9
WTAP_ERR_ENCAP_PER_PACKET_UNSUPPORTED = -9

# #define WTAP_ERR_CANT_WRITE                   -10
WTAP_ERR_CANT_WRITE = -10

# #define WTAP_ERR_CANT_CLOSE                   -11
WTAP_ERR_CANT_CLOSE = -11

# #define WTAP_ERR_SHORT_READ                   -12
WTAP_ERR_SHORT_READ = -12

# #define WTAP_ERR_BAD_FILE                     -13
WTAP_ERR_BAD_FILE = -13

# #define WTAP_ERR_SHORT_WRITE                  -14
WTAP_ERR_SHORT_WRITE = -14

# #define WTAP_ERR_UNC_OVERFLOW                 -15
WTAP_ERR_UNC_OVERFLOW = -15

# #define WTAP_ERR_RANDOM_OPEN_STDIN            -16
WTAP_ERR_RANDOM_OPEN_STDIN = -16

# #define WTAP_ERR_COMPRESSION_NOT_SUPPORTED    -17
WTAP_ERR_COMPRESSION_NOT_SUPPORTED = -17

# #define WTAP_ERR_CANT_SEEK                    -18
WTAP_ERR_CANT_SEEK = -18

# #define WTAP_ERR_CANT_SEEK_COMPRESSED         -19
WTAP_ERR_CANT_SEEK_COMPRESSED = -19

# #define WTAP_ERR_DECOMPRESS                   -20
WTAP_ERR_DECOMPRESS = -20

# #define WTAP_ERR_INTERNAL                     -21
WTAP_ERR_INTERNAL = -21

# #define WTAP_ERR_PACKET_TOO_LARGE             -22
WTAP_ERR_PACKET_TOO_LARGE = -22

# #define WTAP_ERR_CHECK_WSLUA                  -23
WTAP_ERR_CHECK_WSLUA = -23

# #define WTAP_ERR_UNWRITABLE_REC_TYPE          -24
WTAP_ERR_UNWRITABLE_REC_TYPE = -24

# #define WTAP_ERR_UNWRITABLE_REC_DATA          -25
WTAP_ERR_UNWRITABLE_REC_DATA = -25

# #define WTAP_ERR_DECOMPRESSION_NOT_SUPPORTED  -26
WTAP_ERR_DECOMPRESSION_NOT_SUPPORTED = -26

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
epan_uat = None

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
layout_unused = 0
layout_type_5 = 1
layout_type_2 = 2
layout_type_1 = 3
layout_type_4 = 4
layout_type_3 = 5
layout_type_6 = 6
layout_type_max = 7

# typedef enum {
#     layout_pane_content_none,
#     layout_pane_content_plist,
#     layout_pane_content_pdetails,
#     layout_pane_content_pbytes,
#     layout_pane_content_pdiagram,
# } layout_pane_content_e;
layout_pane_content_e = c_int
layout_pane_content_none = 0
layout_pane_content_plist = 1
layout_pane_content_pdetails = 2
layout_pane_content_pbytes = 3
layout_pane_content_pdiagram = 4

# typedef enum {
#     console_open_never,
#     console_open_auto,
#     console_open_always
# } console_open_e;
console_open_e = c_int
console_open_never = 0
console_open_auto = 1
console_open_always = 2

# typedef enum {
#     version_welcome_only,
#     version_title_only,
#     version_both,
#     version_neither
# } version_info_e;
version_info_e = c_int
version_welcome_only = 0
version_title_only = 1
version_both = 2
version_neither = 3

# typedef enum {
#     pref_default,
#     pref_stashed,
#     pref_current
# } pref_source_t;
pref_source_t = c_int
pref_default = 0
pref_stashed = 1
pref_current = 2

# typedef enum {
#     ELIDE_LEFT,
#     ELIDE_RIGHT,
#     ELIDE_MIDDLE,
#     ELIDE_NONE
# } elide_mode_e;
elide_mode_e = c_int
ELIDE_LEFT = 0
ELIDE_RIGHT = 1
ELIDE_MIDDLE = 2
ELIDE_NONE = 3

# typedef enum {
#     UPDATE_CHANNEL_DEVELOPMENT,
#     UPDATE_CHANNEL_STABLE
# } software_update_channel_e;
software_update_channel_e = c_int
UPDATE_CHANNEL_DEVELOPEMENT = 0
UPDATE_CHANNEL_STABLE = 1

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
                ('gui_colorized_fg', color_t),
                ('gui_colorized_bg', color_t),
                ('gui_geometry_save_position', gboolean),
                ('gui_geometry_save_size', gboolean),
                ('gui_geometry_save_maximized', gboolean),
                ('gui_console_open', console_open_e),
                ('gui_recent_df_entries_max', guint),
                ('gui_recent_files_count_max', guint),
                ('gui_fileopen_style', guint),
                ('gui_fileopen_dir', gchar_p),
                ('gui_fileopen_preview', guint),
                ('gui_ask_unsaved', gboolean),
                ('gui_autocomplete_filter', gboolean),
                ('gui_find_wrap', gboolean),
                ('gui_window_title', gchar_p),
                ('gui_prepend_window_title', gchar_p),
                ('gui_start_title', gchar_p),
                ('gui_version_placement', version_info_e),
                ('gui_max_export_objects', guint),
                ('gui_layout_type', layout_type_e),
                ('gui_layout_content_1', layout_pane_content_e),
                ('gui_layout_content_2', layout_pane_content_e),
                ('gui_layout_content_3', layout_pane_content_e),
                ('gui_interfaces_hide_types', gchar_p),
                ('gui_interfaces_show_hidden', gboolean),
                ('gui_interfaces_remote_display', gboolean),
                ('console_log_level', gint),
                ('capture_device', gchar_p),
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
                ('capture_show_info', gboolean),
                ('capture_columns', POINTER(GList)),
                ('tap_update_interval', guint),
                ('display_hidden_proto_items', gboolean),
                ('display_byte_fileds_with_spaces', gboolean),
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

# typedef struct _wmem_tree_t wmem_tree_t;
_wmem_tree_t = None
wmem_tree_t = None

# struct pref_module {
#     const char *name;
#     const char *title;
#     const char *description;
#     void (*apply_cb)(void);
#     GList *prefs;
#     struct pref_module *parent;
#     wmem_tree_t *submodules;
#     int numprefs;
#     unsigned int prefs_changed_flags;
#     gboolean obsolete;
#     gboolean use_gui;
#     unsigned int effect_flags;
# };
class pref_module(Structure):
    pass

pref_module._fields_ = [('name', c_char_p),
                        ('title', c_char_p),
                        ('description', c_char_p),
                        ('apply_cb', CFUNCTYPE(None)),
                        ('prefs', POINTER(GList)),
                        ('parent', POINTER(pref_module)),
                        ('submodules', POINTER(wmem_tree_t)),
                        ('numprefs', c_int),
                        ('prefs_changed_flags', c_uint),
                        ('obsolete', gboolean),
                        ('use_gui', gboolean),
                        ('effect_flags', c_uint)]

# typedef struct pref_module module_t;
module_t = pref_module

# typedef guint (*module_cb)(module_t *module, gpointer user_data);
module_cb = CFUNCTYPE(guint, POINTER(module_t), gpointer)

# typedef struct preference pref_t;
preference = None
pref_t = None

# typedef enum {
#     PREFS_SET_OK,
#     PREFS_SET_SYNTAX_ERR,
#     PREFS_SET_NO_SUCH_PREF,
#     PREFS_SET_OBSOLETE
# } prefs_set_pref_e;
prefs_set_pref_e = c_int
PREFS_SET_OK = 0
PREFS_SET_SYNTAX_ERR = 1
PREFS_SET_NO_SUCH_PREF = 2
PREFS_SET_OBSOLETE = 3

# typedef void (*pref_custom_free_cb) (pref_t* pref);
pref_custom_free_cb = CFUNCTYPE(None, POINTER(pref_t))

# typedef void (*pref_custom_reset_cb) (pref_t* pref);
pref_custom_reset_cb = CFUNCTYPE(None, POINTER(pref_t))

# typedef prefs_set_pref_e (*pref_custom_set_cb) (pref_t* pref, const gchar* value, unsigned int* changed_flags);
pref_custom_set_cb = CFUNCTYPE(prefs_set_pref_e, POINTER(pref_t),
                                                 gchar_p,
                                                 POINTER(c_uint))

# typedef const char * (*pref_custom_type_name_cb) (void);
pref_custom_type_name_cb = CFUNCTYPE(c_char_p)

# typedef char * (*pref_custom_type_description_cb) (void);
pref_custom_type_description_cb = CFUNCTYPE(c_char_p)

# typedef gboolean (*pref_custom_is_default_cb) (pref_t* pref);
pref_custom_is_default_cb = CFUNCTYPE(gboolean, POINTER(pref_t))

# typedef char * (*pref_custom_to_str_cb) (pref_t* pref, gboolean default_val);
pref_custom_to_str_cb = CFUNCTYPE(c_char_p, POINTER(pref_t), gboolean)

# struct pref_custom_cbs {
#     pref_custom_free_cb free_cb;
#     pref_custom_reset_cb reset_cb;
#     pref_custom_set_cb set_cb;
#     pref_custom_type_name_cb type_name_cb;
#     pref_custom_type_description_cb type_description_cb;
#     pref_custom_is_default_cb is_default_cb;
#     pref_custom_to_str_cb to_str_cb;
# };
class pref_custom_cbs(Structure):
    _fields_ = [('free_cb', pref_custom_free_cb),
                ('reset_cb', pref_custom_reset_cb),
                ('set_cb', pref_custom_set_cb),
                ('type_name_cb', pref_custom_type_name_cb),
                ('type_description_cb', pref_custom_type_description_cb),
                ('is_default_cb', pref_custom_is_default_cb),
                ('to_str_cb', pref_custom_to_str_cb)]

# #define PREF_UINT             (1u << 0)
PREF_UINT = 1 << 0

# #define PREF_BOOL             (1u << 1)
PREF_BOOL = 1 << 1

# #define PREF_ENUM             (1u << 2)
PREF_ENUM = 1 << 2

# #define PREF_STRING           (1u << 3)
PREF_STRING = 1 << 3

# #define PREF_RANGE            (1u << 4)
PREF_RANGE = 1 << 4

# #define PREF_STATIC_TEXT      (1u << 5)
PREF_STATIC_TEXT = 1 << 5

# #define PREF_UAT              (1u << 6)
PREF_UAT = 1 << 6

# #define PREF_SAVE_FILENAME    (1u << 7)
PREF_SAVE_FILENAME = 1 << 7

# #define PREF_COLOR            (1u << 8)
PREF_COLOR = 1 << 8

# #define PREF_CUSTOM           (1u << 9)
PREF_CUSTOM = 1 << 9

# #define PREF_OBSOLETE         (1u << 10)
PREF_OBSOLETE = 1 << 10

# #define PREF_DIRNAME          (1u << 11)
PREF_DIRNAME = 1 << 11

# #define PREF_DECODE_AS_UINT   (1u << 12)
PREF_DECODE_AS_UINT = 1 << 12

# #define PREF_DECODE_AS_RANGE  (1u << 13)
PREF_DECODE_AS_RANGE = 1 << 13

# #define PREF_OPEN_FILENAME    (1u << 14)
PREF_OPEN_FILENAME = 1 << 14

# typedef enum {
# 	GUI_ALL,
# 	GUI_GTK,
# 	GUI_QT
# } gui_type_t;
gui_type_t = c_int
GUI_ALL = 0
GUI_GTK = 1
GUI_QT = 2

# typedef prefs_set_pref_e (*pref_set_pair_cb) (gchar *key, const gchar *value, void *private_data, gboolean return_range_errors);
pref_set_pair_cb = CFUNCTYPE(prefs_set_pref_e, gchar_p,
                                               gchar_p,
                                               c_void_p,
                                               gboolean)

# #define PREF_EFFECT_DISSECTION        (1u << 0)
PREF_EFFECT_DISSECTION = 1 << 0

# #define PREF_EFFECT_CAPTURE           (1u << 1)
PREF_EFFECT_CAPTURE = 1 << 1

# #define PREF_EFFECT_GUI               (1u << 2)
PREF_EFFECT_GUI = 1 << 2

# #define PREF_EFFECT_FONT              (1u << 3)
PREF_EFFECT_FONT = 1 << 3

# #define PREF_EFFECT_GUI_LAYOUT        (1u << 4)
PREF_EFFECT_GUI_LAYOUT = 1 << 4

# #define PREF_EFFECT_FIELDS            (1u << 5)
PREF_EFFECT_FIELDS = 1 << 5

# #define PREF_EFFECT_CUSTOM            (1u << 31)
PREF_EFFECT_CUSTOM = 1 << 31

# typedef struct pref_unstash_data
# {
#     module_t *module;
#     gboolean handle_decode_as;
# } pref_unstash_data_t;
class pref_unstash_data(Structure):
    _fields_ = [('module', POINTER(module_t)),
                ('handle_decode_as', gboolean)]

pref_unstash_data_t = pref_unstash_data

# typedef struct {
# 	const char	*name;
# 	const char	*description;
# 	gint		value;
# } enum_val_t;
class enum_val_t(Structure):
    _fields_ = [('name', c_char_p),
                ('description', c_char_p),
                ('value', gint)]

# typedef struct range_admin_tag {
#     guint32 low;
#     guint32 high;
# } range_admin_t;
class range_admin_tag(Structure):
    _fields_ = [('low', guint32),
                ('high', guint32)]

range_admin_t = range_admin_tag

# typedef struct epan_range {
#     guint           nranges;
#     range_admin_t   ranges[1];
# } range_t;
class epan_range(Structure):
    _fields_ = [('nranges', guint),
                ('ranges', range_admin_t * 1)]

range_t = epan_range
