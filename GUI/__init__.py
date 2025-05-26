from tkinter import *
from tkinter import ttk

root = Tk()
root.title("librarie")

mainframe = ttk.Frame(root, padding="12 12 12 12")
b1= ttk.Button(mainframe, text="Lib1")
b2= ttk.Button(mainframe, text="Lib2")
label1 = ttk.Label(mainframe, text="version 1.0", anchor="center")
ok = ttk.Button(mainframe, text="ok")
frame1 = ttk.Frame(mainframe, borderwidth=5, relief="sunken", width=300, height=300)

onevar = BooleanVar(value=True)
twovar = BooleanVar(value=False)

c1 = ttk.Checkbutton(mainframe, text="alpha", variable=onevar, onvalue=True)
c2 = ttk.Checkbutton(mainframe, text="beta", variable=twovar, onvalue=True)

mainframe.grid(column=0, row=0, sticky="nsew")
b1.grid(column=0, row=0, columnspan=2, rowspan=2, sticky="wens")
b2.grid(column=0, row=2, columnspan=2, rowspan=2, sticky="snwe")
label1.grid(column=1, row=5, sticky='we', padx=5, pady=5)
ok.grid(column=0, row=5, sticky="we", padx=(0,5), pady=5)
frame1.grid(column=2, row=0, columnspan=2, rowspan=4, sticky='nsew')
c1.grid(column=2, row=5)
c2.grid(column=3, row=5)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=1)
mainframe.columnconfigure(2, weight=1)
mainframe.columnconfigure(3, weight=1)
mainframe.rowconfigure(0, weight=1)
mainframe.rowconfigure(2, weight=1)

root.mainloop()
