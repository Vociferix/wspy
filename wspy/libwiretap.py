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
import wspy.config as config


class LibWiretap:

    #######################
    # TYPES AND CONSTANTS #
    #######################

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
    WTAP_MAX_PACKET_SIZE_USBPCAP = (128 * 1024 * 1024)

    # #define WTAP_MAX_PACKET_SIZE_EBHSCR      (8*1024*1024)
    WTAP_MAX_PACKET_SIZE_EBHSCR = (8 * 1024 * 1024)

    # #define WTAP_MAX_PACKET_SIZE_DBUS        (128*1024*1024)
    WTAP_MAX_PACKET_SIZE_DBUS = (128 * 1024 * 1024)

    # #define FROM_DCE 0x80
    FROM_DCE = 0x80

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

    # #define PHDR_802_11G_MODE_NORMAL    0
    PHDR_802_11G_MODE_NORMAL = 0

    # #define PHDR_802_11G_MODE_SUPER_G   1
    PHDR_802_11G_MODE_SUPER_G = 1

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

    # #define PHDR_802_11AD_MIN_FREQUENCY    57000
    PHDR_802_11AD_MIN_FREQUENCY = 57000

    # #define PHDR_802_11AD_MAX_FREQUENCY    71000
    PHDR_802_11AD_MAX_FREQUENCY = 71000

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

    # #define MTP2_ANNEX_A_NOT_USED      0
    MTP2_ANNEX_A_NOT_USED = 0

    # #define MTP2_ANNEX_A_USED          1
    MTP2_ANNEX_A_USED = 1

    # #define MTP2_ANNEX_A_USED_UNKNOWN  2
    MTP2_ANNEX_A_USED_UNKNOWN = 2

    # #define K12_PORT_DS0S      0x00010008
    K12_PORT_DS0S = 0x00010008

    # #define K12_PORT_DS1       0x00100008
    K12_PORT_DS1 = 0x00100008

    # #define K12_PORT_ATMPVC    0x01020000
    K12_PORT_ATMPVC = 0x01020000

    # #define MAX_ERF_EHDR 16
    MAX_ERF_EHDR = 16

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

    # #define BTHCI_CHANNEL_COMMAND  1
    BTHCI_CHANNEL_COMMAND = 1

    # #define BTHCI_CHANNEL_ACL      2
    BTHCI_CHANNEL_ACL = 2

    # #define BTHCI_CHANNEL_SCO      3
    BTHCI_CHANNEL_SCO = 3

    # #define BTHCI_CHANNEL_EVENT    4
    BTHCI_CHANNEL_EVENT = 4

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

    # #define LLCP_PHDR_FLAG_SENT 0
    LLCP_PHDR_FLAG_SENT = 0

    # #define REC_TYPE_PACKET               0
    REC_TYPE_PACKET = 0

    # #define REC_TYPE_FT_SPECIFIC_EVENT    1
    REC_TYPE_FT_SPECIFIC_EVENT = 1

    # #define REC_TYPE_FT_SPECIFIC_REPORT   2
    REC_TYPE_FT_SPECIFIC_REPORT = 2

    # #define REC_TYPE_SYSCALL              3
    REC_TYPE_SYSCALL = 3

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

    # #define MAXNAMELEN  	64
    MAXNAMELEN = 64

    # #define WTAP_COMMENT_PER_SECTION        0x00000001
    WTAP_COMMENT_PER_SECTION = 0x00000001

    # #define WTAP_COMMENT_PER_INTERFACE      0x00000002
    WTAP_COMMENT_PER_INTERFACE = 0x00000002

    # #define WTAP_COMMENT_PER_PACKET         0x00000004
    WTAP_COMMENT_PER_PACKET = 0x00000004

    # #define WTAP_TYPE_AUTO 0
    WTAP_TYPE_AUTO = 0

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

    # #define BLOCK_TYPE_SHB              0x0A0D0D0A
    BLOCK_TYPE_SHB = 0x0A0D0D0A

    # #define BLOCK_TYPE_IDB              0x00000001
    BLOCK_TYPE_IDB = 0x00000001

    # #define BLOCK_TYPE_PB               0x00000002
    BLOCK_TYPE_PB = 0x00000002

    # #define BLOCK_TYPE_SPB              0x00000003
    BLOCK_TYPE_SPB = 0x00000003

    # #define BLOCK_TYPE_NRB              0x00000004
    BLOCK_TYPE_NRB = 0x00000004

    # #define BLOCK_TYPE_ISB              0x00000005
    BLOCK_TYPE_ISB = 0x00000005

    # #define BLOCK_TYPE_EPB              0x00000006
    BLOCK_TYPE_EPB = 0x00000006

    # #define BLOCK_TYPE_IRIG_TS          0x00000007
    BLOCK_TYPE_IRIG_TS = 0x00000007

    # #define BLOCK_TYPE_ARINC_429        0x00000008
    BLOCK_TYPE_ARINC_429 = 0x00000008

    # #define BLOCK_TYPE_SYSTEMD_JOURNAL  0x00000009
    BLOCK_TYPE_SYSTEMD_JOURNAL = 0x00000009

    # #define BLOCK_TYPE_DSB              0x0000000A
    BLOCK_TYPE_DSB = 0x0000000A

    # #define BLOCK_TYPE_SYSDIG_EVENT     0x00000204
    BLOCK_TYPE_SYSDIG_EVENT = 0x00000204

    # #define BLOCK_TYPE_SYSDIG_EVF       0x00000208
    BLOCK_TYPE_SYSDIG_EVF = 0x00000208

    # #define SECRETS_TYPE_TLS        0x544c534b
    SECRETS_TYPE_TLS = 0x544c534b

    # #define SECRETS_TYPE_WIREGUARD  0x57474b4c
    SECRETS_TYPE_WIREGUARD = 0x57474b4c

    # #define SECRETS_TYPE_TLS        0x544c534b
    SECRETS_TYPE_TLS = 0x544c534b

    # #define SECRETS_TYPE_WIREGUARD  0x57474b4c
    SECRETS_TYPE_WIREGUARD = 0x57474b4c

    # struct wtap_block;
    # typedef struct wtap_block *wtap_block_t;

    class wtap_block(Structure):
        _fields_ = []

    wtap_block_t = POINTER(wtap_block)

    # typedef enum {
    #     WTAP_BLOCK_NG_SECTION = 0,
    #     WTAP_BLOCK_IF_DESCR,
    #     WTAP_BLOCK_NG_NRB,
    #     WTAP_BLOCK_IF_STATS,
    #     WTAP_BLOCK_DSB,
    #     WTAP_BLOCK_END_OF_LIST
    # } wtap_block_type_t;
    wtap_block_type_t = c_int
    WTAP_BLOCK_NG_SECTION = c_int(0)
    WTAP_BLOCK_IF_DESCR = c_int(1)
    WTAP_BLOCK_NG_NRB = c_int(2)
    WTAP_BLOCK_IF_STATS = c_int(3)
    WTAP_BLOCK_DSB = c_int(4)
    WTAP_BLOCK_END_OF_LIST = c_int(5)

    # typedef enum {
    #     WTAP_OPTTYPE_UINT8,
    #     WTAP_OPTTYPE_UINT64,
    #     WTAP_OPTTYPE_STRING,
    #     WTAP_OPTTYPE_IPv4,
    #     WTAP_OPTTYPE_IPv6,
    #     WTAP_OPTTYPE_CUSTOM
    # } wtap_opttype_e;
    wtap_opttype_e = c_int
    WTAP_OPTTYPE_UINT8 = c_int(0)
    WTAP_OPTTYPE_UINT64 = c_int(1)
    WTAP_OPTTYPE_STRING = c_int(2)
    WTAP_OPTTYPE_IPv4 = c_int(3)
    WTAP_OPTTYPE_IPv6 = c_int(4)
    WTAP_OPTTYPE_CUSTOM = c_int(5)

    # typedef enum {
    #     WTAP_OPTTYPE_SUCCESS = 0,
    #     WTAP_OPTTYPE_NO_SUCH_OPTION = -1,
    #     WTAP_OPTTYPE_NOT_FOUND = -2,
    #     WTAP_OPTTYPE_TYPE_MISMATCH = -3,
    #     WTAP_OPTTYPE_NUMBER_MISMATCH = -4,
    #     WTAP_OPTTYPE_ALREADY_EXISTS = -5
    # } wtap_opttype_return_val;
    wtap_opttype_return_val = c_int
    WTAP_OPTTYPE_SUCCESS = c_int(0)
    WTAP_OPTTYPE_NO_SUCH_OPTION = c_int(-1)
    WTAP_OPTTYPE_NOT_FOUND = c_int(-2)
    WTAP_OPTTYPE_TYPE_MISMATCH = c_int(-3)
    WTAP_OPTTYPE_NUMBER_MISMATCH = c_int(-4)
    WTAP_OPTTYPE_ALREADY_EXISTS = c_int(-5)

    # struct wtap_opttype_custom {
    #     void* data;
    #     guint size;
    # };

    class wtap_opttype_custom(Structure):
        _fields_ = [('data', c_void_p),
                    ('size', LibGLib2.guint)]

    # typedef union {
    #     guint8 uint8val;
    #     guint64 uint64val;
    #     guint32 ipv4val;
    #     ws_in6_addr ipv6val;
    #     char *stringval;
    #     struct wtap_opttype_custom customval;
    # } wtap_optval_t;

    class wtap_optval_t(Union):
        pass

    wtap_optval_t._fields_ = [('uint8val', LibGLib2.guint8),
                              ('uint64val', LibGLib2.guint64),
                              ('ipv4val', LibGLib2.guint32),
                              ('ipv6val', LibWSUtil.ws_in6_addr),
                              ('stringval', c_char_p),
                              ('customval', wtap_opttype_custom)]

    # typedef struct {
    #     guint option_id;
    #     wtap_optval_t value;
    # } wtap_option_t;

    class wtap_option_t(Structure):
        pass

    wtap_option_t._fields_ = [('option_id', LibGLib2.guint),
                              ('value', wtap_optval_t)]

    # struct wtap_dumper;

    class wtap_dumper(Structure):
        pass

    # typedef void (*wtap_block_create_func)(wtap_block_t block);
    wtap_block_create_func = CFUNCTYPE(None, wtap_block_t)

    # typedef void (*wtap_mand_free_func)(wtap_block_t block);
    wtap_mand_free_func = CFUNCTYPE(None, wtap_block_t)

    # typedef void (*wtap_mand_copy_func)(wtap_block_t dest_block,
    # wtap_block_t src_block);
    wtap_mand_copy_func = CFUNCTYPE(None, wtap_block_t, wtap_block_t)

    # typedef void (*wtap_block_foreach_func)(wtap_block_t block, guint
    # option_id, wtap_opttype_e option_type, wtap_optval_t *option, void
    # *user_data);
    wtap_block_foreach_func = CFUNCTYPE(None,
                                        wtap_block_t,
                                        LibGLib2.guint,
                                        wtap_opttype_e,
                                        POINTER(wtap_optval_t),
                                        c_void_p)

    # struct eth_phdr {
    #     gint   fcs_len;
    # };

    class eth_phdr(Structure):
        _fields_ = [('fcs_len', LibGLib2.gint)]

    # struct dte_dce_phdr {
    #     guint8  flags;
    # };

    class dte_dce_phdr(Structure):
        _fields_ = [('fcs_len', LibGLib2.guint8)]

    # struct isdn_phdr {
    #     gboolean uton;
    #     guint8   channel;
    # };

    class isdn_phdr(Structure):
        _fields_ = [('uton', LibGLib2.gboolean), ('channel', LibGLib2.guint8)]

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
        _fields_ = [('flags', LibGLib2.guint32),
                    ('aal', LibGLib2.guint8),
                    ('type', LibGLib2.guint8),
                    ('subtype', LibGLib2.guint8),
                    ('vpi', LibGLib2.guint16),
                    ('vci', LibGLib2.guint16),
                    ('aal2_cid', LibGLib2.guint8),
                    ('channel', LibGLib2.guint16),
                    ('cells', LibGLib2.guint16),
                    ('aal5t_u2u', LibGLib2.guint16),
                    ('aal5t_len', LibGLib2.guint16),
                    ('aal5t_chksum', LibGLib2.guint32)]

    # struct ascend_phdr {
    #     guint16 type;
    #     char    user[ASCEND_MAX_STR_LEN];
    #     guint32 sess;
    #     char    call_num[ASCEND_MAX_STR_LEN];
    #     guint32 chunk;
    #     guint32 task;
    # };

    class ascend_phdr(Structure):
        pass

    ascend_phdr._fields_ = [('type', LibGLib2.guint16),
                            ('user', c_char * ASCEND_MAX_STR_LEN),
                            ('sess', LibGLib2.guint32),
                            ('call_num', c_char * ASCEND_MAX_STR_LEN),
                            ('chunk', LibGLib2.guint32),
                            ('task', LibGLib2.guint32)]

    # struct p2p_phdr {
    #     gboolean sent;
    # };

    class p2p_phdr(Structure):
        _fields_ = [('sent', LibGLib2.gboolean)]

    # struct ieee_802_11_fhss {
    #     guint    has_hop_set:1;
    #     guint    has_hop_pattern:1;
    #     guint    has_hop_index:1;
    #     guint8   hop_set;
    #     guint8   hop_pattern;
    #     guint8   hop_index;
    # };

    class ieee_802_11_fhss(Structure):
        _fields_ = [('has_hop_set', LibGLib2.guint, 1),
                    ('has_hop_pattern', LibGLib2.guint, 1),
                    ('has_hop_index', LibGLib2.guint, 1),
                    ('hop_set', LibGLib2.guint8),
                    ('hop_pattern', LibGLib2.guint8),
                    ('hop_index', LibGLib2.guint8)]

    # struct ieee_802_11b {
    #     guint    has_short_preamble:1;
    #     gboolean short_preamble;
    # };

    class ieee_802_11b(Structure):
        _fields_ = [('has_short_preamble', LibGLib2.guint, 1),
                    ('short_preamble', LibGLib2.gboolean)]

    # struct ieee_802_11a {
    #     guint    has_channel_type:1;
    #     guint    has_turbo_type:1;
    #     guint    channel_type:2;
    #     guint    turbo_type:2;
    # };

    class ieee_802_11a(Structure):
        _fields_ = [('has_channel_type', LibGLib2.guint, 1),
                    ('has_turbo_type', LibGLib2.guint, 1),
                    ('channel_type', LibGLib2.guint, 2),
                    ('turbo_type', LibGLib2.guint, 2)]

    # struct ieee_802_11g {
    #     guint    has_short_preamble:1;
    #     guint    has_mode:1;
    #     gboolean short_preamble;
    #     guint32  mode;
    # };

    class ieee_802_11g(Structure):
        _fields_ = [('has_short_preamble', LibGLib2.guint, 1),
                    ('has_mode', LibGLib2.guint, 1),
                    ('short_preamble', LibGLib2.gboolean),
                    ('mode', LibGLib2.guint32)]

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
        _fields_ = [('has_mcs_index', LibGLib2.guint, 1),
                    ('has_bandwidth', LibGLib2.guint, 1),
                    ('has_short_gi', LibGLib2.guint, 1),
                    ('has_greenfield', LibGLib2.guint, 1),
                    ('has_fec', LibGLib2.guint, 1),
                    ('has_stbc_streams', LibGLib2.guint, 1),
                    ('has_ness', LibGLib2.guint, 1),
                    ('mcs_index', LibGLib2.guint16),
                    ('bandwidth', LibGLib2.guint),
                    ('short_gi', LibGLib2.guint, 1),
                    ('greenfield', LibGLib2.guint, 1),
                    ('fec', LibGLib2.guint, 1),
                    ('stbc_streams', LibGLib2.guint, 1),
                    ('ness', LibGLib2.guint, 1)]

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
        _fields_ = [('has_stbc', LibGLib2.guint, 1),
                    ('has_txop_ps_not_allowed', LibGLib2.guint, 1),
                    ('has_short_gi', LibGLib2.guint, 1),
                    ('has_short_gi_nsym_disambig', LibGLib2.guint, 1),
                    ('has_ldpc_extra_ofdm_symbol', LibGLib2.guint, 1),
                    ('has_beamformed', LibGLib2.guint, 1),
                    ('has_bandwidth', LibGLib2.guint, 1),
                    ('has_fec', LibGLib2.guint, 1),
                    ('has_group_id', LibGLib2.guint, 1),
                    ('has_partial_aid', LibGLib2.guint, 1),
                    ('stbc', LibGLib2.guint, 1),
                    ('txop_ps_not_allowed', LibGLib2.guint, 1),
                    ('short_gi', LibGLib2.guint, 1),
                    ('short_gi_nsym_disambig', LibGLib2.guint, 1),
                    ('ldpc_extra_ofdm_symbol', LibGLib2.guint, 1),
                    ('beamformed', LibGLib2.guint, 1),
                    ('bandwidth', LibGLib2.guint8),
                    ('msc', LibGLib2.guint8 * 4),
                    ('nss', LibGLib2.guint8 * 4),
                    ('fec', LibGLib2.guint8),
                    ('group_id', LibGLib2.guint8),
                    ('partial_aid', LibGLib2.guint16)]

    # struct ieee_802_11ad {
    #     guint    has_mcs_index:1;
    #     guint8   mcs;
    # };

    class ieee_802_11ad(Structure):
        _fields_ = [('has_mcs_index', LibGLib2.guint, 1),
                    ('mcs', LibGLib2.guint8)]

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
        _fields_ = [('has_mcs_index', LibGLib2.guint, 1),
                    ('has_bwru', LibGLib2.guint, 1),
                    ('has_gi', LibGLib2.guint, 1),
                    ('nsts', LibGLib2.guint8, 4),
                    ('mcs', LibGLib2.guint8, 4),
                    ('bwru', LibGLib2.guint8, 4),
                    ('gi', LibGLib2.guint8, 2)]

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
        pass

    ieee_802_11_phy_info._fields_ = [('info_11_fhss', ieee_802_11_fhss),
                                     ('info_11b', ieee_802_11b),
                                     ('info_11a', ieee_802_11a),
                                     ('info_11g', ieee_802_11g),
                                     ('info_11n', ieee_802_11n),
                                     ('info_11ac', ieee_802_11ac),
                                     ('info_11ad', ieee_802_11ad),
                                     ('info_11ax', ieee_802_11ax)]

    # struct ieee_802_11_phdr {
    #     gint     fcs_len;
    #     gboolean decrypted;
    #     gboolean datapad;
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
        pass

    ieee_802_11_phdr._fields_ = [('fcs_len', LibGLib2.gint),
                                 ('decrypted', LibGLib2.gboolean),
                                 ('datapad', LibGLib2.gboolean),
                                 ('phy', LibGLib2.guint),
                                 ('phy_info', ieee_802_11_phy_info),
                                 ('has_channel', LibGLib2.guint, 1),
                                 ('has_frequency', LibGLib2.guint, 1),
                                 ('has_data_rate', LibGLib2.guint, 1),
                                 ('has_signal_percent', LibGLib2.guint, 1),
                                 ('has_noise_percent', LibGLib2.guint, 1),
                                 ('has_signal_dbm', LibGLib2.guint, 1),
                                 ('has_noise_dbm', LibGLib2.guint, 1),
                                 ('has_signal_db', LibGLib2.guint, 1),
                                 ('has_noise_db', LibGLib2.guint, 1),
                                 ('has_tsf_timestamp', LibGLib2.guint, 1),
                                 ('has_aggregate_info', LibGLib2.guint, 1),
                                 ('has_zero_length_psdu_type', LibGLib2.guint, 1),
                                 ('channel', LibGLib2.guint16),
                                 ('frequency', LibGLib2.guint32),
                                 ('data_rate', LibGLib2.guint16),
                                 ('signal_percent', LibGLib2.guint8),
                                 ('noise_percent', LibGLib2.guint8),
                                 ('signal_dbm', LibGLib2.gint8),
                                 ('noise_dbm', LibGLib2.gint8),
                                 ('signal_db', LibGLib2.guint8),
                                 ('noise_db', LibGLib2.guint8),
                                 ('tsf_timestamp', LibGLib2.guint64),
                                 ('aggregate_flags', LibGLib2.guint32),
                                 ('aggregate_id', LibGLib2.guint32),
                                 ('zero_length_psdu_type', LibGLib2.guint8)]

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
        pass

    cosine_phdr._fields_ = [('encap', LibGLib2.guint8),
                            ('direction', LibGLib2.guint8),
                            ('if_name', c_char * COSINE_MAX_IF_NAME_LEN),
                            ('pro', LibGLib2.guint16),
                            ('off', LibGLib2.guint16),
                            ('pri', LibGLib2.guint16),
                            ('rm', LibGLib2.guint16),
                            ('err', LibGLib2.guint16)]

    # struct irda_phdr {
    #     guint16 pkttype;
    # };

    class irda_phdr(Structure):
        _fields_ = [('pkttype', LibGLib2.guint16)]

    # struct nettl_phdr {
    #     guint16 subsys;
    #     guint32 devid;
    #     guint32 kind;
    #     gint32  pid;
    #     guint32 uid;
    # };

    class nettl_phdr(Structure):
        _fields_ = [('subsys', LibGLib2.guint16),
                    ('devid', LibGLib2.guint32),
                    ('kind', LibGLib2.guint32),
                    ('pid', LibGLib2.gint32),
                    ('uid', LibGLib2.guint32)]

    # struct mtp2_phdr {
    #     guint8  sent;
    #     guint8  annex_a_used;
    #     guint16 link_number;
    # };

    class mtp2_phdr(Structure):
        _fields_ = [('sent', LibGLib2.guint8),
                    ('annex_a_used', LibGLib2.guint8),
                    ('link_number', LibGLib2.guint16)]

    # typedef union {
    #     struct {
    #         guint16 vp;
    #         guint16 vc;
    #         guint16 cid;
    #     } atm;
    #     guint32 ds0mask;
    # } k12_input_info_t;

    class _atm_t(Structure):
        _fields_ = [('vp', LibGLib2.guint16),
                    ('vc', LibGLib2.guint16),
                    ('cid', LibGLib2.guint16)]

    class k12_input_info_t(Union):
        pass

    k12_input_info_t._fields_ = [('atm', _atm_t),
                                 ('ds0mask', LibGLib2.guint32)]

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
        pass

    k12_phdr._fields_ = [('input', LibGLib2.guint32),
                         ('input_name', LibGLib2.gchar_p),
                         ('stack_file', LibGLib2.gchar_p),
                         ('input_type', LibGLib2.guint32),
                         ('input_info', k12_input_info_t),
                         ('extra_info', POINTER(LibGLib2.guint8)),
                         ('extra_length', LibGLib2.guint32),
                         ('stuff', c_void_p)]

    # struct lapd_phdr {
    #     guint16 pkttype;
    #     guint8 we_network;
    # };

    class lapd_phdr(Structure):
        _fields_ = [('pkttype', LibGLib2.guint16),
                    ('we_network', LibGLib2.guint8)]

    # struct wtap

    class wtap(Structure):
        pass

    # struct catapult_dct2000_phdr {
    #     union {
    #         struct isdn_phdr isdn;
    #         struct atm_phdr  atm;
    #         struct p2p_phdr  p2p;
    #     } inner_pseudo_header;
    #     gint64       seek_off;
    #     struct wtap *wth;
    # };

    class _inner_pseudo_header_t(Union):
        pass

    _inner_pseudo_header_t._fields_ = [('isdn', isdn_phdr),
                                       ('atm', atm_phdr),
                                       ('p2p', p2p_phdr)]

    class catapult_dct2000_phdr(Structure):
        pass

    catapult_dct2000_phdr._fields_ = [
        ('inner_pseudo_header',
         _inner_pseudo_header_t),
        ('seek_off',
         LibGLib2.gint64),
        ('wth',
         POINTER(wtap))]

    # struct erf_phdr {
    #     guint64 ts;
    #     guint8  type;
    #     guint8  flags;
    #     guint16 rlen;
    #     guint16 lctr;
    #     guint16 wlen;
    # };

    class erf_phdr(Structure):
        _fields_ = [('ts', LibGLib2.guint64),
                    ('type', LibGLib2.guint8),
                    ('flags', LibGLib2.guint8),
                    ('rlen', LibGLib2.guint16),
                    ('lctr', LibGLib2.guint16),
                    ('wlen', LibGLib2.guint16)]

    # struct erf_ehdr {
    #   guint64 ehdr;
    # };

    class erf_ehdr(Structure):
        _fields_ = [('ehdr', LibGLib2.guint64)]

    # struct wtap_erf_eth_hdr {
    #     guint8 offset;
    #     guint8 pad;
    # };

    class wtap_erf_eth_hdr(Structure):
        _fields_ = [('offset', LibGLib2.guint8),
                    ('pad', LibGLib2.guint8)]

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

    class _subhdr_t(Union):
        pass

    _subhdr_t._fields_ = [('eth_hdr', wtap_erf_eth_hdr),
                          ('mc_hdr', LibGLib2.guint32),
                          ('aal2_hdr', LibGLib2.guint32)]

    class erf_mc_phdr(Structure):
        pass

    erf_mc_phdr._fields_ = [('phdr', erf_phdr),
                            ('ehdr_list', erf_ehdr * MAX_ERF_EHDR),
                            ('subhdr', _subhdr_t)]

    # struct sita_phdr {
    #     guint8  sita_flags;
    #     guint8  sita_signals;
    #     guint8  sita_errors1;
    #     guint8  sita_errors2;
    #     guint8  sita_proto;
    # };

    class sita_phdr(Structure):
        _fields_ = [('sita_flags', LibGLib2.guint8),
                    ('sita_signals', LibGLib2.guint8),
                    ('sita_errors1', LibGLib2.guint8),
                    ('sita_errors2', LibGLib2.guint8),
                    ('sita_proto', LibGLib2.guint8)]

    # struct bthci_phdr {
    #     gboolean  sent;
    #     guint32   channel;
    # };

    class bthci_phdr(Structure):
        _fields_ = [('sent', LibGLib2.gboolean),
                    ('channel', LibGLib2.guint32)]

    # struct btmon_phdr {
    #     guint16   adapter_id;
    #     guint16   opcode;
    # };

    class btmon_phdr(Structure):
        _fields_ = [('adapter_id', LibGLib2.guint16),
                    ('opcode', LibGLib2.guint16)]

    # struct l1event_phdr {
    #     gboolean uton;
    # };

    class l1event_phdr(Structure):
        _fields_ = [('uton', LibGLib2.gboolean)]

    # struct i2c_phdr {
    #     guint8  is_event;
    #     guint8  bus;
    #     guint32 flags;
    # };

    class i2c_phdr(Structure):
        _fields_ = [('is_event', LibGLib2.guint8),
                    ('bus', LibGLib2.guint),
                    ('flags', LibGLib2.guint32)]

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
        _fields_ = [('uplink', LibGLib2.gboolean),
                    ('channel', LibGLib2.guint8),
                    ('bsic', LibGLib2.guint8),
                    ('arfcn', LibGLib2.guint16),
                    ('tdma_frame', LibGLib2.guint32),
                    ('error', LibGLib2.guint8),
                    ('timeshift', LibGLib2.guint16)]

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
        _fields_ = [('rec_offset', LibGLib2.gint64),
                    ('rec_len', LibGLib2.gint32),
                    ('nicno_offset', LibGLib2.guint8),
                    ('nicno_len', LibGLib2.guint8),
                    ('dir_offset', LibGLib2.guint8),
                    ('dir_len', LibGLib2.guint8),
                    ('eth_offset', LibGLib2.guint16),
                    ('pcb_offset', LibGLib2.guint8),
                    ('l_pcb_offset', LibGLib2.guint8),
                    ('rec_type', LibGLib2.guint8),
                    ('vlantag_offset', LibGLib2.guint8),
                    ('coreid_offset', LibGLib2.guint8),
                    ('srcnodeid_offset', LibGLib2.guint8),
                    ('destnodeid_offset', LibGLib2.guint8),
                    ('clflags_offset', LibGLib2.guint8),
                    ('src_vmname_len_offset', LibGLib2.guint8),
                    ('dst_vmname_len_offset', LibGLib2.guint8),
                    ('ns_activity_offset', LibGLib2.guint8),
                    ('data_offset', LibGLib2.guint8)]

    # struct nokia_phdr {
    #     struct eth_phdr eth;
    #     guint8 stuff[4];
    # };

    class nokia_phdr(Structure):
        pass

    nokia_phdr._fields_ = [('eth', eth_phdr),
                           ('stuff', LibGLib2.guint8 * 4)]

    # struct llcp_phdr {
    #     guint8 adapter;
    #     guint8 flags;
    # };

    class llcp_phdr(Structure):
        _fields_ = [('adapter', LibGLib2.guint8),
                    ('flags', LibGLib2.guint8)]

    # struct logcat_phdr {
    #     gint version;
    # };

    class logcat_phdr(Structure):
        _fields_ = [('version', LibGLib2.gint)]

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
        pass

    sub_wtap_pseudo_header._fields_ = [('eth', eth_phdr),
                                       ('atm', atm_phdr),
                                       ('ieee_802_11', ieee_802_11_phdr)]

    class netmon_phdr(Structure):
        pass

    netmon_phdr._fields_ = [('title', POINTER(LibGLib2.guint8)),
                            ('descLength', LibGLib2.guint32),
                            ('description', POINTER(LibGLib2.guint8)),
                            ('sub_encap', LibGLib2.guint),
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
        pass

    wtap_pseudo_header._fields_ = [('eth', eth_phdr),
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
        pass

    wtap_packet_header._fields_ = [('caplen', LibGLib2.guint32),
                                   ('len', LibGLib2.guint32),
                                   ('pkt_encap', c_int),
                                   ('interface_id', LibGLib2.guint32),
                                   ('drop_count', LibGLib2.guint64),
                                   ('pack_flags', LibGLib2.guint32),
                                   ('interface_queue', LibGLib2.guint32),
                                   ('packet_id', LibGLib2.guint64),
                                   ('pseudo_header', wtap_pseudo_header)]

    # typedef struct {
    #     guint     record_type;
    #     guint32   record_len;
    # } wtap_ft_specific_header;

    class wtap_ft_specific_header(Structure):
        _fields_ = [('record_type', LibGLib2.guint),
                    ('record_len', LibGLib2.guint32)]

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
        _fields_ = [('record_type', LibGLib2.guint),
                    ('byte_order', c_int),
                    ('timestamp', LibGLib2.guint64),
                    ('thread_id', LibGLib2.guint64),
                    ('event_len', LibGLib2.guint32),
                    ('event_filelen', LibGLib2.guint32),
                    ('event_type', LibGLib2.guint16),
                    ('cpu_id', LibGLib2.guint16)]

    # typedef struct {
    #     guint     rec_type;
    #     guint32   presence_flags;
    #     nstime_t  ts;
    #     int       tsprec;
    #     union {
    #         wtap_packet_header packet_header;
    #         wtap_ft_specific_header ft_specific_header;
    #         wtap_syscall_header syscall_header;
    #     } rec_header;
    #     gchar     *opt_comment;
    #     gboolean  has_comment_changed;
    #     GPtrArray *packet_verdict;
    #     Buffer    options_buf;
    # } wtap_rec;

    class _rec_header_t(Union):
        pass

    _rec_header_t._fields_ = [('packet_header', wtap_packet_header),
                              ('ft_specific_header', wtap_ft_specific_header),
                              ('syscall_header', wtap_syscall_header)]

    class wtap_rec(Structure):
        pass

    wtap_rec._fields_ = [('rec_type', LibGLib2.guint),
                         ('presence_flags', LibGLib2.guint32),
                         ('ts', LibWSUtil.nstime_t),
                         ('tsprec', c_int),
                         ('rec_header', _rec_header_t),
                         ('opt_comment', LibGLib2.gchar_p),
                         ('has_comment_changed', LibGLib2.gboolean),
                         ('packet_verdict', POINTER(LibGLib2.GPtrArray)),
                         ('options_buf', LibWSUtil.Buffer)]

    # typedef struct wtapng_section_mandatory_s {
    #     guint64             section_length;
    # } wtapng_mandatory_section_t;

    class wtapng_mandatory_section_s(Structure):
        _fields_ = [('section_length', LibGLib2.guint64)]

    wtapng_mandatory_section_t = wtapng_mandatory_section_s

    # typedef struct wtapng_iface_descriptions_s {
    #     GArray *interface_data;
    # } wtapng_iface_descriptions_t;

    class wtapng_iface_descriptions_s(Structure):
        _fields_ = [('interface_data', POINTER(LibGLib2.GArray))]

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
                    ('time_units_per_second', LibGLib2.guint64),
                    ('tsprecision', c_int),
                    ('snap_len', LibGLib2.guint32),
                    ('num_stat_entries', LibGLib2.guint8),
                    ('interface_statistics', POINTER(LibGLib2.GArray))]

    wtapng_if_descr_mandatory_t = wtapng_if_descr_mandatory_s

    # typedef struct wtapng_dsb_mandatory_s {
    #     guint32                secrets_type;
    #     guint32                secrets_len;
    #     guint8                *secrets_data;
    # } wtapng_dsb_mandatory_t;

    class wtapng_dsb_mandatory_s(Structure):
        _fields_ = [('secrets_type', LibGLib2.guint32),
                    ('secrets_len', LibGLib2.guint32),
                    ('secrets_data', POINTER(LibGLib2.guint8))]

    wtapng_dsb_mandatory_t = wtapng_dsb_mandatory_s

    # typedef struct wtapng_if_descr_filter_s {
    #     gchar                 *if_filter_str;
    #     guint16                bpf_filter_len;
    #     guint8                *if_filter_bpf_bytes;
    # } wtapng_if_descr_filter_t;

    class wtapng_if_descr_filter_s(Structure):
        _fields_ = [('if_filter_str', LibGLib2.gchar_p),
                    ('bpf_filter_len', LibGLib2.guint16),
                    ('if_filter_bpf_bytes', POINTER(LibGLib2.guint8))]

    wtapng_if_descr_filter_t = wtapng_if_descr_filter_s

    # typedef struct wtapng_if_stats_mandatory_s {
    #     guint32  interface_id;
    #     guint32  ts_high;
    #     guint32  ts_low;
    # } wtapng_if_stats_mandatory_t;

    class wtapng_if_stats_mandatory_s(Structure):
        _fields_ = [('interface_id', LibGLib2.guint32),
                    ('ts_high', LibGLib2.guint32),
                    ('ts_low', LibGLib2.guint32)]

    wtapng_if_stats_mandatory_t = wtapng_if_stats_mandatory_s

    # typedef struct hashipv4 {
    #     guint             addr;
    #     guint8            flags;
    #     gchar             ip[WS_INET_ADDRSTRLEN];
    #     gchar             name[MAXNAMELEN];
    # } hashipv4_t;

    class hashipv4(Structure):
        pass

    hashipv4._fields_ = [('addr', LibGLib2.guint),
                         ('flags', LibGLib2.guint8),
                         ('ip', LibGLib2.gchar * LibWSUtil.WS_INET_ADDRSTRLEN),
                         ('name', LibGLib2.gchar * MAXNAMELEN)]

    hashipv4_t = hashipv4

    # typedef struct hashipv6 {
    #     guint8            addr[16];
    #     guint8            flags;
    #     gchar             ip6[WS_INET6_ADDRSTRLEN];
    #     gchar             name[MAXNAMELEN];
    # } hashipv6_t;

    class hashipv6(Structure):
        pass

    hashipv6._fields_ = [('addr', LibGLib2.guint8 * 16),
                         ('flags', LibGLib2.guint8),
                         ('ip6', LibGLib2.gchar * LibWSUtil.WS_INET6_ADDRSTRLEN),
                         ('name', LibGLib2.gchar * MAXNAMELEN)]

    hashipv6_t = hashipv6

    # typedef struct addrinfo_lists {
    #     GList      *ipv4_addr_list;
    #     GList      *ipv6_addr_list;
    # } addrinfo_lists_t;

    class addrinfo_lists(Structure):
        _fields_ = [('ipv4_addr_list', POINTER(LibGLib2.GList)),
                    ('ipv6_addr_list', POINTER(LibGLib2.GList))]

    addrinfo_lists_t = addrinfo_lists

    # typedef struct wtap_dump_params {
    #     int         encap;
    #     int         snaplen;
    #     GArray     *shb_hdrs;
    #     wtapng_iface_descriptions_t *idb_inf;
    #     GArray     *nrb_hdrs;
    #     GArray     *dsbs_initial;
    #     const GArray *dsbs_growing;
    # } wtap_dump_params;

    class wtap_dump_params(Structure):
        pass

    wtap_dump_params._fields_ = [('encap', c_int),
                                 ('snaplen', c_int),
                                 ('shb_hdrs', POINTER(LibGLib2.GArray)),
                                 ('idb_inf', POINTER(wtapng_iface_descriptions_t)),
                                 ('nrb_hdrs', POINTER(LibGLib2.GArray)),
                                 ('dsbs_initial', POINTER(LibGLib2.GArray)),
                                 ('dsbs_growing', POINTER(LibGLib2.GArray))]

    # #define WTAP_DUMP_PARAMS_INIT {.snaplen=0}
    WTAP_DUMP_PARAMS_INIT = wtap_dump_params(0, 0)

    # typedef struct wtap_reader *FILE_T;

    class wtap_reader(Structure):
        _fields_ = []

    FILE_T = POINTER(wtap_reader)

    # typedef struct wtap_wslua_file_info {
    #     int (*wslua_can_write_encap)(int, void*);
    #     void* wslua_data;
    # } wtap_wslua_file_info_t;

    class wtap_wslua_file_info(Structure):
        _fields_ = [('wslua_can_write_encap', CFUNCTYPE(
            c_int, c_int, c_void_p)), ('wslua_data', c_void_p)]

    wtap_wslua_file_info_t = wtap_wslua_file_info

    # struct file_extension_info {
    #     const char *name;
    #     gboolean is_capture_file;
    #     const char *extensions;
    # };

    class file_extension_info(Structure):
        _fields_ = [('name', c_char_p),
                    ('is_capture_file', LibGLib2.gboolean),
                    ('extensions', c_char_p)]

    # typedef enum {
    #     WTAP_OPEN_NOT_MINE = 0,
    #     WTAP_OPEN_MINE = 1,
    #     WTAP_OPEN_ERROR = -1
    # } wtap_open_return_val;
    wtap_open_return_val = c_int
    WTAP_OPEN_NOT_MINE = c_int(0)
    WTAP_OPEN_MINE = c_int(1)
    WTAP_OPEN_ERROR = c_int(-1)

    # typedef wtap_open_return_val (*wtap_open_routine_t)(struct wtap*, int *,
    # char **);
    wtap_open_routine_t = CFUNCTYPE(
        wtap_open_return_val,
        POINTER(wtap),
        POINTER(c_int),
        POINTER(c_char_p))

    # typedef enum {
    #     OPEN_INFO_MAGIC = 0,
    #     OPEN_INFO_HEURISTIC = 1
    # } wtap_open_type;
    wtap_open_type = c_int
    OPEN_INFO_MAGIC = c_int(0)
    OPEN_INFO_HEURISTIC = c_int(1)

    # struct open_info {
    #     const char *name;
    #     wtap_open_type type;
    #     wtap_open_routine_t open_routine;
    #     const char *extensions;
    #     gchar **extensions_set;
    #     void* wslua_data;
    # };

    class open_info(Structure):
        pass

    open_info._fields_ = [('name', c_char_p),
                          ('type', wtap_open_type),
                          ('open_routine', wtap_open_routine_t),
                          ('extensions', c_char_p),
                          ('extensions_set', POINTER(LibGLib2.gchar_p)),
                          ('wslua_data', c_void_p)]

    # struct file_type_subtype_info {
    #     const char *name;
    #     const char *short_name;
    #     const char *default_file_extension;
    #     const char *additional_file_extensions;
    #     gboolean writing_must_seek;
    #     gboolean has_name_resolution;
    #     guint32 supported_comment_types;
    #     int (*can_write_encap)(int);
    #     int (*dump_open)(wtap_dumper *, int *);
    #     wtap_wslua_file_info_t *wslua_info;
    # };

    class file_type_subtype_info(Structure):
        pass

    file_type_subtype_info._fields_ = [('name', c_char_p),
                                       ('short_name', c_char_p),
                                       ('default_file_extension', c_char_p),
                                       ('additional_file_extensions', c_char_p),
                                       ('writing_must_seek', LibGLib2.gboolean),
                                       ('has_name_resolution', LibGLib2.gboolean),
                                       ('supported_comment_types', LibGLib2.guint32),
                                       ('can_write_encap', CFUNCTYPE(c_int, c_int)),
                                       ('dump_open', CFUNCTYPE(c_int, POINTER(wtap_dumper), POINTER(c_int))),
                                       ('wslua_info', POINTER(wtap_wslua_file_info_t))]

    # typedef void (*wtap_new_ipv4_callback_t) (const guint addr, const gchar
    # *name);
    wtap_new_ipv4_callback_t = CFUNCTYPE(
        None, LibGLib2.guint, LibGLib2.gchar_p)

    # typedef void (*wtap_new_ipv6_callback_t) (const void *addrp, const gchar
    # *name);
    wtap_new_ipv6_callback_t = CFUNCTYPE(None, c_void_p, LibGLib2.gchar_p)

    # typedef void (*wtap_new_secrets_callback_t)(guint32 secrets_type, const
    # void *secrets, guint size);
    wtap_new_secrets_callback_t = CFUNCTYPE(
        None, LibGLib2.guint32, c_void_p, LibGLib2.guint)

    # typedef enum {
    #     WTAP_UNCOMPRESSED,
    #     WTAP_GZIP_COMPRESSED
    # } wtap_compression_type;
    wtap_compression_type = c_int
    WTAP_UNCOMPRESSED = c_int(0)
    WTAP_GZIP_COMPRESSED = c_int(1)

    # struct addrinfo;

    class addrinfo(Structure):
        _fields_ = []

    # typedef struct {
    # 	void (*register_wtap_module)(void);
    # } wtap_plugin;

    class wtap_plugin(Structure):
        _fields_ = [('register_wtap_module', CFUNCTYPE(None))]

    # typedef struct wtap_writer *GZWFILE_T;

    class wtap_writer(Structure):
        _fields_ = []

    GZWFILE_T = POINTER(wtap_writer)

    # typedef enum {
    #     RECORD_PRESENT,
    #     RECORD_NOT_PRESENT,
    #     AT_EOF,
    #     GOT_ERROR
    # } in_file_state_e;
    in_file_state_e = c_int
    RECORD_PRESENT = c_int(0)
    RECORD_NOT_PRESENT = c_int(1)
    AT_EOF = c_int(2)
    GOT_ERROR = c_int(3)

    # typedef struct merge_in_file_s {
    #     const char     *filename;
    #     wtap           *wth;
    #     wtap_rec        rec;
    #     Buffer          frame_buffer;
    #     in_file_state_e state;
    #     guint32         packet_num;
    #     gint64          size;
    #     GArray         *idb_index_map;
    #     guint           dsbs_seen;
    # } merge_in_file_t;

    class merge_in_file_s(Structure):
        pass

    merge_in_file_s._fields_ = [('filename', c_char_p),
                                ('wth', POINTER(wtap)),
                                ('rec', wtap_rec),
                                ('frame_buffer', LibWSUtil.Buffer),
                                ('state', in_file_state_e),
                                ('packet_num', LibGLib2.guint32),
                                ('size', LibGLib2.gint64),
                                ('idb_index_map', POINTER(LibGLib2.GArray)),
                                ('dsbs_seen', LibGLib2.guint)]

    merge_in_file_t = merge_in_file_s

    # typedef enum {
    #     MERGE_OK,
    #     MERGE_USER_ABORTED,
    #     MERGE_ERR_CANT_OPEN_INFILE,
    #     MERGE_ERR_CANT_OPEN_OUTFILE,
    #     MERGE_ERR_CANT_READ_INFILE,
    #     MERGE_ERR_BAD_PHDR_INTERFACE_ID,
    #     MERGE_ERR_CANT_WRITE_OUTFILE,
    #     MERGE_ERR_CANT_CLOSE_OUTFILE,
    #     MERGE_ERR_INVALID_OPTION
    # } merge_result;
    merge_result = c_int
    MERGE_OK = c_int(0)
    MERGE_USER_ABORTED = c_int(1)
    MERGE_ERR_CANT_OPEN_INFILE = c_int(2)
    MERGE_ERR_CANT_OPEN_OUTFILE = c_int(3)
    MERGE_ERR_CANT_READ_INFILE = c_int(4)
    MERGE_ERR_BAD_PHDR_INTERFACE_ID = c_int(5)
    MERGE_ERR_CANT_WRITE_OUTFILE = c_int(6)
    MERGE_ERR_CANT_CLOSE_OUTFILE = c_int(7)
    MERGE_ERR_INVALID_OPTION = c_int(8)

    # typedef enum {
    #     MERGE_EVENT_INPUT_FILES_OPENED,
    #     MERGE_EVENT_FRAME_TYPE_SELECTED,
    #     MERGE_EVENT_READY_TO_MERGE,
    #     MERGE_EVENT_RECORD_WAS_READ,
    #     MERGE_EVENT_DONE
    # } merge_event;
    merge_event = c_int
    MERGE_EVENT_INPUT_FILES_OPENED = c_int(0)
    MERGE_EVENT_FRAME_TYPE_SELECTED = c_int(1)
    MERGE_EVENT_READY_TO_MERGE = c_int(2)
    MERGE_EVENT_RECORD_WAS_READ = c_int(3)
    MERGE_EVENT_DONE = c_int(4)

    # typedef enum {
    #     IDB_MERGE_MODE_NONE = 0,
    #     IDB_MERGE_MODE_ALL_SAME,
    #     IDB_MERGE_MODE_ANY_SAME,
    #     IDB_MERGE_MODE_MAX
    # } idb_merge_mode;
    idb_merge_mode = c_int
    IDB_MERGE_MODE_NONE = c_int(0)
    IDB_MERGE_MODE_ALL_SAME = c_int(1)
    IDB_MERGE_MODE_ANY_SAME = c_int(2)
    IDB_MERGE_MODE_MAX = c_int(3)

    # typedef struct {
    #     gboolean (*callback_func)(merge_event event, int num,
    #                               const merge_in_file_t in_files[], const guint in_file_count,
    #                               void *data);
    #     void *data;
    # } merge_progress_callback_t;

    class merge_progress_callback_t(Structure):
        pass

    merge_progress_callback_t._fields_ = [
        ('callback_func',
         CFUNCTYPE(
             LibGLib2.gboolean,
             merge_event,
             c_int,
             POINTER(merge_in_file_t),
             LibGLib2.guint,
             c_void_p)),
        ('data',
         c_void_p)]

    # typedef struct wtapng_block_s {
    #     guint32      type;
    #     gboolean     internal;
    #     wtap_block_t block;
    #     wtap_rec     *rec;
    #     Buffer       *frame_buffer;
    # } wtapng_block_t;

    class wtapng_block_s(Structure):
        pass

    wtapng_block_s._fields_ = [('type', LibGLib2.guint32),
                               ('internal', LibGLib2.gboolean),
                               ('block', wtap_block_t),
                               ('rec', POINTER(wtap_rec)),
                               ('frame_buffer', POINTER(LibWSUtil.Buffer))]

    wtapng_block_t = wtapng_block_s

    # typedef gboolean (*block_reader)(FILE_T, guint32, gboolean, wtapng_block_t *,
    #                                  int *, gchar **);
    block_reader = CFUNCTYPE(LibGLib2.gboolean,
                             FILE_T,
                             LibGLib2.guint32,
                             LibGLib2.gboolean,
                             POINTER(wtapng_block_t),
                             POINTER(c_int),
                             POINTER(LibGLib2.gchar_p))

    # typedef gboolean (*block_writer)(wtap_dumper *, const wtap_rec *,
    #                                  const guint8 *, int *);
    block_writer = CFUNCTYPE(LibGLib2.gboolean,
                             POINTER(wtap_dumper),
                             POINTER(wtap_rec),
                             POINTER(LibGLib2.guint8),
                             POINTER(c_int))

    # typedef gboolean (*option_handler_fn)(gboolean, guint, guint8 *, int *,
    # gchar **);
    option_handler_fn = CFUNCTYPE(LibGLib2.gboolean,
                                  LibGLib2.gboolean,
                                  LibGLib2.guint,
                                  POINTER(LibGLib2.guint8),
                                  POINTER(c_int),
                                  POINTER(LibGLib2.gchar_p))

    # typedef gboolean (*subtype_read_func)(struct wtap*, wtap_rec *,
    # Buffer *, int *, char **, gint64 *);
    subtype_read_func = CFUNCTYPE(LibGLib2.gboolean,
                                  POINTER(wtap),
                                  POINTER(wtap_rec),
                                  POINTER(LibWSUtil.Buffer),
                                  POINTER(c_int),
                                  POINTER(c_char_p),
                                  POINTER(LibGLib2.gint64))

    # typedef gboolean (*subtype_seek_read_func)(struct wtap*, gint64, wtap_rec *,
    #                                            Buffer *, int *, char **);
    subtype_seek_read_func = CFUNCTYPE(LibGLib2.gboolean,
                                       POINTER(wtap),
                                       LibGLib2.gint64,
                                       POINTER(wtap_rec),
                                       POINTER(LibWSUtil.Buffer),
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
                     ('ispipe', LibGLib2.gboolean),
                     ('file_type_subtype', c_int),
                     ('snapshot_length', LibGLib2.guint),
                     ('shb_hdrs', POINTER(LibGLib2.GArray)),
                     ('interface_data', POINTER(LibGLib2.GArray)),
                     ('nrb_hdrs', POINTER(LibGLib2.GArray)),
                     ('dsbs', POINTER(LibGLib2.GArray)),
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
                     ('fast_seek', POINTER(LibGLib2.GPtrArray))]

    # typedef void *WFILE_T;
    WFILE_T = c_void_p

    # typedef gboolean (*subtype_write_func)(struct wtap_dumper*,
    #                                        const wtap_rec *rec,
    #                                        const guint8*, int*, gchar**);
    subtype_write_func = CFUNCTYPE(LibGLib2.gboolean,
                                   POINTER(wtap_dumper),
                                   POINTER(wtap_rec),
                                   POINTER(LibGLib2.guint8),
                                   POINTER(c_int),
                                   POINTER(LibGLib2.gchar_p))

    # typedef gboolean (*subtype_finish_func)(struct wtap_dumper*, int*);
    subtype_finish_func = CFUNCTYPE(LibGLib2.gboolean,
                                    POINTER(wtap_dumper),
                                    POINTER(c_int))

    # struct wtap_dumper {
    #     WFILE_T                 fh;
    #     int                     file_type_subtype;
    #     int                     snaplen;
    #     int                     encap;
    #     wtap_compression_type   compression_type;
    #     gboolean                needs_reload;
    #     gint64                  bytes_dumped;
    #     void                    *priv;
    #     void                    *wslua_data;
    #     subtype_write_func      subtype_write;
    #     subtype_finish_func     subtype_finish;
    #     addrinfo_lists_t        *addrinfo_lists;
    #     GArray                  *shb_hdrs;
    #     GArray                  *nrb_hdrs;
    #     GArray                  *interface_data;
    #     GArray                  *dsbs_initial;
    #     const GArray            *dsbs_growing;
    #     guint                   dsbs_growing_written;
    # };
    wtap_dumper._fields_ = [('fh', WFILE_T),
                            ('file_type_subtype', c_int),
                            ('snaplen', c_int),
                            ('encap', c_int),
                            ('compression_type', wtap_compression_type),
                            ('needs_reload', LibGLib2.gboolean),
                            ('bytes_dumped', LibGLib2.gint64),
                            ('priv', c_void_p),
                            ('wslua_data', c_void_p),
                            ('subtype_write', subtype_write_func),
                            ('subtype_finish', subtype_finish_func),
                            ('addrinfo_lists', POINTER(addrinfo_lists_t)),
                            ('shb_hdrs', POINTER(LibGLib2.GArray)),
                            ('nrb_hdrs', POINTER(LibGLib2.GArray)),
                            ('interface_data', POINTER(LibGLib2.GArray)),
                            ('dsbs_initial', POINTER(LibGLib2.GArray)),
                            ('dsbs_growing', POINTER(LibGLib2.GArray)),
                            ('dsbs_growing_written', LibGLib2.guint)]

    #######################
    # MACROS/INLINE FUNCS #
    #######################

    # wtap_opttype_return_val
    # wtap_block_add_string_option_format(wtap_block_t block, guint option_id,
    # const char *format, ...)

    def wtap_block_add_string_option_format(
            self, block, option_id, format, *argv):
        args, types = c_va_list(*argv)
        _wtap_block_add_string_option_format = self.dll.wtap_block_add_string_option_format
        _wtap_block_add_string_option_format.restype = self.wtap_opttype_return_val
        _wtap_block_add_string_option_format.argtypes = [
            self.wtap_block_t, LibGLib2.guint, c_char_p] + types
        return _wtap_block_add_string_option_format(
            block, option_id, format, *args)

    # wtap_opttype_return_val
    # wtap_block_set_string_option_value_format(wtap_block_t block, guint
    # option_id, const char *format, ...)

    def wtap_block_set_string_option_value_fromat(
            self, block, option_id, format, *argv):
        args, types = c_va_list(*argv)
        _wtap_block_set_string_option_value_format = self.wtap_block_set_string_option_value_format
        _wtap_block_set_string_option_value_format.restype = self.wtap_opttype_return_val
        _wtap_block_set_string_option_value_format.argtypes = [
            self.wtap_block_t, LibGLib2.guint, c_char_p] + types
        return _wtap_block_set_string_option_value_format(
            block, option_id, format, *args)

    # #define IS_80211AD(frequency) (((frequency) >= PHDR_802_11AD_MIN_FREQUENCY) &&\
    #                                ((frequency) <= PHDR_802_11AD_MAX_FREQUENCY))

    def IS_80211AD(self, frequency):
        return frequency.value >= self.PHDR_802_11AD_MIN_FREQUENCY and frequency.value <= self.PHDR_802_11AD_MAX_FREQUENCY

    # #define PACK_FLAGS_DIRECTION(pack_flags) (((pack_flags) & PACK_FLAGS_DIRECTION_MASK) >> PACK_FLAGS_DIRECTION_SHIFT)

    def PACK_FLAGS_DIRECTION(self, pack_flags):
        return (pack_flags.value &
                self.PACK_FLAGS_DIRECTION_MASK) >> self.PACK_FLAGS_DIRECTION_SHIFT

    # #define PACK_FLAGS_RECEPTION_TYPE(pack_flags) (((pack_flags) & PACK_FLAGS_RECEPTION_TYPE_MASK) >> PACK_FLAGS_RECEPTION_TYPE_SHIFT)

    def PACK_FLAGS_RECEPTION_TYPE(self, pack_flags):
        return (pack_flags.value &
                self.PACK_FLAGS_RECEPTION_TYPE_MASK) >> self.PACK_FLAGS_RECEPTION_TYPE_SHIFT

    # #define PACK_FLAGS_FCS_LENGTH(pack_flags) (((pack_flags) & PACK_FLAGS_FCS_LENGTH_MASK) >> PACK_FLAGS_FCS_LENGTH_SHIFT)

    def PACK_FLAGS_FCS_LENGTH(self, pack_flags):
        return (pack_flags.value &
                self.PACK_FLAGS_FCS_LENGTH_MASK) >> self.PACK_FLAGS_FCS_LENGTH_SHIFT

    # #define PACK_FLAGS_VALUE(direction, reception_type, fcs_length, ll_dependent_errors) \
    #     (((direction) << 30) | \
    #     ((reception_type) << 27) | \
    #     ((fcs_length) << 23) | \
    #     (ll_dependent_errors))

    def PACK_FLAGS_VALUE(
            self,
            direction,
            reception_type,
            fcs_length,
            ll_dependent_errors):
        return LibGLib2.guint32((
            direction.value << 30) | (
            reception_type.value << 27) | (
                fcs_length.value << 23) | ll_dependend_errors.value)

    # #define PBSWAP64(p) \
    #     {            \
    #         guint8 tmp;        \
    #         tmp = (p)[7];      \
    #         (p)[7] = (p)[0];   \
    #         (p)[0] = tmp;      \
    #         tmp = (p)[6];      \
    #         (p)[6] = (p)[1];   \
    #         (p)[1] = tmp;      \
    #         tmp = (p)[5];      \
    #         (p)[5] = (p)[2];   \
    #         (p)[2] = tmp;      \
    #         tmp = (p)[4];      \
    #         (p)[4] = (p)[3];   \
    #         (p)[3] = tmp;      \
    #     }

    def PBSWAP64(self, p):
        tmp = p[7]
        p[7] = p[0]
        p[0] = tmp
        tmp = p[6]
        p[6] = p[1]
        p[1] = tmp
        tmp = p[5]
        p[5] = p[2]
        p[2] = tmp
        tmp = p[4]
        p[4] = p[3]
        p[3] = tmp

    # #define PBSWAP32(p) \
    #     {            \
    #         guint8 tmp;         \
    #         tmp = (p)[3];       \
    #         (p)[3] = (p)[0];    \
    #         (p)[0] = tmp;       \
    #         tmp = (p)[2];       \
    #         (p)[2] = (p)[1];    \
    #         (p)[1] = tmp;       \
    #     }

    def PBSWAP32(self, p):
        tmp = p[3]
        p[3] = p[0]
        p[0] = tmp
        tmp = p[2]
        p[2] = p[1]
        p[1] = tmp

    # #define PBSWAP16(p) \
    #     {            \
    #         guint8 tmp;        \
    #         tmp = (p)[1];      \
    #         (p)[1] = (p)[0];   \
    #         (p)[0] = tmp;      \
    #     }

    def PBSWAP16(self, p):
        tmp = p[1]
        p[1] = p[0]
        p[0] = tmp

    # #define phtons(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 8);    \
    #         (p)[1] = (guint8)((v) >> 0);    \
    #     }

    def phtons(self, p, v):
        p[0] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        p[1] = LibGLib2.guint8(v.value & 0xFF)

    # #define phton24(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 16);    \
    #         (p)[1] = (guint8)((v) >> 8);     \
    #         (p)[2] = (guint8)((v) >> 0);     \
    #     }

    def phton24(self, p, v):
        p[0] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        p[1] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        p[2] = LibGLib2.guint8(v.value & 0xFF)

    # #define phtonl(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 24);    \
    #         (p)[1] = (guint8)((v) >> 16);    \
    #         (p)[2] = (guint8)((v) >> 8);     \
    #         (p)[3] = (guint8)((v) >> 0);     \
    #     }

    def phtonl(self, p, v):
        p[0] = LibGLib2.guint8((v.value >> 24) & 0xFF)
        p[1] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        p[2] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        p[3] = LibGLib2.guint8(v.value & 0xFF)

    # #define phtonll(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 56);    \
    #         (p)[1] = (guint8)((v) >> 48);    \
    #         (p)[2] = (guint8)((v) >> 40);    \
    #         (p)[3] = (guint8)((v) >> 32);    \
    #         (p)[4] = (guint8)((v) >> 24);    \
    #         (p)[5] = (guint8)((v) >> 16);    \
    #         (p)[6] = (guint8)((v) >> 8);     \
    #         (p)[7] = (guint8)((v) >> 0);     \
    #     }

    def phtonll(self, p, v):
        p[0] = LibGLib2.guint8((v.value >> 56) & 0xFF)
        p[1] = LibGLib2.guint8((v.value >> 48) & 0xFF)
        p[2] = LibGLib2.guint8((v.value >> 40) & 0xFF)
        p[3] = LibGLib2.guint8((v.value >> 32) & 0xFF)
        p[4] = LibGLib2.guint8((v.value >> 24) & 0xFF)
        p[5] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        p[6] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        p[7] = LibGLib2.guint8(v.value & 0xFF)

    # #define phtole8(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 0);    \
    #     }

    def phtole8(self, p, v):
        p[0] = LibGLib2.guint8(v.value & 0xFF)

    # #define phtoles(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 0);    \
    #         (p)[1] = (guint8)((v) >> 8);    \
    #     }

    def phtoles(self, p, v):
        p[0] = LibGLib2.guint8(v.value & 0xFF)
        p[1] = LibGLib2.guint8((v.value >> 8) & 0xFF)

    # #define phtole24(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 0);     \
    #         (p)[1] = (guint8)((v) >> 8);     \
    #         (p)[2] = (guint8)((v) >> 16);    \
    #     }

    def phtole24(self, p, v):
        p[0] = LibGLib2.guint8(v.value & 0xFF)
        p[1] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        p[2] = LibGLib2.guint8((v.value >> 16) & 0xFF)

    # #define phtolel(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 0);     \
    #         (p)[1] = (guint8)((v) >> 8);     \
    #         (p)[2] = (guint8)((v) >> 16);    \
    #         (p)[3] = (guint8)((v) >> 24);    \
    #     }

    def phtolel(self, p, v):
        p[0] = LibGLib2.guint8(v.value & 0xFF)
        p[1] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        p[2] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        p[3] = LibGLib2.guint8((v.value >> 24) & 0xFF)

    # #define phtolell(p, v) \
    #     {                 \
    #         (p)[0] = (guint8)((v) >> 0);     \
    #         (p)[1] = (guint8)((v) >> 8);     \
    #         (p)[2] = (guint8)((v) >> 16);    \
    #         (p)[3] = (guint8)((v) >> 24);    \
    #         (p)[4] = (guint8)((v) >> 32);    \
    #         (p)[5] = (guint8)((v) >> 40);    \
    #         (p)[6] = (guint8)((v) >> 48);    \
    #         (p)[7] = (guint8)((v) >> 56);    \
    #     }

    def phtolell(self, p, v):
        p[0] = LibGLib2.guint8(v.value & 0xFF)
        p[1] = LibGLib2.guint8((v.value >> 8) & 0xFF)
        p[2] = LibGLib2.guint8((v.value >> 16) & 0xFF)
        p[3] = LibGLib2.guint8((v.value >> 24) & 0xFF)
        p[4] = LibGLib2.guint8((v.value >> 32) & 0xFF)
        p[5] = LibGLib2.guint8((v.value >> 40) & 0xFF)
        p[6] = LibGLib2.guint8((v.value >> 48) & 0xFF)
        p[7] = LibGLib2.guint8((v.value >> 56) & 0xFF)

    # #define g_ptr_array_len(a)      ((a)->len)

    def g_ptr_array_len(self, a):
        return a[0].len

    def __init__(self, libpath=config.get_libwiretap()):
        libwiretap = CDLL(config.get_libwiretap())
        self.dll = libwiretap

        # void wtap_opttypes_initialize(void);
        self.wtap_opttypes_initialize = libwiretap.wtap_opttypes_initialize
        self.wtap_opttypes_initialize.restype = None
        self.wtap_opttypes_initialize.argtypes = []

        # wtap_block_t wtap_block_create(wtap_block_type_t block_type);
        self.wtap_block_create = libwiretap.wtap_block_create
        self.wtap_block_create.restype = self.wtap_block_t
        self.wtap_block_create.argtypes = [self.wtap_block_type_t]

        # void wtap_block_free(wtap_block_t block);
        self.wtap_block_free = libwiretap.wtap_block_free
        self.wtap_block_free.restype = None
        self.wtap_block_free.argtypes = [self.wtap_block_t]

        # void wtap_block_array_free(GArray* block_array);
        self.wtap_block_array_free = libwiretap.wtap_block_array_free
        self.wtap_block_array_free.restype = None
        self.wtap_block_array_free.argtypes = [POINTER(LibGLib2.GArray)]

        # void* wtap_block_get_mandatory_data(wtap_block_t block);
        self.wtap_block_get_mandatory_data = libwiretap.wtap_block_get_mandatory_data
        self.wtap_block_get_mandatory_data.restype = c_void_p
        self.wtap_block_get_mandatory_data.argtypes = [self.wtap_block_t]

        # wtap_opttype_return_val
        # wtap_block_add_uint8_option(wtap_block_t block, guint option_id, guint8
        # value);
        self.wtap_block_add_uint8_option = libwiretap.wtap_block_add_uint8_option
        self.wtap_block_add_uint8_option.restype = self.wtap_opttype_return_val
        self.wtap_block_add_uint8_option.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint8]

        # wtap_opttype_return_val
        # wtap_block_set_uint8_option_value(wtap_block_t block, guint option_id,
        # guint8 value);
        self.wtap_block_set_uint8_option_value = libwiretap.wtap_block_set_uint8_option_value
        self.wtap_block_set_uint8_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_set_uint8_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint8]

        # wtap_opttype_return_val
        # wtap_block_get_uint8_option_value(wtap_block_t block, guint option_id,
        # guint8* value);
        self.wtap_block_get_uint8_option_value = libwiretap.wtap_block_get_uint8_option_value
        self.wtap_block_get_uint8_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_get_uint8_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(LibGLib2.guint8)]

        # wtap_opttype_return_val
        # wtap_block_add_uint64_option(wtap_block_t block, guint option_id,
        # guint64 value);
        self.wtap_block_add_uint64_option = libwiretap.wtap_block_add_uint64_option
        self.wtap_block_add_uint64_option.restype = self.wtap_opttype_return_val
        self.wtap_block_add_uint64_option.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint64]

        # wtap_opttype_return_val
        # wtap_block_set_uint64_option_value(wtap_block_t block, guint option_id,
        # guint64 value);
        self.wtap_block_set_uint64_option_value = libwiretap.wtap_block_set_uint64_option_value
        self.wtap_block_set_uint64_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_set_uint64_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint64]

        # wtap_opttype_return_val
        # wtap_block_get_uint64_option_value(wtap_block_t block, guint option_id,
        # guint64* value);
        self.wtap_block_get_uint64_option_value = libwiretap.wtap_block_get_uint64_option_value
        self.wtap_block_get_uint64_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_get_uint64_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(LibGLib2.guint64)]

        # wtap_opttype_return_val
        # wtap_block_add_ipv4_option(wtap_block_t block, guint option_id, guint32
        # value);
        self.wtap_block_add_ipv4_option = libwiretap.wtap_block_add_ipv4_option
        self.wtap_block_add_ipv4_option.restype = self.wtap_opttype_return_val
        self.wtap_block_add_ipv4_option.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint32]

        # wtap_opttype_return_val
        # wtap_block_set_ipv4_option_value(wtap_block_t block, guint option_id,
        # guint32 value);
        self.wtap_block_set_ipv4_option_value = libwiretap.wtap_block_set_ipv4_option_value
        self.wtap_block_set_ipv4_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_set_ipv4_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint32]

        # wtap_opttype_return_val
        # wtap_block_get_ipv4_option_value(wtap_block_t block, guint option_id,
        # guint32* value);
        self.wtap_block_get_ipv4_option_value = libwiretap.wtap_block_get_ipv4_option_value
        self.wtap_block_get_ipv4_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_get_ipv4_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(LibGLib2.guint32)]

        # wtap_opttype_return_val
        # wtap_block_add_ipv6_option(wtap_block_t block, guint option_id,
        # ws_in6_addr *value);
        self.wtap_block_add_ipv6_option = libwiretap.wtap_block_add_ipv6_option
        self.wtap_block_add_ipv6_option.restype = self.wtap_opttype_return_val
        self.wtap_block_add_ipv6_option.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(LibWSUtil.ws_in6_addr)]

        # wtap_opttype_return_val
        # wtap_block_set_ipv6_option_value(wtap_block_t block, guint option_id,
        # ws_in6_addr *value);
        self.wtap_block_set_ipv6_option_value = libwiretap.wtap_block_set_ipv6_option_value
        self.wtap_block_set_ipv6_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_set_ipv6_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(LibWSUtil.ws_in6_addr)]

        # wtap_opttype_return_val
        # wtap_block_get_ipv6_option_value(wtap_block_t block, guint option_id,
        # ws_in6_addr* value);
        self.wtap_block_get_ipv6_option_value = libwiretap.wtap_block_get_ipv6_option_value
        self.wtap_block_get_ipv6_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_get_ipv6_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(LibWSUtil.ws_in6_addr)]

        # wtap_opttype_return_val
        # wtap_block_add_string_option(wtap_block_t block, guint option_id, const
        # char *value, gsize value_length);
        self.wtap_block_add_string_option = libwiretap.wtap_block_add_string_option
        self.wtap_block_add_string_option.restype = self.wtap_opttype_return_val
        self.wtap_block_add_string_option.argtypes = [
            self.wtap_block_t, LibGLib2.guint, c_char_p, LibGLib2.gsize]

        # wtap_opttype_return_val
        # wtap_block_set_string_option_value(wtap_block_t block, guint option_id,
        # const char* value, gsize value_length);
        self.wtap_block_set_string_option_value = libwiretap.wtap_block_set_string_option_value
        self.wtap_block_set_string_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_set_string_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, c_char_p]

        # wtap_opttype_return_val
        # wtap_block_set_nth_string_option_value(wtap_block_t block, guint
        # option_id, guint idx, const char* value, gsize value_length);
        self.wtap_block_set_nth_string_option_value = libwiretap.wtap_block_set_nth_string_option_value
        self.wtap_block_set_nth_string_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_set_nth_string_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint, c_char_p, LibGLib2.gsize]

        # wtap_opttype_return_val
        # wtap_block_get_string_option_value(wtap_block_t block, guint option_id,
        # char** value);
        self.wtap_block_get_string_option_value = libwiretap.wtap_block_get_string_option_value
        self.wtap_block_get_string_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_get_string_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(c_char_p)]

        # wtap_opttype_return_val
        # wtap_block_get_nth_string_option_value(wtap_block_t block, guint
        # option_id, guint idx, char** value);
        self.wtap_block_get_nth_string_option_value = libwiretap.wtap_block_get_nth_string_option_value
        self.wtap_block_get_nth_string_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_get_nth_string_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint, POINTER(c_char_p)]

        # wtap_opttype_return_val
        # wtap_block_add_custom_option(wtap_block_t block, guint option_id, void*
        # value, size_t value_size);
        self.wtap_block_add_custom_option = libwiretap.wtap_block_add_custom_option
        self.wtap_block_add_custom_option.restype = self.wtap_opttype_return_val
        self.wtap_block_add_custom_option.argtypes = [
            self.wtap_block_t, LibGLib2.guint, c_void_p, c_size_t]

        # wtap_opttype_return_val
        # wtap_block_set_custom_option_value(wtap_block_t block, guint option_id,
        # void* value);
        self.wtap_block_set_custom_option_value = libwiretap.wtap_block_set_custom_option_value
        self.wtap_block_set_custom_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_set_custom_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, c_void_p]

        # wtap_opttype_return_val
        # wtap_block_get_custom_option_value(wtap_block_t block, guint option_id,
        # void** value);
        self.wtap_block_get_custom_option_value = libwiretap.wtap_block_get_custom_option_value
        self.wtap_block_get_custom_option_value.restype = self.wtap_opttype_return_val
        self.wtap_block_get_custom_option_value.argtypes = [
            self.wtap_block_t, LibGLib2.guint, POINTER(c_void_p)]

        # wtap_opttype_return_val
        # wtap_block_remove_option(wtap_block_t block, guint option_id);
        self.wtap_block_remove_option = libwiretap.wtap_block_remove_option
        self.wtap_block_remove_option.restype = self.wtap_opttype_return_val
        self.wtap_block_remove_option.argtypes = [
            self.wtap_block_t, LibGLib2.guint]

        # wtap_opttype_return_val
        # wtap_block_remove_nth_option_instance(wtap_block_t block, guint option_id,
        #                                       guint idx);
        self.wtap_block_remove_nth_option_instance = libwiretap.wtap_block_remove_nth_option_instance
        self.wtap_block_remove_nth_option_instance.restype = self.wtap_opttype_return_val
        self.wtap_block_remove_nth_option_instance.argtypes = [
            self.wtap_block_t, LibGLib2.guint, LibGLib2.guint]

        # void wtap_block_copy(wtap_block_t dest_block, wtap_block_t
        # src_block);
        self.wtap_block_copy = libwiretap.wtap_block_copy
        self.wtap_block_copy.restype = None
        self.wtap_block_copy.argtypes = [self.wtap_block_t, self.wtap_block_t]

        # void wtap_block_foreach_option(wtap_block_t block,
        # wtap_block_foreach_func func, void* user_data);
        self.wtap_block_foreach_option = libwiretap.wtap_block_foreach_option
        self.wtap_block_foreach_option.restype = None
        self.wtap_block_foreach_option.argtypes = [
            self.wtap_block_t, self.wtap_block_foreach_func, c_void_p]

        # int wtap_opttype_register_custom_block_type(const char* name, const char* description, wtap_block_create_func create,
        # wtap_mand_free_func free_mand, wtap_mand_copy_func copy_mand);
        self.wtap_opttype_register_custom_block_type = libwiretap.wtap_opttype_register_custom_block_type
        self.wtap_opttype_register_custom_block_type.restype = c_int
        self.wtap_opttype_register_custom_block_type.argtypes = [
            c_char_p,
            c_char_p,
            self.wtap_block_create_func,
            self.wtap_mand_free_func,
            self.wtap_mand_copy_func]

        # void wtap_opttypes_cleanup(void);
        self.wtap_opttypes_cleanup = libwiretap.wtap_opttypes_cleanup
        self.wtap_opttypes_cleanup.restype = None
        self.wtap_opttypes_cleanup.argtypes = []

        # void init_open_routines(void);
        self.init_open_routines = libwiretap.init_open_routines
        self.init_open_routines.restype = None
        self.init_open_routines.argtypes = []

        # struct open_info *open_routines;
        self.open_routines = POINTER(
            self.open_info).in_dll(
            libwiretap,
            'open_routines')

        # void wtap_init(gboolean load_wiretap_plugins);
        self.wtap_init = libwiretap.wtap_init
        self.wtap_init.restype = None
        self.wtap_init.argtypes = [LibGLib2.gboolean]

        # struct wtap* wtap_open_offline(const char *filename, unsigned int type, int *err,
        #     gchar **err_info, gboolean do_random);
        self.wtap_open_offline = libwiretap.wtap_open_offline
        self.wtap_open_offline.restype = POINTER(self.wtap)
        self.wtap_open_offline.argtypes = [c_char_p,
                                           c_uint,
                                           POINTER(c_int),
                                           POINTER(LibGLib2.gchar_p),
                                           LibGLib2.gboolean]

        # void wtap_cleareof(wtap *wth);
        self.wtap_cleareof = libwiretap.wtap_cleareof
        self.wtap_cleareof.restype = None
        self.wtap_cleareof.argtypes = [POINTER(self.wtap)]

        # void wtap_set_cb_new_ipv4(wtap *wth, wtap_new_ipv4_callback_t
        # add_new_ipv4);
        self.wtap_set_cb_new_ipv4 = libwiretap.wtap_set_cb_new_ipv4
        self.wtap_set_cb_new_ipv4.restype = None
        self.wtap_set_cb_new_ipv4.argtypes = [
            POINTER(self.wtap), self.wtap_new_ipv4_callback_t]

        # void wtap_set_cb_new_ipv6(wtap *wth, wtap_new_ipv6_callback_t
        # add_new_ipv6);
        self.wtap_set_cb_new_ipv6 = libwiretap.wtap_set_cb_new_ipv6
        self.wtap_set_cb_new_ipv6.restype = None
        self.wtap_set_cb_new_ipv6.argtypes = [
            POINTER(self.wtap), self.wtap_new_ipv6_callback_t]

        # void wtap_set_cb_new_secrets(wtap *wth, wtap_new_secrets_callback_t
        # add_new_secrets);
        self.wtap_set_cb_new_secrets = libwiretap.wtap_set_cb_new_secrets
        self.wtap_set_cb_new_secrets.restype = None
        self.wtap_set_cb_new_secrets.argtypes = [
            POINTER(self.wtap), self.wtap_new_secrets_callback_t]

        # gboolean wtap_read(wtap *wth, wtap_rec *rec, Buffer *buf, int *err,
        #     gchar **err_info, gint64 *offset);
        self.wtap_read = libwiretap.wtap_read
        self.wtap_read.restype = LibGLib2.gboolean
        self.wtap_read.argtypes = [POINTER(self.wtap),
                                   POINTER(self.wtap_rec),
                                   POINTER(LibWSUtil.Buffer),
                                   POINTER(c_int),
                                   POINTER(LibGLib2.gchar_p),
                                   POINTER(LibGLib2.gint64)]

        # gboolean wtap_seek_read(wtap *wth, gint64 seek_off, wtap_rec *rec,
        #     Buffer *buf, int *err, gchar **err_info);
        self.wtap_seek_read = libwiretap.wtap_seek_read
        self.wtap_seek_read.restype = LibGLib2.gboolean
        self.wtap_seek_read.argtypes = [POINTER(self.wtap),
                                        LibGLib2.gint64,
                                        POINTER(self.wtap_rec),
                                        POINTER(LibWSUtil.Buffer),
                                        POINTER(c_int),
                                        POINTER(LibGLib2.gchar_p)]

        # void wtap_rec_init(wtap_rec *rec);
        self.wtap_rec_init = libwiretap.wtap_rec_init
        self.wtap_rec_init.restype = None
        self.wtap_rec_init.argtypes = [POINTER(self.wtap_rec)]

        # void wtap_rec_cleanup(wtap_rec *rec);
        self.wtap_rec_cleanup = libwiretap.wtap_rec_cleanup
        self.wtap_rec_cleanup.restype = None
        self.wtap_rec_cleanup.argtypes = [POINTER(self.wtap_rec)]

        # wtap_compression_type wtap_get_compression_type(wtap *wth);
        self.wtap_get_compression_type = libwiretap.wtap_get_compression_type
        self.wtap_get_compression_type.restype = self.wtap_compression_type
        self.wtap_get_compression_type.argtypes = [POINTER(self.wtap)]

        # const char *wtap_compression_type_description(wtap_compression_type
        # compression_type);
        self.wtap_compression_type_description = libwiretap.wtap_compression_type_description
        self.wtap_compression_type_description.restype = c_char_p
        self.wtap_compression_type_description.argtypes = [
            self.wtap_compression_type]

        # const char *wtap_compression_type_extension(wtap_compression_type
        # compression_type);
        self.wtap_compression_type_extension = libwiretap.wtap_compression_type_extension
        self.wtap_compression_type_extension.restype = c_char_p
        self.wtap_compression_type_extension.argtypes = [
            self.wtap_compression_type]

        # GSList *wtap_get_all_compression_type_extensions_list(void);
        self.wtap_get_all_compression_type_extensions_list = libwiretap.wtap_get_all_compression_type_extensions_list
        self.wtap_get_all_compression_type_extensions_list.restype = POINTER(
            LibGLib2.GSList)
        self.wtap_get_all_compression_type_extensions_list.argtypes = []

        # gint64 wtap_read_so_far(wtap *wth);
        self.wtap_read_so_far = libwiretap.wtap_read_so_far
        self.wtap_read_so_far.restype = LibGLib2.gint64
        self.wtap_read_so_far.argtypes = [POINTER(self.wtap)]

        # gint64 wtap_file_size(wtap *wth, int *err);
        self.wtap_file_size = libwiretap.wtap_file_size
        self.wtap_file_size.restype = LibGLib2.gint64
        self.wtap_file_size.argtypes = [POINTER(self.wtap), POINTER(c_int)]

        # guint wtap_snapshot_length(wtap *wth);
        self.wtap_snapshot_length = libwiretap.wtap_snapshot_length
        self.wtap_snapshot_length.restype = LibGLib2.guint
        self.wtap_snapshot_length.argtypes = [POINTER(self.wtap)]

        # int wtap_file_type_subtype(wtap *wth);
        self.wtap_file_type_subtype = libwiretap.wtap_file_type_subtype
        self.wtap_file_type_subtype.restype = c_int
        self.wtap_file_type_subtype.argtypes = [POINTER(self.wtap)]

        # int wtap_file_encap(wtap *wth);
        self.wtap_file_encap = libwiretap.wtap_file_encap
        self.wtap_file_encap.restype = c_int
        self.wtap_file_encap.argtypes = [POINTER(self.wtap)]

        # int wtap_file_tsprec(wtap *wth);
        self.wtap_file_tsprec = libwiretap.wtap_file_tsprec
        self.wtap_file_tsprec.restype = c_int
        self.wtap_file_tsprec.argtypes = [POINTER(self.wtap)]

        # guint wtap_file_get_num_shbs(wtap *wth);
        #wtap_file_get_num_shbs = libwiretap.wtap_file_get_num_shbs
        #wtap_file_get_num_shbs.restype = LibGLib2.guint
        #wtap_file_get_num_shbs.argtypes = [POINTER(wtap)]

        # wtap_block_t wtap_file_get_shb(wtap *wth, guint shb_num);
        self.wtap_file_get_shb = libwiretap.wtap_file_get_shb
        self.wtap_file_get_shb.restype = self.wtap_block_t
        self.wtap_file_get_shb.argtypes = [POINTER(self.wtap), LibGLib2.guint]

        # GArray* wtap_file_get_shb_for_new_file(wtap *wth);
        self.wtap_file_get_shb_for_new_file = libwiretap.wtap_file_get_shb_for_new_file
        self.wtap_file_get_shb_for_new_file.restype = POINTER(LibGLib2.GArray)
        self.wtap_file_get_shb_for_new_file.argtypes = [POINTER(self.wtap)]

        # void wtap_write_shb_comment(wtap *wth, gchar *comment);
        self.wtap_write_shb_comment = libwiretap.wtap_write_shb_comment
        self.wtap_write_shb_comment.restype = None
        self.wtap_write_shb_comment.argtypes = [
            POINTER(self.wtap), LibGLib2.gchar_p]

        # wtapng_iface_descriptions_t *wtap_file_get_idb_info(wtap *wth);
        self.wtap_file_get_idb_info = libwiretap.wtap_file_get_idb_info
        self.wtap_file_get_idb_info.restype = POINTER(
            self.wtapng_iface_descriptions_t)
        self.wtap_file_get_idb_info.argtypes = [POINTER(self.wtap)]

        # void wtap_free_idb_info(wtapng_iface_descriptions_t *idb_info);
        self.wtap_free_idb_info = libwiretap.wtap_free_idb_info
        self.wtap_free_idb_info.restype = None
        self.wtap_free_idb_info.argtypes = [
            POINTER(self.wtapng_iface_descriptions_t)]

        # gchar *wtap_get_debug_if_descr(const wtap_block_t if_descr,
        #                                const int indent,
        #                                const char* line_end);
        self.wtap_get_debug_if_descr = libwiretap.wtap_get_debug_if_descr
        self.wtap_get_debug_if_descr.restype = LibGLib2.gchar_p
        self.wtap_get_debug_if_descr.argtypes = [
            self.wtap_block_t, c_int, c_char_p]

        # wtap_block_t wtap_file_get_nrb(wtap *wth);
        self.wtap_file_get_nrb = libwiretap.wtap_file_get_nrb
        self.wtap_file_get_nrb.restype = self.wtap_block_t
        self.wtap_file_get_nrb.argtypes = [POINTER(self.wtap)]

        # GArray* wtap_file_get_nrb_for_new_file(wtap *wth);
        self.wtap_file_get_nrb_for_new_file = libwiretap.wtap_file_get_nrb_for_new_file
        self.wtap_file_get_nrb_for_new_file.restype = POINTER(LibGLib2.GArray)
        self.wtap_file_get_nrb_for_new_file.argtypes = [POINTER(self.wtap)]

        # void wtap_fdclose(wtap *wth);
        self.wtap_fdclose = libwiretap.wtap_fdclose
        self.wtap_fdclose.restype = None
        self.wtap_fdclose.argtypes = [POINTER(self.wtap)]

        # gboolean wtap_fdreopen(wtap *wth, const char *filename, int *err);
        self.wtap_fdreopen = libwiretap.wtap_fdreopen
        self.wtap_fdreopen.restype = LibGLib2.gboolean
        self.wtap_fdreopen.argtypes = [
            POINTER(self.wtap), c_char_p, POINTER(c_int)]

        # void wtap_sequential_close(wtap *wth);
        self.wtap_sequential_close = libwiretap.wtap_sequential_close
        self.wtap_sequential_close.restype = None
        self.wtap_sequential_close.argtypes = [POINTER(self.wtap)]

        # void wtap_close(wtap *wth);
        self.wtap_close = libwiretap.wtap_close
        self.wtap_close.restype = None
        self.wtap_close.argtypes = [POINTER(self.wtap)]

        # gboolean wtap_dump_can_open(int filetype);
        self.wtap_dump_can_open = libwiretap.wtap_dump_can_open
        self.wtap_dump_can_open.restype = LibGLib2.gboolean
        self.wtap_dump_can_open.argtypes = [c_int]

        # int wtap_dump_file_encap_type(const GArray *file_encaps);
        self.wtap_dump_file_encap_type = libwiretap.wtap_dump_file_encap_type
        self.wtap_dump_file_encap_type.restype = c_int
        self.wtap_dump_file_encap_type.argtypes = [POINTER(LibGLib2.GArray)]

        # gboolean wtap_dump_can_compress(int filetype);
        self.wtap_dump_can_compress = libwiretap.wtap_dump_can_compress
        self.wtap_dump_can_compress.restype = LibGLib2.gboolean
        self.wtap_dump_can_compress.argtypes = [c_int]

        # gboolean wtap_dump_has_name_resolution(int filetype);
        self.wtap_dump_has_name_resolution = libwiretap.wtap_dump_has_name_resolution
        self.wtap_dump_has_name_resolution.restype = LibGLib2.gboolean
        self.wtap_dump_has_name_resolution.argtypes = [c_uint]

        # gboolean wtap_dump_supports_comment_types(int filetype, guint32
        # comment_types);
        self.wtap_dump_supports_comment_types = libwiretap.wtap_dump_supports_comment_types
        self.wtap_dump_supports_comment_types.restype = LibGLib2.gboolean
        self.wtap_dump_supports_comment_types.argtypes = [
            c_int, LibGLib2.guint32]

        # void wtap_dump_params_init(wtap_dump_params *params, wtap *wth);
        self.wtap_dump_params_init = libwiretap.wtap_dump_params_init
        self.wtap_dump_params_init.restype = None
        self.wtap_dump_params_init.argtypes = [
            POINTER(
                self.wtap_dump_params), POINTER(
                self.wtap)]

        # void wtap_dump_params_discard_decryption_secrets(wtap_dump_params
        # *params);
        self.wtap_dump_params_discard_decryption_secrets = libwiretap.wtap_dump_params_discard_decryption_secrets
        self.wtap_dump_params_discard_decryption_secrets.restype = None
        self.wtap_dump_params_discard_decryption_secrets.argtypes = [
            POINTER(self.wtap_dump_params)]

        # void wtap_dump_params_cleanup(wtap_dump_params *params);
        self.wtap_dump_params_cleanup = libwiretap.wtap_dump_params_cleanup
        self.wtap_dump_params_cleanup.restype = None
        self.wtap_dump_params_cleanup.argtypes = [
            POINTER(self.wtap_dump_params)]

        # wtap_dumper* wtap_dump_open(const char *filename, int file_type_subtype,
        #     wtap_compression_type compression_type, const wtap_dump_params *params,
        #     int *err);
        self.wtap_dump_open = libwiretap.wtap_dump_open
        self.wtap_dump_open.restype = POINTER(self.wtap_dumper)
        self.wtap_dump_open.argtypes = [c_char_p,
                                        c_int,
                                        self.wtap_compression_type,
                                        POINTER(self.wtap_dump_params),
                                        POINTER(c_int)]

        # wtap_dumper* wtap_dump_open_tempfile(char **filenamep, const char *pfx,
        #     int file_type_subtype, wtap_compression_type compression_type,
        #     const wtap_dump_params *params, int *err);
        self.wtap_dump_open_tempfile = libwiretap.wtap_dump_open_tempfile
        self.wtap_dump_open_tempfile.restype = POINTER(self.wtap_dumper)
        self.wtap_dump_open_tempfile.argtypes = [
            POINTER(c_char_p), c_char_p, c_int, self.wtap_compression_type, POINTER(
                self.wtap_dump_params), POINTER(c_int)]

        # wtap_dumper* wtap_dump_fdopen(int fd, int file_type_subtype,
        #     wtap_compression_type compression_type, const wtap_dump_params *params,
        #     int *err);
        self.wtap_dump_fdopen = libwiretap.wtap_dump_fdopen
        self.wtap_dump_fdopen.restype = POINTER(self.wtap_dumper)
        self.wtap_dump_fdopen.argtypes = [c_int,
                                          c_int,
                                          self.wtap_compression_type,
                                          POINTER(self.wtap_dump_params),
                                          POINTER(c_int)]

        # wtap_dumper* wtap_dump_open_stdout(int file_type_subtype,
        #     wtap_compression_type compression_type, const wtap_dump_params *params,
        #     int *err);
        self.wtap_dump_open_stdout = libwiretap.wtap_dump_open_stdout
        self.wtap_dump_open_stdout.restype = POINTER(self.wtap_dumper)
        self.wtap_dump_open_stdout.argtypes = [c_int,
                                               self.wtap_compression_type,
                                               POINTER(self.wtap_dump_params),
                                               POINTER(c_int)]

        # gboolean wtap_dump(wtap_dumper *, const wtap_rec *, const guint8 *,
        #      int *err, gchar **err_info);
        self.wtap_dump = libwiretap.wtap_dump
        self.wtap_dump.restype = LibGLib2.gboolean
        self.wtap_dump.argtypes = [POINTER(self.wtap_dumper),
                                   POINTER(self.wtap_rec),
                                   POINTER(LibGLib2.guint8),
                                   POINTER(c_int),
                                   POINTER(LibGLib2.gchar_p)]

        # void wtap_dump_flush(wtap_dumper *);
        self.wtap_dump_flush = libwiretap.wtap_dump_flush
        self.wtap_dump_flush.restype = None
        self.wtap_dump_flush.argtypes = [POINTER(self.wtap_dumper)]

        # gint64 wtap_get_bytes_dumped(wtap_dumper *);
        self.wtap_get_bytes_dumped = libwiretap.wtap_get_bytes_dumped
        self.wtap_get_bytes_dumped.restype = LibGLib2.gint64
        self.wtap_get_bytes_dumped.argtypes = [POINTER(self.wtap_dumper)]

        # void wtap_set_bytes_dumped(wtap_dumper *wdh, gint64 bytes_dumped);
        self.wtap_set_bytes_dumped = libwiretap.wtap_set_bytes_dumped
        self.wtap_set_bytes_dumped.restype = None
        self.wtap_set_bytes_dumped.argtypes = [
            POINTER(self.wtap_dumper), LibGLib2.gint64]

        # gboolean wtap_addrinfo_list_empty(addrinfo_lists_t *addrinfo_lists);
        self.wtap_addrinfo_list_empty = libwiretap.wtap_addrinfo_list_empty
        self.wtap_addrinfo_list_empty.restype = LibGLib2.gboolean
        self.wtap_addrinfo_list_empty.argtypes = [
            POINTER(self.addrinfo_lists_t)]

        # gboolean wtap_dump_set_addrinfo_list(wtap_dumper *wdh, addrinfo_lists_t
        # *addrinfo_lists);
        self.wtap_dump_set_addrinfo_list = libwiretap.wtap_dump_set_addrinfo_list
        self.wtap_dump_set_addrinfo_list.restype = LibGLib2.gboolean
        self.wtap_dump_set_addrinfo_list.argtypes = [
            POINTER(self.wtap_dumper), POINTER(self.addrinfo_lists_t)]

        # gboolean wtap_dump_get_needs_reload(wtap_dumper *wdh);
        self.wtap_dump_get_needs_reload = libwiretap.wtap_dump_get_needs_reload
        self.wtap_dump_get_needs_reload.restype = LibGLib2.gboolean
        self.wtap_dump_get_needs_reload.argtypes = [POINTER(self.wtap_dumper)]

        # void wtap_dump_discard_decryption_secrets(wtap_dumper *wdh);
        self.wtap_dump_discard_decryption_secrets = libwiretap.wtap_dump_discard_decryption_secrets
        self.wtap_dump_discard_decryption_secrets.restype = None
        self.wtap_dump_discard_decryption_secrets.argtypes = [
            POINTER(self.wtap_dumper)]

        # gboolean wtap_dump_close(wtap_dumper *wdh, int *err);
        self.wtap_dump_close = libwiretap.wtap_dump_close
        self.wtap_dump_close.restype = LibGLib2.gboolean
        self.wtap_dump_close.argtypes = [
            POINTER(self.wtap_dumper), POINTER(c_int)]

        # gboolean wtap_dump_can_write(const GArray *file_encaps, guint32
        # required_comment_types);
        self.wtap_dump_can_write = libwiretap.wtap_dump_can_write
        self.wtap_dump_can_write.restype = LibGLib2.gboolean
        self.wtap_dump_can_write.argtypes = [
            POINTER(LibGLib2.GArray), LibGLib2.guint32]

        # GArray *wtap_get_savable_file_types_subtypes(int file_type,
        #     const GArray *file_encaps, guint32 required_comment_types);
        self.wtap_get_savable_file_types_subtypes = libwiretap.wtap_get_savable_file_types_subtypes
        self.wtap_get_savable_file_types_subtypes.restype = POINTER(
            LibGLib2.GArray)
        self.wtap_get_savable_file_types_subtypes.argtypes = [
            c_int, POINTER(LibGLib2.GArray), LibGLib2.guint32]

        # const char *wtap_file_type_subtype_string(int file_type_subtype);
        self.wtap_file_type_subtype_string = libwiretap.wtap_file_type_subtype_string
        self.wtap_file_type_subtype_string.restype = c_char_p
        self.wtap_file_type_subtype_string.argtypes = [c_int]

        # const char *wtap_file_type_subtype_short_string(int
        # file_type_subtype);
        self.wtap_file_type_subtype_short_string = libwiretap.wtap_file_type_subtype_short_string
        self.wtap_file_type_subtype_short_string.restype = c_char_p
        self.wtap_file_type_subtype_short_string.argtypes = [c_int]

        # int wtap_short_string_to_file_type_subtype(const char *short_name);
        self.wtap_short_string_to_file_type_subtype = libwiretap.wtap_short_string_to_file_type_subtype
        self.wtap_short_string_to_file_type_subtype.restype = c_int
        self.wtap_short_string_to_file_type_subtype.argtypes = [c_char_p]

        # GSList *wtap_get_all_capture_file_extensions_list(void);
        self.wtap_get_all_capture_file_extensions_list = libwiretap.wtap_get_all_capture_file_extensions_list
        self.wtap_get_all_capture_file_extensions_list.restype = POINTER(
            LibGLib2.GSList)
        self.wtap_get_all_capture_file_extensions_list.argtypes = []

        # const char *wtap_default_file_extension(int filetype);
        self.wtap_default_file_extension = libwiretap.wtap_default_file_extension
        self.wtap_default_file_extension.restype = c_char_p
        self.wtap_default_file_extension.argtypes = [c_int]

        # GSList *wtap_get_file_extensions_list(int filetype, gboolean
        # include_compressed);
        self.wtap_get_file_extensions_list = libwiretap.wtap_get_file_extensions_list
        self.wtap_get_file_extensions_list.restype = POINTER(LibGLib2.GSList)
        self.wtap_get_file_extensions_list.argtypes = [
            c_int, LibGLib2.gboolean]

        # GSList *wtap_get_all_file_extensions_list(void);
        self.wtap_get_all_file_extensions_list = libwiretap.wtap_get_all_file_extensions_list
        self.wtap_get_all_file_extensions_list.restype = POINTER(
            LibGLib2.GSList)
        self.wtap_get_all_file_extensions_list.argtypes = []

        # void wtap_free_extensions_list(GSList *extensions);
        self.wtap_free_extensions_list = libwiretap.wtap_free_extensions_list
        self.wtap_free_extensions_list.restype = None
        self.wtap_free_extensions_list.argtypes = [POINTER(LibGLib2.GSList)]

        # const char *wtap_encap_name(int encap);
        self.wtap_encap_name = libwiretap.wtap_encap_name
        self.wtap_encap_name.restype = c_char_p
        self.wtap_encap_name.argtypes = [c_int]

        # const char *wtap_encap_description(int encap);
        self.wtap_encap_description = libwiretap.wtap_encap_description
        self.wtap_encap_description.restype = c_char_p
        self.wtap_encap_description.argtypes = [c_int]

        # int wtap_name_to_encap(const char *short_name);
        self.wtap_name_to_encap = libwiretap.wtap_name_to_encap
        self.wtap_name_to_encap.restype = c_int
        self.wtap_name_to_encap.argtypes = [c_char_p]

        # const char* wtap_tsprec_string(int tsprec);
        self.wtap_tsprec_string = libwiretap.wtap_tsprec_string
        self.wtap_tsprec_string.restype = c_char_p
        self.wtap_tsprec_string.argtypes = [c_int]

        # const char *wtap_strerror(int err);
        self.wtap_strerror = libwiretap.wtap_strerror
        self.wtap_strerror.restype = c_char_p
        self.wtap_strerror.argtypes = [c_int]

        # int wtap_get_num_file_type_extensions(void);
        self.wtap_get_num_file_type_extensions = libwiretap.wtap_get_num_file_type_extensions
        self.wtap_get_num_file_type_extensions.restype = c_int
        self.wtap_get_num_file_type_extensions.argtypes = []

        # int wtap_get_num_encap_types(void);
        self.wtap_get_num_encap_types = libwiretap.wtap_get_num_encap_types
        self.wtap_get_num_encap_types.restype = c_int
        self.wtap_get_num_encap_types.argtypes = []

        # int wtap_get_num_file_types_subtypes(void);
        self.wtap_get_num_file_types_subtypes = libwiretap.wtap_get_num_file_types_subtypes
        self.wtap_get_num_file_types_subtypes.restype = c_int
        self.wtap_get_num_file_types_subtypes.argtypes = []

        # const char *wtap_get_file_extension_type_name(int extension_type);
        self.wtap_get_file_extension_type_name = libwiretap.wtap_get_file_extension_type_name
        self.wtap_get_file_extension_type_name.restype = c_char_p
        self.wtap_get_file_extension_type_name.argtypes = [c_int]

        # GSList *wtap_get_file_extension_type_extensions(guint
        # extension_type);
        self.wtap_get_file_extension_type_extensions = libwiretap.wtap_get_file_extension_type_extensions
        self.wtap_get_file_extension_type_extensions.restype = POINTER(
            LibGLib2.GSList)
        self.wtap_get_file_extension_type_extensions.argtypes = [
            LibGLib2.guint]

        # void wtap_register_file_type_extension(const struct
        # file_extension_info *ei);
        self.wtap_register_file_type_extension = libwiretap.wtap_register_file_type_extension
        self.wtap_register_file_type_extension.restype = None
        self.wtap_register_file_type_extension.argtypes = [
            POINTER(self.file_extension_info)]

        # void wtap_register_plugin(const wtap_plugin *plug);
        self.wtap_register_plugin = libwiretap.wtap_register_plugin
        self.wtap_register_plugin.restype = None
        self.wtap_register_plugin.argtypes = [POINTER(self.wtap_plugin)]

        # void wtap_register_open_info(struct open_info *oi, const gboolean
        # first_routine);
        self.wtap_register_open_info = libwiretap.wtap_register_open_info
        self.wtap_register_open_info.restype = None
        self.wtap_register_open_info.argtypes = [
            POINTER(self.open_info), LibGLib2.gboolean]

        # gboolean wtap_has_open_info(const gchar *name);
        self.wtap_has_open_info = libwiretap.wtap_has_open_info
        self.wtap_has_open_info.restype = LibGLib2.gboolean
        self.wtap_has_open_info.argtypes = [LibGLib2.gchar_p]

        # void wtap_deregister_open_info(const gchar *name);
        self.wtap_deregister_open_info = libwiretap.wtap_deregister_open_info
        self.wtap_deregister_open_info.restype = None
        self.wtap_deregister_open_info.argtypes = [LibGLib2.gchar_p]

        # unsigned int open_info_name_to_type(const char *name);
        self.open_info_name_to_type = libwiretap.open_info_name_to_type
        self.open_info_name_to_type.restype = c_uint
        self.open_info_name_to_type.argtypes = [c_char_p]

        # int wtap_register_file_type_subtypes(const struct
        # file_type_subtype_info* fi, const int subtype);
        self.wtap_register_file_type_subtypes = libwiretap.wtap_register_file_type_subtypes
        self.wtap_register_file_type_subtypes.restype = c_int
        self.wtap_register_file_type_subtypes.argtypes = [
            POINTER(self.file_type_subtype_info), c_int]

        # void wtap_deregister_file_type_subtype(const int file_type_subtype);
        self.wtap_deregister_file_type_subtype = libwiretap.wtap_deregister_file_type_subtype
        self.wtap_deregister_file_type_subtype.restype = None
        self.wtap_deregister_file_type_subtype.argtypes = [c_int]

        # int wtap_register_encap_type(const char *description, const char
        # *name);
        self.wtap_register_encap_type = libwiretap.wtap_register_encap_type
        self.wtap_register_encap_type.restype = c_int
        self.wtap_register_encap_type.argtypes = [c_char_p, c_char_p]

        # void wtap_cleanup(void);
        self.wtap_cleanup = libwiretap.wtap_cleanup
        self.wtap_cleanup.restype = None
        self.wtap_cleanup.argtypes = []

        # gint64 file_seek(FILE_T stream, gint64 offset, int whence, int *err);
        self.file_seek = libwiretap.file_seek
        self.file_seek.restype = LibGLib2.gint64
        self.file_seek.argtypes = [
            self.FILE_T,
            LibGLib2.gint64,
            c_int,
            POINTER(c_int)]

        # gint64 file_tell(FILE_T stream);
        self.file_tell = libwiretap.file_tell
        self.file_tell.restype = LibGLib2.gint64
        self.file_tell.argtypes = [self.FILE_T]

        # gboolean file_iscompressed(FILE_T stream);
        self.file_iscompressed = libwiretap.file_iscompressed
        self.file_iscompressed.restype = LibGLib2.gboolean
        self.file_iscompressed.argtypes = [self.FILE_T]

        # int file_read(void *buf, unsigned int count, FILE_T file);
        self.file_read = libwiretap.file_read
        self.file_read.restype = c_int
        self.file_read.argtypes = [c_void_p, c_uint, self.FILE_T]

        # int file_peekc(FILE_T stream);
        self.file_peekc = libwiretap.file_peekc
        self.file_peekc.restype = c_int
        self.file_peekc.argtypes = [self.FILE_T]

        # int file_getc(FILE_T stream);
        self.file_getc = libwiretap.file_getc
        self.file_getc.restype = c_int
        self.file_getc.argtypes = [self.FILE_T]

        # char *file_gets(char *buf, int len, FILE_T stream);
        self.file_gets = libwiretap.file_gets
        self.file_gets.restype = c_char_p
        self.file_gets.argtypes = [c_char_p, c_int, self.FILE_T]

        # char *file_getsp(char *buf, int len, FILE_T stream);
        self.file_getsp = libwiretap.file_getsp
        self.file_getsp.restype = c_char_p
        self.file_getsp.argtypes = [c_char_p, c_int, self.FILE_T]

        # int file_eof(FILE_T stream);
        self.file_eof = libwiretap.file_eof
        self.file_eof.restype = c_int
        self.file_eof.argtypes = [self.FILE_T]

        # int file_error(FILE_T fh, gchar **err_info);
        self.file_error = libwiretap.file_error
        self.file_error.restype = c_int
        self.file_error.argtypes = [self.FILE_T, POINTER(LibGLib2.gchar_p)]

        # idb_merge_mode merge_string_to_idb_merge_mode(const char *name);
        self.merge_string_to_idb_merge_mode = libwiretap.merge_string_to_idb_merge_mode
        self.merge_string_to_idb_merge_mode.restype = self.idb_merge_mode
        self.merge_string_to_idb_merge_mode.argtypes = [c_char_p]

        # const char* merge_idb_merge_mode_to_string(const int mode);
        self.merge_idb_merge_mode_to_string = libwiretap.merge_idb_merge_mode_to_string
        self.merge_idb_merge_mode_to_string.restype = c_char_p
        self.merge_idb_merge_mode_to_string.argtypes = [c_int]

        # merge_result
        # merge_files(const gchar* out_filename, const int file_type,
        #             const char *const *in_filenames, const guint in_file_count,
        #             const gboolean do_append, const idb_merge_mode mode,
        #             guint snaplen, const gchar *app_name, merge_progress_callback_t* cb,
        #             int *err, gchar **err_info, guint *err_fileno,
        #             guint32 *err_framenum);
        self.merge_files = libwiretap.merge_files
        self.merge_files.restype = self.merge_result
        self.merge_files.argtypes = [LibGLib2.gchar_p,
                                     c_int,
                                     POINTER(c_char_p),
                                     LibGLib2.guint,
                                     LibGLib2.gboolean,
                                     self.idb_merge_mode,
                                     LibGLib2.guint, LibGLib2.gchar_p,
                                     POINTER(self.merge_progress_callback_t),
                                     POINTER(c_int),
                                     POINTER(LibGLib2.gchar_p),
                                     POINTER(LibGLib2.guint),
                                     POINTER(LibGLib2.guint32)]

        # merge_result
        # merge_files_to_tempfile(gchar **out_filenamep, const char *pfx,
        #                         const int file_type, const char *const *in_filenames,
        #                         const guint in_file_count, const gboolean do_append,
        #                         const idb_merge_mode mode, guint snaplen,
        #                         const gchar *app_name, merge_progress_callback_t* cb,
        #                         int *err, gchar **err_info, guint *err_fileno,
        #                         guint32 *err_framenum);
        self.merge_files_to_tempfile = libwiretap.merge_files_to_tempfile
        self.merge_files_to_tempfile.restype = self.merge_result
        self.merge_files_to_tempfile.argtypes = [
            POINTER(
                LibGLib2.gchar_p),
            c_char_p,
            c_int,
            POINTER(c_char_p),
            LibGLib2.guint,
            LibGLib2.gboolean,
            self.idb_merge_mode,
            LibGLib2.guint,
            LibGLib2.gchar_p,
            POINTER(
                self.merge_progress_callback_t),
            POINTER(c_int),
            POINTER(
                LibGLib2.gchar_p),
            POINTER(
                LibGLib2.guint),
            POINTER(
                LibGLib2.guint32)]

        # merge_result
        # merge_files_to_stdout(const int file_type, const char *const *in_filenames,
        #                       const guint in_file_count, const gboolean do_append,
        #                       const idb_merge_mode mode, guint snaplen,
        #                       const gchar *app_name, merge_progress_callback_t* cb,
        #                       int *err, gchar **err_info, guint *err_fileno,
        #                       guint32 *err_framenum);
        self.merge_files_to_stdout = libwiretap.merge_files_to_stdout
        self.merge_files_to_stdout.restype = self.merge_result
        self.merge_files_to_stdout.argtypes = [
            c_int,
            POINTER(c_char_p),
            LibGLib2.guint,
            LibGLib2.gboolean,
            self.idb_merge_mode,
            LibGLib2.guint,
            LibGLib2.gchar_p,
            POINTER(
                self.merge_progress_callback_t),
            POINTER(c_int),
            POINTER(
                LibGLib2.gchar_p),
            POINTER(
                LibGLib2.guint),
            POINTER(
                LibGLib2.guint32)]

        # int wtap_pcap_encap_to_wtap_encap(int encap);
        self.wtap_pcap_encap_to_wtap_encap = libwiretap.wtap_pcap_encap_to_wtap_encap
        self.wtap_pcap_encap_to_wtap_encap.restype = c_int
        self.wtap_pcap_encap_to_wtap_encap.argtypes = [c_int]

        # int wtap_wtap_encap_to_pcap_encap(int encap);
        self.wtap_wtap_encap_to_pcap_encap = libwiretap.wtap_wtap_encap_to_pcap_encap
        self.wtap_wtap_encap_to_pcap_encap.restype = c_int
        self.wtap_wtap_encap_to_pcap_encap.argtypes = [c_int]

        # gboolean wtap_encap_requires_phdr(int encap);
        self.wtap_encap_requires_phdr = libwiretap.wtap_encap_requires_phdr
        self.wtap_encap_requires_phdr.restype = LibGLib2.gboolean
        self.wtap_encap_requires_phdr.argtypes = [c_int]

        # void register_pcapng_block_type_handler(guint block_type, block_reader reader,
        #                                         block_writer writer);
        self.register_pcapng_block_type_handler = libwiretap.register_pcapng_block_type_handler
        self.register_pcapng_block_type_handler.restype = None
        self.register_pcapng_block_type_handler.argtypes = [
            LibGLib2.guint, self.block_reader, self.block_writer]

        # void register_pcapng_option_handler(guint block_type, guint option_code,
        #                                     option_handler_fn hfunc);
        self.register_pcapng_option_handler = libwiretap.register_pcapng_option_handler
        self.register_pcapng_option_handler.restype = None
        self.register_pcapng_option_handler.argtypes = [
            LibGLib2.guint, LibGLib2.guint, self.option_handler_fn]

        # int wtap_fstat(wtap *wth, ws_statb64 *statb, int *err);
        self.wtap_fstat = libwiretap.wtap_fstat
        self.wtap_fstat.restype = c_int
        self.wtap_fstat.argtypes = [
            POINTER(
                self.wtap), POINTER(
                LibWSUtil.ws_statb64), POINTER(c_int)]

        # gboolean wtap_dump_file_write(wtap_dumper *wdh, const void *buf,
        #     size_t bufsize, int *err);
        self.wtap_dump_file_write = libwiretap.wtap_dump_file_write
        self.wtap_dump_file_write.restype = LibGLib2.gboolean
        self.wtap_dump_file_write.argtypes = [POINTER(self.wtap_dumper),
                                              c_void_p,
                                              c_size_t,
                                              POINTER(c_int)]

        # gint64 wtap_dump_file_seek(wtap_dumper *wdh, gint64 offset, int whence,
        # int *err);
        self.wtap_dump_file_seek = libwiretap.wtap_dump_file_seek
        self.wtap_dump_file_seek.restype = LibGLib2.gint64
        self.wtap_dump_file_seek.argtypes = [POINTER(self.wtap_dumper),
                                             LibGLib2.gint64,
                                             c_int,
                                             POINTER(c_int)]

        # gint64 wtap_dump_file_tell(wtap_dumper *wdh, int *err);
        self.wtap_dump_file_tell = libwiretap.wtap_dump_file_tell
        self.wtap_dump_file_tell.restype = LibGLib2.gint64
        self.wtap_dump_file_tell.argtypes = [
            POINTER(self.wtap_dumper), POINTER(c_int)]

        # gboolean
        # wtap_read_bytes_or_eof(FILE_T fh, void *buf, unsigned int count, int *err,
        #     gchar **err_info);
        self.wtap_read_bytes_or_eof = libwiretap.wtap_read_bytes_or_eof
        self.wtap_read_bytes_or_eof.restype = LibGLib2.gboolean
        self.wtap_read_bytes_or_eof.argtypes = [
            self.FILE_T, c_void_p, c_uint, POINTER(c_int), POINTER(
                LibGLib2.gchar_p)]

        # gboolean
        # wtap_read_bytes(FILE_T fh, void *buf, unsigned int count, int *err,
        #     gchar **err_info);
        self.wtap_read_bytes = libwiretap.wtap_read_bytes
        self.wtap_read_bytes.restype = LibGLib2.gboolean
        self.wtap_read_bytes.argtypes = [
            self.FILE_T,
            c_void_p,
            c_uint,
            POINTER(c_int),
            POINTER(
                LibGLib2.gchar_p)]

        # gboolean
        # wtap_read_packet_bytes(FILE_T fh, Buffer *buf, guint length, int *err,
        #     gchar **err_info);
        self.wtap_read_packet_bytes = libwiretap.wtap_read_packet_bytes
        self.wtap_read_packet_bytes.restype = LibGLib2.gboolean
        self.wtap_read_packet_bytes.argtypes = [self.FILE_T,
                                                POINTER(LibWSUtil.Buffer),
                                                LibGLib2.guint,
                                                POINTER(c_int),
                                                POINTER(LibGLib2.gchar_p)]
