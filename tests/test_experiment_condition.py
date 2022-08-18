
from smarte.experiment_condition import ExperimentCondition
from smarte.extended_dict import KEY_VALUE_SEP, VALUE_SEP
import smarte.constants as cn

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
class TestExperimentCondition(unittest.TestCase):

    def setUp(self):
        self.condition = ExperimentCondition(method=METHOD)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertEqual(self.condition[cn.SD_METHOD], METHOD)

    def testStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.condition)
        self.assertEqual(stg.count(VALUE_SEP), len(cn.SD_CONDITIONS))
        #
        condition = ExperimentCondition(biomodel_num=[1, 2])
        stg = str(condition)
        self.assertEqual(stg.count(VALUE_SEP), len(cn.SD_CONDITIONS)+1)

    def testGetFromDF(self):
        if IGNORE_TEST:
            return
        df = pd.read_csv(TEST_FILE)
        conditions = ExperimentCondition.getFromDF(df)
        trues = [isinstance(c, ExperimentCondition) for c in conditions]
        self.assertTrue(all(trues))
        

if __name__ == '__main__':
  unittest.main()
