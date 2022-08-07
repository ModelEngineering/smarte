import smarte as smt
from smarte.analysis.run_analyzer import ReplicationAnalyzer, RunAnalyzer
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
DIR = os.path.join(cn.EXPERIMENT_DIR,
       "Noise--0.1_ColumnsDeleted--0_MinMax--0.25-4.0_Maxfev--1000")
FFILE = os.path.join(DIR, "1.csv")

        

#############################
# Tests
#############################
class TestReplicationAnalyzer(unittest.TestCase):

    def setUp(self):
        self.ffile = FFILE
        self.analyzer = ReplicationAnalyzer(FFILE)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        import pdb; pdb.set_trace()
        


if __name__ == '__main__':
  unittest.main()
