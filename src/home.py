from tkinter import *
from tkinter import ttk

class Home():
    def __init__(self):
        self._root = Tk()
        self._root.title("librarie")
        width=str(self._root.winfo_screenwidth())
        height=str(self._root.winfo_screenheight())
        self._root.geometry(f'{width}x{height}')
        self._root.minsize(1280, 720)
        self._root.protocol("WM_DELETE_WINDOW", self.quit_save)
        self._root.mainloop()


    def quit_save(self):
        prompt = Toplevel(self._root)
        prompt.title("Save & Close")
        prompt.attributes("-topmost", 1)
        text = ttk.Label(prompt, text="Do you want to save your library?", padding="3 3 3 3", anchor='center')
        yes = ttk.Button(prompt, text="Yes")
        no = ttk.Button(prompt, text="No", command= lambda: self._root.destroy())

        text.grid(column=0, row=0, columnspan=2, sticky='we')
        yes.grid(column=0, row=1, sticky='nsew')
        no.grid(column=1, row=1, sticky='senw')

Home()
