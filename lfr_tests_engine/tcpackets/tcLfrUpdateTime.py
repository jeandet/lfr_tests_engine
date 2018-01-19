from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *


class TCLFRUpdateTime(object):
    """docstring for TCLFRUpdateTime"""

    def __init__(self, sequence_cnt, source_id, cp_rpw_time):
        super(TCLFRUpdateTime, self).__init__()

        self.cp_rpw_time = cp_rpw_time
        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_UPDATE_TIME, \
                                  TYPE_TIME_MANAGEMENT, SUBTYPE_UPDATE_TIME, \
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
        # CP_RPW_TIME
        val = (self.cp_rpw_time & 0x0000ff000000) >> 24;
        parameters.append(val)
        val = (self.cp_rpw_time & 0x000000ff0000) >> 16;
        parameters.append(val)
        val = (self.cp_rpw_time & 0x00000000ff00) >> 8;
        parameters.append(val)
        val = (self.cp_rpw_time & 0x0000000000ff);
        parameters.append(val)
        parameters.append(0x00)  # fineTime set to 0
        parameters.append(0x00)  # fineTime set to 0
        return parameters

    def printCCSDSPacketInHex(self):
        print("size of the CCSDS packet = " + str(self.ccsdsPacket.__len__()) + " bytes")
        # for j in range(self.ccsdsPacket.__len__()):
        #	print hex(self.ccsdsPacket[j])
        print(self.ccsdsPacket)

    def setCP_RPW_TIME(self, cp_rpw_time):
        self.cp_rpw_time = cp_rpw_time
        self.ccsdsPacket = self.buildCCSDSPacket()
