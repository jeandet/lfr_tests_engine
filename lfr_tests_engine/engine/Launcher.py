#!/usr/bin/python3
# -*- coding: utf-8 -*-
import importlib
import datetime
import traceback
import os
import sys
import time

__author__ = "Alexis Jeandet"
__copyright__ = "Copyright 2016, Laboratory of Plasma Physics"
__credits__ = []
__license__ = "GPLv2"
__version__ = "1.0.0"
__maintainer__ = "Alexis Jeandet"
__email__ = "alexis.jeandet@member.fsf.org"
__status__ = "Development"

from .test_common import *
from .test import *
from .testcontext import *

if __name__ == '__main__':
    input = ""
    try:
        input_file = sys.argv[1]
    except:
        try:
            input_file = os.environ["INPUT_SCRIPT"]
        except:
            pass
    inputContext = TestContextInputFromFile(input_file)
    try:
        mod = importlib.import_module(inputContext.TestMod, "*")
        test = mod.Test(inputContext)
    except:
        script = open(inputContext.TestScrip, "r")
        exec(script.read())
        test = Test(inputContext)
        test.OutputContext.Exeptions.append(traceback.format_exc())
    try:
        test.OutputContext.T0 = time.time()
        test.beforeTest()
        for step in test.InputContext.TestSteps:
            test.OutputContext.T3.append(time.time())
            try:
                stepRes = test.run(step)
                test.OutputContext.TestStepsResults.append([step, stepRes])
            except:
                test.OutputContext.Exeptions.append(traceback.format_exc())
                test.OutputContext.TestStepsResults.append("Sys error on step")
            test.soc.activeWait(step.delta - (time.time() - test.OutputContext.T3[-1]))
        test.OutputContext.T4 = time.time()
        test.afterTest()
        test.OutputContext.TestResult = "Success"
    except:
        test.OutputContext.Exeptions.append(traceback.format_exc())
        test.OutputContext.TestResult = "Failed"
    test.OutputContext.save(
        input_file.replace(".input", "_"
                           + datetime.datetime.isoformat(datetime.datetime.now())
                           + ".output"))
    if inputContext.QuitAfterTest:
        quit()
