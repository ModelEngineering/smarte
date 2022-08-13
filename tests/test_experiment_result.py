
from smarte.experiment_result import ExperimentResult
from smarte.experiment_condition import ExperimentCondition
import smarte.constants as cn

import unittest

IGNORE_TEST = False
IS_PLOT = False
        

#############################
# Tests
#############################
class TestExperimentResult(unittest.TestCase):

    def setUp(self):
        self.condition = ExperimentCondition()
        self.result = ExperimentResult(self.condition)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertEqual(self.result[cn.SD_METHOD], METHOD)

    def testStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.result)
        self.assertEqual(stg.count(KEY_VALUE_SEP), len(cn.SD_CONDITIONS))

    def testGetResult(self):
        if IGNORE_TEST:
            return
        stg = str(self.result)
        result = self.result.getResult(stg)
        self.assertTrue(result.equals(self.result))
        

if __name__ == '__main__':
  unittest.main()
