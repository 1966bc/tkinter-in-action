#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  2.1 - How do I create and use an application object?
# source:   wxPythonInAction-src/Chapter-02/startup.py
# -----------------------------------------------------------------------------
"""What happens when, and where the output goes.

Run it from a terminal and watch the order. wx has four places to stand -
App.__init__, OnInit, MainLoop, OnExit - and Tkinter has two. The window
that catches stdout is not in Tkinter either; it is built here, and that is
most of the file. See README.md.
"""
import sys
import tkinter as tk


class OutputWindow(tk.Toplevel):
    """Where print() goes, when it is asked to go to a window.

    wx.App(redirect=True) opens one of these by itself and puts stdout and
    stderr in it. Tkinter has nothing of the sort, so here it is: a Text to
    write into, and an object with write() and flush() put in the place of
    the stream. Anything with those two methods is a file as far as print()
    is concerned.
    """

    def __init__(self, parent, title="Output"):
        super().__init__(parent)

        self.title(title)
        self.geometry("450x200")

        self.txt_output = tk.Text(self, wrap=tk.WORD, height=10)
        self.txt_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self, command=self.txt_output.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_output.config(yscrollcommand=scrollbar.set)

    def write(self, text):
        """Take what print() hands over and show it."""
        self.txt_output.insert(tk.END, text)
        self.txt_output.see(tk.END)

    def flush(self):
        """Nothing to flush, but a file is expected to have this."""
        pass


class App(tk.Tk):
    """The application, which is also the first window."""

    def __init__(self, redirect=False):
        print("App __init__")

        super().__init__()

        self.title("Startup")
        self.geometry("300x300")

        # Only now, with a Tk in existence, can a Toplevel be made. This is
        # why wx can offer redirect as an argument to its App and Tkinter
        # cannot: there is nothing to put the window on until Tk() has run.
        if redirect:
            self.output = OutputWindow(self)
            sys.stdout = self.output
            sys.stderr = self.output

        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        frm_main = tk.Frame(self)
        frm_main.pack(fill=tk.BOTH, expand=True)

        print("A pretend error message", file=sys.stderr)

    def on_exit(self):
        """What wx calls OnExit, in the only place Tkinter offers for it."""
        print("on_exit")
        self.destroy()


if __name__ == "__main__":
    app = App(redirect=True)
    print("before mainloop")
    result = app.mainloop()
    print("after mainloop", result, file=sys.__stdout__)
