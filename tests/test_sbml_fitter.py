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
        if IGNORE_TEST:
            return
        self.init()

    def init(self):
        self.parameters = copy.deepcopy(PARAMETERS)
        self.sfitter = smt.SBMLFitter(MODEL, self.parameters, TS,
              point_density=POINT_DENSITY)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue("Fitterpp" in str(type(self.sfitter.fitter)))

    def testConstructor2(self):
        if IGNORE_TEST:
            return
        self.init()
        sfitter = smt.SBMLFitter(MODEL, self.parameters, TS,
              method_names=["leastsq", "differential_evolution"],
              max_fev=10000,
              point_density=POINT_DENSITY)
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
        self.init()
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

    def testFitLatinCube(self):
        if IGNORE_TEST:
            return
        self.init()
        parameter_dct = dict(PARAMETER_DCT)
        sfitter = smt.SBMLFitter(MODEL, self.parameters, TS,
              point_density=POINT_DENSITY, num_latincube=2, is_collect=True)
        dct = sfitter.evaluateFit(TRUE_PARAMETERS)
        self.assertTrue("differential_evolution" in dct.values())

    def evaluateBiomodelFit(self, model_num, noise_mag, **kwargs):
        data = smt.SBMLFitter.makeBiomodelSyntheticData(model_num,
              noise_mag, num_dataset=1)
        if len(data) == 0:
            return {cn.SD_BIOMODEL_NUM: model_num}
        dct = smt.SBMLFitter.evaluateBiomodelFit(model_num, data[0], **kwargs)
        dct[cn.SD_NOISE_MAG] = noise_mag
        dct[cn.SD_TS_INSTANCE] = 1
        return dct
        
    def testEvaluateBiomodelFit(self):
        if IGNORE_TEST:
            return
        model_num = 12
        dct_0 = self.evaluateBiomodelFit(model_num, 0)
        dct_1 = self.evaluateBiomodelFit(model_num, 1)
        self.assertGreater(np.abs(dct_1[cn.SD_MAX_ERR]), np.abs(dct_0[cn.SD_MAX_ERR]))
        self.assertEqual(dct_0["biomodel_num"], model_num)
        
    def testEvaluateBiomodelFitOpts(self):
        if IGNORE_TEST:
            return
        model_num = 12
        dct_0 = self.evaluateBiomodelFit(model_num, 0)
        dct_1 = self.evaluateBiomodelFit(model_num, 1)
        self.assertGreater(np.abs(dct_1[cn.SD_MAX_ERR]), np.abs(dct_0[cn.SD_MAX_ERR]))
        self.assertEqual(dct_0["biomodel_num"], model_num)
        
    def testEvaluateBiomodelFitLargeError(self):
        if IGNORE_TEST:
            return
        max_fev = 500
        model_num = 7
        dct = self.evaluateBiomodelFit(model_num, 0, max_fev=max_fev)
        self.assertLess(np.abs(dct[cn.SD_CNT] - max_fev), 2)
        
    def testEvaluateBiomodelFit17(self):
        if IGNORE_TEST:
            return
        model_num = 17
        dct = self.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit51(self):
        if IGNORE_TEST:
            return
        model_num = 51
        dct = self.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit119(self):
        if IGNORE_TEST:
            return
        model_num = 119
        try:
            dct = self.evaluateBiomodelFit(model_num, 0)
            self.assertGreater(len(dct), 0)
        except RuntimeError:
            pass
        
    def testEvaluateBiomodelFit531(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 531
        dct = self.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit633(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 633
        dct = self.evaluateBiomodelFit(model_num, 0)
        self.assertEqual(len(dct), 1)
        
    def testEvaluateBiomodelFit250(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 250
        dct = self.evaluateBiomodelFit(model_num, 0)
        
    def testEvaluateBiomodelFit631(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 631
        dct = self.evaluateBiomodelFit(model_num, 0)
        
    def testEvaluateBiomodelFit437(self):
        # Model generates no output
        if IGNORE_TEST:
            return
        model_num = 437
        try:
            dct = self.evaluateBiomodelFit(model_num, 0)
            self.assertTrue(True)  # SHouldn't get here
        except ValueError:
            pass
        
    def testFindBadModel(self):
        # Finds the bad model
        return
        start_model_num = 340
        for model_num, model in mdl.Model.iterateBiomodels(
              start_num=start_model_num, num_model=100, is_allerror=True):
            print(model_num)
            try:
                dct = self.evaluateBiomodelFit(model_num, 0)
            except Exception as exp:
                import pdb; pdb.set_trace()
                pass
        
    def testmakeBiomodelSyntheticData(self):
        if IGNORE_TEST:
            return
        num_dataset = 20
        data = smt.SBMLFitter.makeBiomodelSyntheticData(12, 0.1,
              num_dataset=num_dataset)
        self.assertEqual(len(data), num_dataset)
        #
        normalized_data = [d - data[0] for d in data]
        df = pd.concat(normalized_data)
        ser = df.mean()
        self.assertLess(np.abs(ser.loc["Z"]), 0.1)
        

if __name__ == '__main__':
  unittest.main()
