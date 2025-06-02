from book import Book

class Library():
    all_libraries = {}

    def __init__(self, name, repository=None):
        self.name = name
        self.repository = {} if repository is None else repository
        Library.all_libraries[self.name] = self

 
    def __repr__(self):
        return f"{self.name} library"
    
    def load_GUI(self):

 

    def delete(self):
        booklist = list(self.repository.keys())
        for book_id in booklist:
            self.del_book(book_id)
        return Library.all_libraries.pop(self.name)

    def add_book(self, book_id):
        if book_id in Book.all_books:
            book_to_add = Book.all_books[book_id]
            self.repository[book_id] = book_to_add
            book_to_add._library.append(self)
            return True
        print("book_id doesn't exist. Make sure you enter the right one.")
        return False
    
    def del_book(self, book_id):
        if book_id in self.repository:
            book_to_del = Book.all_books[book_id]
            book_to_del._library.remove(self)
            del self.repository[book_id]
            return True
        print(f"book_id not found in {self.name}'s repository")
        return False


