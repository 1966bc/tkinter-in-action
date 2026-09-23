#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.3 - What's a grid bag sizer?
# source:   wxPythonInAction-src/Chapter-11/gridbagsizer.py
# -----------------------------------------------------------------------------
"""Blocks placed by coordinate, two of them spanning several cells.

pos and span are row, column, rowspan and columnspan. This is the
sizer Tkinter matches without arranging anything.
"""
import tkinter as tk

from blockwindow import BlockWindow


LABELS = "one two three four five six seven eight nine".split()

ROWS = 3
COLS = 3

GAP = 5

FILL = tk.N + tk.S + tk.E + tk.W


class App(tk.Tk):
    """A grid of nine blocks with two more spanning across it."""

    def __init__(self):
        super().__init__()

        self.title("GridBagSizer Test")

        for column in range(COLS):
            for row in range(ROWS):
                block = BlockWindow(self, label=LABELS[row * COLS + column])
                block.grid(row=row, column=column,
                           padx=(self.get_gap(column), 0),
                           pady=(self.get_gap(row), 0))

        # Down the right hand side, three rows tall.
        tall = BlockWindow(self, label="span 3 rows")
        tall.grid(row=0, column=COLS, rowspan=ROWS, sticky=FILL,
                  padx=(GAP, 0))

        # Along the bottom, the full width of the grid.
        wide = BlockWindow(self, label="span all columns")
        wide.grid(row=ROWS, column=0, columnspan=COLS + 1, sticky=FILL,
                  pady=(GAP, 0))

        # The last row and column take whatever the window gains.
        self.grid_columnconfigure(COLS, weight=1)
        self.grid_rowconfigure(ROWS, weight=1)

    def get_gap(self, position):
        """The gap for a row or column, which is nothing for the first one."""
        gap = GAP

        if position == 0:
            gap = 0

        return gap


if __name__ == "__main__":
    app = App()
    app.mainloop()
