import smarte as smt

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(TEST_DIR, "test_experiment_result_collection.csv")        
DF = pd.read_csv(TEST_PATH)
RESULT_COLLECTION = smt.ExperimentResultCollection(df=DF)
CONDITIONS = smt.ExperimentCondition.getFromResultCollection(
      RESULT_COLLECTION)
LEN = len(RESULT_COLLECTION)
NUM_CONDITION = 1
        

#############################
# Tests
#############################
class TestWorkunitInfo(unittest.TestCase):

    def setUp(self):
        self.result_collection = RESULT_COLLECTION.copy()
        for key, values in self.result_collection.items():
            self.result_collection[key] = values[:-NUM_CONDITION]
        self.conditions = CONDITIONS[-NUM_CONDITION:]
        self.workunit_info = smt.WorkunitInfo(conditions=self.conditions,
              result_collection=self.result_collection)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertEqual(len(self.workunit_info.conditions), NUM_CONDITION)
        self.assertEqual(len(self.workunit_info.result_collection), LEN-1)

    def testExtend(self):
        if IGNORE_TEST:
            return
        workunit_info = smt.WorkunitInfo(conditions=list(self.conditions),
              result_collection=self.result_collection.copy())
        workunit_info.extend(self.workunit_info)
        self.assertEquals(len(workunit_info.result_collection),
              2*len(self.result_collection))
        self.assertEquals(len(workunit_info.conditions),
              2*len(self.conditions))

    def testClean(self):
        if IGNORE_TEST:
            return
        # TODO: Finish
        # Create a workunitinfo with an ExperimentCondition for all 
        # lists in the ExperimentResultCollection.
        # Cleaning should result in self.workunit_info.
        workunit_info = smt.WorkunitInfo(conditions=CONDITIONS,
              result_collection=self.result_collection)
         


if __name__ == '__main__':
  unittest.main()
