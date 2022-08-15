from smarte.iterate_dict import iterateDict
import smarte.constants as cn

import numpy as np
import unittest

IGNORE_TEST = False
IS_PLOT = False
DCT = {"a": [1, 2], "b": [10], "c": list(range(10))}
DCT2 = {"a": 1, "b": [10], "c": list(range(10))}
COUNT = np.prod([len(v) for v in DCT.values()])
COUNT2 = COUNT / 2
        

#############################
# Tests
#############################
class TestIteratorDict(unittest.TestCase):

    def setUp(self):
        self.iterator = iterateDict(DCT)

    def testIterate1(self):
        if IGNORE_TEST:
            return
        dcts = list(self.iterator)
        self.assertEqual(len(dcts), COUNT)

    def testIterate2(self):
        if IGNORE_TEST:
            return
        iterator = iterateDict(DCT2)
        dcts = list(iterator)
        self.assertEqual(len(dcts), COUNT2)

if __name__ == '__main__':
  unittest.main()
