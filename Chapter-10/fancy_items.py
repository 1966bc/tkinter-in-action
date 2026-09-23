#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.6 - How do I make an item look different?
# source:   wxPythonInAction-src/Chapter-10/fancy_items.py
# -----------------------------------------------------------------------------
"""Menu items with a picture, a font and a colour of their own.

wx needs a wx.MenuItem built separately, given SetFont and SetBitmap, and
then appended - and the book says it works on Windows and is ignored
elsewhere.

A Tk menu entry takes font, foreground, background, image and compound as
options, like any other widget, on every platform. Asked on this machine
a fancy entry reports its font back correctly, which is the test.
"""
import tkinter as tk


class App(tk.Tk):
    """A window with a menu that is not all one colour."""

    def __init__(self):
        super().__init__()

        self.title("Fancy Items Example")
        self.geometry("360x140")

        # Held on self, as ever.
        self.dot = self.get_dot("navy")

        mnu_bar = tk.Menu(self, tearoff=0)
        self.menu = tk.Menu(mnu_bar, tearoff=0)

        self.menu.add_command(label="Plain item", command=self.on_chosen)

        self.menu.add_command(label="Bold and blue", command=self.on_chosen,
                              font=("TkDefaultFont", 11, "bold"),
                              foreground="navy")

        self.menu.add_command(label="With a picture", command=self.on_chosen,
                              image=self.dot, compound=tk.LEFT)

        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Menu", underline=0, menu=self.menu)
        self.config(menu=mnu_bar)

        self.lbl_said = tk.Label(self, text="Open the menu.")
        self.lbl_said.pack(expand=True)

    def get_dot(self, colour):
        """A small square, drawn rather than loaded."""
        dot = tk.PhotoImage(width=14, height=14)
        dot.put(colour, to=(0, 0, 14, 14))

        return dot

    def on_chosen(self):
        """Say that something was chosen."""
        self.lbl_said.config(text="Chosen.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
