from tkinter import font
from book import Book
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

class Library():
    all_libraries = {}

    def __init__(self, name, repository=None):
        self.name = name
        self.repository = {} if repository is None else repository
        Library.all_libraries[self.name] = self
        self._root = None
 
    def __repr__(self):
        return f"{self.name} library"

    def booknames(self):
        return [Book.all_books[bookid].title for bookid in self.repository if bookid in Book.all_books]

    def booknames_all(self):
        return [Book.all_books[bookid].title for bookid in Book.all_books]

    def find_bookid(self, bookname):
        if bookname in self.booknames_all():
            for book in Book.all_books.values():
                if bookname == book.title:
                    return book._id
        else:
            print("Book name not found int list of names.")
            return False

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
        booknamesvar = StringVar(value=self.booknames())
        lbox = Listbox(self.frame, height=10, listvariable=booknamesvar)
        
        self.frame.grid(row=0, column=0, sticky='nsew')
        lbox.grid(column=0, row=0, sticky='nsew')
    
        self._root.rowconfigure(0 , weight=1)
        self._root.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def create_menubar(self):
        if self._root is not None:
            self._root.option_add('*tearOff', FALSE)
            menubar = Menu(self.frame)
            self._root['menu'] = menubar
            new = Menu(menubar)
            edit = Menu(menubar)
            switch = Menu(menubar)
            menubar.add_cascade(menu=new, label='New')
            menubar.add_cascade(menu=edit, label='Edit')
            menubar.add_cascade(menu=switch, label='Switch')
            new.add_command(label='Create Book', command = lambda: GUI_create_book(self._root))
            edit.add_command(label='Manage Books and Libraries', command = lambda: self.GUI_manage())
            for librname in Library.all_libraries:
                switch.add_command(label=f'{librname}', command = lambda name=librname: self.switch_libr(name))

    def GUI_manage(self):
        window = Toplevel(self._root)
        window.title(f'Manage books in {self.name}')
        window.attributes('-topmost', 1)
        windowframe = ttk.Frame(window, padding='12 12 12 12')

        treestyle = ttk.Style()
        treestyle.configure("Treeview", rowheight=40)
        tree = ttk.Treeview(windowframe, columns=('Author', 'Status', 'Tags'))
        tree.heading('Author', text='Author')
        tree.heading('Status', text='Status')
        tree.heading('Tags', text='Tags')
        tree.column('Author', anchor='center')
        tree.column('Status', anchor='center')
        tree.column('Tags', anchor='center')
        s = ttk.Scrollbar(tree, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=s.set)

        tree.tag_configure('library', background='grey50')

        self._generate_tree(tree)

        addlib = ttk.Button(windowframe, text='Add library', padding='6 6 6 6', command = lambda: self.tree_add_libr(tree))
        dellib = ttk.Button(windowframe, text='Delete Library', padding='6 6 6 6', command = lambda: self.tree_del_libr(tree))
        addbook = ttk.Button(windowframe, text='Add Book To ...', padding='6 6 6 6', command= lambda: self.tree_add_book(tree, window))
        delbook = ttk.Button(windowframe, text='Delete Book', padding='6 6 6 6')

        windowframe.grid(row=0, column=0, sticky='nsew')
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        tree.grid(row=0, column=0, sticky='nsew', columnspan=4)
        addlib.grid(row=2, column=0, sticky='nsew')
        dellib.grid(row=2, column=1, sticky='nsew')
        addbook.grid(row=2, column=2, sticky='nsew')
        windowframe.rowconfigure(0, weight=1)
        windowframe.columnconfigure([0,1,2,3], weight=1)

    def switch_libr(self, librname):
        if self._root is not None:
            self.frame.destroy()
            libr = Library.all_libraries[librname]
            libr.load_GUI(self._root)


    def tree_add_libr(self, tree):
        namebox = Toplevel(self.frame)
        namebox.title("Library Creation")
        namebox.attributes("-topmost", 1)
        namebox.resizable(FALSE, FALSE)
        label1 = ttk.Label(namebox, text="Name your library", padding='3 3 3 3', anchor='center')
        librname = StringVar()
        entry1 = ttk.Entry(namebox, textvariable=librname, width=10)
        entry1.focus()
        namebox.bind('<Return>', lambda x: self.tree_create_libr(namebox, entry1.get(), tree))

        label1.grid()
        entry1.grid()

    def tree_create_libr(self, window, librname, tree):
        if not librname:
            messagebox.showinfo(message='Please enter a name', parent=window)
        elif librname in Library.all_libraries:
            messagebox.showinfo(message='Library name already in use', parent=window)
        else:
            Library(librname)
            self._generate_tree(tree)
            print(f"added library: {librname}")
            window.destroy()

    def tree_del_libr(self, tree):
        selection = tree.selection()
        tree_item = selection[0]
        print(f"tis is tree_item_name: {tree_item}")
        if len(selection) != 1:
            print("Treeview selection should highlight 1 item.")
        elif tree_item not in Library.all_libraries:
            print("Please select only libraries to delete.")
        else:
            Library.all_libraries[tree_item].delete()
            self._generate_tree(tree)
            print(f"deleted library: {tree_item}")

    def tree_add_book(self, tree, window):
        selection = tree.selection()
        tree_item = selection[0]
        tree_item_name = tree.item(tree_item, option='text')
        if len(selection) != 1:
            print("Treeview selection should highlight 1 item.")
        elif tree_item_name not in self.booknames_all():
            print("Select a book in order to add it to other libraries.")
            messagebox.showinfo(message="Select a book in order to add it to other libraries.", parent=window)
        else:
            addlocation = Toplevel(window)
            addlocation.title("Choose a location")
            addlocation.attributes("-topmost", 1)
            addlocation.resizable(FALSE, FALSE)
            label1 = ttk.Label(addlocation, text="Choose a library to add your book.", padding='3 3 3 3', anchor='center')
            frame1 = ttk.Frame(addlocation, relief='raised', borderwidth=5, padding='18 18 18 18')
            label1.grid(column=0, row=0, columnspan=2, sticky='nws')
            frame1.grid(column=0, row=1, columnspan=2, sticky='nsew')
            
            i = 0
            checkbutton_style = ttk.Style(window)
            checkbutton_style.configure("Bigfont.TCheckbutton", font=('TkMenuFont', 14))
            self.libr_bool = []
            for librname, libr in Library.all_libraries.items():
                booknames = libr.booknames()
                boolvar = BooleanVar(value=(True if tree_item_name in booknames else False))
                self.libr_bool.append(boolvar)
                librtoggle = ttk.Checkbutton(frame1, text=f'{librname}', variable=boolvar, onvalue=True, offvalue=False, style="Bigfont.TCheckbutton")
                librtoggle.grid(column=0, row=2+i, columnspan=2, sticky='nsew')
                i += 1
            
            savebutton = ttk.Button(addlocation, text="Save", padding='3 3 3 3', command = lambda: self.tree_save_book(addlocation, tree, frame1, tree_item_name))
            cancelbutton = ttk.Button(addlocation, text="Cancel", padding='3 3 3 3')

            savebutton.grid(column=0, row=i, sticky='wnes')
            cancelbutton.grid(column=1, row=i, sticky='wnes')

    def tree_save_book(self, window, tree, frame, tree_item_name):
        for i, child in enumerate(frame.winfo_children()):
            librname = child['text']
            libr = Library.all_libraries[librname]
            print(f"i: {i}, child: {child}, librname: {librname}, libr: {libr}, self.libr_bool[i]: {self.libr_bool[i]}, tree_item_name: {tree_item_name}")
            if self.libr_bool[i].get() is True and tree_item_name not in libr.booknames():
                bookid = self.find_bookid(tree_item_name)
                libr.add_book(bookid)
            elif self.libr_bool[i].get() is False and tree_item_name in libr.booknames():
                bookid = self.find_bookid(tree_item_name)
                libr.del_book(bookid)
            else: 
                print(f"No change to {librname}")
        self._generate_tree(tree)
        self.libr_bool = [] # reset to empty
        window.destroy()


    def _generate_tree(self, tree):
        for item in tree.get_children(''):
            tree.delete(item)
        for librname, libr in Library.all_libraries.items():
            tree.insert('', 'end', librname, text=f'{librname} ({len(libr.repository.keys())})', tags=('library'))
            for bookid, book in libr.repository.items():
                tree.insert(librname, 'end', text=book.title, values=(book.author, book.read_status, book.tags))
        all_books = tree.insert('', 'end', text=f"All Books ({len(Book.all_books.keys())})")
        for buk in Book.all_books.values():
            tree.insert(all_books, 'end', text=buk.title, values=(buk.author, buk.read_status, buk.tags))


