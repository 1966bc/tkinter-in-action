#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.3 - How do I scroll a window?
# source:   wxPythonInAction-src/Chapter-08/scroll_window.py
# -----------------------------------------------------------------------------
"""A window bigger than itself, with a button at each far corner.

wx.ScrolledWindow is a widget: give it a virtual size and it scrolls. Tk
has no such widget, and the way everybody does it is a Canvas with a Frame
inside it. Not a workaround - the documented answer - and it is the most
awkward thing in this book. See README.md.
"""
import tkinter as tk


# The virtual size of the wx original, SetScrollbars(1, 1, 600, 400).
INNER_WIDTH = 600
INNER_HEIGHT = 400


class ScrolledWindow(tk.Frame):
    """What wx.ScrolledWindow is, out of a Canvas, a Frame and two bars.

    Widgets go in self.inner. The Canvas exists only to be scrolled; the
    Frame exists only to hold things; and a canvas window item joins the
    two. Three widgets to do what wx does with one.
    """

    def __init__(self, parent, width, height):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, scrollregion=(0, 0, width, height))

        across = tk.Scrollbar(self, orient=tk.HORIZONTAL,
                              command=self.canvas.xview)
        down = tk.Scrollbar(self, orient=tk.VERTICAL,
                            command=self.canvas.yview)

        self.canvas.config(xscrollcommand=across.set, yscrollcommand=down.set)

        down.pack(side=tk.RIGHT, fill=tk.Y)
        across.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.inner = tk.Frame(self.canvas, width=width, height=height)
        self.canvas.create_window(0, 0, window=self.inner, anchor=tk.NW)

    def scroll_to(self, x, y):
        """Put a point of the inner frame at the top left corner.

        wx.Scroll() takes pixels. Tk's xview_moveto takes a fraction of
        the whole width, which is the same thing said differently and has
        to be worked out.
        """
        region = self.canvas.cget("scrollregion").split()
        width = int(region[2])
        height = int(region[3])

        self.canvas.xview_moveto(x / width)
        self.canvas.yview_moveto(y / height)


class App(tk.Tk):
    """A small window looking at a large one."""

    def __init__(self):
        super().__init__()

        self.title("Scrollbar Example")
        self.geometry("300x200")

        self.scroll = ScrolledWindow(self, INNER_WIDTH, INNER_HEIGHT)
        self.scroll.pack(fill=tk.BOTH, expand=True)

        self.btn_top = tk.Button(self.scroll.inner, text="Scroll Me",
                                 command=self.on_click_top)
        self.btn_top.place(x=50, y=20)

        self.btn_bottom = tk.Button(self.scroll.inner, text="Scroll Back",
                                    command=self.on_click_bottom)
        self.btn_bottom.place(x=460, y=350)

    def on_click_top(self):
        """Go to the far corner."""
        self.scroll.scroll_to(INNER_WIDTH, INNER_HEIGHT)

    def on_click_bottom(self):
        """And back."""
        self.scroll.scroll_to(0, 0)


if __name__ == "__main__":
    app = App()
    app.mainloop()
