import unittest

from smarte.extended_dict import ExtendedDict

IGNORE_TEST = False
IS_PLOT = False
        

#############################
# Tests
#############################
class TestExtendedDict(unittest.TestCase):

    def setUp(self):
        self.dict = ExtendedDict(a=range(10), b=range(10))

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



if __name__ == '__main__':
  unittest.main()
