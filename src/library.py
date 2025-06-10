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
            print("Book name not found in list of names.")
            return False

    def rename(self, newname):
        oldname = self.name
        self.name = newname
        Library.all_libraries.pop(oldname)
        Library.all_libraries[newname] = self

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
        self._home_selection = {}
        self._buttons = {}

        self._root = root
        self.frame = ttk.Frame(self._root, padding='12 12 12 12')
        self.create_menubar()
        topstat1 = ttk.Label(self.frame, text=f'Current Library: {self.name}', anchor='w', padding='12 12 12 12')
        topstat2 = ttk.Label(self.frame, text=f"# of Books Loaded: {len(self.repository.keys())}", anchor='e', padding='12 12 12 12')
        
        print(f'creating frames')
        # Creating left tree frame, top right stats pane, bottom right notes tab and updates
        titlefont = font.Font(size=20, weight='bold')

        title_label = ttk.Label(self.frame, text="Dashboard", font=titlefont, padding='6 6 6 6', anchor='w')
        treeframe = ttk.Frame(self.frame, padding='12 12 12 12', relief='ridge', borderwidth=5)

        treepanes_group = ttk.PanedWindow(treeframe, orient=VERTICAL)
        treepane_1 = ttk.Labelframe(treepanes_group, text='Currently Reading', padding='3 3 3 3')
        treepane_2 = ttk.Labelframe(treepanes_group, text='Backlog (Unread Books)', padding='3 3 3 3')
        treepane_3 = ttk.Labelframe(treepanes_group, text='Finished Reading', padding='3 3 3 3')
        treepanes_group.add(treepane_1, weight=1)
        treepanes_group.add(treepane_2, weight=1)
        treepanes_group.add(treepane_3, weight=1)



        print(f'creating treeviews')
        # creating treeviews:
        treestyle = ttk.Style()
        treestyle.configure("Treeview", rowheight=40)

        self.tree1 = ttk.Treeview(treepane_1, columns=('Title', 'Author'))
        self.tree1.heading('#0', text='#')
        self.tree1.heading('Title', text='Title')
        self.tree1.heading('Author', text='Author')
        self.tree1.column('#0', width=50)
        self.tree1.column('Title', anchor='center', width=400)
        self.tree1.column('Author', anchor='center', width=300)
        tree1_scroll = ttk.Scrollbar(treepane_1, orient=VERTICAL, command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=tree1_scroll.set)

        self.tree2= ttk.Treeview(treepane_2, columns=('Title', 'Author'))
        self.tree2.heading('#0', text='#')
        self.tree2.heading('Title', text='Title')
        self.tree2.heading('Author', text='Author')
        self.tree2.column('#0', width=50)
        self.tree2.column('Title', anchor='center', width=400)
        self.tree2.column('Author', anchor='center', width=300)
        tree2_scroll = ttk.Scrollbar(treepane_2, orient=VERTICAL, command=self.tree2.yview)
        self.tree2.configure(yscrollcommand=tree2_scroll.set)

        self.tree3= ttk.Treeview(treepane_3, columns=('Title', 'Author'))
        self.tree3.heading('#0', text='#')
        self.tree3.heading('Title', text='Title')
        self.tree3.heading('Author', text='Author')
        self.tree3.column('#0', width=50)
        self.tree3.column('Title', anchor='center', width=400)
        self.tree3.column('Author', anchor='center', width=300)
        tree3_scroll = ttk.Scrollbar(treepane_3, orient=VERTICAL, command=self.tree3.yview)
        self.tree3.configure(yscrollcommand=tree3_scroll.set)

        print('binding trees to select')
        # global selection
        self.tree1.bind('<<TreeviewSelect>>', lambda x: self._tree_select(x, [self.tree2, self.tree3], stats_label, notes_frame, notes_box,))
        self.tree2.bind('<<TreeviewSelect>>', lambda x: self._tree_select(x, [self.tree1, self.tree3], stats_label, notes_frame, notes_box))
        self.tree3.bind('<<TreeviewSelect>>', lambda x: self._tree_select(x, [self.tree1, self.tree2], stats_label, notes_frame, notes_box))
    
        print('generating the 3 trees')
        # tree generation
        self._generate_reading_tree(self.tree1)
        self._generate_unread_tree(self.tree2)
        self._generate_finished_tree(self.tree3)

        print('showing book info')
        # book infos
        stats_pane, stats_label = self._load_book_stats()

        print('generating tabs')
        #notes tab
        tabs_group, notes_frame, updates_frame, notes_box, notes_scroll, notes_button, updates_label = self._load_tabs()

        print('generating separators')
        #separator
        greyline = ttk.Style()
        greyline.configure("TSeparator", background='grey50', relief='ridge', width=5)
        separator1 = ttk.Separator(self.frame, orient=VERTICAL)
        separator2 = ttk.Separator(self.frame, orient=HORIZONTAL)

        #hi
        tinyfont = font.Font(size=7, slant='roman', family='Courier')
        tinylabel = ttk.Label(self.frame, padding='3 3 3 3', anchor='se', text='a librarie by Dave', font=tinyfont)
        
        print(f'gridding things')
        self._root.rowconfigure(0 , weight=1)
        self._root.columnconfigure(0, weight=1)

        self.frame.grid(row=0, column=0, sticky='nsew')
        topstat1.grid(column=0, row=0, columnspan=5, sticky='nwes')
        topstat2.grid(column=7, row=0, columnspan=5, sticky='snew')
        title_label.grid(column=0, row=1, columnspan=5, sticky='snew')
        separator1.grid(column=5, row=2, rowspan=8, sticky='ns')
        separator2.grid(column=6, row=5, columnspan=4, sticky='ew')
        treeframe.grid(column=0, row=2, columnspan=5, rowspan=6, sticky='snew')
        treepanes_group.grid(column=0, row=0, sticky='snew')
        treepane_1.rowconfigure(0, weight=1)
        treepane_1.columnconfigure([0], weight=1)
        treepane_2.rowconfigure(0, weight=1)
        treepane_2.columnconfigure([0], weight=1)
        treepane_3.rowconfigure(0, weight=1)
        treepane_3.columnconfigure([0], weight=1)
        treeframe.rowconfigure(0, weight=1)
        treeframe.columnconfigure(0, weight=1)
        self.tree1.grid(row=0, column=0, sticky='snew')
        tree1_scroll.grid(row=0, column=1, sticky='snew')
        self.tree2.grid(row=0, column=0, sticky='snew')
        tree2_scroll.grid(row=0, column=1, sticky='snew')
        self.tree3.grid(row=0, column=0, sticky='snew')
        tree3_scroll.grid(row=0, column=1, sticky='snew')
        stats_pane.grid(column=6, row=2, columnspan=4, rowspan=3, sticky='snew')
        stats_label.grid(column=0, row=0, sticky='snew')
        stats_pane.rowconfigure(0, weight=1)
        stats_pane.columnconfigure(0, weight=1)
        tabs_group.grid(row=6, column=6, rowspan=4, columnspan=4, sticky='snew')
        notes_box.grid(row=0, column=0, columnspan=2, sticky='snew')
        notes_button.grid(row=1, column=0, sticky='snew', columnspan=2, padx=2, pady=2)
        notes_scroll.grid(row=0, column=2, sticky='snew')
        notes_frame.rowconfigure(0, weight=1)
        notes_frame.columnconfigure([0,1], weight=1)
        updates_label.grid(row=0, column=0, sticky='snew')
        updates_frame.rowconfigure(0, weight=1)
        updates_frame.columnconfigure(0, weight=1)
        tinylabel.grid(column=0, row=10, columnspan=10, sticky='snew')

        self.frame.rowconfigure([2,3,4], weight=2)
        self.frame.rowconfigure([6,7,8,9], weight=3)
        self.frame.rowconfigure(5, weight=1) # for the separator
        self.frame.columnconfigure([0,1,2,3,4], weight=3)
        self.frame.columnconfigure([6,7,8,9], weight=2)
        self.frame.columnconfigure(5, weight=1) # for the separator
        
        print('done loading GUI')

    def _load_book_stats(self): # Halfway through making these 2 functions i realised i could use .config to change the info displayed in my info boxes
        stats_pane = ttk.Labelframe(self.frame, text='Book Info:', padding='12 12 12 12')
        stats_label = ttk.Label(stats_pane, text=f'Tags: {self._get_selected_book().tags if self._get_selected_book() is not False else "None"}\nStatus: {self._get_selected_book().read_status if self._get_selected_book() is not False else "None"}', padding='3 3 3 3', anchor='nw', wraplength=300)

        return stats_pane, stats_label

    def _load_tabs(self):
        tabs_group = ttk.Notebook(self.frame)

        notes_frame = ttk.Frame(tabs_group, padding='6 6 6 6', borderwidth=5, relief='groove')
        updates_frame = ttk.Frame(tabs_group, padding='6 6 6 6', borderwidth=5, relief='groove')

        tabs_group.add(notes_frame, text='Notes')
        tabs_group.add(updates_frame, text='Coming soon...')

        notes_box = Text(notes_frame, width=20, height=5, wrap='word', state='disabled') # get with .get('start', 'end')
        if self._get_selected_book() is not False:
            notes_box.configure(state='normal')
            notes_box.insert(1.0, self._get_selected_book().notes)
            notes_box.configure(state='disabled')
        notes_scroll = ttk.Scrollbar(notes_frame, orient=VERTICAL, command=notes_box.yview)
        notes_box.configure(yscrollcommand=notes_scroll.set)
        notes_button = ttk.Button(notes_frame, text='Edit', padding='3 3 3 3', command = lambda: self._home_edit_button(notes_frame, notes_box, notes_button))

        updates_label = ttk.Label(updates_frame, text=f"Features I'm considering:\nOpen Library API Integration\nSearch function\nPDF storage (for books in pdf form)\nColours (?)", wraplength=600, padding='6 6 6 6', anchor='nw')

        return tabs_group, notes_frame, updates_frame, notes_box, notes_scroll, notes_button, updates_label

    def _home_edit_button(self, notes_frame, notes_box, notes_button):
        save_button = ttk.Button(notes_frame, text='Save', padding='3 3 3 3', command = lambda: self._home_edit_save_button(notes_frame, notes_box))
        cancel_button = ttk.Button(notes_frame, text='Cancel', padding='3 3 3 3', command = lambda: self._home_edit_cancel_button(notes_frame, notes_box))
        self._buttons = {}
        self._buttons['save'] = save_button
        self._buttons['cancel'] = cancel_button

        notes_button.destroy()
        save_button.grid(row=1, column=0, sticky='snew', padx=2, pady=2)
        cancel_button.grid(row=1, column=1, sticky='snew', padx=2, pady=2)
        
        notes_box.configure(state='normal')
        notes_box.focus()

    def _home_edit_cancel_button(self, notes_frame, notes_box):
        selected_book = self._get_selected_book()
        if selected_book is not False:
            notes = selected_book.notes
            if notes is None:
                notes_box.configure(state='normal')
                notes_box.delete(1.0, 'end')
                notes_box.configure(state='disabled')
            else:
                notes_box.configure(state='normal')
                notes_box.replace(1.0, 'end', notes)
                notes_box.configure(state='disabled')
        self._buttons['save'].destroy()
        self._buttons['cancel'].destroy()

        notes_button = ttk.Button(notes_frame, text='Edit', padding='3 3 3 3', command = lambda: self._home_edit_button(notes_frame, notes_box, notes_button))
        notes_button.grid(row=1, column=0, columnspan=2, sticky='snew', padx=2, pady=2)

    def _home_edit_save_button(self, notes_frame, notes_box):
        selected_book = self._get_selected_book()
        content = notes_box.get(1.0, 'end')
        if selected_book is not False and content is not None:
            selected_book.edit(notes=content)
        notes_box.configure(state='disabled')
        self._buttons['save'].destroy()
        self._buttons['cancel'].destroy()

        notes_button = ttk.Button(notes_frame, text='Edit', padding='3 3 3 3', command = lambda: self._home_edit_button(notes_frame, notes_box, notes_button))
        notes_button.grid(row=1, column=0, columnspan=2, sticky='snew', padx=2, pady=2)


    def _tree_select(self, event, other_trees, stats_label, notes_frame, notes_box):
        print("_tree_select is called")
        self._home_selection = {}
        current_tree = event.widget

        if len(current_tree.selection()) == 0: # Check if this is a deselection event
            return

        for tree in other_trees: # remove selection from other trees
            tree.selection_remove(tree.selection())

        selected = current_tree.selection()

        if selected:
            self._home_selection['tree'] = current_tree
            self._home_selection['item'] = selected[0]
            print(f'self._home_selection has been updated: {self._home_selection}')

            # Update the 2 info boxes
            selected_book = self._get_selected_book()
            if selected_book is not False:
                tags = selected_book.tags
                status = selected_book.read_status
                notes = selected_book.notes

                stats_label.configure(text=f'Tags: {tags}\nStatus: {status}' )

                if notes_box['state'] == 'normal': # while user was editting, switched books
                    self._buttons['save'].destroy()
                    self._buttons['cancel'].destroy()
                    notes_button = ttk.Button(notes_frame, text='Edit', padding='3 3 3 3', command = lambda: self._home_edit_button(notes_frame, notes_box, notes_button))
                    notes_button.grid(row=1, column=0, columnspan=2, sticky='snew', padx=2, pady=2)


                if notes is None: 
                    notes_box.configure(state='normal')
                    notes_box.delete(1.0, 'end')
                    notes_box.configure(state='disabled')
                else:
                    notes_box.configure(state='normal')
                    notes_box.replace(1.0, 'end', notes)
                    notes_box.configure(state='disabled')

                
        else:
            self._home_selection.clear()
            print('self._home_selection has been cleared')

    def _get_selected_book(self):
        if self._home_selection != {}:
            print(f"this is home selection: {self._home_selection}")
            selected_tree = self._home_selection['tree']
            tree_item = self._home_selection['item']
            tree_item_values = selected_tree.item(tree_item, option='values')
            tree_item_name = tree_item_values[0]
            book_id = self.find_bookid(tree_item_name)
            selected_book = Book.all_books[book_id]
            return selected_book
        else:
            return False

    def _generate_reading_tree(self, tree):
        for item in tree.get_children(''):
            tree.delete(item)
        readinglist = []
        for buk in Book.all_books.values():
            if buk.read_status == "Reading" and buk in self.repository.values():
                readinglist.append(buk)
        for i, buk in enumerate(readinglist):
            tree.insert('', 'end', text=f'{i+1}.', values=(buk.title, buk.author))
        tree.tag_configure("greyed", background='grey50')
        item_ids = tree.get_children()
        for j in range(0, len(item_ids), 2):
            tree.item(item_ids[j], tags=("greyed"))

    def _generate_unread_tree(self, tree):
        for item in tree.get_children(''):
            tree.delete(item)
        unreadlist = []
        for buk in Book.all_books.values():
            if buk.read_status == "Unread" and buk in self.repository.values():
                unreadlist.append(buk)
        for i, buk in enumerate(unreadlist):
            tree.insert('', 'end', text=f'{i+1}.', values=(buk.title, buk.author))
        tree.tag_configure("greyed", background='grey50')
        item_ids = tree.get_children()
        for j in range(0, len(item_ids), 2):
            tree.item(item_ids[j], tags=("greyed"))

    def _generate_finished_tree(self, tree):
        for item in tree.get_children(''):
            tree.delete(item)
        finishedlist = []
        for buk in Book.all_books.values():
            if buk.read_status == "Finished" and buk in self.repository.values():
                finishedlist.append(buk)
        for i, buk in enumerate(finishedlist):
            tree.insert('', 'end', text=f'{i+1}.', values=(buk.title, buk.author))
        tree.tag_configure("greyed", background='grey50')
        item_ids = tree.get_children()
        for j in range(0, len(item_ids), 2):
            tree.item(item_ids[j], tags=("greyed"))
    






    def create_menubar(self):
        if self._root is not None:
            self._root.option_add('*tearOff', FALSE)
            menubar = Menu(self.frame)
            self._root['menu'] = menubar
            books = Menu(menubar)
            manage = Menu(menubar)
            switch = Menu(manage)
            menubar.add_cascade(menu=books, label='Books')
            menubar.add_cascade(menu=manage, label='Manage')
            books.add_command(label='New Book', command = lambda: self.menubar_create_book())
            books.add_command(label='Edit or Delete Book', command= lambda: self.menubar_edit_book())
            manage.add_command(label='Manage Books and Libraries', command = lambda: self.menubar_manage())
            manage.add_cascade(menu=switch, label='Switch Libraries')
            manage.add_command(label='Rename Library', command = lambda: self.menubar_rename_libr())
            for librname in Library.all_libraries:
                print(f"generating library in menubar: {librname}")
                switch.add_command(label=f'{librname}', command = lambda name=librname: self.menubar_switch_libr(name))

    def menubar_manage(self):
        window = Toplevel(self._root)
        window.title(f'Manage books in {self.name}')
        window.attributes('-topmost', 1)
        windowframe = ttk.Frame(window, padding='12 12 12 12')
        treeframe =ttk.Frame(windowframe, padding='6 6 6 6', relief='ridge', borderwidth=5)
        bigfont = font.Font(size=20, weight='bold')
        label1 = ttk.Label(windowframe, text="Library Manager", anchor='w', font=bigfont, padding='6 6 6 6')

        treestyle = ttk.Style()
        treestyle.configure("Treeview", rowheight=40)
        tree = ttk.Treeview(treeframe, columns=('Author', 'Status', 'Tags'))
        tree.heading('#0', text='Library/Books')
        tree.heading('Author', text='Author')
        tree.heading('Status', text='Status')
        tree.heading('Tags', text='Tags')
        tree.column('#0', width=400)
        tree.column('Author', width=300)
        tree.column('Status', anchor='center', width=120)
        tree.column('Tags', anchor='center', width=300)
        s = ttk.Scrollbar(tree, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=s.set)

        tree.tag_configure('library', background='grey50')

        self.treehelper_generate_managelibr(tree)

        addlib = ttk.Button(windowframe, text='Add library', padding='6 6 6 6', command = lambda: self.treehelper_add_libr(tree))
        dellib = ttk.Button(windowframe, text='Delete Library', padding='6 6 6 6', command = lambda: self.treehelper_del_libr(tree, windowframe))
        addbook = ttk.Button(windowframe, text='Add Book To ...', padding='6 6 6 6', command= lambda: self.treehelper_add_book(tree, window))
        rembook = ttk.Button(windowframe, text='Remove Book', padding='6 6 6 6', command = lambda: self.treehelper_remove_book(tree, window))

        windowframe.grid(row=0, column=0, sticky='nsew')
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        label1.grid(row=0, column=0, sticky='w')
        treeframe.grid(row=1, column=0, columnspan=4, sticky='snew')
        tree.grid(row=0, column=0, sticky='nsew')
        addlib.grid(row=2, column=0, sticky='nsew')
        dellib.grid(row=2, column=1, sticky='nsew')
        addbook.grid(row=2, column=2, sticky='nsew')
        rembook.grid(row=2, column=3, sticky='nsew')
        windowframe.rowconfigure(1, weight=1)
        windowframe.columnconfigure([0,1,2,3], weight=1)
        treeframe.rowconfigure(0, weight=1)
        treeframe.columnconfigure(0, weight=1)

    def menubar_switch_libr(self, librname):
        trees = [self.tree1, self.tree2, self.tree3]
        for tree in trees:
            tree.unbind('<<TreeviewSelect>>')
        if self._root is not None:
            self.frame.destroy()
            libr = Library.all_libraries[librname]
            libr.load_GUI(self._root)


    def treehelper_add_libr(self, tree):
        namebox = Toplevel(self.frame)
        namebox.title("Library Creation")
        namebox.attributes("-topmost", 1)
        namebox.geometry("400x150+0+0")
        namebox.resizable(FALSE, FALSE)
        label1 = ttk.Label(namebox, text="Name your library", padding='3 3 3 3', anchor='center')
        librname = StringVar()
        entry1 = ttk.Entry(namebox, textvariable=librname, width=10, justify="center")
        entry1.focus()
        namebox.bind('<Return>', lambda x: self._treehelper_create_libr(namebox, entry1.get(), tree))

        label1.grid(sticky='nsew')
        entry1.grid(sticky='nsew')
        namebox.rowconfigure([0, 1], weight=1)
        namebox.columnconfigure(0, weight=1)

    def _treehelper_create_libr(self, window, librname, tree):
        if not librname:
            messagebox.showinfo(message='Please enter a name', parent=window)
        elif librname in Library.all_libraries:
            messagebox.showinfo(message='Library name already in use', parent=window)
        else:
            Library(librname)
            self.treehelper_generate_managelibr(tree)
            print(f"added library: {librname}")
            window.destroy()

    def treehelper_del_libr(self, tree, windowframe):
        selection = tree.selection()
        if len(selection) != 1:
            print("Treeview selection should highlight 1 item.")
        elif selection[0] not in Library.all_libraries:
            print("Please select only libraries to delete.")
        else:
            tree_item = selection[0]
            if len(Library.all_libraries) > 1:
                Library.all_libraries[tree_item].delete()
                if self in Library.all_libraries.values():
                    self.load_GUI(self._root)
                    self.treehelper_generate_managelibr(tree)
                    print(f"deleted library: {tree_item}")
                else:
                    librname = list(Library.all_libraries.keys())[0]
                    libr = Library.all_libraries[librname]
                    libr.load_GUI(self._root)
                    libr.treehelper_generate_managelibr(tree)
                    print(f"deleted library: {tree_item}")
            else:
                print("Unable to delete: Last library remaining.")
                messagebox.showinfo(message="Unable to delete: Last library remaining.", parent=windowframe)

    def treehelper_add_book(self, tree, window):
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
            frame1 = ttk.Frame(addlocation, relief='ridge', borderwidth=5, padding='18 18 18 18')
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
                librtoggle.grid(column=0, row=i, sticky='nsew')
                i += 1
            
            savebutton = ttk.Button(addlocation, text="Save", padding='3 3 3 3', command = lambda: self._treehelper_save_book(tree, tree_item_name, addlocation, frame1))
            cancelbutton = ttk.Button(addlocation, text="Cancel", padding='3 3 3 3', command = addlocation.destroy)

            savebutton.grid(column=0, row=2, sticky='wnes')
            cancelbutton.grid(column=1, row=2, sticky='wnes')

    def treehelper_remove_book(self, tree, window):
        selection = tree.selection()

        if len(selection) != 1:
            print("Treeview selection should highlight 1 item.")
            return

        if selection is None:
            print("Select a book in order to delete it.")
            messagebox.showinfo(message="Select a book in order to delete it.", parent=window)
            return

        tree_item = selection[0]
        tree_item_name = tree.item(tree_item, option='text')
        
        if tree_item_name not in self.booknames_all():
            print("Select a book in order to delete it.")
            messagebox.showinfo(message="Select a book in order to delete it.", parent=window)
            return

        parent = tree.parent(tree_item)

        if parent not in Library.all_libraries or parent == "all_books":
            print("Select a book under a library to remove it from that library.")
            messagebox.showinfo(message="Select a book under a library to remove it from that library.", parent=window)
            return

        bookid = self.find_bookid(tree_item_name)
        parentlibr = Library.all_libraries[parent]
        parentlibr.del_book(bookid)
        self.treehelper_generate_managelibr(tree)
        self.load_GUI(self._root)
        print(f"Removed {tree_item_name} from {parent}")

    def _treehelper_save_book(self, tree, tree_item_name, window, frame):
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
        self.treehelper_generate_managelibr(tree)
        self.load_GUI(self._root)
        self.libr_bool = [] # reset to empty
        window.destroy()


    def treehelper_generate_managelibr(self, tree):
        for item in tree.get_children(''):
            tree.delete(item)
        for librname, libr in Library.all_libraries.items():
            tree.insert('', 'end', librname, text=f'{librname} ({len(libr.repository.keys())})', tags=('library'), open=TRUE)
            for bookid, book in libr.repository.items():
                tree.insert(librname, 'end', text=book.title, values=(book.author, book.read_status, book.tags))
        all_books = tree.insert('', 'end', 'all_books', text=f"All Books ({len(Book.all_books.keys())})")
        for buk in Book.all_books.values():
            tree.insert(all_books, 'end', text=buk.title, values=(buk.author, buk.read_status, buk.tags))

    def treehelper_generate_editbook(self, tree):
        for item in tree.get_children(''):
            tree.delete(item)
        for i, buk in enumerate(Book.all_books.values()):
            tree.insert('', 'end', text=f'{i+1}.', values=(buk.title, buk.author, buk.read_status, buk.tags))

        tree.tag_configure("greyed", background='grey50')
        item_ids = tree.get_children()
        for j in range(0, len(item_ids), 2):
            tree.item(item_ids[j], tags=("greyed"))

    def menubar_create_book(self, mode=None, tree=None):
        window = Toplevel(self._root)
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
        tags_entry.bind('<Return>', lambda x: self._create_tag(tagsvar.get(), tagslist, tags_frame, tags_entry))
        tags_label_2 = ttk.Label(windowframe, text='Type in a tag and press Enter to add it. Click on the added tags to delete them.', anchor='nw', font=instruction_font, wraplength=500)

        read_status_label = ttk.Label(windowframe, text='Read Status', padding='3 3 3 3', anchor='w')
        read_status = ttk.Combobox(windowframe, textvariable=statusvar, values=('Unread', 'Reading', 'Finished'), state="readonly")
        read_status.bind("<<ComboboxSelected>>", read_status.selection_clear())

        notes_label = ttk.Label(windowframe, text='Leave a note', padding='3 3 3 3', anchor='w') 
        notes_box = Text(windowframe, width=20, height=5, wrap='word') # get with .get('start', 'end')
        s = ttk.Scrollbar(windowframe, orient=VERTICAL, command=notes_box.yview)
        notes_box.configure(yscrollcommand=s.set)

        savebutton = ttk.Button(windowframe, text='Save', command = lambda: self._save_book_creation(window, titlevar.get(), authorvar.get(), tagslist, statusvar.get(), notes_box.get(1.0, 'end')))
        cancelbutton = ttk.Button(windowframe, text='Cancel', command = lambda: window.destroy())

        # Filling in values if in 'edit' mode:
        if mode == 'edit' and tree is not None:
            selection = tree.selection()

            if len(selection) != 1:
                print("Treeview selection should highlight 1 item.")
                return

            if selection is None:
                print("Select a book in order to edit it.")
                messagebox.showinfo(message="Select a book in order to edit it.", parent=window)
                return

            tree_item = selection[0]
            tree_item_values = tree.item(tree_item, option='values')
            tree_item_name = tree_item_values[0]
            
            if tree_item_name not in self.booknames_all():
                print("Something is wrong, the book selected cannot be found.")
                messagebox.showinfo(message="Something is wrong, the book selected cannot be found", parent=window)
                return

            bookid = self.find_bookid(tree_item_name)
            selectedbook = Book.all_books[bookid]
            
            title_entry.insert(0, selectedbook.title) # inserting the values of the selected book into data fields
            author_entry.insert(0, selectedbook.author)
            if selectedbook.tags is not None:
                for each_tag in selectedbook.tags:
                    self._create_tag(each_tag, tagslist, tags_frame, tags_entry)
            read_status.set(selectedbook.read_status)
            if selectedbook.notes is not None:
                notes_box.insert(1.0, selectedbook.notes)
            
            # update the save button 
            savebutton = ttk.Button(windowframe, text='Save', command = lambda: self._save_book_edit(tree, window, selectedbook, titlevar.get(), authorvar.get(), tagslist, statusvar.get(), notes_box.get(1.0, 'end')))
            

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

    def menubar_edit_book(self): 
        window = Toplevel(self._root)
        window.title('Edit / Delete Books')
        window.attributes('-topmost', 1)
        windowframe = ttk.Frame(window, padding='12 12 12 12')
        treeframe =ttk.Frame(windowframe, padding='6 6 6 6', relief='ridge', borderwidth=5)
        label1 = ttk.Label(windowframe, text='Select a book to edit or delete.', anchor='center')

        treestyle = ttk.Style()
        treestyle.configure("Treeview", rowheight=40)
        tree = ttk.Treeview(treeframe, columns=('Title', 'Author', 'Status', 'Tags'))
        tree.heading('Title', text='Title')
        tree.heading('Author', text='Author')
        tree.heading('Status', text='Status')
        tree.heading('Tags', text='Tags')
        tree.column('#0', width=50)
        tree.column('Title', width=400)
        tree.column('Author', width=300)
        tree.column('Status', anchor='center', width=120)
        tree.column('Tags', anchor='center', width=300)
        
        s = ttk.Scrollbar(tree, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=s.set)

        self.treehelper_generate_editbook(tree)

        editbutton = ttk.Button(windowframe, padding='3 3 3 3', text='Edit Book', command = lambda: self.menubar_create_book(mode='edit', tree=tree))
        deletebutton = ttk.Button(windowframe, text='Delete Book', command = lambda: self._delete_book(tree, window))
        donebutton = ttk.Button(windowframe, padding='3 3 3 3', text='Done', command = lambda: window.destroy())

        windowframe.grid(row=0, column=0, sticky='snew')
        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        label1.grid(row=0, column=0, columnspan=3, sticky='snew')
        treeframe.grid(row=1, column=0, columnspan=3, sticky='snew')
        tree.grid(row=0, column=0, sticky='snew')
        editbutton.grid(row=2, column=0, sticky='snew')
        deletebutton.grid(row=2, column=1, sticky='snew')
        donebutton.grid(row=2, column=2, sticky='snew')

        windowframe.rowconfigure([1], weight=1)
        windowframe.columnconfigure([0,1,2], weight=1)

        treeframe.rowconfigure(0, weight=1)
        treeframe.columnconfigure(0, weight=1)
        

    def menubar_rename_libr(self):
        namebox = Toplevel(self.frame)
        namebox.title("Rename Library")
        namebox.attributes("-topmost", 1)
        namebox.geometry("400x150+0+0")
        namebox.resizable(FALSE, FALSE)
        label1 = ttk.Label(namebox, text="Rename your library", padding='3 3 3 3', anchor='center')
        librnamevar = StringVar()
        entry1 = ttk.Entry(namebox, textvariable=librnamevar, width=10, justify='center')
        entry1.insert(0, self.name)
        namebox.bind('<Return>', lambda x: self._menubar_rename_libr(namebox, librnamevar.get()))
        entry1.focus()

        label1.grid(sticky='nsew')
        entry1.grid(sticky='nsew')
        namebox.rowconfigure([0, 1], weight=1)
        namebox.columnconfigure(0, weight=1)

    def _menubar_rename_libr(self, namebox, newname):
        if not newname:
            messagebox.showinfo(message='Please enter a name', parent=namebox)
        elif newname in Library.all_libraries:
            messagebox.showinfo(message='Library name already in use', parent=namebox)
        else:
            oldname = self.name
            self.rename(newname)
            self.load_GUI(self._root)
            print(f'Renamed {oldname} to {newname}')
            namebox.destroy()
     


    def _save_book_creation(self, window, title, author, tags, status, notes):
        if not title or not author:
            messagebox.showinfo(message='Please enter title and author.')
            return
        Book(title, author, tags=tags, read_status=status, notes=notes)
        window.destroy()
        messagebox.showinfo(message='Book saved.')
        self.load_GUI(self._root)

    def _save_book_edit(self, tree, window, selectedbook, title, author, tags, read_status, notes):
        if not title or not author:
            messagebox.showinfo(message='Please enter title and author.')
            return
        selectedbook.edit(title=title, author=author, tags=tags, read_status=read_status, notes=notes)
        messagebox.showinfo(message='Book edit saved.', parent=window)
        window.destroy()
        self.load_GUI(self._root)
        self.treehelper_generate_editbook(tree)

    def _delete_book(self, tree, window): 
        selection = tree.selection()

        if len(selection) != 1:
            print("Treeview selection should highlight 1 item.")
            return

        if selection is None:
            print("Select a book in order to delete it.")
            messagebox.showinfo(message="Select a book in order to delete it.", parent=window)
            return

        tree_item = selection[0]
        tree_item_values = tree.item(tree_item, option='values')
        tree_item_name = tree_item_values[0]
        
        if tree_item_name not in self.booknames_all():
            print("Something is wrong, the book selected cannot be found.")
            messagebox.showinfo(message="Something is wrong, the book selected cannot be found", parent=window)
            return

        bookid = self.find_bookid(tree_item_name)
        selectedbook = Book.all_books[bookid]
        selectedbook.delete()

        self.load_GUI(self._root)
        self.treehelper_generate_editbook(tree)
        messagebox.showinfo(message=f'Deleted {tree_item_name}', parent=window)

    def _create_tag(self, tagname, tagslist, tags_frame, tags_entry):
        if tagname:
            tagslist.append(tagname)
            tag_button = ttk.Button(tags_frame, text=tagname, padding='6 6 6 6', command = lambda: self._annihilate_tag_button(tagname, tagslist, tags_frame, tag_button))
            tag_button.grid(row=int((len(tagslist)-1) / 3), column=(len(tagslist) + 2) % 3, sticky='snew')
            tags_entry.delete(0, 'end')
        else:
            pass


    def _annihilate_tag_button(self, tagname, tagslist, tags_frame, tag_button):
        tagslist.remove(tagname)
        tag_button.destroy()
        for child in tags_frame.winfo_children():
            child.destroy()
        for i in range(len(tagslist)):
            new_button = ttk.Button(tags_frame, text=tagslist[i], padding='6 6 6 6', command = lambda: self._annihilate_tag_button(tagslist[i], tagslist, tags_frame, tag_button))
            new_button.grid(row=int(i / 3), column=((i + 3) % 3), sticky='snew')


