import unittest

from smarte.extended_dict import ExtendedDict, KEY_VALUE_SEP, VALUE_SEP

IGNORE_TEST = True
IS_PLOT = True

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

    def testExtend(self):
        # TESTING
        e_dct = ExtendedDict({"a": [], "b": [1]})
        dct = ExtendedDict(a=[1], b=[])
        e_dct.extend(dct)
        trues = [len(v) == 1 for v in e_dct.values()]
        self.assertTrue(all(trues))
        self.assertEquals(e_dct["a"][0], e_dct["b"][0])

    def testStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.dict)
        self.assertEqual(stg.count(KEY_VALUE_SEP), len(DCT)-1)
        self.assertEqual(stg.count(VALUE_SEP), len(DCT))
        #
        dct = ExtendedDict({"a": [100, 200.2], "b": "testing", "c": 1.04})
        stg = str(dct)
        self.assertEqual(stg.count(KEY_VALUE_SEP), len(dct)-1)
        self.assertEqual(stg.count(VALUE_SEP), len(dct)+1)

    def testEquals(self):
        if IGNORE_TEST:
            return
        self.assertTrue(self.dict.equals(ExtendedDict(DCT)))
        dct = ExtendedDict(DCT)
        del dct["a"]
        self.assertFalse(self.dict.equals(ExtendedDict(dct)))

    def testGet(self):
        if IGNORE_TEST:
            return
        stg = str(self.dict)
        dct = self.dict.getFromStr(stg)
        self.assertTrue(dct.equals(self.dict))
        #
        dct = ExtendedDict({"a": [100, 200.2], "b": "testing", "c": 1.04})
        stg = str(dct)
        new_dct = ExtendedDict.getFromStr(stg)
        self.assertTrue(dct.equals(new_dct))


if __name__ == '__main__':
  unittest.main()
