
from smarte.experiment_result import ExperimentResult
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
class TestExperimentResult(unittest.TestCase):

    def setUp(self):
        self.condition = ExperimentCondition()
        self.result = ExperimentResult(**self.condition)

    def testGet(self):
        if IGNORE_TEST:
            return
        stg = str(self.result)
        result = self.result.getFromStr(stg)
        self.assertTrue(result.equals(self.result))

    def testMakeAggregateResult(self):
        if IGNORE_TEST:
            return
        result = self.result.makeAggregateResult()
        for value in result.values():
             self.assertEqual(len(value), 0)
        #
        dct = {k: [1] for k in cn.SD_ALL}
        df = pd.DataFrame(dct, columns=cn.SD_ALL)
        df = df.set_index(cn.SD_BIOMODEL_NUM)
        result = self.result.makeAggregateResult(df=pd.DataFrame(df))
        for column in cn.SD_ALL:
             if column != cn.SD_BIOMODEL_NUM:
                 self.assertEqual(len(df[column]), 1)
        

if __name__ == '__main__':
  unittest.main()
