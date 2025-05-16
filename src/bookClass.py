from datetime import date, timedelta

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

    def edit_book(self, **kwargs):
        for kwarg in kwargs:
            if kwarg not in vars(self):
                print(f"Books do not have this attribute ---> {kwarg} !")
                continue
            setattr(self, f"{kwarg}", kwargs[kwarg])

    def set_start_date(self, year, month, day):
        self.start_date = date(year, month, day)

    def set_finish_date(self, year, month, day):
        self.finish_date = date(year, month, day)

    def calculate_time_owned(self):
        date1 = self.start_date
        date2 = self.finish_date
        delta = date2 - date1
        return delta.days

