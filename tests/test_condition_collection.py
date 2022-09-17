from smarte.condition_collection import ConditionCollection
import smarte.constants as cn

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False

#############################
# Tests
#############################
class TestConditionCollection(unittest.TestCase):

    def setUp(self):
        self.condition = ConditionCollection(biomodel_num=[1, 3])

    def testMakeFromStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.condition)
        condition = self.condition.makeFromStr(stg)
        self.assertTrue(condition.equals(self.condition))

    def testCopyEquals(self):
        if IGNORE_TEST:
            return
        condition = self.condition.copy()
        self.assertTrue(condition.equals(self.condition))
        condition[cn.SD_BIOMODEL_NUM] = -1
        new_condition = ConditionCollection(**condition)
        self.assertFalse(new_condition.equals(self.condition))
        self.assertTrue(isinstance(new_condition, ConditionCollection))
        

if __name__ == '__main__':
  unittest.main()
