#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.2 - Can I specify a minimum size for my sizer or its children?
# source:   wxPythonInAction-src/Chapter-11/mingridsizer.py
# -----------------------------------------------------------------------------
"""One block is told to be 150x50, and all nine cells grow with it.

The cell size is stated with minsize. See README.md for why not with
uniform, which is the obvious answer and the wrong one.
"""
import tkinter as tk

from blockwindow import BlockWindow, BLOCK_WIDTH, BLOCK_HEIGHT


LABELS = "one two three four five six seven eight nine".split()

ROWS = 3
COLS = 3

GAP = 5

# The block that is given a minimum size, and the size it is given.
BIG_LABEL = "five"
BIG_WIDTH = 150
BIG_HEIGHT = 50


class App(tk.Tk):
    """Nine blocks in a grid whose cells are all as big as the biggest."""

    def __init__(self):
        super().__init__()

        self.title("GridSizer Test")

        for index, label in enumerate(LABELS):
            width = BLOCK_WIDTH
            height = BLOCK_HEIGHT

            if label == BIG_LABEL:
                width = BIG_WIDTH
                height = BIG_HEIGHT

            row = index // COLS
            column = index % COLS

            pad_left = GAP
            if column == 0:
                pad_left = 0

            pad_top = GAP
            if row == 0:
                pad_top = 0

            block = BlockWindow(self, label=label, width=width, height=height)
            block.grid(row=row, column=column, sticky=tk.NW,
                       padx=(pad_left, 0), pady=(pad_top, 0))

        # Every cell as big as the biggest block, plus the gap for the cells
        # that have a neighbour on their left or above them.
        for column in range(COLS):
            minsize = BIG_WIDTH
            if column > 0:
                minsize = BIG_WIDTH + GAP
            self.grid_columnconfigure(column, minsize=minsize)

        for row in range(ROWS):
            minsize = BIG_HEIGHT
            if row > 0:
                minsize = BIG_HEIGHT + GAP
            self.grid_rowconfigure(row, minsize=minsize)


if __name__ == "__main__":
    app = App()
    app.mainloop()
