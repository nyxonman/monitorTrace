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
import json
import webbrowser
import math
from inspect import getframeinfo, stack

# from numpy.lib.function_base import _meshgrid_dispatcher

# list of global variables subject to change
glob = {
    'QUIT': False,
}
json_list = {}

MIN_A7_VER = (10, 0, 519)

OS_POSIX = "posix"
OS_WIN = "nt"
__VERSION__ = "3.3"
APP_VERSION = __VERSION__ + " {OS: " + os.name + "}"
OUTPUT_FILE_NAME = "lastdecodedTraces"
OUTPUT_FILE_EXT = ".log"
FILE_HTML = "monitorTrace_v" + __VERSION__ + ".html"
HEX_TRACE_DIR = "/media/mmcblk0p1/"
DEBUG_LOG_FILE = 'debug.log'

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
GRAPH_HIGHCHARTS = 1
GRAPH_PLOTLY = 2

ID_ALL = 0
ID_PRIM = 1
ID_STS = 2
ID_TRACE = 3
ID_FLAG = 4
ID_OWNERS = 5
ID_MAX = 6

GRAPH_OPTION = GRAPH_HIGHCHARTS
# GRAPH_OPTION = GRAPH_PLOTLY

graphs = {
    'rtt': {},
    'cl_timing': {},
    'timeline': {}
}

GRAPH_NUM_STR = {
    0: 'ALL',
    1: 'RTT Between clata.get and cldata.cnf',
    2: 'CL Timings',
    3: 'Timeline Visualiser',
    4: 'Buffer Management',
    5: 'CL Mode/Channel Stats'
}
DEFAULT_GRAPH = 0

valid_img_ext_list = [
    '.png', '.jpg', '.pdf', '.svg'
]

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
    60: "CL",
    61: "CL_HSM",
    62: "PHY_CALLBACKS_CLAIM",
    63: "PHY_CALLBACKS_RELEASE",
    64: "LMFS_REMOVE_SCH_ENTRY",
    65: "LMFS_REMOVE_SCH_EXIT",
    68: "HSM_EVENT_AND_ENTRY",
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
    125: "LMMGR_SRR_IND",
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
    202: "UPCALL_RX_TX_DELAY",
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
    232: "LMDC_TMR_CB",
    233: "LMDC_SWT_CATCHUP",
    234: "SDC_BYPASS",
    235: "LMDC_RESERVED",
    241: "SA_HAPPY_RETURN",
    242: "SA_ERROR_RETURN",
    243: "SA_HSM_HAPPY_RETURN",
    244: "SA_HSM_ERROR_RETURN",
    245: "SA_RX_START",
    246: "SA_DATA_REQ",
    247: "SA_STAT_REQ",
    248: "SA_PRIM_UP",
    249: "SA_PRIM_DOWN",
    250: "SA_LMSM_TIMEOUT",
    251: "SA_PHY_SR",
    270: "SA_RESERVED",
    271: "ELG",
    272: "ELG_TIMER",
    273: "ELG_EVENT",
    274: "ELG_IRQ",
    290: "ELG_RESERVED",



}
tracing_events_str_num = {value: key for key, value in tracing_events_num_str.items()}
MAX_TRACE_EVT = list(tracing_events_num_str.keys())[-1] + 1

TRACING_DEBUG_MASK_LEN = int(MAX_TRACE_EVT/8) + 1
DEFAULT_DEBUG_MASK = "81FF6702BCFB033EF0C78FFFFFFFFFFF07F4FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF07"

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
    "LMSM_PHYTST",
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
    "OID_LG",
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
    5: "ELG_EV_SFP",
    6: "ELG_EV_SFP_TXDONE",
    7: "ELG_EV_MOLF_WAKEUP",
    8: "ELG_EV_TX_BUNDLE",
    9: "ELG_EV_TX_BUNDLE_DONE",
    10: "ELG_EV_ENTER_SLPM",
    11: "ELG_EV_MAX",
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

mode_str = {
    0: "ILLEGAL",
    1: "100KBPS_MSK",
    2: "150KBPS_MSK",
    3: "150KBPS_GMSK",
    4: "200KBPS_GMSK",
    5: "300KBPS_GMSK",
    6: "DEPRECATED1",
    7: "100KBPS_GMSK",
    8: "4G_50KBPS_2FSK_M1",
    9: "4G_100KBPS_MSK",
    10: "4G_150KBPS_GMSK",
    11: "4G_200KBPS_GMSK",
    12: "4G_50KBPS_2FSK_M1_FEC",
    13: "4G_100KBPS_MSK_FEC",
    14: "4G_150KBPS_GMSK_FEC",
    15: "4G_200KBPS_GMSK_FEC",
    16: "4G_100KBPS_2FSK_M1",
    17: "4G_100KBPS_2FSK_M1_FEC",
    18: "250KBPS_GMSK",
    19: "500KBPS_GMSK",
    20: "DEPRECATED2",
    21: "4G_200KBPS_MSK_M1",
    22: "4G_300KBPS_GMSK",
    23: "4G_200KBPS_MSK_M1_FEC",
    24: "4G_300KBPS_GMSK_FEC",
    25: "4G_50KBPS_OFDM4",
    26: "4G_100KBPS_OFDM4",
    27: "4G_150KBPS_OFDM4",
    28: "4G_200KBPS_OFDM4",
    29: "4G_300KBPS_OFDM4",
    30: "4G_50KBPS_OFDM3",
    31: "4G_100KBPS_OFDM3",
    32: "4G_200KBPS_OFDM3",
    33: "4G_300KBPS_OFDM3",
    34: "4G_400KBPS_OFDM3",
    35: "4G_600KBPS_OFDM3",
    36: "4G_50KBPS_OFDM2",
    37: "4G_100KBPS_OFDM2",
    38: "4G_200KBPS_OFDM2",
    39: "4G_400KBPS_OFDM2",
    40: "4G_600KBPS_OFDM2",
    41: "4G_800KBPS_OFDM2",
    42: "4G_1200KBPS_OFDM2",
    43: "4G_100KBPS_OFDM1",
    44: "4G_200KBPS_OFDM1",
    45: "4G_400KBPS_OFDM1",
    46: "4G_800KBPS_OFDM1",
    47: "4G_1200KBPS_OFDM1",
    48: "4G_1600KBPS_OFDM1",
    49: "4G_2400KBPS_OFDM1",
    50: "4G_6250BPS_OQPSK100",
    51: "4G_12500BPS_OQPSK100",
    52: "4G_25KBPS_OQPSK100",
    53: "4G_50KBPS_OQPSK100",
    54: "HAN_250KBPS_OQPSK2000",
    55: "300KBPS_GMSK_800",
    56: "50KBPS_GFSK",
    57: "100KBPS_GFSK",
    58: "4G_50KBPS_GFSK",
    59: "4G_25KBPS_OQPSK200",
    60: "4G_50KBPS_OQPSK200",
    61: "4G_100KBPS_OQPSK200",
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
    "#252F99", "#00CCFF", "#674E60", "#FC009C", "#92896B",

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
]


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
            print("")
        finally:
            globals()[pkg] = importlib.import_module(package)


def LOG_INFO(msg, console=True):
    ''' string for debug logging info'''
    if console:
        print("{}".format(msg), flush=True)
    if args.debug == 0:
        return

    caller = getframeinfo(stack()[1][0])
    printStr = "{} [INFO:{:04d}] : {}.\n".format(get_datetime(), caller.lineno, msg)
    with open(DEBUG_LOG_FILE, 'a') as f:
        f.write(printStr)


def LOG_ERR(msg, console=True):
    ''' string for debug logging error'''
    if console:
        print("ERR : {}".format(msg), flush=True)
    if args.debug == 0:
        return

    caller = getframeinfo(stack()[1][0])
    printStr = "{} [ERR :{:04d}] : {}.\n".format(get_datetime(), caller.lineno, msg)
    with open(DEBUG_LOG_FILE, 'a') as f:
        f.write(printStr)


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

    LOG_INFO("Exec {} on {}".format(COMMAND, HOST), False)
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
        raw_output, err = p1.communicate(timeout=60)
    except:
        print("prob while communicating quit:{}", glob["QUIT"])
        print("err={}, retCode={}, raw_output={}".format(
            err, p1.returncode, raw_output))
        if glob['QUIT']:
            exit(1)

    # print(err, p1.returncode)
    # print(raw_output)
    if p1.returncode != RET_SUCC:
        LOG_ERR("### ERROR :" + str(err.decode('utf-8', 'ignore')).strip() + " ###", False)
        print("NOk")
    # LOG_DBG(raw_output)

    return p1.returncode, raw_output


def checkNodeReachability(ipv4Addr):
    '''check the reachability of the Root by sending a small packet of size 8B'''

    LOG_INFO(f"Checking Node reachability for {ipv4Addr}", False)

    if os.name == OS_WIN:
        p1 = subprocess.Popen([PING_CMD, PING_CNT, '1', PING_SIZE, '8', PING_RESP_TIME, '2000',
                               ipv4Addr], stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds=True)

    else:
        p1 = subprocess.Popen([PING_CMD, PING_CNT, '1', PING_SIZE, '8', PING_RESP_TIME,
                               '2', ipv4Addr], stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    raw_output, err = p1.communicate()

    LOG_INFO("ret ={},  {}".format(p1.returncode, (raw_output)), False)

    if p1.returncode != 0:
        LOG_ERR("Failed to reach node")
        return RET_FAIL

    return RET_SUCC


def process_cl(code, infoArr):
    """ process all cl related tracing codes """
    info = ""
    global cl_id
    global first_cl_id
    global total_cls

    if tracing_events_num_str[code] == "CL_NEW":
        clId = int(infoArr[14] + infoArr[13], 16)
        cl_id = clId
        if first_cl_id == 0:
            first_cl_id = cl_id
        else:
            total_cls = cl_id - first_cl_id + 1

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
        if not args.quiet:
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
        if not args.quiet:
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
    elif code == tracing_events_str_num["ELG"] or code == tracing_events_str_num["ELG_TIMER"] or code == tracing_events_str_num["ELG_EVENT"] or code == tracing_events_str_num["ELG_IRQ"]:
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
    mode = 'w'

    if showFirstLine:
        if not args.quiet:
            print(firstLine)
        outputList.extend(outputVer + "\n\n")
        outputList.extend(firstLine + "\n")
        csvList.append(["BYTENUM", "FRT_DEC", "FRT_HEX",
                        "[TRACECODE]:", "TRACE INFO"])

    for line in hexdump.splitlines()[startLine:]:
        byteArr = line.split(maxsplit=17)

        # print(byteArr, len(byteArr))
        if len(byteArr) != 18:
            LOG_ERR("Illegal Line #{} => {}".format(nlines, line), False)
            continue
        nlines = nlines + 1
        # get timestamp
        timestamp = int(byteArr[8] + byteArr[7] + byteArr[6] + byteArr[5] +
                        byteArr[4] + byteArr[3] + byteArr[2] + byteArr[1], 16)

        # get trace code
        tracecode = int(byteArr[12] + byteArr[11] +
                        byteArr[10] + byteArr[9], 16)

        if tracecode >= MAX_TRACE_EVT:
            LOG_ERR("Illegal Trace code {} in {}".format(tracecode, line), False)
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

        if not args.quiet:
            print(output, "[{}]".format(cl_id))

    halflen = int(len(output)/2) - int(len(get_datetime())/2)

    if not args.quiet:
        print(("-"*halflen) + "( "+get_datetime() + " )" + ("-" * halflen))

    with open(args.output, mode) as fout:
        fout.writelines(outputList)

    if args.csv:
        with open(csvfile, mode, newline='') as csvfileio:
            writer = csv.writer(csvfileio)
            writer.writerows(csvList)

    LOG_INFO("Written {} lines to {}".format(nlines, args.output), False)

    showFirstLine = False

    return nlines


def cleanup_proc():
    pid = b''
    print(" - Cleaning Residues... ", end='')
    LOG_INFO("Cleaning Residues", False)

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
    # command = "rm " +
    command = "(ls "+HEX_TRACE_DIR + "hexTrace.log >> /dev/null 2>&1 && rm  "+HEX_TRACE_DIR + "hexTrace.log) || echo -1"
    ret, pid = test_ssh(args.ip, command)

    print("REMOVED")
    LOG_INFO("Old Trace {} Removed".format(HEX_TRACE_DIR + "hexTrace.log"), False)


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


class exportAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):

        if not values[-4:] in valid_img_ext_list:

            print("Error: Invalid extension {}.Valid extensions {}".format(values, valid_img_ext_list))
            raise ValueError("Invalid Extension")
        setattr(namespace, self.dest, values)


def my_wait(sec, new_count=0):
    global cl_id
    global first_cl_id
    global total_cls
    for i in range(sec):
        # if(glob['QUIT']):
        #     break
        lines = "[{} lines decoded, startCL {}, lastCL {}, cnt={}]".format(new_count, first_cl_id, cl_id, total_cls)
        print("*** Polling {} ({}) in {:3d}sec... {}".format(args.ip,
                                                             macAddr, sec-i, lines), end='\r')
        sys.stdout.flush()
        time.sleep(1)
    if not args.quiet:
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
def show_required_traces(trace_list):
    for trace in trace_list:
        print(trace, " => ", tracing_events_num_str[trace])


def write_df_to_json(key, df, mode='a', isdict=False):
    with open('myJson.js', mode) as f:
        f.write(key+':')
        f.write('')
        f.write(json.dumps(df)) if isdict else f.write(df.to_json(orient='records'))
        f.write(',\n\n')


def graph_fastlink():
    filter_list = [149, 148]

    fast_link_df = cl_csv_df[(cl_csv_df.tracecode_dec.isin(filter_list))][['byte', 'frt_dec', 'tracecode_dec', 'sts', 'cl_id']]
    trace_list = list(set(list(fast_link_df.tracecode_dec)))
    if sorted(trace_list) != sorted(filter_list):
        print("\n**** All required traces {} are not present {}. Cannot draw the graph".format(filter_list, trace_list))
        show_required_traces(filter_list)
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
        if not args.quiet:
            print("Done...Rendering/Preparing graph...", flush=True, end='')

        # Create figure with secondary y-axisspecs
        if(graphs['rtt'] == {}):
            if GRAPH_OPTION == GRAPH_PLOTLY:
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

            elif GRAPH_OPTION == GRAPH_HIGHCHARTS:
                write_df_to_json('rttJson', rtt_df)
            if not args.quiet:
                print("Done", flush=True)

        else:
            # print(graphs['rtt'])
            graphs['rtt'].data[0].x = list(rtt_df['diff'])
            graphs['rtt'].data[0].y = list(rtt_df['freq'])

            graphs['rtt'].data[1].x = list(rtt_df['diff'])
            graphs['rtt'].data[1].y = list(rtt_df['pdf'])

            graphs['rtt'].data[2].x = list(rtt_df['diff'])
            graphs['rtt'].data[2].y = list(rtt_df['cdf'])


