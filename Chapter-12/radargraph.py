#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  12.3 - How do I manage the pen and the brush?
# source:   wxPythonInAction-src/Chapter-12/radargraph.py
# -----------------------------------------------------------------------------
"""A radar chart, redrawn with new numbers every two seconds.

The chapter's closing example, and the one that shows what a pen and a
brush are for. In wx they are modes: set a pen, draw, set another pen,
draw again, and every line between the two setting calls comes out the
same. On a canvas there are no modes - each item carries its own outline
and fill, given when it is made. See README.md.

The double buffering of the original is not here, for the reason chapter
6 gives: a canvas keeps what is on it and redraws itself.
"""
import math
import random
import tkinter as tk
from tkinter import font


WIDTH = 520
HEIGHT = 520

SPACER = 10

# The rings, as a percentage of the longest spoke.
RINGS = (25, 50, 75, 100)

# How far the axes reach past the outermost ring.
REACH = 110

LABELS = ("Reagent", "Calibrator", "Control", "Sample", "Wash", "Waste")

MILLISECONDS = 2000

FILLS = ("#c85a5a", "#5a8cc8", "#5ac88c", "#c8b45a", "#8c5ac8")


class RadarGraph(tk.Canvas):
    """A spider's web with a shape on it."""

    def __init__(self, parent, title, labels):
        super().__init__(parent, background="white", highlightthickness=0)

        self.title_text = title
        self.labels = labels
        self.data = [0] * len(labels)
        self.fill = FILLS[0]

        self.title_font = font.Font(family="Helvetica", size=16,
                                    weight="bold")
        self.label_font = font.Font(family="Helvetica", size=9)

        # Redraw when the window is resized. This is the one thing the wx
        # original needs EVT_SIZE for that is still needed here, because
        # the drawing depends on how much room there is.
        self.bind("<Configure>", self.on_configure)

    def get_data(self):
        """What is being shown."""
        return self.data[:]

    def set_data(self, data):
        """Show something else."""
        self.data = data[:]
        self.draw_graph()

    def on_configure(self, event):
        """The window changed size, so the web has to be drawn again."""
        self.draw_graph()

    def get_cartesian(self, radius, angle, centre_x, centre_y):
        """A point on a circle, from an angle and a distance."""
        x = radius * math.cos(math.radians(angle))
        y = radius * math.sin(math.radians(angle))

        return centre_x + x, centre_y + y

    def draw_graph(self):
        """Everything, from nothing.

        delete("all") and build it again. On a canvas this is cheap and
        it is what one does: working out which items changed costs more
        than making them all afresh, until there are thousands.
        """
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        if width < 2 or height < 2:
            return

        title_height = self.title_font.metrics("linespace")

        self.create_text(width // 2, SPACER, text=self.title_text,
                         font=self.title_font, anchor=tk.N)

        centre_x = width // 2
        centre_y = (height - title_height) // 2 + title_height

        room = min(centre_x, (height - title_height) // 2)
        scale = room / (REACH + SPACER * 2)

        self.draw_web(centre_x, centre_y, scale)
        self.draw_labels(centre_x, centre_y, scale)
        self.draw_shape(centre_x, centre_y, scale)

    def draw_web(self, centre_x, centre_y, scale):
        """The rings and the two axes.

        In wx this is SetPen, four circles, SetPen again, two lines. Here
        the width is an option on each item, so the two pens never exist
        and nothing has to be set back afterwards.
        """
        for ring in RINGS:
            radius = ring * scale
            self.create_oval(centre_x - radius, centre_y - radius,
                             centre_x + radius, centre_y + radius,
                             outline="black", width=1)

        reach = REACH * scale

        self.create_line(centre_x - reach, centre_y,
                         centre_x + reach, centre_y, fill="black", width=2)
        self.create_line(centre_x, centre_y - reach,
                         centre_x, centre_y + reach, fill="black", width=2)

    def draw_labels(self, centre_x, centre_y, scale):
        """One label per spoke, just outside the outermost ring.

        wx asks the device context for GetTextExtent and places the text
        by hand. A canvas text item has an anchor, so the placing is said
        rather than calculated: the label sits with its inner edge at the
        point, whichever side of the circle it is on.
        """
        step = 360 / len(self.labels)

        for index, label in enumerate(self.labels):
            angle = index * step
            x, y = self.get_cartesian((REACH + SPACER) * scale, angle,
                                      centre_x, centre_y)

            anchor = tk.W

            if x < centre_x - 1:
                anchor = tk.E

            self.create_text(x, y, text=label, font=self.label_font,
                             anchor=anchor)

    def draw_shape(self, centre_x, centre_y, scale):
        """The filled shape, one corner per number.

        This is where a brush would be set in wx. Here fill and outline
        and width are three arguments to the one call that makes the
        polygon, and there is no state left behind to surprise the next
        drawing.
        """
        points = []
        step = 360 / len(self.data)

        for index, value in enumerate(self.data):
            points.extend(self.get_cartesian(value * scale, index * step,
                                             centre_x, centre_y))

        self.create_polygon(points, fill=self.fill, outline="navy", width=3,
                            stipple="gray50")


class App(tk.Tk):
    """A window that changes its own numbers every two seconds."""

    def __init__(self):
        super().__init__()

        self.title("Double Buffered Drawing")
        self.geometry("{}x{}".format(WIDTH, HEIGHT))

        self.graph = RadarGraph(self, "Consumables", LABELS)
        self.graph.pack(fill=tk.BOTH, expand=True)

        self.tick = None
        self.on_timeout()

    def on_timeout(self):
        """New numbers, a new colour, and ask to be called again."""
        self.graph.fill = random.choice(FILLS)
        self.graph.set_data([random.randint(10, 100)
                             for each in LABELS])

        self.tick = self.after(MILLISECONDS, self.on_timeout)

    def destroy(self):
        """Stop the clock, or Tk complains at a window that is not there."""
        if self.tick is not None:
            self.after_cancel(self.tick)
            self.tick = None

        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
