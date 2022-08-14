
from smarte.experiment_condition import ExperimentCondition
from smarte.extended_dict import KEY_VALUE_SEP, VALUE_SEP
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
        self.assertEqual(stg.count(VALUE_SEP), len(cn.SD_CONDITIONS))
        #
        condition = ExperimentCondition(biomodel_num=[1, 2])
        stg = str(condition)
        self.assertEqual(stg.count(VALUE_SEP), len(cn.SD_CONDITIONS)+1)

    def testGet(self):
        if IGNORE_TEST:
            return
        stg = str(self.condition)
        condition = self.condition.get(stg)
        self.assertTrue(condition.equals(self.condition))


        

if __name__ == '__main__':
  unittest.main()
