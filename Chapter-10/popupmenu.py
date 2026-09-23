#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.9 - How do I make a pop-up menu?
# source:   wxPythonInAction-src/Chapter-10/popupmenu.py
# -----------------------------------------------------------------------------
"""A menu that appears where the pointer is.

The same tk.Menu as everywhere else in the chapter, shown with tk_popup
instead of being given to a window. One line, and one line of tidying
after it that is easy to leave out.
"""
import tkinter as tk


ITEMS = ("One", "Two", "Three")


class App(tk.Tk):
    """A window that has something to say when right-clicked."""

    def __init__(self):
        super().__init__()

        self.title("Popup Menu Example")
        self.geometry("380x180")

        self.popup = tk.Menu(self, tearoff=0)

        for label in ITEMS:
            self.popup.add_command(
                label=label,
                command=lambda name=label: self.on_chosen(name))

        self.lbl_said = tk.Label(self, text="Right click anywhere.")
        self.lbl_said.pack(expand=True)

        # Button-3 on X11 and Windows. On a Mac it is Button-2, and a
        # program that must run on all three binds both, which wx hides
        # behind EVT_CONTEXT_MENU.
        self.bind("<Button-3>", self.on_show_popup)

    def on_show_popup(self, event):
        """Put the menu where the pointer is.

        x_root and y_root, not x and y: tk_popup wants a place on the
        screen and the event gives both, which is the pair to get right.
        """
        try:
            self.popup.tk_popup(event.x_root, event.y_root)
        finally:
            # Without this the menu keeps the pointer grabbed on some
            # window managers, and the rest of the desktop stops
            # answering. It is in a finally because an exception in the
            # line above would leave the grab behind for good.
            self.popup.grab_release()

    def on_chosen(self, label):
        """Say which one it was."""
        self.lbl_said.config(text="You chose: {}".format(label))


if __name__ == "__main__":
    app = App()
    app.mainloop()
