#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 8: windows, and the three things that are not there.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import sys
import tkinter as tk
import unittest

import chapter

HERE = chapter.ROOT

EXAMPLES = ("frame_subclass", "help_context", "mdi", "miniframe",
            "scroll_window", "shaped_frame", "shaped_frame_mobile",
            "splitter")


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no windows to build")
class TestChapter08(unittest.TestCase):
    """What a window can be asked for, and what it cannot."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-08")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_every_example_builds(self):
        """Eight windows, one at a time."""
        for name in EXAMPLES:
            module = __import__(name)
            app = module.App()
            app.update_idletasks()
            app.destroy()

    def test_a_window_cannot_be_given_a_shape(self):
        """The reason shaped_frame.py is not a shaped frame. If this ever
        fails, Tk has grown something and the chapter is out of date."""
        self.app = tk.Tk()

        self.assertRaises(tk.TclError, self.app.attributes,
                          "-transparentcolor", "white")

        offered = self.app.attributes()[::2]
        self.assertNotIn("-shape", offered)
        self.assertIn("-alpha", offered)

    def test_the_bare_window_has_no_decorations(self):
        """overrideredirect is the half of FRAME_SHAPED that does work,
        and double clicking puts the title bar back."""
        import shaped_frame

        self.app = shaped_frame.App()
        self.app.update()

        self.assertTrue(self.app.overrideredirect())

        self.app.on_double_click(None)
        self.assertFalse(self.app.overrideredirect())

    def test_dragging_a_bare_window_moves_it(self):
        """A window with no title bar cannot be moved, so the moving is
        written. The offset is what stops it jumping."""
        import shaped_frame_mobile

        self.app = shaped_frame_mobile.App()
        self.app.update()

        event = tk.Event()
        event.x = 40
        event.y = 25
        self.app.on_left_down(event)

        self.assertEqual(self.app.offset, (40, 25))

    def test_the_scrolled_window_is_three_widgets(self):
        """wx.ScrolledWindow is one class. This is a Canvas holding a
        Frame as a canvas item, because a Frame cannot scroll."""
        import scroll_window

        self.app = scroll_window.App()
        self.app.update()

        scroll = self.app.scroll

        self.assertIsInstance(scroll.canvas, tk.Canvas)
        self.assertIsInstance(scroll.inner, tk.Frame)
        self.assertEqual(len(scroll.canvas.find_all()), 1)

        region = scroll.canvas.cget("scrollregion").split()
        self.assertEqual(region[2:], [str(scroll_window.INNER_WIDTH),
                                      str(scroll_window.INNER_HEIGHT)])

    def test_scrolling_moves_the_view(self):
        """wx.Scroll takes pixels, xview_moveto takes a fraction, and the
        arithmetic between them is the part that can be wrong."""
        import scroll_window

        self.app = scroll_window.App()
        self.app.update()

        before = self.app.scroll.canvas.xview()[0]

        self.app.on_click_top()
        self.app.update()
        moved = self.app.scroll.canvas.xview()[0]

        self.app.on_click_bottom()
        self.app.update()
        back = self.app.scroll.canvas.xview()[0]

        self.assertGreater(moved, before)
        self.assertEqual(back, 0.0)

    def test_mdi_children_are_tabs(self):
        """Because there is no way to put a window inside a window."""
        import mdi

        self.app = mdi.App()
        self.app.update()

        self.assertEqual(len(self.app.notebook.tabs()), 0)

        self.app.on_new_window()
        self.app.on_new_window()

        self.assertEqual(len(self.app.notebook.tabs()), 2)

    def test_the_splitter_is_remade_to_turn_it(self):
        """A ttk.PanedWindow is given its orientation when it is made.
        wx turns the same object; here there is a new one."""
        import splitter

        self.app = splitter.App()
        self.app.update()

        self.assertEqual(str(self.app.paned.cget("orient")), "horizontal")

        self.app.on_split_h()
        self.app.update()

        self.assertEqual(str(self.app.paned.cget("orient")), "vertical")
        self.assertEqual(len(self.app.paned.panes()), 2)

        self.app.on_unsplit()
        self.app.update()

        self.assertEqual(len(self.app.paned.panes()), 1)


if __name__ == "__main__":
    unittest.main()
