from smarte.factor_collection import FactorCollection
from smarte.condition import Condition
import smarte.constants as cn

import os
import pandas as pd
import unittest

IGNORE_TEST = False
IS_PLOT = False

#############################
# Tests
#############################
class TestFactorCollection(unittest.TestCase):

    def setUp(self):
        self.collection = FactorCollection(biomodel_num=[1, 3])

    def testContains(self):
        if IGNORE_TEST:
            return
        # TODO: Finish


if __name__ == '__main__':
  unittest.main()
