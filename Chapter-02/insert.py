#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  2.4 - How do I close a window?
# source:   wxPythonInAction-src/Chapter-02/insert.py
# -----------------------------------------------------------------------------
"""A window with a button that closes it, and a close button that asks first.

wx separates Close() from Destroy(): the first sends an event that something
may refuse, the second takes the window away. Tkinter has only the second.
See README.md.
"""
import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    """One button, in the middle, that shuts the window."""

    def __init__(self):
        super().__init__()

        self.title("Frame With Button")
        self.geometry("300x100")

        # The wx original binds EVT_CLOSE, which is what the close button of
        # the title bar raises. Here it is a message from the window
        # manager, and this is where it is caught.
        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        btn_close = tk.Button(self, text="Close", command=self.on_close_me)
        btn_close.place(x=125, y=10, width=50, height=50)

    def on_close_me(self):
        """The button. It closes without asking, as the original does."""
        self.destroy()

    def on_close_window(self):
        """The title bar. This is the place wx gives you with EVT_CLOSE:
        the one chance to refuse, or to ask whether work should be saved."""
        if messagebox.askokcancel("Close", "Close this window?", parent=self):
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
