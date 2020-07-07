from sys import exit, argv, stdin
import sys
import signal
import os
import subprocess
import socket
import atexit
import time
from datetime import datetime
import argparse
import csv

# list of global variables subject to change
glob = {
    'QUIT': False,
}


OS_POSIX = "posix"
OS_WIN = "nt"
__VERSION__ = "1.8"
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
    130: "CLT_RESERVED",
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
    211: "LMDC",
    212: "SDC_CHECK",
    213: "LDC_CHECK",
    214: "SDC_UPDATE",
    215: "LDC_UPDATE",
    216: "SDC_TXDUR_CUR",
    217: "SDC_WINDOW_SPAN",
    218: "SDC_WINDOW_BIN",
    219: "LDC_TXDUR_CUR",
    220: "LDC_WINDOW_SPAN",
    221: "LDC_WINDOW_BIN",
    230: "LMDC_RESERVED",
}
tracing_events_str_num = {value: key for key,
                          value in tracing_events_num_str.items()}
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
    0xFB: "ERROR",
    0xFC: "INVALID",
    0xFD: "LOGGER_IND",
    0xFE: "STATUS_IND",
    0xFF: "SNIFFER_I",

}


def LOG_DBG(str):
    if args.debug == 0:
        return
    print(str)


def convert_pib_val(pibval):
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
        print("==="*40)

    elif tracing_events_num_str[code] == "CL_TX":
        status = int(infoArr[14] + infoArr[13], 16)
        freq = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) freq {:d}KHz".format(
            sts_code_str[status], status, status, freq * 100)

    elif tracing_events_num_str[code] == "CL_RX":
        status = int(infoArr[14] + infoArr[13], 16)
        freq = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) freq {:d}KHz".format(
            sts_code_str[status], status, status, freq * 100)

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
        status = int(infoArr[14] + infoArr[13], 16)
        clId = int(infoArr[16] + infoArr[15], 16)
        processClInfo = "{:s}({:d},0x{:X}) CL Id {:d}".format(
            sts_code_str[status], status, status, clId)

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
        if status == 1:
            statusStr = "TX_SUCCESS"
        elif status == 0:
            statusStr = "TX_FALURE"
        elif status == 2:
            statusStr = "RX_SUCCESS"
        else:
            statusStr = "TX/RX UNDEF"

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
    firstLine = ' byteNUM:   frt_dec   (0xfrt_hexAD)  [TRACECODE]:       TRACE INFO '

    if showFirstLine:
        print(firstLine)
        outputList.extend(outputVer + "\n\n")
        outputList.extend(firstLine + "\n")
        csvList.append(["byteNUM", "frt_dec", "frt_hex",
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

        print(output, "[{}]".format(cl_id))

    halflen = int(len(output)/2) - int(len(get_datetime())/2)

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


def my_wait(sec):
    for i in range(sec):
        # if(glob['QUIT']):
        #     break
        print("*** Polling {} ({}) in {:3d}sec...".format(args.ip,
                                                          macAddr, sec-i), end='\r')
        sys.stdout.flush()
        time.sleep(1)
    print


def signal_handler(sig, frame):
    print('\nYou pressed Ctrl+C!')

    exit_handler()
    glob["QUIT"] = True
    raise SystemExit


def graph_it():
    try:
        import pandas as pd
        import numpy as np
        # import mplcursors
        import matplotlib.pyplot as plt

    except:
        print("installing dependecies...")
        p1 = subprocess.Popen(['pip', 'install', 'pandas'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p1.communicate()
        p1 = subprocess.Popen(['pip', 'install', 'numpy'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p1.communicate()
        p1 = subprocess.Popen(['pip', 'install', 'mplcursors'],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p1.communicate()
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

        # import mplcursors

        import numpy as np

    plt.style.use('seaborn-deep')
    plt.style.use('ggplot')

    graph_dic = {
        0: "All",
        1: "RTT Between CL DataGet Req/Cnf",
        2: "CL duration Histogram",
        3: "CL Timing"
    }

    for key, val in graph_dic.items():
        print("\t{} : {}".format(key, val))
    answer = input("Enter the number(use a single number or array like 1,2)")
    answer_list = answer.split(',')

    print("showing graph", answer_list)

    csv_df = pd.read_csv(sep=',', skiprows=1, names=[
                         'byte', "frt_dec", 'frt_hex', 'trace_code', 'trace_info'], filepath_or_buffer=args.graph)
    # csv_df[['tracecode_dec','tracecode_hex']] = df.Name.str.split(expand=True)
    csv_df[['tracecode_dec', 'tracecode_hex']
           ] = csv_df['trace_code'].str.split(expand=True)
    csv_df.drop(columns=['trace_code'], inplace=True)
    csv_df = csv_df.astype({'tracecode_dec': int})
    csv_df['cl_id'] = csv_df["trace_info"].apply(
        lambda x: x.split()[4] if "CL_OUT_CNF" in x or "CL_START" in x else "")
    csv_df['cl_id'].ffill()
    csv_df = csv_df.replace("", np.nan).ffill()

    traceCodeMap_df = pd.DataFrame(tracing_events_num_str.items(), columns=[
                                   'tracecode_dec', 'trace_str'])

    stat_total = csv_df.groupby('tracecode_dec').count(
    ).reset_index().astype({"tracecode_dec": int})
    stat_total = stat_total[['tracecode_dec', 'byte']]
    stat_total = stat_total.merge(traceCodeMap_df, how='inner', on="tracecode_dec").sort_values(
        by=['tracecode_dec']).reset_index()

    cl_csv_df = csv_df[(csv_df['tracecode_dec'] >= 131) &
                       (csv_df['tracecode_dec'] <= 151)]
    cl_csv_df.drop(columns=['tracecode_hex', 'frt_hex'], inplace=True)
    cl_csv_df['sts'] = cl_csv_df['trace_info'].apply(
        lambda x: "" if "STS" not in x else x.split()[1].split('(')[0])
    cl_csv_df = cl_csv_df.merge(traceCodeMap_df, on="tracecode_dec")
    cl_csv_df.sort_values(by=['byte'], inplace=True)

    cl_stats = cl_csv_df.groupby(
        ['tracecode_dec', 'trace_str', 'sts', ]).count()
    cl_stats = cl_stats['byte']

    # obtain fastlink df
    if '0' in answer_list or '1' in answer_list:
        fig = plt.figure()

        fast_link_df = cl_csv_df[(cl_csv_df["tracecode_dec"] == 149) | (
            cl_csv_df["tracecode_dec"] == 148)][['byte', 'frt_dec', 'tracecode_dec', 'sts', 'cl_id']]
        if not fast_link_df.empty:
            fast_link_df['A_dif'] = fast_link_df['frt_dec'].diff()
            fast_link_df['shifted_frt'] = fast_link_df['frt_dec'].shift()
            fast_link_df['prev_trace'] = fast_link_df['tracecode_dec'].shift()
            fast_link_df['diff'] = fast_link_df.apply(lambda x: np.NaN if (
                x['tracecode_dec'] == x['prev_trace'] or x['tracecode_dec'] == 148) else x['A_dif'], axis=1)
            fast_link_df.drop(
                columns=['A_dif', 'shifted_frt', 'prev_trace'], inplace=True)

            # obtain rtt_df
            rtt_df = fast_link_df[['byte', 'diff']].dropna()
            rtt_df = rtt_df.groupby('diff').agg(
                'count').rename(columns={'byte': 'freq'})

            # PDF
            rtt_df['pdf'] = rtt_df['freq'] / sum(rtt_df['freq'])
            # CDF
            rtt_df['cdf'] = rtt_df['pdf'].cumsum()
            rtt_df = rtt_df.reset_index()

            # Divide the figure into a 1x2 grid, and give me the first section
            rtt_plt = fig.add_subplot(211)

            # Divide the figure into a 1x2 grid, and give me the second section
            rtt_hist = fig.add_subplot(212)
            rtt_df.plot(x='diff', y=['pdf', 'cdf'], grid=True,
                        title="RTT between clDataGet Req/Cnf", ax=rtt_plt)

            rtt_df.plot(kind='bar', x='diff', y='freq',
                        title="Histogram of RTT", ax=rtt_hist)

    if '0' in answer_list or '2' in answer_list:

        cl_dur_df = cl_csv_df[cl_csv_df['tracecode_dec']
                              == 132][['byte', 'sts', 'trace_info']]
        if not cl_dur_df.empty:
            cl_dur_df['dur_ms'] = cl_dur_df.apply(lambda x: x['trace_info'].split(' ')[
                3].split('msec')[0], axis=1)
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
            # print(rtt_df)
            # print(cl_dur_df)

            cl_dur_df.plot(kind='line', x='dur_ms', y=[
                'pdf', 'cdf'], title="Frequency of Duration in msec")

    if '0' in answer_list or '3' in answer_list:
        timings_df = pd.DataFrame()
        timings_df = cl_csv_df[(cl_csv_df['tracecode_dec'] == 131) | (cl_csv_df['tracecode_dec'] == 151) | (
            cl_csv_df['tracecode_dec'] == 141) | (cl_csv_df['tracecode_dec'] == 140) | (cl_csv_df['tracecode_dec'] == 6)]
        print(timings_df)

    # print("clstats\n", cl_stats)

    plt.show()


cl_id = 0

if __name__ == "__main__":
    outputVer = ""
    date_today = get_datetime().split(' ')[0].split('-')
    date_today = date_today[2] + date_today[1] + date_today[0]
    REACHABLE = False
    glob["QUIT"] = False

    epilog = """
    Example Usage:

    Example 1: Running a local hex file
        %(prog)s -f traces.log

    Example 2: Monitoring a live trace using wifi ipv4 addr.
        %(prog)s -i 100.70.100.118

    Example 3: Setting the debug mask and monitoring a live trace
        %(prog)s -m 81FF6702BCFB033E60C78F3FFFFFFFFF070000FFFFFFFFFFFFFDFFFFFF -i 100.70.100.118

    Example 4: Outputing the decoded file (e.g. for live tracing)
        %(prog)s -i 100.70.100.118 -o decodedTraces.log

    Example 5: Monitoring a live trace with mask and save the hex traces and decoded file in csv as well
        %(prog)s -i 10.70.100.118 -m 81FF6702BCFB033E60C78F3FFFFFFFFF070000FFFFFFFFFFFFFDFFFFFF -t -c

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
    my_group.add_argument('-g', '--graph',
                          type=str,
                          help='Show Graphs using decoded.csv')
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
        args.ip = args.ip.strip()
        print(" - Node IP '{}'..VALID..".format(args.ip), end='')
        if checkNodeReachability(args.ip) == RET_FAIL:
            print("UNREACHABLE!!!")
            exit(1)
            # ret=os.system('echo Y | plink -pw itron -ssh root@10.70.100.118 uptime')
        print("REACHABLE")
        REACHABLE = True

    if args.graph:
        graph_it()
        exit()

    # if file mode process and exit
    if args.file:

        with open(args.file, 'r') as file:
            hexdump = file.read()
            # print(hexdump)
            process_hexdump(hexdump, 0, True)
        print("")
        print(
            " - Decoded Traces are saved to {}\{}".format(get_current_path(), args.output))

        exit()

    print(" - Reading the device... ", end='')
    sys.stdout.flush()

    ret, outputVer = test_ssh(
        args.ip, "cat /etc/Version.txt;echo -n 'RF MAC: '; pib -gi 030000A2  --raw;echo -n 'Uptime: ';uptime;echo -n 'MAC ADDR: ';pib -gi FFFFFFF4;", True)
    if (ret != RET_SUCC or str_decode(outputVer)).strip() == "":
        print("FAILED")
        print("Cannot read the pib. Check if DSP is running or NOT and try again.")
        exit(1)

    outputVer = str_decode(outputVer).strip()
    opp_macAddr = outputVer.split()[-1]
    macAddr = convert_pib_val(outputVer.split()[-1])
    outputVer = outputVer.replace(opp_macAddr, macAddr, 1)

    print('')
    print(outputVer)

    # exit(0)
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
        print("{} ...MISMATCH".format(output))
        exit(1)

    print("{} ...SUCCESS".format((output)))

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

    # MAIN monitoring LOOP
    while True:

        if args.mask:
            ret, output = test_ssh(
                args.ip, "pib -si E0000000 -v {} >/dev/null".format(args.mask))
            if (ret != RET_SUCC):
                print("Cannot write the pib. Check if DSP is running or NOT")
                REACHABLE = False
                my_wait(args.poll)
                continue

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

        # time.sleep(args.poll)
        my_wait(args.poll)
