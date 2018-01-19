from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *
import struct


class TCLFRLoadFilterPar(object):
    """docstring for TCLFRLoadFilterPar"""

    def __init__(self, sequence_cnt, source_id):
        super(TCLFRLoadFilterPar, self).__init__()
        self.sy_lfr_pas_filter_enabled = SY_LFR_PAS_FILTER_ENABLED
        self.sy_lfr_pas_filter_modulus = SY_LFR_PAS_FILTER_MODULUS
        self.sy_lfr_pas_filter_tbad = SY_LFR_PAS_FILTER_TBAD
        self.sy_lfr_pas_filter_offset = SY_LFR_PAS_FILTER_OFFSET
        self.sy_lfr_pas_filter_shift = SY_LFR_PAS_FILTER_SHIFT
        self.sy_lfr_sc_rw_delta_f = SY_LFR_SC_RW_DELTA_F
        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_LOAD_FILTER_PAR, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_LOAD_FILTER_PAR, \
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
        # SPARE8_2
        parameters.append(0)
        val = 0
        # 7-bitbit spare + SY_LFR_PAS_FILTER_ENABLED
        val = val + (self.sy_lfr_pas_filter_enabled & 0x1)
        parameters.append(val)
        # SY_LFR_PAS_FILTER_MODULUS
        parameters.append(self.sy_lfr_pas_filter_modulus)
        # SY_LFR_PAS_FILTER_TBAD
        aux = self.floatToBytes(float(self.sy_lfr_pas_filter_tbad))
        parameters.append(aux[0])
        parameters.append(aux[1])
        parameters.append(aux[2])
        parameters.append(aux[3])
        # SY_LFR_PAS_FILTER_OFFSET
        parameters.append(self.sy_lfr_pas_filter_offset)
        # SY_LFR_PAS_FILTER_SHIFT
        aux = self.floatToBytes(float(self.sy_lfr_pas_filter_shift))
        parameters.append(aux[0])
        parameters.append(aux[1])
        parameters.append(aux[2])
        parameters.append(aux[3])
        # SY_LFR_SC_RW_DELTA_F
        aux = self.floatToBytes(float(self.sy_lfr_sc_rw_delta_f))
        parameters.append(aux[0])
        parameters.append(aux[1])
        parameters.append(aux[2])
        parameters.append(aux[3])
        return parameters

    def floatToBytes(self, val):
        # /!\ WARNING Python 2 vs Python3:
        # in Python2 struct.pack() returns strings
        # so we have to ord() values in order to return intergers.
        # In Python3 struct.pack() returns bytes so ord() call
        # should been removed from this method.

        aux = struct.pack('f', val)
        return (ord(aux[3]), ord(aux[2]), ord(aux[1]), ord(aux[0]))

    def printCCSDSPacketInHex(self):
        print("size of the CCSDS packet = " + str(self.ccsdsPacket.__len__()) + " bytes")
        print(self.ccsdsPacket)

    def setSY_LFR_PAS_FILTER_ENABLED(self, sy_lfr_pas_filter_enabled):
        self.sy_lfr_pas_filter_enabled = sy_lfr_pas_filter_enabled
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_PAS_FILTER_MODULUS(self, sy_lfr_pas_filter_modulus):
        self.sy_lfr_pas_filter_modulus = sy_lfr_pas_filter_modulus
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_PAS_FILTER_TBAD(self, sy_lfr_pas_filter_tbad):
        self.sy_lfr_pas_filter_tbad = sy_lfr_pas_filter_tbad
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_PAS_FILTER_OFFSET(self, sy_lfr_pas_filter_offset):
        self.sy_lfr_pas_filter_offset = sy_lfr_pas_filter_offset
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_PAS_FILTER_SHIFT(self, sy_lfr_pas_filter_shift):
        self.sy_lfr_pas_filter_shift = sy_lfr_pas_filter_shift
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_SC_RW_DELTA_F(self, sy_lfr_sc_rw_delta_f):
        self.sy_lfr_sc_rw_delta_f = sy_lfr_sc_rw_delta_f
        self.ccsdsPacket = self.buildCCSDSPacket()
