#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.3 - How do I ask for a file?
# source:   wxPythonInAction-src/Chapter-09/file_box.py
# -----------------------------------------------------------------------------
"""The file chooser, and the one difference worth the file.

A wx wildcard is one string with pipes in it, alternating description and
pattern. A Tkinter filetypes is a list of pairs, and a pair may hold
several patterns. The Tk form is the one that can be read at a glance.
"""
import os
import tkinter as tk
from tkinter import filedialog


# The wx original: "Python source (*.py)|*.py|Compiled Python (*.pyc)|..."
FILETYPES = (("Python source", "*.py"),
             ("Compiled Python", "*.pyc"),
             ("All files", "*.*"))


def main():
    """Ask for a file and print its path."""
    root = tk.Tk()
    root.withdraw()

    path = filedialog.askopenfilename(parent=root, title="Choose a file",
                                      initialdir=os.getcwd(),
                                      filetypes=FILETYPES)

    if path:
        print(path)

    root.destroy()


if __name__ == "__main__":
    main()
