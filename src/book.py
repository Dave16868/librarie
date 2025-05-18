from datetime import date, timedelta
from re import error

class Book:
    def __init__(self, title, author, tags=None, start_date=None, finish_date=None, read_status="Unread", notes=None):
        self.title = title
        self.author = author
        self.tags = tags
        self.start_date = start_date
        self.finish_date = finish_date
        self.read_status = read_status
        self.notes = notes

    def __repr__(self):
        return f"{self.title} by {self.author}.\ntags: {self.tags}.\nread status : {self.read_status}.\nstart date : {self.start_date}.\nfinish date : {self.finish_date}."

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

    def set_start_date(self, year, month, day):
        self.start_date = date(year, month, day)

    def set_finish_date(self, year, month, day):
        self.finish_date = date(year, month, day)

    def calculate_time_owned(self):
        date1 = self.start_date
        date2 = self.finish_date
        delta = date2 - date1
        return delta.days

