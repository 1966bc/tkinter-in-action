#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.3 - What's a static box sizer?
# source:   wxPythonInAction-src/Chapter-11/staticboxsizer.py
# -----------------------------------------------------------------------------
"""Three labelled boxes side by side, three blocks in each.

A ttk.LabelFrame is a real container and the blocks are its children.
A wx.StaticBox is drawn behind blocks that belong to the panel.
"""
import tkinter as tk
from tkinter import ttk

from blockwindow import BlockWindow


LABELS = "one two three four five six seven eight nine".split()

PER_BOX = 3

# wx.ALL with a border of 10 around each box, and of 2 around each block.
BOX_BORDER = 10
BLOCK_BORDER = 2


class App(tk.Tk):
    """Three labelled boxes in a row, three blocks in each."""

    def __init__(self):
        super().__init__()

        self.title("StaticBoxSizer Test")

        for index in range(len(LABELS) // PER_BOX):
            start = index * PER_BOX
            frm_box = ttk.LabelFrame(self, text="Box {}".format(index + 1))
            frm_box.pack(side=tk.LEFT, padx=BOX_BORDER, pady=BOX_BORDER)

            for label in LABELS[start:start + PER_BOX]:
                block = BlockWindow(frm_box, label=label)
                block.pack(padx=BLOCK_BORDER, pady=BLOCK_BORDER)


if __name__ == "__main__":
    app = App()
    app.mainloop()
