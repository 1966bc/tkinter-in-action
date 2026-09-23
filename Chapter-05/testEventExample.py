#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  5.5 - How do I test the event handling?
# source:   wxPythonInAction-src/Chapter-05/testEventExample.py
# -----------------------------------------------------------------------------
"""The same, but by pressing the button instead of calling the handler.

    python3 Chapter-05/testEventExample.py

This is the one the book works hardest for, and the one Tkinter makes
shortest. See README.md.
"""
import os
import sys
import tkinter as tk
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import modelExample


class TestEventExample(unittest.TestCase):
    """What the buttons do when they are pressed rather than called."""

    def setUp(self):
        """A window, built and left unshown."""
        self.app = modelExample.App()

    def tearDown(self):
        """And taken down."""
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

    def test_model(self):
        """Calling the handler, as in testExample.py."""
        self.app.on_barney()

        self.assertEqual("Barney", self.app.model.first)

    def test_event(self):
        """Pressing the button.

        The wx original has to build a wx.CommandEvent of the right type,
        give it the button's id, and hand it to the button's event handler
        with ProcessEvent. A Tk Button has invoke(), which runs its command
        exactly as a press would, and that is the whole of it.
        """
        self.get_button("Wilmafy").invoke()

        self.assertEqual("Wilma", self.app.model.first)
        self.assertEqual("Flintstone", self.app.model.last)

    def test_the_fields_followed(self):
        """Not in the original, and the reason the pattern is worth having:
        nothing wrote to the fields. The button set the model, the model
        said so, and the window read it back."""
        self.get_button("Bettify").invoke()
        self.app.update()

        self.assertEqual(self.app.entries["First Name"].get(), "Betty")
        self.assertEqual(self.app.entries["Last Name"].get(), "Rubble")


if __name__ == "__main__":
    unittest.main()
