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


IGNORE_TEST = True
IS_PLOT = True
if IS_PLOT:
    matplotlib.use("TkAgg")
DIR = os.path.join(cn.EXPERIMENT_DIR,
       "Noise--0.1_ColumnsDeleted--0_MinMax--0.25-4.0_Maxfev--10000")
FFILE = os.path.join(DIR, "1.csv")
        

#############################
# Tests
#############################
class TestReplicationAnalyzer(unittest.TestCase):

    def setUp(self):
        self.ffile = FFILE
        self.analyzer = ReplicationAnalyzer(FFILE)

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
        self.analyzer.plotManyTimes(figsize=[15,15], is_nfev=False)

    def testPlotOneEstimationError(self):
        if IGNORE_TEST:
            return
        self.analyzer.plotOneEstimationError(xaxis=cn.SD_NUM_REACTION, figsize=[5,5],
              is_plot=IS_PLOT)

    def testPlotManyEstimationError(self):
        # TESTING
        self.analyzer.plotManyEstimationError(figsize=[15,15], is_max=False)
        


if __name__ == '__main__':
  unittest.main()
