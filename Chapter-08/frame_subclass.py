#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.1 - How do I subclass a frame?
# source:   wxPythonInAction-src/Chapter-08/frame_subclass.py
# -----------------------------------------------------------------------------
"""A window of one's own, with a button that closes it.

The same ground as Chapter-02/insert.py, and here because the book puts it
here. The point is the difference between closing and being closed.
"""
import tkinter as tk


class App(tk.Tk):
    """A window with one button in it."""

    def __init__(self):
        super().__init__()

        self.title("Frame Subclass")
        self.geometry("300x100")

        # EVT_CLOSE in the original: what the title bar asks for, and the
        # one place where the answer can be no.
        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        btn_close = tk.Button(self, text="Close Me", command=self.on_close_me)
        btn_close.place(x=15, y=15)

    def on_close_me(self):
        """The button. wx calls Close(), which raises EVT_CLOSE and ends up
        at on_close_window; a Tk destroy() goes straight past it, so the
        handler is called by name to keep the two the same."""
        self.on_close_window()

    def on_close_window(self):
        """The title bar, and now the button too."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
