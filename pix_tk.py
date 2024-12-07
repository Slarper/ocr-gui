from tkinter import *
from tkinter import ttk

import tkinter as tk
from PIL import ImageGrab, Image, ImageTk

from ocr_lib import *
from im_lib import *
from pix2text import Pix2Text
import pyperclip

# Tkinter window setup
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

text_widget = Text(frm)
text_widget.grid(column=1, row=1, columnspan = 2)
# Disable the widget to prevent editing
# text_widget.config(state=DISABLED)


label_widget = Label(frm)
# label_widget.grid(column=1, row=0, columnspan=1)
label_widget.grid(column=0, row=1)


check_var = tk.BooleanVar()


# checkbox = tk.Checkbutton(root, text="English Only", variable=check_var)
# checkbox.grid(column=1, row=2)


def update_content():

    # Grab image from clipboard
    im = ImageGrab.grabclipboard()

    p2t = Pix2Text.from_config()
    outs = p2t.recognize_formula(im)

    # Update text in the Text widget
    text_widget.config(state=NORMAL)
    text_widget.delete(1.0, tk.END)  # Clear the current text
    text_widget.insert(tk.END, outs)
    text_widget.config(width=50, height=20)
    # text_widget.config(state=DISABLED)

    im_tk = ImageTk.PhotoImage(resize_to_fit(im, 500, 200))

    label_widget.config(image=im_tk)
    label_widget.image = im_tk  # Keep a reference to avoid garbage collection
    return outs


def update_2():
    outs = text_widget.get(1.0, tk.END)
    out = "$$\n" + outs + "\n$$\n"
    pyperclip.copy(out)


def update_3():
    outs = text_widget.get(1.0, tk.END)
    outs = outs.rstrip("\n")
    out = "$" + outs + "$ "
    pyperclip.copy(out)


# Hello World label
ttk.Button(frm, text="Click me", command=update_content).grid(column=0, row=0)
ttk.Button(frm, text="Copy as block", command=update_2).grid(column=1, row=0)
ttk.Button(frm, text="Copy as snippet", command=update_3).grid(column=2, row=0)

root.mainloop()
