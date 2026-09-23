#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  2.2 - How do I write a program with no main window?
# source:   wxPythonInAction-src/Chapter-02/dialog_scratch.py
# -----------------------------------------------------------------------------
"""Three questions and no window behind them.

Two of the three dialogs are in the standard library. The third, a list to
pick one thing from, is not, and is built here out of simpledialog.Dialog.
See README.md.
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog


VERSIONS = ["1.5.2", "2.0", "2.1.3", "2.2", "2.3.1"]


class SingleChoiceDialog(simpledialog.Dialog):
    """What wx.SingleChoiceDialog does, since Tkinter has nothing like it.

    simpledialog.Dialog supplies the modal window, the OK and Cancel, the
    escape key and the wait: body() fills it, apply() is called if OK was
    pressed and not if it was not. What is left to write is the list.
    """

    def __init__(self, parent, title, prompt, choices):
        self.prompt = prompt
        self.choices = choices
        self.choice = None

        # Last, because this is what shows the dialog and waits for it.
        super().__init__(parent, title)

    def body(self, master):
        """The prompt and the list. What is returned takes the focus."""
        lbl_prompt = tk.Label(master, text=self.prompt)
        lbl_prompt.pack(anchor=tk.W, pady=(0, 5))

        self.lst_choices = tk.Listbox(master, height=len(self.choices),
                                      exportselection=False)

        for choice in self.choices:
            self.lst_choices.insert(tk.END, choice)

        self.lst_choices.selection_set(0)
        self.lst_choices.pack(fill=tk.BOTH, expand=True)

        return self.lst_choices

    def apply(self):
        """Called on OK, and not on Cancel, which is the whole protocol."""
        selected = self.lst_choices.curselection()

        if selected:
            self.choice = self.choices[selected[0]]


class App(tk.Tk):
    """Three dialogs, asked one after the other, and then nothing."""

    def __init__(self):
        super().__init__()

        # There has to be a Tk for a dialog to belong to, and it must not be
        # seen. wx has no equivalent step because a wx.App is not a window.
        self.withdraw()

        messagebox.askyesno("MessageDialog",
                            "Is this the coolest thing ever!", parent=self)

        simpledialog.askstring("A Question",
                               "Who is buried in Grant's tomb?",
                               initialvalue="Cary Grant", parent=self)

        SingleChoiceDialog(self, "Single Choice",
                           "What version of Python are you using?", VERSIONS)

        self.destroy()


if __name__ == "__main__":
    app = App()
