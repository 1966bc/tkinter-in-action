#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  5.2 - What is refactoring and why is it worth doing?
# source:   wxPythonInAction-src/Chapter-05/badExample.py
# -----------------------------------------------------------------------------
"""The same window as goodExample.py, written the way one writes it first.

Everything in __init__, one line per widget, the menu spelled out item by
item. It works. Read it next to goodExample.py and then decide.
"""
import tkinter as tk


class App(tk.Tk):
    """A window built entirely in its own constructor."""

    def __init__(self):
        super().__init__()

        self.title("Refactor Example")
        self.geometry("340x200")
        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        frm_panel = tk.Frame(self, background="white")
        frm_panel.pack(fill=tk.BOTH, expand=True)

        btn_prev = tk.Button(frm_panel, text="<< PREV", command=self.on_prev)
        btn_prev.place(x=80, y=0)

        btn_next = tk.Button(frm_panel, text="NEXT >>", command=self.on_next)
        btn_next.place(x=160, y=0)

        mnu_bar = tk.Menu(self)

        mnu_file = tk.Menu(mnu_bar, tearoff=0)
        mnu_file.add_command(label="Open", underline=0, command=self.on_open)
        mnu_file.add_command(label="Quit", underline=0,
                             command=self.on_close_window)
        mnu_bar.add_cascade(label="File", underline=0, menu=mnu_file)

        mnu_edit = tk.Menu(mnu_bar, tearoff=0)
        mnu_edit.add_command(label="Copy", underline=0, command=self.on_copy)
        mnu_edit.add_command(label="Cut", underline=1, command=self.on_cut)
        mnu_edit.add_command(label="Paste", underline=0, command=self.on_paste)
        mnu_bar.add_cascade(label="Edit", underline=0, menu=mnu_edit)

        self.config(menu=mnu_bar)

        lbl_first = tk.Label(frm_panel, text="First Name", background="white")
        lbl_first.place(x=10, y=50)

        ent_first = tk.Entry(frm_panel, width=14)
        ent_first.place(x=80, y=50)

        lbl_last = tk.Label(frm_panel, text="Last Name", background="white")
        lbl_last.place(x=10, y=80)

        ent_last = tk.Entry(frm_panel, width=14)
        ent_last.place(x=80, y=80)

    def on_prev(self):
        """Nothing yet. The chapter is about the shape, not the work."""
        pass

    def on_next(self):
        """Nothing yet."""
        pass

    def on_open(self):
        """Nothing yet."""
        pass

    def on_copy(self):
        """Nothing yet."""
        pass

    def on_cut(self):
        """Nothing yet."""
        pass

    def on_paste(self):
        """Nothing yet."""
        pass

    def on_close_window(self):
        """Shut the window."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
