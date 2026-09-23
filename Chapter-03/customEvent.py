#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  3.5 - How do I create my own events?
# source:   wxPythonInAction-src/Chapter-03/customEvent.py
# -----------------------------------------------------------------------------
"""An event of one's own: both buttons pressed, and the window is told.

Tk has virtual events, <<LikeThis>>, and they rise to the parent the way a
wx command event does. What they cannot do is carry anything: the count
travels on the panel, not in the event. See README.md.
"""
import tkinter as tk


class TwoButtonPanel(tk.Frame):
    """Two buttons, which together raise <<TwoButton>> once each has been
    pressed. The wx original puts the count inside the event; here it is an
    attribute, and whoever is told reads it from here."""

    def __init__(self, parent, left_text="Left", right_text="Right"):
        super().__init__(parent)

        self.left_click = False
        self.right_click = False
        self.click_count = 0

        btn_left = tk.Button(self, text=left_text, command=self.on_left_click)
        btn_left.place(x=0, y=0)

        btn_right = tk.Button(self, text=right_text,
                              command=self.on_right_click)
        btn_right.place(x=100, y=0)

    def on_left_click(self):
        """One half of what is being waited for."""
        self.left_click = True
        self.on_click()

    def on_right_click(self):
        """The other half."""
        self.right_click = True
        self.on_click()

    def on_click(self):
        """Count the press, and say so if both buttons have now been used."""
        self.click_count = self.click_count + 1

        if self.left_click and self.right_click:
            self.left_click = False
            self.right_click = False
            self.event_generate("<<TwoButton>>")


class App(tk.Tk):
    """A window that counts pairs of clicks in its title."""

    def __init__(self):
        super().__init__()

        self.title("Click Count: 0")
        self.geometry("300x100")

        self.panel = TwoButtonPanel(self)
        self.panel.pack(fill=tk.BOTH, expand=True)

        # Bound on the window, raised on the panel. A virtual event goes to
        # the widget it was generated on and then along its bindtags, of
        # which the toplevel is one, so this catches it without the panel
        # knowing anybody is listening.
        self.bind("<<TwoButton>>", self.on_two_click)

    def on_two_click(self, event):
        """The count is read from the panel, because the event has no room
        for it. event.widget is what raised it, which is all Tk passes on."""
        self.title("Click Count: {}".format(event.widget.click_count))


if __name__ == "__main__":
    app = App()
    app.mainloop()
