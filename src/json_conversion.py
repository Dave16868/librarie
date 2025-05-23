from book import Book
from library import Library

def book_to_dic():
    converted_books = {}
    for book_id,book in Book.all_books.items():
        converted_books[book_id] = {
            "title": book.title,
            "author": book.author,
            "library": book._library,
            "id": book._id,
            "tags": book.tags,
            "start_date": book.start_date,
            "finish_date": book.finish_date,
            "read_status": book.read_status,
            "notes": book.notes
        }
    converted_books["_next_id"] = Book._next_id
    return converted_books

def lib_to_dic():
    converted_libraries = {}
    for lib_name,lib in Library.all_libraries.items():
        lib_keys = [] # get list of each library object's repository keys (book ids)
        for key in lib.repository:
            lib_keys.append(key)
        converted_libraries[lib_name] = {
            "name": lib.name,
            "repository": lib_keys # repository is now a list of book_ids
        }
    return converted_libraries

def all_to_dic():
    converted_books = book_to_dic()
    converted_libraries = lib_to_dic()
    return {
        "books": converted_books,
        "libraries": converted_libraries
    }

def book_from_dic(converted_books):
    for book_id,book in converted_books.items():
        Book(book["title"], book["author"], book["library"], book["id"], book["tags"], book["start_date"], book["finish_date"], book["read_status"], book["notes"])
    Book._next_id = converted_books["_next_id"]

def lib_from_dic(converted_libraries):
    for lib_name,lib in converted_libraries.items():
        Library(lib["name"], lib["repository"])


