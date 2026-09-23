#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.9 - How do I stop the wrong characters being typed?
# source:   wxPythonInAction-src/Chapter-09/validator3.py
# -----------------------------------------------------------------------------
"""Fields that will not accept a letter, or will not accept a digit.

This is the one wx has to fight for and Tkinter is built for. wx binds
EVT_CHAR, decides, and either calls Skip() to let the character through or
does not. A Tk Entry has validatecommand, whose whole purpose is to be
asked before an edit happens and to be allowed to say no.

    %P   what the field would say if the edit were allowed
    %S   the text being inserted
    %d   1 for an insertion, 0 for a deletion

Returning false leaves the field exactly as it was. See README.md.
"""
import tkinter as tk
from tkinter import simpledialog


ABOUT = ("The first field will not accept letters, the second accepts\n"
         "anything, and the third will not accept digits.")


class MyDialog(simpledialog.Dialog):
    """Three fields, two of them fussy."""

    def __init__(self, parent):
        self.entries = {}
        self.answers = None

        super().__init__(parent, "Validators: validating on the fly")

    def body(self, master):
        """A caption and three fields with three different rules."""
        lbl_about = tk.Label(master, text=ABOUT, justify=tk.LEFT)
        lbl_about.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.set_field(master, 1, "Phone", self.get_no_letters())
        self.set_field(master, 2, "Email", None)
        self.set_field(master, 3, "Name", self.get_no_digits())

        return self.entries["Phone"]

    def set_field(self, master, row, name, rule):
        """One caption and one field, with a rule or without."""
        lbl_field = tk.Label(master, text=name + ":")
        lbl_field.grid(row=row, column=0, sticky=tk.W, pady=2)

        entry = tk.Entry(master, width=24)

        if rule is not None:
            # register() gives Tcl a name for a Python function, and the
            # %P is the substitution Tk fills in before calling it.
            entry.config(validate="key",
                         validatecommand=(self.register(rule), "%P"))

        entry.grid(row=row, column=1, sticky=tk.E + tk.W, pady=2)
        self.entries[name] = entry

    def get_no_letters(self):
        """A rule that refuses any edit leaving a letter in the field."""
        def rule(proposed):
            """True if the edit may happen."""
            return not any(character.isalpha() for character in proposed)

        return rule

    def get_no_digits(self):
        """A rule that refuses any edit leaving a digit in the field."""
        def rule(proposed):
            """True if the edit may happen."""
            return not any(character.isdigit() for character in proposed)

        return rule

    def apply(self):
        """On OK."""
        self.answers = {}

        for name, entry in self.entries.items():
            self.answers[name] = entry.get()


def main():
    """Ask, and print what got through."""
    root = tk.Tk()
    root.withdraw()

    dialog = MyDialog(root)

    if dialog.answers is None:
        print("Cancel")
    else:
        print(dialog.answers)

    root.destroy()


if __name__ == "__main__":
    main()
