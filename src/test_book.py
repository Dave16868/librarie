import unittest
from bookClass import Book

class TestBook(unittest.TestCase):
    def test_creation(self):
        book1 = Book("The Origin of Financial Crises", "George Cooper")
        print(book1.__repr__())
        book1.edit_book(title="Safe Haven Investing", author="Mark Spitznagel")
        print(book1.__repr__())
        book1.set_start_date(2025, 3, 1)
        book1.set_finish_date(2025, 5, 1)
        print(book1.__repr__())

        self.assertEqual(1,1)

    def test_calculate_time(self):
        book1 = Book("Diary of a Wimpy Kid", "Wimpy Kid")
        book1.set_start_date(2025, 5, 1)
        book1.set_finish_date(2025, 5, 31)
        self.assertEqual(book1.calculate_time_owned(), 30)

if __name__ == "__main__":
    unittest.main()

