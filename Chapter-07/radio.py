#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.7 - How do I make radio buttons?
# source:   wxPythonInAction-src/Chapter-07/radio.py
# -----------------------------------------------------------------------------
"""Three radio buttons, each enabling its own field.

Where wx groups radio buttons by putting RB_GROUP on the first one and
relying on the order they were made in, Tk groups them by the variable
they share. Nothing depends on the order, and two groups can be
interleaved on the screen without confusing each other.
"""
import tkinter as tk


NAMES = ("Elmo", "Ernie", "Bert")


class App(tk.Tk):
    """One field per name, and only the chosen one can be typed in."""

    def __init__(self):
        super().__init__()

        self.title("Radio Example")
        self.geometry("200x200")

        self.chosen = tk.StringVar(value=NAMES[0])
        self.entries = {}

        for index, name in enumerate(NAMES):
            y_position = 50 + index * 30

            radio = tk.Radiobutton(self, text=name, value=name,
                                   variable=self.chosen,
                                   command=self.on_radio)
            radio.place(x=20, y=y_position)

            entry = tk.Entry(self, width=10, state=tk.DISABLED)
            entry.place(x=90, y=y_position)

            self.entries[name] = entry

        self.on_radio()

    def on_radio(self):
        """Enable the field of the one that is chosen, disable the rest.

        The wx original keeps the last enabled field in an attribute and
        turns it off before turning the new one on. Here the variable
        already knows which is which, so the loop says what it means.
        """
        for name, entry in self.entries.items():
            if name == self.chosen.get():
                entry.config(state=tk.NORMAL)
            else:
                entry.config(state=tk.DISABLED)


if __name__ == "__main__":
    app = App()
    app.mainloop()
