#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.3 - What's a box sizer?
# source:   wxPythonInAction-src/Chapter-11/boxsizer.py
# -----------------------------------------------------------------------------
"""Four windows, one per question a wx.BoxSizer answers.

The first three are pack(). The fourth is grid(), because pack() has
expand, which is a boolean, and cannot be asked for two thirds. The
proportions do not come out the same either; see README.md.
"""
import tkinter as tk

from blockwindow import BlockWindow


LABELS = "one two three four".split()

WIDE = 200
NARROW = 75
TALL = 30


class BoxWindow(tk.Toplevel):
    """A window that lays its blocks out in one row or one column."""

    window_title = "none"

    def __init__(self, parent):
        super().__init__(parent)

        self.title(self.window_title)
        self.build()


class VerticalBox(BoxWindow):
    """A column of blocks, each stretched across the width."""

    window_title = "Vertical BoxSizer"

    def build(self):
        for label in LABELS:
            block = BlockWindow(self, label=label, width=WIDE, height=TALL)
            block.pack(side=tk.TOP, fill=tk.X)


class HorizontalBox(BoxWindow):
    """A row of blocks, each stretched down the height."""

    window_title = "Horizontal BoxSizer"

    def build(self):
        for label in LABELS:
            block = BlockWindow(self, label=label, width=NARROW, height=TALL)
            block.pack(side=tk.LEFT, fill=tk.Y)


class StretchableBox(BoxWindow):
    """A column where the last block takes all the free space."""

    window_title = "Stretchable BoxSizer"

    def build(self):
        for label in LABELS:
            block = BlockWindow(self, label=label, width=WIDE, height=TALL)
            block.pack(side=tk.TOP, fill=tk.X)

        greedy = BlockWindow(self, label="gets all free space",
                             width=WIDE, height=TALL)
        greedy.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class ProportionalBox(BoxWindow):
    """A column where two blocks share the free space one to two.

    Built with grid() and not pack(), because pack() cannot say two thirds.
    """

    window_title = "Proportional BoxSizer"

    def build(self):
        self.grid_columnconfigure(0, weight=1)

        for row, label in enumerate(LABELS):
            block = BlockWindow(self, label=label, width=WIDE, height=TALL)
            block.grid(row=row, column=0, sticky=tk.E + tk.W)

        shares = ((1, "gets 1/3 of the free space"),
                  (2, "gets 2/3 of the free space"))

        for index, share in enumerate(shares):
            weight, label = share
            row = len(LABELS) + index

            block = BlockWindow(self, label=label, width=WIDE, height=TALL)
            block.grid(row=row, column=0,
                       sticky=tk.N + tk.S + tk.E + tk.W)
            self.grid_rowconfigure(row, weight=weight)


class App(tk.Tk):
    """The four windows. The root itself is never shown."""

    def __init__(self):
        super().__init__()

        self.withdraw()

        for window in (VerticalBox, HorizontalBox,
                       StretchableBox, ProportionalBox):
            window(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
