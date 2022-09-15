import smarte as smt
import smarte.constants as cn
from smarte.condition_collection import ConditionCollection
from smarte.condition import Condition
from smarte.factor_collection import FactorCollection
from smarte.workunit import Workunit

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
workunit_str = "biomodel_num--all__columns_deleted--0__max_fev--10000__method--differential_evolution__noise_mag--0.1__latincube_idx--1__range_max_frac--2.0__range_min_frac--0.5__ts_instance--all"
CONDITION_COLLECTION = ConditionCollection.makeFromStr(workunit_str)
        

#############################
# Tests
#############################
class TestWorkunit(unittest.TestCase):

    def setUp(self):
        excluded_factor_levels = FactorCollection(ts_instance=[1, 2, 3, 4],
              biomodel_num=list(range(1195)))
        self.workunit = Workunit(excluded_factor_levels=excluded_factor_levels,
              **CONDITION_COLLECTION)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        special_factors = [cn.SD_BIOMODEL_NUM, cn.SD_TS_INSTANCE]
        for factor in cn.SD_CONDITIONS:
            if not factor in special_factors:
                self.assertEqual(len(self.workunit[factor]), 1)

    def testIterator(self):
        if IGNORE_TEST:
            return
        conditions = list(self.workunit.iterate())
        trues = [isinstance(c, Condition) for c in conditions]
        self.assertTrue(all(trues))
        self.assertEqual(len(conditions), 5)

    def testSerializeDeserializeEquals(self):
        if IGNORE_TEST:
            return
        self.workunit.serialize()
        new_workunit = self.workunit.deserialize(self.workunit.persister_path)
        self.assertTrue(self.workunit.equals(new_workunit))

    def testAppendResult(self):
        if IGNORE_TEST:
            return
        raise RuntimeError("No test")

    def testGetWorkunits(self):
        if IGNORE_TEST:
            return
        raise RuntimeError("No test")

    def testMakeResultCsv(self):
        if IGNORE_TEST:
            return
        raise RuntimeError("No test")

    def testCalcMultivaluedFactors(self):
        if IGNORE_TEST:
            return
        raise RuntimeError("No test")


if __name__ == '__main__':
  unittest.main()
