class CRCForLFR(object):
    """docstring for CRCForLFR"""

    def __init__(self):
        super(CRCForLFR, self).__init__()
        self.table = self.InitLtbl()

    def InitLtbl(self):
        table = []
        for i in range(256):
            tmp = 0
            if (i & 1) != 0: tmp = tmp ^ 0x1021
            if (i & 2) != 0: tmp = tmp ^ 0x2042
            if (i & 4) != 0: tmp = tmp ^ 0x4084
            if (i & 8) != 0: tmp = tmp ^ 0x8108
            if (i & 16) != 0: tmp = tmp ^ 0x1231
            if (i & 32) != 0: tmp = tmp ^ 0x2462
            if (i & 64) != 0: tmp = tmp ^ 0x48c4
            if (i & 128) != 0: tmp = tmp ^ 0x9188
            table.append(tmp)
        return table

    def Crc_opt(self, D, Chk, table):
        return ( \
                ((Chk << 8) & 0xff00) ^ table[(((Chk >> 8) ^ D) & 0x00ff)] \
            )

    def GetCRCAsTwoBytes(self, indata):
        Chk = 0xffff;  # reset syndrom to all ones
        for j in range(indata.__len__()):
            Chk = self.Crc_opt(indata[j], Chk, self.table)
        ChkMSB = (Chk & 0xff00) >> 8
        ChkLSB = (Chk & 0x00ff)
        return (ChkMSB, ChkLSB)
