#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  12.2 - How do I draw an image many times?
# source:   wxPythonInAction-src/Chapter-12/draw_image.py
# -----------------------------------------------------------------------------
"""One picture, put down in fifty places.

The wx original keeps a list of positions and draws the bitmap at each of
them on every EVT_PAINT, because a device context forgets. A canvas does
not: each create_image is an object it keeps and redraws by itself.

Which is chapter 6 again, and here the trade shows the other way round.
Fifty images are fifty objects, and each one can be moved, raised, bound
to a click or deleted by name. In wx they are fifty calls that happened
and left no trace.
"""
import random
import tkinter as tk


WIDTH = 640
HEIGHT = 480

COUNT = 50

BACKGROUND = "sky blue"


def get_drawing():
    """A small picture with a clear corner, made rather than loaded.

    transparency_set is per pixel, and it is what the True at the end of
    the wx DrawBitmap call asks for: draw the picture, and let what is
    behind show through where it is clear.
    """
    drawing = tk.PhotoImage(width=40, height=40)

    drawing.put("firebrick", to=(0, 0, 40, 40))
    drawing.put("white", to=(8, 8, 32, 32))

    for x in range(12):
        for y in range(12):
            if x + y < 12:
                drawing.transparency_set(x, y, True)

    return drawing


class App(tk.Tk):
    """A canvas with the same picture scattered over it."""

    def __init__(self):
        super().__init__()

        self.title("Drawing Images")
        self.geometry("{}x{}".format(WIDTH, HEIGHT))

        self.drawing = get_drawing()

        self.canvas = tk.Canvas(self, background=BACKGROUND,
                                highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.positions = [(10, 10)]

        for each in range(COUNT):
            self.positions.append((random.randint(0, WIDTH),
                                   random.randint(0, HEIGHT)))

        self.set_images()

    def set_images(self):
        """One canvas item per position.

        anchor=NW because a canvas image is centred on its point unless
        told otherwise, and the wx original gives the top left corner.
        """
        for x, y in self.positions:
            self.canvas.create_image(x, y, image=self.drawing, anchor=tk.NW,
                                     tags="drawing")


if __name__ == "__main__":
    app = App()
    app.mainloop()
