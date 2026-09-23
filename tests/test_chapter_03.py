#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 3: events, which are hard to look at and easy to test.

An event either arrives or it does not, so this is the chapter where a test
says more than a screenshot would.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import sys
import tkinter as tk
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "Chapter-03"))


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no events to raise")
class TestChapter03(unittest.TestCase):
    """What arrives, what does not, and what it brings with it."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_custom_event_reaches_the_window(self):
        """Raised on the panel, bound on the window. It gets there because
        the toplevel is one of the panel's bindtags, which is Tk's answer
        to wx propagating a command event up the chain."""
        import customEvent

        self.app = customEvent.App()
        self.app.update()

        for button in self.app.panel.winfo_children():
            button.invoke()

        self.app.update()

        self.assertEqual(self.app.title(), "Click Count: 2")

    def test_custom_event_needs_both_buttons(self):
        """One button is half an event. The original counts every click and
        raises on every pair, and so does this."""
        import customEvent

        self.app = customEvent.App()
        self.app.update()

        self.app.panel.winfo_children()[0].invoke()
        self.app.update()

        self.assertEqual(self.app.title(), "Click Count: 0")

    def test_a_virtual_event_carries_nothing(self):
        """The chapter's one real loss. Tcl has had a data field on virtual
        events since 8.5 and event_generate accepts it, but Tkinter never
        asks for it: %d is not in Event._subst_format, so event.data cannot
        exist. If this test ever fails, Tkinter has gained something and
        the chapter needs rewriting."""
        self.app = tk.Tk()
        self.app.update()

        seen = []
        self.app.bind("<<Carrier>>", lambda event: seen.append(event))
        self.app.event_generate("<<Carrier>>", data="forty-two")
        self.app.update()

        self.assertEqual(len(seen), 1)
        self.assertFalse(hasattr(seen[0], "data"))

    def test_an_event_on_an_unmapped_widget_is_lost(self):
        """Silently, which is the part that costs an evening. The same
        generate works once the window has been through an update()."""
        self.app = tk.Tk()

        frame = tk.Frame(self.app, width=80, height=40)
        frame.pack()

        seen = []
        self.app.bind("<<Early>>", lambda event: seen.append(event))

        frame.event_generate("<<Early>>")
        self.app.update()
        self.assertEqual(seen, [])

        frame.event_generate("<<Early>>")
        self.app.update()
        self.assertEqual(len(seen), 1)

    def test_break_stops_a_button_from_being_pressed(self):
        """wx keeps going only if a handler calls event.Skip(). Tkinter
        keeps going unless a handler returns "break", and this is the one
        place the difference can be seen rather than described."""
        self.app = tk.Tk()
        log = []

        button = tk.Button(self.app, text="x",
                           command=lambda: log.append("command"))
        button.pack()
        button.bind("<Button-1>", lambda event: log.append("press") or "break")
        self.app.update()

        button.event_generate("<Button-1>", x=5, y=5)
        button.event_generate("<ButtonRelease-1>", x=5, y=5)
        self.app.update()

        self.assertEqual(log, ["press"])

    def test_mouse_event_follows_the_pointer(self):
        """<Enter> and <Leave> are EVT_ENTER_WINDOW and EVT_LEAVE_WINDOW,
        and this is the most direct translation in the book."""
        import mouse_event

        self.app = mouse_event.App()
        self.app.update()

        self.assertEqual(self.app.btn_over.cget("text"), mouse_event.AWAY)

        self.app.btn_over.event_generate("<Enter>")
        self.app.update()
        self.assertEqual(self.app.btn_over.cget("text"), mouse_event.OVER)

        self.app.btn_over.event_generate("<Leave>")
        self.app.update()
        self.assertEqual(self.app.btn_over.cget("text"), mouse_event.AWAY)


if __name__ == "__main__":
    unittest.main()
