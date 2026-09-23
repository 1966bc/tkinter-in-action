#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.7 - How do I find a menu item again?
# source:   wxPythonInAction-src/Chapter-10/find_item.py
# -----------------------------------------------------------------------------
"""Finding an item that is already on a menu, and changing it.

wx keeps ids: FindItemById(event.GetId()) hands back the wx.MenuItem, and
the id is in the event, so a handler always knows which item called it.

Tk has no ids and no such event. An entry is found by its label with
index(), and a handler that needs to know which item it was must be told
when it is made - usually by a lambda, which is what this file does.

It is less tidy and it is not worse. The lambda says in the same line
which item does what, where wx says it in two places and a table.
"""
import tkinter as tk


LABELS = ("First", "Second", "Third")


class App(tk.Tk):
    """A window whose menu items can be found and renamed."""

    def __init__(self):
        super().__init__()

        self.title("Find Item Example")
        self.geometry("380x160")

        mnu_bar = tk.Menu(self, tearoff=0)
        self.menu = tk.Menu(mnu_bar, tearoff=0)

        for label in LABELS:
            self.menu.add_command(
                label=label,
                command=lambda name=label: self.on_chosen(name))

        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Menu", underline=0, menu=self.menu)
        self.config(menu=mnu_bar)

        self.lbl_said = tk.Label(self, justify=tk.LEFT,
                                 text="Choose an item. It will be marked.")
        self.lbl_said.pack(expand=True)

    def on_chosen(self, label):
        """Mark the one that was chosen and unmark the others.

        The lambda carries the label because a Tk command is called with
        nothing. Note the default argument: without it every lambda would
        close over the same name and all three would say "Third".
        """
        for each in LABELS:
            position = self.get_position(each)

            if position is not None:
                mark = each

                if each == label:
                    mark = "{} (chosen)".format(each)

                self.menu.entryconfig(position, label=mark)

        self.lbl_said.config(text="You chose: {}\n"
                                  "Its position in the menu is {}.".format(
                                      label, self.get_position(label)))

    def get_position(self, label):
        """Where an item is, by the label it starts with.

        index() wants the label as it is now, and these change. So the
        menu is walked, which is what one ends up doing, and is the part
        an id would have made unnecessary.
        """
        found = None

        for position in range(self.menu.index("end") + 1):
            if str(self.menu.type(position)) == "command":
                current = str(self.menu.entrycget(position, "label"))

                if current.startswith(label):
                    found = position

        return found


if __name__ == "__main__":
    app = App()
    app.mainloop()
