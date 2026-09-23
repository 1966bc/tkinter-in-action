#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 1: the things that would break quietly.

Not much to measure here, but three of the four faults this chapter can have
produce no error at all - a blank window, a coordinate from the wrong origin,
a file that is only found from one directory. Those are what is tested.

Run them from the project directory:

    python3 -m unittest discover -s tests -v

One thing to expect. Tk is meant to be one interpreter per process, and
these tests build and destroy one per example. Running the whole suite
prints a Tcl complaint once, when ttk initialises in a new interpreter and
broadcasts a theme change to every interpreter it has seen, including the
ones already destroyed:

    can't invoke "event" command: application has been destroyed
        while executing "event generate $w <<ThemeChanged>>"

It is noise, not a failure, and it goes away if a module is run on its own.
Removing it for good would mean one process per example, which costs more
than it is worth here.
"""
import os
import sys
import tkinter as tk
import unittest

import chapter

HERE = chapter.ROOT


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says.

    Asking by building a Tk and destroying it also works, and costs more
    than it looks: ttk later broadcasts a theme change to every interpreter
    it has ever seen, the destroyed one included, and the run fills with
    Tcl errors about nothing.
    """
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


class FakeEvent:
    """What Tk hands a <Motion> handler, as far as the handler cares."""

    def __init__(self, x, y):
        self.x = x
        self.y = y


@unittest.skipUnless(has_display(), "no display, no windows to build")
class TestChapter01(unittest.TestCase):
    """The four examples, and the silences they can fail into."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-01")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_spare_opens_a_window_with_a_name(self):
        """The starting point every later example is built from."""
        import spare

        self.app = spare.App()
        self.assertEqual(self.app.title(), "Spare")

    def test_hello_is_the_size_of_its_picture(self):
        """524x125, the image itself. A Label draws a border and a focus
        ring unless asked not to, and the window would come out 526x127
        with the picture clipped by a pixel on each side."""
        import hello

        self.app = hello.App(hello.set_image(hello.IMAGE))
        self.app.update_idletasks()

        self.assertEqual((self.app.winfo_reqwidth(),
                          self.app.winfo_reqheight()),
                         (hello.WIDTH, hello.HEIGHT))

    def test_hello_keeps_a_reference_to_its_image(self):
        """The one that fails in silence. A widget does not own the image
        it shows: it holds the name of a Tk image object, and the Python
        PhotoImage is what keeps that object alive. Held in a local
        variable it is collected when __init__ returns, Tk destroys the
        image, and the Label draws nothing - no error, no traceback,
        nothing in the log. Just an empty window."""
        import hello

        self.app = hello.App(hello.set_image(hello.IMAGE))

        self.assertTrue(hasattr(self.app, "photo"),
                        "the PhotoImage is not held anywhere")
        self.assertEqual(self.app.photo.width(), 524)

    def test_hello_makes_its_own_picture_and_finds_it_anywhere(self):
        """Two things at once.

        The path is built from __file__, so the example runs from any
        directory - the wx original opens its picture by a bare name and
        runs only from the one it sits in.

        And the picture is made rather than shipped, as a JPEG on
        purpose: a PNG would be read by Tk itself and there would be
        nothing left to demonstrate.
        """
        import hello

        self.assertTrue(os.path.isabs(hello.IMAGE))
        self.assertTrue(hello.IMAGE.endswith(".jpg"))

        hello.set_image(hello.IMAGE)
        self.assertTrue(os.path.exists(hello.IMAGE))

        # And Tk still cannot open it, which is the whole lesson. A
        # PhotoImage lives inside an interpreter, so there has to be one
        # before it can refuse.
        self.app = tk.Tk()
        self.assertRaises(tk.TclError, tk.PhotoImage, file=hello.IMAGE)

    def test_sample_reports_the_position_it_was_given(self):
        """Relative to the bound widget, which is what wx reports too.
        winfo_pointerxy() also exists, gives screen coordinates, and would
        look almost right in a window at the top left of the display."""
        import sample

        self.app = sample.App()
        self.app.on_move(FakeEvent(17, 42))

        self.assertEqual(self.app.position.get(), "17, 42")

    def test_python_compare_has_a_menu_and_a_status_bar(self):
        """Tk has no status bar widget. It is a sunken Label at the bottom,
        assembled by hand, and it is easy to leave out."""
        import python_compare

        self.app = python_compare.App()
        self.app.update_idletasks()

        self.assertNotEqual(self.app.cget("menu"), "")

        labels = [w for w in self.app.winfo_children()
                  if w.winfo_class() == "Label"]

        self.assertEqual(len(labels), 1)
        self.assertEqual(str(labels[0].cget("relief")), "sunken")


if __name__ == "__main__":
    unittest.main()
