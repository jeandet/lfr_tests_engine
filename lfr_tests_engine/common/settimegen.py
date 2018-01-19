from ..tcpackets import telecommands as tc
from ..tcpackets.constants import *

from . import general_functions as gen


def setTimeGen(soc, local_time=-1):
    # flush the transmission before changing the spacewire link
    soc.flushTCTransmission()
    soc.setSpaceWireLink(2)

    # get the local time with the following reference date: Jan 01 2000
    if local_time == -1:
        local_time = gen.getLocalTimeInDPUFormat()

    # build the TC that will be sent to the timegen system
    tc_update_time = tc.TCLFRUpdateTime(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, local_time)

    # send the local time to the system time generator
    soc.sendTC(tc_update_time)

    # flush the transmission before changing the spacewire link
    soc.flushTCTransmission()
    soc.setSpaceWireLink(1)


def setTimeGenAutoSoc(local_time=-1):
    # TODO remove this shit
    from __main__ import LFRControlPlugin0
    from __main__ import SpwPlugin0

    soc = socfunctions.SocFunctions(LFRControlPlugin0, SpwPlugin0)

    # flush the transmission before changing the spacewire link
    soc.flushTCTransmission()
    soc.setSpaceWireLink(2)

    # get the local time with the following reference date: Jan 01 2000
    if local_time == -1:
        local_time = gen.getLocalTimeInDPUFormat()

    # build the TC that will be sent to the timegen system
    tc_update_time = tc.TCLFRUpdateTime(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, local_time)

    # send the local time to the system time generator
    soc.sendTC(tc_update_time)

    # flush the transmission before changing the spacewire link
    soc.flushTCTransmission()
    soc.setSpaceWireLink(1)


def configureTrigger(soc, trigger_time=0):
    # flush the transmission before changing the spacewire link
    soc.flushTCTransmission()
    soc.setSpaceWireLink(2)

    # get the local time with the following reference date: Jan 01 2000
    local_time = gen.getLocalTimeInDPUFormat()
    if trigger_time == 0:
        trigger_time = gen.getLocalTimeInDPUFormat() + 5

    # build the TC that will be sent to the timegen system

    tc_update_time = tc.TCLFRUpdateTime(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, local_time)
    tc_enter_mode = tc.TCLFREnterMode(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, STANDBY, trigger_time)

    # send the telecommand to timegen
    soc.sendTC(tc_enter_mode)

    # flush the transmission before changing the spacewire link
    soc.flushTCTransmission()
    soc.setSpaceWireLink(1)


if __name__ == '__main__':
    from ..common import socfunctions

    # create a SocFunction object to access SocEplorer
    soc = socfunctions.SocFunctions(LFRControlPlugin0, SpwPlugin0)

    setTimeGen(0xaaaabbbb)
# configureTrigger( soc )
