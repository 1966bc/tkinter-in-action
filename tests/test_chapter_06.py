#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 6: Sketch, and the drawing that does not need a buffer.

Drawing is tested by drawing: motion events are sent at the canvas and the
objects it holds are counted. A sketch is saved and read back, which is the
one thing in the chapter that can lose somebody's work.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import pickle
import sys
import tempfile
import tkinter as tk
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "Chapter-06"))


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no canvas to draw on")
class TestChapter06(unittest.TestCase):
    """Sketch, from the canvas up."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def get_event(self, x, y):
        """What Tk hands a mouse handler, as far as the handler cares."""
        event = tk.Event()
        event.x = x
        event.y = y

        return event

    def draw(self, sketch, points):
        """Press, drag through the points, release."""
        sketch.on_left_down(self.get_event(*points[0]))

        for x, y in points[1:]:
            sketch.on_motion(self.get_event(x, y))

        sketch.on_left_up(self.get_event(*points[-1]))

    def test_a_line_becomes_objects_on_the_canvas(self):
        """The canvas keeps what was drawn, which is why none of the wx
        buffering machinery has a translation."""
        import example1

        self.app = example1.App()
        self.app.update()

        self.draw(self.app.sketch, [(0, 0), (10, 10), (20, 5)])

        self.assertEqual(len(self.app.sketch.find_all()), 2)
        self.assertEqual(len(self.app.sketch.lines), 1)

    def test_the_canvas_keeps_the_line_after_a_resize(self):
        """In wx this is what InitBuffer, OnSize and OnIdle are for. Here
        there is nothing to test but the absence of the problem."""
        import example1

        self.app = example1.App()
        self.app.update()

        self.draw(self.app.sketch, [(0, 0), (10, 10)])
        self.app.geometry("400x300")
        self.app.update()

        self.assertEqual(len(self.app.sketch.find_all()), 1)

    def test_a_sketch_survives_being_written_and_read(self):
        """The one thing in the chapter that can lose somebody's work."""
        import example6

        self.app = example6.App()
        self.app.update()

        self.draw(self.app.sketch, [(0, 0), (10, 10), (20, 5)])
        drawn = self.app.sketch.get_lines_data()

        path = os.path.join(tempfile.gettempdir(), "test.sketch")
        self.app.filename = path
        self.app.save_file()

        self.app.sketch.set_lines_data([])
        self.assertEqual(self.app.sketch.get_lines_data(), [])

        self.app.read_file()
        self.assertEqual(self.app.sketch.get_lines_data(), drawn)
        self.assertEqual(len(self.app.sketch.find_all()), 2)

        os.remove(path)

    def test_a_file_that_is_not_a_sketch_does_not_pass_for_one(self):
        """Fail safe, and say so. A read that quietly gave back an empty
        sketch would look exactly like an empty sketch.

        showerror has to be taken away for the duration: it is modal, and
        a test that opens it waits for somebody to press OK for ever. That
        is worth knowing before writing a test suite around a program that
        talks to people.
        """
        import example6

        self.app = example6.App()

        shown = []
        showerror = example6.messagebox.showerror
        example6.messagebox.showerror = lambda *args, **kwargs: shown.append(args)

        path = os.path.join(tempfile.gettempdir(), "rubbish.sketch")

        with open(path, "wb") as target:
            target.write(b"this is not a pickle")

        try:
            self.app.filename = path
            self.app.read_file()
        finally:
            example6.messagebox.showerror = showerror
            os.remove(path)

        self.assertEqual(self.app.filename, "")
        self.assertEqual(len(shown), 1)

    def test_choosing_a_colour_in_one_place_moves_the_other(self):
        """The menu item and the toolbar swatch share a StringVar, so the
        two dictionaries and the bookkeeping of the wx original are not
        needed and cannot go out of step."""
        import example5

        self.app = example5.App()
        self.app.update()

        self.app.colour.set("Red")
        self.app.on_color()

        self.assertEqual(self.app.sketch.color, "red")

    def test_a_swatch_is_drawn_not_loaded(self):
        """put() takes a Tcl list of rows of colours, so a name with a
        space in it is read as two colours. All sixteen of the palette are
        drawn here, and forest green is the one that would fail."""
        import example7

        self.app = example7.App()
        self.app.update()

        self.assertEqual(len(self.app.control.swatches), len(example7.PALETTE))

        swatch = self.app.control.swatches["Forest Green"]
        self.assertEqual((swatch.width(), swatch.height()),
                         (example7.SWATCH_WIDTH, example7.SWATCH_HEIGHT))


if __name__ == "__main__":
    unittest.main()
