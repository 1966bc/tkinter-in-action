#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  18.6 - How do I write a multithreaded application?
# source:   wxPythonInAction-src/Chapter-18/worker_threads.py
# -----------------------------------------------------------------------------
"""Work done off the main thread, reported back to the window safely.

The rule is the same in both toolkits and it is absolute: **only the
thread that made the widgets may touch them**. A worker thread that calls
insert() on a Text does not raise; it corrupts the interpreter's state,
and the program falls over later, somewhere else, in a way that cannot be
read backwards.

wx has wx.CallAfter, which takes a function and arranges for the main
thread to call it. Tkinter has no such thing, and what everybody uses
instead is a queue: the workers put messages in it, and the main thread
looks in it every so often with after(). See README.md.
"""
import queue
import random
import threading
import time
import tkinter as tk


# How often the window looks in the queue. Short enough to feel immediate,
# long enough not to be busy work.
MILLISECONDS = 100


class Worker(threading.Thread):
    """A thread that counts slowly and says so.

    It touches no widget. Everything it has to say goes in the queue, and
    the window reads it when it is ready.
    """

    def __init__(self, number, messages):
        super().__init__(daemon=True)

        self.number = number
        self.messages = messages
        self.wanted = True

    def stop(self):
        """Ask it to finish. It notices between one step and the next."""
        self.wanted = False

    def run(self):
        """The work. Nothing here knows what a window is."""
        times = random.randint(5, 12)
        delay = random.uniform(0.3, 1.2)

        self.messages.put(("log", "Thread {} starting: {} steps, {:.2f}s "
                                  "apart".format(self.number, times, delay)))

        step = 0

        while self.wanted and step < times:
            step = step + 1
            time.sleep(delay)

            if self.wanted:
                self.messages.put(("log", "Thread {} step {} of {}".format(
                    self.number, step, times)))

        self.messages.put(("done", self.number))


class App(tk.Tk):
    """A window that starts workers and shows what they say."""

    def __init__(self):
        super().__init__()

        self.title("Worker Threads")
        self.geometry("560x420")

        self.messages = queue.Queue()
        self.workers = []
        self.count = 0
        self.tick = None

        self.lbl_count = tk.Label(self, text="Worker threads: 0",
                                  font=("TkDefaultFont", 12, "bold"))
        self.lbl_count.pack(pady=10)

        frm_buttons = tk.Frame(self)
        frm_buttons.pack()

        btn_start = tk.Button(frm_buttons, text="Start a worker",
                              command=self.on_start)
        btn_start.pack(side=tk.LEFT, padx=5)

        btn_stop = tk.Button(frm_buttons, text="Stop them all",
                             command=self.on_stop)
        btn_stop.pack(side=tk.LEFT, padx=5)

        self.txt_log = tk.Text(self, height=16, wrap=tk.WORD)
        self.txt_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_close_window)
        self.on_poll()

    def on_start(self):
        """One more worker."""
        self.count = self.count + 1

        worker = Worker(self.count, self.messages)
        self.workers.append(worker)
        worker.start()

        self.set_count()

    def on_stop(self):
        """Ask them all to finish.

        Asking, not killing. A thread cannot be stopped from outside in
        Python, and should not be: it might be halfway through writing a
        file. It is told, and it looks.
        """
        for worker in self.workers:
            worker.stop()

    def on_poll(self):
        """The main thread, looking in the queue.

        This is wx.CallAfter turned inside out. There, the worker says
        "run this on the main thread"; here the worker leaves a message
        and the main thread comes to fetch it. The window is the only
        thing that ever touches a widget.
        """
        while True:
            try:
                kind, payload = self.messages.get_nowait()
            except queue.Empty:
                break

            if kind == "log":
                self.log(payload)
            else:
                self.on_finished(payload)

        self.tick = self.after(MILLISECONDS, self.on_poll)

    def log(self, message):
        """Put a line in the window."""
        self.txt_log.insert(tk.END, message + "\n")
        self.txt_log.see(tk.END)

    def on_finished(self, number):
        """A worker has stopped, so take it off the list."""
        self.workers = [worker for worker in self.workers
                        if worker.number != number]

        self.log("Thread {} finished".format(number))
        self.set_count()

    def set_count(self):
        """How many are running."""
        self.lbl_count.config(text="Worker threads: {}".format(
            len(self.workers)))

    def on_close_window(self):
        """Ask the workers to stop before going away.

        They are daemon threads, so the program would exit anyway. Asking
        first means they are not halfway through something when it does.
        """
        self.on_stop()
        self.destroy()

    def destroy(self):
        """And stop looking in the queue."""
        if self.tick is not None:
            self.after_cancel(self.tick)
            self.tick = None

        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
