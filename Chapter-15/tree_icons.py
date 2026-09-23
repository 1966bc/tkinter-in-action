#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  15.2 - How do I put pictures on the items?
# source:   wxPythonInAction-src/Chapter-15/tree_icons.py
# -----------------------------------------------------------------------------
"""A tree where a branch looks different when it is open.

wx keeps an image list and gives each item an index into it, with a
separate index for the selected and expanded states -
SetItemImage(item, index, wx.TreeItemIcon_Expanded).

A Treeview item takes an image directly, and has no notion of a different
one when open. So the swapping is done by hand, on the events the widget
does raise, which is four lines and works the same.
"""
import tkinter as tk
from tkinter import ttk

import data


SIZE = 14


class App(tk.Tk):
    """A window whose folders open and shut."""

    def __init__(self):
        super().__init__()

        self.title("Tree with icons")
        self.geometry("460x420")

        # Held on self, or collected before the tree is drawn.
        self.icons = {"shut": self.get_icon("#c8a45a", "#8c6a20"),
                      "open": self.get_icon("#e8d49a", "#8c6a20"),
                      "leaf": self.get_icon("white", "#808080")}

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_tree = ttk.Treeview(frm_main, selectmode="browse")
        self.trv_tree.heading("#0", text=data.COLUMNS[0], anchor=tk.W)
        self.trv_tree.pack(fill=tk.BOTH, expand=True)

        self.trv_tree.bind("<<TreeviewOpen>>", self.on_open)
        self.trv_tree.bind("<<TreeviewClose>>", self.on_close)

        self.root = self.trv_tree.insert("", tk.END, text=data.ROOT,
                                         image=self.icons["open"], open=True)
        self.set_children(self.root, data.TREE)

    def get_icon(self, fill, edge):
        """A small square, drawn rather than loaded."""
        icon = tk.PhotoImage(width=SIZE, height=SIZE)
        icon.put(edge, to=(0, 0, SIZE, SIZE))
        icon.put(fill, to=(2, 2, SIZE - 2, SIZE - 2))

        return icon

    def set_children(self, parent, nodes):
        """A branch gets a folder, a leaf gets a leaf."""
        for name, note, children in nodes:
            icon = self.icons["leaf"]

            if children:
                icon = self.icons["shut"]

            item = self.trv_tree.insert(parent, tk.END, text=name,
                                        image=icon)
            self.set_children(item, children)

    def on_open(self, event):
        """The one that was opened, which the widget knows and the event
        does not say: focus() is where the action was."""
        item = self.trv_tree.focus()

        if self.trv_tree.get_children(item):
            self.trv_tree.item(item, image=self.icons["open"])

    def on_close(self, event):
        """And back again."""
        item = self.trv_tree.focus()

        if self.trv_tree.get_children(item):
            self.trv_tree.item(item, image=self.icons["shut"])


if __name__ == "__main__":
    app = App()
    app.mainloop()
