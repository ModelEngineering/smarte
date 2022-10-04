from smarte.analysis import util as ut
import smarte.constants as cn

import os
import pandas as pd
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False
        

#############################
# Tests
#############################
class TestFunction(unittest.TestCase):

    def testSubsetLabels(self):
        if IGNORE_TEST:
            return
        labels = ["a", "bb", "ccc", "dddd", "eeeee"]
        def test(max_label):
            new_labels = ut.subsetLabels(labels, max_label)
            count = len([v for v in new_labels if len(v) > 0])
            self.assertEqual(count, max_label)
        test(5)
        test(2)
        test(4)
 


if __name__ == '__main__':
  unittest.main()
