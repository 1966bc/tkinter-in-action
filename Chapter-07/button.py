#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.2 - How do I make a button?
# source:   wxPythonInAction-src/Chapter-07/button.py
# -----------------------------------------------------------------------------
"""A button that changes its own label when pressed.

wx.Button and tk.Button, with one difference worth the file: wx has
SetDefault(), and Tk has an appearance but no behaviour to go with it.
"""
import tkinter as tk


class App(tk.Tk):
    """One button, which is the default one."""

    def __init__(self):
        super().__init__()

        self.title("Button Example")
        self.geometry("300x100")

        self.btn_hello = tk.Button(self, text="Hello", default=tk.ACTIVE,
                                   command=self.on_click)
        self.btn_hello.place(x=50, y=20)

        # SetDefault() in wx does two things: it draws the button as the
        # default one and it makes Return press it. Tk's default=ACTIVE
        # only draws it, so the second half is asked for here.
        self.bind("<Return>", lambda event: self.btn_hello.invoke())

        self.btn_hello.focus_set()

    def on_click(self):
        """Say that it happened."""
        self.btn_hello.config(text="Clicked")


if __name__ == "__main__":
    app = App()
    app.mainloop()