def GUI_create_book(root):
    window = Toplevel(root)
    window.title('Book Creation')
    window.attributes('-topmost', 1)
    window.resizable(FALSE, FALSE)
    windowframe = ttk.Frame(window, padding='12 12 12 12')

    titlevar = StringVar()
    authorvar = StringVar()
    tagsvar = StringVar()
    statusvar = StringVar()
    tagslist = []
    instruction_font = font.Font(size=7, slant='italic')

    title_label = ttk.Label(windowframe, text='Title of Book', padding='3 3 3 3', anchor='w')
    title_entry = ttk.Entry(windowframe, textvariable=titlevar, width=20)

    author_label = ttk.Label(windowframe, text='Author of Book', padding = '3 3 3 3', anchor='w')
    author_entry = ttk.Entry(windowframe, textvariable=authorvar, width=20)

    tags_label = ttk.Label(windowframe, text='Tags', padding='3 3 3 3', anchor='w')
    tags_entry = ttk.Entry(windowframe, textvariable=tagsvar, width=10)
    tags_frame = ttk.Frame(windowframe, relief='sunken', borderwidth=5, padding='12 12 12 12', width=300, height=300)
    tags_entry.bind('<Return>', lambda x: _create_tag(tagsvar.get(), tagslist, tags_frame, tags_entry))
    tags_label_2 = ttk.Label(windowframe, text='Type in a tag and press Enter to add it. Click on the added tags to delete them.', anchor='nw', font=instruction_font, wraplength=500)

    read_status_label = ttk.Label(windowframe, text='Read Status', padding='3 3 3 3', anchor='w')
    read_status = ttk.Combobox(windowframe, textvariable=statusvar, values=('Unread', 'Reading', 'Finished'), state="readonly")
    read_status.bind("<<ComboboxSelected>>", read_status.selection_clear())

    notes_label = ttk.Label(windowframe, text='Leave a note', padding='3 3 3 3', anchor='w') 
    notes_box = Text(windowframe, width=20, height=5, wrap='word') # get with .get('start', 'end')
    s = ttk.Scrollbar(windowframe, orient=VERTICAL, command=notes_box.yview)
    notes_box.configure(yscrollcommand=s.set)

    savebutton = ttk.Button(windowframe, text='Save', command = lambda: _save(window, titlevar.get(), authorvar.get(), tagslist, statusvar.get(), notes_box.get(1.0, 'end')))
    cancelbutton = ttk.Button(windowframe, text='Cancel', command = lambda: windowframe.destroy())

    windowframe.grid(column=0, row=0, sticky='nsew')
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)

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

def _save(window, title, author, tags, status, notes):
    if not title or not author:
        messagebox.showinfo(message='Please enter title and author.')
        return
    Book(title, author, tags=tags, read_status=status, notes=notes)
    window.destroy()
    messagebox.showinfo(message='Book saved.')

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


