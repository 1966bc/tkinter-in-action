#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 2: the pieces that had to be built by hand.

Nothing here has a wx window to be measured against. What is tested is that
the things Tkinter does not come with - a window that catches print(), a
status bar, a toolbar, a list to choose from - are there and do what they
are supposed to.

Run them from the project directory:

    python3 -m unittest discover -s tests -v

One thing to expect. Tk is meant to be one interpreter per process, and
these tests build and destroy one per example. Running the whole suite
prints a Tcl complaint once, when ttk initialises in a new interpreter and
broadcasts a theme change to every interpreter it has seen, including the
ones already destroyed. It is noise, not a failure.
"""
import io
import os
import sys
import tkinter as tk
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "Chapter-02"))


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no windows to build")
class TestChapter02(unittest.TestCase):
    """What wx supplies and Tkinter does not."""

    def setUp(self):
        """Every test builds and destroys its own window.

        The streams are caught first: startup.py prints on purpose, and a
        test run is not where those lines are wanted.
        """
        self.app = None
        self.real_stdout = sys.stdout
        self.real_stderr = sys.stderr

        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        self.stdout = sys.stdout

    def tearDown(self):
        """Put the streams back. startup.py takes them on purpose."""
        sys.stdout = self.real_stdout
        sys.stderr = self.real_stderr

        if self.app is not None:
            self.app.destroy()

    def test_startup_catches_what_is_printed(self):
        """wx.App(redirect=True) is one argument. This is the window it
        would have opened, and the test is that print() reaches it."""
        import startup

        self.app = startup.App(redirect=True)
        self.app.update_idletasks()

        print("into the window")
        print("and the error stream too", file=sys.stderr)

        written = self.app.output.txt_output.get("1.0", tk.END)

        self.assertIn("into the window", written)
        self.assertIn("and the error stream too", written)

    def test_startup_leaves_the_streams_alone_when_not_asked(self):
        """Redirection is a choice, and the default is the terminal."""
        import startup

        self.app = startup.App(redirect=False)

        self.assertIs(sys.stdout, self.stdout)

    def test_insert_has_one_button_that_closes_the_window(self):
        """The wx original binds EVT_BUTTON. A Tk Button is given its
        command when it is made, and binding <Button-1> instead would lose
        the keyboard and the pressed look."""
        import insert

        self.app = insert.App()

        buttons = [w for w in self.app.winfo_children()
                   if w.winfo_class() == "Button"]

        self.assertEqual(len(buttons), 1)
        self.assertNotEqual(buttons[0].cget("command"), "")

    def test_toolbar_has_the_three_pieces_of_furniture(self):
        """A menu, a raised Frame of flat buttons, and a sunken Label. Only
        the first of the three is a thing Tkinter has."""
        import toolbar

        self.app = toolbar.App()
        self.app.update_idletasks()

        self.assertNotEqual(self.app.cget("menu"), "")

        frames = [w for w in self.app.winfo_children()
                  if w.winfo_class() == "Frame"]
        self.assertEqual(len(frames), 1)
        self.assertEqual(str(frames[0].cget("relief")), "raised")
        self.assertEqual(len(frames[0].winfo_children()), 2)

        labels = [w for w in self.app.winfo_children()
                  if w.winfo_class() == "Label"]
        self.assertEqual(len(labels), 1)
        self.assertEqual(str(labels[0].cget("relief")), "sunken")

    def test_toolbar_keeps_its_icons_alive(self):
        """The chapter 1 trap again, twice: a button does not own the
        PhotoImage it shows, and both icons would go blank."""
        import toolbar

        self.app = toolbar.App()

        self.assertEqual(sorted(self.app.images), ["exit", "new"])

    def test_images_carries_the_pngs_of_the_book(self):
        """Sixteen by fifteen, the same bytes the original embeds. Tk reads
        PNG since 8.6, so nothing had to be converted to get it in."""
        import images

        self.app = tk.Tk()
        photo = images.get_new_image()

        self.assertEqual((photo.width(), photo.height()), (16, 15))


if __name__ == "__main__":
    unittest.main()
