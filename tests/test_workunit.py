import smarte as smt
import smarte.constants as cn

import os
import pandas as pd
import unittest

IGNORE_TEST = True
IS_PLOT = True
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
class TestWorkunit(unittest.TestCase):

    def setUp(self):
        self.result_collection = RESULT_COLLECTION.copy()
        for key, values in self.result_collection.items():
            self.result_collection[key] = values[:-NUM_CONDITION]
        self.conditions = CONDITIONS[-NUM_CONDITION:]
        self.workunit = smt.Workunit(include_conditions=self.conditions,
              result_collection=self.result_collection)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertEqual(len(self.workunit.include_conditions), NUM_CONDITION)
        self.assertEqual(len(self.workunit.result_collection), LEN-1)

    def testMakeWorkunit(self):
        if IGNORE_TEST:
            return
        workunit = smt.Workunit(include_conditions=CONDITIONS)
        for value in workunit.values():
            self.assertEqual(len(value), len(CONDITIONS))

    @staticmethod
    def setList(lst):
        if lst is None:
            return []
        else:
            return lst

    def testIterator(self):
        if IGNORE_TEST:
            return
        def test(result_collection=None, include_conditions=None,
              exclude_conditions=None):
            include_conditions = self.setList(include_conditions)
            exclude_conditions = self.setList(exclude_conditions)
            max_size = 4
            for size in range(1, max_size + 1):
                workunit = smt.Workunit(biomodel_num=list(range(10, 10+size)),
                     ts_instance=[1], result_collection=result_collection,
                     include_conditions=include_conditions,
                     exclude_conditions=exclude_conditions)
                self.assertEqual(size, len(list(workunit.iterator)))
            #
        test()
        test(self.result_collection)
        # TODO: tests for overlapping results, includes, excludes

    def testExtend(self):
        if IGNORE_TEST:
            return
        workunit = smt.Workunit(biomodel_num=[1, 2, 3],
              result_collection=self.result_collection.copy())
        workunit1 = smt.Workunit(biomodel_num=[4,2, 6],
              result_collection=self.result_collection.copy())
        workunit.extend(workunit1)
        self.assertEqual(len(workunit[cn.SD_BIOMODEL_NUM]), 5)
        self.assertFalse(5 in workunit[cn.SD_BIOMODEL_NUM])
        self.assertEqual(len(workunit.result_collection),
              2*len(workunit1.result_collection))

    def testSerializeDeserialize(self):
        # TESTING
        workunit = smt.Workunit(**self.conditions[0])
        workunit.serialize()
        new_workunit = self.workunit.deserialize()
        self.assertTrue(workunit.equals(new_workunit))
        #
        workunit = smt.Workunit(**self.conditions[0],
              result_collection=self.result_collection)
        self.assertFalse(workunit.equals(new_workunit))
        import pdb; pdb.set_trace()
    
         


if __name__ == '__main__':
  unittest.main()
