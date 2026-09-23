#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.1 - How do I display static text?
# source:   wxPythonInAction-src/Chapter-07/static_text.py
# -----------------------------------------------------------------------------
"""Static text, aligned, coloured, in another font, and over several lines.

One thing needs saying. wx has ALIGN_CENTER and ALIGN_RIGHT and they do
two jobs at once. Tk keeps them apart: anchor says where the block of text
sits inside the widget, justify says how the lines line up with each
other. A single line only notices anchor; several lines notice both.
"""
import tkinter as tk


REVERSED = {"foreground": "white", "background": "black"}

SPLIT = ("Your text\ncan be split\n"
         "over multiple lines\n\neven blank ones")

SPLIT_RIGHT = ("Multi-line text\ncan also\n"
               "be right aligned\n\neven with a blank")


class App(tk.Tk):
    """Seven labels, each saying what it is."""

    def __init__(self):
        super().__init__()

        self.title("Static Text Example")
        self.geometry("400x300")

        lbl_plain = tk.Label(self, text="This is an example of static text")
        lbl_plain.place(x=100, y=10)

        lbl_reversed = tk.Label(self, text="Static Text With Reversed Colors",
                                **REVERSED)
        lbl_reversed.place(x=100, y=30)

        lbl_centre = tk.Label(self, text="align center", anchor=tk.CENTER,
                              **REVERSED)
        lbl_centre.place(x=100, y=50, width=160)

        lbl_right = tk.Label(self, text="align right", anchor=tk.E, **REVERSED)
        lbl_right.place(x=100, y=70, width=160)

        # A font is a tuple, and the three parts are family, size and
        # style. wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL) names
        # a family by what it is for; Tk names it by what it is called,
        # and "Times" is on every machine Tk runs on.
        lbl_font = tk.Label(self, text="You can also change the font.",
                            font=("Times", 18, "italic"))
        lbl_font.place(x=20, y=100)

        lbl_split = tk.Label(self, text=SPLIT, justify=tk.LEFT)
        lbl_split.place(x=20, y=150)

        lbl_split_right = tk.Label(self, text=SPLIT_RIGHT, justify=tk.RIGHT)
        lbl_split_right.place(x=220, y=150)


if __name__ == "__main__":
    app = App()
    app.mainloop()
