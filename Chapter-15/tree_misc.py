#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  15.3 - What events does a tree raise?
# source:   wxPythonInAction-src/Chapter-15/tree_misc.py
# -----------------------------------------------------------------------------
"""The events, sorting a branch, and editing a label in place.

wx raises six: expanding, expanded, collapsing, collapsed, selection
changed, activated - and begin label edit, which can be refused.

Tk raises three: <<TreeviewOpen>>, <<TreeviewClose>>, <<TreeviewSelect>>.
There is no *expanding* - nothing to refuse, and nothing to fill a branch
during, which tree_virtual.py has to work around - no activation event,
and no label editing at all. See README.md.
"""
import tkinter as tk
from tkinter import ttk

import data


class App(tk.Tk):
    """A tree that says what is happening to it."""

    def __init__(self):
        super().__init__()

        self.title("Tree events")
        self.geometry("560x460")

        # The Entry used to edit a label, when there is one.
        self.editor = None

        self.set_menu_bar()

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_tree = ttk.Treeview(frm_main, selectmode="browse")
        self.trv_tree.heading("#0", text=data.COLUMNS[0], anchor=tk.W)
        self.trv_tree.pack(fill=tk.BOTH, expand=True)

        self.trv_tree.bind("<<TreeviewOpen>>", self.on_item_expanded)
        self.trv_tree.bind("<<TreeviewClose>>", self.on_item_collapsed)
        self.trv_tree.bind("<<TreeviewSelect>>", self.on_selection_changed)
        self.trv_tree.bind("<Double-Button-1>", self.on_activated)
        self.trv_tree.bind("<Return>", self.on_activated)

        self.lbl_said = tk.Label(self, anchor=tk.W, relief=tk.SUNKEN,
                                 borderwidth=1)
        self.lbl_said.pack(side=tk.BOTTOM, fill=tk.X)

        self.root = self.trv_tree.insert("", tk.END, text=data.ROOT,
                                         open=True)
        self.set_children(self.root, data.TREE)

    def set_menu_bar(self):
        """Sorting a branch, which wx has as SortChildren."""
        mnu_bar = tk.Menu(self, tearoff=0)
        mnu_tree = tk.Menu(mnu_bar, tearoff=0)

        mnu_tree.add_command(label="Sort the chosen branch",
                             command=self.on_sort_children)
        mnu_tree.add_command(label="Edit the chosen label",
                             command=self.on_edit_label)
        mnu_tree.add_separator()
        mnu_tree.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Tree", underline=0, menu=mnu_tree)
        self.config(menu=mnu_bar)

    def set_children(self, parent, nodes):
        """The whole hierarchy."""
        for name, note, children in nodes:
            item = self.trv_tree.insert(parent, tk.END, text=name)
            self.set_children(item, children)

    def say(self, what, item):
        """Put a line in the status bar."""
        self.lbl_said.config(text="{}: {}".format(
            what, self.trv_tree.item(item, "text")))

    def on_item_expanded(self, event):
        """EVT_TREE_ITEM_EXPANDED. focus() is the item it happened to."""
        self.say("Expanded", self.trv_tree.focus())

    def on_item_collapsed(self, event):
        """EVT_TREE_ITEM_COLLAPSED."""
        self.say("Collapsed", self.trv_tree.focus())

    def on_selection_changed(self, event):
        """EVT_TREE_SEL_CHANGED, and the widget is asked what is chosen."""
        selected = self.trv_tree.selection()

        if selected:
            self.say("Selected", selected[0])

    def on_activated(self, event):
        """EVT_TREE_ITEM_ACTIVATED, which is a binding here.

        Bound to Return as well as to a double click, because a tree that
        answers the mouse and not the keyboard is half a tree.
        """
        item = self.trv_tree.focus()

        if item:
            self.say("Activated", item)

    def on_sort_children(self):
        """Sort one branch, the same way chapter 13 sorts a table.

        wx.TreeCtrl has SortChildren and a comparison method to override.
        There is nothing to override here: the children are fetched, put
        in order, and moved.
        """
        parent = self.trv_tree.focus() or self.root
        children = list(self.trv_tree.get_children(parent))

        children.sort(key=lambda item: self.trv_tree.item(item, "text"))

        for position, item in enumerate(children):
            self.trv_tree.move(item, parent, position)

        self.say("Sorted the children of", parent)

    def on_edit_label(self):
        """What EVT_TREE_BEGIN_LABEL_EDIT is for, built by hand.

        A wx.TreeCtrl with TR_EDIT_LABELS lets a label be typed over in
        place, and raises an event that may refuse. A Treeview has
        nothing of the kind, so an Entry is put over the row and taken
        away again. It is the same answer as editing a cell in chapter 5,
        and the same fifty lines everybody writes.
        """
        item = self.trv_tree.focus()

        if item and self.editor is None:
            box = self.trv_tree.bbox(item, "#0")

            if box:
                self.set_editor(item, box)

    def set_editor(self, item, box):
        """Put an Entry exactly over the label and let it be typed in."""
        x, y, width, height = box

        self.editor = tk.Entry(self.trv_tree)
        self.editor.insert(0, self.trv_tree.item(item, "text"))
        self.editor.select_range(0, tk.END)
        self.editor.place(x=x, y=y, width=width, height=height)
        self.editor.focus_set()

        self.editor.bind("<Return>", lambda event: self.on_end_edit(item,
                                                                    True))
        self.editor.bind("<Escape>", lambda event: self.on_end_edit(item,
                                                                    False))
        self.editor.bind("<FocusOut>", lambda event: self.on_end_edit(item,
                                                                      False))

    def on_end_edit(self, item, keep):
        """Take the Entry away, keeping what was typed or not."""
        if self.editor is not None:
            if keep:
                self.trv_tree.item(item, text=self.editor.get())

            self.editor.destroy()
            self.editor = None
            self.say("Edited", item)


if __name__ == "__main__":
    app = App()
    app.mainloop()
