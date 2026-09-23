#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  12.1 - How do I load and scale an image?
# source:   wxPythonInAction-src/Chapter-12/images.py
# -----------------------------------------------------------------------------
"""One picture in several formats, each shown at full size and at half.

The wx original loads the same drawing as .bmp, .gif, .jpg and .png, and
wx.Image reads all four. A PhotoImage reads two of them.

The picture is drawn here rather than shipped, and written out in the
formats Tk can write, which is a short list for the same reason.
See README.md.
"""
import os
import tempfile
import tkinter as tk


WIDTH = 120
HEIGHT = 90

# What a PhotoImage can read without help. BMP and JPEG are not on it.
FORMATS = ("png", "gif")

GAP = 10


def get_drawing(width, height):
    """A picture, made rather than loaded.

    put() takes a Tcl list of rows of colours, so a picture can be built
    a rectangle at a time. A colour name with a space in it would be read
    as two colours, which chapter 6 found the hard way.
    """
    drawing = tk.PhotoImage(width=width, height=height)

    drawing.put("navy", to=(0, 0, width, height))
    drawing.put("gold", to=(6, 6, width - 6, height - 6))
    drawing.put("firebrick", to=(width // 4, height // 4,
                                 width * 3 // 4, height * 3 // 4))

    return drawing


class App(tk.Tk):
    """Each format at full size, and beside it the same at half."""

    def __init__(self, directory):
        super().__init__()

        self.title("Loading Images")

        # Held on self. Images in a local would be collected before the
        # window is drawn and every cell would be empty.
        self.images = []

        drawing = get_drawing(WIDTH, HEIGHT)

        for row, suffix in enumerate(FORMATS):
            path = os.path.join(directory, "image." + suffix)
            drawing.write(path, format=suffix)

            self.set_row(row, suffix, path)

    def set_row(self, row, suffix, path):
        """One format: the picture, then the same picture at half size."""
        lbl_name = tk.Label(self, text=suffix)
        lbl_name.grid(row=row, column=0, padx=GAP, pady=GAP)

        full = tk.PhotoImage(file=path)

        # wx scales to any size at all. A PhotoImage divides by a whole
        # number: subsample(2) halves it, subsample(3) takes a third, and
        # nothing at all takes two thirds.
        half = full.subsample(2, 2)

        self.images.extend([full, half])

        for column, image in enumerate([full, half], start=1):
            lbl_image = tk.Label(self, image=image, borderwidth=0)
            lbl_image.grid(row=row, column=column, padx=GAP, pady=GAP)


if __name__ == "__main__":
    app = App(tempfile.mkdtemp(prefix="tkinter-in-action-"))
    app.mainloop()
