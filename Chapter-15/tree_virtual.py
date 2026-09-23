#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  15.5 - How do I show a tree too big to build?
# source:   wxPythonInAction-src/Chapter-15/tree_virtual.py
# -----------------------------------------------------------------------------
"""A tree that is filled a branch at a time, as it is opened.

The interesting file of the chapter, because of what it says about the
one before it. A **virtual list** has no answer in Tkinter - chapter 13
says so - and a **virtual tree** has a good one, for a reason that is
worth seeing.

A list is flat. Nothing happens between one row and the next, so there is
no moment at which a program could be asked for row nine hundred
thousand: the widget simply has the rows or it does not.

A tree has an event. A branch is opened, and that is the moment. So a
Treeview given one empty child per branch shows an expander, and fills
the branch the first time somebody asks for it - and the rest of the
hierarchy is never built at all.

This is the same pattern as the namespace tree in chapter 4, and it is
the one Tkinter pattern in this book worth learning by heart.
"""
import tkinter as tk
from tkinter import ttk

import data


class App(tk.Tk):
    """A tree that builds itself as it is explored."""

    def __init__(self):
        super().__init__()

        self.title("Tree filled on demand")
        self.geometry("560x460")

        # What is under each item, kept until it is needed.
        self.pending = {}
        self.built = 0

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_tree = ttk.Treeview(frm_main, selectmode="browse")
        self.trv_tree.heading("#0", text=data.COLUMNS[0], anchor=tk.W)
        self.trv_tree.pack(fill=tk.BOTH, expand=True)

        self.trv_tree.bind("<<TreeviewOpen>>", self.on_open)

        self.lbl_said = tk.Label(self, anchor=tk.W, relief=tk.SUNKEN,
                                 borderwidth=1)
        self.lbl_said.pack(side=tk.BOTTOM, fill=tk.X)

        self.root = self.add_item("", data.ROOT, data.TREE)
        self.say()

    def add_item(self, parent, name, children):
        """One item, with a dummy child if there is anything under it.

        The dummy is what makes the expander appear. Without it a branch
        with nothing in it yet looks like a leaf and cannot be opened, so
        the event that would fill it never comes.
        """
        item = self.trv_tree.insert(parent, tk.END, text=name)
        self.built = self.built + 1

        if children:
            self.trv_tree.insert(item, tk.END, text="")
            self.pending[item] = children

        return item

    def on_open(self, event):
        """Fill a branch the first time it is asked for."""
        item = self.trv_tree.focus()
        children = self.pending.pop(item, None)

        if children is not None:
            self.trv_tree.delete(*self.trv_tree.get_children(item))

            for name, note, grandchildren in children:
                self.add_item(item, name, grandchildren)

            self.say()

    def say(self):
        """How much of the hierarchy has actually been made."""
        self.lbl_said.config(text="Items built so far: {}".format(self.built))


if __name__ == "__main__":
    app = App()
    app.mainloop()
