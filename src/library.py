from book import Book

class Library():
    def __init__(self, name):
        self.name = name
        self.repository = {}

    def add_book(self, title, author="Anon"):
        new_book = Book(title, author, library=self) 
        self.repository[title] = new_book
        return self.repository[title]
    
    def del_book(self, title):
        if title in self.repository:
            del self.repository[title]
            return True
        print(f"book '{title}' not found in {self.name}'s repository")
        return False

    def find_book(self, title):
        return self.repository.get(title, "book not found :(")

