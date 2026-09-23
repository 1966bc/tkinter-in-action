#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.7 - How do I make a radio box?
# source:   wxPythonInAction-src/Chapter-07/radio_box.py
# -----------------------------------------------------------------------------
"""Nine choices laid out in a labelled box, twice.

wx.RadioBox is one widget that is a frame, a label and a set of radio
buttons in so many columns. Tkinter has the three parts and not the
compound, so the compound is assembled: a LabelFrame and a grid.
"""
import tkinter as tk
from tkinter import ttk


SAMPLE = ("zero", "one", "two", "three", "four", "five",
          "six", "seven", "eight")


class RadioBox(tk.Frame):
    """What wx.RadioBox is, in the parts Tkinter has.

    A LabelFrame when there is a label, a plain Frame when there is not,
    and the buttons filled down the columns as wx.RA_SPECIFY_COLS does.
    """

    def __init__(self, parent, label, values, columns):
        super().__init__(parent)

        self.value = tk.StringVar(value=values[0])

        if label:
            box = ttk.LabelFrame(self, text=label)
        else:
            box = ttk.Frame(self, borderwidth=0)

        box.pack(fill=tk.BOTH, expand=True)

        rows = -(-len(values) // columns)

        for index, name in enumerate(values):
            button = ttk.Radiobutton(box, text=name, value=name,
                                     variable=self.value)
            button.grid(row=index % rows, column=index // rows,
                        sticky=tk.W, padx=4, pady=1)

    def get(self):
        """Which one is chosen."""
        return self.value.get()


class App(tk.Tk):
    """Two radio boxes, one with a label and one without."""

    def __init__(self):
        super().__init__()

        self.title("Radio Box Example")
        self.geometry("350x200")

        self.box_labelled = RadioBox(self, "A Radio Box", SAMPLE, 2)
        self.box_labelled.place(x=10, y=10)

        self.box_plain = RadioBox(self, "", SAMPLE, 3)
        self.box_plain.place(x=180, y=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
