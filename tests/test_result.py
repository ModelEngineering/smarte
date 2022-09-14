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
        import pdb; pdb.set_trace()
        
        

if __name__ == '__main__':
  unittest.main()
