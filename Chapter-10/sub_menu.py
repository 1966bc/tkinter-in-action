#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.2 - How do I make a sub-menu?
# source:   wxPythonInAction-src/Chapter-10/sub_menu.py
# -----------------------------------------------------------------------------
"""A menu inside a menu.

Nothing new: a sub-menu is a tk.Menu added to another with add_cascade,
which is exactly how a menu is put on the bar. The bar, the menu and the
sub-menu are the same class three times.
"""
import tkinter as tk


class App(tk.Tk):
    """A window with a menu that has a menu in it."""

    def __init__(self):
        super().__init__()

        self.title("Sub-menu Example")
        self.geometry("320x120")

        mnu_bar = tk.Menu(self, tearoff=0)
        mnu_main = tk.Menu(mnu_bar, tearoff=0)

        mnu_main.add_command(label="Simple menu item",
                             command=lambda: self.on_chosen("Simple"))

        mnu_sub = tk.Menu(mnu_main, tearoff=0)
        mnu_sub.add_command(label="Sub-item 1",
                            command=lambda: self.on_chosen("Sub-item 1"))
        mnu_sub.add_command(label="Sub-item 2",
                            command=lambda: self.on_chosen("Sub-item 2"))

        mnu_main.add_cascade(label="Sub-menu", menu=mnu_sub)
        mnu_main.add_separator()
        mnu_main.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Menu", underline=0, menu=mnu_main)
        self.config(menu=mnu_bar)

        self.lbl_said = tk.Label(self, text="Nothing chosen yet.")
        self.lbl_said.pack(expand=True)

    def on_chosen(self, what):
        """Say which one it was."""
        self.lbl_said.config(text="{} was chosen.".format(what))


if __name__ == "__main__":
    app = App()
    app.mainloop()
