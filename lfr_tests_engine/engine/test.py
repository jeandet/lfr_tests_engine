from .testcontext import *
from .test_common import *
import glob
import __main__

class LFRTest(object):
    def __init__(self, InputContext):
        self.InputContext = InputContext
        self.OutputContext = TestContextOutput(self.InputContext)
        self.OutputContext.T0 = time.time()
        self.OutputContext.T1 = time.time()
        self.OutputContext.T2 = time.time()
        self.OutputContext.T3 = []
        self.OutputContext.T4 = time.time()

    def beforeTest(self):
        self.T1 = time.time()
        __main__.proxy.loadSysDriver("SpwPlugin", "SpwPlugin0")
        self.OutputContext.StartDate = datetime.datetime.now()
        self.PacketList0 = glob.glob(PacketFolder+"/*.data")
        if self.InputContext.BootTg :
            setupTimegen(self.InputContext.TgSpwLink)
            bootTimegen(self.InputContext.TgSW)
        self.soc = setupLFR(self.InputContext.LFRSpwLink,self.InputContext.BootTg)
        if self.InputContext.BootLFR :
            bootLFR (self.InputContext.FSW, self.InputContext.BootTg)
            self.soc.activeWait(2)
        autoEnterMode(self.InputContext, self.soc)
        if self.InputContext.RecordRawPackets :
            __main__.LFRControlPlugin0.storePacketsRAW(True)
            __main__.LFRControlPlugin0.logPackets(True)
        self.OutputContext.T2 = time.time()
        self.soc.activeWait(self.InputContext.TestDelayBeforeStart)

    def run(self, step):
        pass

    def afterTest(self):
        self.soc.activeWait(self.InputContext. TestDelayBeforeExit)
        if self.InputContext.RecordRawPackets :
            __main__.LFRControlPlugin0.storePacketsRAW(False)
            __main__.LFRControlPlugin0.logPackets(False)
        if self.InputContext.BootLFR:
            killLFR(self.InputContext.LFRSpwLink)
        if self.InputContext.BootTg:
            killTimegen(self.InputContext.TgSpwLink)
        self.OutputContext.StopDate = datetime.datetime.now()
        self.PacketList1 = glob.glob(PacketFolder+"/*.data")
        self.AddedFiles = listDiff(self.PacketList0, self.PacketList1)
        self.OutputContext.OutputFiles = listDiff(self.PacketList0, self.PacketList1)
        __main__.SpwPlugin0.disconnectBridge()
        __main__.proxy.closeSysDriver("SpwPlugin0")
