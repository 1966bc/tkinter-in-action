#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  13.3 - What else can a list control do?
# source:   wxPythonInAction-src/Chapter-13/list_report_etc.py
# -----------------------------------------------------------------------------
"""The same rows, with the options a list control is usually given.

A menu that turns the headings off, switches between one selection and
many, and stripes the rows. And the three events: selected, deselected,
activated. See README.md for the one option that has no equivalent.
"""
import tkinter as tk
from tkinter import ttk

import data


STRIPE = "#f0f0f0"


class App(tk.Tk):
    """A window whose list can be told how to behave."""

    def __init__(self):
        super().__init__()

        self.title("Treeview options")
        self.geometry("660x420")

        self.headings = tk.BooleanVar(value=True)
        self.many = tk.BooleanVar(value=False)
        self.striped = tk.BooleanVar(value=False)

        self.set_menu_bar()

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_rows = ttk.Treeview(frm_main, columns=data.COLUMNS,
                                     show="headings", selectmode="browse")

        for name in data.COLUMNS:
            self.trv_rows.heading(name, text=name, anchor=tk.W)
            self.trv_rows.column(name, anchor=tk.W, width=145, stretch=True)

        scrollbar = ttk.Scrollbar(frm_main, orient=tk.VERTICAL,
                                  command=self.trv_rows.yview)
        self.trv_rows.config(yscrollcommand=scrollbar.set)

        self.trv_rows.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # A tag is a name given to rows, and its appearance is configured
        # once. This is how a Treeview is striped, and it is the nearest
        # thing to the rules a wx.ListCtrl can be asked for.
        self.trv_rows.tag_configure("odd", background=STRIPE)

        self.trv_rows.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.trv_rows.bind("<Double-Button-1>", self.on_item_activated)

        self.lbl_said = tk.Label(self, anchor=tk.W, relief=tk.SUNKEN,
                                 borderwidth=1)
        self.lbl_said.pack(side=tk.BOTTOM, fill=tk.X)

        self.set_rows()

    def set_menu_bar(self):
        """What the wx original asks for with style flags."""
        mnu_bar = tk.Menu(self, tearoff=0)
        mnu_list = tk.Menu(mnu_bar, tearoff=0)

        mnu_list.add_checkbutton(label="Show headings",
                                 variable=self.headings,
                                 command=self.on_headings)
        mnu_list.add_checkbutton(label="Select many",
                                 variable=self.many, command=self.on_many)
        mnu_list.add_checkbutton(label="Stripe the rows",
                                 variable=self.striped,
                                 command=self.on_striped)
        mnu_list.add_separator()
        mnu_list.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="List", underline=0, menu=mnu_list)
        self.config(menu=mnu_bar)

    def set_rows(self):
        """Put the rows in, striping every other one if asked."""
        self.trv_rows.delete(*self.trv_rows.get_children(""))

        for index, row in enumerate(data.ROWS):
            tags = ()

            if self.striped.get() and index % 2:
                tags = ("odd",)

            self.trv_rows.insert("", tk.END, values=row, tags=tags)

    def on_headings(self):
        """LC_NO_HEADER, which is show="" against show="headings"."""
        shown = "headings"

        if not self.headings.get():
            shown = ""

        self.trv_rows.config(show=shown)

    def on_many(self):
        """LC_SINGLE_SEL, the other way round.

        browse is one row at a time, extended is several with shift and
        control. There is also none, which is a list nobody can choose
        anything in and is sometimes what a display wants.
        """
        mode = "browse"

        if self.many.get():
            mode = "extended"

        self.trv_rows.config(selectmode=mode)

    def on_striped(self):
        """Stripes have to be put back on the rows, so they go in again."""
        self.set_rows()

    def on_item_selected(self, event):
        """<<TreeviewSelect>> is raised once for the new selection.

        wx raises EVT_LIST_ITEM_SELECTED and EVT_LIST_ITEM_DESELECTED
        separately and tells each one which item. Tk raises one event and
        tells you nothing: the widget is asked what is selected now, and
        what was selected before is yours to remember if you need it.
        """
        selected = self.trv_rows.selection()

        if not selected:
            self.lbl_said.config(text="Nothing selected.")
        else:
            first = self.trv_rows.set(selected[0], data.COLUMNS[0])
            self.lbl_said.config(text="Selected: {} ({} row(s))".format(
                first, len(selected)))

    def on_item_activated(self, event):
        """EVT_LIST_ITEM_ACTIVATED: a double click, or Return.

        Tk has no such event either. A double click is a binding, and
        Return has to be bound as well if it is to work the same way -
        which it should, because that is how a keyboard gets through a
        list.
        """
        selected = self.trv_rows.selection()

        if selected:
            first = self.trv_rows.set(selected[0], data.COLUMNS[0])
            self.lbl_said.config(text="Activated: {}".format(first))


if __name__ == "__main__":
    app = App()
    app.mainloop()
