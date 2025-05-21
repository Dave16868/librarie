from book import Book

class Library():
    all_libraries = {}

    def __init__(self, name):
        self.name = name
        self.repository = {}
        Library.all_libraries[self.name] = self

    def add_book(self, book_id):
        if book_id in Book.all_books:
            self.repository[book_id] = Book.all_books[book_id]
            return True
        print("book_id doesn't exist. Make sure you enter the right one.")
        return False
    
    def del_book(self, book_id):
        if book_id in self.repository:
            del self.repository[book_id]
            return True
        print(f"book_id not found in {self.name}'s repository")
        return False


