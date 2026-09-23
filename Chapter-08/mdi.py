#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.5 - How do I make an MDI application?
# source:   wxPythonInAction-src/Chapter-08/mdi.py
# -----------------------------------------------------------------------------
"""Many documents in one window - which Tkinter does not do.

wx.MDIParentFrame holds wx.MDIChildFrames: real windows, with title bars,
that live inside another window and can be tiled, cascaded and minimised
there. Tkinter has nothing of the sort and no way to build one.

What one does instead is here: a ttk.Notebook. It is the arrangement that
replaced MDI everywhere in the twenty years since the book, and it is
better for most of what MDI was used for and worse for one thing. See
README.md.
"""
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    """A window whose documents are tabs."""

    def __init__(self):
        super().__init__()

        self.title("MDI Parent")
        self.geometry("600x400")

        self.count = 0

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.set_menu_bar()

    def set_menu_bar(self):
        """New Window and Exit, as in the original."""
        mnu_bar = tk.Menu(self)
        mnu_file = tk.Menu(mnu_bar, tearoff=0)

        mnu_file.add_command(label="New Window", underline=0,
                             command=self.on_new_window)
        mnu_file.add_command(label="Exit", underline=1, command=self.destroy)

        mnu_bar.add_cascade(label="File", underline=0, menu=mnu_file)
        self.config(menu=mnu_bar)

    def on_new_window(self):
        """A new child. In wx it would be a window inside the window."""
        self.count = self.count + 1

        child = tk.Frame(self.notebook)
        lbl_child = tk.Label(child, text="Child Window {}".format(self.count))
        lbl_child.pack(expand=True)

        self.notebook.add(child, text="Child {}".format(self.count))
        self.notebook.select(child)


if __name__ == "__main__":
    app = App()
    app.mainloop()
