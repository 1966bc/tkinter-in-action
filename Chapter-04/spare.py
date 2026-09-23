#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  4.4 - How do I use PyWrap?
# source:   wxPythonInAction-src/Chapter-04/spare.py
# -----------------------------------------------------------------------------
"""A starting point for simple Tkinter programs, and something to wrap.

The same file as in chapter 1. It is here because PyWrap needs a program to
run, and this is the smallest one that has a window class to be found.
"""
import tkinter as tk


class App(tk.Tk):
    """The application, which is also the window. Start here."""

    def __init__(self):
        super().__init__()

        self.title("Spare")
        self.geometry("400x200")

        frm_main = tk.Frame(self)
        frm_main.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
