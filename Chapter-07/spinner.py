#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.9 - How do I make a spinner?
# source:   wxPythonInAction-src/Chapter-07/spinner.py
# -----------------------------------------------------------------------------
"""A number with a pair of arrows beside it.

wx.SpinCtrl is a number and refuses anything else. A ttk.Spinbox is an
Entry with arrows, and what is typed in it is whatever the keyboard sent,
so a range is a promise the arrows keep and the keyboard does not.
"""
import tkinter as tk
from tkinter import ttk


LOWEST = 1
HIGHEST = 100
START = 5


class App(tk.Tk):
    """One spinner, from one to a hundred, starting at five."""

    def __init__(self):
        super().__init__()

        self.title("Spinner Example")
        self.geometry("160x100")

        self.value = tk.IntVar(value=START)

        self.spn_value = ttk.Spinbox(self, from_=LOWEST, to=HIGHEST,
                                     textvariable=self.value, width=8)
        self.spn_value.place(x=30, y=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()
