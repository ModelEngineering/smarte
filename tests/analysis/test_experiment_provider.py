import smarte as smt
import smarte.constants as cn

import copy
import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILENAME = "test_experiment_provider.zip"
PROVIDER = smt.ExperimentProvider(TEST_FILENAME, directory=TEST_DIR,
      is_filter=True)

        

#############################
# Tests
#############################
class TestExperimentProvider(unittest.TestCase):

    def setUp(self):
        self.provider = copy.deepcopy(PROVIDER)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue(isinstance(self.provider.df, pd.DataFrame))
        self.assertGreater(len(self.provider.df), 0)

    def testFilerUnsuccessfulExperimentsFilterDuplicateConditions(self):
        if IGNORE_TEST:
            return
        provider = smt.ExperimentProvider(TEST_FILENAME, directory=TEST_DIR,
              is_filter=False)
        self.assertLess(len(self.provider.df), len(provider.df))

    def testMakeCountSeries(self):
        if IGNORE_TEST:
            return
        ser = self.provider.makeCountSeries(cn.SD_TS_INSTANCE)
        self.assertEqual(len(ser), 5)
        std = ser.std()
        self.assertLess(std, 5)

    def testPlotConditionCounts(self):
        if IGNORE_TEST:
            return
        self.provider.plotFactorCounts(is_plot=IS_PLOT)
        

    
        


if __name__ == '__main__':
  unittest.main()
