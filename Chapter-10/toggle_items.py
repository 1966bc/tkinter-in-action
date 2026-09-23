#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.4 - How do I make items that can be ticked?
# source:   wxPythonInAction-src/Chapter-10/toggle_items.py
# -----------------------------------------------------------------------------
"""Three items that can each be ticked, and three of which only one can.

AppendCheckItem and AppendRadioItem are add_checkbutton and
add_radiobutton, with the difference that runs through this whole book: a
wx item remembers whether it is ticked and a Tk item keeps it in a
variable you provide and must keep alive.

The saving is the same as in chapter 6. wx radio items are a group
because they are next to each other in the menu; Tk radio items are a
group because they share a variable, so they can be anywhere - one in a
menu, one on a toolbar, one in a panel - and they still agree.
"""
import tkinter as tk


CHECKS = ("Check Item 1", "Check Item 2", "Check Item 3")
RADIOS = ("Radio Item 1", "Radio Item 2", "Radio Item 3")


class App(tk.Tk):
    """A window whose menu holds both kinds."""

    def __init__(self):
        super().__init__()

        self.title("Toggle Items")
        self.geometry("360x160")

        # Held on self. A variable in a local is collected and the item
        # stops remembering anything.
        self.checked = {}
        self.chosen = tk.StringVar(value=RADIOS[0])

        mnu_bar = tk.Menu(self, tearoff=0)
        menu = tk.Menu(mnu_bar, tearoff=0)

        for label in CHECKS:
            self.checked[label] = tk.BooleanVar()
            menu.add_checkbutton(label=label, variable=self.checked[label],
                                 command=self.on_toggle)

        menu.add_separator()

        for label in RADIOS:
            menu.add_radiobutton(label=label, value=label,
                                 variable=self.chosen, command=self.on_toggle)

        menu.add_separator()
        menu.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Toggle Items", underline=0, menu=menu)
        self.config(menu=mnu_bar)

        self.lbl_state = tk.Label(self, justify=tk.LEFT)
        self.lbl_state.pack(expand=True)

        self.on_toggle()

    def on_toggle(self):
        """Show what is ticked and which one is chosen."""
        ticked = [label for label in CHECKS if self.checked[label].get()]

        self.lbl_state.config(text="Ticked: {}\nChosen: {}".format(
            ", ".join(ticked) or "nothing", self.chosen.get()))


if __name__ == "__main__":
    app = App()
    app.mainloop()
