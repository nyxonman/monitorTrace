from sys import exit, argv
import sys
import signal
import os
import subprocess
import socket
import time
from datetime import datetime
import argparse
import csv
import random

# list of global variables subject to change
glob = {
    'QUIT': False,
}

MIN_A7_VER = (10, 0, 519)

OS_POSIX = "posix"
OS_WIN = "nt"
__VERSION__ = "2.0"
APP_VERSION = __VERSION__ + " {OS: " + os.name + "}"
OUTPUT_FILE_NAME = "lastdecodedTraces"
OUTPUT_FILE_EXT = ".log"

# pings
if os.name == OS_POSIX:
    PING_CMD = 'ping'
    PING_CMD_XTRA = ''
    PING_CNT = '-c'
    PING_SIZE = '-s'
    PING_INTV = '-i'
    PING_RESP_TIME = '-W'
    CLEAR_CMD = 'clear'


elif os.name == OS_WIN:
    PING_CMD = 'ping'
    PING_CMD_XTRA = ''
    PING_CNT = '-n'
    PING_SIZE = '-l'
    PING_INTV = '-i'  # OS_WIN does not support this
    PING_RESP_TIME = '-w'
    CLEAR_CMD = 'cls'

RET_SUCC = 0
RET_FAIL = -1
POLL_INTERVAL = 10  # in seconds

SDU_TX_SUCCESS = 0
SDU_TX_FAILURE = -1

ID_ALL = 0
ID_PRIM = 1
ID_STS = 2
ID_TRACE = 3
ID_FLAG = 4
ID_OWNERS = 5
ID_MAX = 6

graphs = {
    'rtt': {},
    'cl_timing': {},
    'timeline': {}
}

tracing_events_num_str = {
    0: "LMMGR_PRE_IND",
    1: "LMMGR_PHR_IND",
    2: "LMMGR_FC_IND",
    3: "LMMGR_EDI_IND",
    4: "LMMGR_DATA_IND",
    5: "LMMGR_DATA_REQ",
    6: "LMMGR_DATA_CONF",
    7: "CHMGR_ACK_REQ",
    8: "CHMGR_ACK_CONF",
    9: "CHMGR_MCPS_REQ",
    10: "CHMGR_MCPS_CONF",
    11: "CHMGR_CSMA_START",
    12: "CHMGR_CSMA_CW",
    13: "CHMGR_CSMA_PCS",
    14: "CHMGR_DBR_RECV",
    15: "CHMGR_DBR_DB_SEND",
    16: "CHMGR_SBR_RECV",
    17: "CHMGR_SBR_SB_SEND",
    18: "CHMGR_HB_REQ",
    19: "BUFMGR_GET",
    20: "BUFMGR_RELEASE",
    21: "HW_GPIO",
    22: "CHMGR_VCS_TX_SET",
    23: "SYS_STARTUP",
    24: "THREADX_EXEC_CHANGE_NOTIFY",
    25: "CHMGR_SBR_REQ",
    26: "SYS_EXCEPTION",
    27: "SYS_EXCEPTION_DUMP_START",
    28: "SYS_EXCEPTION_DUMP_END",
    29: "SYS_EXCEPTION_REBOOTING",
    30: "ALINK_DL_IRQ",
    31: "ALINK_DL_DMA",
    32: "ALINK_DL_CB",
    33: "ALINK_UL_TIMEOUT",
    34: "CHMGR_REQ_HOLD",
    35: "CHMGR_REQ_RELEASE",
    36: "MACMGR_BINDRX",
    37: "MACMGR_BINDTX",
    38: "WATCHDOG_ISR",
    39: "CHMGR_HB_TX",
    40: "CHMGR_ACK_IND_CRC",
    41: "CHMGR_ACK_REQ_CRC",
    42: "SYS_MEMORY_INTEGRITY_FAIL",
    43: "CHMGR_ALE_RX",
    44: "CHMGR_ALE_TX",
    45: "CHMGR_TIMESLOT_START",
    46: "CHMGR_RX_TX_FRAME_KIND",
    47: "CHMGR_RX_TX_SHR_BEGIN_TIME",
    48: "CHMGR_RX_TX_FULL_DURATION",
    49: "CHMGR_RX_TX_SEQ_NUM",
    50: "LMMGR_NHL_DATA_IN",
    51: "LMMGR_NHL_MGMNT_IN",
    53: "LMFS_EXTEND_SCH_ENTRY",
    54: "LMFS_EXTEND_SCH_EXIT",
    55: "LMFS_ADD_SCH_ENTRY",
    56: "LMFS_ADD_SCH_EXIT",
    57: "LMMGR_HWTIMER",
    58: "LMMGR_SWTIMER",
    59: "PHYTST_DATA_CONF",
    62: "PHY_CALLBACKS_CLAIM",
    63: "PHY_CALLBACKS_RELEASE",
    64: "LMFS_REMOVE_SCH_ENTRY",
    65: "LMFS_REMOVE_SCH_EXIT",
    68: "HSM_EVENT",
    68: "HSM_EVENT_ENTRY",
    69: "HSM_EVENT_INITIAL",
    70: "HSM_EVENT_DO",
    71: "HSM_EVENT_EXIT",
    72: "HSM_EVENT_LMFS_TIMER",
    73: "HSM_EVENT_LMSM_TIMER",
    74: "HSM_EVENT_FH_TIMER",
    75: "HSM_EVENT_START_FH",
    76: "HSM_EVENT_SCH_START",
    77: "HSM_EVENT_SCH_END",
    78: "HSM_EVENT_PHY_CCA",
    79: "HSM_EVENT_PHY_PHR",
    80: "HSM_EVENT_PHY_FC",
    81: "HSM_EVENT_PHY_EDI",
    82: "HSM_EVENT_PHY_DIND",
    83: "HSM_EVENT_PHY_DCONF",
    84: "HSM_EVENT_EPF",
    85: "HSM_EVENT_EPF_EARLY",
    86: "HSM_EVENT_EPF_RESTORE",
    87: "FH",
    88: "FH_NEXT_HOP_DUR",
    89: "FH_HOP_TMR_TIMEOUT",
    90: "FH_ET",
    91: "RXB",
    92: "RXB_HSM",
    93: "UPCALL_CALL",
    94: "UPCALL_INVALID_ID",
    95: "UPCALL_INVALID_CB",
    96: "CLT_MACADDR_L",
    97: "CLT_MACADDR_H",
    98: "CLT_EPOCH_START_L",
    99: "CLT_EPOCH_START_H",
    100: "CLT_DESIRED_TXTIME_L",
    101: "CLT_DESIRED_TXTIME_H",
    102: "CLT_PEER_EPOCHLEN",
    103: "CLT_PEER_TIME_IN_EPOCH",
    104: "CLT_PEER_TIME_IN_SLOT",
    105: "CLT_DRIFT",
    106: "CLT_LWIN",
    107: "CLT_RWIN",
    108: "CLT_TARGET_SLOT",
    109: "CLT_CH",
    110: "CLT_TXDELAY",
    111: "CLT_PEER_CURSLOT",
    112: "CLT_RWIN_QUALTIME",
    120: "CLT_RESERVED",
    121: "FRT32_TX_START",
    122: "FRT32_TX_END",
    123: "FRT32_RX_START",
    124: "FRT32_RX_END",
    129: "CL_FRT32_TX_CALL",
    130: "CL_FRT32_RX_CALL",
    131: "CL_NEW",
    132: "CL_END",
    133: "CL_OUT_REQ",
    134: "CL_OUT_CNF",
    135: "CL_IN",
    136: "CL_START",
    137: "CL_SEND_PRIMITIVE",
    138: "CL_REGISTER_SCH",
    139: "CL_TXDONE",
    140: "CL_TX",
    141: "CL_RX",
    142: "CL_NEXT_CLI",
    143: "CL_NEXT_RX_TX",
    144: "CL_SEQ_CTRL",
    145: "CL_CANCEL_SCH",
    146: "CL_PDLL_FLAGS",
    147: "CL_PEER_MAC_ADDR",
    148: "CL_DATA_REQ",
    149: "CL_DATA_RESP",
    150: "CL_PTR",
    151: "CL_DEBUG",
    152: "TXB_STARTUP",
    153: "TXB_REGISTER_SCH",
    154: "TXB_SW_TIMER",
    155: "TXB_GET_REQ",
    156: "TXB_GET_CNF",
    157: "TXB_IND",
    158: "TXB_START",
    159: "TXB_NEXT",
    160: "TXB_FAST",
    172: "TXB_DEBUG",
    173: "BCAST_HAPPY_RETURN",
    174: "BCAST_ERROR_RETURN",
    180: "BCAST_CONF_STS",
    181: "BCAST_IND_STS",
    182: "BCAST_CHID_PSDULEN",
    183: "BCAST_TXTIME_FRT_L",
    184: "BCAST_TXTIME_FRT_H",
    185: "BCAST_DATALEN_PKTID",
    186: "BCAST_EXPIRY_FRT_L",
    187: "BCAST_EXPIRY_FRT_H",
    188: "BCAST_CHID_PRIMSEQNUM",
    189: "BCAST_CANCELLED_SCHID",
    200: "BCAST_RESERVED",
    201: "UPCALL_RX_TX_DELAY",
    211: "LMDC_ERROR",
    212: "RLT_LINK",
    213: "LDC_CHECK",
    214: "LDC_TXDUR_CUR",
    215: "LDC_WINDOW_SPAN",
    216: "LDC_WINDOW_BIN",
    217: "SDC_CHECK",
    218: "SDC_TXDUR_CUR",
    219: "SDC_WINDOW_SPAN",
    220: "SDC_WINDOW_BIN",
    221: "RLT_CHECK",
    222: "TTC_TOK_ADDED_SINCE_LAST_TX",
    223: "TTC_TOK_IN_BUCKET",
    224: "TTC_TOK_AVAILABLE",
    225: "TTC_TOK_ERROR",
    226: "RLT_RETRY",
    227: "LDC_UPDATE",
    228: "SDC_UPDATE",
    229: "TTC_TX_UPDATE",
    230: "TTC_TMR_CB",
    231: "LMDC_EEROR_LN",
    235: "LMDC_RESERVED",
    241: "SA_HAPPY_RETURN",
    242: "SA_ERROR_RETURN",
    243: "SA_HSM_HAPPY_RETURN",
    244: "SA_HSM_ERROR_RETURN",
    270: "SA_RESERVED",
    271: "ELG",
    272: "ELG_TIMER",
    273: "ELG_EVENT",
    290: "ELG_RESERVED",

}
tracing_events_str_num = {value: key for key, value in tracing_events_num_str.items()}
MAX_TRACE_EVT = list(tracing_events_num_str.keys())[-1] + 1

TRACING_DEBUG_MASK_LEN = int(MAX_TRACE_EVT/8) + 1

state_arr = [
    "LMSM_TOP",
    "LMSM_IDLE",
    "LMSM_FH",
    "LMSM_RXB",
    "LMSM_TXB",
    "LMSM_CL",
    "LMSM_BCAST",
    "LMSM_SA",
    "LMSM_LLS",
    "LMSM_ELG",
]

cl_substate_arr = {
    0: "CL_INCOMING",
    1: "CL_OUTGOING",
    2: "CL_WFR",
    10: "CL_WFR_TX2RX",
    11: "CL_WFR_PHR",
    12: "CL_WFR_FCTRL",
    13: "CL_WFR_EDI",
    14: "CL_WFR_DIND",
    15: "CL"
}

fh_substate_arr = [
    "FH_DO_NOTHING",
    "FH_WAIT_CCA",
    "FH_WAIT_PHR",
    "FH_WAIT_FC",
    "FH_WAIT_EDI",
    "FH_WAIT_DIND",
]

elg_substate_arr = [
    "ELG_PHR",
    "ELG_FC",
    "ELG_EDI",
    "ELG_DIND",
    "ELG_TX",
    "ELG_DCONF"
]

rxb_substate_arr = [
    "RXB_PHR",
    "RXB_FC",
    "RXB_EDI",
    "RXB_DIND"
]


owner_ids_arr = [
    "OID_INVALID",
    "OID_PIBENGINE",
    "OID_MACMGR",
    "OID_LMMGR",
    "OID_ALINK",
    "OID_PHYRX",
    "OID_PHYTX",
    "OID_SECURITY",
    "OID_DEBUG",
    "OID_SYSTEM",
    "OID_MNQ",
    "OID_LMFS",
    "OID_TXBCON",
    "OID_RXBCON",
    "OID_FH",
    "OID_SA",
    "OID_LLS",
    "OID_CL",
    "OID_ELG",
    "OID_TXBCAST",
    "OID_LMDC",
    "OID_PHYTST",
    "OID_MAX"
]

elg_code_str = {
    1: "ELG_TIMER_CB",
    2: "ELG_AC_LOSS_ISR",
    3: "ELG_EPF_ISR",
    50: "ELG_EPF_EVENTS_OFS",
}


elg_event_code_str = {
    0: "ELG_EV_INVALID",
    1: "ELG_EV_TIMER",
    2: "ELG_EV_AC_LOSS",
    3: "ELG_EV_AC_RESTORED",
    4: "ELG_EV_EPF",
    5: "ELG_EV_SFP_START",
    6: "ELG_EV_SFP_TXDONE",
    7: "ELG_EV_MOLF_WAKEUP",
    8: "ELG_EV_TX_BUNDLE",
    9: "ELG_EV_TX_BUNDLE_DONE",
    10: "ELG_EV_MAX",
}

