#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  6.1 - How do I draw on a window?
# source:   wxPythonInAction-src/Chapter-06/example1.py
# -----------------------------------------------------------------------------
"""Sketch: a window that can be drawn on with the mouse.

The foundation the rest of the chapter is built on, and the shortest file
of the seven by a long way. Forty lines of the wx original are about
keeping a bitmap and painting it back; a Canvas keeps what was drawn on it
and paints itself. See README.md.
"""
import tkinter as tk


BACKGROUND = "white"


class SketchWindow(tk.Canvas):
    """A canvas that remembers the lines drawn on it.

    self.lines is kept for the same reason the wx original keeps it: so
    that a sketch can be saved and read back. The canvas does not need it
    to redraw - it has the lines already, as objects.
    """

    def __init__(self, parent):
        super().__init__(parent, background=BACKGROUND, highlightthickness=0)

        self.color = "black"
        self.thickness = 1

        self.lines = []
        self.current_line = []
        self.position = (0, 0)

        self.bind("<Button-1>", self.on_left_down)
        self.bind("<B1-Motion>", self.on_motion)
        self.bind("<ButtonRelease-1>", self.on_left_up)

    def get_lines_data(self):
        """A copy of the sketch, for whoever is going to save it."""
        return self.lines[:]

    def set_lines_data(self, lines):
        """Replace the sketch with one that was read from somewhere."""
        self.lines = lines[:]
        self.redraw()

    def redraw(self):
        """Put self.lines back on the canvas.

        Only needed after the lines have been replaced from outside. A
        resize or an uncovered window does not come here: Tk redraws what
        is on a canvas by itself, which is what the wx buffer was for.
        """
        self.delete("all")

        for color, thickness, line in self.lines:
            for coords in line:
                self.create_line(*coords, fill=color, width=thickness)

    def on_left_down(self, event):
        """Start a line.

        The wx original calls CaptureMouse() here so that dragging outside
        the window keeps reporting. Tk grabs the pointer for the duration
        of a button press by itself, so there is nothing to ask for and
        nothing to release.
        """
        self.current_line = []
        self.position = (event.x, event.y)

    def on_motion(self, event):
        """Draw from where the pointer was to where it is now."""
        coords = self.position + (event.x, event.y)

        self.current_line.append(coords)
        self.create_line(*coords, fill=self.color, width=self.thickness)

        self.position = (event.x, event.y)

    def on_left_up(self, event):
        """Finish the line and keep it."""
        self.lines.append((self.color, self.thickness, self.current_line))
        self.current_line = []

    def set_color(self, color):
        """The colour the next line will be drawn in."""
        self.color = color

    def set_thickness(self, thickness):
        """The width the next line will be drawn at."""
        self.thickness = thickness


class App(tk.Tk):
    """A window with nothing in it but somewhere to draw."""

    def __init__(self):
        super().__init__()

        self.title("Sketch Frame")
        self.geometry("800x600")

        self.sketch = SketchWindow(self)
        self.sketch.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
