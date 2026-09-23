#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.2 - How do I ask somebody to pick one of these?
# source:   wxPythonInAction-src/Chapter-09/choice_box.py
# -----------------------------------------------------------------------------
"""A list of words, and one of them chosen.

wx.SingleChoiceDialog has no counterpart, as Chapter-02 found. This is the
same stand-in, and it is here because this is the chapter where the book
introduces it.
"""
import tkinter as tk
from tkinter import simpledialog


CHOICES = ("Alpha", "Baker", "Charlie", "Delta")


class SingleChoiceDialog(simpledialog.Dialog):
    """A modal list to choose one thing from.

    simpledialog.Dialog gives the window, the buttons, the escape key and
    the waiting. body() fills it and returns what takes the focus; apply()
    runs on OK and not on Cancel.
    """

    def __init__(self, parent, title, prompt, choices):
        self.prompt = prompt
        self.choices = choices
        self.choice = None

        super().__init__(parent, title)

    def body(self, master):
        """The prompt and the list."""
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
        """On OK only."""
        selected = self.lst_choices.curselection()

        if selected:
            self.choice = self.choices[selected[0]]


def main():
    """Ask, and print what was chosen."""
    root = tk.Tk()
    root.withdraw()

    dialog = SingleChoiceDialog(root, "Choices", "Pick A Word", CHOICES)

    if dialog.choice is not None:
        print("You selected: {}".format(dialog.choice))

    root.destroy()


if __name__ == "__main__":
    main()
