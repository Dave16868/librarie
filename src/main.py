import json
from json_conversion import *
import os

import library

print("Booting up librarie...")
if os.path.exists("librarie.json"):
    with open('librarie.json', 'r') as f:
        metadict = json.load(f)
        print(f"Books found: {list(metadict["books"].keys())}")
        print(f"Libraries found: {list(metadict["libraries"].keys())}")
        loaded_books = book_from_dic(metadict["books"])
        loaded_libs = lib_from_dic(metadict["libraries"])
        Book._next_id = metadict["book_next_id"]
        print(f"Books loaded: {list(loaded_books.keys())}")
        print(f"Libraries loaded: {list(loaded_libs.keys())}")
        print("===============testing references================")
        print(f"Book.all_books looks like... {Book.all_books}")
        print(f"the library of book0 is... {Book.all_books[0]._library[0]}")
        print(f"the library of book3 is... {Book.all_books[3]._library[0]}")
        print(f"the repository of moo looks like... {Library.all_libraries["moo"].repository}")
        print(f"the repository of noo looks like... {Library.all_libraries["noo"].repository}")
        print(f"the repository of too looks like... {Library.all_libraries["too"].repository}")
        # this is where I run the GUI program
else: # no save file, simply run GUI
    print("No save file found.")
    # running...        

# implementation of saving and quitting


