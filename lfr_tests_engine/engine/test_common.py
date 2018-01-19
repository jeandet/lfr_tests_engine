#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import __main__
from ..tcpackets import telecommands as tc
from ..tcpackets.constants import *
from ..common import socfunctions
from .testcontext import *
from .. import config as _cfg
import datetime


__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2016, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Production"


try:
    # for Python2
    import Tkinter as tk
    import tkFileDialog as filedialog
except:
    # for Python3
    import tkinter as tk
    from tkinter import filedialog


if  _cfg.has_key("GLOBAL", "PacketFolder"):
    PacketFolder = _cfg.get_value("GLOBAL", "PacketFolder")
else:
    dir = filedialog.askdirectory()
    if dir == "":
        raise ValueError("No directory")
    else:
        PacketFolder = _cfg.set_value("GLOBAL", "PacketFolder", dir)

LFR_Fs0 = 24576
LFR_Fs1 = 4096
LFR_Fs2 = 256
LFR_Fs3 = 16
LFR_Fs = [LFR_Fs0, LFR_Fs1, LFR_Fs2, LFR_Fs3]

def listDiff(list1, list2):
    res = []
    for i in list1:
        if list2.count(i) == 0:
            res.append(i)
    for i in list2:
        if list1.count(i) == 0:
            res.append(i)
    return res

# triggerMode is 0 for 'custom' or 1 for 'tickout'
def bootTimegen(tg="/opt/LFR/TIMEGEN/0.0.0.1/timegen",triggerMode=1):
    print("Uploading and booting Timegen...")
    __main__.dsu3plugin0.openFile(tg)
    __main__.dsu3plugin0.loadFile()
    __main__.dsu3plugin0.run()
    print("Timecodes period set to 1Hz...")
    __main__.SpwPlugin0.StarDundeeStartTimecodes( 1 )
    __main__.SpwPlugin0.disconnectBridge()
    __main__.SpwPlugin0.Write(0x80000c00,[triggerMode])
    print("Timegen is running... Spw plugin will be unloaded in 2s.")
    time.sleep(2)
    __main__.proxy.closeSysDriver("SpwPlugin0")
    time.sleep(1)

def setupTimegen(linkNumber=2):
    __main__.proxy.loadSysDriver("SpwPlugin","SpwPlugin0")
    __main__.SpwPlugin0.selectBridge("STAR-Dundee Spw USB Brick")
    __main__.proxy.loadSysDriverToParent("dsu3plugin","SpwPlugin0")
    availableBrickCount = __main__.SpwPlugin0.StarDundeeGetAvailableBrickCount()
    print(str(availableBrickCount) + " SpaceWire brick(s) found")
    time.sleep(1)
    __main__.SpwPlugin0.StarDundeeSelectBrick(1)
    __main__.SpwPlugin0.StarDundeeSetBrickAsARouter(1)
    __main__.SpwPlugin0.StarDundeeSelectLinkNumber( linkNumber )
    time.sleep(1)
    print("Connecting to TIMEGEN device...")
    __main__.SpwPlugin0.connectBridge()
    time.sleep(1)

def killTimegen(linkNumber=2):
    __main__.proxy.closeSysDriver("SpwPlugin0")
    time.sleep(1)
    __main__.proxy.loadSysDriver("SpwPlugin", "SpwPlugin0")
    __main__.proxy.loadSysDriverToParent("dsu3plugin", "SpwPlugin0")
    __main__.SpwPlugin0.selectBridge("STAR-Dundee Spw USB Brick")
    availableBrickCount = __main__.SpwPlugin0.StarDundeeGetAvailableBrickCount()
    print(str(availableBrickCount) + " SpaceWire brick(s) found")
    time.sleep(1)
    __main__.SpwPlugin0.StarDundeeSelectBrick(1)
    __main__.SpwPlugin0.StarDundeeSetBrickAsARouter(1)
    time.sleep(1)
    __main__.SpwPlugin0.StarDundeeSelectLinkNumber( linkNumber )
    __main__.SpwPlugin0.connectBridge()
    __main__.dsu3plugin0.stop()
    __main__.dsu3plugin0.cacheDisable()
    time.sleep(1)

def killLFR(linkNumber=1):
    __main__.dsu3plugin0.stop()
    __main__.dsu3plugin0.cacheDisable()

def bootLFR(fsw="/opt/LFR/LFR-FSW/3.0.0.22/fsw", AutoLocalTime=True):
    if not os.path.exists(fsw):
        raise IOException('File does not exist: %s' % fsw)
    __main__.dsu3plugin0.openFile(fsw)
    __main__.dsu3plugin0.loadFile()
    __main__.dsu3plugin0.run()
    if AutoLocalTime:
        time.sleep(1)
# Might not Work!
        __main__.settimegen.setTimeGenAutoSoc()
        time.sleep(1)

