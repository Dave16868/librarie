from tkinter import Tk, ttk, Label, Text

window = Tk()
print(window)
window.title("librarie")

label = ttk.Label(window, text="Tkinter Window")
label.pack()

button = ttk.Button(window, width=25, text="moo button")
button.pack()

entry= ttk.Entry(window)
entry.pack()

text_box = Text(window)
text_box.pack()

window.mainloop()
