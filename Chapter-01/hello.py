#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  1.4 - Creating the final hello.py program
# source:   wxPythonInAction-src/Chapter-01/hello.py
# -----------------------------------------------------------------------------
"""A window the size of a photograph, with the photograph in it.

The first thing in the book that Tkinter cannot do alone: it has no JPEG
reader. Pillow supplies one. And the image has to be kept alive by hand or
it vanishes; see README.md for both.

The picture is made on the first run rather than shipped, which keeps the
point rather than weakening it: Pillow writes a JPEG, and then Pillow has
to be asked to read it back, because a PhotoImage cannot.
"""
import os
import sys
import tkinter as tk

try:
    from PIL import Image, ImageDraw, ImageTk
except ImportError:
    sys.exit("This example needs Pillow: apt install python3-pil.imagetk")


# Beside this file, not in whatever directory the program was started from.
IMAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "hello.jpg")

WIDTH = 524
HEIGHT = 125


def set_image(path):
    """Draw the picture, once, if it is not already there.

    A JPEG on purpose. A PNG would be read by Tk itself and there would be
    nothing left to demonstrate.
    """
    if not os.path.exists(path):
        image = Image.new("RGB", (WIDTH, HEIGHT), "#0f1b2d")
        draw = ImageDraw.Draw(image)

        draw.rectangle((8, 8, WIDTH - 9, HEIGHT - 9), outline="#2a3d5c",
                       width=2)
        draw.text((30, 44), "Hello, Tkinter!", fill="white")
        draw.text((30, 70), "This picture is a JPEG, so Tk cannot read it.",
                  fill="#8fa8c8")

        image.save(path, "JPEG", quality=90)

    return path


class App(tk.Tk):
    """A window showing one image, sized to it."""

    def __init__(self, path):
        super().__init__()

        self.title("Hello, Tkinter!")

        image = Image.open(path)
        width, height = image.size

        # The Label does not own what it displays: if the only reference to
        # the PhotoImage is this local name, it is collected the moment
        # __init__ returns and the Label goes blank. Keeping it on self is
        # the whole fix, and there is nothing like it in wx.
        self.photo = ImageTk.PhotoImage(image)

        # A Label draws a border and a focus ring by default, two pixels in
        # each direction. The window is meant to be the size of the picture,
        # so they are asked for at nought.
        lbl_image = tk.Label(self, image=self.photo, borderwidth=0,
                             highlightthickness=0)
        lbl_image.pack(fill=tk.BOTH, expand=True)

        self.geometry("{}x{}".format(width, height))
        self.resizable(False, False)


if __name__ == "__main__":
    app = App(set_image(IMAGE))
    app.mainloop()
