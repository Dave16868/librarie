from json_conversion import book_to_dic, lib_to_dic
from library import Library
from book import Book
import unittest

class TestJson(unittest.TestCase):
    def test_booktodic(self):
        dicked = book_to_dic()
        self.assertEqual(True, isinstance(dicked, dict))

    def test_libtodic(self):
        libbed = lib_to_dic()
        print(libbed)
        self.assertEqual(True, isinstance(libbed, dict))


if __name__ == "__main__":
    unittest.main()
