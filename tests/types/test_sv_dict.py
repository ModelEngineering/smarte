from smarte.types.sv_dict import SVDict

import unittest


IGNORE_TEST = False
IS_PLOT = False

DCT = {"a": 100, "b": "testing", "c": 1.04}


class SVDictTest(SVDict):
    default_dct = {"a": None, "b": None, "c": None}
        

#############################
# Tests
#############################
class TestSVDict(unittest.TestCase):

    def setUp(self):
        self.dict = SVDictTest(**DCT)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertTrue(isinstance(self.dict, dict))
        #
        with self.assertRaises(ValueError):
            self.dict = SVDictTest(d=10)

    def testConstructorList(self):
        if IGNORE_TEST:
            return
        with self.assertRaises(ValueError):
            _ = SVDict(a=100, b=[1, 2, 3])


if __name__ == '__main__':
  unittest.main()
