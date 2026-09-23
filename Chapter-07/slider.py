#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.8 - How do I make a slider?
# source:   wxPythonInAction-src/Chapter-07/slider.py
# -----------------------------------------------------------------------------
"""Two sliders, one across and one down, with ticks and a number on them.

This is the one place in the chapter where tk beats ttk. A ttk.Scale has
neither ticks nor a value on it; tk.Scale has tickinterval and showvalue,
which is what the wx original asks for with SL_AUTOTICKS and SL_LABELS.
"""
import tkinter as tk


LOWEST = 1
HIGHEST = 100
START = 25


class App(tk.Tk):
    """A horizontal slider and a vertical one."""

    def __init__(self):
        super().__init__()

        self.title("Slider Example")
        self.geometry("300x350")

        self.scl_across = tk.Scale(self, from_=LOWEST, to=HIGHEST,
                                   orient=tk.HORIZONTAL, tickinterval=25,
                                   showvalue=True)
        self.scl_across.set(START)
        self.scl_across.place(x=10, y=10, width=250)

        self.scl_down = tk.Scale(self, from_=LOWEST, to=HIGHEST,
                                 orient=tk.VERTICAL, tickinterval=20,
                                 showvalue=True)
        self.scl_down.set(START)
        self.scl_down.place(x=125, y=70, height=250)


if __name__ == "__main__":
    app = App()
    app.mainloop()
