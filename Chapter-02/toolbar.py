#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  2.5 - How do I add a toolbar, a menu and a status bar?
# source:   wxPythonInAction-src/Chapter-02/toolbar.py
# -----------------------------------------------------------------------------
"""The three pieces of furniture a window is expected to have.

wx makes two of them with a method call each. Tkinter has a menu and nothing
else: a toolbar is a Frame of flat buttons and a status bar is a sunken
Label. Both are assembled here. See README.md.
"""
import os
import tkinter as tk
from tkinter import messagebox

import images


ICONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")

STATUS = "Copy in status bar"


class App(tk.Tk):
    """A window with a toolbar, a menu bar and a status bar."""

    def __init__(self):
        super().__init__()

        self.title("Toolbars")
        self.geometry("300x200")

        # A PhotoImage must outlive the call that made it, and a widget does
        # not keep it alive. Held here, they last as long as the window.
        self.images = {"new": images.get_new_image(),
                       "exit": tk.PhotoImage(file=os.path.join(ICONS,
                                                               "exit.png"))}

        self.set_menu()
        self.set_toolbar()
        self.set_status_bar()

    def set_menu(self):
        """File and Edit, as in the original."""
        mnu_bar = tk.Menu(self)

        mnu_file = tk.Menu(mnu_bar, tearoff=0)
        mnu_bar.add_cascade(label="File", underline=0, menu=mnu_file)

        mnu_edit = tk.Menu(mnu_bar, tearoff=0)
        mnu_bar.add_cascade(label="Edit", underline=0, menu=mnu_edit)

        mnu_edit.add_command(label="Copy", underline=0)
        mnu_edit.add_command(label="Cut", underline=1)
        mnu_edit.add_command(label="Paste", underline=0)
        mnu_edit.add_separator()
        mnu_edit.add_command(label="Options...", underline=0)

        self.config(menu=mnu_bar)

    def set_toolbar(self):
        """What wx gets from CreateToolBar(), made out of a Frame.

        Two buttons, for the two ways of getting a picture into one: the
        first from images.py, carried in the source as the book does it; the
        second read from icons/ at run time, which is the shorter way when
        the file can be relied on to be there.
        """
        frm_toolbar = tk.Frame(self, borderwidth=1, relief=tk.RAISED)

        btn_new = tk.Button(frm_toolbar, image=self.images["new"],
                            relief=tk.FLAT, command=self.on_about)
        btn_new.pack(side=tk.LEFT, padx=2, pady=2)

        btn_exit = tk.Button(frm_toolbar, image=self.images["exit"],
                             relief=tk.FLAT, command=self.on_close_me)
        btn_exit.pack(side=tk.LEFT, padx=2, pady=2)

        frm_toolbar.pack(side=tk.TOP, fill=tk.X)

    def set_status_bar(self):
        """What wx gets from CreateStatusBar(), made out of a Label."""
        lbl_status = tk.Label(self, text=STATUS, borderwidth=1,
                              relief=tk.SUNKEN, anchor=tk.W)
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

    def on_about(self):
        """The long help of the wx tool, which has nowhere else to go."""
        messagebox.showinfo("New", "Long help for 'New'", parent=self)

    def on_close_me(self):
        """Shut the window, and with it the program."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
