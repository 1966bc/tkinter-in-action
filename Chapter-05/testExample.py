#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  5.5 - How do I test a wxPython application?
# source:   wxPythonInAction-src/Chapter-05/testExample.py
# -----------------------------------------------------------------------------
"""The model, tested without pressing anything.

    python3 Chapter-05/testExample.py

The handler is called directly and the model is asked what it holds. No
window has to be looked at, which is the reward for having separated them.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import modelExample


class TestExample(unittest.TestCase):
    """What the buttons do to the model."""

    def setUp(self):
        """A window. It is built but never shown."""
        self.app = modelExample.App()

    def tearDown(self):
        """And taken down, or the next test inherits it."""
        self.app.destroy()

    def test_model(self):
        """The handler is a method and can simply be called. wx passes an
        event that the handler ignores, so the original passes None; a Tk
        command takes no arguments and there is nothing to pass."""
        self.app.on_barney()

        self.assertEqual("Barney", self.app.model.first)
        self.assertEqual("Rubble", self.app.model.last)


if __name__ == "__main__":
    unittest.main()
