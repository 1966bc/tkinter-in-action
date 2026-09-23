#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  6.4 - How do I add a toolbar?
# source:   wxPythonInAction-src/Chapter-06/example5.py
# -----------------------------------------------------------------------------
"""example4.py, with a toolbar, including one colour swatch per colour.

The swatches are drawn rather than loaded, as in the original. wx makes an
empty bitmap and clears it to a colour; a PhotoImage is made empty and
filled with put(). See README.md for why the three file icons are words
here instead of pictures.
"""
import tkinter as tk

from example1 import SketchWindow


SHARES = (1, 2, 3)

COLOURS = ("Black", "Red", "Green", "Blue")

# The size of the wx swatch, wx.EmptyBitmap(16, 15).
SWATCH_WIDTH = 16
SWATCH_HEIGHT = 15


class App(tk.Tk):
    """A sketch window with a menu, a toolbar and a status bar."""

    def __init__(self):
        super().__init__()

        self.title("Sketch Frame")
        self.geometry("800x600")

        self.colour = tk.StringVar(value=COLOURS[0])
        self.swatches = {}

        self.fields = self.get_status_bar()
        self.set_menu_bar()
        self.set_tool_bar()

        self.sketch = SketchWindow(self)
        self.sketch.pack(fill=tk.BOTH, expand=True)

        self.sketch.bind("<Motion>", self.on_sketch_motion)

    def get_tool_bar_data(self):
        """The tools, as data: a label, its help, and what it does.

        The wx original names a .bmp for each. Those files belong to the
        book and are not copied here, and Tk cannot read BMP in any case,
        so these three are words.
        """
        return (("New", "Create new sketch", self.on_new),
                ("", "", None),
                ("Open", "Open existing sketch", self.on_open),
                ("Save", "Save existing sketch", self.on_save))

    def get_swatch(self, colour):
        """A small rectangle of one colour, drawn rather than loaded.

        wx.EmptyBitmap(16, 15) cleared with a brush; here an empty
        PhotoImage and put(), which fills a rectangle of it with a colour
        name. The result has to be kept alive, as ever.
        """
        swatch = tk.PhotoImage(width=SWATCH_WIDTH, height=SWATCH_HEIGHT)
        swatch.put(colour, to=(0, 0, SWATCH_WIDTH, SWATCH_HEIGHT))

        return swatch

    def set_tool_bar(self):
        """A Frame of flat buttons, and then one radio button per colour."""
        frm_toolbar = tk.Frame(self, borderwidth=1, relief=tk.RAISED)
        frm_toolbar.pack(side=tk.TOP, fill=tk.X)

        for label, help_text, handler in self.get_tool_bar_data():
            if not label:
                separator = tk.Frame(frm_toolbar, width=2, relief=tk.SUNKEN,
                                     borderwidth=1)
                separator.pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=2)
            else:
                button = tk.Button(frm_toolbar, text=label, relief=tk.FLAT,
                                   command=handler)
                button.pack(side=tk.LEFT, padx=2, pady=2)

        for colour in COLOURS:
            self.swatches[colour] = self.get_swatch(colour.lower())

            tool = tk.Radiobutton(frm_toolbar, image=self.swatches[colour],
                                  value=colour, variable=self.colour,
                                  indicatoron=False, command=self.on_color)
            tool.pack(side=tk.LEFT, padx=2, pady=2)

    def get_menu_data(self):
        """The menus, as data."""
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
        """One item. The Color menu gets radio items, the rest commands.

        The radio items and the toolbar swatches share self.colour, so
        choosing in one moves the other. wx has to be told to keep them in
        step; a Tk variable is the thing they have in common.
        """
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
        """Nothing yet."""
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
