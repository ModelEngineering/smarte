
from smarte.experiment_condition import ExperimentCondition, KEY_VALUE_SEP
import smarte.constants as cn

import unittest

IGNORE_TEST = False
IS_PLOT = False
METHOD = "leastsq"
        

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
        self.assertEqual(stg.count(KEY_VALUE_SEP), len(cn.SD_CONDITIONS))

    def testGetCondition(self):
        if IGNORE_TEST:
            return
        stg = str(self.condition)
        condition = self.condition.getCondition(stg)
        self.assertTrue(condition.equals(self.condition))


        

if __name__ == '__main__':
  unittest.main()
