from smarte.analysis.error_analyzer import ErrorAnalyzer
import smarte as smt
import smarte.constants as cn

import copy
import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = True
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILENAME = "test_experiment_provider.zip"
PROVIDER = smt.ExperimentProvider(directory=TEST_DIR, is_filter=True)
SER = PROVIDER.df[cn.SD_MEDIAN_FRCERR]
SER.name = cn.SD_MEDIAN_FRCERR
        

#############################
# Tests
#############################
class TestErrorAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = ErrorAnalyzer(copy.deepcopy(SER))

    def testContructor(self):
        if IGNORE_TEST:
            return
        self.assertGreater(len(SER), len(self.analyzer.ser))

    def testPlot(self):
        if IGNORE_TEST:
            return
        self.analyzer.plot(is_plot=IS_PLOT)

    def testHist(self):
        if IGNORE_TEST:
            return
        self.analyzer.hist(is_plot=IS_PLOT, bins=25)


if __name__ == '__main__':
  unittest.main()
