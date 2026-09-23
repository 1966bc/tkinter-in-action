#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.2 - How do I show a message?
# source:   wxPythonInAction-src/Chapter-09/message_box.py
# -----------------------------------------------------------------------------
"""A question with a yes and a no in it.

wx offers the dialog as a class and again as a function. Tkinter has only
the function, which is the one everybody used anyway.
"""
import tkinter as tk
from tkinter import messagebox


def main():
    """Ask twice, as the original does."""
    root = tk.Tk()
    root.withdraw()

    # askyesno is the whole of wx.YES_NO | wx.ICON_QUESTION: the buttons
    # and the icon are chosen together, by which function is called, and
    # cannot be mixed. askokcancel, askretrycancel and askyesnocancel are
    # the others.
    if messagebox.askyesno("A Message Box", "Is this explanation OK?",
                           parent=root):
        print("yes")
    else:
        print("no")

    if messagebox.askyesno("Via Function", "Is this way easier?",
                           parent=root):
        print("yes")
    else:
        print("no")

    root.destroy()


if __name__ == "__main__":
    main()
