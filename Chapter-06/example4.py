#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  6.3 - How do I build a menu from data?
# source:   wxPythonInAction-src/Chapter-06/example4.py
# -----------------------------------------------------------------------------
"""example3.py, with a menu built the way chapter 5 argued for.

The colour menu uses radio items, which Tk has and calls radiobutton, and
which need a variable to agree on rather than an id to check.
"""
import tkinter as tk

from example1 import SketchWindow


SHARES = (1, 2, 3)

COLOURS = ("Black", "Red", "Green", "Blue")


class App(tk.Tk):
    """A sketch window with a menu that knows about colours."""

    def __init__(self):
        super().__init__()

        self.title("Sketch Frame")
        self.geometry("800x600")

        # What the radio items of the colour menu agree on. Tk radio items
        # share a variable and each one holds a value; wx gives each an id
        # and the handler asks which one it was.
        self.colour = tk.StringVar(value=COLOURS[0])

        self.fields = self.get_status_bar()
        self.set_menu_bar()

        self.sketch = SketchWindow(self)
        self.sketch.pack(fill=tk.BOTH, expand=True)

        self.sketch.bind("<Motion>", self.on_sketch_motion)

    def get_menu_data(self):
        """The menus, as data: a name, then its items.

        An item is a label, the help the wx original puts in the status
        bar, and what it does. An empty label is a separator, and a colour
        name in the third place means a radio item.
        """
        return (("File",
                 (("New", "New sketch file", self.on_new),
                  ("Open", "Open sketch file", self.on_open),
                  ("Save", "Save sketch file", self.on_save),
                  ("", "", None),
                  ("Quit", "Quit", self.on_close_window))),
                ("Color",
                 tuple((name, "", None) for name in COLOURS)))

    def set_menu_bar(self):
        """One menu per line of get_menu_data()."""
        mnu_bar = tk.Menu(self)

        for label, items in self.get_menu_data():
            menu = tk.Menu(mnu_bar, tearoff=0)

            for item_label, status, handler in items:
                self.set_menu_item(menu, label, item_label, status, handler)

            mnu_bar.add_cascade(label=label, underline=0, menu=menu)

        self.config(menu=mnu_bar)

    def set_menu_item(self, menu, menu_label, label, status, handler):
        """One item. The Color menu gets radio items, the rest commands."""
        if not label:
            menu.add_separator()
        elif menu_label == "Color":
            menu.add_radiobutton(label=label, value=label,
                                 variable=self.colour, command=self.on_color)
        else:
            menu.add_command(label=label, command=handler)

    def get_status_bar(self):
        """Three sunken Labels sharing the width one to two to three."""
        frm_status = tk.Frame(self)
        frm_status.pack(side=tk.BOTTOM, fill=tk.X)

        fields = []

        for column, share in enumerate(SHARES):
            label = tk.Label(frm_status, borderwidth=1, relief=tk.SUNKEN,
                             anchor=tk.W)
            label.grid(row=0, column=column, sticky=tk.E + tk.W)
            frm_status.grid_columnconfigure(column, weight=share)
            fields.append(label)

        return fields

    def on_sketch_motion(self, event):
        """The position, the line being drawn, and how many there are."""
        self.fields[0].config(text="Pos: ({}, {})".format(event.x, event.y))
        self.fields[1].config(text="Current Pts: {}".format(
            len(self.sketch.current_line)))
        self.fields[2].config(text="Line Count: {}".format(
            len(self.sketch.lines)))

    def on_color(self):
        """The variable already holds the colour that was chosen."""
        self.sketch.set_color(self.colour.get().lower())

    def on_new(self):
        """Nothing yet. example6.py is where the files arrive."""
        pass

    def on_open(self):
        """Nothing yet."""
        pass

    def on_save(self):
        """Nothing yet."""
        pass

    def on_close_window(self):
        """Shut the window."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
