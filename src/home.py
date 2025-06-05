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
        width = 1280
        height = 720
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
            messagebox.showinfo(message="Opening an empty library")

    def load_GUI(self):
        self.frame = ttk.Frame(self._root, padding='12 12 12 12')
        self.frame.grid(sticky='snew')
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)

        librlist = list(Library.all_libraries.keys())
        librlistvar = StringVar(value=librlist)
        l = Listbox(self.frame, height=10, listvariable=librlistvar)

        infoframe = ttk.Frame(self.frame, borderwidth=5, relief="ridge", width=400, height=400, padding ='6 6 6 6')
        loadlibr = ttk.Button(self.frame, text="Load Library", padding='6 6 6 6', command= lambda: self.load_libr(l, librlist))
        dellibr = ttk.Button(self.frame, text="Delete Library", padding='6 6 6 6', command= lambda: self.del_libr(l, librlist, librlistvar))
        addlibr = ttk.Button(self.frame, text="Add Library", command= lambda: self.add_libr(librlist, librlistvar))

        l.grid(column=0, row=0, rowspan=6, sticky='snew')
        infoframe.grid(column=1, row=0, columnspan=2, rowspan=4, sticky='nsew')
        addlibr.grid(column=1, row=4, sticky="snew")
        dellibr.grid(column=2, row=4, sticky="snew")
        loadlibr.grid(column=1, row=5, columnspan=5, sticky='ew')

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        l.bind('<Double-1>', lambda x: self.load_libr(l, librlist))


    def del_libr(self, listbox, librlist, librlistvar):
        selection = listbox.curselection()
        if len(selection) == 1:
            idx = selection[0]
            librname = librlist[idx]
            Library.all_libraries[librname].delete()
            librlist.pop(idx)
            librlistvar.set(librlist)
            print(f"deleted library: {librname}")

    def add_libr(self, librlist, librlistvar):
        namebox = Toplevel(self.frame)
        namebox.title("Library Creation")
        namebox.attributes("-topmost", 1)
        namebox.resizable(FALSE, FALSE)
        label1 = ttk.Label(namebox, text="Name your library", padding='3 3 3 3', anchor='center')
        librname = StringVar()
        entry1 = ttk.Entry(namebox, textvariable=librname, width=10)
        entry1.focus()
        namebox.bind('<Return>', lambda x: self.create_libr(namebox, entry1.get(), librlist, librlistvar))

        label1.grid()
        entry1.grid()
        
    def create_libr(self, window, librname, librlist, librlistvar):
        if librname:
            Library(librname)
            librlist.append(librname)
            librlistvar.set(librlist)
            print(f"added library: {librname}")
            window.destroy()
        else:
            messagebox.showinfo(message='Please enter a name')

    def load_libr(self, listbox, librlist):
        selection = listbox.curselection()
        if len(selection) == 1:
            idx = selection[0]
            librname = librlist[idx]
            libr_to_load = Library.all_libraries[librname]

            self.frame.destroy()
            libr_to_load.load_GUI(self._root)



Home(Tk())
