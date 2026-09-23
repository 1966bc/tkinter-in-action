#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  3.4 - What happens when two handlers want the same event?
# source:   wxPythonInAction-src/Chapter-03/double_event_one.py
# -----------------------------------------------------------------------------
"""One click, two handlers: the button's own, and the raw mouse press.

Both run. wx keeps a handler going by calling event.Skip() and stops it by
not calling it; Tkinter keeps going by default and stops when a handler
returns the string "break". See README.md.
"""
import tkinter as tk


class App(tk.Tk):
    """A button that hears its own press twice, in two different ways."""

    def __init__(self):
        super().__init__()

        self.title("Frame With Button")
        self.geometry("300x100")

        self.frm_panel = tk.Frame(self)
        self.frm_panel.pack(fill=tk.BOTH, expand=True)

        self.btn_click = tk.Button(self.frm_panel, text="Click Me",
                                   command=self.on_button_click)
        self.btn_click.place(x=100, y=15)

        # The command is what the Button raises when it has been pressed
        # and released on itself. This is the press, before the Button has
        # decided anything, and it arrives first.
        self.btn_click.bind("<Button-1>", self.on_mouse_down)

    def on_button_click(self):
        """The button's own event. The panel turns green."""
        self.frm_panel.config(background="green")

    def on_mouse_down(self, event):
        """The raw press. It runs before the Button's own handling, and
        returning "break" here would end the matter - no pressed look, no
        command, nothing. Not returning it is wx's event.Skip()."""
        self.btn_click.config(text="Again!")


if __name__ == "__main__":
    app = App()
    app.mainloop()
