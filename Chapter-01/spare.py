#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  1.3 - Extending the bare-minimum wxPython program
# source:   wxPythonInAction-src/Chapter-01/spare.py
# -----------------------------------------------------------------------------
"""A starting point for simple Tkinter programs.

bare.py with the three things a program that is going to grow will want: a
class of its own, a name for the window, and a main guard.
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
