#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.4 - How do I make a combo box?
# source:   wxPythonInAction-src/Chapter-07/combo_box.py
# -----------------------------------------------------------------------------
"""Two combo boxes: one that drops down, one that is always open.

The first is ttk.Combobox. The second, wx.CB_SIMPLE, has no equivalent and
is built here out of an Entry and a Listbox, which is what it is anyway.
"""
import tkinter as tk
from tkinter import ttk


SAMPLE = ("zero", "one", "two", "three", "four", "five",
          "six", "seven", "eight")

DEFAULT = "default value"


class SimpleCombo(tk.Frame):
    """What wx.CB_SIMPLE is: a field with its list always showing.

    ttk.Combobox drops down and cannot be told not to. The parts are an
    Entry and a Listbox, and the only work is keeping them in step.
    """

    def __init__(self, parent, values, value=""):
        super().__init__(parent)

        self.ent_value = tk.Entry(self)
        self.ent_value.insert(0, value)
        self.ent_value.pack(fill=tk.X)

        self.lst_values = tk.Listbox(self, height=6, exportselection=False)

        for item in values:
            self.lst_values.insert(tk.END, item)

        self.lst_values.pack(fill=tk.BOTH, expand=True)
        self.lst_values.bind("<<ListboxSelect>>", self.on_select)

    def on_select(self, event):
        """Put what was chosen in the field."""
        selected = self.lst_values.curselection()

        if selected:
            self.ent_value.delete(0, tk.END)
            self.ent_value.insert(0, self.lst_values.get(selected[0]))

    def get(self):
        """What the field says, typed or chosen."""
        return self.ent_value.get()


class App(tk.Tk):
    """One of each kind."""

    def __init__(self):
        super().__init__()

        self.title("Combo Box Example")
        self.geometry("350x300")

        lbl_select = tk.Label(self, text="Select one:")
        lbl_select.place(x=15, y=15)

        self.cb_drop = ttk.Combobox(self, values=SAMPLE, width=14)
        self.cb_drop.set(DEFAULT)
        self.cb_drop.place(x=15, y=35)

        self.cb_simple = SimpleCombo(self, SAMPLE, DEFAULT)
        self.cb_simple.place(x=160, y=35, width=130, height=140)


if __name__ == "__main__":
    app = App()
    app.mainloop()