def setupLFR(linkNumber=1, timecodes=False, delta_timescodes_ms=100):
    __main__.proxy.loadSysDriver("SpwPlugin", "SpwPlugin0")
    __main__.SpwPlugin0.selectBridge("STAR-Dundee Spw USB Brick")
    __main__.proxy.loadSysDriverToParent("dsu3plugin","dsu3plugin0", "SpwPlugin0")
    __main__.proxy.loadSysDriverToParent("LFRControlPlugin","LFRControlPlugin0", "SpwPlugin0")
    availableBrickCount = __main__.SpwPlugin0.StarDundeeGetAvailableBrickCount()
    print(str(availableBrickCount) + " SpaceWire brick(s) found")
    __main__.SpwPlugin0.StarDundeeSelectBrick(1)
    __main__.SpwPlugin0.StarDundeeSetBrickAsARouter(1)
    __main__.SpwPlugin0.StarDundeeSelectLinkNumber(linkNumber)
    __main__.SpwPlugin0.connectBridge()
    if timecodes:
        print("Timecodes period set to 1Hz...")
        __main__.SpwPlugin0.StarDundeeStartTimecodes(0)
        while round(datetime.datetime.now().microsecond/10000)!=round(delta_timescodes_ms/10):
            pass
        __main__.SpwPlugin0.StarDundeeStartTimecodes(1)
    __main__.SpwPlugin0.TCPServerConnect()
    __main__.LFRControlPlugin0.TCPServerConnect()
    __main__.LFRControlPlugin0.TMEchoBridgeOpenPort()

    return socfunctions.SocFunctions(__main__.LFRControlPlugin0, __main__.SpwPlugin0 )

def loadCommonPar(inputContext, soc):
    tc_load_common_par = tc.TCLFRLoadCommonPar(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL)
    tc_load_common_par.setSY_LFR_BW(inputContext.BiasWorkPar)
    tc_load_common_par.setSY_LFR_SP0(inputContext.ShapingPar[0])
    tc_load_common_par.setSY_LFR_SP1(inputContext.ShapingPar[1])
    tc_load_common_par.setSY_LFR_R0(inputContext.RoutingPar[0])
    tc_load_common_par.setSY_LFR_R1(inputContext.RoutingPar[1])
    tc_load_common_par.setSY_LFR_R2(inputContext.RoutingPar[2])
    soc.sendTC(tc_load_common_par)

def loadNormalPar(inputContext, soc):
    tc_load_normal_par = tc.TCLFRLoadNormalPar(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL)
    tc_load_normal_par.setSY_LFR_N_ASM_P(inputContext.ASM_P)
    tc_load_normal_par.setSY_LFR_N_SWF_P(inputContext.SWF_P)
    tc_load_normal_par.setSY_LFR_N_CWF_LONG_F3(inputContext.LongF3)
    soc.sendTC(tc_load_normal_par)

def loadFilterPar(inputContext, soc):
    tc_load_filter_par = tc.TCLFRLoadFilterPar(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL)
    soc.sendTC(tc_load_filter_par)

def updateInfo(inputContext, soc):
    tc_update_info = tc.TCLFRUpdateInfo(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL)
    soc.sendTC(tc_update_info)

def enterNormalMode(soc, inputContext):
    tc_enter_mode = tc.TCLFREnterMode(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, NORMAL, 0)
    soc.sendTC(tc_enter_mode)

def enterStandbyMode(soc, inputContext):
    tc_enter_mode = tc.TCLFREnterMode(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, STANDBY, 0)
    soc.sendTC(tc_enter_mode)

def enterSBM1Mode(soc, inputContext):
    tc_enter_mode = tc.TCLFREnterMode(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, SBM1, 0)
    soc.sendTC(tc_enter_mode)


def enterSBM2Mode(soc, inputContext):
    tc_enter_mode = tc.TCLFREnterMode(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL, SBM2, 0)
    soc.sendTC(tc_enter_mode)


def dumpPar(soc):
    tc_dump_par = tc.TCLFRDumpPar(DEFAULT_SEQUENCE_COUNT, RPW_INTERNAL)
    soc.sendTC(tc_dump_par)


__autoMode__ = {STANDBY:enterStandbyMode,
                NORMAL:enterNormalMode,
                SBM1:enterSBM1Mode,
                SBM2:enterSBM2Mode}


def autoEnterMode(inputContext, soc):
    if inputContext.LFRMode != None:
        loadNormalPar(inputContext, soc)
        loadCommonPar(inputContext, soc)
        __autoMode__[inputContext.LFRMode](soc, inputContext)


def saveWidget(widget,  file,  size = __main__.QtCore.QSize(0, 0)):
    if size.width() == 0:
        size = widget.size
    else:
        widget.setFloating(True)
        widget.resize(size)
    pix = __main__.QtGui.QPixmap(size)
    widget.render(pix)
    if widget.floating:
        widget.setFloating(False)
    pix.save(file)

