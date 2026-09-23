#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 13: a list of rows, and the sort that looks right and is not.

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


@unittest.skipUnless(has_display(), "no display, no list to show")
class TestChapter13(unittest.TestCase):
    """What the Treeview holds, and in what order."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-13")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def get_show(self, tree):
        """What "show" says, which Tk hands back as a list of words."""
        return [str(word) for word in tree.cget("show")]

    def test_the_rows_are_all_there(self):
        """And the tree column is hidden, which is the commonest thing
        wrong with a Tkinter table."""
        import data
        import list_report

        self.app = list_report.App()
        self.app.update()

        self.assertEqual(len(self.app.trv_rows.get_children("")),
                         len(data.ROWS))
        self.assertIn("headings", self.get_show(self.app.trv_rows))

    def test_numbers_sort_as_numbers(self):
        """The bug this file exists to avoid. Everything in a Treeview is
        text, and as text 10 comes before 9 - and the list looks sorted,
        which is what makes it expensive."""
        import list_report_colsort

        self.app = list_report_colsort.App()
        self.app.update()

        self.app.on_heading("Request ID")

        found = [self.app.trv_rows.set(item, "Request ID")
                 for item in self.app.trv_rows.get_children("")]

        self.assertEqual([int(each) for each in found],
                         sorted(int(each) for each in found))
        self.assertNotEqual(found, sorted(found))

    def test_clicking_twice_reverses(self):
        """And the arrow follows the column that is sorted."""
        import list_report_colsort

        self.app = list_report_colsort.App()
        self.app.update()

        self.app.on_heading("Summary")
        first = self.app.trv_rows.set(
            self.app.trv_rows.get_children("")[0], "Summary")

        self.app.on_heading("Summary")
        last = self.app.trv_rows.set(
            self.app.trv_rows.get_children("")[0], "Summary")

        self.assertNotEqual(first, last)
        self.assertTrue(self.app.trv_rows.heading("Summary")["text"]
                        .startswith("Summary"))
        self.assertNotEqual(self.app.trv_rows.heading("Summary")["text"],
                            "Summary")

    def test_sorting_moves_rows_rather_than_rebuilding_them(self):
        """move() keeps the items, so a selection survives a sort."""
        import list_report_colsort

        self.app = list_report_colsort.App()
        self.app.update()

        items = self.app.trv_rows.get_children("")
        self.app.trv_rows.selection_set(items[3])
        chosen = self.app.trv_rows.set(items[3], "Request ID")

        self.app.on_heading("Date")

        self.assertEqual(len(self.app.trv_rows.selection()), 1)
        self.assertEqual(
            self.app.trv_rows.set(self.app.trv_rows.selection()[0],
                                  "Request ID"), chosen)

    def test_the_options_the_style_flags_become(self):
        """LC_NO_HEADER and LC_SINGLE_SEL are options that can be
        changed while the window is open, which flags cannot."""
        import list_report_etc

        self.app = list_report_etc.App()
        self.app.update()

        self.app.headings.set(False)
        self.app.on_headings()
        self.assertNotIn("headings", self.get_show(self.app.trv_rows))

        self.app.many.set(True)
        self.app.on_many()
        self.assertEqual(str(self.app.trv_rows.cget("selectmode")),
                         "extended")

    def test_stripes_are_a_tag_and_not_rules(self):
        """Which is better than the rules wx offers: the same mechanism
        marks a row red because its control failed."""
        import list_report_etc

        self.app = list_report_etc.App()
        self.app.update()

        self.app.striped.set(True)
        self.app.on_striped()

        items = self.app.trv_rows.get_children("")

        self.assertEqual(self.app.trv_rows.item(items[0], "tags"), "")
        self.assertIn("odd", self.app.trv_rows.item(items[1], "tags"))

    def test_selection_is_asked_for_rather_than_announced(self):
        """wx says which item was selected and which was deselected. Tk
        raises one event and the widget is asked what is selected now."""
        import list_report_etc

        self.app = list_report_etc.App()
        self.app.update()

        items = self.app.trv_rows.get_children("")
        self.app.trv_rows.selection_set(items[2])
        self.app.on_item_selected(None)

        self.assertIn("Selected:", self.app.lbl_said.cget("text"))

        self.app.on_item_activated(None)
        self.assertIn("Activated:", self.app.lbl_said.cget("text"))


if __name__ == "__main__":
    unittest.main()
