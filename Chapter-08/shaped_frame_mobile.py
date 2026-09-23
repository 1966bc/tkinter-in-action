#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.6 - How do I move a window with no title bar?
# source:   wxPythonInAction-src/Chapter-08/shaped_frame_mobile.py
# -----------------------------------------------------------------------------
"""shaped_frame.py, and now it can be dragged by its middle.

A window with no title bar cannot be moved, because moving a window is
what a title bar is for. So the moving is written: remember where in the
window the pointer went down, and on every drag put the window where the
pointer is now, less that offset.

Seven lines, and the same seven in any toolkit. wx does it with
ClientToScreen and Move; Tk with winfo_pointerx and geometry.
"""
import tkinter as tk

import images


class App(tk.Tk):
    """A bare window that can be dragged about by its picture."""

    def __init__(self):
        super().__init__()

        self.title("Shaped Window")

        self.shaped = True
        self.image = images.get_vippi_image()

        # Where in the window the pointer was when the drag started.
        self.offset = (0, 0)

        self.lbl_image = tk.Label(self, image=self.image, borderwidth=0,
                                  highlightthickness=0)
        self.lbl_image.pack()

        self.geometry("{}x{}".format(self.image.width(),
                                     self.image.height()))
        self.set_shape()

        self.bind("<Button-1>", self.on_left_down)
        self.bind("<B1-Motion>", self.on_motion)
        self.bind("<Double-Button-1>", self.on_double_click)
        self.bind("<Button-3>", self.on_exit)

    def set_shape(self):
        """No title bar, no border, no taskbar entry."""
        self.overrideredirect(self.shaped)

    def on_left_down(self, event):
        """Remember where in the window the pointer went down."""
        self.offset = (event.x, event.y)

    def on_motion(self, event):
        """Put the window where the pointer is, less the offset.

        event.x is relative to the widget and winfo_pointerx is relative
        to the screen, which is the pair one needs: without the offset the
        window jumps so that its corner is under the pointer.
        """
        x = self.winfo_pointerx() - self.offset[0]
        y = self.winfo_pointery() - self.offset[1]

        self.geometry("+{}+{}".format(x, y))

    def on_double_click(self, event):
        """Put the decorations back, or take them away again."""
        self.shaped = not self.shaped
        self.set_shape()

    def on_exit(self, event):
        """Right click closes it."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