def graph_cl_timings():
    global timings_df

    # target2txphr
    timings_df['dummy'] = timings_df.dc_col.shift(-2)
    timings_df['dummy_frt'] = timings_df.frt_val.shift(-2)
    timings_df['target2txphr'] = np.where(((timings_df.beforetx_col == 'beforeTx') & (timings_df.dummy == 'dc')), timings_df.dummy_frt-timings_df.frt_val, np.nan)
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

    # txcall2txphr
    timings_df['dummy'] = timings_df.dc_col.shift(-2)
    timings_df['dummy_frt'] = timings_df.frt_val.shift(-2)
    timings_df['txcall2txphr'] = np.where(((timings_df.beforetx_col == 'beforeTx') & (timings_df.dummy == 'dc')), timings_df.dummy_frt-timings_df.frt_dec, np.nan)
    timings_df.drop(columns=['dummy', 'dummy_frt'], inplace=True)

    # freq
    txcall2txphr_df = timings_df[['byte', 'txcall2txphr']].groupby('txcall2txphr').agg('count').rename(columns={'byte': 'freq'}).reset_index()
    txcall2txphr_df = txcall2txphr_df.astype({'txcall2txphr': int})
    # PDF
    txcall2txphr_df['pdf'] = txcall2txphr_df['freq'] / sum(txcall2txphr_df['freq'])
    # CDF
    txcall2txphr_df['cdf'] = txcall2txphr_df['pdf'].cumsum()
    txcall2txphr_df = txcall2txphr_df.reset_index()

    # txend2rxstart
    timings_df['dummy'] = timings_df.beforerx_col.shift(-1)
    timings_df['dummy_frt'] = timings_df.frt_dec.shift(-1)
    timings_df['txend2rxstart'] = np.where(((timings_df.txend_col == 'txEnd') & (timings_df.dummy == 'beforeRx')), timings_df.dummy_frt-timings_df.frt_val, np.nan)
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
    timings_df['rxend2targettime'] = np.where(((timings_df.rxend_col == 'rxEnd') & (timings_df.dummy == 'beforeTx') & (
        timings_df.cl_id == timings_df.dummy_cl_id)), timings_df.dummy_frt-timings_df.frt_val, np.nan)
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
    timings_df['rxend2txtime'] = np.where(((timings_df.rxend_col == 'rxEnd') & (timings_df.dummy == 'dc') & (
        timings_df.cl_id == timings_df.dummy_cl_id)), timings_df.dummy_frt-timings_df.frt_val, np.nan)
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
    timings_df['txcall2targettime'] = np.where(((timings_df.beforetx_col == 'beforeTx')), timings_df.frt_val-timings_df.frt_dec, np.nan)
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
    timings_df['txcall2aftertx'] = np.where(((timings_df.beforetx_col == 'beforeTx') & (timings_df.dummy == 'afterTx')), timings_df.dummy_frt-timings_df.frt_dec, np.nan)
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
    timings_df['rxend2txcall'] = np.where(((timings_df.rxend_col == 'rxEnd') & (timings_df.dummy == 'beforeTx') & (
        timings_df.cl_id == timings_df.dummy_cl_id)), timings_df.dummy_frt-timings_df.frt_val, np.nan)
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
    # timings_df.rxcall2afterrx = timings_df.apply(lambda x: x.dummy_frt-x.frt_dec if x.beforerx_col == 'beforeRx' and x.dummy == 'afterRx' else np.nan, axis=1)
    timings_df['rxcall2afterrx'] = np.where(((timings_df.beforerx_col == 'beforeRx') & (timings_df.dummy == 'afterRx')), timings_df.dummy_frt-timings_df.frt_dec, np.nan)
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
        cl_dur_df['cl_dur'] = cl_dur_df.apply(lambda x: x['trace_info'].split(' ')[3].split('msec')[0], axis=1)
        cl_dur_df.drop(columns=['trace_info', 'sts'], inplace=True)
        cl_dur_df['cl_dur'] = cl_dur_df['cl_dur'].astype(int)
        # cl_dur_df = cl_dur_df.sort_values(by='cl_dur')
        cl_dur_df = cl_dur_df.groupby('cl_dur').agg(
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
    timings_df.drop(columns=['dummy_frt'], inplace=True)

    # drop values higher than 3sec
    timings_df.afterRx2rxPHR = timings_df.apply(lambda x: np.nan if np.isnan([x.afterRx2rxPHR]) or x.afterRx2rxPHR > 3000.0 else x.afterRx2rxPHR, axis=1)

    if not args.quiet:
        print("Done...Rendering/Preparing Graph...Report...", flush=True, end='')

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

    # Obtain the min/max/avg NaN safe
    txcall2aftertx_mean = int(timings_df.txcall2aftertx.mean()) if not np.isnan(timings_df.txcall2aftertx.mean()) else 0
    txcall2targettime_mean = int(timings_df.txcall2targettime.mean()) if not np.isnan(timings_df.txcall2targettime.mean()) else 0
    target2txphr_mean = int(timings_df.target2txphr.mean()) if not np.isnan(timings_df.target2txphr.mean()) else 0
    txend2rxstart_mean = int(timings_df.txend2rxstart.mean()) if not np.isnan(timings_df.txend2rxstart.mean()) else 0
    rxcall2afterrx_mean = int(timings_df.rxcall2afterrx.mean()) if not np.isnan(timings_df.rxcall2afterrx.mean()) else 0
    rxend2txcall_mean = int(timings_df.rxend2txcall.mean()) if not np.isnan(timings_df.rxend2txcall.mean()) else 0
    afterRx2rxPHR_mean = int(timings_df.afterRx2rxPHR.mean()) if not np.isnan(timings_df.afterRx2rxPHR.mean()) else 0
    txcall2targettime_mean = int(timings_df.txcall2targettime.mean()) if not np.isnan(timings_df.txcall2targettime.mean()) else 0
    rxend2targettime_mean = int(timings_df.rxend2targettime.mean()) if not np.isnan(timings_df.rxend2targettime.mean()) else 0
    rxend2txtime_mean = int(timings_df.rxend2txtime.mean()) if not np.isnan(timings_df.rxend2txtime.mean()) else 0
    target2txphr_mean = int(timings_df.target2txphr.mean()) if not np.isnan(timings_df.target2txphr.mean()) else 0

    txcall2aftertx_max = int(timings_df.txcall2aftertx.max()) if not np.isnan(timings_df.txcall2aftertx.max()) else 0
    txcall2targettime_max = int(timings_df.txcall2targettime.max()) if not np.isnan(timings_df.txcall2targettime.max()) else 0
    target2txphr_max = int(timings_df.target2txphr.max()) if not np.isnan(timings_df.target2txphr.max()) else 0
    txend2rxstart_max = int(timings_df.txend2rxstart.max()) if not np.isnan(timings_df.txend2rxstart.max()) else 0
    rxcall2afterrx_max = int(timings_df.rxcall2afterrx.max()) if not np.isnan(timings_df.rxcall2afterrx.max()) else 0
    rxend2txcall_max = int(timings_df.rxend2txcall.max()) if not np.isnan(timings_df.rxend2txcall.max()) else 0
    afterRx2rxPHR_max = int(timings_df.afterRx2rxPHR.max()) if not np.isnan(timings_df.afterRx2rxPHR.max()) else 0
    txcall2targettime_max = int(timings_df.txcall2targettime.max()) if not np.isnan(timings_df.txcall2targettime.max()) else 0
    rxend2targettime_max = int(timings_df.rxend2targettime.max()) if not np.isnan(timings_df.rxend2targettime.max()) else 0
    rxend2txtime_max = int(timings_df.rxend2txtime.max()) if not np.isnan(timings_df.rxend2txtime.max()) else 0
    target2txphr_max = int(timings_df.target2txphr.max()) if not np.isnan(timings_df.target2txphr.max()) else 0

    txcall2aftertx_min = int(timings_df.txcall2aftertx.min()) if not np.isnan(timings_df.txcall2aftertx.min()) else 0
    txcall2targettime_min = int(timings_df.txcall2targettime.min()) if not np.isnan(timings_df.txcall2targettime.min()) else 0
    target2txphr_min = int(timings_df.target2txphr.min()) if not np.isnan(timings_df.target2txphr.min()) else 0
    txend2rxstart_min = int(timings_df.txend2rxstart.min()) if not np.isnan(timings_df.txend2rxstart.min()) else 0
    rxcall2afterrx_min = int(timings_df.rxcall2afterrx.min()) if not np.isnan(timings_df.rxcall2afterrx.min()) else 0
    rxend2txcall_min = int(timings_df.rxend2txcall.min()) if not np.isnan(timings_df.rxend2txcall.min()) else 0
    afterRx2rxPHR_min = int(timings_df.afterRx2rxPHR.min()) if not np.isnan(timings_df.afterRx2rxPHR.min()) else 0
    txcall2targettime_min = int(timings_df.txcall2targettime.min()) if not np.isnan(timings_df.txcall2targettime.min()) else 0
    rxend2targettime_min = int(timings_df.rxend2targettime.min()) if not np.isnan(timings_df.rxend2targettime.min()) else 0
    rxend2txtime_min = int(timings_df.rxend2txtime.min()) if not np.isnan(timings_df.rxend2txtime.min()) else 0
    target2txphr_min = int(timings_df.target2txphr.min()) if not np.isnan(timings_df.target2txphr.min()) else 0

    diff_points_dic = {
        'wrapperCall2Return1': txcall2aftertx_mean,
        'wrapperCall2TargetTx1': txcall2targettime_mean,
        'targetTx2TxPHR1': target2txphr_mean,
        'endTxTime2rxStartbefore': txend2rxstart_mean,
        'rxstartBefore2After': rxcall2afterrx_mean,
        'rxEnd2wrapperCall': rxend2txcall_mean,
        'rxstartAfter2rxPHR': afterRx2rxPHR_mean,
        'wrapperCall2TargetTx2': txcall2targettime_mean,
        'rxEnd2targetTx': rxend2targettime_mean,
        'rxEnd2TxPHR': rxend2txtime_mean,
        'targetTx2TxPHR2': target2txphr_mean,
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

    # fill in the min/max/avg
    val_texts = [
        str(txcall2aftertx_min)+'/'+str(txcall2aftertx_max)+'/'+str(txcall2aftertx_mean),
        str(txcall2targettime_min)+'/'+str(txcall2targettime_max)+'/'+str(txcall2targettime_mean),
        str(target2txphr_min)+'/'+str(target2txphr_max)+'/'+str(target2txphr_mean),
        str(txend2rxstart_min)+'/'+str(txend2rxstart_max)+'/'+str(txend2rxstart_mean),
        '1000(default)',
        str(rxcall2afterrx_min)+'/'+str(rxcall2afterrx_max)+'/'+str(rxcall2afterrx_mean),
        str(afterRx2rxPHR_min)+'/'+str(afterRx2rxPHR_max)+'/'+str(afterRx2rxPHR_mean),
        str(rxend2txcall_min)+'/'+str(rxend2txcall_max)+'/'+str(rxend2txcall_mean),
        str(rxend2targettime_min)+'/'+str(rxend2targettime_max)+'/'+str(rxend2targettime_mean),
        str(rxend2txtime_min)+'/'+str(rxend2txtime_max)+'/'+str(rxend2txtime_mean),
        str(txcall2targettime_min)+'/'+str(txcall2targettime_max)+'/'+str(txcall2targettime_mean),
        str(target2txphr_min)+'/'+str(target2txphr_max)+'/'+str(target2txphr_mean),
    ]

    # MAKE THE TIMING REPORT

    # Create the base line
    if GRAPH_OPTION == GRAPH_PLOTLY:
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
                width=2,
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
    else:
        summary = {
            "colors_dic": colors_dic,
            "val_texts": val_texts,
            "levels_dic": levels_dic,
            "arrows_x": arrows_x,
            "rx_dur": rx_dur,
            "names_label_dic": names_label_dic,
            # "txdiff": txdiff,
            "points_dic": points_dic,
        }
        write_df_to_json('cltimingJson', summary, isdict=True)
    # end of if GRAPH_OPTION == GRAPH_PLOTLY:

    if not args.quiet:
        print("Done... timing...", flush=True, end='')

    # MAKE THE TIMING GRAPHS
    # plot
    if GRAPH_OPTION == GRAPH_PLOTLY:
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

        fig.add_bar(x=cl_dur_df['cl_dur'], y=cl_dur_df['freq'], name="Count", opacity=0.8, row=4, col=2)
        fig.add_scatter(x=cl_dur_df['cl_dur'], y=cl_dur_df['pdf'], name="PDF", secondary_y=True, row=4, col=2)
        fig.add_scatter(x=cl_dur_df['cl_dur'], y=cl_dur_df['cdf'], name="CDF", secondary_y=True, row=4, col=2)

        fig.update_layout(
            title="CL Timings",
            showlegend=False,
            hovermode='x',
            yaxis2=dict(
                title='PDF/CDF',
            )
        )
        fig.show()
    else:
        write_df_to_json("cltimings_target2txphrJson", target2txphr_df)
        write_df_to_json("cltimings_txcall2txphrJson", txcall2txphr_df)
        write_df_to_json("cltimings_txend2rxstartJson", txend2rxstart_df)
        write_df_to_json("cltimings_rxend2targettimeJson", rxend2targettime_df)
        write_df_to_json("cltimings_rxend2txtimeJson", rxend2txtime_df)
        write_df_to_json("cltimings_txcall2targettimeJson", txcall2targettime_df)
        write_df_to_json("cltimings_txcall2aftertxJson", txcall2aftertx_df)
        write_df_to_json("cltimings_rxend2txcallJson", rxend2txcall_df)
        write_df_to_json("cltimings_rxcall2afterrxJson", rxcall2afterrx_df)
        write_df_to_json("cltimings_cl_durJson", cl_dur_df)

    if not args.quiet:
        print("Done", flush=True, end='\n')


def graph_timeline_visualiser():
    timeline_tx_color = {

        "TOP": colors_list[0],
        "IDLE": colors_list[1],
        "FH": 'cornflowerblue',
        "RXB": 'RoyalBlue',
        "TXB": 'crimson',
        "CL": 'darksalmon',
        "BCAST": 'Violet',
        "SA": colors_list[7],
        "LLS": colors_list[8],
        "ELG": colors_list[9],
    }
    timeline_rx_color = {

        "TOP": colors_list[0],
        "IDLE": colors_list[1],
        "FH": 'LightSeaGreen',
        "RXB": 'RoyalBlue',
        "TXB": 'crimson',
        "CL": 'darkseagreen',
        "BCAST": 'Violet',
        "SA": colors_list[7],
        "LLS": colors_list[8],
        "ELG": colors_list[9],
    }

    def hoverinfo(x, type):

        if type == "rx":
            seqinfo = str(x.rx_seq_ctrl)
            ts_start = str(x.ts_rxstart)
            ts_end = str(x.ts_rxend)
            dur = str(x.rx_dur/1000).strip()
        else:
            seqinfo = str(x.tx_seq_ctrl)
            ts_start = str(x.ts_txstart)
            ts_end = str(x.ts_txend)
            dur = str(x.tx_dur/1000).strip()

        ret = ""
        ret = "~~~( " + x.owner + " )~~~<br>"
        if(x.owner == "CL"):
            ret = ret + "<b>CLId </b>" + str(x.cl_id) + ", " + x.cl_mac[10:] + "<br>" + \
                x.txrx_param + "<br>" + \
                "<b>seqctrl:</b> " + seqinfo + "<br>"
        if(x.owner == 'CL' or x.owner == 'FH'):
            ret = ret + str(x.nextcli) + "<br>"
        ret = ret + "<br><b>Start:</b>" + ts_start + "<br><b>End:</b>" + ts_end + "<br><b>dur: </b>" + dur + " msec"
        return ret

    # rx
    timeline_rx_df = pd.DataFrame()
    timeline_rx_df = timings_df[['byte', 'owner', 'nextcli', 'cl_id', 'cl_mac', 'rx_seq_ctrl', 'txrx_param', 'ts_rxstart', 'ts_rxend']]
    timeline_rx_df = timeline_rx_df.assign(ts_rxend=timeline_rx_df.ts_rxend.shift(-1))
    timeline_rx_df.dropna(subset=['ts_rxstart', 'ts_rxend'], inplace=True)
    timeline_rx_df['rx_dur'] = timeline_rx_df.ts_rxend - timeline_rx_df.ts_rxstart
    timeline_rx_df['color'] = timeline_rx_df.owner.apply(lambda x: timeline_rx_color[x])
    timeline_rx_df['hoverinfo'] = timeline_rx_df.apply(lambda x: hoverinfo(x, "rx"), axis=1)
    err_df = timeline_rx_df[timeline_rx_df.rx_dur <= 0]

    if(not (err_df.empty)):
        timeline_rx_df = timeline_rx_df[timeline_rx_df.rx_dur > 0]
        print("\n\n\t\t **** ERROR timeline_rx_df")
        print(err_df.head())
        print(err_df.shape)

    # tx
    timeline_tx_df = timings_df[['byte', 'owner', 'nextcli', 'cl_id', 'cl_mac', 'tx_seq_ctrl', 'txrx_param', 'ts_txstart', 'ts_txend']]
    timeline_tx_df = timeline_tx_df.assign(ts_txend=timeline_tx_df.ts_txend.shift(-1))
    timeline_tx_df.dropna(subset=['ts_txstart', 'ts_txend'], inplace=True)
    timeline_tx_df['tx_dur'] = timeline_tx_df.ts_txend - timeline_tx_df.ts_txstart
    timeline_tx_df['color'] = timeline_tx_df.owner.apply(lambda x: timeline_tx_color[x])
    timeline_tx_df['hoverinfo'] = timeline_tx_df.apply(lambda x: hoverinfo(x, "tx"), axis=1)
    timeline_tx_df = timeline_tx_df[timeline_tx_df.tx_dur <= 500000]
    err_df = timeline_tx_df[timeline_tx_df.tx_dur <= 0]

    if(not (err_df.empty)):
        timeline_tx_df = timeline_tx_df[timeline_tx_df.tx_dur > 0]
        print("\n\n\t\t **** ERROR timeline_tx_df")
        print(err_df.head())
        print(err_df.shape)

    # PHY INDICATIONS and CALLs
    filter_list = [1, 2, 3, 4, 6, 113, 114, 115, 116, 117, 118, 140, 141, 148, 149]
    timeline_phycallind_df = pd.DataFrame()
    timeline_phycallind_df = cl_csv_df[cl_csv_df.tracecode_dec.isin(filter_list)]
    timeline_phycallind_df = timeline_phycallind_df.assign(y1=pd.Series(np.nan))

    timeline_phycallind_df['color'] = timeline_phycallind_df.tracecode_dec.apply(lambda x: colors_list[x])
    timeline_phycallind_df.drop(columns=['frt_hex'], inplace=True)

    # CL Traces
    filter_list = [129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 142, 143, 144, 145, 146, 147, 150]
    timeline_cl_df = pd.DataFrame()
    timeline_cl_df = cl_csv_df[cl_csv_df.tracecode_dec.isin(filter_list)]
    timeline_cl_df = timeline_cl_df.assign(color=pd.Series(np.nan))
    timeline_cl_df['color'] = timeline_cl_df.tracecode_dec.apply(lambda x: colors_list[x+64])

    # CL start END
    filter_list = [131, 132]

    timeline_cl_start_df = cl_csv_df[cl_csv_df.tracecode_dec == 131][['byte', 'frt_dec', 'cl_id', 'cl_mac']].rename(columns={'frt_dec': 'clstart'})
    timeline_cl_end_df = cl_csv_df[cl_csv_df.tracecode_dec == 132][['byte', 'frt_dec', 'cl_id', 'cl_mac']].rename(columns={'frt_dec': 'clend'})

    timeline_cl_startend_df = timeline_cl_start_df.merge(timeline_cl_end_df, on='cl_id', how='left')
    timeline_cl_startend_df['cldiff'] = timeline_cl_startend_df.clend - timeline_cl_startend_df.clstart
    timeline_cl_startend_df = timeline_cl_startend_df.dropna()
    timeline_cl_startend_df['hoverinfo'] = "CL " + timeline_cl_startend_df.cl_id.astype(str) + ", " + (
        timeline_cl_startend_df.cldiff/1000).astype(int).astype(str) + "msec<br>" + timeline_cl_startend_df.cl_mac_x.str[10:]
    err_df = timeline_cl_startend_df[timeline_cl_startend_df.cldiff <= 0]

    if(not (err_df.empty)):
        timeline_cl_startend_df = timeline_cl_startend_df[timeline_cl_startend_df.cldiff > 0]
        print("\n\n\t\t **** ERROR timeline_cl_startend_df")
        print(err_df.head())
        print(err_df.shape)

    if not args.quiet:
        print("Done...Rendering/Preparing Graph...", flush=True, end='')
    if GRAPH_OPTION == GRAPH_PLOTLY:

        fig = go.Figure()

        # add clstart end
        fig.add_bar(
            x=timeline_cl_startend_df.clstart + timeline_cl_startend_df.cldiff/2,
            y=[6]*len(timeline_tx_df.index),
            width=timeline_cl_startend_df.cldiff,
            base=-3,
            name="CL",
            text=timeline_cl_startend_df.hoverinfo,
            textposition="outside",
            hovertemplate='%{text}',            # hoverinfo="none",
            # hoverinfo="none",
            marker=dict(
                # color='darksalmon',
                color='Wheat',
                opacity=0.35,
                line=dict(width=1,
                          color='orange'))
        )

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
                # color='darksalmon',
                color=timeline_tx_df['color'],
                opacity=1,
                line=dict(width=1,
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
                # color='darkseagreen',
                color=timeline_rx_df['color'],
                line=dict(width=1,
                          color=timeline_rx_df['color']))
        )
        # add PHY Indications and calls

        fig.add_scatter(
            x=timeline_phycallind_df.frt_dec,
            y=[0]*len(timeline_phycallind_df.index),
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
        # add CL traces
        fig.add_scatter(
            x=timeline_cl_df.frt_dec,
            y=[0]*len(timeline_cl_df.index),
            mode="markers",
            name="CL Traces",
            text="<b>CL_ID:</b> " + timeline_cl_df.cl_id + "<br>" + timeline_cl_df.trace_info,
            hovertemplate="<b>FRT:</b>%{x}<br>%{text}",
            visible="legendonly",
            # hoverinfo="none",
            marker=dict(
                color='white',
                line=dict(width=1,
                          color=timeline_cl_df.color))
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

    elif GRAPH_OPTION == GRAPH_HIGHCHARTS:

        write_df_to_json("timeline_clStartEndJson", timeline_cl_startend_df[['cl_id', 'cldiff', 'clend', 'clstart', 'hoverinfo']])

        write_df_to_json("timeline_txJson", timeline_tx_df[['cl_id', 'color', 'hoverinfo', 'ts_txstart', 'ts_txend', 'tx_dur']])

        write_df_to_json("timeline_rxJson", timeline_rx_df[['cl_id', 'color', 'hoverinfo', 'ts_rxstart', 'ts_rxend', 'rx_dur']])

        write_df_to_json("timeline_phyIndJson", timeline_phycallind_df[["cl_id", "frt_dec", "trace_info", "color"]])

        write_df_to_json("timeline_clTracesJson", timeline_cl_df[["cl_id", "frt_dec", "trace_info", "color"]])

    if not args.quiet:
        print("Done", flush=True, end='\n')


def graph_buf_mgr():
    bufmgr_df = pd.DataFrame()
    filter_list = [19, 20]
    bufmgr_df = csv_df[csv_df.tracecode_dec.isin(filter_list)]

    trace_list = list(set(list(bufmgr_df.tracecode_dec)))
    if not set(filter_list).issubset(trace_list):
        print("\n**** All required traces {} are not present. Cannot draw the graph".format(filter_list))
        show_required_traces(filter_list)
        return
    bufmgr_df = bufmgr_df.assign(buffer=bufmgr_df.trace_info.str[-4:])
    bufmgr_df['buffer_dec'] = bufmgr_df.buffer.apply(int, base=16)

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

    if not args.quiet:
        print("Done...Rendering Graph...", flush=True, end='')

    # print(px.colors.qualitative.Dark24)
    # buff_colors = get_n_colors(len(unique_owners));
    if GRAPH_OPTION == GRAPH_PLOTLY:
        buff_colors = px.colors.qualitative.Dark24
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

        fig.show()

    # bufmgr_get_df.leak = bufmgr_get_df.leak.replace(0,np.nan)
    buf_summary_df = (bufmgr_get_df.groupby('owner').count()).reset_index()[['owner', 'frt_dec', 'rel_frt', 'leak']]
    buf_summary_df.rename(columns={'frt_dec': 'buf_claim', 'rel_frt': 'buf_release', 'leak': 'buf_leak'}, inplace=True)
    # fig = px.bar(buf_summary_df, x="owner", y=["buf_claim", "buf_release", "buf_leak"],
    #              barmode='group', row=2, col=1
    #              )
    if GRAPH_OPTION == GRAPH_PLOTLY:

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

    if GRAPH_OPTION == GRAPH_HIGHCHARTS:
        write_df_to_json("buffer_summaryJson", buf_summary_df[['owner', 'buf_claim', 'buf_release', 'buf_leak']])
        # print(buf_owner_dic)
        bufmgr_get_unleaked_df
        write_df_to_json("buffer_Json", bufmgr_get_unleaked_df[['frt_dec', 'owner', 'buffer_dec', 'rel_frt', 'frt_diff', 'info']])

        # for key, owner_df in buf_owner_dic.items():
        #     val = "buffer_" + key.lower() + "Json"
        #     write_df_to_json(val, owner_df[['frt_dec', 'buffer_dec', 'frt_diff', 'rel_frt', 'info']])

        # write_df_to_json("buffer_ownerJson", buf_owner_dic[['frt_dec', 'buf_dec', 'frt_diff', 'rel_frt', 'info']])

    if not args.quiet:
        print("Done", flush=True, end='\n')


def graph_mode_chan():
    modechan_df = pd.DataFrame()
    filter_list = [140, 141]
    modechan_df = csv_df[csv_df.tracecode_dec.isin(filter_list)][['byte', 'txrx_param', 'tracecode_dec']]
    trace_list = list(set(list(modechan_df.tracecode_dec)))
    if not set(filter_list).issubset(trace_list):
        print("\n**** All required traces {} are not present. Cannot draw the graph".format(filter_list))
        show_required_traces(filter_list)
        return
    modechan_df[['del1', 'mode', 'del2', 'chan']] = modechan_df.txrx_param.str.split(expand=True)
    modechan_df.drop(columns=['del1', 'del2', 'txrx_param'], inplace=True)
    modechan_df['mode'] = modechan_df['mode'].apply(lambda x: mode_str[int(x, 10)] + "("+x+")")

    modechan_tx_df = modechan_df[modechan_df.tracecode_dec == 140]
    modechan_rx_df = modechan_df[modechan_df.tracecode_dec == 141]

    modestats_tx_df = modechan_tx_df[['byte', 'mode']].groupby(['mode']).agg('count').rename(columns={'byte': 'count'}).reset_index()
    modestats_rx_df = modechan_rx_df[['byte', 'mode']].groupby(['mode']).agg('count').rename(columns={'byte': 'count'}).reset_index()

    chanstats_tx_df = modechan_tx_df[['byte', 'chan']].groupby(['chan']).agg('count').rename(columns={'byte': 'count'}).reset_index()
    chanstats_rx_df = modechan_rx_df[['byte', 'chan']].groupby(['chan']).agg('count').rename(columns={'byte': 'count'}).reset_index()

    if not args.quiet:
        print("Done...Rendering/Preparing Graph...", flush=True, end='')
    if GRAPH_OPTION == GRAPH_PLOTLY:

        fig = go.Figure()
        fig = make_subplots(rows=2, cols=1, subplot_titles=("Mode Usage",
                                                            "Channel Usage",),
                            x_title="Channel",
                            )

        fig.add_bar(x=modestats_rx_df['mode'], y=modestats_rx_df['count'], name="MODE RX", opacity=0.7, textposition="outside", text=modestats_rx_df['count'], row=1, col=1,)
        fig.add_bar(x=modestats_tx_df['mode'], y=modestats_tx_df['count'], name="MODE TX", opacity=0.7, textposition="outside", text=modestats_tx_df['count'], row=1, col=1,)

        fig.add_bar(x=chanstats_rx_df['chan'], y=chanstats_rx_df['count'], name="CHAN RX", opacity=0.7, textposition="outside", text=chanstats_rx_df['count'], row=2, col=1,)
        fig.add_bar(x=chanstats_tx_df['chan'], y=chanstats_tx_df['count'], name="CHAN TX", opacity=0.7, textposition="outside", text=chanstats_tx_df['count'], row=2, col=1,)

        fig.update_layout(
            title="Mode Channel Usage",
            yaxis_title="Count",
            xaxis_title="Modes",
            xaxis={"type": "category"},

        )
    elif GRAPH_OPTION == GRAPH_HIGHCHARTS:

        write_df_to_json('modeRxJson', modestats_rx_df)
        write_df_to_json('chanRxJson', chanstats_rx_df)
        write_df_to_json('modeTxJson', modestats_tx_df)
        write_df_to_json('chanTxJson', chanstats_tx_df)

    # fig.show()
    if not args.quiet:
        print("Done", flush=True, end='\n')


def create_html_file():
    # check if the html file already exists. If yes, no need to create it again
    # print(FILE_HTML)
    # if os.path.isfile(FILE_HTML):
    #     return

    # created using http://minifycode.com/html-minifier/
    if not args.quiet:
        print("\nRendering HTML file ", end='')
        print('file://{}...'.format(os.path.realpath(FILE_HTML)), end='')
    myHtmlStr = '''
    <!DOCTYPE HTML><html><head><meta charset="utf-8"><title>Monitor Trace</title><meta name="description" content="Tool to monitor the DSP Traces"><meta name="author" content="SitePoint"><meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"><link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous"><style>body{font-family:"Roboto",sans-serif}.page{background-color:#F4F7FA}p-0{padding:0 !important}.subtitle{color:orange;font-size:30px}.shadow,hr{box-shadow:0 .5rem 1rem rgba(0, 0, 0, .15) !important}.sticky-top{position:-webkit-sticky;position:sticky;top:0;z-index:1050}.section-padding{}.header{padding-top:10px}.countdownString.float-right{color:#f5deb3;margin-top:5px}.modal-tip{cursor:pointer}.modal-tip:hover{color:orange}#nodeip{font-size:1rem;font-style:italic}.dashboard-counts .count-number{font-size:2em}.chartContainer{min-height:500px}.tab{overflow:hidden;border:1px solid #ccc;background-color:#f1f1f1}.tab button{background-color:inherit;float:left;border:none;outline:none;cursor:pointer;padding:5px 20px;transition:0.3s;font-size:17px;border-right:1px solid #bbb}.tab button:hover{background-color:#ddd}.tab button.active{background-color:#ccc}.tabcontent{display:none;padding:6px 12px;border:1px solid #ccc;border-top:none}.underCLTimings{border:1px solid #eee;margin-bottom:25px}.markerTable{margin-top:12px}.markerTableList{max-height:120px;padding:16px;overflow-y:auto;overflow-x:hidden}.markerTableList .marker{border-radius:1px;max-height:28px;font-size:12px;margin-bottom:5px}.removeMkrBtnClass{font-size:20px;cursor:pointer}.removeMkrBtnClass:hover{color:rgb(174, 0, 0) !important}.highcharts-data-table table tr:nth-child(even){background-color:#f2f2f2}#pills-timings{display:flex !important}.dashboard-counts{color:#333}footer{height:100px}</style></head><body> <nav class="navbar-dark sticky-top bg-dark flex-md-nowrap p-0 shadow"><div class="container-fluid"><div class="row header"><div class="col-sm-6"><h3 class="text-white">Gen5Riva <span class="subtitle">MonitorTrace</span> <span id="nodeip"></span> <i class="fas fa-info-circle modal-tip" data-toggle="modal" data-target="#monitorTraceTips" title="G5R MonitorTrace Tips"></i></h3></div><div class="modal fade" id="monitorTraceTips" tabindex="-1" role="dialog" aria-labelledby="monitorTraceTipsTitle" aria-hidden="true"><div class="modal-dialog modal-dialog-centered" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="exampleModalLongTitle">G5R Monitor Trace Tips Info</h5> <button type="button" class="close" data-dismiss="modal" aria-label="Close"> <span aria-hidden="true">&times;</span> </button></div><div class="modal-body"><ul class="list-group"><li class="list-group-item list-group-item-info"><u><b>For Pie Charts,</b></u> Left Click on the chart to get drilldown.</li><li class="list-group-item list-group-item-info"><u><b>To Zoom In,</b></u> Left Click on a chart and move right or left<br>Left Click on the + button</li><li class="list-group-item list-group-item-info"><u><b>To Zoom Out,</b></u> Left Click on the - button</li><li class="list-group-item list-group-item-info"><u><b>To Pan,</b></u> Ctrl+ Left Click on a chart and move right or left</li><li class="list-group-item list-group-item-info"><u><b>To Reset Zoom/Pan.,</b></u> Left Click on a Reset zoom button on the chart or O button</li><li class="list-group-item list-group-item-info"><u><b>To Add a Marker,</b></u> Shift + Left Click on a chart. Available only in line charts</li><li class="list-group-item list-group-item-info"><u><b>To remove one marker,</b></u> Click on the x on marker in the 'Marker List' table</li><li class="list-group-item list-group-item-info"><u><b>To remove all markers,</b></u> Click on the Remove All Marker in the top</li><li class="list-group-item list-group-item-info"><u><b>To highlight a particular series,</b></u> Hover on the series name in the legend</li><li class="list-group-item list-group-item-info"><u><b>To hide/show a particular series,</b></u> Click on the series name in the legend</li></ul></div><div class="modal-footer"> <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div></div></div></div><div class="col-sm-1"> <span class="countdownString float-right"></span></div><div class=" col-sm-2 "> <button class="btn btn-sm btn-outline-warning float-right" id="removeAllMarkers">Remove all Markers</button></div><div class=" col-sm-3"><div class="input-group mb-3"><div class="input-group-prepend"> <label class="input-group-text" for="refreshIntvDur">Refresh Interval</label></div> <select class="custom-select" id="refreshIntvDur"><option value="0" selected>None</option><option value="5">5</option><option value="10">10</option><option value="15">15</option><option value="30">30</option><option value="45">45</option><option value="60">60</option> </select> <select class="form-control" id="refreshIntUnit"><option value="1">sec</option><option value="60">min</option> </select></div></div></div></div></nav><div id="alertDiv"></div><div class="page"><div class="container-fluid"><section class="dashboard-counts section-padding"><div class="container-fluid"><div class="row"><div class="col-md-3 "><div id="clpietotal" class="pieChartContainer"></div></div><div class="col-md-3 "><div id="clpiedatareqresp" class="pieChartContainer"></div></div><div class="col-md-3 "><div id="clpietxrx" class="pieChartContainer"></div></div><div class="col-md-3 "><div id="clpietxdone" class="pieChartContainer"></div></div></div></div> </section><hr><div class="row"><div class="col-lg-12"><div class="tab"> <button class="tablinks" graphId="rtt" onclick="openGraph(event, 'rttTab')">RTT</button> <button class="tablinks" graphId="mode" onclick="openGraph(event, 'modeTab')">Mode Stats</button> <button class="tablinks" graphId="chan" onclick="openGraph(event, 'chanTab')">Chan Stats</button> <button class="tablinks" graphId="buffer" onclick="openGraph(event, 'bufferTab')">Buffer Mgmt</button> <button class="tablinks" graphId="timeline" id="firstTab" onclick="openGraph(event, 'timelineTab')">Timeline</button> <button class="tablinks" id="" graphId="cltiming" onclick="openGraph(event, 'cltimingTab')">CL Timing Summary</button> <button class="tablinks" id="" graphId="cltimings" onclick="openGraph(event, 'cltimingsTab')">CL Timings</button></div><div id="rttTab" class="tabcontent" style="width: 100%;"><div id="rtt" class="chartContainer"></div><div class="markerTable"> <i class="fas fa-tags"></i> Markers List <sup>(Shift + LeftClick to add Markers.)</sup><div class="row markerTableList" id="markersList-rttTab"></div></div></div><div id="modeTab" class="tabcontent" style="width: 100%;"><div id="mode" class="chartContainer"></div></div><div id="chanTab" class="tabcontent" style="width: 100%;"><div id="chan" class="chartContainer"></div></div><div id="timelineTab" class="tabcontent" style="width: 100%;"><div class="col-sm-4 offset-sm-8 input-group input-group-sm clFilter"><div class="input-group-prepend"> <span class="input-group-text" id="inputGroup-sizing-sm">Filter CL Id</span></div> <input type="text" class="form-control filterInput" aria-label="Start CL ID" aria-describedby="inputGroup-sizing-sm" id="timelineStartClId"><input type="text" class="form-control filterInput" aria-label="Last CL ID" aria-describedby="inputGroup-sizing-sm" id="timelineEndClId"><div class="input-group-append"> <span class="input-group-text totalCls" id="inputGroup-sizing-sm"></span><button class="btn btn-outline-primary filterBtn" type="button" id="timelineFilterBtn">Filter</button> <button class="btn btn-outline-danger filterBtn" type="button" id="timelineResetBtn">Reset</button></div></div><div id="timeline" class="chartContainer"></div><div class="markerTable"> <i class="fas fa-tags"></i> Markers List <sup>(Shift + LeftClick to add Markers.)</sup><div class="row markerTableList" id="markersList-timelineTab"></div></div></div><div id="bufferTab" class="tabcontent" style="width: 100%;"><div id="buffer" class="chartContainer"></div><hr><div id="buffer2" class="chartContainer2"></div><div class="markerTable"> <i class="fas fa-tags"></i> Markers List <sup>(Shift + LeftClick to add Markers.)</sup><div class="row markerTableList" id="markersList-bufferTab"></div></div></div><div id="cltimingTab" class="tabcontent" style="width: 100%;"><div id="cltiming" class="chartContainer"></div><div class="markerTable"> <i class="fas fa-tags"></i> Markers List <sup>(Shift + LeftClick to add Markers.)</sup><div class="row markerTableList" id="markersList-cltimingTab"></div></div></div><div id="cltimingsTab" class="tabcontent" style="width: 100%;"><div id="cltimings" class="row"><div id="txcall2txphr" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="txend2rxstart" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="rxcall2afterrx" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="txcall2aftertx" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="txcall2targettime" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="target2txphr" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="rxend2targettime" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="rxend2txtime" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="rxend2txcall" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div><div id="cl_dur" class="col-md-4 col-sm-6 chartContainer underCLTimings"></div></div></div></div></div></div></div> <script src="https://code.jquery.com/jquery-3.5.1.min.js" 		integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" 		integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" 		crossorigin="anonymous"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" 		integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" 		crossorigin="anonymous"></script> <script src="https://code.highcharts.com/highcharts.js"></script> <script src="https://code.highcharts.com/modules/data.js"></script> <script src="https://code.highcharts.com/modules/boost.js"></script> <script src="https://code.highcharts.com/modules/exporting.js"></script> <script src="https://code.highcharts.com/modules/export-data.js"></script> <script src="https://code.highcharts.com/modules/accessibility.js"></script> <script src="https://code.highcharts.com/highcharts-more.js"></script> <script src="https://code.highcharts.com/modules/dumbbell.js"></script> <script src="https://code.highcharts.com/modules/lollipop.js"></script> <script src="https://code.highcharts.com/modules/annotations.js"></script> <script src="http://code.highcharts.com/modules/drilldown.js"></script> <script type="text/javascript" src="./myJson.js"></script> <script type="text/javascript" >console.log("Monitoring on Node IP ",nodeip);console.log("Monitoring on Node File ",nodefile);console.log("jsonData",jsonData);RTT_CHART_ID='rtt';MODE_CHART_ID='mode';CHAN_CHART_ID='chan';TIMELINE_CHART_ID='timeline';BUFFER_CHART_ID="buffer";CLTIMING_CHART_ID="cltiming";CLTIMINGS_CHART_ID="cltimings";TARGET2TXPHR_CHART_ID="target2txphr";TXEND2RXSTART_CHART_ID="txend2rxstart";RXEND2TARGETTIME_CHART_ID="rxend2targettime";RXEND2TXTIME_CHART_ID="rxend2txtime";TXCALL2TARGETTIME_CHART_ID="txcall2targettime";TXCALL2AFTERTX_CHART_ID="txcall2aftertx";TXCALL2TXPHR_CHART_ID="txcall2txphr";RXEND2TXCALL_CHART_ID="rxend2txcall";RXCALL2AFTERRX_CHART_ID="rxcall2afterrx";CL_DUR_CHART_ID="cl_dur";charts={"rtt":{},"cltiming":{},"cltimings":{},"timeline":{},"buffer":{},'chan':{},'mode':{}};datasets={"rtt":[],"cltiming":[],"cltimings":[],"timeline":[],"buffer":[],'modechan':[],};chartOptions={'rtt':{"chartTitle":"RTT between clData.get and clData.cnf","xAxisType":'linear',"xAxisTitle":"RTT in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},'mode':{"chartTitle":"Mode Usage","xAxisType":'category',"xAxisTitle":"Modes","yAxisTitle":"Count",},'chan':{"chartTitle":"Channel Usage","xAxisType":'category',"xAxisTitle":"Channel","yAxisTitle":"Count",},'buffer':{"chartTitle":"Buffer Stats","xAxisType":'category',"xAxisTitle":"Owner","yAxisTitle":"Count",},'buffer2':{"chartTitle":"Buffer Management","xAxisType":'linear',"xAxisTitle":"Timestamp in usecs","yAxisTitle":"Buffer",},'timeline':{"chartTitle":"Timeline Visualiser","xAxisType":'linear',"xAxisTitle":"Timestamp in usecs","yAxisMax":7,"yAxisMin":-7,},'cltiming':{"chartTitle":"CL Timing Summary Report","xAxisType":'linear',"xAxisTitle":"Timestamp in usecs","yAxisMax":3,"yAxisMin":-3,},"target2txphr":{"chartTitle":"Target Time to TX PHR","xAxisType":'linear',"xAxisTitle":"target2txphr in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"txend2rxstart":{"chartTitle":"txend to RX start Call","xAxisType":'linear',"xAxisTitle":"txend2rxstart in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"rxend2targettime":{"chartTitle":"RX end to Target Tx Time","xAxisType":'linear',"xAxisTitle":"rxend2targettime in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"rxend2txtime":{"chartTitle":"RX end to TX PHR time","xAxisType":'linear',"xAxisTitle":"rxend2txtime in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"txcall2targettime":{"chartTitle":"TX Wrapper call to Target Time","xAxisType":'linear',"xAxisTitle":"txcall2targettime in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"txcall2aftertx":{"chartTitle":"TX Wrapper call to Wrapper Return","xAxisType":'linear',"xAxisTitle":"txcall2afterTx in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"txcall2txphr":{"chartTitle":"TX Wrapper call to Tx PHR","xAxisType":'linear',"xAxisTitle":"txcall2txphr in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"rxend2txcall":{"chartTitle":"RX End to TX Call","xAxisType":'linear',"xAxisTitle":"rxend2txcall in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"rxcall2afterrx":{"chartTitle":"RX CAL duration","xAxisType":'linear',"xAxisTitle":"rxcall2afterrx in usecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},"cl_dur":{"chartTitle":"CL Duration","xAxisType":'linear',"xAxisTitle":"cl_dur in msecs","yAxisTitle":"Count","yAxisTitle2":"PDF/CDF","yAxis2Max":1,},};function drawChart(chartId,tabName,renderFlag){switch(chartId){case RTT_CHART_ID:create_rtt_chart(tabName,renderFlag);break;case MODE_CHART_ID:create_mode_chart(tabName,renderFlag);break;case CHAN_CHART_ID:create_chan_chart(tabName,renderFlag);break;case TIMELINE_CHART_ID:create_timeline_chart(tabName,renderFlag);break;case CLTIMING_CHART_ID:create_cltiming_chart(tabName,renderFlag);break;case CLTIMINGS_CHART_ID:create_cltimings_chart(tabName,renderFlag);break;case BUFFER_CHART_ID:create_buffer_chart(tabName,renderFlag);break;default:alert("Improper chart type "+chartId+" for ");}} function display_alert(type='warning',msg=""){var alertDivStr='<div class="alert alert-'+type+' alert-dismissible fade show" role="alert">'+msg+'<button type = "button" class="close" data-dismiss="alert" aria- label="Close" ><span aria-hidden="true">&times;</span></button ></div>';$('#alertDiv').html(alertDivStr);} var markerCnt=0;function create_marker_line(tabName,markerNum,frt,markerColor,id){var markerListDiv=document.getElementById('markersList'+'-'+tabName);var firstMarkerNum=0;var secondMarkerNum=0;var firstMarkerElem,secondMarkerElem;var firstMarkerVal=0,secondMarkerVal=0;if(markerNum%2!=0){firstMarkerNum=markerNum;secondMarkerNum=markerNum+1;lineHtml=`<div class="marker col-sm-6 "style="border:2px solid ${markerColor}"id="divMarkerVal-${firstMarkerNum}-${secondMarkerNum}"><div class="row"><div class="col-sm-3">M${firstMarkerNum}:<span name="marker1"class="markerVal"id="marker${firstMarkerNum}Val"></span></div><div class="col-sm-3">M${secondMarkerNum}:<span name="marker2"class="markerVal"id="marker${secondMarkerNum}Val"></span></div><div class="col-sm-6">Delta:<span class="deltaVal"id="deltaVal${firstMarkerNum}${secondMarkerNum}"></span><i style="color:${markerColor};"class="fas fa-backspace fs-lg removeMkrBtnClass float-right"id="removeMkrBtn${firstMarkerNum}${secondMarkerNum}"></i></div></div></div>`;markerListDiv.innerHTML=markerListDiv.innerHTML+lineHtml;}else{firstMarkerNum=markerNum-1;secondMarkerNum=markerNum;} firstMarkerElem=document.getElementById(`marker${firstMarkerNum}Val`);secondMarkerElem=document.getElementById(`marker${secondMarkerNum}Val`);if(markerNum%2!=0){firstMarkerVal=parseInt(frt,10);firstMarkerElem.innerHTML=firstMarkerVal;secondMarkerVal=document.getElementById(`marker${secondMarkerNum}Val`).innerHTML;}else{firstMarkerVal=document.getElementById(`marker${firstMarkerNum}Val`).innerHTML;secondMarkerVal=parseInt(frt,10);secondMarkerElem.innerHTML=secondMarkerVal;} if(firstMarkerVal!=0&&secondMarkerVal!=0){var delta=parseInt(secondMarkerVal)-parseInt(firstMarkerVal);var signStr=Math.sign(delta)==-1?"-":"";var deltaElem=document.getElementById(`deltaVal${firstMarkerNum}${secondMarkerNum}`);var deltaSec=0;var deltaMs=0;var deltaUs=0;var deltaStr=delta+' usec (';var deltaMsStr='';var deltaSecStr='';var deltaUsStr=delta+'usec ';var extra=0;delta=Math.abs(delta);if(delta>1000){deltaMs=parseInt(delta/1000,10);deltaUs=delta%1000;deltaMsStr=deltaMs+"ms ";extra=1;} if(deltaMs>1000){deltaSec=parseInt(deltaMs/1000,10);deltaMs=deltaMs%1000;deltaSecStr=deltaSec+" sec ";deltaMsStr=deltaMs+"ms ";} if(deltaUs<=0){deltaUs='';deltaUsStr='';}else{deltaUsStr=deltaUs+"us";} deltaStr=extra?delta+" ( "+deltaSecStr+deltaMsStr+deltaUsStr+" )":delta;deltaElem.innerHTML=signStr+deltaStr;}} var redrawEnabled=true;function create_pie_highchart(id,chartData,dd_data=[],containerDiv='container',annotations_arr=[]){console.log(id,chartData,dd_data);var pie_colors=["#44A9A8","#F7A35C","#90ed7d","#f7a35c","#e4d354","#f45b5b","#91e8e1"];chart=Highcharts.chart(containerDiv,{credits:{enabled:false},plotOptions:{pie:{dataLabels:{enabled:true,distance:-10,inside:true,format:'{point.name} {point.y}',crop:true,overflow:'allow'},colors:pie_colors}},exporting:false,chart:{height:150,backgroundColor:"transparent"},dataLabels:{},title:false,legend:{verticalAlign:'top',},tooltip:{headerFormat:'<span style="font-size:11px">{series.name}</span><br>',pointFormat:'<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}</b>'},series:chartData,drilldown:{series:dd_data,},});} function create_highchart(id,tabName,chartData,containerDiv='container',annotations_arr=[]){console.log(id,tabName,chartData);var zoomRatio=1;chart=Highcharts.chart(containerDiv,{credits:{enabled:false},boost:{useGPUTranslations:true,seriesThreshold:252,useAlpha:false},exporting:{sourceWidth:1920,sourceHeight:920,},chart:{zoomType:'x',panKey:'ctrl',panning:true,events:{load:function(event){const myChart=this;myChart.renderer.button('+',30,10).attr({zIndex:99,}).on('click',function(){var xMin=chart.xAxis[0].getExtremes().min;var xMax=chart.xAxis[0].getExtremes().max;delta=xMax-xMin;chart.xAxis[0].setExtremes(xMin+delta/4,xMax-delta/4);}).add();myChart.renderer.button('-',60,10).attr({zIndex:99,}).on('click',function(){var xMin=chart.xAxis[0].getExtremes().min;var xMax=chart.xAxis[0].getExtremes().max;delta=xMax-xMin;chart.xAxis[0].setExtremes(xMin-delta/2,xMax+delta/2);}).add();myChart.renderer.button('O',90,10).attr({zIndex:99}).on('click',function(){chart.zoomOut();}).add();},redraw:function(event){var extremes=this.xAxis[0].getExtremes();var border=35942400000;var border=60000000;var boostEnabled;var diff=extremes.userMax-extremes.userMin;if(Number.isNaN(diff)) diff=extremes.max-extremes.min;boostEnabled=diff<border?0:1;if(redrawEnabled){redrawEnabled=false;this.update({boost:{enabled:boostEnabled},});redrawEnabled=true;}},click:function(e){if(!e.shiftKey&&!e.ctrlKey)return;let chart=this;let xAxis=chart.xAxis[0];let xValue=xAxis.toValue(this.mouseDownX);let clickX=0;if(markerCnt%2==0) colorCnt=markerCnt%10;else colorCnt=(markerCnt-1)%10;markerColor=Highcharts.getOptions().colors[colorCnt];markerCnt++;create_marker_line(tabName,markerCnt,xValue,markerColor,id);xAxis.addPlotLine({value:xValue,cursor:'pointer',color:markerColor,width:1,label:{rotation:90,text:`M${markerCnt}`,className:"markerLabel markerLabel"+markerCnt},zIndex:99,className:`marker marker${markerCnt}Line`,dashStyle:'ShortDash',events:{mousedown:function(e){chart.clickX=e.pageX;chart.activePlotLine=this;}}});}}},title:{text:chartOptions[id].chartTitle},plotOptions:{area:{marker:{enabled:false,states:{hover:{enabled:false}}},},},legend:{verticalAlign:'top',},tooltip:{shared:true,useHTML:true,followPointer:false,outside:true},xAxis:{title:{text:chartOptions[id].xAxisTitle},type:chartOptions[id].xAxisType,crosshair:{enabled:true,snap:chartOptions[id].xAxisType=='category'?true:false,},},yAxis:[{labels:{enabled:id==TIMELINE_CHART_ID||id==CLTIMING_CHART_ID?false:true,},plotLines:[{value:0,width:1,color:'#999',zIndex:10}],title:{text:chartOptions[id].yAxisTitle,},max:chartOptions[id].yAxisMax?chartOptions[id].yAxisMax:null,min:chartOptions[id].yAxisMin?chartOptions[id].yAxisMin:null,},{title:{text:chartOptions[id].yAxisTitle2?chartOptions[id].yAxisTitle2:null,},max:chartOptions[id].yAxis2Max?chartOptions[id].yAxis2Max:null,opposite:true}],series:chartData,annotations:annotations_arr});charts[id]=chart;} function drawPieChart_cl_newend(){if(!jsonData.clstatsJson.hasOwnProperty('CL_NEW_END'))return;jsonData_clnewend=jsonData.clstatsJson.CL_NEW_END;if(Object.keys(jsonData_clnewend).length==0)return;dd_clouts_data=[];for(const[key,value]of Object.entries(jsonData_clnewend.CL_NEW.drilldown.CL_OUT.drilldown)){dd_clouts_data.push({name:key,y:value});} dd_clends_data=[];for(const[key,value]of Object.entries(jsonData_clnewend.CL_END.drilldown)){dd_clends_data.push({name:key,y:value});} chartData=[{type:"pie",name:"CL",data:[{name:"CL NEW",y:jsonData_clnewend.CL_NEW.val,drilldown:"dd_cl_new",},{name:"CL END",y:jsonData_clnewend.CL_END.val,drilldown:"dd_cl_end"},],},];dd_data=[{name:"CL NEW",type:'pie',id:"dd_cl_new",data:[{name:"CL_OUT",y:jsonData_clnewend.CL_NEW.drilldown.CL_OUT.val,drilldown:'dd_cl_out'},{name:"CL_IN",y:jsonData_clnewend.CL_NEW.drilldown.CL_IN},]},{name:"CL_OUT",type:'pie',id:'dd_cl_out',data:dd_clouts_data},{name:"CL_END",type:'pie',id:'dd_cl_end',data:dd_clends_data}];create_pie_highchart("clpietotal",chartData,dd_data,'clpietotal');} function drawPieChart_cl_data_reqresp(){if(!jsonData.clstatsJson.hasOwnProperty('CL_DATA_REQ_RESP'))return;cl_data_reqresp_stats=jsonData.clstatsJson.CL_DATA_REQ_RESP;if(Object.keys(cl_data_reqresp_stats).length==0)return;dd_cldata_reqresp_data=[];for(const[key,value]of Object.entries(cl_data_reqresp_stats.CL_DATA_RESP.drilldown)){dd_cldata_reqresp_data.push({name:key,y:value});} chartData=[{type:"pie",name:"CL DATA",colorByPoint:true,data:[{name:"DATAREQ",y:cl_data_reqresp_stats.CL_DATA_REQ.val,},{name:"DATARESP",y:cl_data_reqresp_stats.CL_DATA_RESP.val,drilldown:"dd_cl_data_resp"},],},];dd_data=[{name:"DATARESP",type:'pie',id:"dd_cl_data_resp",data:dd_cldata_reqresp_data}];create_pie_highchart("clpiedatareqresp",chartData,dd_data,'clpiedatareqresp');} function drawPieChart_cl_tx_rx(){if(!jsonData.clstatsJson.hasOwnProperty('CL_TX_RX'))return;jsonData_cltxrx=jsonData.clstatsJson.CL_TX_RX;if(Object.keys(jsonData_cltxrx).length==0)return;dd_cltx_data=[];for(const[key,value]of Object.entries(jsonData_cltxrx.CL_TX.drilldown)){dd_cltx_data.push({name:key,y:value});} dd_clrx_data=[];for(const[key,value]of Object.entries(jsonData_cltxrx.CL_RX.drilldown)){dd_clrx_data.push({name:key,y:value});} chartData=[{type:"pie",name:"CL TX RX",colorByPoint:true,data:[{name:"TX",y:jsonData_cltxrx.CL_TX.val,drilldown:"dd_cl_tx"},{name:"RX",y:jsonData_cltxrx.CL_RX.val,drilldown:"dd_cl_rx"},],},];dd_data=[{name:"TX",type:'pie',id:"dd_cl_tx",data:dd_cltx_data},{name:"RX",type:'pie',id:"dd_cl_rx",data:dd_clrx_data}];create_pie_highchart("clpietxrx",chartData,dd_data,'clpietxrx');} function drawPieChart_cl_txdone(){if(!jsonData.clstatsJson.hasOwnProperty('CL_TXDONE'))return;jsonData_cltxdone=jsonData.clstatsJson.CL_TXDONE;if(Object.keys(jsonData_cltxdone).length==0)return;dd_cltx_done=[];for(const[key,value]of Object.entries(jsonData_cltxdone.drilldown)){dd_cltx_done.push({name:key,y:value});} chartData=[{type:"pie",name:"CL TXDONE",colorByPoint:true,data:[{name:"TXDONE",y:jsonData_cltxdone.val,drilldown:"dd_cl_txdone"},],},];dd_data=[{name:"TX",type:'pie',id:"dd_cl_txdone",data:dd_cltx_done}];create_pie_highchart("clpietxdone",chartData,dd_data,'clpietxdone');} function drawPieChart(){if(!jsonData.hasOwnProperty('clstatsJson'))return;clstats=jsonData.clstatsJson;console.log('clstats ',clstats);drawPieChart_cl_newend();drawPieChart_cl_data_reqresp();drawPieChart_cl_tx_rx();drawPieChart_cl_txdone();} function create_rtt_chart(tabName,renderFlag){if(!jsonData.hasOwnProperty('rttJson'))return;console.log('creating RTT');let freqData=[];let pdfData=[];let cdfData=[];let x_data=[];jsonData.rttJson.forEach(item=>{freqData.push({x:item.diff,y:item.freq});pdfData.push({x:item.diff,y:item.pdf});cdfData.push({x:item.diff,y:item.cdf});});chartData=[{type:"column",name:"Freq",data:freqData,color:Highcharts.getOptions().colors[0]},{type:"line",name:"PDF",yAxis:1,data:pdfData,color:Highcharts.getOptions().colors[3]},{type:"line",name:"CDF",yAxis:1,data:cdfData,color:Highcharts.getOptions().colors[2]},];create_highchart(RTT_CHART_ID,tabName,chartData,RTT_CHART_ID);return;} function create_mode_chart(tabName,renderFlag){if(!jsonData.hasOwnProperty('modeTxJson'))return;console.log('creating modechanchart');let modeRxData=[];let modeTxData=[];jsonData.modeRxJson.forEach(item=>{;modeRxData.push({name:item.mode,y:item.count})});jsonData.modeTxJson.forEach(item=>{modeTxData.push({name:item.mode,y:item.count});});chartData=[{type:"column",name:"ModeRx",data:modeRxData,dataLabels:{enabled:true,},color:Highcharts.getOptions().colors[7]},{type:"column",name:"ModeTx",data:modeTxData,dataLabels:{enabled:true,},color:Highcharts.getOptions().colors[3]},];create_highchart(MODE_CHART_ID,tabName,chartData,MODE_CHART_ID);} function create_chan_chart(tabName,renderFlag){if(!jsonData.hasOwnProperty('chanTxJson'))return;console.log('creating chanchanchart');let chanRxData=[];let chanTxData=[];jsonData.chanRxJson.forEach(item=>{chanRxData.push({name:item.chan,y:item.count});});chanRxData.sort(function(a,b){return a.name-b.name;});jsonData.chanTxJson.forEach(item=>{chanTxData.push({name:item.chan,y:item.count});});chanTxData.sort(function(a,b){return a.name-b.name;});chartData=[{type:"column",name:"Chan Rx",data:chanRxData,dataLabels:{enabled:true,},color:Highcharts.getOptions().colors[7],},{type:"column",name:"Chan Tx",data:chanTxData,dataLabels:{enabled:true,},color:Highcharts.getOptions().colors[3],},];create_highchart(CHAN_CHART_ID,tabName,chartData,CHAN_CHART_ID);} function create_buffer_chart(tabName,renderFlag){if(!jsonData.hasOwnProperty('buffer_Json'))return;console.log('creating buffer summary chart');let bufClaimData=[];let bufRelData=[];let bufLeakData=[];let chartData=[];jsonData.buffer_summaryJson.forEach(item=>{bufClaimData.push({name:item.owner,y:item.buf_claim});bufRelData.push({name:item.owner,y:item.buf_release});bufLeakData.push({name:item.owner,y:item.buf_leak});});chartData=[{type:"column",name:"Buff Claim",dataLabels:{enabled:true,color:Highcharts.getOptions().colors[7]},data:bufClaimData,color:Highcharts.getOptions().colors[7]},{type:"column",name:"Buff release",dataLabels:{enabled:true,color:Highcharts.getOptions().colors[3]},data:bufRelData,color:Highcharts.getOptions().colors[3]},{type:"column",name:"Buff Leaks",dataLabels:{enabled:true,color:Highcharts.getOptions().colors[5]},data:bufLeakData,color:Highcharts.getOptions().colors[5]},];create_highchart(BUFFER_CHART_ID,tabName,chartData,BUFFER_CHART_ID);console.log('creating buffer alloc');chartData=[];buf_colors={'CL':'#ff0000','FH':'#00ff00','RXBCON':'#0000ff','ALINK':'#009999','MACMGR':'#003f5c',"LMMGR":"#444e86","TXBCON":"#955196","SA":"#dd5182","ELG":"#ff6e54","TXBCAST":"#ffa600",};if(!jsonData.hasOwnProperty('buffer_Json')){return;} jsonData.buffer_Json.forEach(item=>{chartData.push({type:'area',findNearestPointBy:'xy',data:[[item.frt_dec,0],[item.frt_dec,item.buffer_dec],{x:item.frt_dec+item.frt_diff/2.0,y:item.buffer_dec,},[item.rel_frt,item.buffer_dec],[item.rel_frt,0],],states:{inactive:{opacity:0.6}},zIndex:5,name:item.owner,showInLegend:false,color:buf_colors[item.owner],lineWidth:0.25,fillOpacity:0.1,tooltip:{useHTML:true,headerFormat:'<span style="color: {series.color}">{series.name} </span>: 0x'+item.buffer_dec.toString(16),pointFormat:'<br><span>claimedFRT: '+item.frt_dec+'</span><br> releasedFRT:'+item.rel_frt+'<br>Dur: '+item.frt_diff+" usec"},})});create_highchart(BUFFER_CHART_ID+"2",tabName,chartData,BUFFER_CHART_ID+"2");} function create_cltimings_chart(tabName,renderFlag){let freqData=[];let pdfData=[];let cdfData=[];let chartData=[];console.log('creating cltimings');for(const[key,value]of Object.entries(jsonData)){freqData=[];pdfData=[];cdfData=[];chartData=[];let id='';if(!key.startsWith('cltimings_')) continue;id=key.slice(10,-4);jsonData[key].forEach(item=>{freqData.push({x:item[id],y:item.freq});pdfData.push({x:item[id],y:item.pdf});cdfData.push({x:item[id],y:item.cdf});});chartData=[{type:"column",name:"Freq",data:freqData,color:Highcharts.getOptions().colors[0]},{type:"line",name:"PDF",yAxis:1,data:pdfData,color:Highcharts.getOptions().colors[3]},{type:"line",name:"CDF",yAxis:1,data:cdfData,color:Highcharts.getOptions().colors[2]},];create_highchart(id,tabName,chartData,id);}} function create_cltiming_chart(tabName,renderFlag){if(!jsonData.hasOwnProperty('cltimingJson'))return;console.log("cltiming",jsonData.cltimingJson);let chartData=[];tx_dur=2000;points_dic=jsonData.cltimingJson.points_dic;rx_dur=points_dic['rxEnd']-(points_dic['rxPHR']);txdiff=points_dic['TxPHR1']-points_dic['TargetTx1'];chartData.push({type:'area',findNearestPointBy:'xy',data:[[points_dic.TxPHR1,0],[points_dic.TxPHR1,0.5],{x:points_dic.TxPHR1+tx_dur/2,y:0.5,dataLabels:{enabled:true,format:"Transmission e.g. POLL",}},[points_dic.TxPHR1+tx_dur,0.5],[points_dic.TxPHR1+tx_dur,0],],enableMouseTracking:false,zIndex:5,states:{inactive:{opacity:1}},name:"POLL",showInLegend:false,color:'#E9967A',lineWidth:2,fillOpacity:0.6,tooltip:{enabled:false},},{type:'area',findNearestPointBy:'xy',data:[[points_dic.rxPHR,0],[points_dic.rxPHR,-0.5],{x:points_dic.rxPHR+rx_dur/2,y:-0.5,dataLabels:{enabled:true,format:"Reception e.g. ACK",verticalAlign:'top'}},[points_dic.rxPHR+rx_dur,-0.5],[points_dic.rxPHR+rx_dur,0],],name:"ACK",enableMouseTracking:false,zIndex:5,states:{inactive:{opacity:1}},showInLegend:false,color:'#8FBC8F',lineWidth:2,fillOpacity:0.6,tooltip:{enabled:false},},{type:'area',findNearestPointBy:'xy',data:[[points_dic.TxPHR2,0],[points_dic.TxPHR2,0.5],{x:points_dic.TxPHR2+(tx_dur+500)/2,y:0.5,dataLabels:{enabled:true,format:"Transmission e.g. DATA",}},[points_dic.TxPHR2+tx_dur+500,0.5],[points_dic.TxPHR2+tx_dur+500,0],],enableMouseTracking:false,zIndex:5,states:{inactive:{opacity:1}},name:"Data",showInLegend:false,color:'#E9967A',lineWidth:2,fillOpacity:0.6,tooltip:{enabled:false},});let lollipopData=[];let annotations=[];value_levels={"WrapperCall1":-2,"WrapperReturn":2,"TargetTx1":-2,"TxPHR1":-2,"EndTxTime":-2,"rxStart_beforeCall":2,"rxStart_afterCall":2,"rxPHR":2,"rxEnd":-2,"WrapperCall2":2,"TargetTx2":-2,"TxPHR2":-2,};cnt=0;for(const[key,value]of Object.entries(jsonData.cltimingJson.points_dic)){lollipopData.push({x:value,y:jsonData.cltimingJson.levels_dic[key],color:jsonData.cltimingJson.colors_dic[key],id:key,name:jsonData.cltimingJson.names_label_dic[key],});annotations.push({labelOptions:{backgroundColor:'rgba(255,255,0,0.3)',verticalAlign:jsonData.cltimingJson.levels_dic[key]<0?'top':'bottom',distance:10,},labels:[{point:key,text:jsonData.cltimingJson.names_label_dic[key]}]});annotations.push({draggable:'',shapes:[{fill:'none',stroke:'red',strokeWidth:1,dashStyle:'LongDash',type:'path',points:[{x:jsonData.cltimingJson.arrows_x[cnt].x1,y:jsonData.cltimingJson.arrows_x[cnt].y,xAxis:0,yAxis:0},{x:jsonData.cltimingJson.arrows_x[cnt].x2,y:jsonData.cltimingJson.arrows_x[cnt].y,xAxis:0,yAxis:0}],}],labelOptions:{backgroundColor:'rgba(255,255,255,0.4)',borderColor:'rgba(0,0,0,0)',style:{color:"black",},verticalAlign:value_levels[key]<0?'bottom':'top',y:value_levels[key],},labels:[{point:{x:(jsonData.cltimingJson.arrows_x[cnt].x1+jsonData.cltimingJson.arrows_x[cnt].x2)/2,y:jsonData.cltimingJson.arrows_x[cnt].y,xAxis:0,yAxis:0},text:jsonData.cltimingJson.val_texts[cnt],allowOverlap:true,padding:2}]});cnt++;} annotations.push({labelOptions:{backgroundColor:'rgba(0,0,0,0.8)',},labels:[{point:{x:150,y:0,},text:"min/max/avg"}]});chartData.push({type:'lollipop',findNearestPointBy:'xy',data:lollipopData,zIndex:7,states:{inactive:{opacity:1}},showInLegend:false,connectorWidth:2,fillOpacity:0.6,toolTip:{enabled:false},enableMouseTracking:false,});create_highchart(CLTIMING_CHART_ID,tabName,chartData,CLTIMING_CHART_ID,annotations_arr=annotations);} function create_timeline_chart(tabName,renderFlag){if(!jsonData.hasOwnProperty('timeline_clStartEndJson'))return;console.log('creating timeline chart');let chartData=[];let dataPoints=[];new_timeline_txJson=jsonData.timeline_txJson.filter((item)=>{return((parseInt(item.cl_id)>=new_start_cl_id)&&((parseInt(item.cl_id)<=new_end_cl_id)));});new_timeline_rxJson=jsonData.timeline_rxJson.filter((item)=>{return((parseInt(item.cl_id)>=new_start_cl_id)&&(parseInt(item.cl_id)<=new_end_cl_id));});new_timeline_clStartEndJson=jsonData.timeline_clStartEndJson.filter((item)=>{return((parseInt(item.cl_id)>=new_start_cl_id)&&(parseInt(item.cl_id)<=new_end_cl_id));});new_timeline_phyIndJson=jsonData.timeline_phyIndJson.filter((item)=>{return((parseInt(item.cl_id)>=new_start_cl_id)&&(parseInt(item.cl_id)<=new_end_cl_id));});new_timeline_clTracesJson=jsonData.timeline_clTracesJson.filter((item)=>{return((parseInt(item.cl_id)>=new_start_cl_id)&&(parseInt(item.cl_id)<=new_end_cl_id));});new_timeline_txJson.forEach(item=>{chartData.push({type:'area',findNearestPointBy:'xy',data:[[item.ts_txstart,0],[item.ts_txstart,1],{x:item.ts_txstart+item.tx_dur/2.0,y:1,},[item.ts_txend,1],[item.ts_txend,0],],states:{inactive:{opacity:0.8}},zIndex:5,name:"TX",showInLegend:false,color:item.color,tooltip:{split:true,useHTML:true,headerFormat:'<span style="color: {series.color}">{series.name}</span>: ',pointFormat:'<span>FRT: {point.x}</span><br>'+item.hoverinfo},turboThreshold:0,})});new_timeline_rxJson.forEach(item=>{chartData.push({type:'area',findNearestPointBy:'xy',data:[[item.ts_rxstart,0],[item.ts_rxstart,-1],{x:item.ts_rxstart+item.rx_dur/2.0,y:-1,toolTip:false},[item.ts_rxend,-1],[item.ts_rxend,0]],turboThreshold:0,states:{inactive:{opacity:0.8}},showInLegend:false,zIndex:5,name:"RX",color:item.color,tooltip:{useHTML:true,headerFormat:'<span style="color: {series.color}">{series.name}</span>: ',pointFormat:'<span>FRT: {point.x}</span><br>'+item.hoverinfo},})});new_timeline_clStartEndJson.forEach(item=>{chartData.push({type:'area',data:[[item.clstart,0],[item.clstart,3],{x:item.clstart+item.cldiff/2.0,y:3,dataLabels:{enabled:true,format:item.hoverinfo}},[item.clend,3],[item.clend,-3],[item.clstart,-3],[item.clstart,0],],states:{inactive:{opacity:0.8}},zIndex:1,showInLegend:false,grouping:true,name:"CL "+item.cl_id,fillColor:'rgba(247, 228, 194,0.35)',color:"rgba(247, 228, 194,1)",turboThreshold:0,tooltip:{useHTML:true,headerFormat:'<span style="color: rgba(170, 135, 54,1)">{series.name}</span>: ',pointFormat:'<span>FRT: {point.x}</span> '+item.hoverinfo},})});dataPoints=[];dataPoints=new_timeline_phyIndJson.map((item)=>{if(!Number(item.frt_dec)){console.log("Error..",item);} return{x:item.frt_dec,y:-6,color:item.color,info:item.trace_info};});chartData.push({type:"scatter",findNearestPointBy:'xy',name:"phyData Indications",showInLegend:true,states:{inactive:{opacity:0.8}},visible:false,data:dataPoints,tooltip:{headerFormat:'<span style="font-size:10px">FRT: {point.key}</span><table>',pointFormat:'<tr><td style="color:{series.color};padding:0">{point.info} </td></tr>',footerFormat:'</table>',useHTML:true,followPointer:false,},marker:{symbol:"triangle"},turboThreshold:0,});dataPoints=[];dataPoints=new_timeline_clTracesJson.map((item)=>{return{x:item.frt_dec,y:6,color:item.color,info:item.trace_info,clid:item.cl_id};});chartData.push({type:"scatter",findNearestPointBy:'xy',name:"CL Traces",showInLegend:true,states:{inactive:{opacity:0.8}},marker:{symbol:"triangle-down"},color:"red",visible:false,data:dataPoints,tooltip:{headerFormat:'<span style="font-size:10px">FRT: {point.key}, CL id {point.clid}</span><table>',pointFormat:'<tr><td style="color:{series.color};padding:0">{point.info} </td></tr>',footerFormat:'</table>',useHTML:true,followPointer:false,},turboThreshold:0,});create_highchart(TIMELINE_CHART_ID,tabName,chartData,TIMELINE_CHART_ID);} function openGraph(evt,tabName){var i,tabcontent,tablinks;tabcontent=document.getElementsByClassName("tabcontent");for(i=0;i<tabcontent.length;i++){tabcontent[i].style.display="none";} tablinks=document.getElementsByClassName("tablinks");for(i=0;i<tablinks.length;i++){tablinks[i].className=tablinks[i].className.replace(" active","");} document.getElementById(tabName).style.display="block";evt.currentTarget.className+=" active";graphId=evt.currentTarget.attributes.graphId.value;if(Object.keys(charts[graphId]).length==0) drawChart(graphId,tabName,true);} function init_timeline_cl_filter(){if(!jsonData.hasOwnProperty('timeline_clStartEndJson'))return;orig_start_cl_id=Math.min(parseInt(jsonData.timeline_txJson[0].cl_id),parseInt(jsonData.timeline_rxJson[0].cl_id));orig_end_cl_id=Math.max(jsonData.timeline_txJson[jsonData.timeline_txJson.length-1].cl_id,jsonData.timeline_rxJson[jsonData.timeline_rxJson.length-1].cl_id);$('#timelineStartClId').val(orig_start_cl_id);$('#timelineEndClId').val(orig_end_cl_id);old_start_cl_id=orig_start_cl_id;old_end_cl_id=orig_end_cl_id;new_start_cl_id=orig_start_cl_id;new_end_cl_id=orig_end_cl_id;$('.clFilter .totalCls').html((new_end_cl_id-new_start_cl_id+1)+" CL(s)");console.log("total CLs",new_end_cl_id-new_start_cl_id);console.log("Filter init ",{new_start_cl_id,new_end_cl_id});} var new_start_cl_id=0;var new_end_cl_id=0;var old_start_cl_id=0;var old_end_cl_id=0;var orig_start_cl_id=0;var orig_end_cl_id=0;var diff=0;function prepare_timeline_cl_filter(evt=false){if(evt.target.id=="timelineResetBtn"){new_start_cl_id=Math.min(parseInt(jsonData.timeline_txJson[0].cl_id),parseInt(jsonData.timeline_rxJson[0].cl_id));new_end_cl_id=Math.max(jsonData.timeline_txJson[jsonData.timeline_txJson.length-1].cl_id,jsonData.timeline_rxJson[jsonData.timeline_rxJson.length-1].cl_id);$('#timelineStartClId').val(new_start_cl_id);$('#timelineEndClId').val(new_end_cl_id);$(".alert").alert('close');}else{new_start_cl_id=parseInt($('#timelineStartClId').val());new_end_cl_id=parseInt($('#timelineEndClId').val());} if(new_start_cl_id<orig_start_cl_id||new_start_cl_id>orig_end_cl_id){display_alert('warning',`<b>Start CL Id ${new_start_cl_id}&nbsp;is out of range[${orig_start_cl_id},${orig_end_cl_id}].</b>Resetting to the min possible value.`);new_start_cl_id=orig_start_cl_id;$('#timelineStartClId').val(new_start_cl_id);} if(new_end_cl_id>orig_end_cl_id||new_end_cl_id<orig_start_cl_id){display_alert('warning',`<b>End CL Id ${new_end_cl_id}&nbsp;is out of range[${orig_start_cl_id},${orig_end_cl_id}].</b>Resetting to the max possible value.`);new_end_cl_id=orig_end_cl_id;$('#timelineEndClId').val(new_end_cl_id);} if(new_start_cl_id==old_start_cl_id&&new_end_cl_id==old_end_cl_id)return;diff=new_end_cl_id-new_start_cl_id;if(diff<0){display_alert('warning',`<b>End CL id ${new_end_cl_id}&nbsp;>Start CL id ${new_start_cl_id}</b>.Resetting to the range[${orig_start_cl_id},${orig_end_cl_id}]`);new_start_cl_id=orig_start_cl_id;new_end_cl_id=orig_end_cl_id;$('#timelineStartClId').val(new_start_cl_id);$('#timelineEndClId').val(new_end_cl_id);} $('.clFilter .totalCls').html((new_end_cl_id-new_start_cl_id+1)+" CL(s)");drawChart(TIMELINE_CHART_ID,"timelineTab",true);old_start_cl_id=new_start_cl_id;old_end_cl_id=new_end_cl_id;} window.onload=function(){if(nodeip!='None'||nodeip.length!=4){$('#nodeip').html(nodeip);}else if(nodefile!='None'){$('#nodeip').html(nodefile);} drawPieChart();init_timeline_cl_filter();$(document).on("click",".filterBtn",prepare_timeline_cl_filter);$('.filterInput').keypress(function(event){var keycode=(event.keyCode?event.keyCode:event.which);if(keycode=='13'){prepare_timeline_cl_filter(event);}});document.getElementById("firstTab").click();$(document).on("click",".removeMkrBtnClass",function(event){parentRow=$(this).parent().parent().parent();id=parentRow.attr('id').split('-');$(`.marker${id[1]}Line`).remove();$(`.marker${id[2]}Line`).remove();$(`.markerLabel${id[1]}`).remove();$(`.markerLabel${id[2]}`).remove();parentRow.remove();});$(document).on("click","#removeAllMarkers",function(event){$('.marker').remove();$('.markerLabel').remove();markerCnt=0;});refreshIntv=$('#refreshIntvDur').val()*$('#refreshIntUnit').val()*1000;var seconds=refreshIntv/1000;var secondTimer;console.log("refreshIntv",refreshIntv);if(refreshIntv>0){refreshTimer=setTimeout(function(){location.reload();},refreshIntv);secondTimer=setInterval(function(){$('.countdownString').html(`<i class="fas fa-sync"></i>&nbsp;in ${seconds--}...`);},1000);} $(document).on("change","#refreshIntvDur,#refreshIntUnit",function(event){refreshIntv=$('#refreshIntvDur').val()*$('#refreshIntUnit').val()*1000;seconds=refreshIntv/1000;if(typeof refreshTimer!=='undefined')clearTimeout(refreshTimer);if(secondTimer)clearInterval(secondTimer);if(refreshIntv>0){refreshTimer=setTimeout(function(){location.reload();},refreshIntv);secondTimer=setInterval(function(){$('.countdownString').html(`<i class="fas fa-sync"></i>&nbsp;in ${seconds--}...`);},1000);}else{$('.countdownString').html('');}});}</script> </body></html>
    '''
    with open(FILE_HTML, 'w') as f:
        f.write(myHtmlStr)
    if not args.quiet:
        print("Ok")


def graph_it():

    if not os.path.isfile(graph_file):
        print("{} not found. Use -c option to create the required csv.".format(graph_file))
        return

    packages = []
    packages.append("pandas")
    if GRAPH_OPTION == GRAPH_PLOTLY:
        packages.append("plotly==4.9.0")

    check_and_install_package(packages)

    try:
        import pandas as pd
        import numpy as np
        global pd
        global np
        # import mplcursors
        # import matplotlib.pyplot as plt
        if GRAPH_OPTION == GRAPH_PLOTLY:
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            import plotly.offline as py
            global px
            global go
            global make_subplots
            global py

    except:
        print("Error while installing packages")
        # import matplotlib.pyplot as plt

    # plt.style.use('seaborn-deep')
    # plt.style.use('ggplot')
    if not args.quiet:
        if(args.range):
            print("showing graph {} CLs {} from '{}'".format(graph_ans_list, cl_id_range, graph_file))
        else:
            print("showing graph {} from '{}'".format(graph_ans_list, graph_file))

    # plt.show()
    global csv_df
    global cl_csv_df
    global timings_df

    csv_df = pd.read_csv(sep=',', skiprows=1, names=['byte', "frt_dec", 'frt_hex', 'trace_code', 'trace_info'], filepath_or_buffer=graph_file)
    # csv_df[['tracecode_dec','tracecode_hex']] = df.Name.str.split(expand=True)
    csv_df = csv_df.assign(tracecode_dec=pd.Series(np.nan))
    csv_df = csv_df.assign(tracecode_hex=pd.Series(np.nan))

    csv_df[['tracecode_dec', 'tracecode_hex']
           ] = csv_df['trace_code'].str.split(expand=True)
    csv_df.drop(columns=['trace_code'], inplace=True)
    csv_df = csv_df.astype({'tracecode_dec': int})
    # csv_df = csv_df.assign(cl_id=pd.Series(np.nan))

    # csv_df['cl_id'] = csv_df["trace_info"].apply(lambda x: x.split(' ', 5)[4] if "CL_OUT_CNF" in x or "CL_START" in x else np.nan)
    cl_id_df = csv_df[(csv_df.tracecode_dec == 134) | (csv_df.tracecode_dec == 136)][['byte', 'trace_info']]
    if cl_id_df.empty:
        csv_df = csv_df.assign(cl_id=pd.Series(np.nan))
    else:
        cl_id_df.rename(columns={'trace_info': 'cl_id'}, inplace=True)
        cl_id_df.cl_id = cl_id_df.cl_id.str.rsplit(' ', 1, expand=True).drop([0], axis=1)
        csv_df = csv_df.merge(cl_id_df, on='byte', how='left')

    # csv_df['cl_mac'] = csv_df.apply(lambda x: x.trace_info.split('>', 2)[1].strip() if x.tracecode_dec == 147 else np.nan, axis=1)
    cl_mac_df = csv_df[csv_df.tracecode_dec == 147][['byte', 'trace_info']]
    if cl_mac_df.empty:
        csv_df = csv_df.assign(cl_mac=pd.Series(np.nan))
    else:
        cl_mac_df.rename(columns={'trace_info': 'cl_mac'}, inplace=True)
        cl_mac_df.cl_mac = cl_mac_df.cl_mac.str.split('>', 2, expand=True).drop([0], axis=1)
        csv_df = csv_df.merge(cl_mac_df, on='byte', how='left')

    # csv_df['txrx_param'] = csv_df.apply(lambda x: x.trace_info.split(')', 2)[1].strip() if x.tracecode_dec == 140 else np.nan, axis=1)
    tx_param = csv_df[csv_df.tracecode_dec == 140][['byte', 'trace_info']]
    rx_param = csv_df[csv_df.tracecode_dec == 141][['byte', 'trace_info']]
    txrx_param_df = pd.concat([tx_param, rx_param]).sort_values(by=['byte']).rename(columns={'trace_info': 'txrx_param'})
    if txrx_param_df.empty:
        csv_df = csv_df.assign(txrx_param=pd.Series(np.nan))
    else:
        txrx_param_df.txrx_param = txrx_param_df.txrx_param.str.split(')', 2, expand=True).drop([0], axis=1)
        csv_df = csv_df.merge(txrx_param_df, on='byte', how='left')

    traceCodeMap_df = pd.DataFrame(tracing_events_num_str.items(), columns=['tracecode_dec', 'trace_str'])

    # add owner id
    owner_df = csv_df[csv_df.tracecode_dec == 68][['byte', 'trace_info']].rename(columns={'trace_info': 'owner'})
    if owner_df.empty:
        csv_df = csv_df.assign(owner=pd.Series(np.nan))
    else:
        owner_df.owner = owner_df.owner.str.split('LMSM_', 2, expand=True).drop([0], axis=1)
        owner_df.owner = owner_df.owner.str.split('(', 2, expand=True).drop([1], axis=1)
        csv_df = csv_df.merge(owner_df, on='byte', how='left')
        csv_df = csv_df.ffill()

    # filter for clId Ranges
    max_cl_val = str(int(csv_df.cl_id.astype(float).max())) if not math.isnan(csv_df.cl_id.astype(float).max()) else "0"
    min_cl_val = str(int(csv_df.cl_id.astype(float).min())) if not math.isnan(csv_df.cl_id.astype(float).min()) else "0"

    if args.range:
        cl_range_start, cl_range_end = cl_id_range.split(':')
        cl_range_start = int(cl_range_start)-1 if cl_range_start else 0
        cl_range_end = min(int(cl_range_end), int(max_cl_val)) if cl_range_end else max_cl_val
        csv_df = csv_df[(csv_df.cl_id.astype(float) >= float(cl_range_start)) & (csv_df.cl_id.astype(float) <= float(cl_range_end))]

    # seq contrl
    tx_seq_ctrl_df = csv_df[(csv_df.tracecode_dec == 144) & (csv_df.trace_info.str.contains("TX"))][['byte', 'trace_info']].rename(columns={'trace_info': 'tx_seq_ctrl'})
    rx_seq_ctrl_df = csv_df[(csv_df.tracecode_dec == 144) & (csv_df.trace_info.str.contains("RX"))][['byte', 'trace_info']].rename(columns={'trace_info': 'rx_seq_ctrl'})

    if not tx_seq_ctrl_df.empty:
        tx_seq_ctrl_df.tx_seq_ctrl = tx_seq_ctrl_df.tx_seq_ctrl.str.strip().str.split('SeqNum', 2, expand=True).drop([0], axis=1)
    if not rx_seq_ctrl_df.empty:
        rx_seq_ctrl_df.rx_seq_ctrl = rx_seq_ctrl_df.rx_seq_ctrl.str.strip().str.split('SeqNum', 2, expand=True).drop([0], axis=1)

    csv_df = csv_df.merge(tx_seq_ctrl_df, on='byte', how='left')
    csv_df = csv_df.merge(rx_seq_ctrl_df, on='byte', how='left')

    csv_df.tx_seq_ctrl = np.where((csv_df.tracecode_dec == tracing_events_str_num['CL_TX']), 'X', csv_df.tx_seq_ctrl)
    csv_df.rx_seq_ctrl = np.where((csv_df.tracecode_dec == tracing_events_str_num['CL_RX']), 'X', csv_df.rx_seq_ctrl)

    csv_df = csv_df.bfill()

    # FRT_trace_val
    # csv_df['frt32_val'] = csv_df.apply(lambda x: (x.trace_info[-8:]) if x.tracecode_dec in [6, 121, 122, 123, 124, 129, 130] else np.nan, axis=1)
    frt32_val_df = csv_df[csv_df.tracecode_dec.isin([6, 121, 122, 123, 124, 129, 130])][['byte', 'trace_info']]
    frt32_val_df.trace_info = frt32_val_df.trace_info.str[-8:]
    frt32_val_df.rename(columns={'trace_info': 'frt32_val'}, inplace=True)
    csv_df = csv_df.merge(frt32_val_df, on='byte', how='left')

    csv_df['dummy'] = csv_df.tracecode_dec.shift(1)
    csv_df['dummy_frt'] = csv_df.frt32_val.shift(-1)
    csv_df['dup'] = np.where((csv_df.tracecode_dec == csv_df.dummy), 1, 0)

    csv_df['frt_val'] = csv_df.dummy_frt + csv_df.frt32_val
    csv_df['frt_val'] = csv_df.frt_val.apply(lambda x: int(x, 16) if type(x) == str else np.nan)

    # csv_df.frt_val = csv_df.frt_val.apply(lambda x: "hello" if x!=np.nan else np.nan)
    csv_df = csv_df[csv_df.dup == 0]
    csv_df.drop(columns=['frt32_val', 'dummy', 'dummy_frt', 'dup'], inplace=True)

    # stat_total = csv_df.groupby('tracecode_dec').count().reset_index().astype({"tracecode_dec": int})
    # stat_total = stat_total[['tracecode_dec', 'byte']]
    # stat_total = stat_total.merge(traceCodeMap_df, how='inner', on="tracecode_dec").sort_values(by=['tracecode_dec']).reset_index()
    cl_filter_list = list(range(121, 152))
    cl_filter_list.extend(list(range(0, 7)))
    cl_filter_list.extend(list(range(113, 119)))
    # print(cl_filter_list)
    # exit(0)
    cl_csv_df = pd.DataFrame()
    cl_csv_df = csv_df[csv_df.tracecode_dec.isin(cl_filter_list)]
    # cl_csv_df = csv_df.loc[(csv_df['tracecode_dec'] > 120) & (csv_df['tracecode_dec'] <= 151) | (csv_df.tracecode_dec <= 6)]
    cl_csv_df = cl_csv_df.drop(columns=['tracecode_hex'])

    # cl_csv_df = cl_csv_df.assign(sts=pd.Series(np.nan))
    cl_csv_df['sts'] = cl_csv_df.trace_info.apply(lambda x: "" if ("STS" not in x) and ("SDU_" not in x) else x.split()[1].split('(')[0])
    cl_csv_df = cl_csv_df.merge(traceCodeMap_df, on="tracecode_dec")
    cl_csv_df.sort_values(by=['byte'], inplace=True)

    cl_stats = cl_csv_df.groupby(
        ['trace_str', 'sts', ]).count()
    cl_stats = cl_stats['byte']

    if not args.quiet:
        print("="*30)
        print("Total CLs    : {} [{},{}]".format(int(max_cl_val, 10)-int(min_cl_val, 10), int(min_cl_val, 10), int(max_cl_val, 10)))
        if args.range:
            print("Filtered CLs : {} [{},{}]".format(cl_range_end - cl_range_start, cl_range_start, cl_range_end))
        print("")
        print(cl_stats)

    # print(time.process_time() - start, flush=True)
    start = time.process_time()
    cl_stats_data_df = cl_stats.reset_index().groupby(['trace_str']).sum().reset_index()
    cl_stats_data_df.rename(columns={'byte': 'count'}, inplace=True)
    # cl_stats_data_df.set_index('trace_str', inplace=True)

    cl_filter_list = ['CL_NEW', 'CL_END', 'CL_OUT_REQ', 'CL_OUT_CNF', 'CL_IN', 'CL_START', 'CL_TX', 'CL_RX', 'CL_DATA_REQ', 'CL_DATA_RESP', 'CL_TXDONE']

    cl_stats_data_df = cl_stats_data_df[cl_stats_data_df.trace_str.isin(cl_filter_list)]
    dd_cl_stats = {
        'CL_NEW_END': {},
        'CL_TX_RX': {},
        'CL_DATA_REQ_RESP': {},
        'CL_TXDONE': {},
    }

    if not cl_stats_data_df.empty:

        cl_stats_data_df.set_index("trace_str", inplace=True)
        # print(cl_stats_data_df)
        cl_stats = cl_stats.reset_index()

        cl_stats_dict = cl_stats_data_df.to_dict()['count']

        # cl new end
        cl_ends = cl_stats[cl_stats.trace_str == 'CL_END'].drop(columns='trace_str').set_index('sts').to_dict()['byte']
        dd_cl_stats['CL_NEW_END']['CL_END'] = {
            'val': cl_stats_dict['CL_END'],
            'drilldown': cl_ends
        }
        cl_out_cnfs = cl_stats[cl_stats.trace_str == 'CL_OUT_CNF'].drop(columns='trace_str').set_index('sts').to_dict()['byte']

        dd_cl_stats['CL_NEW_END']['CL_NEW'] = {
            'val': cl_stats_dict['CL_NEW'] if 'CL_NEW' in cl_stats_dict else 0,
            'drilldown': {
                'CL_IN': cl_stats_dict['CL_IN'] if 'CL_IN' in cl_stats_dict else {},
                'CL_OUT': {
                    'val': cl_stats_dict['CL_OUT_REQ'] if 'CL_OUT_REQ' in cl_stats_dict else 0,
                    'drilldown': cl_out_cnfs
                }
            }
        }

        # cl tx rx
        cl_txs = cl_stats[cl_stats.trace_str == 'CL_TX'].drop(columns='trace_str').set_index('sts').to_dict()['byte']
        cl_rxs = cl_stats[cl_stats.trace_str == 'CL_RX'].drop(columns='trace_str').set_index('sts').to_dict()['byte']
        dd_cl_stats['CL_TX_RX']['CL_TX'] = {
            'val': cl_stats_dict['CL_TX'] if 'CL_TX' in cl_stats_dict else 0,
            'drilldown': cl_txs
        }
        dd_cl_stats['CL_TX_RX']['CL_RX'] = {
            'val': cl_stats_dict['CL_RX'] if 'CL_RX' in cl_stats_dict else 0,
            'drilldown': cl_rxs
        }

        # cl data req resp
        cl_data_resps = cl_stats[cl_stats.trace_str == 'CL_DATA_RESP'].drop(columns='trace_str').set_index('sts').to_dict()['byte']
        dd_cl_stats['CL_DATA_REQ_RESP']['CL_DATA_REQ'] = {
            'val': cl_stats_dict['CL_DATA_REQ'] if 'CL_DATA_REQ' in cl_stats_dict else 0,
            'drilldown': {}
        }
        dd_cl_stats['CL_DATA_REQ_RESP']['CL_DATA_RESP'] = {
            'val': cl_stats_dict['CL_DATA_RESP'] if 'CL_DATA_RESP' in cl_stats_dict else 0,
            'drilldown': cl_data_resps
        }

        # cl tx done
        cl_tx_dones = cl_stats[cl_stats.trace_str == 'CL_TXDONE'].drop(columns='trace_str').set_index('sts').to_dict()['byte']
        dd_cl_stats['CL_TXDONE'] = {
            'val': cl_stats_dict['CL_TXDONE'] if 'CL_TXDONE' in cl_stats_dict else 0,
            'drilldown': cl_tx_dones
        }

    if GRAPH_OPTION == GRAPH_HIGHCHARTS:
        with open('myJson.js', 'w') as f:
            f.write('// data logged at {}.\n\n'.format(get_datetime()))
            f.write('const nodeip="{}";\n'.format(args.ip))
            f.write('const nodefile="{}";\n'.format(args.file))
            f.write('const jsonData={\n')
        write_df_to_json('clstatsJson', dd_cl_stats, isdict=True)

    # obtain fastlink df
    if '0' in graph_ans_list or '1' in graph_ans_list:
        if not args.quiet:
            print("\nFastLink...Data Processing...", flush=True, end='')

        graph_fastlink()

    if '0' in graph_ans_list or '2' in graph_ans_list or '3' in graph_ans_list:
        while True:
            timings_df = pd.DataFrame()
            timings_plot_df = pd.DataFrame()
            filter_list = [6, 122, 123, 124, 129, 130, 141, 140, 142]
            timings_df = cl_csv_df[cl_csv_df.tracecode_dec.isin(filter_list)]

            trace_list = list(set(list(timings_df.tracecode_dec)))
            if not set(filter_list).issubset(trace_list):
                print("\n**** All required traces {} are not present. {}  Cannot draw the graph".format(filter_list, trace_list))
                show_required_traces(filter_list)
                break

            # nextCLI

            nextcli_df = timings_df[timings_df.tracecode_dec == tracing_events_str_num['CL_NEXT_CLI']][['byte', 'trace_info']].rename(columns={'trace_info': 'nextcli'})
            nextcli_df[['rx', 'tx']] = nextcli_df.nextcli.str.split(' ', expand=True).drop(columns=[0, 1, 3], axis=1)
            nextcli_df.nextcli = "CLI(" + nextcli_df.tx + "," + nextcli_df.rx.str[:-1] + ")"
            nextcli_df.drop(columns=['rx', 'tx'], inplace=True)

            timings_df = timings_df.merge(nextcli_df, on='byte', how='left')
            timings_df.nextcli = timings_df.nextcli.fillna(method='bfill')
            timings_df = timings_df[timings_df.tracecode_dec != tracing_events_str_num['CL_NEXT_CLI']]

            # # aftertxcol
            timings_df['aftertx_col'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['CL_TX']), "afterTx", np.nan)

            # beforetxcol
            timings_df['beforetx_col'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['CL_FRT32_TX_CALL']), "beforeTx", np.nan)

            # dc
            timings_df['dummyAftertx'] = timings_df.aftertx_col.shift(1)
            timings_df['dummyclid'] = timings_df.cl_id.shift(1)
            timings_df['dc_col'] = np.where(((timings_df.tracecode_dec == tracing_events_str_num['LMMGR_DATA_CONF']) & (
                timings_df.dummyAftertx == "afterTx") & (timings_df.cl_id == timings_df.dummyclid)), "dc", np.nan)
            timings_df.drop(columns=['dummyclid', 'dummyAftertx'], inplace=True)

            # txend
            timings_df['txend_col'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['FRT32_TX_END']), "txEnd", np.nan)

            # afterRx
            timings_df['afterrx_col'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['CL_RX']), "afterRx", np.nan)

            # beforeRx
            timings_df['beforerx_col'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['CL_FRT32_RX_CALL']), "beforeRx", np.nan)

            # rxstart
            timings_df['dummyAfterrx'] = timings_df.afterrx_col.shift(1)
            timings_df['dummyclid'] = timings_df.cl_id.shift(1)
            timings_df['rxstart_col'] = np.where(((timings_df.tracecode_dec == tracing_events_str_num['FRT32_RX_START']) & (
                timings_df.dummyAfterrx == "afterRx") & (timings_df.cl_id == timings_df.dummyclid)), "rxStart", np.nan)
            timings_df.drop(columns=['dummyclid', 'dummyAfterrx'], inplace=True)

            # rxend
            timings_df['dummyRxstart'] = timings_df.rxstart_col.shift(1)
            timings_df['dummyclid'] = timings_df.cl_id.shift(1)
            timings_df['rxend_col'] = np.where(((timings_df.tracecode_dec == tracing_events_str_num['FRT32_RX_END']) & (
                timings_df.dummyRxstart == "rxStart") & (timings_df.cl_id == timings_df.dummyclid)), "rxEnd", np.nan)
            timings_df.drop(columns=['dummyclid', 'dummyRxstart'], inplace=True)

            # timings_df['rxend_col'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['FRT32_RX_END']), "rxEnd", np.nan)

            # # FRT_dec
            # timings_df['frt_dec'] = timings_df.apply(lambda x: int(x.frt_hex[-min(len(x.frt_hex)-2, 8):], 16), axis=1)

            timings_df.drop(columns=['frt_hex'], inplace=True)

            # timestamps for tx rx start and end
            timings_df['ts_rxstart'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['FRT32_RX_START']), timings_df.frt_val, np.nan)
            timings_df['ts_rxend'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['FRT32_RX_END']), timings_df.frt_val, np.nan)
            timings_df['ts_txstart'] = np.where((timings_df.dc_col == "dc"), timings_df.frt_val, np.nan)
            timings_df['ts_txend'] = np.where((timings_df.tracecode_dec == tracing_events_str_num['FRT32_TX_END']), timings_df.frt_val, np.nan)

        # exit(0)
            if '0' in graph_ans_list or '2' in graph_ans_list:
                if not args.quiet:
                    print("\nCL Timings...Data Processing...", flush=True, end='')
                graph_cl_timings()

            if '0' in graph_ans_list or '3' in graph_ans_list:
                if not args.quiet:
                    print("\nTimelineVisualizer...Data Processing...", flush=True, end='')
                graph_timeline_visualiser()

            break

    # buffer get/release
    if '0' in graph_ans_list or '4' in graph_ans_list:
        if not args.quiet:
            print("\nBufMgr...Data Processing...", flush=True, end='')
        graph_buf_mgr()

    # mode stats
    if '0' in graph_ans_list or '5' in graph_ans_list:
        if not args.quiet:
            print("\nModeChan Stats...Data Processing...", flush=True, end='')
        graph_mode_chan()
    if GRAPH_OPTION == GRAPH_HIGHCHARTS:

        with open('myJson.js', 'a') as f:
            f.write('\n}')

    # create a html file
    create_html_file()


