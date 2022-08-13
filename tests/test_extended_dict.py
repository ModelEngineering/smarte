import unittest

from smarte.extended_dict import ExtendedDict
import smarte.constants as cn

IGNORE_TEST = False
IS_PLOT = False

DCT = {"a": 100, "b": "testing", "c": 1.04}
        

#############################
# Tests
#############################
class TestExtendedDict(unittest.TestCase):

    def setUp(self):
        self.dict = ExtendedDict(DCT)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue(isinstance(self.dict, dict))

    def testAppend(self):
        if IGNORE_TEST:
            return
        e_dct = ExtendedDict()
        dct = ExtendedDict(a=1, b=2)
        e_dct.append(dct)
        trues = [len(v) == 1 for v in e_dct.values()]
        self.assertTrue(all(trues))
        e_dct.append(dct)
        trues = [len(v) == 2 for v in e_dct.values()]
        self.assertTrue(all(trues))

    def testStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.dict)
        self.assertEqual(stg.count(cn.KEY_VALUE_SEP), len(DCT))

    def testEquals(self):
        if IGNORE_TEST:
            return
        self.assertTrue(self.dict.equals(ExtendedDict(DCT))
        dct = ExtendedDict(DCT)
        del dct["a"]
        self.assertFalse(self.dict.equals(ExtendedDict(dct))

    def testGet(self):
        if IGNORE_TEST:
            return
        stg = str(self.dict)
        dct = self.dict.get(stg)
        self.assertTrue(dct.equals(self.dict))




if __name__ == '__main__':
  unittest.main()
