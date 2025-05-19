import unittest
from book import Book
from library import Library 

class TestLibrary(unittest.TestCase):
    def test_basic_functionality(self):
        libbie = Library("basic")
        libbie.add_book("Dao", "Mark")
        libbie.add_book("Swan", "Nassim")
        libbie.add_book("Goliath", "David")
        self.assertEqual(libbie.repository["Swan"], libbie.find_book("Swan"))
        libbie.del_book("Goliath")
        self.assertEqual(len(libbie.repository), 2)
        blackswan = libbie.find_book("Swan")
        blackswan.edit_title("Black Swan")
        blackswan.edit_author("Nassim Taleb")
        blackswan.add_tags("philosophy", "risk", "intellectualism")
        blackswan.del_tag("intellectualism")
        self.assertEqual(libbie.repository["Black Swan"].tags, ["philosophy", "risk"])
        blackswan.set_start_date(2025, 1, 1)
        blackswan.set_finish_date(2025, 2, 15)
        blackswan.set_finish_date(2025, 12, 31)
        self.assertEqual(libbie.repository["Black Swan"].calculate_time_owned(), 364)

if __name__ == "__main__":
    unittest.main()
