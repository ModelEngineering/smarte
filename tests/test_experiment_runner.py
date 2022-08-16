import smarte as smt
import SBMLModel as mdl
import fitterpp as fpp
import smarte.constants as cn

import copy
import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False
TS_INSTANCE = 1
NUM_MODEL = 10
CONDITION = smt.ExperimentCondition(biomodel_num=list(range(1, NUM_MODEL + 1)),
      ts_instance=TS_INSTANCE, noise_mag=0.1)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
REMOVE_FILES = []
TEST_FILE = os.path.join(TEST_DIR, "test_experiment_runner.csv")        
        

#############################
# Tests
#############################
class TestExperimentRunner(unittest.TestCase):

    def init(self):
        self.remove()
        self.runner = smt.ExperimentRunner(CONDITION, directory=TEST_DIR)

    def tearDown(self):
        self.remove()

    def remove(self):
        for ffile in REMOVE_FILES:
            if os.path.isfile(ffile):
                os.remove(ffile)

    def testMakePath(self):
        if IGNORE_TEST:
            return
        path = smt.ExperimentRunner.makePath(CONDITION, TEST_DIR)
        self.assertTrue(str(TS_INSTANCE) + ".csv" in path)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.init()
        self.assertTrue(cn.SD_BIOMODEL_NUM in self.runner.out_path)

    def testGetTimeseries(self):
        if IGNORE_TEST:
            return
        biomodel_num = 12
        noise_mag = 0.1
        ts_instance = 1
        ts = smt.ExperimentRunner.getTimeseries(biomodel_num, noise_mag, ts_instance)
        #
        with self.assertRaises(FileNotFoundError):
            ts_instance = -1
            _ = smt.ExperimentRunner.getTimeseries(biomodel_num, noise_mag, ts_instance)

    def testRun(self):
        if IGNORE_TEST:
            return
        self.init()
        df = self.runner.run(is_report=IGNORE_TEST, is_recover=False)
        new_df = smt.ExperimentRunner.readCsv(condition=CONDITION, directory=TEST_DIR)
        self.assertEqual(len(df), len(new_df))

    def testReadCsv(self):
        if IGNORE_TEST:
            return
        df = smt.ExperimentRunner.readCsv(path=TEST_FILE)
        self.assertGreater(len(df), 0)


if __name__ == '__main__':
  unittest.main()
