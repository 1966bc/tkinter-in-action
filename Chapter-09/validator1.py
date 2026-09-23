#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.9 - How do I check what was typed?
# source:   wxPythonInAction-src/Chapter-09/validator1.py
# -----------------------------------------------------------------------------
"""Three fields that must not be empty when OK is pressed.

wx attaches a validator object to each field. Tkinter has no such object
and does not need one here: a dialog that knows what it wants can say so
in one method. See README.md.
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


ABOUT = ("The check in this example makes sure the fields are not empty\n"
         "when OK is pressed, and will not let you leave if one is.")

FIELDS = ("Name", "Email", "Phone")

EMPTY = "pink"


class MyDialog(simpledialog.Dialog):
    """A form that refuses to close with an empty field in it."""

    def __init__(self, parent):
        self.entries = {}
        self.answers = None

        super().__init__(parent, "Validators: validating")

    def body(self, master):
        """A caption and a field for each name."""
        lbl_about = tk.Label(master, text=ABOUT, justify=tk.LEFT)
        lbl_about.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)

        for index, name in enumerate(FIELDS):
            lbl_field = tk.Label(master, text=name + ":")
            lbl_field.grid(row=index + 1, column=0, sticky=tk.W, pady=2)

            entry = tk.Entry(master, width=24)
            entry.grid(row=index + 1, column=1, sticky=tk.E + tk.W, pady=2)

            self.entries[name] = entry

        return self.entries[FIELDS[0]]

    def validate(self):
        """Called on OK. Returning false keeps the dialog open.

        wx asks each validator in turn and stops at the first that
        refuses. This is the same walk, and it is in the dialog because
        that is what knows that these three fields go together.
        """
        wrong = None

        for name in FIELDS:
            entry = self.entries[name]

            if entry.get().strip():
                entry.config(background="white")
            else:
                entry.config(background=EMPTY)

                if wrong is None:
                    wrong = name

        if wrong is not None:
            messagebox.showerror("Error", "This field must contain "
                                          "some text!", parent=self)
            self.entries[wrong].focus_set()

        return wrong is None

    def apply(self):
        """On OK, and only after validate() agreed."""
        self.answers = {}

        for name in FIELDS:
            self.answers[name] = self.entries[name].get()


def main():
    """Ask, and print what was given."""
    root = tk.Tk()
    root.withdraw()

    dialog = MyDialog(root)

    if dialog.answers is None:
        print("Cancel")
    else:
        for name in FIELDS:
            print("{}: {}".format(name, dialog.answers[name]))

    root.destroy()


if __name__ == "__main__":
    main()
