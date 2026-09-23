#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.10 - How do I make a text field?
# source:   wxPythonInAction-src/Chapter-07/text_ctrl.py
# -----------------------------------------------------------------------------
"""A field to type in, and one that hides what is typed.

TE_PASSWORD is show="*", and the only thing to say about it is that it
hides the characters from the screen and from nothing else: the text is in
the widget in the clear, and get() returns it.
"""
import tkinter as tk


BASIC = "I've entered some text!"
PASSWORD = "password"

GAP = 6


class App(tk.Tk):
    """Two labelled fields, one of them a password."""

    def __init__(self):
        super().__init__()

        self.title("Text Entry Example")
        self.geometry("300x100")

        lbl_basic = tk.Label(self, text="Basic Control:")
        lbl_basic.grid(row=0, column=0, padx=GAP, pady=GAP, sticky=tk.W)

        self.ent_basic = tk.Entry(self, width=22)
        self.ent_basic.insert(0, BASIC)
        self.ent_basic.icursor(0)
        self.ent_basic.grid(row=0, column=1, padx=GAP, pady=GAP)

        lbl_password = tk.Label(self, text="Password:")
        lbl_password.grid(row=1, column=0, padx=GAP, pady=GAP, sticky=tk.W)

        self.ent_password = tk.Entry(self, width=22, show="*")
        self.ent_password.insert(0, PASSWORD)
        self.ent_password.grid(row=1, column=1, padx=GAP, pady=GAP)


if __name__ == "__main__":
    app = App()
    app.mainloop()
