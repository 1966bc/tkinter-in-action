#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.2 - How do I ask for a line of text?
# source:   wxPythonInAction-src/Chapter-09/text_box.py
# -----------------------------------------------------------------------------
"""One line of text, with a default already in it.

wx.TextEntryDialog and simpledialog.askstring, and the difference is only
that Tkinter hands back None for Cancel instead of a code to compare.
"""
import tkinter as tk
from tkinter import simpledialog


def main():
    """Ask for a line and print it."""
    root = tk.Tk()
    root.withdraw()

    answer = simpledialog.askstring(
        "Text Entry", "What kind of text would you like to enter?",
        initialvalue="Default Value", parent=root)

    if answer is not None:
        print("You entered: {}".format(answer))

    root.destroy()


if __name__ == "__main__":
    main()
