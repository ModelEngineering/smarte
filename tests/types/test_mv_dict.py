from smarte.types.sv_dict import SVDict
from smarte.types.mv_dict import MVDict, ALL
from smarte.types.elemental_type import isList

import unittest


IGNORE_TEST = False
IS_PLOT = False

DCT = {"a": [100], "b": "testing", "c": ALL}


class SVDictTest(SVDict):
    default_dct = {"a": None, "b": None, "c": None}

class MVDictTest(MVDict):
    default_dct = {"a": [], "b": [], "c": []}
    expansion_dct = {"c": list(range(4))}
        

#############################
# Tests
#############################
class TestMVDict(unittest.TestCase):

    def setUp(self):
        self.dict = MVDictTest(**DCT)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        trues = [isList(v) for v in self.dict.values()]
        self.assertTrue(all(trues))
        self.assertGreater(len(self.dict["c"]), 1)

    def testAppend(self):
        if IGNORE_TEST:
            return
        e_dct = MVDictTest()
        dct = SVDictTest(a=1, b=2)
        e_dct.append(dct)
        trues = [len(v) == 1 for v in e_dct.values()]
        self.assertTrue(all(trues))
        e_dct.append(dct)
        trues = [len(v) == 2 for v in e_dct.values()]
        self.assertTrue(all(trues))

    def testExtend(self):
        if IGNORE_TEST:
            return
        def test():
            e_dct = MVDictTest()
            e_dct = MVDictTest(a=[], b=[1, 1])
            dct = MVDictTest(a=[1, 1], b=[], c=[2,2])
            e_dct.extend(dct)
            count = 2
            trues = [len(v) == count for v in e_dct.values()]
            self.assertTrue(all(trues))
            self.assertEquals(e_dct["a"][0], e_dct["b"][0])
        #
        test()

if __name__ == '__main__':
  unittest.main()