sts_code_str = {
    0: "STS_SUCCESS",
    219: "STS_COUNTER_ERROR",
    220: "STS_IMPROPER_KEY_TYPE",
    221: "STS_IMPROPER_SECURITY_LEVEL",
    222: "STS_UNSUPPORTED_LEGACY",
    223: "STS_UNSUPPORTED_SECURITY",
    224: "STS_BEACON_LOSS",
    225: "STS_CHANNEL_ACCESS_FAILURE",
    226: "STS_DENIED",
    227: "STS_DISABLE_TRX_FAILURE",
    228: "STS_SECURITY_ERROR",
    229: "STS_FRAME_TOO_LONG",
    230: "STS_INVALID_GTS",
    231: "STS_INVALID_HANDLE",
    232: "STS_INVALID_PARAMETER",
    233: "STS_NO_ACK",
    234: "STS_NO_BEACON",
    235: "STS_NO_DATA",
    236: "STS_NO_SHORT_ADDRESS",
    237: "STS_OUT_OF_CAP",
    238: "STS_PAN_ID_CONFLICT",
    239: "STS_REALIGNMENT",
    240: "STS_TRANSACTION_EXPIRED",
    241: "STS_TRANSACTION_OVERFLOW",
    242: "STS_TX_ACTIVE",
    243: "STS_UNAVAILABLE_KEY",
    244: "STS_UNSUPPORTED_ATTRIBUTE",
    245: "STS_INVALID_ADDRESS",
    246: "STS_ON_TIME_TOO_LONG",
    247: "STS_PAST_TIME",
    248: "STS_TRACKING_OFF",
    249: "STS_INVALID_INDEX",
    250: "STS_LIMIT_REACHED",
    251: "STS_READ_ONLY",
    252: "STS_SCAN_IN_PROGRESS",
    253: "STS_SUPERFRAME_OVERLAP",
    255: "STS_RESERVED_MAC_PRIM",
    256: "STS_FAILURE",
    257: "STS_NACK_BUFFER_FULL",
    258: "STS_NACK_NO_CHANNEL",
    259: "STS_NACK_NOT_SYNC",
    260: "STS_NACK_SYNC_MAINTENANCE",
    261: "STS_NACK_RANK_INCONSISTENCY_UP",
    262: "STS_NACK_RANK_INCONSISTENCY_DOWN",
    263: "STS_NACK_LINK_EVAL",
    264: "STS_NACK_TLM_BUFFER_FULL",
    265: "STS_NACK_EARLIER_FRAGMENT",
    266: "STS_NACK_MIGRATED",
    267: "STS_NACK_DUPLICATED",
    268: "STS_NACK_WRONG_PAN",
    511: "STS_RESERVED_NAN_SPEC",
    512: "STS_INVALID_IE",
    513: "STS_INVALID_LAYER",
    514: "STS_INVALID_SIZE",
    515: "STS_PTR_INVALID",
    516: "STS_NOT_SUPPORTED",
    517: "STS_ACK_RCVD_NODSN_NOSA",
    518: "STS_BEACON_FRAME_SEG_HEADER_ERR",
    519: "STS_TONEMAP_RESPONSE_SEG_HEADER_ERR",
    520: "STS_FC_ERROR_FRAME_VER",
    521: "STS_FC_ERROR_FRAME_TYPE_RESERVED",
    522: "STS_FC_ERROR_PENDING",
    523: "STS_FC_ERROR_ACK_FRAME",
    524: "STS_FC_ERROR_ADDR_MODE",
    525: "STS_ERROR_EVENT_ID",
    526: "STS_DST_ADDR_ERROR_PAN_ID",
    527: "STS_DST_ADDR_ERROR_SHORT_ADDR",
    528: "STS_DST_ADDR_ERROR_EXT_ADDR",
    529: "STS_TX_ERROR_SPLIT_PACKET",
    530: "STS_TX_MSG_NOT_SUPPORTED",
    531: "STS_TX_ERR_PAYLOAD_ZERO",
    532: "STS_TX_DATA_TIMEOUT",
    533: "STS_TIMEOUT",
    534: "STS_TX_PENDING",
    535: "STS_RX_ERR_CRC16",
    536: "STS_RX_ERR_PAYLOAD_ZERO",
    537: "STS_RX_CCM_ERROR",
    538: "STS_BAD_CHANNEL",
    539: "STS_PHY_LAYER_FAILURE",
    540: "STS_NOT_CONFIGURED",
    541: "STS_NOT_SYNCHRONIZED",
    542: "STS_NOT_REGISTERED",
    543: "STS_INVALID_UTC",
    544: "STS_FSM_BUSY",
    545: "STS_TX_BUSY",
    546: "STS_SYNC_LOSS",
    547: "STS_TONE_MAP_NO_EXIST",
    548: "STS_TONE_MAP_AGED",
    549: "STS_NO_CALLBACK_FUNC",
    550: "STS_NO_ETT_COMP",
    551: "STS_REQUEST_PREEMPTED",
    552: "STS_NO_ETT_PROBE",
    553: "STS_LINK_EVAL_PENDING",
    554: "STS_NO_INPROGRESS_SERVICE",
    555: "STS_ERROR_OUT_OF_MARGIN",
    556: "STS_NOT_FOUND",
    557: "STS_PIB_EMPTY",
    558: "STS_NOTIFY_EXCEED_LIMIT",
    559: "STS_NOTIFY_DUPLICATE_FOUND",
    560: "STS_PROTECT_EXCEED_LIMIT",
    561: "STS_PROTECT_DUPLICATE_FOUND",
    562: "STS_MUTEX_FAIL",
    563: "STS_NO_POST_MSG_FUNC",
    564: "STS_ERR_POST_MESSAGE",
    565: "STS_MEMORY_FAILURE",
    566: "STS_BUFFER_ALLOC_FAILED",
    567: "STS_BUFFER_RELEASE_FAILED",
    568: "STS_BUFFER_TOO_LARGE",
    569: "STS_BUSY_SYNCING",
    570: "STS_ALREADY_TX",
    571: "STS_INVALID_BPD_SLOT",
    572: "STS_NACK_NO_CONNECTIVITY",
    573: "STS_BUFFER_TOO_SMALL",
    574: "STS_SHARED_INTEGRITY_TIMESTAMP_ERROR",
    575: "STS_LOCAL_INTEGRITY_TIMESTAMP_ERROR",
    576: "STS_REJECTED_REQUEST",
    577: "STS_DELAY",
    578: "STS_FRAME_INVALID",
    579: "STS_INADEQUATE_TIME",
    580: "STS_DLL_CRC_ERR",
    581: "STS_INPROGRESS",
    582: "STS_MAC_BACKOFF",
    583: "STS_FATAL_ERROR",
    584: "STS_RLT_TX_PKT_NOT_ALLOWED",
    585: "STS_RLT_TX_PKT_OK",
    586: "STS_RLT_TX_PKT_LAST",
}

txsts_code_str = {
    0: "SDU_TX_SUCCESS",
    65535: "SDU_TX_FAILURE",
    65534: "SDU_TX_NO_TX"
}

seqctrl_sts_code_str = {
    0: "TX_SUCCESS",
    1: "TX_FAILURE",
    2: "TX_NO_TX",
    15: "RX_SUCCESS",
}
pdll_flag_str = {
    0x0001: "RX_ET",
    0x0002: "POLLED",
    0x0004: "RX_DST",
    0x0008: "RX_SRC",
    0x0010: "POLL_RXD",
    0x0020: "DATA_TXD",
    0x0040: "DATA_RXD",
    0x0080: "CLI_TXD",
    0x0100: "CLI_RXD",
    0x0200: "TX_ET",
    0x0400: "RX_PHY_CHANGE",
    0x0800: "TX_PHY_CHANGE",
    0x1000: "SENT_RSSI",
    0x2000: "RX_DLC_END",
    0x4000: "RX_DLL_CRC",
    0x8000: "RX_TX_RX_TIME",
    0x10000: "RX_AUX_SEC",
}

prim_code_str = {
    0x00: "INVALID_REQ",
    0x01: "INVALID_CONF",
    0x02: "CL_START_IND",
    0x03: "CL_END_IND",
    0x04: "TX_BCAST_REQ",
    0x05: "TX_BCAST_CONF",
    0x06: "RXB_SCH_REQ",
    0x07: "RXB_SCH_CONF",
    0x08: "RXB_SCH_IND",
    0x09: "SA_START_REQ",
    0x0A: "SA_START_CONF",
    0x0B: "SA_DONE_IND",
    0x0C: "PD_UPD_REQ",
    0x0D: "PD_UPD_CONF",
    0x0E: "PKTD_UPD_REQ",
    0x0F: "PKTD_UPD_CONF",
    0x10: "TXP_UPD_REQ",
    0x11: "TXP_UPD_CONF",
    0x12: "CMID_UPD_REQ",
    0x13: "CMID_UPD_CONF",
    0x14: "PIBGET",
    0x15: "PIBGETCONF",
    0x16: "PIBSET",
    0x17: "PIBSETCONF",
    0x18: "MNQ_DELETE_REQ",
    0x19: "MNQ_DELETE_CONF",
    0x1A: "PKT_DUR_REQ",
    0x1B: "PKT_DUR_CONF",
    0x1C: "PREFNOD_LG_REQ",
    0x1D: "PREFNOD_LG_CONF",
    0x1E: "LLS_TX_REQ",
    0x1F: "LLS_TX_CONF",
    0x20: "LLS_TX_DONE_IND",
    0x21: "SECMIB_SET_REQ",
    0x22: "SECMIB_SET_CONF",
    0x23: "SECMIB_CLR_REQ",
    0x24: "SECMIB_CLR_CONF",
    0x25: "SECMIB_CLRA_REQ",
    0x26: "SECMIB_CLRA_CONF",
    0x27: "DLLRX_DATA_IND",
    0x28: "DLLTX_DONE_IND",
    0x29: "CLTX_DONE_IND",
    0x2A: "TX_BCAST_DONE_IND",
    0x2B: "FILT_RSSI_UPD_REQ",
    0x2C: "FILT_RSSI_UPD_CONF",
    0x30: "MAC_CNTRL_REQ",
    0x31: "MAC_CNTRL_CONF",
    0x32: "MAC_CNTRL_IND",
    0x33: "MAC_TXB_GET_REQ",
    0x34: "MAC_TXB_GET_CONF",
    0x35: "MAC_TXB_STATUS_IND",
    0x36: "CL_DATA_GET_REQ",
    0x37: "CL_DATA_GET_CONF",
    0x38: "CLI_REQ",
    0x39: "CLI_CONF",
    0x3A: "TST_START_REQ",
    0x3B: "TST_START_CONF",
    0x3C: "TST_START_IND",
    0x3D: "TST_STOP_REQ",
    0x3E: "TST_STOP_CONF",
    0x3F: "TST_STOP_IND",
    0x40: "MAC_TXB_SET_FAST_BCN_REQ",
    0x41: "MAC_TXB_SET_FAST_BCN_CONF",
    0x42: "CL_STAT_IND",
    0x43: "TST_NFL_IND",
    0x44: "ELG_SRV_INFO_REQ",
    0x45: "ELG_SRV_INFO_CONF",
    0x46: "LINKLAYER_SEC_KEY_UPD_REQ",
    0x47: "LINKLAYER_SEC_KEY_UPD_CONF",
    0x48: "LINKLAYER_SEC_INFO_UPD_REQ",
    0x49: "LINKLAYER_SEC_INFO_UPD_CONF",
    0x4A: "SA_START_IND",
    0x4B: "SA_ERRPKT_IND",
    0xFB: "ERROR",
    0xFC: "INVALID",
    0xFD: "LOGGER_IND",
    0xFE: "STATUS_IND",
    0xFF: "SNIFFER_I",

}

colors_list = [
    "#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
    "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
    "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
    "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
    "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
    "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
    "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
    "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",

    "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
    "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
    "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
    "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
    "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
    "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
    "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
    "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58",

    "#7A7BFF", "#D68E01", "#353339", "#78AFA1", "#FEB2C6", "#75797C", "#837393", "#943A4D",
    "#B5F4FF", "#D2DCD5", "#9556BD", "#6A714A", "#001325", "#02525F", "#0AA3F7", "#E98176",
    "#DBD5DD", "#5EBCD1", "#3D4F44", "#7E6405", "#02684E", "#962B75", "#8D8546", "#9695C5",
    "#E773CE", "#D86A78", "#3E89BE", "#CA834E", "#518A87", "#5B113C", "#55813B", "#E704C4",
    "#00005F", "#A97399", "#4B8160", "#59738A", "#FF5DA7", "#F7C9BF", "#643127", "#513A01",
    "#6B94AA", "#51A058", "#A45B02", "#1D1702", "#E20027", "#E7AB63", "#4C6001", "#9C6966",
    "#64547B", "#97979E", "#006A66", "#391406", "#F4D749", "#0045D2", "#006C31", "#DDB6D0",
    "#7C6571", "#9FB2A4", "#00D891", "#15A08A", "#BC65E9", "#FFFFFE", "#C6DC99", "#203B3C",

    "#671190", "#6B3A64", "#F5E1FF", "#FFA0F2", "#CCAA35", "#374527", "#8BB400", "#797868",
    "#C6005A", "#3B000A", "#C86240", "#29607C", "#402334", "#7D5A44", "#CCB87C", "#B88183",
    "#AA5199", "#B5D6C3", "#A38469", "#9F94F0", "#A74571", "#B894A6", "#71BB8C", "#00B433",
    "#789EC9", "#6D80BA", "#953F00", "#5EFF03", "#E4FFFC", "#1BE177", "#BCB1E5", "#76912F",
    "#003109", "#0060CD", "#D20096", "#895563", "#29201D", "#5B3213", "#A76F42", "#89412E",
    "#1A3A2A", "#494B5A", "#A88C85", "#F4ABAA", "#A3F3AB", "#00C6C8", "#EA8B66", "#958A9F",
    "#BDC9D2", "#9FA064", "#BE4700", "#658188", "#83A485", "#453C23", "#47675D", "#3A3F00",
    "#061203", "#DFFB71", "#868E7E", "#98D058", "#6C8F7D", "#D7BFC2", "#3C3E6E", "#D83D66",

    "#2F5D9B", "#6C5E46", "#D25B88", "#5B656C", "#00B57F", "#545C46", "#866097", "#365D25",
    "#252F99", "#00CCFF", "#674E60", "#FC009C", "#92896B"]


def check_and_install_package(pkg_list):
    """ check and installs the packages present in the list pkg_list """
    import importlib
    for pkg in pkg_list:
        package = pkg.split('=', 2)[0]
        try:
            importlib.import_module(package)
        except ImportError:
            print("\n\t\t ##### INSTALLING PKG {} (one time) #####".format(pkg))
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        finally:
            globals()[pkg] = importlib.import_module(package)
        print("")


