#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.1 - How do I make a frame?
# source:   wxPythonInAction-src/Chapter-08/simple_frame.py
# -----------------------------------------------------------------------------
"""A window, with nothing asked of it and nothing in it.

Eight lines in wx, four here, and the difference is the whole of chapter 1:
a wx.App has to be made before a wx.Frame can exist, and tk.Tk() is both.
"""
import tkinter as tk


if __name__ == "__main__":
    app = tk.Tk()
    app.title("A Frame")
    app.geometry("200x100")
    app.mainloop()
