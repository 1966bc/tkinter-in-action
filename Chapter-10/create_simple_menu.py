#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.1 - How do I put a menu on the menu bar?
# source:   wxPythonInAction-src/Chapter-10/create_simple_menu.py
# -----------------------------------------------------------------------------
"""A menu bar with one menu on it, and an item that does something.

wx has wx.MenuBar and wx.Menu, two classes. Tkinter has tk.Menu, and the
bar is a menu whose items happen to cascade. config(menu=...) is what
makes one a bar - a menu given to a window that way is drawn along the
top, and the same object given to tk_popup would appear at the pointer.
"""
import tkinter as tk


class App(tk.Tk):
    """A window with a menu bar."""

    def __init__(self):
        super().__init__()

        self.title("Simple Menu")
        self.geometry("320x120")

        mnu_bar = tk.Menu(self, tearoff=0)

        mnu_simple = tk.Menu(mnu_bar, tearoff=0)
        mnu_simple.add_command(label="Simple menu item",
                               command=self.on_simple)
        mnu_simple.add_separator()
        mnu_simple.add_command(label="Exit", command=self.destroy)

        # underline is the ampersand of "E&xit": which letter is the one
        # Alt reaches. wx counts it in the string, Tk counts it as a
        # position, which means a translated label does not silently move
        # the underline to the wrong letter.
        mnu_bar.add_cascade(label="Simple Menu", underline=0,
                            menu=mnu_simple)

        self.config(menu=mnu_bar)

        self.lbl_said = tk.Label(self, text="Nothing chosen yet.")
        self.lbl_said.pack(expand=True)

    def on_simple(self):
        """Say that it was chosen."""
        self.lbl_said.config(text="Simple menu item was chosen.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
