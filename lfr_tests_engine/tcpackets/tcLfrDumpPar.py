from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *


class TCLFRDumpPar(object):
    """docstring for TCLFRDumpPar"""

    def __init__(self, sequence_cnt, source_id):
        super(TCLFRDumpPar, self).__init__()

        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_DUMP_PAR, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_DUMP_PAR, \
                                  source_id).tcHeader;

        self.ccsdsPacket = self.buildCCSDSPacket()

    def buildCCSDSPacket(self):
        packet = self.header
        (ChkMSB, ChkLSB) = self.crcGenerator.GetCRCAsTwoBytes(packet);
        packet.append(ChkMSB)
        packet.append(ChkLSB)
        return packet
