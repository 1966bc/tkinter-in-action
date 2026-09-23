#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  3.2 - How do I bind an event to a menu item?
# source:   wxPythonInAction-src/Chapter-03/menu_event.py
# -----------------------------------------------------------------------------
"""A menu with one item, and the item does something.

wx binds the frame to EVT_MENU for that item. A Tk menu item is given its
command when it is made, and there is no event object at all.
"""
import tkinter as tk


class App(tk.Tk):
    """A window whose only furniture is File / Exit."""

    def __init__(self):
        super().__init__()

        self.title("Menus")
        self.geometry("300x200")

        mnu_bar = tk.Menu(self)
        mnu_file = tk.Menu(mnu_bar, tearoff=0)

        mnu_bar.add_cascade(label="File", underline=0, menu=mnu_file)
        mnu_file.add_command(label="Exit...", underline=1,
                             command=self.on_close_me)

        self.config(menu=mnu_bar)

    def on_close_me(self):
        """No event argument: nothing was asked and nothing is passed."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
