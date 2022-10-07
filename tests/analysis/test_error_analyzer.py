from smarte.analysis.error_analyzer import ErrorAnalyzer
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
TEST_FILE = os.path.join(TEST_DIR, "test_anova.csv")
df = pd.read_csv(TEST_FILE)
df = df[ df["num_latincube"] == 1]
df = df.set_index(cn.SD_BIOMODEL_NUM)
SER = df[cn.SD_MEDIAN_ERR]
        

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
