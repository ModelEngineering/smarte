import smarte as smt
import SBMLModel as mdl
import fitterpp as fpp
import smarte.constants as cn

import copy
import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = True
IS_PLOT = True
CONDITION = smt.ExperimentCondition(biomodel_num=list(range(10)), ts_instance=1)
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        

#############################
# Tests
#############################
class TestExperimentRunner(unittest.TestCase):

    def init(self):
        self.runner = smt.ExperimentRunner(CONDITION, directory=TEST_DIR)

    def testMakePath(self):
        # TESTING
        path = smt.ExperimentRunner.makePath(CONDITION, TEST_DIR)
        import pdb; pdb.set_trace()

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.init()

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.init()

        

if __name__ == '__main__':
  unittest.main()
