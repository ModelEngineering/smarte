import smarte as smt
import analyzeSBML as anl
import fitterpp as fpp
import smarte.constants as cn

import lmfit
import matplotlib
import pandas as pd
import numpy as np
import tellurium as te
import unittest


IGNORE_TEST = False
IS_PLOT = False
if IS_PLOT:
    matplotlib.use("TkAgg")
MODEL = """
J1: S1 -> S2; k1*S1
J2: S2 -> S3; k2*S2
J3: S3 -> S1; k4*S3

S1 = 10
S2 = 0
S3 = 0
k1 = 1
k2 = 2
k3 = 3
k4 = 4
"""
POINT_DENSITY = 2
END_TIME = 5
NUM_POINT = END_TIME*POINT_DENSITY + 1
rr = te.loada(MODEL)
arr = rr.simulate(0, END_TIME, NUM_POINT)
TS = anl.Timeseries(arr)
if False:
    anl.plotOneTS(TS)

        

#############################
# Tests
#############################
class TestSBMLFitter(unittest.TestCase):

    def setUp(self):
        self.parameters = lmfit.Parameters()
        for name in ["k1", "k2", "k3", "k4"]:
            self.parameters.add(name=name, value=0, min=0, max=10)
        self.sfitter = smt.SBMLFitter(MODEL, TS, self.parameters,
              point_density=POINT_DENSITY)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue("Fitterpp" in str(type(self.sfitter.fitter)))

    def testSimulate(self):
        if IGNORE_TEST:
            return
        df = self.sfitter._simulate(is_dataframe=True, **{"k1": 4, "k2": 4})
        self.assertTrue(np.abs(df.loc[5000, "S3"] - 10) < 0.1)

    def testFit(self):
        if IGNORE_TEST:
            return



if __name__ == '__main__':
  unittest.main()
