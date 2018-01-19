from .constants import *


class TCLFRHeader(object):
    """docstring for TCLFRHeader"""

    def __init__(self, sequence_cnt, packet_length, \
                 service_type, service_subtype, \
                 source_id):
        super(TCLFRHeader, self).__init__()
        # PACKET_HEADER
        self.ccsds_version_number = CCSDS_VERSION_NUMBER
        self.packet_type = TC_PACKET
        self.data_field_header_flag = WITH_HEADER
        self.process_id = RPW_PID_2
        self.packet_category = PRIVATE_SCIENCE_OR_TELECOMMAND
        self.segmentation_grouping_flag = STANDALONE_PACKET
        self.sequence_cnt = sequence_cnt
        self.packet_length = packet_length
        # PACKET_DATA_FIELD
        self.ccsds_secondary_header_flag = 0
        self.pus_version = PUS_VERSION
        self.ack_execution_completion = 0
        self.ack_execution_progress = 0
        self.ack_execution_start = 0
        self.ack_acceptance = 0
        self.service_type = service_type
        self.service_subtype = service_subtype
        self.source_id = source_id

        self.tcHeader = []
        self.buildTCHeader();

    def buildTCHeader(self):
        val = self.ccsds_version_number << 5
        val = val + (self.packet_type << 4)
        val = val + (self.data_field_header_flag << 3)
        val = val + (self.process_id >> 4)
        self.tcHeader.append(val)  # Byte 0

        val = (self.process_id & 0x0f) << 4
        val = val + (self.packet_category & 0x0f)
        self.tcHeader.append(val)  # Byte 1

        val = (self.segmentation_grouping_flag & 0xc0) << 6
        val = val + ((self.sequence_cnt & 0x3f00) >> 8)
        self.tcHeader.append(val)  # Byte 2

        val = (self.sequence_cnt & 0x00ff)
        self.tcHeader.append(val)  # Byte 3

        # PACKET_LENGTH
        val = (self.packet_length & 0xff00) >> 8
        self.tcHeader.append(val)  # Byte 4
        val = (self.packet_length & 0x00ff)
        self.tcHeader.append(val)  # Byte 5

        val = (self.ccsds_secondary_header_flag & 0x80) << 7
        val = val + ((self.pus_version & 0x07) << 4)
        val = val + ((self.ack_execution_completion) << 3)
        val = val + ((self.ack_execution_progress) << 2)
        val = val + ((self.ack_execution_start) << 1)
        val = val + (self.ack_acceptance)
        self.tcHeader.append(val)  # Byte 6

        # SERVICE_TYPE
        self.tcHeader.append(self.service_type)  # Byte 7

        # SERVICE_SUBTYPE
        self.tcHeader.append(self.service_subtype)  # Byte 8

        # SOURCE_ID
        self.tcHeader.append(self.source_id)  # Byte 9
