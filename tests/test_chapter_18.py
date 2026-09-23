#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 18: the clipboard, a timer, and threads that behave.

The threads test is the one worth having. It waits for real messages to
come back through a real queue, because the failure it guards against -
a worker touching a widget - does not raise and cannot be caught.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import queue
import sys
import time
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
class TestChapter18(unittest.TestCase):
    """The clipboard, the clock and the workers."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-18")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_copy_and_paste_go_through_the_clipboard(self):
        """Three methods, and no opening and closing."""
        import clipboard

        self.app = clipboard.App()
        self.app.update()

        self.app.on_copy()
        self.app.update()
        self.app.on_paste()

        self.assertEqual(self.app.ent_to.get(), self.app.ent_from.get())
        self.assertIn("Pasted", self.app.lbl_said.cget("text"))

    def test_copying_twice_does_not_give_both(self):
        """clipboard_append adds to what is there, so the clear matters."""
        import clipboard

        self.app = clipboard.App()
        self.app.update()

        self.app.on_copy()
        self.app.on_copy()
        self.app.update()

        self.assertEqual(self.app.clipboard_get(), self.app.ent_from.get())

    def test_pasting_nothing_says_so_instead_of_raising(self):
        """clipboard_get raises TclError on an empty clipboard. It does
        not return an empty string, and a Paste button that does not
        catch it is a traceback waiting for a Tuesday."""
        import clipboard

        self.app = clipboard.App()
        self.app.update()
        self.app.clipboard_clear()
        self.app.update()

        self.app.on_paste()

        self.assertIn("Nothing", self.app.lbl_said.cget("text"))

    def test_the_clock_can_be_stopped_and_started(self):
        """wx.Timer is an object that keeps going. after() runs once and
        the handler asks for the next, so stopping is not cancelling a
        timer but declining to ask again."""
        import timer

        self.app = timer.App()
        self.app.update()

        self.assertIsNotNone(self.app.tick)

        self.app.on_stop()
        self.assertIsNone(self.app.tick)
        self.assertEqual(str(self.app.btn_start.cget("state")), "normal")

        self.app.on_start()
        self.assertIsNotNone(self.app.tick)

    def test_the_clock_stops_with_the_window(self):
        """Or a pending callback fires at a window that is not there."""
        import timer

        self.app = timer.App()
        self.app.update()
        self.app.destroy()

        self.assertIsNone(self.app.tick)
        self.app = None

    def test_a_worker_reports_through_the_queue_and_not_the_widget(self):
        """The rule that is not negotiable. The worker is given a queue
        and nothing else: it has no way to reach a widget even if it
        wanted to, which is the point of the arrangement."""
        import worker_threads

        messages = queue.Queue()
        worker = worker_threads.Worker(1, messages)

        self.assertFalse(hasattr(worker, "window"))

        worker.start()

        kind, payload = messages.get(timeout=5)

        self.assertEqual(kind, "log")
        self.assertIn("Thread 1", payload)

        worker.stop()
        worker.join(timeout=5)

        self.assertFalse(worker.is_alive())

    def test_the_window_drains_the_queue_when_it_polls(self):
        """wx.CallAfter turned inside out: the worker leaves a message
        and the main thread comes to fetch it."""
        import worker_threads

        self.app = worker_threads.App()
        self.app.update()

        self.app.messages.put(("log", "a line from somewhere else"))
        self.app.messages.put(("log", "and another"))

        self.app.on_poll()

        written = self.app.txt_log.get("1.0", tk.END)

        self.assertIn("a line from somewhere else", written)
        self.assertIn("and another", written)
        self.assertTrue(self.app.messages.empty())

    def test_a_worker_is_asked_to_stop_and_not_killed(self):
        """A thread cannot be stopped from outside in Python and should
        not be: it might be halfway through writing a file."""
        import worker_threads

        self.app = worker_threads.App()
        self.app.update()

        self.app.on_start()
        self.app.on_start()

        self.assertEqual(len(self.app.workers), 2)
        self.assertTrue(all(worker.wanted for worker in self.app.workers))

        self.app.on_stop()

        self.assertTrue(all(not worker.wanted for worker in self.app.workers))

        for worker in self.app.workers:
            worker.join(timeout=5)
            self.assertFalse(worker.is_alive())


if __name__ == "__main__":
    unittest.main()
