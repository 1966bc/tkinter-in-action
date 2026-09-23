#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  6.2 - How do I add a status bar?
# source:   wxPythonInAction-src/Chapter-06/example2.py
# -----------------------------------------------------------------------------
"""example1.py, with the pointer position shown at the bottom.

CreateStatusBar() again, and a sunken Label again. What is new is that the
window listens to a motion event on a widget it does not own.
"""
import tkinter as tk

from example1 import SketchWindow


class App(tk.Tk):
    """A sketch window with a status bar under it."""

    def __init__(self):
        super().__init__()

        self.title("Sketch Frame")
        self.geometry("800x600")

        self.lbl_status = tk.Label(self, borderwidth=1, relief=tk.SUNKEN,
                                   anchor=tk.W)
        self.lbl_status.pack(side=tk.BOTTOM, fill=tk.X)

        self.sketch = SketchWindow(self)
        self.sketch.pack(fill=tk.BOTH, expand=True)

        # The canvas already binds <B1-Motion> for drawing. This binding is
        # on <Motion>, which is a different event, so neither is in the
        # other's way and no "break" is wanted here.
        self.sketch.bind("<Motion>", self.on_sketch_motion)

    def on_sketch_motion(self, event):
        """Say where the pointer is."""
        self.lbl_status.config(text="({}, {})".format(event.x, event.y))


if __name__ == "__main__":
    app = App()
    app.mainloop()
