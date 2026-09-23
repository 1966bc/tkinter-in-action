#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  1.5 - What can wxPython do?
# source:   wxPythonInAction-src/Chapter-01/sample.py
# -----------------------------------------------------------------------------
"""The mouse position, written into a field as the pointer moves.

The first example with an event in it. wx asks the event object where the
pointer is; Tkinter puts it on the event as x and y, already relative to the
widget that was bound.
"""
import tkinter as tk


class App(tk.Tk):
    """A panel that reports where the pointer is over it."""

    def __init__(self):
        super().__init__()

        self.title("My Frame")
        self.geometry("300x300")

        self.position = tk.StringVar()

        frm_panel = tk.Frame(self)
        frm_panel.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)
        frm_panel.bind("<Motion>", self.on_move)

        lbl_position = tk.Label(frm_panel, text="Pos:")
        lbl_position.place(x=10, y=10)

        ent_position = tk.Entry(frm_panel, background="white",
                                textvariable=self.position)
        ent_position.place(x=40, y=10)

    def on_move(self, event):
        """Where the pointer is, in the coordinates of the bound widget."""
        self.position.set("{}, {}".format(event.x, event.y))


if __name__ == "__main__":
    app = App()
    app.mainloop()
