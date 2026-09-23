#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 4: a shell that has to actually run things.

The shell is the one thing in this book that can be wrong in a way nobody
notices until it matters, so it is tested by using it: statements are
pushed at it and what comes back is read out of the Text.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import importlib.util
import os
import sys
import tkinter as tk
import unittest

import chapter

HERE = chapter.ROOT
CHAPTER = os.path.join(HERE, "Chapter-04")


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


def get_module(name, path):
    """Load a file whose name Python would not accept as a module name."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


@unittest.skipUnless(has_display(), "no display, no windows to build")
class TestChapter04(unittest.TestCase):
    """The shell, the namespace tree, and the wrapper."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-04")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def get_shell(self, namespace):
        """A shell window over a namespace, with a root to hang it on."""
        pywrap = get_module("pywrap", os.path.join(CHAPTER, "PyWrap.py"))
        self.app = tk.Tk()

        return pywrap.ShellWindow(self.app, namespace)

    def say(self, shell, source):
        """Type a line at the shell and press return."""
        shell.txt_shell.insert(tk.END, source)
        shell.on_return(None)

        return shell.txt_shell.get("1.0", tk.END)

    def test_the_shell_evaluates(self):
        """code.InteractiveConsole does the language; what is tested is
        that the answer finds its way back into the Text."""
        shell = self.get_shell({})

        self.assertIn("2", self.say(shell, "1 + 1"))

    def test_the_shell_keeps_state_between_lines(self):
        """A shell that forgets is not a shell."""
        shell = self.get_shell({})

        self.say(shell, "x = 21")

        self.assertIn("42", self.say(shell, "x * 2"))

    def test_the_shell_shows_an_error_instead_of_raising_it(self):
        """A traceback in the window, and the program still running. This
        is what InteractiveConsole is for and it would be easy to lose by
        catching the wrong thing."""
        shell = self.get_shell({})

        written = self.say(shell, "1/0")

        self.assertIn("ZeroDivisionError", written)

    def test_the_shell_reaches_the_running_window(self):
        """The point of the chapter. Not a shell on the desktop: a shell
        holding the window that is open."""
        shell = self.get_shell({})
        shell.console.locals["app"] = self.app

        self.say(shell, "app.title('changed from the shell')")
        self.app.update()

        self.assertEqual(self.app.title(), "changed from the shell")

    def test_pywrap_finds_the_window_class(self):
        """wx looks for a wx.App because an application is not a window.
        Here they are one thing, so it looks for the tk.Tk subclass."""
        pywrap = get_module("pywrap", os.path.join(CHAPTER, "PyWrap.py"))

        for name in ("Chapter-01/spare.py", "Chapter-02/toolbar.py",
                     "Chapter-03/customEvent.py"):
            module = pywrap.get_module(os.path.join(HERE, name))
            found = pywrap.get_window_class(module)

            self.assertIsNotNone(found, name)
            self.assertTrue(issubclass(found, tk.Tk), name)
            self.assertIsNot(found, tk.Tk, name)

    def test_the_namespace_tree_fills_a_branch_when_it_is_opened(self):
        """Filled a level at a time on <<TreeviewOpen>>, because walking a
        namespace all at once is how a window comes up after five seconds
        instead of at once."""
        foundation = get_module(
            "pycrust_foundation",
            os.path.join(CHAPTER, "pycrust-foundation.py"))

        self.app = tk.Tk()
        names = foundation.NamespaceWindow(self.app, {"thing": self.app})
        self.app.update()

        node = names.trv_names.get_children()[0]
        children = names.trv_names.get_children(node)

        self.assertEqual(len(children), 1)
        self.assertEqual(names.trv_names.item(children[0], "text"), "")

        names.trv_names.focus(node)
        names.on_open(None)

        self.assertGreater(len(names.trv_names.get_children(node)), 1)


if __name__ == "__main__":
    unittest.main()
