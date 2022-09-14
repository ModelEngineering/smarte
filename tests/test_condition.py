from smarte.condition import Condition
import smarte.constants as cn

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False

#############################
# Tests
#############################
class TestCondition(unittest.TestCase):

    def setUp(self):
        self.condition = Condition(biomodel_num=3)

    def testGetFromStr(self):
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
        new_condition = Condition(**condition)
        self.assertFalse(new_condition.equals(self.condition))
        self.assertTrue(isinstance(new_condition, Condition))
        

if __name__ == '__main__':
  unittest.main()
