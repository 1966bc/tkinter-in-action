#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.1 - How do I create a menu?
# source:   wxPythonInAction-src/Chapter-10/create_just_menu.py
# -----------------------------------------------------------------------------
"""A menu that belongs to nothing yet.

wx.Menu can be made on its own and attached later. A tk.Menu is the same,
and the same class is used for the bar, for a menu on it, for a sub-menu
and for a pop-up. There is one menu widget in Tkinter and four uses.
"""
import tkinter as tk


class App(tk.Tk):
    """A window whose menu exists and is not on the bar."""

    def __init__(self):
        super().__init__()

        self.title("Just a Menu")
        self.geometry("320x120")

        # tearoff=0 everywhere in this book. Without it Tk puts a dashed
        # line at the top of every menu which, when clicked, tears the
        # menu off into a window of its own. It is a Motif habit from
        # 1990 and nobody expects it now.
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Simple menu item")
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.destroy)

        lbl_hint = tk.Label(self, text="The menu exists. It is not on the\n"
                                       "menu bar, so nothing shows it.\n\n"
                                       "create_simple_menu.py puts it there.")
        lbl_hint.pack(expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
