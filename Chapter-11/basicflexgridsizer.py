#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.3 - What's a flex grid sizer?
# source:   wxPythonInAction-src/Chapter-11/basicflexgridsizer.py
# -----------------------------------------------------------------------------
"""A wx.FlexGridSizer: only the row and column holding the big block grow.

Which is what grid() does with nothing asked for. The flex sizer is
Tkinter's ordinary behaviour; it was wx.GridSizer that needed work.
"""
import tkinter as tk

from blockwindow import BlockWindow, BLOCK_WIDTH, BLOCK_HEIGHT


LABELS = "one two three four five six seven eight nine".split()

COLS = 3

GAP = 5

BIG_LABEL = "five"
BIG_WIDTH = 150
BIG_HEIGHT = 50


class App(tk.Tk):
    """Nine blocks in a grid where only the middle row and column grow."""

    def __init__(self):
        super().__init__()

        self.title("FlexGridSizer")

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
