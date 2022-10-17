from smarte import util as ut

import pandas as pd
import unittest


IGNORE_TEST = False
IS_PLOT = False
        

#############################
# Tests
#############################
class TestFunctions(unittest.TestCase):


    def testCleanDf(self):
        if IGNORE_TEST:
            return
        df = pd.DataFrame({
              "a": range(5),
              "b": range(5),
              ut.INDEX: range(5),
              ut.UNNAMED: range(5),
              })
        new_df = ut.cleanDf(df)
        self.assertEqual(len(new_df.columns), len(df.columns) - 2)
        #
        new_df = ut.cleanDf(df, others=["a"])
        self.assertEqual(len(new_df.columns), len(df.columns) - 3)
              

if __name__ == '__main__':
  unittest.main()
