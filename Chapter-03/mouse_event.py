#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  3.3 - How do I know when the mouse is over a widget?
# source:   wxPythonInAction-src/Chapter-03/mouse_event.py
# -----------------------------------------------------------------------------
"""A button that says whether the pointer is over it.

EVT_ENTER_WINDOW and EVT_LEAVE_WINDOW are <Enter> and <Leave>, which is as
direct as a translation gets in this book.
"""
import tkinter as tk


OVER = "Over Me!"
AWAY = "Not Over"


class App(tk.Tk):
    """One button, which notices the pointer arriving and leaving."""

    def __init__(self):
        super().__init__()

        self.title("Frame With Button")
        self.geometry("300x100")

        self.frm_panel = tk.Frame(self)
        self.frm_panel.pack(fill=tk.BOTH, expand=True)

        self.btn_over = tk.Button(self.frm_panel, text=AWAY,
                                  command=self.on_button_click)
        self.btn_over.place(x=100, y=15)

        self.btn_over.bind("<Enter>", self.on_enter_window)
        self.btn_over.bind("<Leave>", self.on_leave_window)

    def on_button_click(self):
        """The panel turns green, as in the original."""
        self.frm_panel.config(background="green")

    def on_enter_window(self, event):
        """The wx original calls event.Skip() here so that the button still
        draws itself as hovered. Tkinter goes on to the class binding by
        itself, and it is returning "break" that would stop it."""
        self.btn_over.config(text=OVER)

    def on_leave_window(self, event):
        """And back again."""
        self.btn_over.config(text=AWAY)


if __name__ == "__main__":
    app = App()
    app.mainloop()
