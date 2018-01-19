from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *
import struct


class TCLFRLoadKCoefficients(object):
    """docstring for TCLFRLoadKCoefficients"""

    def __init__(self, sequence_cnt, source_id, freq=0, defaultValue=1.0):
        super(TCLFRLoadKCoefficients, self).__init__()

        self.sy_lfr_kcoeff_frequency = freq
        self.defaultValue = defaultValue
        self.crc = 0

        self.crcGenerator = CRCForLFR()

        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_LOAD_KCOEFFICIENTS, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_LOAD_KCOEFFICIENTS, \
                                  source_id).tcHeader;

        self.kCoeffTable = self.initKCoeffTable(self.defaultValue)

        self.ccsdsPacket = self.buildCCSDSPacket()

    def initKCoeffTable(self, defaultValue):
        kCoeffTable = []
        for freq in range(36):
            vect = []
            for k in range(32):
                vect.append(defaultValue)
            kCoeffTable.append(vect)
        return kCoeffTable

    def resetKCoeffTable(self, defaultValue):
        kCoeffTable = []
        for freq in range(36):
            vect = []
            for k in range(32):
                vect.append(defaultValue)
            kCoeffTable.append(vect)
        self.kCoeffTable = kCoeffTable
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_KCOEFF_FREQUENCY(self, freq):
        self.sy_lfr_kcoeff_frequency = freq
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setSY_LFR_KCOEFF(self, freq, coeff, value):
        self.kCoeffTable[freq][coeff] = float(value)
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
        # sy_lfr_kcoeff_frequency
        val = (self.sy_lfr_kcoeff_frequency & 0xff00) >> 8;
        parameters.append(val)
        val = (self.sy_lfr_kcoeff_frequency & 0x00ff);
        parameters.append(val)
        # sy_lfr_kcoeff_
        for k in range(32):
            # val = 1. / (k+1)
            val = self.kCoeffTable[self.sy_lfr_kcoeff_frequency][k]
            aux = self.floatToBytes(val)
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


if __name__ == "__main__":
    packet = TCLFRLoadKCoefficients(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, 1, 1.0)
    # packet.printCCSDSPacketInHex()

    print("kCoeffTable")
    print(packet.kCoeffTable)
    packet.setKCoeff(0, 2, 100)
    print(packet.kCoeffTable)
