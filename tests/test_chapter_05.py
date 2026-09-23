#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 5: the chapter that tests itself.

Two of the book's own files are unit tests, and they run. What is here is
what they do not cover: that the window never writes to itself, and that a
StringVar really would have done the simple half of the job.

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


@unittest.skipUnless(has_display(), "no display, no windows to build")
class TestChapter05(unittest.TestCase):
    """The model, the listeners, and what the book's own tests leave out."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-05")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def get_button(self, label):
        """The button with that text, wherever it is in the window."""
        found = None

        for panel in self.app.winfo_children():
            for widget in panel.winfo_children():
                if widget.winfo_class() == "Button":
                    if widget.cget("text") == label:
                        found = widget

        return found

    def test_the_model_tells_and_the_window_reads(self):
        """Nothing in the handler touches a widget. The fields fill because
        the model said it had changed, which is the whole chapter."""
        import modelExample

        self.app = modelExample.App()
        self.app.update()

        self.get_button("Fredify").invoke()
        self.app.update()

        self.assertEqual(self.app.entries["First Name"].get(), "Fred")
        self.assertEqual(self.app.entries["Last Name"].get(), "Flintstone")

    def test_a_listener_can_stop_listening(self):
        """A window that is destroyed while still on the model's list is a
        model calling a dead widget. on_close_window removes it first."""
        import modelExample

        self.app = modelExample.App()
        before = len(self.app.model.listeners)

        self.app.model.remove_listener(self.app.on_update)

        self.assertEqual(len(self.app.model.listeners), before - 1)

    def test_the_model_speaks_once_for_both_names(self):
        """Why a model and not two StringVars. set() changes first and last
        and calls update() once, so nobody ever sees the new first name
        beside the old last one."""
        import abstractmodel
        import modelExample

        heard = []
        model = modelExample.SimpleName()
        model.add_listener(lambda each: heard.append((each.first, each.last)))

        model.set("Wilma", "Flintstone")

        self.assertEqual(heard, [("Wilma", "Flintstone")])

    def test_a_stringvar_is_the_observer_tkinter_already_has(self):
        """What the book has to build, for a single value. Two widgets stay
        in step with no code between them."""
        self.app = tk.Tk()
        heard = []

        name = tk.StringVar()
        name.trace_add("write", lambda *args: heard.append(name.get()))

        lbl_name = tk.Label(self.app, textvariable=name)
        ent_name = tk.Entry(self.app, textvariable=name)

        name.set("Barney")
        self.app.update()

        self.assertEqual(heard, ["Barney"])
        self.assertEqual(lbl_name.cget("text"), "Barney")
        self.assertEqual(ent_name.get(), "Barney")

    def test_the_line_up_shows_nine_rows(self):
        """gridNoModel is a Treeview, which shows rows and columns and is
        not a grid: nothing in it can be typed into."""
        import gridNoModel

        self.app = gridNoModel.App()
        self.app.update()

        rows = self.app.trv_line_up.get_children()

        self.assertEqual(len(rows), 9)
        self.assertEqual(self.app.trv_line_up.item(rows[0], "text"), "CF")
        self.assertEqual(self.app.trv_line_up.item(rows[0], "values"),
                         ("Bob", "Dernier"))


if __name__ == "__main__":
    unittest.main()
