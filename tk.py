from tkinter import *
from tkinter import ttk

import tkinter as tk
from PIL import ImageGrab, Image, ImageTk

from ocr_lib import *
from im_lib import *


# Tkinter window setup
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()


# Grab image from clipboard
# im = ImageGrab.grabclipboard()

# Check if image exists and create a Tkinter image object
# if isinstance(im, Image.Image):
#     im = resize_to_fit(im, 720, 720 / 1.33)  # Resize the image (optional)
#     tk_image = ImageTk.PhotoImage(im)

#     # Display the image in a Label widget
#     label = Label(frm, image=tk_image)
#     label.grid(column=0, row=1, columnspan=1)
# else:
#     print("No image in clipboard")

# # Quit button
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

text_widget = Text(frm)
text_widget.grid(column=1, row=1)
# Disable the widget to prevent editing
text_widget.config(state=DISABLED)


label_widget = Label(frm)
label_widget.grid(column=0, row=1, columnspan=1)


check_var = tk.BooleanVar()


checkbox = tk.Checkbutton(
    root, text="English Only", variable=check_var
)
checkbox.grid(column=1, row=2)
def update_content():

    en_only = check_var.get()

    # Grab image from clipboard
    im = ImageGrab.grabclipboard()
    result = ocr(from_pil(im)) if not en_only else ocr(from_pil(im), lang="en")

    lines = text_only(result)
    text = "\n".join(lines)
    boxes = boxes_only(result)
    im_box = draw_polygons(im, boxes)

    im_tk = ImageTk.PhotoImage(resize_to_fit(im_box, 720, 720 / 1.33))

    # Update text in the Text widget
    text_widget.config(state=NORMAL)
    text_widget.delete(1.0, tk.END)  # Clear the current text
    text_widget.insert(tk.END, text)
    max_length = max(len(line) for line in lines)
    text_widget.config(width=max_length if en_only else 50, height = 20)
    text_widget.config(state=DISABLED)

    label_widget.config(image=im_tk)
    label_widget.image = im_tk  # Keep a reference to avoid garbage collection

# Hello World label
ttk.Button(frm, text="Click me", command=update_content).grid(column=0, row=0)

root.mainloop()
