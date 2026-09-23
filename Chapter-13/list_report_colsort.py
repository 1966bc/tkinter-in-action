#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  13.4 - How do I sort by clicking a column?
# source:   wxPythonInAction-src/Chapter-13/list_report_colsort.py
# -----------------------------------------------------------------------------
"""Click a heading and the rows sort by it. Click again and they reverse.

wx has a mixin for this, ColumnSorterMixin, which wants the data in a
dictionary keyed by item, a GetListCtrl method and a pair of arrow
bitmaps. Tkinter has no mixin and nothing to inherit: a heading takes a
command, and the sorting is eight lines.

The eight lines are worth reading for one of them. A column of numbers
sorted as text puts 10 before 9, and that is the bug this file exists to
avoid. See README.md.
"""
import tkinter as tk
from tkinter import ttk

import data


ARROWS = {True: " ▼", False: " ▲"}


class App(tk.Tk):
    """A window whose columns sort when their headings are clicked."""

    def __init__(self):
        super().__init__()

        self.title("Sorting by column")
        self.geometry("640x360")

        # Which column is sorted, and whether backwards.
        self.sorted_by = None
        self.reverse = False

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_rows = ttk.Treeview(frm_main, columns=data.COLUMNS,
                                     show="headings", selectmode="browse")

        for name in data.COLUMNS:
            self.trv_rows.heading(
                name, text=name, anchor=tk.W,
                command=lambda column=name: self.on_heading(column))
            self.trv_rows.column(name, anchor=tk.W, width=140, stretch=True)

        scrollbar = ttk.Scrollbar(frm_main, orient=tk.VERTICAL,
                                  command=self.trv_rows.yview)
        self.trv_rows.config(yscrollcommand=scrollbar.set)

        self.trv_rows.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for row in data.ROWS:
            self.trv_rows.insert("", tk.END, values=row)

    def get_key(self, column):
        """How to read a value in that column so that it sorts properly.

        Everything in a Treeview is text. A column of numbers sorted as
        text puts 10 before 9 and 1001 before 42, and the list looks
        sorted, which is what makes it expensive: nobody checks a sorted
        list.
        """
        def key(item):
            """One row's value, as the thing it actually is."""
            value = self.trv_rows.set(item, column)

            if column in data.NUMERIC:
                return float(value)

            return value

        return key

    def on_heading(self, column):
        """Sort by that column, the other way round if it was already it."""
        if column == self.sorted_by:
            self.reverse = not self.reverse
        else:
            self.reverse = False

        self.sorted_by = column

        items = sorted(self.trv_rows.get_children(""),
                       key=self.get_key(column), reverse=self.reverse)

        # move() with an index is how a Treeview is reordered. Nothing is
        # deleted and nothing is inserted, so the selection survives.
        for position, item in enumerate(items):
            self.trv_rows.move(item, "", position)

        self.set_headings()

    def set_headings(self):
        """Put an arrow on the column that is sorted, and only on it."""
        for name in data.COLUMNS:
            text = name

            if name == self.sorted_by:
                text = name + ARROWS[self.reverse]

            self.trv_rows.heading(name, text=text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
