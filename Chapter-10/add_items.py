#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.3 - How do I add an item while the program is running?
# source:   wxPythonInAction-src/Chapter-10/add_items.py
# -----------------------------------------------------------------------------
"""Type a word, press the button, and it is on the menu.

wx keeps a menu as a list of wx.MenuItem objects and gives each an id. Tk
keeps it as a list of entries addressed by position, or by their label,
and there are no ids at all. Adding is add_command either way; the
difference shows up when something has to be found again, which is
find_item.py.
"""
import tkinter as tk


class App(tk.Tk):
    """A window whose menu grows."""

    def __init__(self):
        super().__init__()

        self.title("Add Items Example")
        self.geometry("360x140")

        mnu_bar = tk.Menu(self, tearoff=0)
        self.menu = tk.Menu(mnu_bar, tearoff=0)
        self.menu.add_command(label="Exit", command=self.destroy)
        mnu_bar.add_cascade(label="Menu", underline=0, menu=self.menu)
        self.config(menu=mnu_bar)

        self.ent_label = tk.Entry(self, width=24)
        self.ent_label.insert(0, "New item")
        self.ent_label.pack(pady=15)

        btn_add = tk.Button(self, text="Add to the menu",
                            command=self.on_add)
        btn_add.pack()

        self.lbl_said = tk.Label(self, text="")
        self.lbl_said.pack(pady=10)

    def on_add(self):
        """Put what was typed on the menu, above Exit."""
        label = self.ent_label.get().strip()

        if label:
            # insert_command rather than add_command: add puts it at the
            # end, which would be below Exit. wx has Insert() for the
            # same reason and counts from the same place.
            self.menu.insert_command(
                self.menu.index("Exit"), label=label,
                command=lambda: self.on_chosen(label))

            self.lbl_said.config(text="Added: {}".format(label))

    def on_chosen(self, label):
        """Say which of the new items it was."""
        self.lbl_said.config(text="You chose: {}".format(label))


if __name__ == "__main__":
    app = App()
    app.mainloop()
