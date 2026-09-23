#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.7 - How do I make my own dialog?
# source:   wxPythonInAction-src/Chapter-09/modal_dialog.py
# -----------------------------------------------------------------------------
"""A dialog of one's own, with an OK and a Cancel that mean something.

wx.Dialog knows about wx.ID_OK and wx.ID_CANCEL: a button given one of
those ids closes the dialog and ShowModal returns it. The knowledge is in
the ids.

simpledialog.Dialog knows about two methods instead. buttonbox() may be
replaced to change the buttons; ok() and cancel() are what they call; and
apply() runs on OK and not on Cancel, which is where the answer is taken
out of the widgets before they are destroyed.
"""
import tkinter as tk
from tkinter import simpledialog


class SubclassDialog(simpledialog.Dialog):
    """A dialog with a field in it, and an answer afterwards."""

    def __init__(self, parent):
        self.answer = None

        super().__init__(parent, "Dialog Subclass")

    def body(self, master):
        """What is returned takes the keyboard focus."""
        lbl_prompt = tk.Label(master, text="Say something:")
        lbl_prompt.pack(anchor=tk.W)

        self.ent_answer = tk.Entry(master, width=30)
        self.ent_answer.pack(pady=5)

        return self.ent_answer

    def validate(self):
        """Called on OK, before apply(). Returning false keeps it open.

        This is where wx would use a wx.Validator, and it is simpler: one
        method, called once, on the dialog that knows what it wants.
        """
        return bool(self.ent_answer.get().strip())

    def apply(self):
        """On OK, and after validate() agreed. The widgets still exist
        here and will not a moment later, so this is where to read them."""
        self.answer = self.ent_answer.get()


def main():
    """Show it and say what came back."""
    root = tk.Tk()
    root.withdraw()

    dialog = SubclassDialog(root)

    if dialog.answer is None:
        print("Cancel")
    else:
        print("OK: {}".format(dialog.answer))

    root.destroy()


if __name__ == "__main__":
    main()
