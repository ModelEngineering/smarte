import smarte as smt
import analyzeSBML as anl
import smarte.constants as cn

import matplotlib
import pandas as pd
import numpy as np
import tellurium as te
import unittest


IGNORE_TEST = True
IS_PLOT = True
if IS_PLOT:
    matplotlib.use("TkAgg")
MODEL = """
J1: S1 -> S2; k1*S1
J2: S2 -> S3; k2*S2
J3: S3 ->; k3*S3
J4: S3 -> S1; k4*S3

S1 = 10
S2 = 0
S3 = 0
k1 = 1
k2 = 2
k3 = 3
k4 = 4
"""
rr = te.loada(MODEL)
arr = rr.simulate()
TS = anl.Timeseries(arr)
if False:
    anl.plotOneTS(TS)

        

#############################
# Tests
#############################
class TestSmarteCore(unittest.TestCase):

    def setUp(self):
        k1_prm = anl.Parameter("k1", lower=0, upper=10)
        k2_prm = anl.Parameter("k2", lower=0, upper=20)
        k3_prm = anl.Parameter("k3", lower=0, upper=30)
        k4_prm = anl.Parameter("k4", lower=0, upper=40)
        self.smarte = smt.SmarteCore(MODEL, TS, [k1_prm, k2_prm, k3_prm, k4_prm])

    def testConstructor(self):
        # TESTING
        self.assertTrue("Model" in str(type(self.smarte.model)))
        import pdb; pdb.set_trace()



if __name__ == '__main__':
  unittest.main()
