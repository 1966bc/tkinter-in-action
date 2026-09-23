#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.2 - How do sizers manage the size and alignment of their children?
# source:   wxPythonInAction-src/Chapter-11/resizegridsizer.py
# -----------------------------------------------------------------------------
"""Nine blocks, each told what to do with a cell bigger than itself.

Resize the window: at its natural size every cell fits its block and
none of this shows. The wx alignment flags are sticky. wx.SHAPED has
no equivalent and block "eight" is left alone; see README.md.
"""
import tkinter as tk

from blockwindow import BlockWindow


LABELS = "one two three four five six seven eight nine".split()

ROWS = 3
COLS = 3

GAP = 5

FILL = tk.N + tk.S + tk.E + tk.W

# The alignment flags of the wx original. Anything not named here keeps the
# wx default, which is the top left corner.
STICKY = {"one": tk.S + tk.W,
          "two": "",
          "four": tk.N + tk.E,
          "six": FILL,
          "seven": FILL}


class App(tk.Tk):
    """Nine blocks that each answer a resize differently."""

    def __init__(self):
        super().__init__()

        self.title("GridSizer Resizing")

        for index, label in enumerate(LABELS):
            row = index // COLS
            column = index % COLS

            pad_left = GAP
            if column == 0:
                pad_left = 0

            pad_top = GAP
            if row == 0:
                pad_top = 0

            block = BlockWindow(self, label=label)
            block.grid(row=row, column=column,
                       sticky=STICKY.get(label, tk.N + tk.W),
                       padx=(pad_left, 0), pady=(pad_top, 0))

        # Equal weights: the spare space is shared equally, which is what a
        # wx.GridSizer does with everything it is given. Without a weight a
        # row or column keeps its natural size and the window grows around it.
        for column in range(COLS):
            self.grid_columnconfigure(column, weight=1)

        for row in range(ROWS):
            self.grid_rowconfigure(row, weight=1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
