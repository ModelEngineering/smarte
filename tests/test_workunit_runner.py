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
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_WORKUNITS_FILE = os.path.join(TEST_DIR, "test_workunit_runner_workunits.txt")
TEST_FILE = os.path.join(TEST_DIR, "test_experiment_runner.csv")
TEST_FILE1 = os.path.join(TEST_DIR, "test_experiment_runner1.csv")
WORKUNIT = smt.Workunit(biomodel_num=list(range(1, NUM_MODEL + 1)),
      ts_instance=TS_INSTANCE, noise_mag=0.1,
      out_dir=TEST_DIR)
REMOVE_FILES = [TEST_FILE1]


#############################
# Tests
#############################
class TestWorkunitRunner(unittest.TestCase):

    def init(self):
        self.workunit = copy.deepcopy(WORKUNIT)
        self.runner = smt.WorkunitRunner(self.workunit)
        self.remove()

    def tearDown(self):
        self.remove()

    def remove(self):
        ffiles = os.listdir(TEST_DIR)
        for ffile in ffiles:
            is_remove = ffile in REMOVE_FILES
            is_remove = is_remove or (cn.SD_BIOMODEL_NUM in ffile)
            if is_remove:
                path = os.path.join(TEST_DIR, ffile)
                os.remove(path)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.init()
        self.assertTrue(cn.SD_BIOMODEL_NUM in self.runner.workunit.filename)

    def testGetTimeseries(self):
        if IGNORE_TEST:
            return
        biomodel_num = 12
        noise_mag = 0.1
        ts_instance = 1
        ts = smt.WorkunitRunner.getTimeseries(biomodel_num, noise_mag, ts_instance)
        self.assertTrue("Timeseries" in str(type(ts)))
        self.assertGreater(len(ts), 0)
        #
        with self.assertRaises(FileNotFoundError):
            ts_instance = -1
            _ = smt.WorkunitRunner.getTimeseries(biomodel_num,
                  noise_mag, ts_instance)

    def testRun(self):
        if IGNORE_TEST:
            return
        self.init()
        df = self.runner.run(is_report=IGNORE_TEST)
        self.assertTrue(isinstance(df, pd.DataFrame))
        count = len(df[df[cn.SD_STATUS] == cn.SD_STATUS_SUCCESS])
        self.assertGreater(count, 0)
        self.assertGreater(len(df), count)

    def testRunWorkunitBug1(self):
        if IGNORE_TEST:
            return
        self.init()
        stg = "biomodel_num--1__columns_deleted--0__max_fev--10000__method--leastsq__noise_mag--0.1__latincube_idx--2__range_max_frac--2.0__range_min_frac--0.5__ts_instance--1"
        workunit = smt.Workunit.makeFromStr(stg, out_dir=TEST_DIR)
        self.runner = smt.WorkunitRunner(workunit)
        df = self.runner.run(is_report=IGNORE_TEST)
        self.assertGreater(len(df), 0)
        self.assertTrue(isinstance(df, pd.DataFrame))


if __name__ == '__main__':
  unittest.main()
