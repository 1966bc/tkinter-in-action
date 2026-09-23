#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  15.4 - Can a tree have columns?
# source:   wxPythonInAction-src/Chapter-15/tree_treelist.py
# -----------------------------------------------------------------------------
"""A tree with a second column beside it.

wx needs a different widget for this: wx.gizmos.TreeListCtrl, which is a
contributed control with its own AddColumn and SetItemText(item, text,
column).

A ttk.Treeview is already both. The tree lives in column #0 and any other
columns are given when it is made - which is why chapter 13 uses the same
widget for a flat table. One widget, two chapters.
"""
import tkinter as tk
from tkinter import ttk

import data


class App(tk.Tk):
    """A window with a tree that has a description column."""

    def __init__(self):
        super().__init__()

        self.title("Tree with columns")
        self.geometry("680x420")

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_tree = ttk.Treeview(frm_main, columns=("description",),
                                     selectmode="browse")

        self.trv_tree.heading("#0", text=data.COLUMNS[0], anchor=tk.W)
        self.trv_tree.heading("description", text=data.COLUMNS[1],
                              anchor=tk.W)

        self.trv_tree.column("#0", width=280, stretch=False)
        self.trv_tree.column("description", anchor=tk.W, stretch=True)

        scrollbar = ttk.Scrollbar(frm_main, orient=tk.VERTICAL,
                                  command=self.trv_tree.yview)
        self.trv_tree.config(yscrollcommand=scrollbar.set)

        self.trv_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.root = self.trv_tree.insert("", tk.END, text=data.ROOT,
                                         values=("Everything below",),
                                         open=True)
        self.set_children(self.root, data.TREE)

    def set_children(self, parent, nodes):
        """text is the tree column, values are all the others."""
        for name, note, children in nodes:
            item = self.trv_tree.insert(parent, tk.END, text=name,
                                        values=(note,))
            self.set_children(item, children)


if __name__ == "__main__":
    app = App()
    app.mainloop()
