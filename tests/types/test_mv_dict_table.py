from smarte.types.sv_dict import SVDict
from smarte.types.mv_dict import MVDict, ALL
from smarte.types.mv_dict_table import MVDictTable
from smarte.types.elemental_type import isList

import copy
import numpy as np
import unittest


IGNORE_TEST = False
IS_PLOT = False

DCT = {"a": [100], "b": "testing", "c": ALL}


class SVDictTest(SVDict):
    default_dct = {"a": None, "b": None, "c": None}

class MVDictTableTest(MVDictTable):
    default_dct = {"a": [], "b": [], "c": []}

SIZE = 10
ARR = np.array(range(SIZE))
MV_DICT_TABLE = MVDictTableTest(
    a=list(ARR), b=list(10*ARR), c= list(100*ARR))
        

#############################
# Tests
#############################
class TestMVDictTable(unittest.TestCase):

    def setUp(self):
        self.dict = copy.deepcopy(MV_DICT_TABLE)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        trues = [len(v) == SIZE for v in self.dict.values()]
        self.assertTrue(all(trues))
        #
        with self.assertRaises(ValueError):
            _ = MVDictTableTest(a=list(ARR), b=list(10*ARR), c=list(ARR)[1:])

    def testIterate(self):
        if IGNORE_TEST:
            return
        sv_dicts = list(self.dict.iterate(SVDictTest))
        self.assertEqual(len(sv_dicts), SIZE)
        trues = [isinstance(e, SVDictTest) for e in sv_dicts]
        self.assertTrue(all(trues))

    def testMakeFromSVDicts(self):
        if IGNORE_TEST:
            return
        sv_dicts = list(self.dict.iterate(SVDictTest))
        mv_dict_table = MVDictTableTest.makeFromSVDicts(sv_dicts)
        self.assertTrue(self.dict.equals(mv_dict_table))


if __name__ == '__main__':
  unittest.main()
