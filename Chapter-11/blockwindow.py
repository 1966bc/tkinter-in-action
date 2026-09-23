#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.2 - Basic sizers with the grid sizer
# source:   wxPythonInAction-src/Chapter-11/blockwindow.py
# -----------------------------------------------------------------------------
"""A labelled block, so that a sizer example has something to lay out.

A Frame with a Label placed at its centre. The wx original paints its
own text, because a wx.Panel has none.
"""
import tkinter as tk


# The wx original asks for 100x25 pixels. A Label measures its width and
# height in characters, not pixels, so the size is put on the Frame and the
# Label is placed inside it: place() never asks the parent to grow, which is
# what keeps the block at the size it was given.
BLOCK_WIDTH = 100
BLOCK_HEIGHT = 25


class BlockWindow(tk.Frame):
    """A white block with a raised border and a centred label."""

    def __init__(self, parent, label="",
                 width=BLOCK_WIDTH, height=BLOCK_HEIGHT):
        super().__init__(parent, width=width, height=height,
                         relief=tk.RAISED, borderwidth=2, background="white")

        self.label = label

        lbl_block = tk.Label(self, text=label, background="white")
        lbl_block.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
