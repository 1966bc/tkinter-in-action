#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  5.3 - How do I separate the model from the view?
# source:   wxPythonInAction-src/Chapter-05/modelExample.py
# -----------------------------------------------------------------------------
"""Four buttons, two fields, and a model in between that does not know them.

The buttons do not write in the fields. They set the model; the model says
it has changed; the window, which asked to be told, goes and reads it. See
README.md for what Tkinter offers instead and why this is still the file
worth copying.
"""
import tkinter as tk

import abstractmodel


class SimpleName(abstractmodel.AbstractModel):
    """A first name and a last name, and nothing about windows."""

    def __init__(self, first="", last=""):
        super().__init__()

        self.first = first
        self.last = last

        self.update()

    def set(self, first, last):
        """Change both, then say so. Once, after both, not after each."""
        self.first = first
        self.last = last

        self.update()


class App(tk.Tk):
    """A window that shows a SimpleName and never writes to itself."""

    def __init__(self):
        super().__init__()

        self.title("Flintstones")
        self.geometry("340x200")
        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        frm_panel = tk.Frame(self, background="white")
        frm_panel.pack(fill=tk.BOTH, expand=True)

        self.entries = {}
        self.set_text_fields(frm_panel)

        self.model = SimpleName()
        self.model.add_listener(self.on_update)

        self.set_button_bar(frm_panel)

    def get_button_data(self):
        """Who each button turns the model into."""
        return (("Fredify", self.on_fred),
                ("Wilmafy", self.on_wilma),
                ("Barnify", self.on_barney),
                ("Bettify", self.on_betty))

    def get_text_field_data(self):
        """The two fields, and where they go."""
        return (("First Name", (10, 50)),
                ("Last Name", (10, 80)))

    def set_button_bar(self, parent, y_position=0):
        """The buttons in a row, each starting where the last one ended."""
        x_position = 0

        for label, handler in self.get_button_data():
            button = tk.Button(parent, text=label, command=handler)
            button.place(x=x_position, y=y_position)
            button.update_idletasks()
            x_position = x_position + button.winfo_reqwidth()

    def set_text_fields(self, parent):
        """A caption and a read-only field for each line of the data."""
        for label, position in self.get_text_field_data():
            x_position, y_position = position

            lbl_caption = tk.Label(parent, text=label, background="white")
            lbl_caption.place(x=x_position, y=y_position)

            entry = tk.Entry(parent, width=14, state="readonly")
            entry.place(x=x_position + 70, y=y_position)

            self.entries[label] = entry

    def set_entry(self, label, value):
        """Write into a field that is read-only to everybody else.

        A Tk Entry in state="readonly" refuses insert() as firmly as it
        refuses the keyboard, so it is opened, written and closed again.
        """
        entry = self.entries[label]

        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def on_update(self, model):
        """Called by the model. The window reads; it is not told what."""
        self.set_entry("First Name", model.first)
        self.set_entry("Last Name", model.last)

    def on_fred(self):
        """Set the model. Nothing here touches a widget."""
        self.model.set("Fred", "Flintstone")

    def on_wilma(self):
        """Set the model."""
        self.model.set("Wilma", "Flintstone")

    def on_barney(self):
        """Set the model."""
        self.model.set("Barney", "Rubble")

    def on_betty(self):
        """Set the model."""
        self.model.set("Betty", "Rubble")

    def on_close_window(self):
        """Stop listening before going away, or the model keeps a dead
        window on its list and calls it."""
        self.model.remove_listener(self.on_update)
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
