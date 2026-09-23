#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.3 - What's a flex grid sizer?
# source:   wxPythonInAction-src/Chapter-11/resizeflexgridsizer.py
# -----------------------------------------------------------------------------
"""The flex grid told which rows and columns may grow, and by how much.

AddGrowableCol(1, 2) is grid_columnconfigure(1, weight=2). The same
numbers and the same arithmetic.
"""
import tkinter as tk

from blockwindow import BlockWindow, BLOCK_WIDTH, BLOCK_HEIGHT


LABELS = "one two three four five six seven eight nine".split()

COLS = 3

GAP = 5

BIG_LABEL = "five"
BIG_WIDTH = 150
BIG_HEIGHT = 50

# The shares of AddGrowableCol and AddGrowableRow, in order.
COLUMN_WEIGHTS = (1, 2, 1)
ROW_WEIGHTS = (1, 5, 1)


class App(tk.Tk):
    """A flex grid whose middle row and column take the larger share."""

    def __init__(self):
        super().__init__()

        self.title("Resizing Flex Grid Sizer")

        for index, label in enumerate(LABELS):
            row = index // COLS
            column = index % COLS

            pad_left = GAP
            if column == 0:
                pad_left = 0

            pad_top = GAP
            if row == 0:
                pad_top = 0

            width = BLOCK_WIDTH
            height = BLOCK_HEIGHT

            if label == BIG_LABEL:
                width = BIG_WIDTH
                height = BIG_HEIGHT

            block = BlockWindow(self, label=label, width=width, height=height)
            block.grid(row=row, column=column, sticky=tk.NW,
                       padx=(pad_left, 0), pady=(pad_top, 0))

        for column, weight in enumerate(COLUMN_WEIGHTS):
            self.grid_columnconfigure(column, weight=weight)

        for row, weight in enumerate(ROW_WEIGHTS):
            self.grid_rowconfigure(row, weight=weight)


if __name__ == "__main__":
    app = App()
    app.mainloop()
