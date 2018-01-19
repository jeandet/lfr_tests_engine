from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *


class TCLFRLoadNormalPar(object):
    """docstring for TCLFRLoadNormalPar"""

    def __init__(self, sequence_cnt, source_id):
        super(TCLFRLoadNormalPar, self).__init__()

        self.sy_lfr_n_swf_l = SY_LFR_N_SWF_L
        self.sy_lfr_n_swf_p = SY_LFR_N_SWF_P
        self.sy_lfr_n_asm_p = SY_LFR_N_ASM_P
        self.sy_lfr_n_bp_p0 = SY_LFR_N_BP_P0
        self.sy_lfr_n_bp_p1 = SY_LFR_N_BP_P1
        self.sy_lfr_n_cwf_long_f3 = SY_LFR_N_CWF_LONG_F3
        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_LOAD_NORMAL_PAR, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_LOAD_NORMAL_PAR, \
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
        # SWF_L
        val = (self.sy_lfr_n_swf_l & 0xff00) >> 8;
        parameters.append(val)
        val = (self.sy_lfr_n_swf_l & 0x00ff);
        parameters.append(val)
        # SWF_P
        val = (self.sy_lfr_n_swf_p & 0xff00) >> 8;
        parameters.append(val)
        val = (self.sy_lfr_n_swf_p & 0x00ff);
        parameters.append(val)
        # ASM_P
        val = (self.sy_lfr_n_asm_p & 0xff00) >> 8;
        parameters.append(val)
        val = (self.sy_lfr_n_asm_p & 0x00ff);
        parameters.append(val)
        # BP_P0
        val = (self.sy_lfr_n_bp_p0 & 0xff);
        parameters.append(val)
        # BP_P1
        val = (self.sy_lfr_n_bp_p1 & 0xff);
        parameters.append(val)
        # CWF_LONG_F3
        val = (self.sy_lfr_n_cwf_long_f3 & 0xff);
        parameters.append(val)
        # SPARE
        parameters.append(0)
        return parameters

    def printCCSDSPacketInHex(self):
        print("size of the CCSDS packet = " + str(self.ccsdsPacket.__len__()) + " bytes")
        # for j in range(self.ccsdsPacket.__len__()):
        #	print hex(self.ccsdsPacket[j])
        print(self.ccsdsPacket)

    def setSY_LFR_N_SWF_P(self, sy_lfr_n_swf_p):
        self.sy_lfr_n_swf_p = sy_lfr_n_swf_p
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_N_ASM_P(self, sy_lfr_n_asm_p):
        self.sy_lfr_n_asm_p = sy_lfr_n_asm_p
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_N_CWF_LONG_F3(self, sy_lfr_n_cwf_long_f3):
        self.sy_lfr_n_cwf_long_f3 = sy_lfr_n_cwf_long_f3
        self.ccsdsPacket = self.buildCCSDSPacket()
