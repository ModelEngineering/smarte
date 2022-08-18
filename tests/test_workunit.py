from smarte.experiment_condition import ExperimentCondition
import smarte as smt
import smarte.constants as cn
from smarte.extended_dict import VALUE_SEP, KEY_VALUE_SEP

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False
METHOD = "leastsq"
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(TEST_DIR, "test_experiment_runner.csv")        
        

#############################
# Tests
#############################
class TestWorkunit(unittest.TestCase):

    def setUp(self):
        self.workunit = smt.Workunit(method=METHOD)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertEqual(self.workunit[cn.SD_METHOD][0], METHOD)

    def testStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.workunit)
        self.assertEqual(stg.count(VALUE_SEP), len(cn.SD_CONDITIONS))
        #
        condition = smt.Workunit(biomodel_num=[1, 2])
        stg = str(condition)
        self.assertEqual(stg.count(VALUE_SEP), len(cn.SD_CONDITIONS)+1)

    def testCalcMultivaluedFactors(self):
        if IGNORE_TEST:
            return
        def test(size, **kwargs):
            workunit = smt.Workunit(**kwargs)
            factors = workunit.calcMultivaluedFactors()
            self.assertEqual(len(factors), size)
        #
        test(2)
        test(0, biomodel_num=1, ts_instance=1)
        test(1, biomodel_num=1)
        test(3, range_min_frac=[1, 2])

    def testIterator(self):
        if IGNORE_TEST:
            return
        workunit = smt.Workunit(biomodel_num=[1, 2], ts_instance=[1])
        conditions = list(workunit.iterator)
        self.assertEqual(len(conditions), 2)

        

if __name__ == '__main__':
  unittest.main()
