#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.4 - How do I split a window?
# source:   wxPythonInAction-src/Chapter-08/splitter.py
# -----------------------------------------------------------------------------
"""Two panes with a bar between them that can be dragged.

wx.SplitterWindow holds two windows and splits horizontally or vertically.
ttk.PanedWindow holds as many as it is given and is told its orientation
when it is made, so switching between the two means making another one.
"""
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk


FIRST = "pink"
SECOND = "sky blue"


class App(tk.Tk):
    """A window whose two panes can be split either way, or not at all."""

    def __init__(self):
        super().__init__()

        self.title("Splitter Example")
        self.geometry("500x400")

        self.minimum = 0
        self.position = 0

        self.paned = None
        self.frm_first = None
        self.frm_second = None

        self.set_menu_bar()
        self.set_panes(tk.HORIZONTAL)

    def set_menu_bar(self):
        """One menu, as in the original."""
        mnu_bar = tk.Menu(self)
        mnu_file = tk.Menu(mnu_bar, tearoff=0)

        mnu_file.add_command(label="Split horizontally",
                             command=self.on_split_h)
        mnu_file.add_command(label="Split vertically", command=self.on_split_v)
        mnu_file.add_command(label="Unsplit", command=self.on_unsplit)
        mnu_file.add_separator()
        mnu_file.add_command(label="Set initial sash position",
                             command=self.on_set_position)
        mnu_file.add_command(label="Set minimum pane size",
                             command=self.on_set_minimum)
        mnu_file.add_separator()
        mnu_file.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="File", underline=0, menu=mnu_file)
        self.config(menu=mnu_bar)

    def set_panes(self, orientation, split=True):
        """Build the panes, in the orientation asked for.

        A ttk.PanedWindow is given its orientation when it is made and
        cannot be turned afterwards, which is where wx's Split and
        SplitHorizontally on one object become a new object here.
        """
        if self.paned is not None:
            self.paned.destroy()

        self.paned = ttk.PanedWindow(self, orient=orientation)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.frm_first = tk.Frame(self.paned, background=FIRST,
                                  relief=tk.SUNKEN, borderwidth=2)
        self.paned.add(self.frm_first, weight=1)

        self.frm_second = tk.Frame(self.paned, background=SECOND,
                                   relief=tk.SUNKEN, borderwidth=2)

        if split:
            self.paned.add(self.frm_second, weight=1)

            if self.position:
                self.update_idletasks()
                self.paned.sashpos(0, self.position)

    def on_split_h(self):
        """Two panes, one above the other."""
        self.set_panes(tk.VERTICAL)

    def on_split_v(self):
        """Two panes, side by side."""
        self.set_panes(tk.HORIZONTAL)

    def on_unsplit(self):
        """One pane. wx calls this Unsplit; here the second is not added."""
        self.set_panes(tk.HORIZONTAL, split=False)

    def on_set_position(self):
        """Where the bar starts, in pixels from the near edge."""
        answer = simpledialog.askinteger("Sash", "Initial sash position",
                                         initialvalue=self.position,
                                         parent=self)

        if answer is not None:
            self.position = answer
            self.update_idletasks()
            self.paned.sashpos(0, self.position)

    def on_set_minimum(self):
        """How small a pane may be dragged.

        wx has SetMinimumPaneSize on the splitter. In Tk it is not the
        pane's business but the child's: a Frame will not be made smaller
        than the size it asks for, so the minimum is set there.
        """
        answer = simpledialog.askinteger("Minimum", "Minimum pane size",
                                         initialvalue=self.minimum,
                                         parent=self)

        if answer is not None:
            self.minimum = answer
            self.frm_first.config(width=answer, height=answer)
            self.frm_second.config(width=answer, height=answer)


if __name__ == "__main__":
    app = App()
    app.mainloop()