def LOG_DBG(str):
    if args.debug == 0:
        return
    print(str)


def convert_pib_val(pibval):
    """ convert the pibval into correct format """
    size = len(pibval)
    ret = ""
    for i in range(0, size, 2):
        # print(i, pibval[size-i-2,size-i])
        ret = ret + pibval[size-i-2:size-i]
    return ret


def get_datetime():
    'get current date in a particular format'
    # return (datetime.now().strftime('%d %b %Y %H:%M:%S'))
    return (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def get_current_path():
    '''get the current path'''
    return os.getcwd()


def str_decode(data, encoding='utf-8', error='ignore'):
    '''Decodes and return the string using the encoding and error type'''
    return str(data.decode(encoding, error)) if data else ""


def test_ssh(host, command, acceptKey=False):
    '''Runs a command on a remote node by passing the password depending upon the OS'''
    HOST = "root@"+host
    COMMAND = command
    PWD = "itron"
    raw_output = b''
    err = ''

    LOG_DBG("Exec {} on {}".format(COMMAND, HOST))
    # run ssh or plink depending upon the os
    if os.name == OS_POSIX:
        p1 = subprocess.Popen(['sshpass', '-p', PWD, 'ssh', "-o StrictHostKeyChecking=no", "-o LogLevel=ERROR",
                               "-o UserKnownHostsFile=/dev/null", HOST, COMMAND], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
        # p1 = subprocess.Popen(['sshpass','-p', PWD, 'ssh', "-o StrictHostKeyChecking=no" ,"-o LogLevel=ERROR", "-o UserKnownHostsFile=/dev/null", HOST,COMMAND], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        # plink -v youruser@yourhost.com -pw yourpw "some linux command"
        if(acceptKey == True):
            p1 = subprocess.Popen(['echo', 'Y', '|', 'plink', "-pw", PWD, HOST, COMMAND],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            p1 = subprocess.Popen(['plink', "-batch", "-pw", PWD, HOST, COMMAND],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # p1 = subprocess.Popen(['plink',"-pw", PWD, HOST,COMMAND], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell= True, close_fds=True)
    try:
        # p1.terminate()
        raw_output, err = p1.communicate(timeout=30)
    except:
        print("prob while communicating quit:{}", glob["QUIT"])
        print("err={}, retCode={}, raw_output={}".format(
            err, p1.returncode, raw_output))
        if glob['QUIT']:
            exit(1)

    # print(err, p1.returncode)
    # print(raw_output)
    if p1.returncode != RET_SUCC:
        # print("### ERROR :" + str(err.decode('utf-8', 'ignore')).strip() + " ###")
        LOG_DBG("not suc")
    # LOG_DBG(raw_output)

    return p1.returncode, raw_output


def checkNodeReachability(ipv4Addr):
    '''check the reachability of the Root by sending a small packet of size 8B'''

    if os.name == OS_WIN:
        p1 = subprocess.Popen([PING_CMD, PING_CNT, '1', PING_SIZE, '8', PING_RESP_TIME, '2000',
                               ipv4Addr], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds=True)

    else:
        p1 = subprocess.Popen([PING_CMD, PING_CNT, '1', PING_SIZE, '8', PING_RESP_TIME,
                               '2', ipv4Addr], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    raw_output, err = p1.communicate()

    LOG_DBG("ret ={},  {}".format(p1.returncode, (raw_output)))

    if p1.returncode != 0:
        return RET_FAIL

    return RET_SUCC


def process_cl(code, infoArr):
    """ process all cl related tracing codes """
    info = ""
    global cl_id

    if tracing_events_num_str[code] == "CL_NEW":
        clId = int(infoArr[14] + infoArr[13], 16)
        cl_id = clId
        duration = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "CL Id {:d} (0x{:X}) duration {:d}msec".format(
            clId, clId, duration)

    elif tracing_events_num_str[code] == "CL_END":
        status = int(infoArr[14] + infoArr[13], 16)
        duration = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) duration {:d}msec".format(
            sts_code_str[status], status, status, duration)

    elif tracing_events_num_str[code] == "CL_REGISTER_SCH":
        status = int(infoArr[14] + infoArr[13], 16)
        duration = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) duration {:d}msec".format(
            sts_code_str[status], status, status, duration)

    elif tracing_events_num_str[code] == "CL_OUT_REQ":
        pktId = int(infoArr[16]+infoArr[15]+infoArr[14]+infoArr[13], 16)
        processClInfo = "pktId {:d}(0x{:X})".format(pktId, pktId)
        if not args.nolog:
            print("==="*40)

    elif tracing_events_num_str[code] == "CL_OUT_CNF" or tracing_events_num_str[code] == "CL_START":
        status = int(infoArr[14] + infoArr[13], 16)
        clId = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) CL Id {:d}".format(
            sts_code_str[status], status, status, clId)

    elif tracing_events_num_str[code] == "CL_IN":
        crcstatus = int(infoArr[16] + infoArr[15] +
                        infoArr[14] + infoArr[13], 16)
        processClInfo = "crc {:d}(0x{:X})".format(crcstatus, crcstatus)
        if not args.nolog:
            print("==="*40)

    elif tracing_events_num_str[code] == "CL_TX" or tracing_events_num_str[code] == "CL_RX":
        status = int(infoArr[14] + infoArr[13], 16)
        mode = int(infoArr[16], 16)
        channel = int(infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) mode {:d} chan {:d}".format(
            sts_code_str[status], status, status, mode, channel)

    elif tracing_events_num_str[code] == "CL_SEND_PRIMITIVE":
        status = int(infoArr[14] + infoArr[13], 16)
        primId = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) PRIM {:s}({:d}, 0x{:02X})".format(
            sts_code_str[status], status, status, prim_code_str[primId], primId, primId)

    elif tracing_events_num_str[code] == "CL_NEXT_CLI":
        rx_time = int(infoArr[14] + infoArr[13], 16)
        tx_time = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "rxTime {:d}ms, txTime {:d}ms".format(rx_time, tx_time)

    elif tracing_events_num_str[code] == "CL_NEXT_RX_TX":
        next_time = int(infoArr[16] + infoArr[15] +
                        infoArr[14] + infoArr[13], 16)
        processClInfo = "nextTime {:d}(0x{:08X})".format(next_time, next_time)

    elif tracing_events_num_str[code] == "CL_TXDONE":
        txstatus = int(infoArr[14] + infoArr[13], 16)
        clId = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) CL Id {:d}".format(
            txsts_code_str[txstatus], txstatus, txstatus, clId)

    elif tracing_events_num_str[code] == "CL_DATA_REQ":
        status = int(infoArr[14] + infoArr[13], 16)
        clId = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) CL Id {:d}".format(
            sts_code_str[status], status, status, clId)

    elif tracing_events_num_str[code] == "CL_DATA_RESP":
        status = int(infoArr[14] + infoArr[13], 16)
        dataPtr = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) 0x{:04X}".format(
            sts_code_str[status], status, status, dataPtr)

    elif tracing_events_num_str[code] == "CL_SEQ_CTRL":
        field = int(infoArr[14] + infoArr[13], 16)
        status = field & 0x000F
        fraglen = (field & 0xFFF0) >> 4
        fraglen = "|{:d}B".format(fraglen) if fraglen != 0 else ""

        statusStr = seqctrl_sts_code_str[status]

        seqInfo = int(infoArr[16] + infoArr[15], 16)
        seqNum = seqInfo & 0x3FF
        fragNum = (seqInfo & 0x3C00) >> 10
        morefrags = (seqInfo & 0x4000) >> 14
        retry = (seqInfo & 0x8000) >> 15

        processClInfo = "{:s} SeqNum {:d}(0x{:X}) frag {:d}{:s} {:s} {:s} {:s}".format(
            statusStr, seqNum, seqNum, fragNum, fraglen,
            "More" if morefrags == 1 else "",
            "retry" if retry == 1 else "",
            "(INVALID)" if seqInfo == 0xFFFF else ""
        )

    elif tracing_events_num_str[code] == "CL_CANCEL_SCH":
        next_time = int(infoArr[16] + infoArr[15] +
                        infoArr[14] + infoArr[13], 16)
        processClInfo = "nextTime {:d} 0x{:08X}".format(next_time, next_time)
    elif tracing_events_num_str[code] == "CL_PTR":
        next_32 = int(infoArr[16] + infoArr[15] +
                      infoArr[14] + infoArr[13], 16)
        processClInfo = "ptr 0x{:08X}".format(next_32)
    elif tracing_events_num_str[code] == "CL_DEBUG":
        next_32 = int(infoArr[16] + infoArr[15] +
                      infoArr[14] + infoArr[13], 16)
        processClInfo = "param32 {:d}(0x{:08X})".format(next_32, next_32)

    elif tracing_events_num_str[code] == "CL_PDLL_FLAGS":
        flag = int(infoArr[16] + infoArr[15] +
                   infoArr[14] + infoArr[13], 16)
        flag_str = ''
        flag_str_arr = []

        for i in pdll_flag_str:
            if (i & flag):
                flag_str_arr.append(pdll_flag_str[i])

        flag_str = ' | '.join(str(x) for x in flag_str_arr)
        # flag_str.rjust(250)
        processClInfo = "param32 {:d}(0x{:08X}) {:s}".format(
            flag, flag, flag_str)

    elif tracing_events_num_str[code] == "CL_PEER_MAC_ADDR":
        mac_add = "{:s}:{:s}:{:s}:{:s}".format(
            infoArr[13], infoArr[14], infoArr[15], infoArr[16])
        processClInfo = "addr=> xx:xx:xx:xx:{}".format(mac_add)

    else:
        next_32 = int(infoArr[16] + infoArr[15] +
                      infoArr[14] + infoArr[13], 16)

        processClInfo = "UNKNOWN CL TRACE {} param32{:08X}".format(
            code, next_32)

    return processClInfo


def get_substate_str(state, substate):
    stateStr = state_arr[state]
    if substate == 0x0F:
        return stateStr.split('_')[1]
    if stateStr == "LMSM_FH":
        return fh_substate_arr[substate]
    elif stateStr == "LMSM_RXB":
        return rxb_substate_arr[substate]
    elif stateStr == "LMSM_CL":
        return cl_substate_arr[substate]
    else:
        return "NONE"


def process_one_trace(code, infoArr):
    """ process a single trace """
    info = ""

    if (code >= tracing_events_str_num["HSM_EVENT_ENTRY"]) and (code <= tracing_events_str_num["HSM_EVENT_EPF_RESTORE"]) and (code != tracing_events_str_num["HSM_EVENT_LMFS_TIMER"]):
        evt_id = int(infoArr[15], 16)
        substate = int(infoArr[16], 16) & 0x0F
        state = int(infoArr[16], 16) >> 4

        stateStr = state_arr[state]
        evt_arg = int(infoArr[14] + infoArr[13], 16)
        subStateStr = get_substate_str(state, substate)
        info = "evt 0x{:02X},arg 0x{:02X} state {:s}(0x{:X})".format(
            evt_id, evt_arg,
            stateStr, state)
        if subStateStr != "NONE":
            info = info + "-->{:s}(0x{:X})".format(subStateStr, substate)

    elif (code >= tracing_events_str_num["CL_NEW"]) and (code <= tracing_events_str_num["CL_DEBUG"]):
        info = process_cl(code, infoArr)

    # bufmgr_get
    elif code == tracing_events_str_num["BUFMGR_GET"]:
        owner_id = int(infoArr[16], 16)
        sub_func_id = int(infoArr[15], 16)
        block_ptr = int(infoArr[14] + infoArr[13], 16)
        info = "ownr_Id {:s}(0x{:X}) subFunc_Id 0x{:02X} block_ptr 0x{:04X}".format(owner_ids_arr[owner_id],
                                                                                    owner_id, sub_func_id, block_ptr)

    # LMFS REMOVE
    elif code == tracing_events_str_num['LMFS_REMOVE_SCH_ENTRY']:
        owner_id = int(infoArr[16], 16)
        sch_id = int(infoArr[15] + infoArr[14] + infoArr[13], 16)
        info = "ownr_Id {:s}(0x{:X}) sch_id {:d}(0x{:X})".format(
            owner_ids_arr[owner_id], owner_id, sch_id, sch_id)

    # bugmgr_rel
    elif code == tracing_events_str_num["BUFMGR_RELEASE"]:
        block_ptr = int(infoArr[16] + infoArr[15] +
                        infoArr[14] + infoArr[13], 16)
        info = "block_ptr 0x{:08X}".format(block_ptr)

    # phy callbacks
    elif code == tracing_events_str_num["PHY_CALLBACKS_CLAIM"] or code == tracing_events_str_num["PHY_CALLBACKS_RELEASE"]:
        field_32 = int(infoArr[16] + infoArr[15] +
                       infoArr[14] + infoArr[13], 16)
        info = "ptr 0x{:08X}".format(field_32)
    # elg
    elif code == tracing_events_str_num["ELG"] or code == tracing_events_str_num["ELG_TIMER"] or code == tracing_events_str_num["ELG_EVENT"]:
        field_32 = int(infoArr[16] + infoArr[15] +
                       infoArr[14] + infoArr[13], 16)
        if (code == tracing_events_str_num["ELG_EVENT"]):
            info = "ev {}".format(elg_event_code_str[field_32])

        else:
            info = "param 0x{:08X}".format(field_32)
    else:
        field32 = int(infoArr[16] + infoArr[15] +
                      infoArr[14] + infoArr[13], 16)
        info = "param32 0x{:08X}".format(field32)

    return info


outputList = []
csvList = []


