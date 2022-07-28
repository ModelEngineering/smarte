import smarte as smt
import analyzeSBML as anl
import fitterpp as fpp
import smarte.constants as cn

import copy
import lmfit
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
J1a: $X0 -> S4; k5*X0
J2: S2 -> S3; k2*S2
J3: S3 -> S1; k4*S3
J4: X0 -> S4; k5*S3

X0 = 10
S1 = 10
S2 = 0
S3 = 0
k1 = 1
k2 = 2
k3 = 3
k4 = 4
k5 = 4
"""
PARAMETER_NAMES = ["k1", "k2", "k3", "k4"]
RR = te.loada(MODEL)
PARAMETER_DCT = {n: RR[n] for n in PARAMETER_NAMES}
POINT_DENSITY = 2
END_TIME = 5
NUM_POINT = END_TIME*POINT_DENSITY + 1
rr = te.loada(MODEL)
arr = rr.simulate(0, END_TIME, NUM_POINT)
TS = anl.Timeseries(arr)
if False:
    anl.plotOneTS(TS)
PARAMETERS = lmfit.Parameters()
for name in PARAMETER_NAMES:
    PARAMETERS.add(name=name, value=0, min=0, max=10)

        

#############################
# Tests
#############################
class TestSBMLFitter(unittest.TestCase):

    def setUp(self):
        self.parameters = copy.deepcopy(PARAMETERS)
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

    def testFitAllColumns(self):
        if IGNORE_TEST:
            return
        parameter_dct = dict(PARAMETER_DCT)
        del parameter_dct["k3"]
        self.sfitter.fit()
        values_dct = dict(self.sfitter.fitter.final_params.valuesdict())
        for name, value in parameter_dct.items():
            self.assertTrue(np.isclose(value, values_dct[name]))

    def testFitS1S4(self):
        # TESTING
        def test(ts, is_fail=False):
            sfitter = smt.SBMLFitter(MODEL, ts, self.parameters,
                  point_density=POINT_DENSITY)
            parameter_dct = dict(PARAMETER_DCT)
            del parameter_dct["k3"]
            sfitter.fit()
            values_dct = dict(sfitter.fitter.final_params.valuesdict())
            trues = True
            for name, value in parameter_dct.items():
                trues = trues and np.isclose(value, values_dct[name])
            if is_fail:
                self.assertFalse(trues)
            else:
                self.assertTrue(trues)
        #
        test(TS)
        ts = anl.Timeseries(TS[["S1", "S3"]])
        test(ts)
        ts = anl.Timeseries(TS[["S4"]])
        test(ts, is_fail=True)


if __name__ == '__main__':
  unittest.main()
