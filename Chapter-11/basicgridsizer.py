#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.2 - Basic sizers with the grid sizer
# source:   wxPythonInAction-src/Chapter-11/basicgridsizer.py
# -----------------------------------------------------------------------------
"""wx.GridSizer(rows=3, cols=3, hgap=5, vgap=5) as grid().

Nine blocks in a 3x3 grid, five pixels between the cells and nothing
around the outside.
"""
import tkinter as tk

from blockwindow import BlockWindow


LABELS = "one two three four five six seven eight nine".split()

COLS = 3

# The hgap and vgap of the wx original.
GAP = 5


class App(tk.Tk):
    """Nine blocks in a grid of three rows by three columns."""

    def __init__(self):
        super().__init__()

        self.title("Basic Grid Sizer")

        for index, label in enumerate(LABELS):
            row = index // COLS
            column = index % COLS

            # The gap goes on the left of every column but the first, and on
            # the top of every row but the first. What faces the outside of
            # the grid gets nothing.
            pad_left = GAP
            if column == 0:
                pad_left = 0

            pad_top = GAP
            if row == 0:
                pad_top = 0

            block = BlockWindow(self, label=label)
            block.grid(row=row, column=column,
                       padx=(pad_left, 0), pady=(pad_top, 0))


if __name__ == "__main__":
    app = App()
    app.mainloop()
