import unittest
from book import Book

class TestBook(unittest.TestCase):
    def test_creation(self):
        book1 = Book("The Origin of Financial Crises", "George Cooper")
        book2 = Book("name of book 2", "author of book2")
        book3 = Book("name of book 3", "author of book3")
        book2.delete()
        self.assertEqual(len(Book.all_books), 2)
        book3.edit_title("Joe")
        book3.edit_author("Dart")
        self.assertEqual(book3.title, "Joe")
        self.assertEqual(book3.author, "Dart")
        book3.add_tags("tag1", "tag2")
        book3.del_tag("tag2")
        self.assertEqual(book3.tags, ["tag1"])
        book3.set_read_status("Reading")
        self.assertEqual(book3.read_status, "Reading")
        book3.edit_note("white")
        self.assertEqual(book3.notes, "white")
        self.assertEqual(len(Book.all_books), 2)

if __name__ == "__main__":
    unittest.main()

