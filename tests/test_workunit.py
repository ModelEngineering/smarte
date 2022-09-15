import smarte as smt
import smarte.constants as cn
from smarte.condition_collection import ConditionCollection
from smarte.condition import Condition
from smarte.result import Result
from smarte.factor_collection import FactorCollection
from smarte.workunit import Workunit

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
workunit_str = "biomodel_num--1__columns_deleted--0__max_fev--10000__method--differential_evolution__noise_mag--0.1__latincube_idx--1__range_max_frac--2.0__range_min_frac--0.5__ts_instance--1"
WORKUNIT_STR2  = "biomodel_num--1__columns_deleted--0__max_fev--10000__method--differential_evolution__noise_mag--0.1__latincube_idx--1__range_max_frac--2.0__range_min_frac--0.5__ts_instance--1--2--3--4--5"
WORKUNIT_STR3  = "biomodel_num--all__columns_deleted--0__max_fev--10000__method--differential_evolution__noise_mag--0.1__latincube_idx--1__range_max_frac--2.0__range_min_frac--0.5__ts_instance--all"
CONDITION_COLLECTION = ConditionCollection.makeFromStr(workunit_str)
        

#############################
# Tests
#############################
class TestWorkunit(unittest.TestCase):

    def setUp(self):
        excluded_factor_collection = FactorCollection(ts_instance=[1, 2, 3, 4],
              biomodel_num=list(range(1195)))
        self.workunit = Workunit(excluded_factor_collection=excluded_factor_collection,
              out_dir=TEST_DIR,
              **CONDITION_COLLECTION)
        self.remove()

    def teatDown(self):
        self.remove()

    def remove(self):
        ffiles = os.listdir(TEST_DIR)
        for ffile in ffiles:
            if ffile[0:3] == "wu_":
                path = os.path.join(TEST_DIR, ffile)
                os.remove(path)

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
        workunit = Workunit.makeFromStr(WORKUNIT_STR2)
        conditions = list(workunit.iterate())
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
        result = Result()
        self.workunit.appendResult(result)
        trues = [len(v) == 1 for v in self.workunit.values()]
        self.assertTrue(all(trues))

    def testGetWorkunits(self):
        if IGNORE_TEST:
            return
        self.workunit.serialize()
        workunits = self.workunit.getWorkunits(out_dir=TEST_DIR)
        self.assertEqual(len(workunits), 1)
        self.assertTrue("Workunit" in str(type(workunits[0])))

    def testMakeResultCsv(self):
        if IGNORE_TEST:
            return
        self.workunit.serialize()
        workunit = self.workunit.getWorkunits(out_dir=TEST_DIR)[0]
        workunit.appendResult(Result())
        workunit.appendResult(Result())
        df = workunit.makeResultCsv()
        self.assertEqual(len(df), 2)

    def testCalcMultivaluedFactors(self):
        if IGNORE_TEST:
            return
        workunit = Workunit.makeFromStr(WORKUNIT_STR3)
        factors = workunit.calcMultivaluedFactors()
        diff = set([cn.SD_BIOMODEL_NUM, cn.SD_TS_INSTANCE]).symmetric_difference(
              factors)
        self.assertEqual(len(diff), 0)


if __name__ == '__main__':
  unittest.main()
