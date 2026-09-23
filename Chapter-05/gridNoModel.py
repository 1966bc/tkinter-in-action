#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  5.4 - What does a grid look like without a model?
# source:   wxPythonInAction-src/Chapter-05/gridNoModel.py
# -----------------------------------------------------------------------------
"""Nine rows of a baseball line-up, put in one cell at a time.

Tkinter has no grid widget. A ttk.Treeview shows rows and columns and is as
far as the standard library goes, which is far enough for this file and not
far enough for the rest of the chapter. See README.md.
"""
import tkinter as tk
from tkinter import ttk


# Position, first name, last name. The 1984 Chicago Cubs, as in the book.
LINE_UP = (("CF", "Bob", "Dernier"),
           ("2B", "Ryne", "Sandberg"),
           ("LF", "Gary", "Matthews"),
           ("1B", "Leon", "Durham"),
           ("RF", "Keith", "Moreland"),
           ("3B", "Ron", "Cey"),
           ("C", "Jody", "Davis"),
           ("SS", "Larry", "Bowa"),
           ("P", "Rick", "Sutcliffe"))

COLUMNS = (("#0", "Position", 80),
           ("first", "First", 110),
           ("last", "Last", 110))


class App(tk.Tk):
    """The line-up, shown and not editable."""

    def __init__(self):
        super().__init__()

        self.title("Grid")

        frm_main = ttk.Frame(self, padding=8)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.trv_line_up = ttk.Treeview(frm_main,
                                        columns=[name for name, _, _
                                                 in COLUMNS[1:]],
                                        height=len(LINE_UP))

        for name, heading, width in COLUMNS:
            self.trv_line_up.heading(name, text=heading, anchor=tk.W)
            self.trv_line_up.column(name, anchor=tk.W, width=width,
                                    stretch=False)

        scrollbar = ttk.Scrollbar(frm_main, orient=tk.VERTICAL,
                                  command=self.trv_line_up.yview)
        self.trv_line_up.config(yscrollcommand=scrollbar.set)

        self.trv_line_up.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.set_values()

    def set_values(self):
        """One row per player. The wx original writes one cell at a time,
        which is what the chapter is complaining about."""
        for position, first, last in LINE_UP:
            self.trv_line_up.insert("", tk.END, iid=position, text=position,
                                    values=(first, last))


if __name__ == "__main__":
    app = App()
    app.mainloop()
