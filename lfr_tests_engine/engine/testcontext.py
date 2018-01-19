import jsonpickle
from ..tcpackets.constants import *
import datetime

'''
    LFR_Mode=
'''


class TestStep(object):
    def __init__(self, delta=24, values={}):
        self.delta = delta
        self.inputValues = values

    def __str__(self):
        return str("delta:%d" % self.delta) + str(self.inputValues)


class TestContextInput(object):
    def __init__(self):
        self.LFRMode = NORMAL
        self.TestSteps = []
        self.TestScrip = ""
        self.TestMod = ""
        self.TestDelayBeforeExit = 24
        self.TestDelayBeforeStart = 12
        self.TgSW = "/opt/LFR/TIMEGEN/0.0.0.1/timegen"
        self.TgSpwLink = 2
        self.BootTg = False
        self.FSW = "/opt/LFR/LFR-FSW/3.0.0.22/fsw"
        self.LFRSpwLink = 1
        self.BootLFR = True
        self.RecordRawPackets = True
        self.RoutingPar = [0, 0, 0]
        self.ShapingPar = [0, 0]
        self.BiasWorkPar = 1
        self.ASM_P = 3600
        self.SWF_P = 300
        self.SWF_L = 2048
        self.LongF3 = 0
        self.QuitAfterTest = True
        self.values = {}

    def save(self, file):
        file = open(file, "w")
        file.write(jsonpickle.encode(self))
        file.close()


class TestContextOutput(object):
    def __init__(self, input):
        self.Input = input
        self.OutputFiles = []
        self.Exeptions = []
        self.StartDate = datetime.datetime.now()
        self.TestStepsResults = []
        self.TestResult = "Failed"
        self.StopDate = datetime.datetime.now()

    def save(self, file):
        file = open(file, "w")
        file.write(jsonpickle.encode(self))
        file.close()


def TestContextInputFromFile(file):
    F = open(file, "r")
    inputContext = jsonpickle.decode(F.read())
    F.close()
    return inputContext


def TestContextOutputFromFile(file):
    F = open(file, "r")
    outputContext = jsonpickle.decode(F.read())
    F.close()
    return outputContext
