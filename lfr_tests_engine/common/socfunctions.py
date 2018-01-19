from ..tcpackets.constants import *
import time


class SocFunctions(object):
    """docstring for SocFunctions"""

    def __init__(self, lfrControlPlugin, spwPlugin):
        super(SocFunctions, self).__init__()
        self.lfrControlPlugin = lfrControlPlugin
        self.spwPlugin = spwPlugin

    def sendTC(self, telecommand):
        ccsdsPacket = telecommand.ccsdsPacket
        targetLogicalAddress = [TARGET_LOGICAL_ADDRESS]
        protocoleIdentifier = [PROTOCOLE_IDENTIFIER_CCSDS]
        reserved = [RESERVED_DEFAULT]
        userApplication = [USER_APPLICATION]
        ccsdsPacket = targetLogicalAddress + protocoleIdentifier \
                      + reserved + userApplication \
                      + ccsdsPacket

        self.lfrControlPlugin.WriteSPW(ccsdsPacket)

    def flushTCTransmission(self):
        spwTransmitted = self.spwPlugin.StarDundeeGetNbCCSDSPacketsTransmittedToSpw()
        lfrControlTransmitted = self.lfrControlPlugin.getNbTransmittedPackets()
        timeOut = 1.
        localTime = time.time()
        stopTime = time.time() + timeOut
        while (lfrControlTransmitted != spwTransmitted) and (localTime < stopTime):
            self.lfrControlPlugin.ProcessPendingEvents()
            spwTransmitted = self.spwPlugin.StarDundeeGetNbCCSDSPacketsTransmittedToSpw()
            lfrControlTransmitted = self.lfrControlPlugin.getNbTransmittedPackets()
            localTime = time.time()
        if lfrControlTransmitted != spwTransmitted:
            print
            "timeout (" + str(timeOut) + " s) error in flushTCTransmission"

    def activeWait(self, timeToWait):
        localTime = time.time()
        stopTime = time.time() + timeToWait
        while (localTime < stopTime):
            self.lfrControlPlugin.ProcessPendingEvents()
            localTime = time.time()
        return 0

    def setSpaceWireLink(self, link):
        timeOut = 1.
        localTime = time.time()
        stopTime = time.time() + timeOut
        self.spwPlugin.StarDundeeSelectLinkNumber(link)
        linkNumber = self.spwPlugin.StarDundeeGetLinkNumber()
        while (linkNumber != link) and (localTime < stopTime):
            self.lfrControlPlugin.ProcessPendingEvents()
            linkNumber = self.spwPlugin.StarDundeeGetLinkNumber()
            localTime = time.time()
        if linkNumber != link:
            print
            "timeout error in setSpaceWireLink, link is " + str(linkNumber) + " instead of " + str(link)

    def getLFRControlPluginVersion(self):
        return self.lfrControlPlugin.getSoftwareVersion()

    def generatePDF(self, doc, filename):
        self.lfrControlPlugin.generatePDFFromQTextDocument(doc, filename)

    def getVHDLVersion(self):
        value = self.spwPlugin.Read(0x80000ff0, 1)[0]
        value1 = (value & 0x00ff0000) >> 16
        value2 = (value & 0x0000ff00) >> 8
        value3 = (value & 0x000000ff)
        return str(value1) + '.' + str(value2) + '.' + str(value3)
