from smarte.analysis.anova import Anova
import smarte.constants as cn

import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(TEST_DIR, "test_anova.csv")
DF = pd.read_csv(TEST_FILE)
CAT_NUM_SPECIES = "cat_num_species"
values = []
for value in DF[cn.SD_NUM_SPECIES]:
    if (value is None) or (value <= 0) or np.isnan(value):
        new_value = 0
    else:
        new_value = int(np.log10(value))
    values.append(new_value)
DF[CAT_NUM_SPECIES] = values
FACTOR_NAME = CAT_NUM_SPECIES
REPLICATION_NAME = cn.SD_TS_INSTANCE
VALUE_NAME = cn.SD_MEDIAN_ERR
DF = DF[[FACTOR_NAME, REPLICATION_NAME, VALUE_NAME]]
        

#############################
# Tests
#############################
class TestAnova(unittest.TestCase):

    def setUp(self):
        self.anova = Anova(DF, FACTOR_NAME, REPLICATION_NAME, VALUE_NAME)

    def testContructor(self):
        if IGNORE_TEST:
            return
        import pdb; pdb.set_trace()


if __name__ == '__main__':
  unittest.main()
