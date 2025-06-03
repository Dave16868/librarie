from tkinter import font
from book import Book
from tkinter import *
from tkinter import ttk
from tkinter import font

class Library():
    all_libraries = {}

    def __init__(self, name, repository=None):
        self.name = name
        self.repository = {} if repository is None else repository
        Library.all_libraries[self.name] = self
        self._root = None

 
    def __repr__(self):
        return f"{self.name} library"

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


    def load_GUI(self, root):
        self._root = root
        self.frame = ttk.Frame(self._root, padding='12 12 12 12')
        self.create_menubar()
        bookids = list(self.repository.keys())
        booknames = []
        for bookid in bookids:
            if bookid in Book.all_books:
                booknames.append(Book.all_books[bookid].title)
        booknamesvar = StringVar(value=booknames)
        lbox = Listbox(self.frame, height=10, listvariable=booknamesvar)
        
        self.frame.grid(row=0, column=0, sticky='nsew')
        lbox.grid(column=0, row=0, sticky='nsew')
    
        self._root.rowconfigure(0 , weight=1)
        self._root.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def create_menubar(self):
        self._root.option_add('*tearOff', FALSE)
        menubar = Menu(self.frame)
        self._root['menu'] = menubar
        new = Menu(menubar)
        edit = Menu(menubar)
        delete = Menu(menubar)
        menubar.add_cascade(menu=new, label='New')
        menubar.add_cascade(menu=edit, label='Edit')
        menubar.add_cascade(menu=delete, label='Delete')
        new.add_command(label='New Book', command=self.create_book)
        edit.add_command(label='Edit Books')


    def create_book(self):
        window = Toplevel(self._root)
        window.title('Book Creation')
        window.attributes('-topmost', 1)
        window.resizable(FALSE, FALSE)

        titlevar = StringVar()
        authorvar = StringVar()
        tagsvar = StringVar()
        statusvar = StringVar()
        tagslist = []
        instruction_font = font.Font(size=7, slant='italic')

        title_label = ttk.Label(window, text='Title of Book', padding='3 3 3 3', anchor='w')
        title_entry = ttk.Entry(window, textvariable=titlevar, width=20)

        author_label = ttk.Label(window, text='Author of Book', padding = '3 3 3 3', anchor='w')
        author_entry = ttk.Entry(window, textvariable=authorvar, width=20)

        tags_label = ttk.Label(window, text='Tags', padding='3 3 3 3', anchor='w')
        tags_entry = ttk.Entry(window, textvariable=tagsvar, width=10)
        tags_frame = ttk.Frame(window, relief='sunken', borderwidth=5, padding='12 12 12 12', width=300, height=300)
        tags_entry.bind('<Return>', lambda x: _create_tag(tagsvar.get(), tagslist, tags_frame, tags_entry))
        tags_label_2 = ttk.Label(window, text='Type in a tag and press Enter to add it. Click on the added tags to delete them.', anchor='nw', font=instruction_font, wraplength=500)

        read_status_label = ttk.Label(window, text='Read Status', padding='3 3 3 3', anchor='w')
        read_status = ttk.Combobox(window, textvariable=statusvar, values=('Unread', 'Reading', 'Finished'), state="readonly")
        read_status.bind("<<ComboboxSelected>>", read_status.selection_clear())

        notes_label = ttk.Label(window, text='Leave a note', padding='3 3 3 3', anchor='w') 
        notes_box = Text(window, width=20, height=5, wrap='word') # get with .get('start', 'end')
        s = ttk.Scrollbar(window, orient=VERTICAL, command=notes_box.yview)
        notes_box.configure(yscrollcommand=s.set)

        savebutton = ttk.Button(window, text='Save')
        cancelbutton = ttk.Button(window, text='Cancel', command= lambda: window.destroy())

        title_label.grid(column=0, row=0, columnspan=2, sticky='w')
        title_entry.grid(column=0, row=1, columnspan=2, sticky='nsew')
        author_label.grid(column=0, row=2, columnspan=2, sticky='w')
        author_entry.grid(column=0, row=3, columnspan=2, sticky='nsew')
        tags_label.grid(column=0, row=4, columnspan=2, sticky='w')
        tags_entry.grid(column=0, row=5, columnspan=2, sticky='nsew')
        tags_frame.grid(column=0, row=6, columnspan=2, sticky='nsew')
        tags_label_2.grid(column=0, row=7, columnspan=2, sticky='nw')
        read_status_label.grid(column=0, row=8, columnspan=2, sticky='w')
        read_status.grid(column=0, row=9, columnspan=2, sticky='nsew')
        notes_label.grid(column=0, row=10, columnspan=2, sticky='w')
        notes_box.grid(column=0, row=11, columnspan=2, sticky='nsew')
        s.grid(column=2, row=11, sticky='ns')
        savebutton.grid(column=0, row=12, sticky='nsew')
        cancelbutton.grid(column=1, row=12, sticky='nsew')

        title_entry.focus()

def _create_tag(tagname, tagslist, tags_frame, tags_entry):
    if tagname:
        tagslist.append(tagname)
        tag_button = ttk.Button(tags_frame, text=tagname, padding='6 6 6 6', command = lambda: _annihilate_button(tagname, tagslist, tags_frame, tag_button))
        tag_button.grid(row=int((len(tagslist)-1) / 3), column=(len(tagslist) + 2) % 3, sticky='snew')
        tags_entry.delete(0, 'end')
    else:
        pass


def _annihilate_button(tagname, tagslist, tags_frame, tag_button):
    tagslist.remove(tagname)
    tag_button.destroy()
    for child in tags_frame.winfo_children():
        child.destroy()
    for i in range(len(tagslist)):
        new_button = ttk.Button(tags_frame, text=tagslist[i], padding='6 6 6 6', command = lambda: _annihilate_button(tagslist[i], tagslist, tags_frame, tag_button))
        new_button.grid(row=int(i / 3), column=((i + 3) % 3), sticky='snew')


