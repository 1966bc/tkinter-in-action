#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  18.5 - How do I do something every so often?
# source:   wxPythonInAction-src/Chapter-18/timer.py
# -----------------------------------------------------------------------------
"""A clock that ticks, and can be started and stopped.

wx.Timer is an object. It is made, it is bound to EVT_TIMER, it is
started with an interval and it keeps going until it is stopped.

after() is not an object and does not keep going. It runs something once,
after so many milliseconds, and hands back a name the thing can be
cancelled by. To repeat, the handler asks for the next one - which makes
the repetition visible in the code, and makes it possible to forget.
"""
import time
import tkinter as tk


MILLISECONDS = 1000


class App(tk.Tk):
    """A window with a clock in it."""

    def __init__(self):
        super().__init__()

        self.title("Timer")
        self.geometry("360x160")

        # What after() gave back last, or None when nothing is pending.
        self.tick = None
        self.count = 0

        self.lbl_time = tk.Label(self, font=("TkDefaultFont", 20))
        self.lbl_time.pack(expand=True)

        self.lbl_count = tk.Label(self, text="Ticks: 0")
        self.lbl_count.pack()

        frm_buttons = tk.Frame(self)
        frm_buttons.pack(pady=10)

        self.btn_start = tk.Button(frm_buttons, text="Start",
                                   command=self.on_start)
        self.btn_start.pack(side=tk.LEFT, padx=5)

        self.btn_stop = tk.Button(frm_buttons, text="Stop",
                                  command=self.on_stop, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5)

        self.on_tick(count=False)
        self.on_start()

    def on_tick(self, count=True):
        """Show the time, and ask to be called again.

        The asking is at the end, not the beginning: a handler that
        re-arms first and then raises leaves a timer running against a
        window that is in a state nobody planned.
        """
        self.lbl_time.config(text=time.strftime("%H:%M:%S"))

        if count:
            self.count = self.count + 1
            self.lbl_count.config(text="Ticks: {}".format(self.count))

        if self.tick is not None or count:
            self.tick = self.after(MILLISECONDS, self.on_tick)

    def on_start(self):
        """Start ticking, if it is not already."""
        if self.tick is None:
            self.tick = self.after(MILLISECONDS, self.on_tick)
            self.btn_start.config(state=tk.DISABLED)
            self.btn_stop.config(state=tk.NORMAL)

    def on_stop(self):
        """Stop. after_cancel is wx.Timer.Stop, and it must be called."""
        if self.tick is not None:
            self.after_cancel(self.tick)
            self.tick = None
            self.btn_start.config(state=tk.NORMAL)
            self.btn_stop.config(state=tk.DISABLED)

    def destroy(self):
        """A pending after() outlives the window unless it is cancelled."""
        self.on_stop()
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