def check_system_dependency():
    # run ssh or plink depending upon the os
    LOG_INFO(f"Checking system dependency", False)

    LOG_INFO(f"System OS={os.name}", False)
    if os.name == OS_POSIX:
        p1 = subprocess.Popen(['which', 'sshpass'], stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
    else:

        p1 = subprocess.Popen(['where', "plink", ],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    LOG_INFO(f'{p1}', False)
    try:
        raw_output, err = p1.communicate(timeout=30)
    except:
        print("prob while communicating quit:{}", glob["QUIT"])
        print("err={}, retCode={}, raw_output={}".format(
            err, p1.returncode, raw_output))
        LOG_ERR("prob while communicating")
        return False

    if "plink.exe" in raw_output.decode('utf-8') or "sshpass" in raw_output.decode('utf-8'):
        LOG_INFO(f'plink or ssh exists', False)
        return True

    if os.name == OS_POSIX:
        LOG_ERR("*** Requires sshpass to continue. Install using sudo apt install sshpass")
    else:
        LOG_ERR("*** Requires plink.exe to continue. Please install plink.")

    return False


cl_id = 0
first_cl_id = 0
total_cls = 0

if __name__ == "__main__":
    outputVer = ""
    date_today = get_datetime().split(' ')[0].split('-')
    date_today = date_today[2] + date_today[1] + date_today[0]
    graph_file = 'decoded.csv'
    graph_ans_list = []
    REACHABLE = False
    glob["QUIT"] = False
    lastseqinfo = ""

    # verify we have python atleast 3.x+
    assert sys.version_info >= (3, 6), "Requires Python 3.6+. Current Version is {}".format(sys.version.split(" ", 2)[0])

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
        %(prog)s -f decoded.csv -g 1,3
        %(prog)s -f hex_trace.txt -g 0
        In second example, the app will create the necessary csv file

    Example 7: Monitoring a live trace with mask,save the hex traces and decoded file in csv and plot the graphs 1,2,3
        %(prog)s -i 10.70.100.118 -m 81FF6702BCFB033E60C78F3FFFBFFF01000000FFFFFFFFFFFFFDDFFDDFFFFFFFFF7FFCFFFF -t -c -g 1,2,3
    """

    # write to a file per day
    outputfile = OUTPUT_FILE_NAME + "_" + date_today + OUTPUT_FILE_EXT

    my_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                        description='''A CLI tool to decode the hex trace for DSP for G5R
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
                           help='Debug Mode. Debug Logs are saved under {}'.format(DEBUG_LOG_FILE))
    # my_parser.add_argument('-e', '--export', metavar="export",
    #                        type=str,
    #                        action=exportAction,
    #                        help='Export Graph to a file. Supported extensions {}. \nWorks only with -g option. Currenlty not used.'.format(valid_img_ext_list))

    my_group.add_argument('-f', '--file',
                          type=str,
                          help='Path to the local file to decode. The local file should be obtained from hexdump -C option')
    my_parser.add_argument('-g', '--graph',
                           type=str,
                           help="Show Graphs live or using decoded csv file or the hex traces.\n You may select multiple separating by comma (,)\n  {}".format('\n  '.join(str(key)+" : "+str(val) for key, val in GRAPH_NUM_STR.items())))
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
    my_parser.add_argument('-o', '--output',
                           default=outputfile,
                           help='Output to a file (Default={})'.format(outputfile))
    my_parser.add_argument('-p', '--poll',
                           type=float,
                           default=POLL_INTERVAL,
                           help='Polling Inverval in seconds (Default:{})'.format(POLL_INTERVAL))
    my_parser.add_argument('-q', '--quiet',
                           action='store_true',
                           help='Quiet the output. Do not show the decoded traces in the output')
    my_parser.add_argument('-r', '--range',
                           type=str,
                           default='',
                           help="Give a range of CLs to decode based on CL ID. Format startCLId:endCLId")
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

    if args.debug:
        with open(DEBUG_LOG_FILE, 'w') as f:
            f.write("MonitorTrace V{}\n".format(APP_VERSION))
    LOG_INFO("System Version {}".format(sys.version_info), False)
    LOG_INFO("CLI arguments Parsed", False)
    LOG_INFO(args, False)

    # check for system dependcies i.e. sshpass for linux and plink for windows
    if not check_system_dependency():
        exit(0)

    # if export option is provided with graphing option exit
    # if args.export and not args.graph:
    #     print("Error -e option works only with -g")
    #     exit(0)

    LOG_INFO("*** Monitoring traces v" + APP_VERSION +
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
            hexMaskStr = args.mask if args.mask else DEFAULT_DEBUG_MASK
            print("\n~~~ TRACE IDs MAP (0x{}) ~~~\n".format(hexMaskStr))
            # hexMaskStr = 80FF6702BCFB033E00C78F3FFFBFFF01000000FFFFFFFFFFFFF9F7FFFFFFFFFFFF7FF8FFFF

            newHexStr = ""
            for index in range(0, len(hexMaskStr), 2):
                newHexStr += str(hexMaskStr[index+1]) + str(hexMaskStr[index])
            # newHexStr = 08FF7620CBBF30E3007CF8F3FFFBFF10000000FFFFFFFFFFFF9F7FFFFFFFFFFFFFF78FFFFF

            correctedbinaryStr = ""
            for nib in newHexStr:
                bitStr = "{:04b}".format(int(nib, 16))[::-1]
                correctedbinaryStr = correctedbinaryStr + bitStr
            # correctedbinaryStr = 00000001111111111110011001000000001111011101111111000000011111000000000011100011111100011111110011111111111111011111111110000000000000000000000000000000111111111111111111111111111111111111111111111111100111111110111111111111111111111111111111111111111111111111111111111110000111111111111111111111
            TRACING_DEBUG_VALUES_LIST = list(correctedbinaryStr)

            for key, val in tracing_events_num_str.items():
                print("{:>28s} => {:10s} [{:3d}, 0x{:03X}] ".format( val, "ENABLED" if TRACING_DEBUG_VALUES_LIST[key] == '0' else "DISABLED", key, key),
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
            LOG_ERR("UNREACHABLE!!!")
            exit(1)
            # ret=os.system('echo Y | plink -pw itron -ssh root@10.70.100.118 uptime')
        print("REACHABLE")
        LOG_INFO("Node {} REACHABLE".format(args.ip), False)
        REACHABLE = True

    if args.range:
        cl_id_range = args.range
        cnt_colon = cl_id_range.count(':')
        if cnt_colon > 1:
            LOG_ERR("Error: Format not correct. Range format should be start:end")
            exit(0)

    if args.graph:

        graph_ans_list = args.graph.split(',')
        result = all(int(elem, 10) in list(GRAPH_NUM_STR.keys()) for elem in graph_ans_list)

        if not result:
            LOG_ERR("Invalid entry {}. Choose from {}\n  {}".format(graph_ans_list,
                                                                    list(GRAPH_NUM_STR.keys()),
                                                                    '\n  '.join(str(key)+" : "+str(val) for key, val in GRAPH_NUM_STR.items())))
            exit(0)

    # if file mode process and exit
    if args.file:
        extension = args.file.split('.')[-1].strip().lower()
        if not os.path.isfile(args.file):
            LOG_ERR("*** Cannot find the file '{}'".format(args.file))
            exit()
        if (extension == 'csv'):
            LOG_INFO("{} is CSV, using it directly".format(args.file), False)
            graph_file = args.file

        else:
            LOG_INFO("{} is NOT CSV, processing hexdump".format(args.file), False)
            with open(args.file, 'r') as file:
                hexdump = file.read()
                # print(hexdump)
                process_hexdump(hexdump, 0, True)
            print("")
            LOG_INFO(
                " - Decoded Traces are saved to {}\{}".format(get_current_path(), args.output))

        if args.graph:
            LOG_INFO("Creating Graph", False)
            graph_it()
            LOG_INFO("Opening in web at file://{}".format(os.path.realpath(FILE_HTML)), False)
            webbrowser.open('file://' + os.path.realpath(FILE_HTML))

        exit()

    print(" - Reading the device... ", end='', flush=True)

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
        LOG_ERR("\n\n*** The node Version A7 {} is not compatible. Minimum Required {}".format(a7_ver, MIN_A7_VER))
        choice = input("The APP may not function properly. Continue? (y/n)? ")
        if choice.lower() != 'y':
            exit(0)

    LOG_INFO("macAddr {}".format(macAddr), False)
    LOG_INFO("Version {}".format(a7_ver), False)

    # if mask is provided, set and read back
    if args.mask:
        print(" - Setting the mask... {} ...".format(args.mask), end='')
        ret, output = test_ssh(
            args.ip, "pib -si E0000000 -v {} >/dev/null".format(args.mask))
        if (ret != RET_SUCC):
            print("FAILED")
            LOG_ERR("Cannot write the pib. Check if DSP is running or NOT")
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
    LOG_INFO("Running hexdump in the target", False)
    ret, output = test_ssh(
        args.ip, "cat /dev/dsp_rf_tracing |hexdump -C > " + HEX_TRACE_DIR + "hexTrace.log &")

    if ret != RET_SUCC:
        LOG_ERR("error {}".format(ret))
        exit()

    cur_line = 0
    last_count = 0
    showFirstLine = True

    LOG_INFO(" - Decoded Traces will be saved to {}\{}".format(get_current_path(), args.output))
    if args.trace:
        LOG_INFO(" - Hex Traces will be saved to {}\{}".format(get_current_path(), hexfile))
    if args.csv:
        LOG_INFO(" - decoded CSV will be saved to {}\{}".format(get_current_path(), csvfile))

    LOG_INFO("\n*** Monitoring LIVE on {} (Poll intv:{} secs)".format(args.ip, args.poll))
    print("")

    graph_shown = False
    new_count = 0

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
        mode = 'w'

        my_wait(args.poll, new_count)

        REACHABLE = True

        # trace_cmd = "lastline=$( wc -l < " + HEX_TRACE_DIR + "hexTrace.log)p; sed -n " + str(hexTraceLastLine) + ",$lastline < " + HEX_TRACE_DIR + "hexTrace.log"
        ret, output = test_ssh(args.ip, "cat " + HEX_TRACE_DIR + "hexTrace.log")

        hexdump = output.decode('utf-8')

        new_count = hexdump.count('\n')

        if (last_count != new_count):

            last_count = new_count
            cur_line = process_hexdump(hexdump, cur_line, showFirstLine)

            if (args.trace and hexdump):
                with open(hexfile, mode) as fout:
                    fout.writelines(hexdump)
            showFirstLine = False

            if (args.graph and (not graph_shown or GRAPH_OPTION == GRAPH_HIGHCHARTS)):
                if GRAPH_OPTION == GRAPH_PLOTLY:
                    print("\n\n##### Graphs are not live. It will be shown only once.")
                graph_it()
                if not graph_shown:
                    webbrowser.open('file://{}'.format(os.path.realpath(FILE_HTML)), new=0)
                graph_shown = True

        # time.sleep(args.poll)
