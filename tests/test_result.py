from smarte.result import Result
from smarte.condition import Condition
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
class TestResult(unittest.TestCase):

    def setUp(self):
        self.condition = Condition(biomodel_num=3)
        self.result = Result(**self.condition)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertGreater(len(self.result), len(self.condition))
        trues = [self.result[k] == v for k, v in self.condition.items()]
        self.assertTrue(all(trues))
        
        

if __name__ == '__main__':
  unittest.main()
