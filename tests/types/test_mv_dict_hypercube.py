from smarte.types.mv_dict_hypercube import MVDictHypercube
from smarte.types.elemental_type import isList

import unittest


IGNORE_TEST = False
IS_PLOT = False

DCT = dict(a=[1, 2], b=[10], c="all")

class MVDictHypercubeTest(MVDictHypercube):
    default_dct = {k: [] for k in DCT.keys()}
    expansion_dct = {"c": list(range(4))}
        

#############################
# Tests
#############################
class TestMVDictHypercube(unittest.TestCase):

    def setUp(self):
        self.dict = MVDictHypercubeTest(**DCT)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        trues = [isList(v) for v in self.dict.values()]
        self.assertTrue(all(trues))
        self.assertEqual(len(self.dict["c"]),
              len(MVDictHypercubeTest.expansion_dct["c"]))

    def testExtend(self):
        if IGNORE_TEST:
            return
        dct = self.dict.copy()
        dct.extend(self.dict)
        for key, value in dct.items():
            self.assertEqual(2*len(self.dict[key]), len(value))

    def testMakeMVDictTable(self):
        if IGNORE_TEST:
            return
        mv_dict_table = self.dict.makeMVDictTable()
        length = len(self.dict)
        self.assertEqual(length, len(mv_dict_table))


if __name__ == '__main__':
  unittest.main()
