import pandas as pds
import numpy as np
import sys
import os
import path
import glob
import datetime
from tabipy import Table, TableHeaderRow, TableCell
from IPython.display import display
from .testcontext import *
from .. import config as _cfg

class ResultLoader(object):
    def __init__(self, result_file, overhide_path=None):
        self._notebook = False
        self.OutputContext = TestContextOutputFromFile(result_file)
        self.PacketsRecords = []
        self.PacketsLogs = []
        self.Products = {}
        self.asmSz = [88, 104, 96]
        self.asmRng = {
            'F0': np.arange(1632, 9985, 96),
            'F1': np.arange(96, 1745, 16),
            'F2': np.arange(7, 103, 1)
        }

        for file in self.OutputContext.OutputFiles:
            if file.count("_record.data"):
                if overhide_path is None:
                    self.PacketsRecords.append(file)
                else:
                    self.PacketsRecords.append(overhide_path + "/" + os.path.basename(file))
            else:
                if file.count("_log.data"):
                    if overhide_path is None:
                        self.PacketsLogs.append(file)
                    else:
                        self.PacketsLogs.append(overhide_path + "/" + os.path.basename(file))

    def enable_notebook(self, enable=True):
        self._notebook = enable

    def displayTestConditions(self):
        t = Table(TableHeaderRow('Parameter', 'Value'))
        t.append_row(("Start date", self.OutputContext.StartDate))
        t.append_row(("Stop date", self.OutputContext.StopDate))
        t.append_row(("Test duration", self.OutputContext.StopDate - self.OutputContext.StartDate))
        t.append_row(("Produced files", ""))
        for outf in self.OutputContext.OutputFiles:
            t.append_row(("", outf))
        t.append_row(("Test result", self.OutputContext.TestResult))
        t.append_row(("LFR is booted", self.OutputContext.Input.BootLFR))
        t.append_row(("FSW", self.OutputContext.Input.FSW))
        t.append_row(("BIAS", self.OutputContext.Input.BiasWorkPar))
        t.append_row(("Routing", self.OutputContext.Input.RoutingPar))
        t.append_row(("Shaping", self.OutputContext.Input.ShapingPar))
        if self._notebook:
            display(t)
        else:
            return t

    def decomutePackets(self, force=True, debug=0):
        for file in self.PacketsRecords:
            # create the subdirectory /decom of the binary file directory
            # where the ascii decommuted files can be stored
            if not os.path.exists(os.path.dirname(file)+'/decom'):
                os.mkdir(os.path.dirname(file)+'/decom')
            os.chdir(path.path(file).dirname()+'/decom')
            basename_search = os.path.basename(file).replace(".data", ".sum")
            file_search = os.path.dirname(file) + '/decom/' + basename_search
            if debug:
                print("basename_search="+basename_search)
                print("file_search="+file_search)
            if (not os.path.exists(file_search)) or force:
                os.system("LFR_packet_decom "+file.replace(" ", "\ "))

    def _loadSWF(self, freq=0):
        for file in self.PacketsRecords:
            basename = os.path.basename(file).replace(".data", "_NORMAL.sf%d"%freq)
            file = os.path.dirname(file) + '/decom/' + basename
            if os.path.exists(file):
                df = pds.read_csv(file,comment='#',  header=None,
                                  delim_whitespace=True,
                                  parse_dates=False,
                                  index_col=None)
                labels = ['V', 'E1', 'E2', 'B1', 'B2', 'B3']
                df.columns = labels
                self.Products["SWF%d"%freq] = df

    def _loadCWF(self, freq=1, debug=0):
        for file in self.PacketsRecords:
            if freq == 1:
                basename = os.path.basename(file).replace(".data", "_SBM1.cf1")
                file = os.path.dirname(file) + '/decom/' + basename
            elif freq == 2:
                basename = os.path.basename(file).replace(".data", "_SBM2.cf2")
                file = os.path.dirname(file) + '/decom/' + basename
            elif freq == 3:
                basename = os.path.basename(file).replace(".data", "_NORMAL_LONG.cf3")
                file = os.path.dirname(file) + '/decom/' + basename
                if not os.path.exists(file):
                    basename = os.path.basename(file).replace(".data", "_NORMAL.cf3")
                    file = os.path.dirname(file) + '/decom/' + basename
            if os.path.exists(file):
                df = pds.read_csv(file, comment='#', header=None,
                                  delim_whitespace=True,
                                  parse_dates=False,
                                  index_col=None)
                labels = ['V', 'E1', 'E2', 'B1', 'B2', 'B3']
                df.columns = labels
                self.Products["CWF%d"%freq] = df
            else:
                if debug:
                    print("File not found: "+file)

    def _loadASM(self, freq=0):
        for file in self.PacketsRecords:
            basename = os.path.basename(file).replace(".data", "_NORMAL.af%d"%freq)
            file = os.path.dirname(file) + '/decom/' + basename
            if os.path.exists(file):
                df = pds.read_csv(file,comment='#', header=None,
                                  delim_whitespace=True,
                                  parse_dates=False,
                                  index_col=None)
                dfCplx = pds.DataFrame(dtype=np.complex128, columns=['b1b1', 'b1b2', 'b1b3', 'b1e1', 'b1e2', 'b2b2','b2b3', 'b2e1', 'b2e2', 'b3b3', 'b3e1', 'b3e2', 'e1e1', 'e1e2', 'e2e2'])
                dfCplx[['b1b1', 'b2b2', 'b3b3', 'e1e1', 'e2e2']] = df[[0, 9, 16, 21, 24]]
                dfCplx['b1b2'] = df[1] + 1j*df[2]
                dfCplx['b1b3'] = df[3] + 1j*df[4]
                dfCplx['b1e1'] = df[5] + 1j*df[6]
                dfCplx['b1e2'] = df[7] + 1j*df[8]
                dfCplx['b2b3'] = df[10] + 1j*df[11]
                dfCplx['b2e1'] = df[12] + 1j*df[13]
                dfCplx['b2e2'] = df[14] + 1j*df[15]
                dfCplx['b3e1'] = df[17] + 1j*df[18]
                dfCplx['b3e2'] = df[19] + 1j*df[20]
                dfCplx['e1e2'] = df[22] + 1j*df[23]

                self.Products["ASM%d"%freq] = dfCplx

    def _loadBP2(self, freq=0, stepNbr=0, stepDuration=60, bp2param='auto', bp2Index=0):
        for file in self.PacketsRecords:
            basename = os.path.basename(file).replace(".data", "_NORMAL.2f%d"%freq)
            file = os.path.dirname(file) + '/decom/' + basename
            if os.path.exists(file):
                #here should be the retrieving of the good BP2 line
                #self.Products["BP2"] =
                pass

    def loadSWF(self):
        for freq in [0, 1, 2]:
            self._loadSWF(freq)

    def loadCWF(self):
        for freq in [1, 2, 3]:
            self._loadCWF(freq)

    def loadASM(self):
        for freq in [0, 1, 2]:
            self._loadASM(freq)

    def SWF(self, freq=0, Number=0):
        try:
            snapshotSz = self.OutputContext.Input.SWF_L
        except:
            snapshotSz = 2048
        return self.Products["SWF%d"%freq][(Number*snapshotSz):((Number+1)*snapshotSz)]

    def ASM(self, freq=0, Number=0):
        res = self.Products["ASM%d"%freq][(Number*self.asmSz[freq]):((Number+1)*self.asmSz[freq])]
        res.index = self.asmRng["F%d"%freq]
        return res

    def CWF(self, freq=0, Number=0):
        try:
            return self.Products["CWF%d"%freq]
        except:
            return None

    def BP2(self, freq=0, param='auto'):
        pass

    def SWFCount(self):
        try:
            snapshotSz = self.OutputContext.Input.SWF_L
        except:
            snapshotSz = 2048
        return (int)(self.Products["SWF0"].shape[0]/snapshotSz)

    def ASMCount(self):
        return (int)(self.Products["ASM0"].shape[0]/self.asmSz[0])
