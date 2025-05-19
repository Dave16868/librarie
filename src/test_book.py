import unittest
from book import Book

class TestBook(unittest.TestCase):
    def test_creation(self):
        book1 = Book("The Origin of Financial Crises", "George Cooper")
        book1.edit(title="Safe Haven Investing", author="Mark Spitznagel")

        self.assertEqual(1,1)

    def test_calculate_time(self):
        book1 = Book("Diary of a Wimpy Kid", "Wimpy Kid")
        book1.set_start_date(2025, 5, 1)
        book1.set_finish_date(2025, 5, 31)
        self.assertEqual(book1.calculate_read_time(), 30)

    def test_add_tags(self):
        book1 = Book("Diary of a Wimpy Kid", "Wimpy Kid")
        book1.add_tags("comedy", "biography")
        self.assertEqual(book1.tags, ["comedy", "biography"])

    def test_del_tags(self):
        book2 = Book("Mein Kampf", "Hitler")
        book2.add_tags("gore", "horror")
        book2.del_tag("gore")
        self.assertEqual(book2.tags, ["horror"])


if __name__ == "__main__":
    unittest.main()

