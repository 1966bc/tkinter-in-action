#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.3 - How do I make a checkbox?
# source:   wxPythonInAction-src/Chapter-07/checkbox.py
# -----------------------------------------------------------------------------
"""Three checkboxes.

wx keeps the state inside the widget and is asked with GetValue(). A Tk
Checkbutton keeps it in a variable you provide, and if you provide none it
keeps it in one of its own that you cannot find again.
"""
import tkinter as tk


LABELS = ("Alpha", "Beta", "Gamma")


class App(tk.Tk):
    """Three boxes to tick."""

    def __init__(self):
        super().__init__()

        self.title("Checkbox Example")
        self.geometry("150x200")

        # Held on self, not in a local: a variable that is collected takes
        # the state of its widget with it. The same trap as an image.
        self.values = {}

        for index, label in enumerate(LABELS):
            self.values[label] = tk.BooleanVar()

            chk_box = tk.Checkbutton(self, text=label, anchor=tk.W,
                                     variable=self.values[label])
            chk_box.place(x=35, y=40 + index * 20, width=150, height=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()
