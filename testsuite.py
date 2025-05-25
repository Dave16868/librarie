import unittest

from test_book import *
from test_library import *
from test_json_conversion import *

suite = unittest.TestSuite()
testcases = [TestBook, TestLibrary, TestJson]
for case in testcases:
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(case))

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
