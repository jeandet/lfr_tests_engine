# -*- coding: utf-8 -*-
from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *
import struct


class TCLFRUpdateInfo(object):
    """docstring for TCLFRUpdateInfo"""

    def __init__(self, sequence_cnt, source_id):
        super(TCLFRUpdateInfo, self).__init__()
        self.cp_rpw_sc_rw1_f1 = 1.0
        self.cp_rpw_sc_rw1_f2 = 2.0
        self.cp_rpw_sc_rw2_f1 = 3.0
        self.cp_rpw_sc_rw2_f2 = 4.0
        self.cp_rpw_sc_rw3_f1 = 5.0
        self.cp_rpw_sc_rw3_f2 = 6.0
        self.cp_rpw_sc_rw4_f1 = 7.0
        self.cp_rpw_sc_rw4_f2 = 8.0
        self.cp_rpw_sc_rw1_f1_flag = CP_RPW_SC_RW1_F1_FLAG
        self.cp_rpw_sc_rw1_f2_flag = CP_RPW_SC_RW1_F2_FLAG
        self.cp_rpw_sc_rw2_f1_flag = CP_RPW_SC_RW2_F1_FLAG
        self.cp_rpw_sc_rw2_f2_flag = CP_RPW_SC_RW2_F2_FLAG
        self.cp_rpw_sc_rw3_f1_flag = CP_RPW_SC_RW3_F1_FLAG
        self.cp_rpw_sc_rw3_f2_flag = CP_RPW_SC_RW3_F2_FLAG
        self.cp_rpw_sc_rw4_f1_flag = CP_RPW_SC_RW4_F1_FLAG
        self.cp_rpw_sc_rw4_f2_flag = CP_RPW_SC_RW4_F2_FLAG

        self.fillValue = 0
        self.crc = 0
        self.crcGenerator = CRCForLFR()
        self.header = TCLFRHeader(sequence_cnt, \
                                  LENGTH_UPDATE_INFO, \
                                  TYPE_EQ_CONFIGURATION, SUBTYPE_UPDATE_INFO, \
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
        rwfList = [self.cp_rpw_sc_rw1_f1, self.cp_rpw_sc_rw1_f2, self.cp_rpw_sc_rw2_f1, self.cp_rpw_sc_rw2_f2,
                   self.cp_rpw_sc_rw3_f1, self.cp_rpw_sc_rw3_f2, self.cp_rpw_sc_rw4_f1, self.cp_rpw_sc_rw4_f2]
        rwfFlagList = [self.cp_rpw_sc_rw1_f1_flag, self.cp_rpw_sc_rw1_f2_flag, self.cp_rpw_sc_rw2_f1_flag,
                       self.cp_rpw_sc_rw2_f2_flag, self.cp_rpw_sc_rw3_f1_flag, self.cp_rpw_sc_rw3_f2_flag,
                       self.cp_rpw_sc_rw4_f1_flag, self.cp_rpw_sc_rw4_f2_flag]

        # We fill bytes 10-43 with self.fillValue because not relevant
        # for now.
        for i in range(34):
            parameters.append(self.fillValue)

        # cp_rpw_sc_rwx_fx
        for i in range(8):
            aux = self.floatToBytes(rwfList[i])
            parameters.append(aux[0])
            parameters.append(aux[1])
            parameters.append(aux[2])
            parameters.append(aux[3])

        # We fill byte 76 with 0 because spare
        parameters.append(0)

        # cp_rpw_sc_rwx_fx_flag
        stack = 0
        k = 0
        for i in range(7, -1, -1):
            stack = stack + (rwfFlagList[k] << i)
            k = k + 1
        parameters.append(stack)

        # We fill bytes 78-107 with 0 because spare
        for i in range(30):
            parameters.append(0)
        return parameters

    # This method is used to set self.cp_rpw_sc_rw[rw_num]_f[freq_num]
    def setRW_FREQUENCY(self, rw_num, freq_num, freq):
        setattr(self, 'cp_rpw_sc_rw' + str(rw_num) + '_f' + str(freq_num), freq)
        self.ccsdsPacket = self.buildCCSDSPacket()

    def setRW_FLAG(self, rw_num, freq_num, flag):
        setattr(self, 'cp_rpw_sc_rw' + str(rw_num) + '_f' + str(freq_num) + '_flag', flag)
        self.ccsdsPacket = self.buildCCSDSPacket()

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
