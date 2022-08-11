import smarte as smt
from smarte.analysis.run_analyzer import RunAnalyzer
from smarte.analysis.replication_analyzer import ReplicationAnalyzer
import SBMLModel as mdl
import fitterpp as fpp
import smarte.constants as cn

import copy
import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False
PATH = os.path.join(cn.EXPERIMENT_DIR,
       "Noise--0.1_ColumnsDeleted--0_RangeMin--0.5_RangeMax--2.0_Maxfev--1000")
        

#############################
# Tests
#############################
class TestRunAalyzer(unittest.TestCase):

    def setUp(self):
        if IGNORE_TEST:
            return
        self.path = PATH
        self.analyzer = RunAnalyzer(PATH)

    def testGetReplications(self):
        if IGNORE_TEST:
            return
        replications = RunAnalyzer.getReplications(PATH)
        for replication in replications:
            self.assertTrue(isinstance(replication, ReplicationAnalyzer))
            self.assertGreater(len(replication.df), 0)

    def testGetConditionDctMkPath(self):
        if IGNORE_TEST:
            return
        path = "Noise--0.1_ColumnsDeleted--0_RangeMin--0.5_RangeMax--2.0_Maxfev--1000"
        condition_dct = RunAnalyzer.getConditionDct(path)
        trues = [c in condition_dct for c in cn.CD_ALL]
        self.assertTrue(all(trues))
        #
        new_path = RunAnalyzer.mkPath(condition_dct)
        self.assertEqual(path, new_path)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        


if __name__ == '__main__':
  unittest.main()