def process_hexdump(hexdump, startLine=-1, showFirstLine=False):
    # print(hexdump)
    global cl_id
    output = ''
    nlines = startLine
    firstLine = ' BYTENUM:   FRT_DEC   (0xFRT_HEXAD)  [TRACECODE]:       TRACE INFO '

    if showFirstLine:
        if not args.nolog:
            print(firstLine)
        outputList.extend(outputVer + "\n\n")
        outputList.extend(firstLine + "\n")
        csvList.append(["BYTENUM", "FRT_DEC", "FRT_HEX",
                        "[TRACECODE]:", "TRACE INFO"])

    for line in hexdump.splitlines()[startLine:]:
        byteArr = line.split(maxsplit=17)

        # print(byteArr, len(byteArr))
        if len(byteArr) != 18:
            continue
        nlines = nlines + 1
        # get timestamp
        timestamp = int(byteArr[8] + byteArr[7] + byteArr[6] + byteArr[5] +
                        byteArr[4] + byteArr[3] + byteArr[2] + byteArr[1], 16)

        # get trace code
        tracecode = int(byteArr[12] + byteArr[11] +
                        byteArr[10] + byteArr[9], 16)

        if tracecode >= MAX_TRACE_EVT:
            continue

        info = process_one_trace(tracecode, byteArr)

        output = "{:s}: {:d} (0x{:X}) [{:03d},0x{:04X}]: {:s} {:s}".format(
            byteArr[0],
            timestamp, timestamp,
            tracecode, tracecode, tracing_events_num_str[tracecode],
            info)

        outputList.extend(output + "\n")
        csvList.append([byteArr[0], timestamp, hex(timestamp), str(
            tracecode) + " (" + str(hex(tracecode)) + ")", tracing_events_num_str[tracecode]+" " + info])

        if not args.nolog:
            print(output, "[{}]".format(cl_id))

    halflen = int(len(output)/2) - int(len(get_datetime())/2)

    if not args.nolog:
        print(("-"*halflen) + "( "+get_datetime() + " )" + ("-" * halflen))

    with open(args.output, 'w') as fout:
        fout.writelines(outputList)

    if args.csv:
        with open(csvfile, 'w', newline='') as csvfileio:
            writer = csv.writer(csvfileio)
            writer.writerows(csvList)

    LOG_DBG("Written to {} lines to {}".format(nlines, args.output))

    showFirstLine = False

    return nlines


def cleanup_proc():
    pid = b''
    print(" - Cleaning Residues... ", end='')

    command = "ps | grep 'cat /dev/dsp_rf_tracing' | grep -v grep | awk '{print $1}'"
    ret, pid = test_ssh(args.ip, command)
    if ret != RET_SUCC:
        print("FAILED", end='')
        return
    pid = pid.decode('utf-8')
    pids = pid.replace('\n', ' ')

    print("{}{}".format("" if pids.strip() == "" else "PID ", pids), end='')

    if ret == RET_SUCC and pid != "":
        ret, output = test_ssh(args.ip, 'kill -9 {}'.format(pids))

        if ret != RET_SUCC:
            print("KILL FAILED", end='')
            return
        print("KILLED...", end='')

    print("old trace...", end='')
    command = "rm /tmp/hexTrace.log"
    ret, pid = test_ssh(args.ip, command)

    print("REMOVED")


def clear_local_logs():
    with open(args.output, 'w'):
        pass
    with open(csvfile, 'w'):
        pass
    if args.trace:
        with open(hexfile, 'w'):
            pass


def exit_handler():
    if not args.file:
        print(' - Cleaning UP.... Wait')
        if REACHABLE:
            cleanup_proc()
        print(
            " - Decoded Traces are saved to {}\{}".format(get_current_path(), args.output))

    # exit(0)


class Ipv4Action(argparse.Action):
    """
    Supports checking email agains different patterns. The current available patterns is:
    RFC5322 (http://www.ietf.org/rfc/rfc5322.txt)
    """

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            socket.inet_pton(socket.AF_INET, values.strip())
        except:  # not a valid address
            print("error: '{}' is NOT a valid IPv4 Address".format(values))
            raise

        setattr(namespace, self.dest, values)


class maskAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        try:
            decNum = int(values, 16)
            hexNum = hex(decNum)
            hexNum = hexNum[2:]
        except:
            print(
                "error: {} has illegal characters. Not in a hex format [0-9][A-F]".format(values))
            raise
        if len(hexNum) != TRACING_DEBUG_MASK_LEN*2:
            print("error: Invalid mask {} . Got {} characters. Should be {} characters".format(
                values, len(values), TRACING_DEBUG_MASK_LEN*2))
            raise ValueError("Invalid Len")
        setattr(namespace, self.dest, values)


class listIdAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        if values >= ID_MAX or values < ID_ALL:
            print("error: Invalid list ID {}. Valid Range [{}:{}]".format(
                values, ID_ALL, ID_MAX-1))
            raise ValueError("Invalid List ID")
        setattr(namespace, self.dest, values)


def my_wait(sec, new_count=0):
    for i in range(sec):
        # if(glob['QUIT']):
        #     break
        lines = "[{} lines decoded]".format(new_count)
        print("*** Polling {} ({}) in {:3d}sec... {}".format(args.ip,
                                                             macAddr, sec-i, lines), end='\r')
        sys.stdout.flush()
        time.sleep(1)
    print


def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')

    exit_handler()
    glob["QUIT"] = True
    raise SystemExit


def get_n_colors(n):
    ret = []
    r = min(int(random.random() * 256) - n - 1, 0)
    for i in range(n):
        ret.append(colors_list[r+i])
    return ret


def get_colors(n):
    ret = []
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    step = 256 / n
    for i in range(n):
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        # ret.append((r/256, g/256, b/256))
        ret.append('rgb({},{},{})'.format(r, g, b))
    return ret


# x, y, c, s = rand(4, 100)


