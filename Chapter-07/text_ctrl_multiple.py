#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.10 - How do I make a multi-line or styled field?
# source:   wxPythonInAction-src/Chapter-07/text_ctrl_multiple.py
# -----------------------------------------------------------------------------
"""Text over several lines, and text with more than one style in it.

This is the file where Tkinter has the better of it. wx needs TE_RICH2 and
the platform's agreement - "if supported by the native control", says the
original - and applies a style to a range by counting characters. A Tk Text
has tags, everywhere, always, and a tag is a name that can be moved,
found, unmapped, bound to an event and asked which ranges it covers.
"""
import tkinter as tk


GAP = 6

MULTI = ("Here is a looooooooooooooong line of text set in the control.\n\n"
         "See that it wrapped, and that this line is after a blank")

RICH = ("If supported by the native control, this is reversed, "
        "and this is a different font.")


class App(tk.Tk):
    """One plain multi-line field and one with styles in it."""

    def __init__(self):
        super().__init__()

        self.title("Text Entry Example")
        self.geometry("420x250")

        lbl_multi = tk.Label(self, text="Multi-line")
        lbl_multi.grid(row=0, column=0, padx=GAP, pady=GAP, sticky=tk.NW)

        self.txt_multi = tk.Text(self, width=30, height=6, wrap=tk.WORD)
        self.txt_multi.insert("1.0", MULTI)
        self.txt_multi.grid(row=0, column=1, padx=GAP, pady=GAP)

        lbl_rich = tk.Label(self, text="Rich Text")
        lbl_rich.grid(row=1, column=0, padx=GAP, pady=GAP, sticky=tk.NW)

        self.txt_rich = tk.Text(self, width=30, height=6, wrap=tk.WORD)
        self.txt_rich.insert("1.0", RICH)
        self.set_styles()
        self.txt_rich.grid(row=1, column=1, padx=GAP, pady=GAP)

    def set_styles(self):
        """Two tags, over the same ranges the original counts out.

        "1.0 + 44 chars" is how a Text is told about a position: a line,
        a column, and then as many steps as one likes. wx counts from the
        start of the whole control, which is the same arithmetic done by
        hand.
        """
        self.txt_rich.tag_configure("reversed", foreground="white",
                                    background="black")
        self.txt_rich.tag_add("reversed", "1.0 + 44 chars", "1.0 + 52 chars")

        self.txt_rich.tag_configure("other", foreground="blue",
                                    font=("Times", 13, "bold italic"),
                                    underline=True)
        self.txt_rich.tag_add("other", "1.0 + 68 chars", "1.0 + 82 chars")


if __name__ == "__main__":
    app = App()
    app.mainloop()
