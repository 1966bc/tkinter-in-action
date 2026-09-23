#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  4.4 - How do I use PyWrap?
# source:   wxPythonInAction-src/Chapter-04/PyWrap.py
# -----------------------------------------------------------------------------
"""Runs somebody else's Tkinter program with a Python prompt attached.

    python3 Chapter-04/PyWrap.py Chapter-01/spare.py
    python3 Chapter-04/PyWrap.py Chapter-02/toolbar.py

The program is imported rather than run, its window class is found, and it
is started with a shell whose namespace holds it. Nothing in the program
needs to know. The original does the same for a wx.App; what changes is what
is looked for, because in Tkinter the application and the window are one
thing.
"""
import code
import contextlib
import io
import importlib.util
import os
import sys
import tkinter as tk


BANNER = "The window is called app."


class ShellWindow(tk.Toplevel):
    """A Python prompt over a namespace handed to it.

    The same class as in pycrust-foundation.py, kept here rather than
    imported: that file is named as the book names it, with a hyphen, and a
    hyphen is not a name Python can import.
    """

    def __init__(self, parent, namespace, banner=""):
        super().__init__(parent)

        self.title("PyWrap")
        self.geometry("560x320")

        self.console = code.InteractiveConsole(namespace)

        self.txt_shell = tk.Text(self, wrap=tk.WORD, background="white",
                                 insertbackground="black")
        self.txt_shell.pack(fill=tk.BOTH, expand=True)
        self.txt_shell.bind("<Return>", self.on_return)

        if banner:
            self.write(banner + "\n")

        self.write(">>> ")

    def write(self, text):
        """Put text at the end and keep it in view."""
        self.txt_shell.insert(tk.END, text)
        self.txt_shell.see(tk.END)

    def on_return(self, event):
        """Run what was typed on this line and show what came back."""
        line = self.txt_shell.get("insert linestart", "insert lineend")
        source = line

        if line.startswith(">>> ") or line.startswith("... "):
            source = line[4:]

        self.write("\n")

        caught = io.StringIO()
        more = False

        try:
            with contextlib.redirect_stdout(caught):
                with contextlib.redirect_stderr(caught):
                    more = self.console.push(source)
        except SystemExit:
            self.write("(exit ignored in a window)\n")

        self.write(caught.getvalue())

        if more:
            self.write("... ")
        else:
            self.write(">>> ")

        return "break"


def get_module(path):
    """Import a program by its file name, whatever that name is.

    A file called pycrust-foundation.py cannot be imported by name, and one
    in another directory is not on the path, so both are loaded from the
    file itself.
    """
    name = os.path.splitext(os.path.basename(path))[0].replace("-", "_")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)

    sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
    spec.loader.exec_module(module)

    return module


def get_window_class(module):
    """The Tk subclass in a module, which is its application.

    wx looks for a wx.App, because in wx the application is not a window.
    Here the two are the same object, so what is looked for is the window.
    """
    found = None

    for name in dir(module):
        thing = getattr(module, name)

        if isinstance(thing, type) and issubclass(thing, tk.Tk):
            if thing is not tk.Tk:
                found = thing

    return found


def main(path):
    """Start the program, and a prompt looking at it."""
    module = get_module(path)
    window_class = get_window_class(module)

    if window_class is None:
        print("no tk.Tk subclass found in {}".format(path), file=sys.stderr)
    else:
        app = window_class()
        ShellWindow(app, {"app": app, "tk": tk, "module": module}, BANNER)
        app.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: PyWrap.py <program.py>", file=sys.stderr)
    else:
        main(sys.argv[1])
