#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  1.6 - Why choose wxPython?
# source:   wxPythonInAction-src/Chapter-01/python_compare.py
# -----------------------------------------------------------------------------
"""A window with a menu, a status bar and an about box.

The example the book uses to show what a real toolkit gives you. Tkinter
gives two of the three: there is no status bar widget, and a sunken Label is
how one is made. See README.md.
"""
import tkinter as tk
from tkinter import messagebox


ABOUT_TITLE = "About Hello World"
ABOUT_TEXT = "This is a wxPython Hello world sample"

WELCOME = "Welcome to wxPython!"


class App(tk.Tk):
    """Hello World, with the furniture a window is expected to have."""

    def __init__(self):
        super().__init__()

        self.title("Hello World")
        self.geometry("450x340+50+60")

        # The close button is not an event one can listen for: it is a
        # message from the window manager, and this is where it is caught.
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        self.set_menu()
        self.set_status_bar()

    def set_menu(self):
        """A File menu with About and Exit."""
        mnu_bar = tk.Menu(self)
        mnu_file = tk.Menu(mnu_bar, tearoff=0)

        mnu_bar.add_cascade(label="File", underline=0, menu=mnu_file)
        mnu_file.add_command(label="About...", underline=0,
                             command=self.on_about)
        mnu_file.add_separator()
        mnu_file.add_command(label="Exit", underline=1, command=self.on_quit)

        self.config(menu=mnu_bar)

    def set_status_bar(self):
        """What wx gets from CreateStatusBar(), made out of a Label."""
        lbl_status = tk.Label(self, text=WELCOME, borderwidth=1,
                              relief=tk.SUNKEN, anchor=tk.W)
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def on_about(self):
        """Say what this is."""
        messagebox.showinfo(ABOUT_TITLE, ABOUT_TEXT, parent=self)

    def on_quit(self):
        """Close the window, and with it the program."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
