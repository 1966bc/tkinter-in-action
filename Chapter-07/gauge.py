#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.5 - How do I show progress?
# source:   wxPythonInAction-src/Chapter-07/gauge.py
# -----------------------------------------------------------------------------
"""A bar that fills up and starts again.

The widget translates straight across. What does not is how it is driven:
wx counts on EVT_IDLE, and Tkinter has no idle event of that kind.
"""
import tkinter as tk
from tkinter import ttk


MAXIMUM = 50

# How often to move it on. The wx original uses EVT_IDLE, which fires
# whenever the event loop has nothing else to do - that is as fast as the
# machine allows, and on a fast one the bar is a blur. after() says how
# fast in so many words.
MILLISECONDS = 40


class App(tk.Tk):
    """A progress bar that fills and starts again."""

    def __init__(self):
        super().__init__()

        self.title("Gauge Example")
        self.geometry("350x150")

        self.count = 0

        # What after() gives back, so that it can be taken away again.
        self.tick = None

        self.pgb_count = ttk.Progressbar(self, maximum=MAXIMUM,
                                         mode="determinate")
        self.pgb_count.place(x=20, y=50, width=250, height=25)

        self.on_tick()

    def on_tick(self):
        """One step, and ask to be called again.

        after() is the whole of Tkinter's timing. There is also
        after_idle(), which is closer to EVT_IDLE and is for work that must
        happen before the screen is next drawn, not for animation.
        """
        self.count = self.count + 1

        if self.count >= MAXIMUM:
            self.count = 0

        self.pgb_count.config(value=self.count)
        self.tick = self.after(MILLISECONDS, self.on_tick)

    def destroy(self):
        """Stop the clock before going away.

        A repeating after() outlives the window that asked for it. The
        callback then fires at a widget that is not there any more and Tk
        says "invalid command name", from inside its own event loop, with
        no traceback worth reading. Every repeating after() needs an
        after_cancel somewhere.
        """
        if self.tick is not None:
            self.after_cancel(self.tick)
            self.tick = None

        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
