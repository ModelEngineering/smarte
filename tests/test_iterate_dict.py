from smarte.iterate_dict import iterateDict
import smarte.constants as cn

import numpy as np
import unittest

IGNORE_TEST = True
IS_PLOT = True
DCT = {"a": [1, 2], "b": [10], "c": list(range(10))}
COUNT = np.prod([len(v) for v in DCT.values()])
        

#############################
# Tests
#############################
class TestIteratorDict(unittest.TestCase):

    def setUp(self):
        self.iterator = iterateDict(DCT)

    def testIterate1(self):
        # TESTING
        dcts = list(self.iterator)
        self.assertEqual(len(dcts), COUNT)

if __name__ == '__main__':
  unittest.main()
