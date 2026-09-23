#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 9: dialogs, which are modal and therefore hard to test.

A modal dialog waits for somebody, so almost nothing here opens one. What
is tested is the parts that can be: the rules, the counting, the tips
file, and the font chooser that Tkinter does not admit to having.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import sys
import tkinter as tk
import unittest

import chapter

HERE = chapter.ROOT


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no dialogs to build")
class TestChapter09(unittest.TestCase):
    """The pieces of the dialogs that do not need somebody present."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-09")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_tk_has_a_font_chooser(self):
        """Which Python does not wrap and the internet says does not
        exist. If Tk ever loses it, font_box.py stops working and this
        says so first."""
        self.app = tk.Tk()
        self.app.update()

        options = self.app.tk.call("tk", "fontchooser", "configure")
        names = [str(option) for option in options[::2]]

        self.assertIn("-command", names)
        self.assertIn("-visible", names)

    def test_a_rule_refuses_an_edit_instead_of_undoing_it(self):
        """wx binds EVT_CHAR and decides whether to pass it on.
        validatecommand is asked before the edit happens, and a refusal
        leaves the field exactly as it was."""
        import validator3

        self.app = tk.Tk()

        dialog = validator3.MyDialog.__new__(validator3.MyDialog)
        dialog.entries = {}
        dialog.register = self.app.register
        dialog.body(tk.Frame(self.app))

        phone = dialog.entries["Phone"]

        phone.insert(0, "06")
        self.assertEqual(phone.get(), "06")

        phone.insert(tk.END, "a")
        self.assertEqual(phone.get(), "06")

        name = dialog.entries["Name"]
        name.insert(0, "Rossi")
        name.insert(tk.END, "7")
        self.assertEqual(name.get(), "Rossi")

    def test_the_free_field_takes_anything(self):
        """The middle one has no rule, and must not have inherited one."""
        import validator3

        self.app = tk.Tk()

        dialog = validator3.MyDialog.__new__(validator3.MyDialog)
        dialog.entries = {}
        dialog.register = self.app.register
        dialog.body(tk.Frame(self.app))

        email = dialog.entries["Email"]
        email.insert(0, "a.b@c.it 42")

        self.assertEqual(email.get(), "a.b@c.it 42")

    def test_the_progress_box_counts_and_stops(self):
        """The bar is not the point. The point is that the work is cut
        into pieces so that Cancel can be pressed between them."""
        import progress_box

        self.app = tk.Tk()
        self.app.withdraw()

        box = progress_box.ProgressBox(self.app, "t", "m", 100)

        self.assertTrue(box.update_to(10))
        self.assertEqual(box.count, 10)

        box.on_cancel()

        self.assertFalse(box.update_to(11))

    def test_the_progress_box_shows_both_clocks(self):
        """PD_ELAPSED_TIME and PD_REMAINING_TIME, which wx gets as flags
        and this has to work out."""
        import progress_box

        self.app = tk.Tk()
        self.app.withdraw()

        box = progress_box.ProgressBox(self.app, "t", "m", 100)
        box.update_to(50)

        self.assertIn("Elapsed time:", box.lbl_elapsed.cget("text"))
        self.assertIn("remaining", box.lbl_remaining.cget("text"))
        self.assertEqual(box.get_clock(0), "00:00")
        self.assertEqual(box.get_clock(61), "01:01")

    def test_the_tips_file_is_read_and_the_answer_is_kept(self):
        """The answer to "show these at startup" goes in a file, because
        a program that asks again every morning has saved nobody
        anything."""
        import startup_tip

        tips = startup_tip.get_tips(startup_tip.TIPS)

        self.assertGreater(len(tips), 3)
        self.assertFalse(any(tip.startswith("#") for tip in tips))

        self.assertTrue(startup_tip.get_showing("/nowhere/at/all"))

    def test_the_wizard_walks_its_pages(self):
        """Back is off on the first page and Next becomes Finish on the
        last, which is the whole of what a wizard is."""
        import wizard

        self.app = tk.Tk()
        self.app.withdraw()

        walker = wizard.Wizard(self.app, "t")

        for number in range(1, 4):
            walker.add_page(wizard.TitledPage(walker.frm_pages,
                                              "Page {}".format(number)))

        walker.show_page()
        self.assertEqual(str(walker.btn_back.cget("state")), "disabled")
        self.assertEqual(walker.btn_next.cget("text"), "Next >")

        walker.on_next()
        self.assertEqual(str(walker.btn_back.cget("state")), "normal")

        walker.on_next()
        self.assertEqual(walker.btn_next.cget("text"), "Finish")

        walker.destroy()


if __name__ == "__main__":
    unittest.main()
