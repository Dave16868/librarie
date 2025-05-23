import unittest
from book import Book
from library import Library 

class TestLibrary(unittest.TestCase):
    def test_creation(self):
        moo_lib = Library("moo")
        too_lib = Library("too")
        book1 = Book("red", "power ranger")
        book2 = Book("green", "power ranger")
        book3 = Book("blue", "power ranger")
        moo_lib.add_book(book1._id)
        moo_lib.add_book(book2._id)
        moo_lib.add_book(0)
        moo_lib.del_book(0)
        book2.delete()
        self.assertEqual(len(moo_lib.repository), 1)
        self.assertEqual(len(Book.all_books), 4)

if __name__ == "__main__":
    unittest.main()
