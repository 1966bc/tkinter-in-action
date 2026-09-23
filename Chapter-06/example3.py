#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  6.2 - How do I put more than one thing in a status bar?
# source:   wxPythonInAction-src/Chapter-06/example3.py
# -----------------------------------------------------------------------------
"""example2.py, with three fields in the status bar instead of one.

wx asks the status bar for three fields and gives them relative widths.
Tkinter has no status bar, so there are three Labels in a Frame, and the
relative widths are pack() and expand. See README.md.
"""
import tkinter as tk

from example1 import SketchWindow


# The relative widths of the wx original, [-1, -2, -3], which means one
# share, two shares, three shares of whatever there is.
SHARES = (1, 2, 3)


class App(tk.Tk):
    """A sketch window with a status bar of three fields."""

    def __init__(self):
        super().__init__()

        self.title("Sketch Frame")
        self.geometry("800x600")

        self.fields = self.get_status_bar()

        self.sketch = SketchWindow(self)
        self.sketch.pack(fill=tk.BOTH, expand=True)

        self.sketch.bind("<Motion>", self.on_sketch_motion)

    def get_status_bar(self):
        """Three sunken Labels in a row, sharing the width one to two to
        three. pack() has no proportions, so the shares are grid weights,
        for the reason chapter 11 gives."""
        frm_status = tk.Frame(self)
        frm_status.pack(side=tk.BOTTOM, fill=tk.X)

        fields = []

        for column, share in enumerate(SHARES):
            label = tk.Label(frm_status, borderwidth=1, relief=tk.SUNKEN,
                             anchor=tk.W)
            label.grid(row=0, column=column, sticky=tk.E + tk.W)
            frm_status.grid_columnconfigure(column, weight=share)
            fields.append(label)

        return fields

    def on_sketch_motion(self, event):
        """The position, the line being drawn, and how many there are."""
        self.fields[0].config(text="Pos: ({}, {})".format(event.x, event.y))
        self.fields[1].config(text="Current Pts: {}".format(
            len(self.sketch.current_line)))
        self.fields[2].config(text="Line Count: {}".format(
            len(self.sketch.lines)))


if __name__ == "__main__":
    app = App()
    app.mainloop()
