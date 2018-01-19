from .constants import *
from .tcLfrHeader import *
from .crcForLFR import *

class TCLFRLoadFbinsMask(object):
	"""docstring for TCLFRLoadFbinsMask"""
	def __init__(self, sequence_cnt, source_id, defaultValue = 0xff):
		super(TCLFRLoadFbinsMask, self).__init__()

		self.crc = 0

		self.crcGenerator = CRCForLFR()

		self.header = TCLFRHeader( sequence_cnt, \
				LENGTH_LOAD_FBINS_MASK, \
				TYPE_EQ_CONFIGURATION, SUBTYPE_LOAD_FBINS_MASK, \
				source_id).tcHeader;

		self.ccsdsPacket = self.buildCCSDSPacket( defaultValue )

	def buildCCSDSPacket(self, defaultValue):
		parameters	= self.buildTCParameters( defaultValue );
		packet 		= self.header + parameters
		(ChkMSB, ChkLSB) = self.crcGenerator.GetCRCAsTwoBytes( packet );
		packet.append( ChkMSB )
		packet.append( ChkLSB )
		return packet

	def updateCCSDSPacket(self):
		packet 		= self.ccsdsPacket
		packet.pop()
		packet.pop()
		(ChkMSB, ChkLSB) = self.crcGenerator.GetCRCAsTwoBytes( packet );
		packet.append( ChkMSB )
		packet.append( ChkLSB )
		return packet

	def buildTCParameters(self, defaultValue):
		parameters = []
		# sy_lfr_fbins
		for k in range( 12 * 4 ):
			parameters.append( defaultValue )
		return parameters

	def setSY_LFR_FBINS(self, fChannel, word, byte0, byte1, byte2, byte3):
		self.ccsdsPacket[ 10 + fChannel * 16 + word * 4 + 0 ] = byte0;
		self.ccsdsPacket[ 10 + fChannel * 16 + word * 4 + 1 ] = byte1;
		self.ccsdsPacket[ 10 + fChannel * 16 + word * 4 + 2 ] = byte2;
		self.ccsdsPacket[ 10 + fChannel * 16 + word * 4 + 3 ] = byte3;
		self.updateCCSDSPacket()

	def printCCSDSPacketInHex(self):
		print( "size of the CCSDS packet = " + str(self.ccsdsPacket.__len__()) + " bytes")
		print( self.ccsdsPacket)

if __name__ == "__main__":
	packet = TCLFRLoadFbinsMask( DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, 0xff )
	packet.printCCSDSPacketInHex()
	packet.setSY_LFR_FBINS(0, 0, 0x10, 0x20, 0x30, 0x40)
	packet.setSY_LFR_FBINS(1, 0, 0x50, 0x60, 0x70, 0x80)
	packet.printCCSDSPacketInHex()
