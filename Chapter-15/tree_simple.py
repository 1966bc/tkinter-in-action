#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  15.1 - How do I make a tree?
# source:   wxPythonInAction-src/Chapter-15/tree_simple.py
# -----------------------------------------------------------------------------
"""A tree with a root, branches and leaves.

wx.TreeCtrl has AddRoot and then AppendItem under whatever is given. A
ttk.Treeview has insert(parent, index, ...), and the root of the tree is
the empty string - not an item one makes, but the absence of a parent.

Which means a Treeview can have several roots and a wx.TreeCtrl cannot,
and that a tree with one visible root has to make it like any other item.
"""
import tkinter as tk
from tkinter import ttk

import data


class App(tk.Tk):
    """A window with the hierarchy in it."""

    def __init__(self):
        super().__init__()

        self.title("Simple Tree")
        self.geometry("460x420")

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_tree = ttk.Treeview(frm_main, selectmode="browse")
        self.trv_tree.heading("#0", text=data.COLUMNS[0], anchor=tk.W)

        scrollbar = ttk.Scrollbar(frm_main, orient=tk.VERTICAL,
                                  command=self.trv_tree.yview)
        self.trv_tree.config(yscrollcommand=scrollbar.set)

        self.trv_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.root = self.trv_tree.insert("", tk.END, text=data.ROOT,
                                         open=True)
        self.set_children(self.root, data.TREE)

    def set_children(self, parent, nodes):
        """Put a branch in, and everything under it.

        The whole tree at once, which is what the original does. For a
        big one this is the wrong thing and tree_virtual.py is the right
        one.
        """
        for name, note, children in nodes:
            item = self.trv_tree.insert(parent, tk.END, text=name)
            self.set_children(item, children)


if __name__ == "__main__":
    app = App()
    app.mainloop()
