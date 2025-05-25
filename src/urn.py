from library import Library
from book import Book
from json_conversion import *
import json

book1 = Book("The Origin of Financial Crises", "George Cooper")
book2 = Book("name of book 2", "author of book2")
book3 = Book("name of book 3", "author of book3")
book4 = Book("red", "power ranger")
book5 = Book("green", "power ranger")
book6 = Book("blue", "power ranger")

moo_lib = Library("moo")
too_lib = Library("too")
noo_lib = Library("noo")

moo_lib.add_book(book1._id)
moo_lib.add_book(book2._id)
moo_lib.add_book(book3._id)
too_lib.add_book(book4._id)
too_lib.add_book(book5._id)
too_lib.add_book(book6._id)

json_format = all_to_dic()
with open("librarie.json", 'w') as f:
    json.dump(json_format, f)
