from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from json_conversion import *
import json
from library import Library
from book import Book

class Home():
    def __init__(self, root):
        self._root = root
        self._root.title("librarie")
        width = 1920
        height = 1080
        self._root.geometry(f'{width}x{height}+0+0')
        self._root.minsize(1280, 720)
        self._root.protocol("WM_DELETE_WINDOW", self.quit_save)
        self.start_load()
        self.load_GUI()
        self._root.mainloop()



    def quit_save(self):
        prompt = Toplevel(self._root)
        prompt.title("Save & Close")
        prompt.attributes("-topmost", 1)
        prompt.resizable(FALSE, FALSE)
        text = ttk.Label(prompt, text="Do you want to save your librarie profile?", padding="3 3 3 3", anchor='center')
        yes = ttk.Button(prompt, text="Yes", command= lambda: self.helper_save())
        no = ttk.Button(prompt, text="No", command= lambda: self._root.destroy())

        text.grid(column=0, row=0, columnspan=2, sticky='we')
        yes.grid(column=0, row=1, sticky='nsew')
        no.grid(column=1, row=1, sticky='senw')

    def helper_save(self):
        filename = filedialog.asksaveasfilename(title="Save Library As", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            with open(filename, 'w') as f:
                json.dump(all_to_dic(), f)
            self._root.destroy()
        return

    def start_load(self):
        filename = filedialog.askopenfilename(title="Open Library", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if filename:
            with open(filename, 'r') as f:
                try:
                    metadict = json.load(f)
                    print(f"Books found: {list(metadict["books"].keys())}")
                    print(f"Libraries found: {list(metadict["libraries"].keys())}")
                    loaded_books = book_from_dic(metadict["books"])
                    loaded_libs = lib_from_dic(metadict["libraries"])
                    Book._next_id = metadict["book_next_id"]
                    print(f"Books loaded: {list(loaded_books.keys())}")
                    print(f"Libraries loaded: {list(loaded_libs.keys())}")
                except:
                    print("Error: invalid JSON file. Try selecting a different file.")
                    self.start_load()
        else:
            messagebox.showinfo(message="No libraries found.")

    def load_GUI(self):
        self.frame = ttk.Frame(self._root, padding='12 12 12 12')
        treeframe =ttk.Frame(self.frame, padding='6 6 6 6', relief='ridge', borderwidth=5)
        label1 = ttk.Label(self.frame, text='Select a Library to Load', anchor='center')

        treestyle = ttk.Style()
        treestyle.configure("Treeview", rowheight=40)
        tree = ttk.Treeview(treeframe, columns=('Library', '# of Books'))
        tree.heading('Library', text='Library')
        tree.heading('# of Books', text='# of Books')
        tree.column('#0', width=50)
        tree.column('Library', width=400, anchor='center')
        tree.column('# of Books', width=200, anchor='center')

        s = ttk.Scrollbar(tree, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=s.set)

        self.treeview_generate(tree)

        loadlibr = ttk.Button(self.frame, text="Load Library", padding='6 6 6 6', command= lambda: self.load_libr(tree))
        dellibr = ttk.Button(self.frame, text="Delete Library", padding='6 6 6 6', command= lambda: self.del_libr(tree))
        addlibr = ttk.Button(self.frame, text="Add Library", command= lambda: self.add_libr(tree))

        self.frame.grid(row=0, column=0, sticky='snew')
        tree.grid(row=0, column=0, sticky='snew')
        treeframe.grid(column=0, row=1, columnspan=2, sticky='snew')
        label1.grid(row=0, column=0, columnspan=2, sticky='nsew')
        addlibr.grid(column=0, row=2, sticky="snew")
        dellibr.grid(column=1, row=2, sticky="snew")
        loadlibr.grid(column=0, row=3, columnspan=2, sticky='nsew')

        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self.frame.columnconfigure([0,1], weight=1)
        self.frame.rowconfigure(1, weight=1)
        treeframe.rowconfigure(0, weight=1)
        treeframe.columnconfigure(0, weight=1)
        
        tree.bind('<Double-1>', lambda x: self.load_libr(tree))


    def del_libr(self, tree):
        selection = tree.selection()
        if len(selection) != 1:
            print("Treeview selection should highlight 1 item.")
            return

        tree_item = selection[0]
        tree_item_values = tree.item(tree_item, option='values')
        librname = tree_item_values[0]
        
        if librname not in Library.all_libraries:
            print("Please select only libraries to delete.")
            return

        Library.all_libraries[librname].delete()
        self.load_GUI()
        print(f"deleted library: {librname}")

    def add_libr(self, tree):
        namebox = Toplevel(self.frame)
        namebox.title("Library Creation")
        namebox.attributes("-topmost", 1)
        namebox.geometry("400x150+0+0")
        namebox.resizable(FALSE, FALSE)
        label1 = ttk.Label(namebox, text="Name your library", padding='3 3 3 3', anchor='center')
        librname = StringVar()
        entry1 = ttk.Entry(namebox, textvariable=librname, width=10, justify='center')
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
            self.treeview_generate(tree)
            print(f"added library: {librname}")
            window.destroy()
        
    def create_libr(self, window, librname, librlist, librlistvar):
        if not librname:
            messagebox.showinfo(message='Please enter a name', parent=window)
        elif librname in Library.all_libraries:
            messagebox.showinfo(message='Library name already in use', parent=window)
        else:
            Library(librname)
            librlist.append(librname)
            librlistvar.set(librlist)
            print(f"added library: {librname}")
            window.destroy()

    def load_libr(self, tree):
        selection = tree.selection()
        if len(selection) != 1:
            print("Treeview selection should highlight 1 item.")
            return

        tree_item = selection[0]
        tree_item_values = tree.item(tree_item, option='values')
        librname = tree_item_values[0]

        if librname not in Library.all_libraries:
            print("Please select only libraries to delete.")

        libr_to_load = Library.all_libraries[librname]
        self.frame.destroy()
        libr_to_load.load_GUI(self._root)
        print(f"Loading library: {librname}")

    def treeview_generate(self, tree):
        for item in tree.get_children(''):
            tree.delete(item)
        for i, libr in enumerate(Library.all_libraries.values()):
            tree.insert('', 'end', text=f'{i+1}.', values=(libr.name, len(libr.repository.keys())))

        tree.tag_configure("greyed", background='grey50')
        item_ids = tree.get_children()
        for j in range(0, len(item_ids), 2):
            tree.item(item_ids[j], tags=("greyed"))

Home(Tk())
