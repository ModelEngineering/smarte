from smarte.result_collection import ResultCollection
from smarte.condition_collection import ConditionCollection
import smarte.constants as cn

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False
RESULT_DCT = {k: [1, 2] for k in cn.SD_ALL}

#############################
# Tests
#############################
class TestResultCollection(unittest.TestCase):

    def setUp(self):
        self.result_collection = ResultCollection(**RESULT_DCT)

    def testMakeFromStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.result_collection)
        result = self.result_collection.makeFromStr(stg)
        self.assertTrue(result.equals(self.result_collection))

    def testAggregateResults(self):
        if IGNORE_TEST:
            return
        result_collection = ResultCollection()
        result_collection.extend(RESULT_DCT)
        self.assertTrue(result_collection.equals(result_collection))
        

if __name__ == '__main__':
  unittest.main()
