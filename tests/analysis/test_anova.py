from smarte.analysis import anova as anv
import smarte.constants as cn

import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(TEST_DIR, "test_anova.csv")
DF_FULL = pd.read_csv(TEST_FILE)
CAT_NUM_SPECIES = "cat_num_species"
values = []
for value in DF_FULL[cn.SD_NUM_SPECIES]:
    if (value is None) or (value <= 0) or np.isnan(value):
        new_value = 0
    else:
        new_value = int(np.log10(value))
    values.append(new_value)
DF_FULL[CAT_NUM_SPECIES] = values
FACTOR_NAME = CAT_NUM_SPECIES
REPLICATION_NAME = cn.SD_TS_INSTANCE
VALUE_NAME = cn.SD_MEDIAN_ERR
DF = DF_FULL[[FACTOR_NAME, REPLICATION_NAME, VALUE_NAME]]
        

#############################
# Tests
#############################
class TestAnova(unittest.TestCase):

    def setUp(self):
        self.anova = anv.Anova(DF, FACTOR_NAME, REPLICATION_NAME, VALUE_NAME)

    def testContructor(self):
        if IGNORE_TEST:
            return
        self.assertGreater(self.anova.fstat.sl, 0)

    def testCalcSl1(self):
        if IGNORE_TEST:
            return
        sl_ser = anv.Anova.calcSl([cn.SD_MAX_FEV, cn.SD_METHOD], DF_FULL, FACTOR_NAME,
              REPLICATION_NAME, VALUE_NAME)
        self.assertEqual(len(sl_ser), 2)

    def testCalcSl2(self):
        if IGNORE_TEST:
            return
        instance_names = [cn.SD_BIOMODEL_NUM, cn.SD_MAX_FEV, cn.SD_METHOD]
        sl_ser = anv.Anova.calcSl(instance_names, 
              DF_FULL, FACTOR_NAME, REPLICATION_NAME, VALUE_NAME)
        indices = list(sl_ser.index)
        self.assertEqual(indices[0].count(anv.SEPARATOR), len(instance_names) - 1)
        ser = sl_ser[sl_ser < 1.0]
        self.assertEqual(len(ser), 1)


if __name__ == '__main__':
  unittest.main()
