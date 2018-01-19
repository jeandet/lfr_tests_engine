CCSDS_VERSION_NUMBER = 0
TC_PACKET = 1
WITH_HEADER = 1
RPW_PID_2 = 76
PRIVATE_SCIENCE_OR_TELECOMMAND = 12
STANDALONE_PACKET = 3
CCSDS_SECONDARY_HEADER_FLAG = 0
PUS_VERSION = 1

DEFAULT_SEQUENCE_COUNT = 0

TARGET_LOGICAL_ADDRESS = 254
PROTOCOLE_IDENTIFIER_CCSDS = 2
RESERVED_DEFAULT = 0
USER_APPLICATION = 0

CCSDS_TC_TM_PACKET_OFFSET = 7
LENGTH_ENTER_MODE 		= 20 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_LOAD_COMMON_PAR 	= 14 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_LOAD_NORMAL_PAR  = 22 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_UPDATE_TIME		= 18 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_LOAD_KCOEFFICIENTS = 142 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_LOAD_FBINS_MASK  = 60 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_EN_CAL   = 12 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_DIS_CAL   = 12 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_LOAD_FILTER_PAR  = 28 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_UPDATE_INFO = 110 - CCSDS_TC_TM_PACKET_OFFSET
LENGTH_DUMP_PAR = 12 - CCSDS_TC_TM_PACKET_OFFSET

# SERVICE TYPES
TYPE_EQ_CONFIGURATION = 181
TYPE_TIME_MANAGEMENT  = 9

# SERVICE SUBTYPES
SUBTYPE_LOAD_COMMON_PAR = 11
SUBTYPE_LOAD_NORMAL_PAR = 13
SUBTYPE_ENTER_MODE = 41
SUBTYPE_LOAD_KCOEFFICIENTS = 93
SUBTYPE_DUMP_KCOEFFICIENTS = 95
SUBTYPE_LOAD_FBINS_MASK = 91
SUBTYPE_UPDATE_TIME = 129
SUBTYPE_EN_CAL    =   61
SUBTYPE_DIS_CAL   =   63
SUBTYPE_LOAD_FILTER_PAR = 97
SUBTYPE_UPDATE_INFO = 51
SUBTYPE_DUMP_PAR = 31

RPW_INTERNAL = 254

STANDBY	= 0
NORMAL 	= 1
BURST 	= 2
SBM1 	= 3
SBM2 	= 4

# TC_LFR_LOAD_COMMON_PAR
SY_LFR_BW = 1
SY_LFR_SP0 = 0
SY_LFR_SP1 = 0
SY_LFR_R0 = 0
SY_LFR_R1 = 0
SY_LFR_R2 = 0

# TC_LFR_LOAD_NORMAL_PAR
SY_LFR_N_SWF_L = 2048
SY_LFR_N_SWF_P = 300
SY_LFR_N_ASM_P = 3600
SY_LFR_N_BP_P0 = 4
SY_LFR_N_BP_P1 = 20
SY_LFR_N_CWF_LONG_F3 = 0

# TC_LFR_LOAD_FILTER_PAR
SY_LFR_PAS_FILTER_ENABLED = 0
SY_LFR_PAS_FILTER_MODULUS = 4
SY_LFR_PAS_FILTER_TBAD = 1.0
SY_LFR_PAS_FILTER_OFFSET = 0
SY_LFR_PAS_FILTER_SHIFT = 0.5
SY_LFR_SC_RW_DELTA_F = 0.025

# TC_LFR_UPDATE_INFO
CP_RPW_SC_RW1_F1_FLAG = 1
CP_RPW_SC_RW1_F2_FLAG = 1
CP_RPW_SC_RW2_F1_FLAG = 1
CP_RPW_SC_RW2_F2_FLAG = 1
CP_RPW_SC_RW3_F1_FLAG = 1
CP_RPW_SC_RW3_F2_FLAG = 1
CP_RPW_SC_RW4_F1_FLAG = 1
CP_RPW_SC_RW4_F2_FLAG = 1
