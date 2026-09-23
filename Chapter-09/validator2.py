#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.9 - How do I move data in and out of the fields?
# source:   wxPythonInAction-src/Chapter-09/validator2.py
# -----------------------------------------------------------------------------
"""A dictionary in, the same dictionary out, and no code in between.

wx gives its validator TransferToWindow and TransferFromWindow, called
when the dialog opens and when OK is pressed, and the validator carries a
reference to the data and the key it is responsible for.

Tkinter does the same thing with a StringVar, and it does it continuously
rather than twice: a variable given to a field with textvariable is the
field, in both directions, at every moment. What is left to write is the
step from the variables to the dictionary. See README.md.
"""
import tkinter as tk
from tkinter import simpledialog


ABOUT = ("Each field is tied to a variable, and the variable is the\n"
         "field. Nothing copies anything while the dialog is open.")

FIELDS = ("Name", "Email", "Phone")


class MyDialog(simpledialog.Dialog):
    """A form over a dictionary."""

    def __init__(self, parent, data):
        self.data = data
        self.values = {}
        self.saved = False

        super().__init__(parent, "Validators: data transfer")

    def body(self, master):
        """A caption and a field for each name, each with its variable."""
        lbl_about = tk.Label(master, text=ABOUT, justify=tk.LEFT)
        lbl_about.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)

        for index, name in enumerate(FIELDS):
            # This is TransferToWindow, and it is the constructor.
            self.values[name] = tk.StringVar(value=self.data.get(name, ""))

            lbl_field = tk.Label(master, text=name + ":")
            lbl_field.grid(row=index + 1, column=0, sticky=tk.W, pady=2)

            entry = tk.Entry(master, width=24,
                             textvariable=self.values[name])
            entry.grid(row=index + 1, column=1, sticky=tk.E + tk.W, pady=2)

        return master

    def apply(self):
        """And this is TransferFromWindow.

        It is here and not on the variables because the dictionary must
        not be changed unless OK was pressed. The variables have been
        following the fields all along; this is the moment the answer is
        accepted.
        """
        for name in FIELDS:
            self.data[name] = self.values[name].get()

        self.saved = True


def main():
    """Show a dialog over a dictionary and print it afterwards."""
    root = tk.Tk()
    root.withdraw()

    data = {"Name": "Jane Doe", "Email": "jdoe@example.com", "Phone": ""}
    dialog = MyDialog(root, data)

    if dialog.saved:
        print(data)
    else:
        print("Cancel, and the dictionary is untouched: {}".format(data))

    root.destroy()


if __name__ == "__main__":
    main()
