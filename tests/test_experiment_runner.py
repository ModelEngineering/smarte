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
WORKUNIT = smt.Workunit(biomodel_num=list(range(1, NUM_MODEL + 1)),
      ts_instance=TS_INSTANCE, noise_mag=0.1)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(TEST_DIR, "test_experiment_result_collection.csv")
TEST_FILE1 = os.path.join(TEST_DIR, "test_experiment_runner1.csv")
REMOVE_FILES = []


#############################
# Tests
#############################
class TestExperimentRunner(unittest.TestCase):

    def init(self):
        self.remove()
        self.runner = smt.ExperimentRunner(WORKUNIT, directory=TEST_DIR)
        self.remove()

    def tearDown(self):
        self.remove()
        self.remove()

    def remove(self):
        for ffile in REMOVE_FILES:
            if os.path.isfile(ffile):
                os.remove(ffile)
        #
        ffiles = os.listdir(TEST_DIR)
        for ffile in ffiles:
            if cn.SD_BIOMODEL_NUM in ffile:
                path = os.path.join(TEST_DIR, ffile)
                os.remove(path)

    def testMakePath(self):
        if IGNORE_TEST:
            return
        path = smt.ExperimentRunner.makePath(WORKUNIT, TEST_DIR)
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
            _ = smt.ExperimentRunner.getTimeseries(biomodel_num,
                  noise_mag, ts_instance)

    def testGetWorkunitInfo(self):
        if IGNORE_TEST:
            return
        self.init()
        df = self.runner.runWorkunit(is_report=IGNORE_TEST,
              is_recover=True)
        conditions, result_collection = self.runner.getWorkunitInfo(is_recover=False)
        self.assertEqual(len(result_collection[cn.SD_BIOMODEL_NUM]), 0)
        conditions, result_collection = self.runner.getWorkunitInfo(is_recover=True)
        self.assertGreater(len(result_collection[cn.SD_BIOMODEL_NUM]), 1)

    def testRunWorkunit(self):
        if IGNORE_TEST:
            return
        self.init()
        df = self.runner.runWorkunit(is_report=IGNORE_TEST)
        new_df = smt.ExperimentRunner.readCsv(workunit=WORKUNIT,
              directory=TEST_DIR)
        self.assertEqual(len(df), len(new_df))

    def testRunWorkunitBug1(self):
        if IGNORE_TEST:
            return
        self.init()
        stg = "biomodel_num--1__columns_deleted--0__max_fev--10000__method--leastsq__noise_mag--0.1__latincube_idx--2__range_max_frac--2.0__range_min_frac--0.5__ts_instance--1"
        workunit = smt.Workunit.getFromStr(stg)
        self.runner = smt.ExperimentRunner(workunit, directory=TEST_DIR)
        df = self.runner.runWorkunit(is_report=IGNORE_TEST, is_recover=False)
        self.assertGreater(len(df), 0)
        self.assertTrue(isinstance(df, pd.DataFrame))


    def testReadCsv(self):
        if IGNORE_TEST:
            return
        df = smt.ExperimentRunner.readCsv(path=TEST_FILE)
        self.assertGreater(len(df), 0)

    def makeResults(self):
        self.init()
        df = self.runner.runWorkunit(is_report=IGNORE_TEST, is_recover=False)
        results = []
        for idx, row in df.iterrows():
            dct= row.to_dict()
            dct[cn.SD_BIOMODEL_NUM] = idx
            result = smt.ExperimentResult(**dct)
            results.append(result)
        return results

    def testWriteResults(self):
        if IGNORE_TEST:
            return
        results = self.makeResults()
        df = self.runner.writeResults(results, path=TEST_FILE1)
        new_df = self.runner.readCsv(path=TEST_FILE1)
        columns = list(df.columns)
        columns.remove(cn.SD_METHOD)
        columns.remove(cn.SD_STATUS)
        dff = df[columns] - new_df[columns]
        self.assertTrue(np.isclose(dff.sum().sum(), 0))
        os.remove(TEST_FILE1)

    def testRunWorkunits(self):
        if IGNORE_TEST:
            return
        return
        df = smt.ExperimentRunner.runWorkunits()

    def testIterateWorkunitInfo(self):
        if IGNORE_TEST:
            return
        self.init()
        size = 2
        num_workunit = 0
        for workunit_info in self.runner.iterateWorkunitInfo(num_partition=size):
            num_workunit += 1
            self.assertEqual(len(workunit_info.result_collection[cn.SD_BIOMODEL_NUM]), 0)
        self.assertEqual(num_workunit, size)


if __name__ == '__main__':
  unittest.main()
