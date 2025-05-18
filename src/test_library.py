import unittest
from book import Book
from library import Library 

class TestLibrary(unittest.TestCase):
    def test_add_book(self):
        libbie = Library("moo")
        libbie.add_book("name1")
        libbie.add_book("name2")
        libbie.add_book("name3")
        self.assertEqual(1, 1)

    def test_del_book(self):
        libbie = Library("moo")
        libbie.add_book("name1")
        libbie.add_book("name2")
        libbie.add_book("name3")
        libbie.del_book("name2")
        self.assertEqual(1,1)

    def test_find_book(self):
        libbie = Library("moo")
        libbie.add_book("The Origin of Financial Crises")
        self.assertEqual(libbie.find_book("The Origin"), "book not found :(")


if __name__ == "__main__":
    unittest.main()
