#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.2 - How do sizers manage the border around each child?
# source:   wxPythonInAction-src/Chapter-11/bordergridsizer.py
# -----------------------------------------------------------------------------
"""Each block asks for 10 pixels of border on some of its sides.

wx chooses the sides with flags and gives one number for all of them.
padx and pady each take a (left, right) pair and need no flags.
"""
import tkinter as tk

from blockwindow import BlockWindow, BLOCK_WIDTH, BLOCK_HEIGHT


LABELS = "one two three four five six seven eight nine".split()

ROWS = 3
COLS = 3

GAP = 5

# The border of the wx original, and where each block asks for it.
BORDER = 10

ALL_SIDES = {"left", "right", "top", "bottom"}

BORDERS = {"one": {"bottom"},
           "two": ALL_SIDES,
           "three": {"top"},
           "four": {"left"},
           "five": ALL_SIDES,
           "six": {"right"},
           "seven": {"top", "bottom"},
           "eight": ALL_SIDES,
           "nine": {"left", "right"}}

# Every cell is as big as the widest child with its border on both sides,
# which is what a wx.GridSizer does by itself.
CELL_WIDTH = BLOCK_WIDTH + 2 * BORDER
CELL_HEIGHT = BLOCK_HEIGHT + 2 * BORDER


def get_border(sides, side):
    """The border in pixels for one side of a block, 0 if it asked for none."""
    border = 0

    if side in sides:
        border = BORDER

    return border


class App(tk.Tk):
    """Nine blocks, each with a border on the sides it asked for."""

    def __init__(self):
        super().__init__()

        self.title("GridSizer Borders")

        for index, label in enumerate(LABELS):
            row = index // COLS
            column = index % COLS

            sides = BORDERS.get(label, set())

            # The gap towards the neighbour, then the block's own border on
            # top of it. Towards the outside of the grid there is no gap, so
            # only the border is left.
            pad_left = get_border(sides, "left")
            if column > 0:
                pad_left = pad_left + GAP

            pad_top = get_border(sides, "top")
            if row > 0:
                pad_top = pad_top + GAP

            block = BlockWindow(self, label=label)
            block.grid(row=row, column=column, sticky=tk.NW,
                       padx=(pad_left, get_border(sides, "right")),
                       pady=(pad_top, get_border(sides, "bottom")))

        for column in range(COLS):
            minsize = CELL_WIDTH
            if column > 0:
                minsize = CELL_WIDTH + GAP
            self.grid_columnconfigure(column, minsize=minsize)

        for row in range(ROWS):
            minsize = CELL_HEIGHT
            if row > 0:
                minsize = CELL_HEIGHT + GAP
            self.grid_rowconfigure(row, minsize=minsize)


if __name__ == "__main__":
    app = App()
    app.mainloop()
