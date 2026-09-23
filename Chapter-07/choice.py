#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.4 - How do I make a drop-down list?
# source:   wxPythonInAction-src/Chapter-07/choice.py
# -----------------------------------------------------------------------------
"""A list to choose one thing from, closed until it is asked for.

wx.Choice is a drop-down that cannot be typed into. ttk.Combobox with
state="readonly" is the same thing; without that state it is the editable
one of combo_box.py.
"""
import tkinter as tk
from tkinter import ttk


SAMPLE = ("zero", "one", "two", "three", "four", "five",
          "six", "seven", "eight")


class App(tk.Tk):
    """A caption and a drop-down beside it."""

    def __init__(self):
        super().__init__()

        self.title("Choice Example")
        self.geometry("250x200")

        lbl_select = tk.Label(self, text="Select one:")
        lbl_select.place(x=15, y=20)

        self.cb_sample = ttk.Combobox(self, values=SAMPLE, state="readonly",
                                      width=12)
        self.cb_sample.place(x=85, y=18)


if __name__ == "__main__":
    app = App()
    app.mainloop()
