#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.3 - How do I ask for a font?
# source:   wxPythonInAction-src/Chapter-09/font_box.py
# -----------------------------------------------------------------------------
"""The font chooser that Tkinter has and does not offer you.

There is no tkinter.fontchooser. But Tk itself has had one since 8.6, and
a Tkinter program can reach it through the interpreter:

    root.tk.call("tk", "fontchooser", "show")

It is not a dialog one waits for. wx shows its font dialog, blocks, and
returns a code; Tk's chooser stays open, and a font is announced by
calling back whenever one is chosen, which may be several times. See
README.md.
"""
import tkinter as tk


class App(tk.Tk):
    """A label, and a chooser that changes it while it is open."""

    def __init__(self):
        super().__init__()

        self.title("Font Box")
        self.geometry("420x160")

        self.lbl_sample = tk.Label(self, text="The quick brown fox")
        self.lbl_sample.pack(expand=True)

        btn_choose = tk.Button(self, text="Choose a font...",
                               command=self.on_choose)
        btn_choose.pack(pady=10)

        # register() hands Tcl a name it can call back on. The chooser
        # calls it with the font as a Tcl font description.
        self.tk.call("tk", "fontchooser", "configure",
                     "-parent", self,
                     "-title", "Choose a font",
                     "-command", self.register(self.on_font))

    def on_choose(self):
        """Show it. It does not block, so this returns at once."""
        self.tk.call("tk", "fontchooser", "show")

    def on_font(self, *description):
        """Called by Tk, every time a font is chosen, while it is open."""
        font = " ".join(description)

        self.lbl_sample.config(font=font)
        print("You selected: {}".format(font))


if __name__ == "__main__":
    app = App()
    app.mainloop()
