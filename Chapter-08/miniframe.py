#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.2 - What other kinds of frame are there?
# source:   wxPythonInAction-src/Chapter-08/miniframe.py
# -----------------------------------------------------------------------------
"""A small window that floats over another one: a tool palette.

wx.MiniFrame is a frame with a thin title bar that stays above its parent
and keeps out of the taskbar. Tkinter has no such class, and two of the
three halves of it are one line each. See README.md.
"""
import tkinter as tk


class MiniFrame(tk.Toplevel):
    """What a wx.MiniFrame is, in the pieces Tkinter has."""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Mini Frame")
        self.geometry("300x100")

        # transient() is the half that matters: it stays above its parent,
        # is iconified with it, and the window manager usually keeps it out
        # of the taskbar. The thin title bar is the half that is missing -
        # that is the window manager's to draw and Tk does not ask for it.
        self.transient(parent)

        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        btn_close = tk.Button(self, text="Close Me", command=self.on_close_me)
        btn_close.place(x=15, y=15)

    def on_close_me(self):
        """The button."""
        self.on_close_window()

    def on_close_window(self):
        """The title bar."""
        self.destroy()


class App(tk.Tk):
    """A window, with a mini frame floating over it."""

    def __init__(self):
        super().__init__()

        self.title("Mini Frame Parent")
        self.geometry("400x300")

        lbl_hint = tk.Label(self, text="The mini frame floats over this one.")
        lbl_hint.pack(pady=20)

        self.mini = MiniFrame(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
