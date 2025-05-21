from book import Book
from library import Library

# for each book in Book.all_books, key = book_id, value = all the stats
# put the final dictionary as a value of a dictionary with one key -- "books"
# for each library in Library.all_libraries, key = library_name, value = library stats
# put final dictionary as a value of a dctionary with one key == "libraries"

# remember to separate functionality of books and library. Since 1 book can be under 2 libraries, i want each book to be its own entities, and referenced only by its libraries.

# also all the tests should be messed up now so redo test.
