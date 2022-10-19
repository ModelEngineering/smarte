import smarte as smt
import smarte.constants as cn
from smarte.persister import Persister

import copy
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = True
IS_PLOT = True
MAX_TS_INSTANCE = 2
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PERSISTER = os.path.join(TEST_DIR, "test_experiment_provider.pcl")
PERSISTER = Persister(TEST_PERSISTER)
TEST_FILENAME = "test_experiment_provider1.zip"
if PERSISTER.isExist():
    PROVIDER = PERSISTER.load()
else:
    provider = smt.ExperimentProvider(is_filter=False)
    test_df = provider._makeTestData(max_ts_instance=MAX_TS_INSTANCE)
    PROVIDER = smt.ExperimentProvider(df=test_df, is_filter=True)
    PERSISTER.dump(PROVIDER)
        

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
        self.assertLess(len(provider.df), len(self.provider.df))

    def testMakeCountSeries(self):
        if IGNORE_TEST:
            return
        ser = PROVIDER.makeCountSeries(cn.SD_TS_INSTANCE)
        self.assertEqual(len(ser), MAX_TS_INSTANCE)

    def testPlotConditionCounts(self):
        if IGNORE_TEST:
            return
        self.init()
        self.provider.plotFactorCounts(is_plot=IS_PLOT, exclude_factors=[])

    def testCalcBestLatincubeFitter(self):
        if IGNORE_TEST:
            return
        self.init()
        df10 = self.provider.calcBestLatincubeFits(10)
        df2 = self.provider.calcBestLatincubeFits(2)
        plt.hist(df10[cn.SD_RSSQ], bins=200)
        trues = [x <= y for x, y in zip (df10[cn.SD_RSSQ], df2[cn.SD_RSSQ])]
        self.assertTrue(all(trues))

    def testMakeDataStatisticsDf(self):
        # TESTING
        self.init()
        df = self.provider.makeDataStatisticsDf()
        self.assertGreater(len(df), 0)
        self.assertEqual(len(df.columns), 3)


if __name__ == '__main__':
  unittest.main()
