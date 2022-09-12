from smarte.types.elemental_dict import ElementalDict,  \
      VALUE_SEP, LIST_BREAK, KEY_VALUE_SEP

import unittest


IGNORE_TEST = False
IS_PLOT = False

DCT = {"a": 100, "b": "testing", "c": 1.04}
        

#############################
# Tests
#############################
class TestElementalDict(unittest.TestCase):

    def setUp(self):
        self.dict = ElementalDict(**DCT)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue(isinstance(self.dict, dict))

    def testStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.dict)
        self.assertEqual(stg.count(KEY_VALUE_SEP), len(DCT)-1)
        self.assertEqual(stg.count(VALUE_SEP), len(DCT))
        #
        dct = ElementalDict(a=[100, 200.2], b="testing", c=1.04)
        stg = str(dct)
        self.assertEqual(stg.count(KEY_VALUE_SEP), len(dct)-1)
        self.assertEqual(stg.count(VALUE_SEP), len(dct)+1)

    def testEquals(self):
        if IGNORE_TEST:
            return
        self.assertTrue(self.dict.equals(ElementalDict(**DCT)))
        dct = ElementalDict(**DCT)
        del dct["a"]
        self.assertFalse(self.dict.equals(ElementalDict(**dct)))

    def tesMakeFromStr(self):
        if IGNORE_TEST:
            return
        stg = str(self.dict)
        dct = self.dict.makeFromStr(stg)
        self.assertTrue(dct.equals(self.dict))
        #
        dct = ElementalDict(a=[100, 200.2], b="testing", c=1.04)
        stg = str(dct)
        new_dct = ElementalDict.makeFromStr(stg)
        self.assertTrue(dct.equals(new_dct))
        #
        dct = ElementalDict(a=[100, 200.2, 300, 20, 2, 6], b="testing", c=1.04)
        stg = str(dct)
        self.assertTrue(LIST_BREAK in stg)
        with self.assertRaises(ValueError):
            _ = ElementalDict.makeFromStr(stg)


if __name__ == '__main__':
  unittest.main()
