#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.5 - How do I enable and disable an item?
# source:   wxPythonInAction-src/Chapter-10/disable_item.py
# -----------------------------------------------------------------------------
"""A button that turns a menu item off, and on again.

The difference of the chapter. wx gives every menu item an id and reaches
it with that id from anywhere: menubar.Enable(ID_SIMPLE, False). Tk has no
ids. An entry is addressed by its position in its menu, or by its label,
and the menu object has to be in hand.

Both have a cost. An id survives a label being changed or translated and
a position does not; a label is readable and an id is a number somebody
has to keep in a table.
"""
import tkinter as tk


TARGET = "Simple menu item"


class App(tk.Tk):
    """A window with an item that can be turned off."""

    def __init__(self):
        super().__init__()

        self.title("Enable/Disable Menu Example")
        self.geometry("360x140")

        mnu_bar = tk.Menu(self, tearoff=0)

        # Kept, because entryconfig is a method of the menu the item is
        # in. wx would look the item up from the menu bar by its id.
        self.menu = tk.Menu(mnu_bar, tearoff=0)
        self.menu.add_command(label=TARGET, command=self.on_simple)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Menu", underline=0, menu=self.menu)
        self.config(menu=mnu_bar)

        self.btn_toggle = tk.Button(self, command=self.on_toggle)
        self.btn_toggle.pack(pady=20)

        self.lbl_said = tk.Label(self, text="")
        self.lbl_said.pack()

        self.set_button()

    def get_enabled(self):
        """Whether the item is enabled at the moment."""
        return str(self.menu.entrycget(TARGET, "state")) != "disabled"

    def set_button(self):
        """The button says what it is going to do."""
        word = "Disable"

        if not self.get_enabled():
            word = "Enable"

        self.btn_toggle.config(text="{} Item".format(word))

    def on_toggle(self):
        """Turn it off, or on."""
        state = tk.DISABLED

        if not self.get_enabled():
            state = tk.NORMAL

        self.menu.entryconfig(TARGET, state=state)
        self.set_button()

    def on_simple(self):
        """Say it was chosen, which it can only be when enabled."""
        self.lbl_said.config(text="The item was chosen.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
