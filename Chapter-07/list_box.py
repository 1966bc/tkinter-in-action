#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.6 - How do I make a list box?
# source:   wxPythonInAction-src/Chapter-07/list_box.py
# -----------------------------------------------------------------------------
"""A list of fifteen things with the fourth already chosen.

wx.ListBox and tk.Listbox, and the only difference is that Tk's does not
scroll by itself: a Listbox with no Scrollbar beside it simply shows what
fits and says nothing about the rest.
"""
import tkinter as tk


SAMPLE = ("zero", "one", "two", "three", "four", "five",
          "six", "seven", "eight", "nine", "ten", "eleven",
          "twelve", "thirteen", "fourteen")


class App(tk.Tk):
    """One list, single selection, with the fourth item chosen."""

    def __init__(self):
        super().__init__()

        self.title("List Box Example")
        self.geometry("250x200")

        self.lst_sample = tk.Listbox(self, selectmode=tk.SINGLE,
                                     exportselection=False)

        for item in SAMPLE:
            self.lst_sample.insert(tk.END, item)

        self.lst_sample.selection_set(3)
        self.lst_sample.see(3)
        self.lst_sample.place(x=20, y=20, width=80, height=120)

        scrollbar = tk.Scrollbar(self, command=self.lst_sample.yview)
        self.lst_sample.config(yscrollcommand=scrollbar.set)
        scrollbar.place(x=100, y=20, height=120)


if __name__ == "__main__":
    app = App()
    app.mainloop()
