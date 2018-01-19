from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *


class TCLFREnterMode(object):
    """docstring for TCLFREnterMode"""

    def __init__(self, sequence_cnt, source_id, cp_lfr_mode, cp_lfr_enter_mode_time):
        super(TCLFREnterMode, self).__init__()

        self.cp_lfr_mode = cp_lfr_mode
        self.cp_lfr_enter_mode_time = cp_lfr_enter_mode_time
        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_ENTER_MODE, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_ENTER_MODE, \
                                  source_id).tcHeader;

        self.ccsdsPacket = self.buildCCSDSPacket()

    def buildCCSDSPacket(self):
        parameters = self.buildTCParameters();
        packet = self.header + parameters
        (ChkMSB, ChkLSB) = self.crcGenerator.GetCRCAsTwoBytes(packet);
        packet.append(ChkMSB)
        packet.append(ChkLSB)
        return packet

    def buildTCParameters(self):
        parameters = []
        # CP_LFR_MODE
        parameters.append(0x00)  # spare Bytes
        parameters.append(self.cp_lfr_mode & 0x0f)
        # CP_LFR_ENTER_MODE_TIME
        val = (self.cp_lfr_enter_mode_time & 0x0000ff000000) >> 24;
        parameters.append(val)
        val = (self.cp_lfr_enter_mode_time & 0x000000ff0000) >> 16;
        parameters.append(val)
        val = (self.cp_lfr_enter_mode_time & 0x00000000ff00) >> 8;
        parameters.append(val)
        val = (self.cp_lfr_enter_mode_time & 0x0000000000ff);
        parameters.append(val)
        parameters.append(0x00)  # fineTime set to 0
        parameters.append(0x00)  # fineTime set to 0
        return parameters

    def printCCSDSPacketInHex(self):
        print("size of the CCSDS packet = " + str(self.ccsdsPacket.__len__()) + " bytes")
        # for j in range(self.ccsdsPacket.__len__()):
        #	print hex(self.ccsdsPacket[j])
        print(self.ccsdsPacket)

    def setCP_LFR_MODE(self, cp_lfr_mode):
        self.cp_lfr_mode = cp_lfr_mode
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setCP_LFR_ENTER_MODE_TIME(self, cp_lfr_enter_mode_time):
        self.cp_lfr_enter_mode_time = cp_lfr_enter_mode_time
        self.ccsdsPacket = self.buildCCSDSPacket()
