from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *


class TCLFRLoadCommonParR2(object):
    """docstring for TCLFRLoadCommonParR2"""

    def __init__(self, sequence_cnt, source_id):
        super(TCLFRLoadCommonParR2, self).__init__()

        self.sy_lfr_bw = SY_LFR_BW
        self.sy_lfr_sp0 = SY_LFR_SP0
        self.sy_lfr_sp1 = SY_LFR_SP1
        self.sy_lfr_r0 = SY_LFR_R0
        self.sy_lfr_r1 = SY_LFR_R1
        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_LOAD_COMMON_PAR, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_LOAD_COMMON_PAR, \
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
        # SPARE
        parameters.append(0)
        val = 0
        # BW
        val = val + ((self.sy_lfr_bw & 0x1) << 4)
        # SP0
        val = val + ((self.sy_lfr_sp0 & 0x1) << 3)
        # SP1
        val = val + ((self.sy_lfr_sp1 & 0x1) << 2)
        # R0
        val = val + ((self.sy_lfr_r0 & 0x1) << 1)
        # R1
        val = val + ((self.sy_lfr_r1 & 0x1))
        parameters.append(val)
        return parameters

    def printCCSDSPacketInHex(self):
        print("size of the CCSDS packet = " + str(self.ccsdsPacket.__len__()) + " bytes")
        print(self.ccsdsPacket)

    def setSY_LFR_BW(self, sy_lfr_bw):
        self.sy_lfr_bw = sy_lfr_bw
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_SP0(self, sy_lfr_sp0):
        self.sy_lfr_sp0 = sy_lfr_sp0
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_SP1(self, sy_lfr_sp1):
        self.sy_lfr_sp1 = sy_lfr_sp1
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_R0(self, sy_lfr_r0):
        self.sy_lfr_r0 = sy_lfr_r0
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_R1(self, sy_lfr_r1):
        self.sy_lfr_r1 = sy_lfr_r1
        self.ccsdsPacket = self.buildCCSDSPacket()
