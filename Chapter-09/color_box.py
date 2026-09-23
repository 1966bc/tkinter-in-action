#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.3 - How do I ask for a colour?
# source:   wxPythonInAction-src/Chapter-09/color_box.py
# -----------------------------------------------------------------------------
"""The colour chooser.

wx builds a dialog, shows it, asks whether OK was pressed and then asks it
what colour. Tkinter asks one question and gets one answer, or None if the
person changed their mind.
"""
import tkinter as tk
from tkinter import colorchooser


def main():
    """Ask for a colour and say which one it was."""
    root = tk.Tk()
    root.withdraw()

    # Two things back: the colour as numbers, and the same as the "#rrggbb"
    # that every Tk widget wants. Both are None if Cancel was pressed.
    rgb, name = colorchooser.askcolor(parent=root)

    if name is not None:
        print("You selected: {} {}".format(rgb, name))

    root.destroy()


if __name__ == "__main__":
    main()
