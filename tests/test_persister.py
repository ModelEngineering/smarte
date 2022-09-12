import smarte.persister as per

import os
import unittest

IGNORE_TEST = False
IS_PLOT = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(TEST_DIR, "test_persister.pcl")
LIST = list(range(10))
REMOVE_FILES = [TEST_PATH]
        

#############################
# Tests
#############################
class TestPersister(unittest.TestCase):

    def setUp(self):
        self.persister = per.Persister(TEST_PATH)
        self.remove()

    def tearDown(self):
        self.remove()

    def remove(self):
        for ffile in REMOVE_FILES:
            if os.path.isfile(ffile):
                os.remove(ffile)

    def testConstructor(self):
        if IGNORE_TEST:
            return
        self.assertEqual(self.persister.path, TEST_PATH)

    def testDumpLoad(self):
        if IGNORE_TEST:
            return
        self.persister.dump(LIST)
        lst = self.persister.load()
        self.assertTrue([x == y for x, y in zip(lst, LIST)])
        self.assertTrue(self.persister.isExist())

    def testRemove(self):
        if IGNORE_TEST:
            return
        self.persister.dump(LIST)
        self.persister.delete()
        self.assertFalse(self.persister.isExist())
    
        
    


if __name__ == '__main__':
  unittest.main()
