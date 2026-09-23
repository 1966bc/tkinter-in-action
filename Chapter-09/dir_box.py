#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.3 - How do I ask for a directory?
# source:   wxPythonInAction-src/Chapter-09/dir_box.py
# -----------------------------------------------------------------------------
"""The directory chooser.

wx.DD_NEW_DIR_BUTTON asks for a button that makes a new folder. Tkinter has
no such option: whether the dialog offers one is the platform's business,
and on this machine it does.
"""
import tkinter as tk
from tkinter import filedialog


def main():
    """Ask for a directory and print it."""
    root = tk.Tk()
    root.withdraw()

    # Empty string on Cancel, not None. The dialogs of tkinter are not of
    # one mind about this, so each is checked for what it actually returns.
    path = filedialog.askdirectory(parent=root, title="Choose a directory:")

    if path:
        print(path)

    root.destroy()


if __name__ == "__main__":
    main()
