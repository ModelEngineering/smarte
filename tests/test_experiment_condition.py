from smarte.experiment_condition import ExperimentCondition
import smarte.constants as cn

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False

#############################
# Tests
#############################
class TestExperimentCondition(unittest.TestCase):

    def setUp(self):
        self.condition = ExperimentCondition(biomodel_num=[1, 3])
        self.condition = ExperimentCondition(**self.condition)

    def testGetFromStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.condition)
        condition = self.condition.getFromStr(stg)
        self.assertTrue(condition.equals(self.condition))

    def testCopyEquals(self):
        if IGNORE_TEST:
            return
        condition = self.condition.copy()
        self.assertTrue(condition.equals(self.condition))
        condition[cn.SD_BIOMODEL_NUM] = -1
        new_condition = ExperimentCondition(**condition)
        self.assertFalse(new_condition.equals(self.condition))
        self.assertTrue(isinstance(new_condition, ExperimentCondition))
        

if __name__ == '__main__':
  unittest.main()
