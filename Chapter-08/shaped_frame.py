#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.6 - How do I make a shaped window?
# source:   wxPythonInAction-src/Chapter-08/shaped_frame.py
# -----------------------------------------------------------------------------
"""A window with no title bar, showing a picture. Not a shaped one.

The wx original builds a region from the bitmap's transparency and hands
it to SetShape, so the window really is the shape of the drawing and the
desktop shows through everywhere else.

Tk cannot do this, and the reason is not that nobody got round to it.
Asked on this machine, a Tk window offers exactly these attributes:

    -alpha  -topmost  -zoomed  -fullscreen  -type

-alpha is the transparency of the whole window at once, which is a
different thing. -transparentcolor exists on Windows and Tk says "bad
attribute" here. The X11 shape extension is not exposed at all.

So what is left is the half that does work: overrideredirect(True) for a
window with no decorations, the picture in it, double click to put the
border back and right click to close. The corners stay square, and that is
the difference. See README.md.
"""
import tkinter as tk

import images


class App(tk.Tk):
    """A bare window with a picture in it, draggable and closable."""

    def __init__(self):
        super().__init__()

        self.title("Shaped Window")

        self.shaped = True
        self.image = images.get_vippi_image()

        self.lbl_image = tk.Label(self, image=self.image, borderwidth=0,
                                  highlightthickness=0)
        self.lbl_image.pack()

        self.geometry("{}x{}".format(self.image.width(),
                                     self.image.height()))
        self.set_shape()

        self.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<Button-3>", self.on_exit)

    def set_shape(self):
        """As close as Tk gets: no title bar, no border, no taskbar entry."""
        self.overrideredirect(self.shaped)

    def on_double_click(self, event):
        """Put the decorations back, or take them away again."""
        self.shaped = not self.shaped
        self.set_shape()

    def on_exit(self, event):
        """Right click closes it, because with no title bar there is no
        other way, which is a thing to think about before using this."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
