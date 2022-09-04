from smarte.extended_dict import ExtendedDict, VALUE_SEP, LIST_BREAK, KEY_VALUE_SEP

import unittest


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

    def testExtend(self):
        if IGNORE_TEST:
            return
        def test(is_duplicates):
            e_dct = ExtendedDict({"a": [], "b": [1, 1]})
            dct = ExtendedDict(a=[1, 1], b=[])
            e_dct.extend(dct, is_duplicates=is_duplicates)
            if is_duplicates:
                count = 2
            else:
                count = 1
            trues = [len(v) == count for v in e_dct.values()]
            self.assertTrue(all(trues))
            self.assertEquals(e_dct["a"][0], e_dct["b"][0])
        #
        test(False)
        test(True)

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
        #
        dct = ExtendedDict({"a": [100, 200.2, 300, 20, 2, 6], "b": "testing", "c": 1.04})
        stg = str(dct)
        self.assertTrue(LIST_BREAK in stg)
        with self.assertRaises(ValueError):
            _ = ExtendedDict.getFromStr(stg)


if __name__ == '__main__':
  unittest.main()
