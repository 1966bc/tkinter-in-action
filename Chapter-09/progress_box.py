#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.4 - How do I show progress?
# source:   wxPythonInAction-src/Chapter-09/progress_box.py
# -----------------------------------------------------------------------------
"""A box that counts to a hundred and can be stopped.

wx.ProgressDialog is a class with flags: PD_CAN_ABORT for the button,
PD_ELAPSED_TIME and PD_REMAINING_TIME for the two clocks. Tkinter has none
of it, so here it is, and the interesting part is not the bar.

The wx original counts in a loop with wx.Sleep(1) in it, which works
because wx.Sleep lets the event loop run. Tkinter has no such thing:
time.sleep in a handler stops everything, the window stops redrawing and
the Cancel button cannot be pressed. The work has to be cut into pieces
and handed back to the event loop with after(). See README.md.
"""
import time
import tkinter as tk
from tkinter import ttk


MAXIMUM = 100

# A tenth of a second a step, so that the whole thing takes ten seconds
# instead of the original's hundred.
MILLISECONDS = 100


class ProgressBox(tk.Toplevel):
    """What wx.ProgressDialog is, in the parts Tkinter has."""

    def __init__(self, parent, title, message, maximum):
        super().__init__(parent)

        self.title(title)
        self.geometry("360x150")
        self.transient(parent)
        self.resizable(False, False)

        self.maximum = maximum
        self.count = 0
        self.started = time.monotonic()
        self.cancelled = False
        self.tick = None

        lbl_message = tk.Label(self, text=message)
        lbl_message.pack(pady=(15, 5))

        self.pgb_count = ttk.Progressbar(self, maximum=maximum, length=300)
        self.pgb_count.pack(pady=5)

        self.lbl_elapsed = tk.Label(self, text="")
        self.lbl_elapsed.pack()

        self.lbl_remaining = tk.Label(self, text="")
        self.lbl_remaining.pack()

        self.btn_cancel = tk.Button(self, text="Cancel",
                                    command=self.on_cancel)
        self.btn_cancel.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)

    def update_to(self, count):
        """Move the bar and both clocks. True unless Cancel was pressed."""
        self.count = count
        self.pgb_count.config(value=count)

        elapsed = time.monotonic() - self.started
        self.lbl_elapsed.config(text="Elapsed time: {}".format(
            self.get_clock(elapsed)))

        remaining = 0.0

        if count:
            remaining = elapsed * (self.maximum - count) / count

        self.lbl_remaining.config(text="Estimated remaining time: {}".format(
            self.get_clock(remaining)))

        return not self.cancelled

    def get_clock(self, seconds):
        """Seconds as minutes and seconds, which is what wx shows."""
        return "{:02d}:{:02d}".format(int(seconds) // 60, int(seconds) % 60)

    def on_cancel(self):
        """Say so. Whoever is counting notices and stops."""
        self.cancelled = True
        self.btn_cancel.config(state=tk.DISABLED, text="Cancelling...")


class App(tk.Tk):
    """A window that counts, in pieces, so that the box stays alive."""

    def __init__(self):
        super().__init__()

        self.withdraw()

        self.box = ProgressBox(self, "A progress box", "Time remaining",
                               MAXIMUM)
        self.count = 0

        self.after(MILLISECONDS, self.on_step)

    def on_step(self):
        """One step of the work, and then back to the event loop.

        This is the shape of every long job in Tkinter: do a little, ask
        to be called again, and let the window breathe in between.
        """
        self.count = self.count + 1
        keep_going = self.box.update_to(self.count)

        if keep_going and self.count < MAXIMUM:
            self.after(MILLISECONDS, self.on_step)
        else:
            self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
