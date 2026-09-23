#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.2 - How do you add or remove children from a sizer?
# source:   wxPythonInAction-src/Chapter-11/prependgridsizer.py
# -----------------------------------------------------------------------------
"""The nine blocks laid out backwards, by Prepend() instead of Add().

Nothing to translate: a wx sizer keeps an ordered list, grid() takes a
row and a column, so Prepend() becomes arithmetic on the index.
"""
import tkinter as tk

from blockwindow import BlockWindow


LABELS = "one two three four five six seven eight nine".split()

COLS = 3

GAP = 5


class App(tk.Tk):
    """The nine blocks laid out from the last cell backwards."""

    def __init__(self):
        super().__init__()

        self.title("Prepend Grid Sizer")

        for index, label in enumerate(LABELS):
            # What Prepend() does to the list, done to the index: the first
            # block goes in the last cell.
            position = len(LABELS) - 1 - index

            row = position // COLS
            column = position % COLS

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