def graph_it():

    if not os.path.isfile(graph_file):
        print("{} not found. Use -c option to create the required csv.".format(graph_file))
        return

    check_and_install_package(["pandas", "plotly==4.9.0"])

    try:
        import pandas as pd
        import numpy as np
        # import mplcursors
        # import matplotlib.pyplot as plt
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import plotly.offline as py

    except:
        print("Error while installing packages")
        # import matplotlib.pyplot as plt

    # plt.style.use('seaborn-deep')
    # plt.style.use('ggplot')

    print("showing graph {} from '{}'".format(graph_ans_list, graph_file))

    # plt.show()

    csv_df = pd.read_csv(sep=',', skiprows=1, names=['byte', "frt_dec", 'frt_hex', 'trace_code', 'trace_info'], filepath_or_buffer=graph_file)
    # csv_df[['tracecode_dec','tracecode_hex']] = df.Name.str.split(expand=True)
    csv_df = csv_df.assign(tracecode_dec=pd.Series(np.nan))
    csv_df = csv_df.assign(tracecode_hex=pd.Series(np.nan))

    csv_df[['tracecode_dec', 'tracecode_hex']
           ] = csv_df['trace_code'].str.split(expand=True)
    csv_df.drop(columns=['trace_code'], inplace=True)
    csv_df = csv_df.astype({'tracecode_dec': int})
    csv_df = csv_df.assign(cl_id=pd.Series(np.nan))

    csv_df['cl_id'] = csv_df["trace_info"].apply(lambda x: x.split()[4] if "CL_OUT_CNF" in x or "CL_START" in x else np.nan)
    csv_df['cl_mac'] = csv_df.apply(lambda x: x.trace_info.split('>', 2)[1].strip() if x.tracecode_dec == 147 else np.nan, axis=1)
    csv_df['txrx_param'] = csv_df.apply(lambda x: x.trace_info.split(')', 2)[1].strip() if x.tracecode_dec == 140 or x.tracecode_dec == 141 else np.nan, axis=1)

    # csv_df['cl_id'].ffill()
    # csv_df = csv_df.replace("", np.nan).ffill()

    traceCodeMap_df = pd.DataFrame(tracing_events_num_str.items(), columns=['tracecode_dec', 'trace_str'])

    # add owner id
    csv_df = csv_df.assign(owner=pd.Series(np.nan))
    csv_df['owner'] = csv_df.apply(lambda x: x.trace_info.split('LMSM_')[1].split('(', 2)[0] if x.tracecode_dec == 68 else "", axis=1)
    csv_df = csv_df.replace("", np.nan).ffill()

    # FRT_trace_val
    csv_df['frt32_val'] = csv_df.apply(lambda x: (x.trace_info[-8:]) if x.tracecode_dec in [6, 121, 122, 123, 124, 129, 130] else np.nan, axis=1)

    csv_df['dummy'] = csv_df.tracecode_dec.shift(1)
    csv_df['dummy_frt'] = csv_df.frt32_val.shift(-1)
    csv_df['dup'] = csv_df.apply(lambda x: 1 if x.tracecode_dec == x.dummy else 0, axis=1)

    csv_df['frt_val'] = csv_df.dummy_frt + csv_df.frt32_val
    csv_df['frt_val'] = csv_df.frt_val.apply(lambda x: int(x, 16) if type(x) == str else np.nan)
    # csv_df.frt_val = csv_df.frt_val.apply(lambda x: "hello" if x!=np.nan else np.nan)
    csv_df = csv_df[csv_df.dup == 0]
    csv_df.drop(columns=['frt32_val', 'dummy', 'dummy_frt', 'dup'], inplace=True)

    stat_total = csv_df.groupby('tracecode_dec').count().reset_index().astype({"tracecode_dec": int})
    stat_total = stat_total[['tracecode_dec', 'byte']]
    stat_total = stat_total.merge(traceCodeMap_df, how='inner', on="tracecode_dec").sort_values(by=['tracecode_dec']).reset_index()

    cl_csv_df = csv_df.loc[(csv_df['tracecode_dec'] > 120) & (csv_df['tracecode_dec'] <= 151) | (csv_df.tracecode_dec <= 6)]
    cl_csv_df = cl_csv_df.drop(columns=['tracecode_hex'])

    # cl_csv_df = cl_csv_df.assign(sts=pd.Series(np.nan))
    cl_csv_df['sts'] = cl_csv_df.trace_info.apply(lambda x: "" if "STS" not in x else x.split()[1].split('(')[0])
    cl_csv_df = cl_csv_df.merge(traceCodeMap_df, on="tracecode_dec")
    cl_csv_df.sort_values(by=['byte'], inplace=True)

    cl_stats = cl_csv_df.groupby(
        ['tracecode_dec', 'trace_str', 'sts', ]).count()
    cl_stats = cl_stats['byte']

    print(cl_stats)

    # obtain fastlink df
    if '0' in graph_ans_list or '1' in graph_ans_list:
        filter_list = [149, 148]

        fast_link_df = cl_csv_df[(cl_csv_df.tracecode_dec.isin(filter_list))][['byte', 'frt_dec', 'tracecode_dec', 'sts', 'cl_id']]
        trace_list = list(set(list(fast_link_df.tracecode_dec)))
        if sorted(trace_list) != sorted(filter_list):
            print("\n**** All required traces {} are not present {}. Cannot draw the graph".format(filter_list, trace_list))
            return

        if not fast_link_df.empty:
            fast_link_df['A_dif'] = fast_link_df['frt_dec'].diff()
            fast_link_df['shifted_frt'] = fast_link_df['frt_dec'].shift()
            fast_link_df['prev_trace'] = fast_link_df['tracecode_dec'].shift()
            fast_link_df['diff'] = fast_link_df.apply(lambda x: np.NaN if (x['tracecode_dec'] == x['prev_trace'] or x['tracecode_dec'] == 148) else x['A_dif'], axis=1)
            fast_link_df.drop(columns=['A_dif', 'shifted_frt', 'prev_trace'], inplace=True)

            # obtain rtt_df
            rtt_df = fast_link_df[['byte', 'diff']].dropna()
            rtt_df = rtt_df.groupby('diff').agg(
                'count').rename(columns={'byte': 'freq'})

            # PDF
            rtt_df['pdf'] = rtt_df['freq'] / sum(rtt_df['freq'])
            # CDF
            rtt_df['cdf'] = rtt_df['pdf'].cumsum()
            rtt_df = rtt_df.reset_index()
            rtt_df = rtt_df.astype({'diff': int})

            # Create figure with secondary y-axisspecs
            if(graphs['rtt'] == {}):
                graphs['rtt'] = make_subplots(specs=[[{"secondary_y": True}]])

                # Add traces
                graphs['rtt'].add_bar(x=rtt_df['diff'], y=rtt_df['freq'], name="Count", opacity=0.5)
                graphs['rtt'].add_scatter(x=rtt_df['diff'], y=rtt_df['pdf'], name="PDF", secondary_y=True)
                graphs['rtt'].add_scatter(x=rtt_df['diff'], y=rtt_df['cdf'], name="CDF", secondary_y=True)
                # graphs['rtt'].add_trace(go.Bar(x=rtt_df['diff'], y=rtt_df['freq'], name="Count", opacity=0.5,
                #                      ), secondary_y=True)
                # graphs['rtt'].add_trace(go.Scatter(x=rtt_df['diff'], y=rtt_df['pdf'], name="PDF"))
                # graphs['rtt'].add_trace(go.Scatter(x=rtt_df['diff'], y=rtt_df['cdf'], name='CDF'))
                graphs['rtt'].update_layout(
                    # template="plotly_dark",
                    title="Round Trip time in usec",
                    xaxis_title="RTT (usecs)",
                    yaxis_title="Count",
                    yaxis2_title="PDF & CDF",
                    hovermode='x',

                )
                graphs['rtt'].show()

            else:
                print(graphs['rtt'])
                graphs['rtt'].data[0].x = list(rtt_df['diff'])
                graphs['rtt'].data[0].y = list(rtt_df['freq'])

                graphs['rtt'].data[1].x = list(rtt_df['diff'])
                graphs['rtt'].data[1].y = list(rtt_df['pdf'])

                graphs['rtt'].data[2].x = list(rtt_df['diff'])
                graphs['rtt'].data[2].y = list(rtt_df['cdf'])

            # fig.show()

    if '0' in graph_ans_list or '2' in graph_ans_list or '3' in graph_ans_list:

        timings_df = pd.DataFrame()
        timings_plot_df = pd.DataFrame()
        filter_list = [6, 122, 123, 124, 129, 130, 141, 140, 142]
        timings_df = cl_csv_df[cl_csv_df.tracecode_dec.isin(filter_list)]

        trace_list = list(set(list(timings_df.tracecode_dec)))
        if not set(filter_list).issubset(trace_list):
            print("\n**** All required traces {} are not present. {}  Cannot draw the graph".format(filter_list, trace_list))
            return

        # nextCLI
        timings_df = timings_df.assign(nextcli=pd.Series(np.nan))
        timings_df.nextcli = timings_df.apply(lambda x: "CLI(" + x.trace_info.split(' ')[4] + ", " + x.trace_info.split(' ')
                                              [2][:-1] + ")" if x.tracecode_dec == tracing_events_str_num['CL_NEXT_CLI'] else np.nan, axis=1)
        timings_df.nextcli = timings_df.nextcli.fillna(method='bfill')
        timings_df = timings_df[timings_df.tracecode_dec != tracing_events_str_num['CL_NEXT_CLI']]

        # aftertxcol
        timings_df = timings_df.assign(aftertx_col=pd.Series(np.nan))
        timings_df['aftertx_col'] = timings_df.apply(lambda x: "afterTx" if x['tracecode_dec'] == tracing_events_str_num['CL_TX'] else np.nan, axis=1)
        timings_df.afertx_col = np.zeros

        # beforetxcol
        timings_df = timings_df.assign(beforetx_col=pd.Series(np.nan))
        timings_df.beforetx_col = timings_df.tracecode_dec.apply(lambda x: "beforeTx" if x == tracing_events_str_num['CL_FRT32_TX_CALL'] else np.nan)

        # dc
        timings_df['dummy'] = timings_df.aftertx_col.shift(1)
        timings_df = timings_df.assign(dc_col=pd.Series(np.nan))
        timings_df.dc_col = timings_df.apply(lambda x: "dc" if x.tracecode_dec == tracing_events_str_num['LMMGR_DATA_CONF'] else np.nan, axis=1)
        timings_df.drop(columns=['dummy'], inplace=True)

        # txend
        timings_df = timings_df.assign(txend_col=pd.Series(np.nan))
        timings_df.txend_col = timings_df.apply(lambda x: "txEnd" if x.tracecode_dec == tracing_events_str_num['FRT32_TX_END'] else np.nan, axis=1)
        # afterRx
        timings_df = timings_df.assign(afterrx_col=pd.Series(np.nan))
        timings_df.afterrx_col = timings_df.apply(lambda x: "afterRx" if x.tracecode_dec == tracing_events_str_num['CL_RX'] else np.nan, axis=1)

        # beforeRx
        timings_df = timings_df.assign(beforerx_col=pd.Series(np.nan))
        timings_df.beforerx_col = timings_df.apply(lambda x: "beforeRx" if x.tracecode_dec == tracing_events_str_num['CL_FRT32_RX_CALL'] else np.nan, axis=1)

        # rxend
        timings_df = timings_df.assign(rxend_col=pd.Series(np.nan))
        timings_df.rxend_col = timings_df.apply(lambda x: "rxEnd" if x.tracecode_dec == tracing_events_str_num['FRT32_RX_END'] else np.nan, axis=1)

        # # FRT_dec
        # timings_df['frt_dec'] = timings_df.apply(lambda x: int(x.frt_hex[-min(len(x.frt_hex)-2, 8):], 16), axis=1)

        timings_df.drop(columns=['frt_hex'], inplace=True)

        # timestamps for tx rx start and end
        timings_df['ts_rxstart'] = timings_df.apply(lambda x: x.frt_val if x.tracecode_dec == tracing_events_str_num['FRT32_RX_START'] else np.nan, axis=1)
        timings_df['ts_rxend'] = timings_df.apply(lambda x: x.frt_val if x.tracecode_dec == tracing_events_str_num['FRT32_RX_END'] else np.nan, axis=1)
        timings_df['ts_txstart'] = timings_df.apply(lambda x: x.frt_val if x.dc_col == "dc" else np.nan, axis=1)
        timings_df['ts_txend'] = timings_df.apply(lambda x: x.frt_val if x.tracecode_dec == tracing_events_str_num['FRT32_TX_END'] else np.nan, axis=1)

    if '0' in graph_ans_list or '3' in graph_ans_list:
        timeline_color = {

            "TOP": colors_list[0],
            "IDLE": colors_list[1],
            "FH": 'orange',
            "RXB": 'blue',
            "TXB": 'green',
            "CL": 'red',
            "BCAST": 'purple',
            "SA": colors_list[7],
            "LLS": colors_list[8],
            "ELG": colors_list[9],
        }
        # rx
        timeline_rx_df = pd.DataFrame()
        timeline_rx_df = timings_df[['byte', 'owner', 'nextcli', 'cl_id', 'cl_mac', 'txrx_param', 'ts_rxstart', 'ts_rxend']]
        timeline_rx_df = timeline_rx_df.assign(ts_rxend=timeline_rx_df.ts_rxend.shift(-1))
        timeline_rx_df.dropna(subset=['ts_rxstart', 'ts_rxend'], inplace=True)
        timeline_rx_df['rx_dur'] = timeline_rx_df.ts_rxend - timeline_rx_df.ts_rxstart
        timeline_rx_df['color'] = timeline_rx_df.owner.apply(lambda x: timeline_color[x])
        timeline_rx_df['hoverinfo'] = "~~~ " + timeline_rx_df.owner + " ~~~<br>" + \
            "<b>CL ID </b>" + timeline_rx_df.cl_id.astype(str) + ", <b>dur</b> " + timeline_rx_df.rx_dur.astype(int).astype(str) + "usec"+ \
            "<br>" + timeline_rx_df.cl_mac + "<br>" + \
            timeline_rx_df.txrx_param + "<br>" + \
            timeline_rx_df.nextcli+ "<br>" + \
            "<br><b>Start:</b>"+timeline_rx_df.ts_rxstart.astype(str)+"<br><b>End:</b>" + timeline_rx_df.ts_rxend.astype(str)

        # tx
        timeline_tx_df = timings_df[['byte', 'owner', 'nextcli', 'cl_id', 'cl_mac', 'txrx_param', 'ts_txstart', 'ts_txend']]
        timeline_tx_df = timeline_tx_df.assign(ts_txend=timeline_tx_df.ts_txend.shift(-1))
        timeline_tx_df.dropna(subset=['ts_txstart', 'ts_txend'], inplace=True)
        timeline_tx_df['tx_dur'] = timeline_tx_df.ts_txend - timeline_tx_df.ts_txstart
        timeline_tx_df['color'] = timeline_tx_df.owner.apply(lambda x: timeline_color[x])
        timeline_tx_df['hoverinfo'] = "~~~ " + timeline_tx_df.owner + " ~~~<br>" + \
            "<b>CL ID </b>" + timeline_tx_df.cl_id.astype(str) + ", <b>dur</b> " + timeline_tx_df.tx_dur.astype(int).astype(str) + "usec"+ \
            "<br>" + timeline_tx_df.cl_mac + "<br>" + \
             timeline_tx_df.txrx_param + "<br>" + \
            timeline_tx_df.nextcli + "<br>" + \
            "<br><b>Start:</b>"+timeline_tx_df.ts_txstart.astype(str)+"<br><b>End:</b>" + timeline_tx_df.ts_txend.astype(str)

        timeline_tx_df = timeline_tx_df[timeline_tx_df.tx_dur <= 500000]

        # PHY INDICATIONS and CALLs
        filter_list = [1, 2, 3, 4, 6, 140, 141, 148, 149]
        timeline_phycallind_df = pd.DataFrame()
        timeline_phycallind_df = cl_csv_df[cl_csv_df.tracecode_dec.isin(filter_list)]
        timeline_phycallind_df = timeline_phycallind_df.assign(y1=pd.Series(np.nan))

        y0 = 0
        y1 = 3
        timeline_phycallind_df['y1'] = timeline_phycallind_df.tracecode_dec.apply(lambda x: -y1 if x in [1, 2, 3, 4, 141] else y1)
        timeline_phycallind_df['y0'] = timeline_phycallind_df.tracecode_dec.apply(lambda x: -y0 if x in [1, 2, 3, 4, 141] else y0)
        timeline_phycallind_df['color'] = timeline_phycallind_df.tracecode_dec.apply(lambda x: colors_list[x])
        timeline_phycallind_df.drop(columns=['frt_hex'], inplace=True)

        fig = go.Figure()

        # add TXs
        fig.add_bar(
            x=timeline_tx_df.ts_txstart + timeline_tx_df.tx_dur/2,
            y=[2]*len(timeline_tx_df.index),
            width=timeline_tx_df.tx_dur,
            # base=1,
            name="TX",
            text=timeline_tx_df.hoverinfo,
            textposition="inside",
            hovertemplate='%{text}',            # hoverinfo="none",
            # offset=-timeline_tx_df.tx_dur/2,
            # hoverinfo="none",
            marker=dict(
                color='darksalmon',
                opacity=1,
                line=dict(width=0.5,
                          color=timeline_tx_df['color']))
        )

        # add RXs
        fig.add_bar(
            x=timeline_rx_df.ts_rxstart + timeline_rx_df.rx_dur/2,
            y=[-2]*len(timeline_rx_df.index),
            width=timeline_rx_df.rx_dur,
            name="RX",
            text=timeline_rx_df.hoverinfo,
            textposition="inside",
            hovertemplate='%{text}',            # hoverinfo="none",
            marker=dict(
                color='darkseagreen',
                line=dict(width=0.5,
                          color=timeline_rx_df['color']))
        )

        # add PHY Indications and calls

        fig.add_scatter(
            x=timeline_phycallind_df.frt_dec,
            y=timeline_phycallind_df.y0,
            mode="markers",
            name="Internal Controls/Indications",
            text="<b>CL_ID:</b> " + timeline_phycallind_df.cl_id + "<br>" + timeline_phycallind_df.trace_info,
            hovertemplate="<b>FRT:</b>%{x}<br>%{text}",
            visible="legendonly",
            # hoverinfo="none",
            marker=dict(
                color='white',
                line=dict(width=1,
                          color=timeline_phycallind_df.color))
        )

        # add annotations for tx and rx
        fig.add_annotation(
            x=min(timeline_tx_df.ts_txend),
            y=3.5,
            text="Transmissions",
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="red"
            ),
            showarrow=False,)
        fig.add_annotation(
            x=min(timeline_rx_df.ts_rxend),
            y=-4,
            text="Receptions",
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="green"
            ),
            showarrow=False,)

        # # add tx-rx start/end
        # fig.add_scatter(
        #     x=timeline_tx_df.ts_txstart.append(timeline_tx_df.ts_txend).append(timeline_rx_df.ts_rxstart).append(timeline_rx_df.ts_rxend),
        #     # x=pandas.concat(timeline_tx_df.ts_txstart,timeline_tx_df.ts_txend, timeline_rx_df.ts_rxstart,timeline_rx_df.ts_rxend),
        #     y=[0]*(len(timeline_tx_df.index)*2 + len(timeline_tx_df.index)*2),
        #     mode="markers",
        #     name="TX/RX Start/End",
        #     hovertemplate="<b>FRT:</b>%{x}",
        #     visible="legendonly",
        #     # hoverinfo="none",
        #     marker=dict(
        #         color='red',
        #         line=dict(width=1,
        #                   color="black"))
        # )

        fig.update_layout(
            title="Timeline Visualizer",
            showlegend=True,
            xaxis_tickformat='f',
            yaxis=dict(
                # visible=False,
                range=[-8, 8],
                fixedrange=True,
                showticklabels=False,
            ),
            legend=dict(orientation='h', yanchor='top', xanchor='center', y=1, x=0.5)
            # hovermode='x',
            # shapes=shapes,
        )
        fig.update_xaxes(rangeslider_visible=True, title="FRT usec",)
        fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='grey')

        fig.show()

        # exit(0)
    if '0' in graph_ans_list or '2' in graph_ans_list:

        # target2txphr

        timings_df['dummy'] = timings_df.dc_col.shift(-2)
        timings_df['dummy_frt'] = timings_df.frt_val.shift(-2)
        timings_df = timings_df.assign(target2txphr=pd.Series(np.nan))
        timings_df.target2txphr = timings_df.apply(lambda x: x.dummy_frt-x.frt_val if x.beforetx_col == 'beforeTx' and x.dummy == 'dc' else np.nan, axis=1)
        timings_df.drop(columns=['dummy', 'dummy_frt'], inplace=True)
        # freq
        target2txphr_df = timings_df[['byte', 'target2txphr']].groupby('target2txphr').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        target2txphr_df = target2txphr_df.astype({'target2txphr': int})
        # PDF
        target2txphr_df['pdf'] = target2txphr_df['freq'] / sum(target2txphr_df['freq'])
        # CDF
        target2txphr_df['cdf'] = target2txphr_df['pdf'].cumsum()
        target2txphr_df = target2txphr_df.reset_index()
        # target2txphr_df = target2txphr_df.astype({'target2txphr': 'int64'})

        # txend2rxstart
        timings_df['dummy'] = timings_df.beforerx_col.shift(-1)
        timings_df['dummy_frt'] = timings_df.frt_dec.shift(-1)
        timings_df = timings_df.assign(txend2rxstart=pd.Series(np.nan))
        timings_df.txend2rxstart = timings_df.apply(lambda x: x.dummy_frt-x.frt_val if x.txend_col == 'txEnd' and x.dummy == 'beforeRx' else np.nan, axis=1)
        timings_df.drop(columns=['dummy', 'dummy_frt'], inplace=True)
        # freq
        txend2rxstart_df = timings_df[['byte', 'txend2rxstart']].groupby('txend2rxstart').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        txend2rxstart_df = txend2rxstart_df.astype({'txend2rxstart': int})
        # PDF
        txend2rxstart_df['pdf'] = txend2rxstart_df['freq'] / sum(txend2rxstart_df['freq'])
        # CDF
        txend2rxstart_df['cdf'] = txend2rxstart_df['pdf'].cumsum()
        txend2rxstart_df = txend2rxstart_df.reset_index()

        # rxend2targettime
        timings_df['dummy'] = timings_df.beforetx_col.shift(-1)
        timings_df['dummy_frt'] = timings_df.frt_val.shift(-1)
        timings_df['dummy_cl_id'] = timings_df.cl_id.shift(-1)

        timings_df = timings_df.assign(rxend2targettime=pd.Series(np.nan))

        timings_df.rxend2targettime = timings_df.apply(lambda x: x.dummy_frt-x.frt_val if x.rxend_col == 'rxEnd' and x.dummy == 'beforeTx' and x.cl_id == x.dummy_cl_id else np.nan, axis=1)
        timings_df.drop(columns=['dummy', 'dummy_frt', 'dummy_cl_id'], inplace=True)
        # freq
        rxend2targettime_df = timings_df[['byte', 'rxend2targettime']].groupby('rxend2targettime').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        rxend2targettime_df = rxend2targettime_df.astype({'rxend2targettime': int})
        # PDF
        rxend2targettime_df['pdf'] = rxend2targettime_df['freq'] / sum(rxend2targettime_df['freq'])
        # CDF
        rxend2targettime_df['cdf'] = rxend2targettime_df['pdf'].cumsum()
        rxend2targettime_df = rxend2targettime_df.reset_index()

        # rxend2txtime
        timings_df['dummy'] = timings_df.dc_col.shift(-3)
        timings_df['dummy_frt'] = timings_df.frt_val.shift(-3)
        timings_df['dummy_cl_id'] = timings_df.cl_id.shift(-3)
        timings_df = timings_df.assign(rxend2txtime=pd.Series(np.nan))
        timings_df.rxend2txtime = timings_df.apply(lambda x: x.dummy_frt-x.frt_val if x.rxend_col == 'rxEnd' and x.dummy == 'dc' and x.cl_id == x.dummy_cl_id else np.nan, axis=1)
        timings_df.drop(columns=['dummy', 'dummy_frt', 'dummy_cl_id'], inplace=True)
        # freq
        rxend2txtime_df = timings_df[['byte', 'rxend2txtime']].groupby('rxend2txtime').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        rxend2txtime_df = rxend2txtime_df.astype({'rxend2txtime': int})
        # PDF
        rxend2txtime_df['pdf'] = rxend2txtime_df['freq'] / sum(rxend2txtime_df['freq'])
        # CDF
        rxend2txtime_df['cdf'] = rxend2txtime_df['pdf'].cumsum()
        rxend2txtime_df = rxend2txtime_df.reset_index()

        # txcall2targettime
        timings_df = timings_df.assign(txcall2targettime=pd.Series(np.nan))
        timings_df.txcall2targettime = timings_df.apply(lambda x: x.frt_val-x.frt_dec if x.beforetx_col == 'beforeTx' else np.nan, axis=1)
        # freq
        txcall2targettime_df = timings_df[['byte', 'txcall2targettime']].groupby('txcall2targettime').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        txcall2targettime_df = txcall2targettime_df.astype({'txcall2targettime': int})
        # PDF
        txcall2targettime_df['pdf'] = txcall2targettime_df['freq'] / sum(txcall2targettime_df['freq'])
        # CDF
        txcall2targettime_df['cdf'] = txcall2targettime_df['pdf'].cumsum()
        txcall2targettime_df = txcall2targettime_df.reset_index()
        # txcall2aftertx
        timings_df['dummy'] = timings_df.aftertx_col.shift(-1)
        timings_df['dummy_frt'] = timings_df.frt_dec.shift(-1)
        timings_df = timings_df.assign(txcall2aftertx=pd.Series(np.nan))
        timings_df.txcall2aftertx = timings_df.apply(lambda x: x.dummy_frt-x.frt_dec if x.beforetx_col == 'beforeTx' and x.dummy == 'afterTx' else np.nan, axis=1)
        timings_df.drop(columns=['dummy', 'dummy_frt'], inplace=True)
        # freq
        txcall2aftertx_df = timings_df[['byte', 'txcall2aftertx']].groupby('txcall2aftertx').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        txcall2aftertx_df = txcall2aftertx_df.astype({'txcall2aftertx': int})
        # PDF
        txcall2aftertx_df['pdf'] = txcall2aftertx_df['freq'] / sum(txcall2aftertx_df['freq'])
        # CDF
        txcall2aftertx_df['cdf'] = txcall2aftertx_df['pdf'].cumsum()
        txcall2aftertx_df = txcall2aftertx_df.reset_index()

        # rxend2txcall
        timings_df['dummy'] = timings_df.beforetx_col.shift(-1)
        timings_df['dummy_frt'] = timings_df.frt_dec.shift(-1)
        timings_df['dummy_cl_id'] = timings_df.cl_id.shift(-1)

        timings_df = timings_df.assign(rxend2txcall=pd.Series(np.nan))
        timings_df.rxend2txcall = timings_df.apply(lambda x: x.dummy_frt-x.frt_val if x.rxend_col == 'rxEnd' and x.dummy == 'beforeTx' and x.cl_id == x.dummy_cl_id else np.nan, axis=1)
        timings_df.drop(columns=['dummy', 'dummy_frt', 'dummy_cl_id'], inplace=True)
        # freq
        rxend2txcall_df = timings_df[['byte', 'rxend2txcall']].groupby('rxend2txcall').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        rxend2txcall_df = rxend2txcall_df.astype({'rxend2txcall': int})
        # PDF
        rxend2txcall_df['pdf'] = rxend2txcall_df['freq'] / sum(rxend2txcall_df['freq'])
        # CDF
        rxend2txcall_df['cdf'] = rxend2txcall_df['pdf'].cumsum()
        rxend2txcall_df = rxend2txcall_df.reset_index()

        # rxcall2afterrx
        timings_df['dummy'] = timings_df.afterrx_col.shift(-1)
        timings_df['dummy_frt'] = timings_df.frt_dec.shift(-1)
        timings_df = timings_df.assign(rxcall2afterrx=pd.Series(np.nan))
        timings_df.rxcall2afterrx = timings_df.apply(lambda x: x.dummy_frt-x.frt_dec if x.beforerx_col == 'beforeRx' and x.dummy == 'afterRx' else np.nan, axis=1)
        timings_df.drop(columns=['dummy', 'dummy_frt'], inplace=True)
        # freq
        rxcall2afterrx_df = timings_df[['byte', 'rxcall2afterrx']].groupby('rxcall2afterrx').agg('count').rename(columns={'byte': 'freq'}).reset_index()
        rxcall2afterrx_df = rxcall2afterrx_df.astype({'rxcall2afterrx': int})
        # PDF
        rxcall2afterrx_df['pdf'] = rxcall2afterrx_df['freq'] / sum(rxcall2afterrx_df['freq'])
        # CDF
        rxcall2afterrx_df['cdf'] = rxcall2afterrx_df['pdf'].cumsum()
        rxcall2afterrx_df = rxcall2afterrx_df.reset_index()

        cl_dur_df = cl_csv_df[cl_csv_df['tracecode_dec'] == 132][['byte', 'sts', 'trace_info']]
        if not cl_dur_df.empty:
            cl_dur_df['dur_ms'] = cl_dur_df.apply(lambda x: x['trace_info'].split(' ')[3].split('msec')[0], axis=1)
            cl_dur_df.drop(columns=['trace_info', 'sts'], inplace=True)
            cl_dur_df['dur_ms'] = cl_dur_df['dur_ms'].astype(int)
            # cl_dur_df = cl_dur_df.sort_values(by='dur_ms')
            cl_dur_df = cl_dur_df.groupby('dur_ms').agg(
                'count').rename(columns={'byte': 'freq'}).reset_index()
            # PDF
            cl_dur_df['pdf'] = cl_dur_df['freq'] / sum(cl_dur_df['freq'])
            # CDF
            cl_dur_df['cdf'] = cl_dur_df['pdf'].cumsum()
            cl_dur_df = cl_dur_df.reset_index()

        # rxcall2rxPHR
        timings_df['dummy_frt'] = timings_df.ts_rxstart.shift(-1)
        timings_df = timings_df.assign(afterRx2rxPHR=pd.Series(np.nan))
        timings_df.afterRx2rxPHR = timings_df.apply(lambda x: x.dummy_frt - x.frt_dec if x.afterrx_col == 'afterRx' and x.dummy_frt != np.nan else np.nan, axis=1)

        # drop values higher than 3sec
        timings_df.afterRx2rxPHR = timings_df.apply(lambda x: np.nan if np.isnan([x.afterRx2rxPHR]) or x.afterRx2rxPHR > 3000.0 else x.afterRx2rxPHR, axis=1)

        # PLOT THE TIMING DIAGRAM
        # A list of Matplotlib releases and their dates
        # Taken from https://api.github.com/repos/matplotlib/matplotlib/releases
        names = ['WrapperCall1', 'WrapperReturn', 'TargetTx1', 'TxPHR1', 'EndTxTime', 'rxStart_beforeCall', 'rxStart_afterCall', 'rxPHR',
                 'rxEnd', 'WrapperCall2', 'TargetTx2', 'TxPHR2', ]

        tx_dur = 2000
        rx_dur = 1500

        names_label_dic = {
            'WrapperCall1': "WrapperCall",
            'WrapperReturn': "WrapperReturn",
            'TargetTx1': "TargetTx",
            'TxPHR1': "TxPHR",
            'EndTxTime': "EndTxTime",
            'rxStart_beforeCall': "rxStart\nbeforeCall",
            'rxStart_afterCall': "rxStart\nafterCall",
            'rxPHR': "rx PHR",
            'rxEnd': "rxEnd",
            'WrapperCall2': "WrapperCall",
            'TargetTx2': "TargetTx",
            'TxPHR2': "TxPHR",
        }

        levels_dic = {
            'WrapperCall1': 2,
            'WrapperReturn': 2,
            'TargetTx1': 1,
            'TxPHR1': 2,
            'EndTxTime': 1,
            'rxStart_beforeCall': -1.2,
            'rxStart_afterCall': -2,
            'rxPHR': -2,
            'rxEnd': -1,
            'WrapperCall2': 2,
            'TargetTx2': 1,
            'TxPHR2': 1,
        }

        colors_dic = {
            'WrapperCall1': 'royalblue',
            'WrapperReturn': 'royalblue',
            'TargetTx1': 'crimson',
            'TxPHR1': 'crimson',
            'EndTxTime': 'crimson',
            'rxStart_beforeCall': 'LightSeaGreen',
            'rxStart_afterCall': 'LightSeaGreen',
            'rxPHR': 'LightSeaGreen',
            'rxEnd': 'LightSeaGreen',
            'WrapperCall2': 'royalblue',
            'TargetTx2': 'crimson',
            'TxPHR2': 'crimson',
        }

        diff_points_dic = {
            'wrapperCall2Return1': int(timings_df.txcall2aftertx.mean()),
            'wrapperCall2TargetTx1': int(timings_df.txcall2targettime.mean()),
            'targetTx2TxPHR1': int(timings_df.target2txphr.mean()),
            'endTxTime2rxStartbefore': int(timings_df.txend2rxstart.mean()),
            'rxstartBefore2After': int(timings_df.rxcall2afterrx.mean()),
            'rxEnd2wrapperCall': int(timings_df.rxend2txcall.mean()),
            'rxstartAfter2rxPHR': int(timings_df.afterRx2rxPHR.mean()),
            'wrapperCall2TargetTx2': int(timings_df.txcall2targettime.mean()),
            'rxEnd2targetTx': int(timings_df.rxend2targettime.mean()),
            'rxEnd2TxPHR': int(timings_df.rxend2txtime.mean()),
            'targetTx2TxPHR2': int(timings_df.target2txphr.mean())
        }

        diff_points_arr = list(diff_points_dic.values())

        points_dic = {}
        points_dic['WrapperCall1'] = 1
        points_dic['WrapperReturn'] = points_dic['WrapperCall1'] + diff_points_dic['wrapperCall2Return1']
        points_dic['TargetTx1'] = points_dic['WrapperCall1'] + diff_points_dic['wrapperCall2TargetTx1']
        points_dic['TxPHR1'] = points_dic['TargetTx1'] + diff_points_dic['targetTx2TxPHR1']
        points_dic['EndTxTime'] = points_dic['TxPHR1'] + tx_dur
        points_dic['rxStart_beforeCall'] = points_dic['EndTxTime'] + diff_points_dic['endTxTime2rxStartbefore']
        points_dic['rxStart_afterCall'] = points_dic['rxStart_beforeCall'] + diff_points_dic['rxstartBefore2After']
        points_dic['rxPHR'] = points_dic['rxStart_afterCall'] + diff_points_dic['rxstartAfter2rxPHR']
        points_dic['rxEnd'] = points_dic['rxPHR'] + rx_dur
        points_dic['WrapperCall2'] = points_dic['rxEnd'] + diff_points_dic['rxEnd2wrapperCall']
        points_dic['TargetTx2'] = points_dic['WrapperCall2'] + diff_points_dic['wrapperCall2TargetTx2']
        points_dic['TxPHR2'] = points_dic['TargetTx2'] + diff_points_dic['targetTx2TxPHR2']

        points = list(points_dic.values())

        arrows_x = [
            {'x1': points_dic['WrapperCall1'], 'x2':points_dic['WrapperReturn'], 'y': 1.5},
            {'x1': points_dic['WrapperCall1'], 'x2':points_dic['TargetTx1'], 'y': 0.5},
            {'x1': points_dic['TargetTx1'], 'x2':points_dic['TxPHR1'], 'y': 0.75},
            {'x1': points_dic['EndTxTime'], 'x2': points_dic['rxStart_beforeCall'], 'y': -0.5},
            {'x1': points_dic['EndTxTime'], 'x2': points_dic['EndTxTime']+1000, 'y': 0.5},
            {'x1': points_dic['rxStart_beforeCall'], 'x2':points_dic['rxStart_afterCall'], 'y': -0.75},
            {'x1': points_dic['rxStart_afterCall'], 'x2':points_dic['rxPHR'], 'y': -1.5},
            {'x1': points_dic['rxEnd'], 'x2':points_dic['WrapperCall2'], 'y': 0.5},
            {'x1': points_dic['rxEnd'], 'x2':points_dic['TargetTx2'], 'y': -0.5},
            {'x1': points_dic['rxEnd'], 'x2':points_dic['TxPHR2'], 'y': -0.75},
            {'x1': points_dic['WrapperCall2'], 'x2':points_dic['TargetTx2'], 'y': 0.75},
            {'x1': points_dic['TargetTx2'], 'x2':points_dic['TxPHR2'], 'y': 0.5},
        ]

        val_texts = [
            str(int(timings_df.txcall2aftertx.min()))+'/'+str(int(timings_df.txcall2aftertx.max()))+'/'+str(int(timings_df.txcall2aftertx.mean())),
            str(int(timings_df.txcall2targettime.min()))+'/'+str(int(timings_df.txcall2targettime.max()))+'/'+str(int(timings_df.txcall2targettime.mean())),
            str(int(timings_df.target2txphr.min()))+'/'+str(int(timings_df.target2txphr.max()))+'/'+str(int(timings_df.target2txphr.mean())),
            str(int(timings_df.txend2rxstart.min()))+'/'+str(int(timings_df.txend2rxstart.max()))+'/'+str(int(timings_df.txend2rxstart.mean())),
            '1000(to have)',
            str(int(timings_df.rxcall2afterrx.min()))+'/'+str(int(timings_df.rxcall2afterrx.max()))+'/'+str(int(timings_df.rxcall2afterrx.mean())),
            str(int(timings_df.afterRx2rxPHR.min()))+'/'+str(int(timings_df.afterRx2rxPHR.max()))+'/'+str(int(timings_df.afterRx2rxPHR.mean())),
            str(int(timings_df.rxend2txcall.min()))+'/'+str(int(timings_df.rxend2txcall.max()))+'/'+str(int(timings_df.rxend2txcall.mean())),
            str(int(timings_df.rxend2targettime.min()))+'/'+str(int(timings_df.rxend2targettime.max()))+'/'+str(int(timings_df.rxend2targettime.mean())),
            str(int(timings_df.rxend2txtime.min()))+'/'+str(int(timings_df.rxend2txtime.max()))+'/'+str(int(timings_df.rxend2txtime.mean())),
            str(int(timings_df.txcall2targettime.min()))+'/'+str(int(timings_df.txcall2targettime.max()))+'/'+str(int(timings_df.txcall2targettime.mean())),
            str(int(timings_df.target2txphr.min()))+'/'+str(int(timings_df.target2txphr.max()))+'/'+str(int(timings_df.target2txphr.mean())),
        ]

        # MAKE THE TIMING REPORT

        # Create the base line
        start = min(points)
        stop = max(points)

        fig = go.Figure()

        # Add baseline
        fig.add_shape(
            # Line Horizontal
            type="line",
            x0=start, y0=0,
            x1=stop, y1=0,
            line=dict(
                color="grey",
                width=1,
            ),
        )

        # legend for min/max/avg
        fig.add_annotation(
            x=1000, y=-1,
            xref="x", yref="y",
            text="min/max/avg",
            showarrow=False,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
            ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#636363",
            ax=20, ay=-30,
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
        )

        # add vertical lines
        for ii, (iname, ipt) in enumerate(zip(names, points)):
            level = levels_dic[iname]
            vert = 'top' if level < 0 else 'bottom'
            # fig.add_scatter(x=target2txphr_df['target2txphr'], y=target2txphr_df['pdf'], name="PDF", secondary_y=True, row=1, col=1)
            # print(ii, iname, ipt)
            fig.add_shape(
                # Line vertical
                type="line",
                x0=ipt, y0=0,
                x1=ipt, y1=level,
                line=dict(
                    color=colors_dic[iname],
                    width=2,
                )
            )

        # add labels to the lines
        fig.add_trace(go.Scatter(
            x=points,
            # y=[i * 1.05 for i in list(levels_dic.values())],
            y=[i for i in list(levels_dic.values())],
            text=list(names_label_dic.values()),
            textposition="top center",
            mode="text+markers",
            hoverinfo="none",
            marker=dict(size=12,
                        color='white',
                        line=dict(width=2,
                                  color='black'))
        ))

        # draw the horizontal lines
        i = 0
        for d in arrows_x:
            x1, x2, y = d.values()
            fig.add_shape(
                # Line horizontals for texts
                type="line",
                x0=x1, y0=y,
                x1=x2, y1=y,
                line=dict(
                    color='DarkOrange',
                    width=2,
                    dash="dot"
                )
            )

            i = i+1

        # add the values;labels over the horizontal line.
        x = [(sub["x1"]+sub["x2"]) / 2 for sub in arrows_x]
        y = [sub["y"]*1.15 for sub in arrows_x]
        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            text=val_texts,
            mode="text",
            hoverinfo="none",

        ))
        # POLL/ACK/DATA
        rx_dur = points_dic['rxEnd']-(points_dic['rxPHR'])
        txdiff = points_dic['TxPHR1'] - points_dic['TargetTx1']
        fig.add_bar(
            x=[(points_dic['TxPHR1']-txdiff+(tx_dur+txdiff)/2), (points_dic['rxPHR']-txdiff+(rx_dur+txdiff)/2), (points_dic['TxPHR2']-txdiff+(tx_dur+txdiff+100)/2)],
            y=[0.25, -0.25, 0.25],
            width=[tx_dur+txdiff, rx_dur+txdiff, (tx_dur+100+txdiff)],
            text=["POLL", "ACK", "DATA"],
            textposition="inside",
            hoverinfo="none",
            marker=dict(
                color=['darksalmon', 'darkseagreen', 'darksalmon'],
                line=dict(width=2,
                          color='black'))
        )

        fig.update_layout(
            title="CL Timing Summary Report",
            showlegend=False,
            yaxis=dict(
                showticklabels=False
            ),

        )

        fig.show()

        # MAKE THE TIMING GRAPHS
        # plot
        fig = make_subplots(4, 2,
                            specs=[[{"secondary_y": True},    {"secondary_y": True}],
                                   [{"secondary_y": True},    {"secondary_y": True}],
                                   [{"secondary_y": True},    {"secondary_y": True}],
                                   [{"secondary_y": True}, {"secondary_y": True}]],
                            subplot_titles=("Target Time to Tx PHR Time",
                                            "Tx End to Rx Start",
                                            "Rx End to Target Time",
                                            "rxend2txtime",
                                            "Tx Call to Target Time",
                                            "Rx End to Tx Call",
                                            "Rxcall to After Rx",
                                            "CL duration in msec"),
                            x_title="time in msec",
                            y_title="Frequency",
                            )

        # Add traces
        fig.add_bar(x=target2txphr_df['target2txphr'], y=target2txphr_df['freq'], name="Count", opacity=0.8, row=1, col=1)
        fig.add_scatter(x=target2txphr_df['target2txphr'], y=target2txphr_df['pdf'], name="PDF", secondary_y=True, row=1, col=1)
        fig.add_scatter(x=target2txphr_df['target2txphr'], y=target2txphr_df['cdf'], name="CDF", secondary_y=True, row=1, col=1)

        fig.add_bar(x=txend2rxstart_df['txend2rxstart'], y=txend2rxstart_df['freq'], name="Count", opacity=0.8, row=1, col=2)
        fig.add_scatter(x=txend2rxstart_df['txend2rxstart'], y=txend2rxstart_df['pdf'], name="PDF", secondary_y=True, row=1, col=2)
        fig.add_scatter(x=txend2rxstart_df['txend2rxstart'], y=txend2rxstart_df['cdf'], name="CDF", secondary_y=True, row=1, col=2)

        fig.add_bar(x=rxend2targettime_df['rxend2targettime'], y=rxend2targettime_df['freq'], name="Count", opacity=0.8, row=2, col=1)
        fig.add_scatter(x=rxend2targettime_df['rxend2targettime'], y=rxend2targettime_df['pdf'], name="PDF", secondary_y=True, row=2, col=1)
        fig.add_scatter(x=rxend2targettime_df['rxend2targettime'], y=rxend2targettime_df['cdf'], name="CDF", secondary_y=True, row=2, col=1)

        fig.add_bar(x=rxend2txtime_df['rxend2txtime'], y=rxend2txtime_df['freq'], name="Count", opacity=0.8, row=2, col=2)
        fig.add_scatter(x=rxend2txtime_df['rxend2txtime'], y=rxend2txtime_df['pdf'], name="PDF", secondary_y=True, row=2, col=2)
        fig.add_scatter(x=rxend2txtime_df['rxend2txtime'], y=rxend2txtime_df['cdf'], name="CDF", secondary_y=True, row=2, col=2)

        fig.add_bar(x=txcall2targettime_df['txcall2targettime'], y=txcall2targettime_df['freq'], name="Count", opacity=0.8, row=3, col=1)
        fig.add_scatter(x=txcall2targettime_df['txcall2targettime'], y=txcall2targettime_df['pdf'], name="PDF", secondary_y=True, row=3, col=1)
        fig.add_scatter(x=txcall2targettime_df['txcall2targettime'], y=txcall2targettime_df['cdf'], name="CDF", secondary_y=True, row=3, col=1)

        fig.add_bar(x=rxend2txcall_df['rxend2txcall'], y=rxend2txcall_df['freq'], name="Count", opacity=0.8, row=3, col=2)
        fig.add_scatter(x=rxend2txcall_df['rxend2txcall'], y=rxend2txcall_df['pdf'], name="PDF", secondary_y=True, row=3, col=2)
        fig.add_scatter(x=rxend2txcall_df['rxend2txcall'], y=rxend2txcall_df['cdf'], name="CDF", secondary_y=True, row=3, col=2)

        fig.add_bar(x=rxcall2afterrx_df['rxcall2afterrx'], y=rxcall2afterrx_df['freq'], name="Count", opacity=0.8, row=4, col=1)
        fig.add_scatter(x=rxcall2afterrx_df['rxcall2afterrx'], y=rxcall2afterrx_df['pdf'], name="PDF", secondary_y=True, row=4, col=1)
        fig.add_scatter(x=rxcall2afterrx_df['rxcall2afterrx'], y=rxcall2afterrx_df['cdf'], name="CDF", secondary_y=True, row=4, col=1)

        fig.add_bar(x=cl_dur_df['dur_ms'], y=cl_dur_df['freq'], name="Count", opacity=0.8, row=4, col=2)
        fig.add_scatter(x=cl_dur_df['dur_ms'], y=cl_dur_df['pdf'], name="PDF", secondary_y=True, row=4, col=2)
        fig.add_scatter(x=cl_dur_df['dur_ms'], y=cl_dur_df['cdf'], name="CDF", secondary_y=True, row=4, col=2)

        fig.update_layout(
            title="CL Timings",
            showlegend=False,
            hovermode='x',
            yaxis2=dict(
                title='PDF/CDF',
            )

        )

        fig.show()

    # buffer get/release
    if '0' in graph_ans_list or '4' in graph_ans_list:

        bufmgr_df = pd.DataFrame()
        filter_list = [19, 20]
        bufmgr_df = csv_df[csv_df.tracecode_dec.isin(filter_list)]

        trace_list = list(set(list(bufmgr_df.tracecode_dec)))
        if not set(filter_list).issubset(trace_list):
            print("\n**** All required traces {} are not present. Cannot draw the graph".format(filter_list))
            return
        bufmgr_df = bufmgr_df.assign(buffer=bufmgr_df.trace_info.str[-4:])
        bufmgr_df['buffer_dec'] = bufmgr_df.buffer.apply(int, base=16)
        # print(bufmgr_df[['tracecode_dec','buffer']].head(30))
        # print(bufmgr_df.head(10))

        bufmgr_get_df = bufmgr_df[bufmgr_df["tracecode_dec"] == 19][['byte', 'frt_dec', 'trace_info', 'buffer', 'buffer_dec']]

        bufmgr_get_df['owner'] = bufmgr_get_df.trace_info.str.split().str[2].str.split("(").str[0]
        bufmgr_get_df['owner'] = bufmgr_get_df.owner.str[4:]
        bufmgr_get_df['subfunc'] = bufmgr_get_df.trace_info.str.split().str[4]
        bufmgr_get_df.reset_index(inplace=True)

        # to get the rel frt
        def buf_filter(x):
            mydf = bufmgr_df[bufmgr_df.frt_dec > x.frt_dec]
            index = mydf[mydf.buffer == x.buffer].first_valid_index()

            if index:
                return mydf.at[index, 'frt_dec']
            else:
                return np.nan

        bufmgr_get_df['rel_frt'] = bufmgr_get_df.apply(buf_filter, axis=1)
        bufmgr_get_df['frt_diff'] = (bufmgr_get_df['rel_frt'] - bufmgr_get_df['frt_dec'])
        bufmgr_get_df['info'] = "<br><b>"+bufmgr_get_df.owner + "</b></br>" + " 0x" + bufmgr_get_df.buffer + " " + bufmgr_get_df.frt_diff.astype(str) + "us"
        # check if there are any leaks
        bufmgr_leak_df = bufmgr_get_df[bufmgr_get_df.isna().any(axis=1)]
        bufmgr_get_unleaked_df = bufmgr_get_df.dropna()
        bufmgr_get_df['leak'] = bufmgr_get_df.apply(lambda x: 1 if np.isnan([x.rel_frt]) else np.nan, axis=1)

        # print(bufmgr_leak_df.tail(30))
        unique_owners = bufmgr_get_unleaked_df.owner.unique()

        buf_owner_dic = dict()
        for owner in unique_owners:
            buf_owner_dic[owner] = (bufmgr_get_unleaked_df[bufmgr_get_unleaked_df['owner'].str.match(owner)])[['frt_dec', 'owner', 'buffer_dec', 'rel_frt', 'frt_diff', 'info']]

        # print(px.colors.qualitative.Dark24)
        buff_colors = px.colors.qualitative.Dark24
        # buff_colors = get_n_colors(len(unique_owners));

        fig = go.Figure()
        fig = make_subplots(rows=2, cols=1, subplot_titles=("Buffer claimed and released Timeline",
                                                            "Buffer claims, releases and leaks stats",),
                            )

        shapes = list()
        i = 0

        # per owner graphing
        for key, owner_df in buf_owner_dic.items():
            # print(key, owner_df)
            # draw a rectangle
            fig.add_bar(
                x=owner_df.frt_dec,
                y=owner_df.buffer_dec,
                width=owner_df.frt_diff,
                name=key,
                text=owner_df['info'] + "<br>FRT start:" + owner_df.frt_dec.astype(str) + "<br> FRT end: " + owner_df.rel_frt.astype(str),
                # hoverinfo='text',
                # hovertext="FRT start:" + owner_df.frt_dec.astype(str) +"<br> FRT end: " +owner_df.rel_frt.astype(str) +"<br>" + owner_df['info'],
                textposition="inside",
                hovertemplate='%{text}',            # hoverinfo="none",
                row=1,
                col=1,
                marker=dict(
                    color=buff_colors[i],
                    opacity=0.7,
                    line=dict(width=0.5,
                              color=buff_colors[i]))
            )
            i = i+1

        fig.update_layout(
            title="Buffer Management",
            showlegend=True,
            xaxis_tickformat='f',
            yaxis=dict(
                # visible=False,
                fixedrange=True,
            ),
            # hovermode='x',
            # shapes=shapes,
        )
        # fig.show()

        # bufmgr_get_df.leak = bufmgr_get_df.leak.replace(0,np.nan)
        buf_summary_df = (bufmgr_get_df.groupby('owner').count()).reset_index()[['owner', 'frt_dec', 'rel_frt', 'leak']]
        buf_summary_df.rename(columns={'frt_dec': 'buf_claim', 'rel_frt': 'buf_release', 'leak': 'buf_leak'}, inplace=True)
        # fig = px.bar(buf_summary_df, x="owner", y=["buf_claim", "buf_release", "buf_leak"],
        #              barmode='group', row=2, col=1
        #              )
        fig.add_trace(
            go.Bar(x=buf_summary_df.owner, y=buf_summary_df["buf_claim"], name="buf_claim", text=buf_summary_df["buf_claim"],
                   textposition='auto',),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=buf_summary_df.owner, y=buf_summary_df["buf_release"], name="buf_release", text=buf_summary_df["buf_release"],
                   textposition='auto',),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=buf_summary_df.owner, y=buf_summary_df["buf_leak"], name="buf_leak", text=buf_summary_df["buf_leak"],
                   textposition='auto',),
            row=2, col=1
        )

        # # print(fig)
        fig.update_layout(barmode='group')
        fig.show()

        # count of buffers get and released


