from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *


class TCLFRCalDisable(object):
    """docstring for TCLFRCalDisable"""

    def __init__(self, sequence_cnt, source_id):
        super(TCLFRCalDisable, self).__init__()

        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_DIS_CAL, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_DIS_CAL, \
                                  source_id).tcHeader;

        self.ccsdsPacket = self.buildCCSDSPacket()

    def buildCCSDSPacket(self):
        packet = self.header
        (ChkMSB, ChkLSB) = self.crcGenerator.GetCRCAsTwoBytes(packet);
        packet.append(ChkMSB)
        packet.append(ChkLSB)
        return packet
