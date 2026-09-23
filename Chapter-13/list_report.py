#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  13.1 - What is report mode?
# source:   wxPythonInAction-src/Chapter-13/list_report.py
# -----------------------------------------------------------------------------
"""Rows and columns, shown and not editable.

wx.ListCtrl in LC_REPORT mode is a table of text with headings.
ttk.Treeview does the same job and is called a tree because it can also
do chapter 15. It is not a grid: nothing in it can be typed into. See
README.md.
"""
import tkinter as tk
from tkinter import ttk

import data


class App(tk.Tk):
    """A window showing the rows."""

    def __init__(self):
        super().__init__()

        self.title("Treeview in report mode")
        self.geometry("640x360")

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        # show="headings" hides the first column, the one a Treeview
        # keeps for the tree itself. Without it every row starts with an
        # empty space where an expander would be, which is the commonest
        # thing wrong with a Tkinter table.
        self.trv_rows = ttk.Treeview(frm_main, columns=data.COLUMNS,
                                     show="headings", selectmode="browse")

        for name in data.COLUMNS:
            self.trv_rows.heading(name, text=name, anchor=tk.W)
            self.trv_rows.column(name, anchor=tk.W, width=140, stretch=True)

        scrollbar = ttk.Scrollbar(frm_main, orient=tk.VERTICAL,
                                  command=self.trv_rows.yview)
        self.trv_rows.config(yscrollcommand=scrollbar.set)

        self.trv_rows.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.set_rows()

    def set_rows(self):
        """One insert per row.

        wx inserts the first column and then sets each of the others, one
        call per cell. A Treeview takes the whole row at once, and there
        is no cell to address on its own - which is the same limitation
        seen from the other side.
        """
        for row in data.ROWS:
            self.trv_rows.insert("", tk.END, values=row)


if __name__ == "__main__":
    app = App()
    app.mainloop()
