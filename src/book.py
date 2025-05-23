from datetime import date, timedelta
from re import error

class Book:
    all_books = {}
    _next_id = 0

    def __init__(self, title, author, library=None, id=None, tags=None, start_date=None, finish_date=None, read_status="Unread", notes=None):
        self._library = [] if library is None else library
        if id is None:
            self._id = Book._next_id
            Book._next_id += 1
        else:
            self._id = id
        Book.all_books[self._id] = self
        self.title = title
        self.author = author
        self.tags = tags
        self.start_date = start_date
        self.finish_date = finish_date
        self.read_status = read_status
        self.notes = notes

    def __str__(self):
        return f"A BOOK NAMED {self.title}"

    def __repr__(self):
        return f"{self.title} by {self.author}.\n library: {self._library}.\n id: {self._id}\n"

    def delete(self):
        for libr in self._library:
           libr.del_book(self._id)
        return Book.all_books.pop(self._id)

    def edit(self, **kwargs):
        changed_attributes = []
        for kwarg in kwargs:
            if kwarg not in vars(self):
                print(f"Books do not have this attribute ---> {kwarg} !")
                continue
            setattr(self, f"{kwarg}", kwargs[kwarg])
            changed_attributes.append(kwarg)
        print(f"list of attributes successfully editted: {changed_attributes}")

    def edit_title(self, new_title):
        self.title = new_title
        return True

    def edit_author(self, new_author):
        self.author = new_author
        return True

    def add_tags(self, *tags):
        added_tags = []
        if type(self.tags) != list:
            self.tags = []
        for tag in tags:
            if isinstance(tag, (str, int)):
                self.tags.append(tag)
                added_tags.append(tag)
            else:
                print(f"'{tag} is not a valid tag ---> strings or integers only")
                continue
        print(f"added tags: {added_tags} to {self.title}'s tags")
        return added_tags

    def del_tag(self, tag):
        if not self.tags:
            print(f"book has no tags")
            return False
        if tag not in self.tags:
            print(f"tag not found in {self.title}")
            return False
        self.tags.remove(tag)
        print(f"removed tag '{tag}', remaining tags: {self.tags}")
        return True

    def set_read_status(self, status):
        if isinstance(status, str):
            self.read_status = status.capitalize()
            print(f"set status of {self.title} to : {self.read_status}")
            return True
        print("unable to set status, kindly enter a string")
        return False

    def edit_note(self, note):
        self.notes = note
        return True

    def set_start_date(self, year, month, day):
        self.start_date = date(year, month, day)

    def set_finish_date(self, year, month, day):
        self.finish_date = date(year, month, day)

    def calculate_read_time(self):
        date1 = self.start_date
        date2 = self.finish_date
        delta = date2 - date1
        return delta.days

