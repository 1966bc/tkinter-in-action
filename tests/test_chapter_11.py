#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 11 measured against the windows wxPython draws.

The reference is tests/wx_geometry.json, recorded from the book's own
examples by tools/record_wx_geometry.py. These tests need neither wxPython
nor the book's sources: they need a display and the file.

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

A failure here means a translation has moved. It does not always mean it has
got worse, but it always means somebody should look.
"""
import json
import os
import sys
import tkinter as tk
import unittest

import chapter

HERE = chapter.ROOT

REFERENCE = json.load(open(os.path.join(HERE, "tests", "wx_geometry.json")))


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


def get_windows(app, size):
    """Every window of a running example, measured the way wx was."""
    if size is not None:
        app.geometry("{}x{}".format(size[0], size[1]))

    app.update_idletasks()

    tops = [app]
    tops.extend(w for w in app.winfo_children() if isinstance(w, tk.Toplevel))

    measured = {}

    for top in tops:
        if size is not None:
            top.geometry("{}x{}".format(size[0], size[1]))
            top.update_idletasks()

        blocks = {}

        for child in top.winfo_children():
            label = getattr(child, "label", None)

            if label is not None:
                blocks[label] = (child.winfo_x(), child.winfo_y(),
                                 child.winfo_width(), child.winfo_height())

        width = top.winfo_reqwidth()
        height = top.winfo_reqheight()

        if size is not None:
            width = top.winfo_width()
            height = top.winfo_height()

        measured[top.title()] = {"width": width, "height": height,
                                 "blocks": blocks}

    return measured


def get_reference(name, size):
    """The wx measurements of one example, by window title."""
    windows = {}

    for entry in REFERENCE["Chapter-11"][name]:
        asked = entry["asked"]

        if asked is not None:
            asked = tuple(asked)

        if asked == size:
            blocks = {}

            for widget in entry["widgets"]:
                blocks[widget["name"]] = (widget["x"], widget["y"],
                                          widget["width"], widget["height"])

            windows[entry["title"]] = {"width": entry["width"],
                                       "height": entry["height"],
                                       "blocks": blocks}

    return windows


@unittest.skipUnless(has_display(), "no display, no windows to measure")
class TestChapter11(unittest.TestCase):
    """Each example beside the window the book's own code draws."""

    def setUp(self):
        """Nothing built yet. Every test makes and destroys its own window."""
        chapter.use("Chapter-11")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def measure(self, name, size=None):
        """Build one example and hand back both sets of numbers."""
        module = __import__(name)
        self.app = module.App()

        return get_windows(self.app, size), get_reference(name, size)

    def assert_same(self, name, size=None, except_blocks=()):
        """Same window size, same block in the same place, as wx."""
        ours, theirs = self.measure(name, size)

        self.assertEqual(sorted(ours), sorted(theirs), "different windows")

        for title in theirs:
            self.assertEqual((ours[title]["width"], ours[title]["height"]),
                             (theirs[title]["width"], theirs[title]["height"]),
                             "{}: window size".format(title))

            for label in theirs[title]["blocks"]:
                if label not in except_blocks:
                    self.assertEqual(ours[title]["blocks"].get(label),
                                     theirs[title]["blocks"][label],
                                     "{}: block {}".format(title, label))

    def test_basicgridsizer_is_the_same_window(self):
        """Nine equal cells, five pixels apart, and nothing around them."""
        self.assert_same("basicgridsizer")

    def test_mingridsizer_is_the_same_window(self):
        """One block grows and all nine cells grow, which is minsize doing
        the work uniform cannot do without disturbing the gap."""
        self.assert_same("mingridsizer")

    def test_prependgridsizer_is_the_same_window(self):
        """Nine in the first cell and one in the last: Prepend() is
        arithmetic on the index, and the arithmetic has to be right."""
        self.assert_same("prependgridsizer")

    def test_bordergridsizer_is_the_same_window(self):
        """Nine different borders, each the sum of a gap and a side."""
        self.assert_same("bordergridsizer")

    def test_basicflexgridsizer_is_the_same_window(self):
        """Only the row and column of the big block grow, which is what
        grid() does when nothing is asked of it."""
        self.assert_same("basicflexgridsizer")

    def test_gridbagsizer_is_the_same_window(self):
        """Including the two blocks that span, which is where a rowspan
        gets counted wrong if it is going to be."""
        self.assert_same("gridbagsizer")

    def test_resizeflexgridsizer_shares_the_space_as_wx_does(self):
        """Weights of 1, 2, 1 against AddGrowableCol: the same arithmetic,
        down to which row gets the pixel that will not divide."""
        self.assert_same("resizeflexgridsizer", size=(500, 300))

    def test_resizegridsizer_aligns_as_wx_does(self):
        """The alignment flags are sticky. Block eight is wx.SHAPED, which
        has no equivalent, and block six is one pixel of rounding: both are
        written down in README.md and left out here on purpose."""
        self.assert_same("resizegridsizer", size=(500, 250),
                         except_blocks=("eight", "six"))

    def test_boxsizer_packs_three_of_its_four_windows_as_wx_does(self):
        """pack() is a box sizer. The fourth window is not compared: wx
        divides the free space in the given ratio, Tk divides the surplus,
        and the difference is the subject of that example."""
        ours, theirs = self.measure("boxsizer")

        for title in ("Vertical BoxSizer", "Horizontal BoxSizer",
                      "Stretchable BoxSizer"):
            self.assertEqual((ours[title]["width"], ours[title]["height"]),
                             (theirs[title]["width"], theirs[title]["height"]),
                             "{}: window size".format(title))
            self.assertEqual(ours[title]["blocks"], theirs[title]["blocks"],
                             "{}: blocks".format(title))

    def test_boxsizer_proportions_differ_from_wx_by_a_known_amount(self):
        """The one place the two disagree on purpose. If this ever passes
        as equal, Tk has changed and the chapter is wrong."""
        ours, theirs = self.measure("boxsizer")
        title = "Proportional BoxSizer"

        self.assertEqual(ours[title]["height"], 180)
        self.assertEqual(theirs[title]["height"], 210)

    def test_staticboxsizer_keeps_the_arrangement(self):
        """Not the pixels: a ttk.LabelFrame and a wx.StaticBox draw their
        own frame and put their label where the theme says. Three boxes in
        a row, each holding three blocks, is what has to hold."""
        module = __import__("staticboxsizer")
        self.app = module.App()
        self.app.update_idletasks()

        boxes = self.app.winfo_children()
        self.assertEqual(len(boxes), 3)

        for box in boxes:
            self.assertEqual(len(box.winfo_children()), 3)

    def test_realworld_spaces_its_buttons_evenly(self):
        """The three empty columns with a weight are the wx spacers. If a
        weight is missed the buttons slide to one side."""
        module = __import__("realworld")
        self.app = module.App()
        self.app.geometry("430x300")
        self.app.update_idletasks()

        frames = [w for w in self.app.winfo_children()
                  if w.winfo_class() == "TFrame"]
        buttons = frames[-1].winfo_children()

        self.assertEqual(len(buttons), 2)

        left = buttons[0].winfo_x()
        gap = buttons[1].winfo_x() - (buttons[0].winfo_x()
                                      + buttons[0].winfo_width())
        right = (frames[-1].winfo_width()
                 - (buttons[1].winfo_x() + buttons[1].winfo_width()))

        self.assertEqual(left, right)
        self.assertEqual(left, gap)


if __name__ == "__main__":
    unittest.main()
