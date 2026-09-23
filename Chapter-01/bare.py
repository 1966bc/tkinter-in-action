#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  1.2 - Creating the bare-minimum wxPython program
# source:   wxPythonInAction-src/Chapter-01/bare.py
# -----------------------------------------------------------------------------
"""The smallest program that puts a window on the screen.

There is no class and nothing is subclassed, because in Tkinter there is
nothing yet that needs to be. See README.md.
"""
import tkinter as tk


root = tk.Tk()
root.title("Bare")
root.mainloop()