cl_id = 0

if __name__ == "__main__":
    outputVer = ""
    date_today = get_datetime().split(' ')[0].split('-')
    date_today = date_today[2] + date_today[1] + date_today[0]
    graph_file = 'decoded.csv'
    graph_ans_list = []
    REACHABLE = False
    glob["QUIT"] = False

    # verify we have python atleast 3.x+
    assert sys.version_info >= (3, 0), "Requires Python 3.x+. Current Version is {}".format(sys.version.split(" ", 2)[0])

    check_and_install_package(['numpy'])

    epilog = """
    Example Usage:

    Example 1: Running a local hex file
        %(prog)s -f traces.log

    Example 2: Monitoring a live trace using wifi ipv4 addr.
        %(prog)s -i 100.70.100.118

    Example 3: Setting the debug mask and monitoring a live trace
        %(prog)s -m 81FF6702BCFB033E60C78F3FFFBFFF01000000FFFFFFFFFFFFFDDFFDDFFFFFFFFF7FFCFFFF -i 100.70.100.118

    Example 4: Outputing the decoded file (e.g. for live tracing)
        %(prog)s -i 100.70.100.118 -o decodedTraces.log

    Example 5: Monitoring a live trace with mask and save the hex traces and decoded file in csv as well
        %(prog)s -i 10.70.100.118 -m 81FF6702BCFB033E60C78F3FFFBFFF01000000FFFFFFFFFFFFFDDFFDDFFFFFFFFF7FFCFFFF -t -c

    Example 6: Display some graphs using decoded file in csv
        %(prog)s -f decoded.csv -g
        %(prog)s -f hex_trace.txt -g
        In second example, the app will create the necessary csv file

    """

    # write to a file per day
    outputfile = OUTPUT_FILE_NAME + "_" + date_today + OUTPUT_FILE_EXT

    my_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                        description='''Decode the hex trace for DSP for G5R
            - Live with the IPv4 Wifi address of the node
            - From a local file

    Requires Python 3.x''',
                                        epilog=epilog,
                                        )

    my_group = my_parser.add_mutually_exclusive_group(required=True)

    # Add the arguments
    my_parser.add_argument('-c', '--csv',
                           action='store_true',
                           help='Output CSV format also')
    my_parser.add_argument('-d', '--debug',
                           action='store_true',
                           help='Debug Mode')
    my_group.add_argument('-f', '--file',
                          type=str,
                          help='path to the local file to decode. The local file should be obtained from hexdump -C option')
    my_parser.add_argument('-g', '--graph',
                           action='store_true',
                           help='Show Graphs using decoded csv file or the hex traces. Limited functionality with live option -i')
    my_group.add_argument('-i', '--ip', metavar="IPv4",
                          type=str,
                          action=Ipv4Action,
                          help='Wifi IPv4 addr of the Node')

    my_group.add_argument('-l', '--listid',
                          type=int,
                          default=-1,
                          action=listIdAction,
                          help='''List the various IDs used. {}: ALL, {}: TRACE, {}: OWNERS, {}: STS, {}: FLAG, {}: PRIM'''.format(ID_ALL, ID_TRACE, ID_OWNERS, ID_STS, ID_FLAG, ID_PRIM))
    my_parser.add_argument('-m', '--mask',
                           action=maskAction,
                           help='{} byte tracing debug mask to set for live tracing'.format(TRACING_DEBUG_MASK_LEN))
    my_parser.add_argument('-n', '--nolog',
                           action='store_true',
                           help='Do not show the decoded traces in the output')
    my_parser.add_argument('-p', '--poll',
                           type=float,
                           default=POLL_INTERVAL,
                           help='Polling Inverval in seconds (Default:{})'.format(POLL_INTERVAL))

    my_parser.add_argument('-o', '--output',
                           default=outputfile,
                           help='Output to a file (Default={})'.format(outputfile))

    my_parser.add_argument('-t', '--trace',
                           action='store_true',
                           help='Output hex traces also. Works only with -i option')
    my_parser.add_argument('-v', action='version',
                           version="%(prog)s v" + __VERSION__)

    # Execute the parse_args() method
    try:
        args = my_parser.parse_args()
    except:
        exit()

    print("*** Monitoring traces v" + APP_VERSION +
          " started at " + get_datetime())

    tmp = args.output.split('.')
    hexfile = tmp[0]+"_hex."+tmp[1]
    csvfile = "decoded.csv"

    # register a handler when exiting
    signal.signal(signal.SIGINT, signal_handler)

    # check for -l option to just show the list of masks available for this version
    if args.listid != -1:
        even = False

        if args.listid == ID_ALL or args.listid == ID_TRACE:
            print("\n~~~ TRACE IDs MAP ~~~")
            for key, val in tracing_events_num_str.items():
                print("{:3d} 0x{:03X} {:50s} ".format(key, key, val),
                      end='\n' if even == True else'\t')
                even = not even
        if args.listid == ID_ALL or args.listid == ID_STS:
            print("\n~~~ STS IDs MAP ~~~")
            for key, val in sts_code_str.items():
                print("{:3d} 0x{:03X} {:50s} ".format(key, key, val),
                      end='\n' if even == True else'\t')
                even = not even
        if args.listid == ID_ALL or args.listid == ID_PRIM:
            print("\n~~~ PRIM IDs MAP ~~~")
            for key, val in prim_code_str.items():
                print("{:3d} 0x{:03X} {:50s} ".format(key, key, val),
                      end='\n' if even == True else'\t')
                even = not even
        if args.listid == ID_ALL or args.listid == ID_OWNERS:
            print("\n~~~ OWNERS IDs MAP ~~~")
            for key in range(len(owner_ids_arr)):
                print("{:2d} 0x{:02X} {:50s}".format(
                    key, key, owner_ids_arr[key]), end='\n' if even == True else'\t')
                even = not even
        if args.listid == ID_ALL or args.listid == ID_FLAG:
            print("\n~~~ FLAG IDs MAP ~~~")
            for key, val in pdll_flag_str.items():
                print("0x{:05X} {}".format(key, val))

        exit(0)

    # check node reachability
    if args.ip:
        if args.graph and not args.csv:
            print("-g option requires -c option. Please add the param and try again")
            exit(0)
        args.ip = args.ip.strip()
        print(" - Node IP '{}'..VALID..".format(args.ip), end='')
        if checkNodeReachability(args.ip) == RET_FAIL:
            print("UNREACHABLE!!!")
            exit(1)
            # ret=os.system('echo Y | plink -pw itron -ssh root@10.70.100.118 uptime')
        print("REACHABLE")
        REACHABLE = True

    if args.graph:

        graph_dic = {
            0: "All",
            1: "RTT Between CL DataGet Req/Cnf",
            2: "CL Timings",
            3: "Timeline Visualizer",
            4: "Buffer Get/Release",
        }

        for key, val in graph_dic.items():
            print("\t{} : {}".format(key, val))
        graph_ans = input("Which graph (use a single number or list like 1,2) ")
        graph_ans_list = graph_ans.split(',')
        result = all(int(elem, 10) in list(graph_dic.keys()) for elem in graph_ans_list)
        if not result:
            print("Invalid entry {}. Choose from {}".format(graph_ans, list(graph_dic.keys())))
            exit(0)

    # if file mode process and exit
    if args.file:
        extension = args.file.split('.')[-1].strip().lower()
        if not os.path.isfile(args.file):
            print("\n*** Cannot find the file '{}'".format(args.file))
            exit()
        if (extension == 'csv'):
            graph_file = args.file

        else:
            with open(args.file, 'r') as file:
                hexdump = file.read()
                # print(hexdump)
                process_hexdump(hexdump, 0, True)
            print("")
            print(
                " - Decoded Traces are saved to {}\{}".format(get_current_path(), args.output))

        if args.graph:
            graph_it()
        exit()

    print(" - Reading the device... ", end='')
    sys.stdout.flush()

    ret, outputVer = test_ssh(
        args.ip, "cat /etc/Version.txt;echo -n 'RF MAC: '; pib -gi 030000A2  --raw;echo -n 'Uptime: ';uptime;echo -n 'MAC ADDR: ';pib -gi FFFFFFF4;", True)
    if (ret != RET_SUCC or len(outputVer) == 0 or outputVer.strip() == ""):
        print("FAILED")
        print("Cannot read the pib. Check if DSP is running or NOT and try again.")
        exit(1)

    outputVer = str_decode(outputVer).strip()
    opp_macAddr = outputVer.split()[-1]
    macAddr = convert_pib_val(outputVer.split()[-1])
    outputVer = outputVer.replace(opp_macAddr, macAddr, 1)

    print('')
    print(outputVer)
    a7_ver_list = outputVer.split('\n')[2:5]
    a7_major = int(a7_ver_list[0].split(':', 2)[1], 10)
    a7_minor = int(a7_ver_list[1].split(':', 2)[1], 10)
    a7_build = int(a7_ver_list[2].split(':', 2)[1], 10)
    a7_ver = (a7_major, a7_minor, a7_build)
    if(a7_ver < MIN_A7_VER):
        print("\n\n*** The node Version A7 {} is not compatible. Minimum Required {}".format(a7_ver, MIN_A7_VER))
        choice = input("The APP may not function properly. Continue? (y/n)? ")
        if choice.lower() != 'y':
            exit(0)

    # if mask is provided, set and read back
    if args.mask:
        print(" - Setting the mask... {} ...".format(args.mask), end='')
        ret, output = test_ssh(
            args.ip, "pib -si E0000000 -v {} >/dev/null".format(args.mask))
        if (ret != RET_SUCC):
            print("FAILED")
            print("Cannot write the pib. Check if DSP is running or NOT")
            exit(1)
        print(" SUCCESS")

    print(" - Reading the mask... ", end='')
    ret, output = test_ssh(args.ip, "pib -gi E0000000")
    if (ret != RET_SUCC or str_decode(output)).strip() == "":
        print("FAILED")
        exit(1)
    output = str_decode(output).strip()
    output = convert_pib_val(output)
    if (args.mask and output != args.mask):
        print("{} ... MISMATCH".format(output))
        exit(1)

    print("{} ... SUCCESS".format((output)))

    # clean up once to remove residues.

    cleanup_proc()

    # handle exit to cleanup pipe
    # atexit.register(exit_handler)

    ret, output = test_ssh(
        args.ip, "cat /dev/dsp_rf_tracing |hexdump -C >> /tmp/hexTrace.log &")

    if ret != RET_SUCC:
        print("error {}".format(ret))
        exit()

    cur_line = 0
    last_count = 0
    showFirstLine = True

    print(" - Decoded Traces will be saved to {}\{}".format(get_current_path(), args.output))
    if args.trace:
        print(" - Hex Traces will be saved to {}\{}".format(get_current_path(), hexfile))
    if args.csv:
        print(" - decoded CSV will be saved to {}\{}".format(get_current_path(), csvfile))

    print("\n*** Monitoring LIVE on {} (Poll intv:{} secs)".format(args.ip, args.poll))
    print("")

    graph_shown = False

    # MAIN monitoring LOOP
    while True:

        # if args.mask:
        #     ret, output = test_ssh(
        #         args.ip, "pib -si E0000000 -v {} >/dev/null".format(args.mask))
        #     if (ret != RET_SUCC):
        #         print("Cannot write the pib. Check if DSP is running or NOT")
        #         REACHABLE = False
        #         my_wait(args.poll)
        #         continue

        REACHABLE = True
        ret, output = test_ssh(args.ip, "cat /tmp/hexTrace.log")

        hexdump = output.decode('utf-8')

        new_count = hexdump.count('\n')

        if (last_count != new_count):

            last_count = new_count
            cur_line = process_hexdump(hexdump, cur_line, showFirstLine)
            showFirstLine = False

            if (args.trace and hexdump):
                with open(hexfile, 'w') as fout:
                    fout.writelines(hexdump)

            if (args.graph and not graph_shown):
                print("\n\n##### Graphs are not live. It will be shown only once.")
                graph_it()
                graph_shown = True

        # time.sleep(args.poll)
        my_wait(args.poll, new_count)
