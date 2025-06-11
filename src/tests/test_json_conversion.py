from json_conversion import *
from library import Library
from book import Book
import unittest

class TestJson(unittest.TestCase):
    def test_booktodic(self):
        bookdicked = book_to_dic()
        self.assertEqual(True, isinstance(bookdicked, dict))

    def test_libtodic(self):
        libdicked = lib_to_dic()
        self.assertEqual(True, isinstance(libdicked, dict))

    def test_alltodic(self):
        jsonformat = all_to_dic()
        self.assertEqual(True, isinstance(jsonformat, dict))






if __name__ == "__main__":
    unittest.main()
