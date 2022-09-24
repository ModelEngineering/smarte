import smarte as smt
import smarte.constants as cn

import copy
import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = True
IS_PLOT = True
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILENAME = "test_experiment_provider.zip"
PROVIDER = smt.ExperimentProvider(directory=TEST_DIR, is_filter=True)

        

#############################
# Tests
#############################
class TestExperimentProvider(unittest.TestCase):

    def init(self):
        self.provider = copy.deepcopy(PROVIDER)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.init()
        self.assertTrue(isinstance(self.provider.df, pd.DataFrame))
        self.assertGreater(len(self.provider.df), 0)

    def testGetZippaths(self):
        if IGNORE_TEST:
            return
        paths = smt.ExperimentProvider.getZippaths()
        trues = ["zip" in f for f in paths]
        self.assertTrue(all(trues))

    def testMakeDataframe(self):
        if IGNORE_TEST:
            return
        df = smt.ExperimentProvider.makeDataframe()
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertGreaterEqual(len(df[cn.SD_METHOD]), 2)
        self.assertGreaterEqual(len(df[cn.SD_TS_INSTANCE]), 5)

    def testFilerUnsuccessfulExperimentsFilterDuplicateConditions(self):
        if IGNORE_TEST:
            return
        self.init()
        provider = smt.ExperimentProvider(TEST_FILENAME, directory=TEST_DIR,
              is_filter=False)
        self.assertLess(len(self.provider.df), len(provider.df))

    def testMakeCountSeries(self):
        if IGNORE_TEST:
            return
        self.init()
        ser = self.provider.makeCountSeries(cn.SD_TS_INSTANCE)
        self.assertEqual(len(ser), 5)
        std = ser.std()
        self.assertLess(std, 5)

    def testPlotConditionCounts(self):
        if IGNORE_TEST:
            return
        self.init()
        self.provider.plotFactorCounts(is_plot=IS_PLOT)


if __name__ == '__main__':
  unittest.main()
