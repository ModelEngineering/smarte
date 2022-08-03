import smarte as smt
import SBMLModel as mdl
import fitterpp as fpp
import smarte.constants as cn

import copy
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
J1a: $X0 -> S4; k5*X0
J2: S2 -> S3; k2*S2

X0 = 10
S1 = 10
S2 = 0
S3 = 0
k1 = 1
k2 = 2
k5 = 4
"""
PARAMETER_NAMES = ["k1", "k2", "k5"]
RR = te.loada(MODEL)
PARAMETER_DCT = {n: RR[n] for n in PARAMETER_NAMES}
POINT_DENSITY = 2
END_TIME = 5
NUM_POINT = END_TIME*POINT_DENSITY + 1
rr = te.loada(MODEL)
arr = rr.simulate(0, END_TIME, NUM_POINT)
TS = mdl.Timeseries(arr)
PARAMETERS = lmfit.Parameters()
TRUE_PARAMETERS = lmfit.Parameters()
for name in PARAMETER_NAMES:
    PARAMETERS.add(name=name, value=1, min=1, max=10)
    TRUE_PARAMETERS.add(name=name, value=RR[name], min=1, max=10)

        

#############################
# Tests
#############################
class TestSBMLFitter(unittest.TestCase):

    def setUp(self):
        self.parameters = copy.deepcopy(PARAMETERS)
        self.sfitter = smt.SBMLFitter(MODEL, self.parameters, TS,
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
        del parameter_dct["k5"]
        self.sfitter.fit()
        values_dct = dict(self.sfitter.fitter.final_params.valuesdict())
        for name, value in parameter_dct.items():
            self.assertLess(np.abs(value - values_dct[name]), 0.01)

    def testFitS1S4(self):
        if IGNORE_TEST:
            return
        def test(ts, is_fail=False):
            sfitter = smt.SBMLFitter(MODEL, self.parameters, ts,
                  point_density=POINT_DENSITY)
            parameter_dct = dict(PARAMETER_DCT)
            del parameter_dct["k5"]
            sfitter.fit()
            values_dct = dict(sfitter.fitter.final_params.valuesdict())
            trues = True
            for name, value in parameter_dct.items():
                trues = trues and (np.abs(value - values_dct[name]) < 0.01)
            if is_fail:
                self.assertFalse(trues)
            else:
                self.assertTrue(trues)
        #
        test(TS)
        ts = TS[["S1", "S3"]]
        test(ts)
        ts = TS["S4"]
        test(ts, is_fail=True)

    def testSubsetToMuteableParameters(self):
        if IGNORE_TEST:
            return
        def test(parameters, excepts=None):
            if excepts is None:
                excepts = []
            new_parameters = self.sfitter.subsetToMuteableParameters(parameters)
            for name, value in parameters.valuesdict().items():
                if name in excepts:
                    continue
                self.assertEqual(value, new_parameters.valuesdict()[name])
        #
        parameters = PARAMETERS.copy()
        test(parameters)
        parameters.add(name="J1", value=0, min=0, max=100)
        test(parameters, excepts=["J1"])
        
    def testGetAccuracies(self):
        if IGNORE_TEST:
            return
        ser = self.sfitter.getAccuracies(TRUE_PARAMETERS)
        self.assertTrue(isinstance(ser, pd.Series))
        self.assertLess(np.abs(ser.mean()), 0.001)
        
    def testEvaluateFit(self):
        if IGNORE_TEST:
            return
        sfitter = smt.SBMLFitter(MODEL, self.parameters, TS, is_collect=True,
              point_density=POINT_DENSITY)
        dct = sfitter.evaluateFit(TRUE_PARAMETERS)
        self.assertTrue(isinstance(dct, dict))
        self.assertTrue("differential_evolution" in dct["method"])
        
    def testEvaluateBiomodelFit(self):
        if IGNORE_TEST:
            return
        model_num = 12
        dct_0 = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
        dct_1 = smt.SBMLFitter.evaluateBiomodelFit(model_num, 1)
        self.assertGreater(3*dct_1["max_err"], dct_0["max_err"])
        self.assertEqual(dct_0["biomodel_num"], model_num)
        
    def testEvaluateBiomodelFit17(self):
        if IGNORE_TEST:
            return
        model_num = 17
        dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit51(self):
        if IGNORE_TEST:
            return
        model_num = 51
        dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit119(self):
        if IGNORE_TEST:
            return
        model_num = 119
        try:
            dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
            self.assertGreater(len(dct), 0)
        except RuntimeError:
            pass
        
    def testEvaluateBiomodelFit531(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 531
        dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit633(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 633
        dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit250(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 250
        dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
        
    def testEvaluateBiomodelFit631(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 631
        dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
        
    def testFindBadModel(self):
        # Finds the bad model
        return
        start_model_num = 632
        for model_num in range(start_model_num, 1000):
            try:
                dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, 0)
            except Exception as exp:
                import pdb; pdb.set_trace()
                pass


if __name__ == '__main__':
  unittest.main()
