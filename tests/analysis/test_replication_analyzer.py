import smarte as smt
from smarte.analysis.replication_analyzer import ReplicationAnalyzer
import SBMLModel as mdl
import fitterpp as fpp
import smarte.constants as cn

import copy
import os
import matplotlib
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False
if IS_PLOT:
    matplotlib.use("TkAgg")
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(TEST_DIR, "replication_analyzer.csv")
        

#############################
# Tests
#############################
class TestReplicationAnalyzer(unittest.TestCase):

    def setUp(self):
        self.ffile = TEST_FILE
        self.analyzer = ReplicationAnalyzer(self.ffile)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue(isinstance(self.analyzer.df, pd.DataFrame))
        self.assertGreater(len(self.analyzer.df), 0)

    def testPlotOneTime(self):
        if IGNORE_TEST:
            return
        self.analyzer.plotOneTime(xaxis=cn.SD_NUM_REACTION, figsize=[5,5],
              is_plot=IS_PLOT)

    def testPlotManyTime(self):
        if IGNORE_TEST:
            return
        self.analyzer.plotManyTimes(figsize=[15,15], is_nfev=False,
              is_plot=IS_PLOT)

    def testPlotOneEstimationError(self):
        if IGNORE_TEST:
            return
        self.analyzer.plotOneEstimationError(xaxis=cn.SD_NUM_REACTION,
              figsize=[5,5], is_plot=IS_PLOT)
        self.analyzer.plotOneEstimationError(xaxis=cn.SD_NUM_REACTION,
              is_log2_ratio=False, figsize=[5,5], is_plot=IS_PLOT)

    def testPlotManyEstimationError(self):
        if IGNORE_TEST:
            return
        self.analyzer.plotManyEstimationError(figsize=[15,15], is_max=False,
              is_plot=IS_PLOT)

    def testCalcErrorFraction(self):
        if IGNORE_TEST:
            return
        self.assertTrue(np.isclose(self.analyzer.calcErrorFraction(-1), -0.5))
        self.assertTrue(np.isclose(self.analyzer.calcErrorFraction(1), 1.0))
        self.assertTrue(np.isclose(self.analyzer.calcErrorFraction(0), 0))
        self.assertLess(self.analyzer.calcErrorFraction(0.5), 1.0)
   

if __name__ == '__main__':
  unittest.main()
