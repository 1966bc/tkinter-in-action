#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  6.6 - Putting it together
# source:   wxPythonInAction-src/Chapter-06/example7.py
# -----------------------------------------------------------------------------
"""Sketch, finished: a control panel, an about window and a splash screen.

Three things arrive here. The panel of sixteen colours and sixteen widths,
which Tk makes shorter than wx does. The about window, which in the
original is a page of HTML and here is not, because Tkinter has no HTML
widget. And the splash screen, which wx has as a class and Tkinter has as
a Toplevel with its decorations turned off. See README.md.
"""
import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from example1 import SketchWindow


WILDCARD = [("Sketch files", "*.sketch"), ("All files", "*.*")]


SHARES = (1, 2, 3)

COLOURS = ("Black", "Red", "Green", "Blue")

# The sixteen of the control panel. Every one of these is a name Tk knows.
PALETTE = ("Black", "Yellow", "Red", "Green", "Blue", "Purple",
           "Brown", "Aquamarine", "Forest Green", "Light Blue",
           "Goldenrod", "Cyan", "Orange", "Navy", "Dark Grey",
           "Light Grey")

MAX_THICKNESS = 16
PANEL_COLUMNS = 4

ABOUT = """Sketch!

Sketch is a demonstration program for wxPython in Action, chapter 6. It is
based on the SuperDoodle demo included with wxPython.

SuperDoodle and wxPython are brought to you by Robin Dunn and Total Control
Software, Copyright 1997-2006.

This is the Tkinter translation. The original about window is a page of
HTML, which Tkinter has no widget for; this is a Text, which is what one
uses instead.
"""

SPLASH_MILLISECONDS = 1000

# The size of the wx swatch, wx.EmptyBitmap(16, 15).
SWATCH_WIDTH = 16
SWATCH_HEIGHT = 15


class SketchAbout(tk.Toplevel):
    """What the original shows as a page of HTML.

    wx.html.HtmlWindow renders markup. Tkinter has no such widget, in this
    chapter or any other, and this is why chapter 16 of the book is not in
    this one. A read-only Text with the same words is the honest stand-in:
    the information arrives, the formatting does not.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.title("About Sketch")
        self.geometry("440x400")
        self.transient(parent)

        txt_about = tk.Text(self, wrap=tk.WORD, padx=10, pady=10,
                            background="#ACAA60", relief=tk.FLAT)
        txt_about.insert("1.0", ABOUT)
        txt_about.config(state=tk.DISABLED)
        txt_about.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        btn_okay = tk.Button(self, text="Okay", command=self.destroy)
        btn_okay.pack(pady=5)

        self.grab_set()


class ControlPanel(tk.Frame):
    """Sixteen colours and sixteen widths, to choose one of each.

    The wx original keeps two maps of button id to value, and when one
    button goes down it looks the old one up and sends it back up by hand.
    A Tk Radiobutton with indicatoron=False is a button that stays down,
    and a group of them sharing a variable puts the old one up by itself.
    Two dictionaries and four lines of bookkeeping are not needed.
    """

    def __init__(self, parent, sketch):
        super().__init__(parent, relief=tk.RAISED, borderwidth=2)

        self.sketch = sketch
        self.swatches = {}

        self.colour = tk.StringVar(value=PALETTE[0])
        self.thickness = tk.IntVar(value=1)

        self.set_colour_grid()
        self.set_thickness_grid()

    def set_colour_grid(self):
        """One swatch per colour, four to a row."""
        frm_colours = tk.Frame(self)
        frm_colours.pack(padx=4, pady=4)

        for index, name in enumerate(PALETTE):
            self.swatches[name] = self.get_swatch(name.lower())

            tool = tk.Radiobutton(frm_colours, image=self.swatches[name],
                                  value=name, variable=self.colour,
                                  indicatoron=False, borderwidth=3,
                                  command=self.on_set_colour)
            tool.grid(row=index // PANEL_COLUMNS,
                      column=index % PANEL_COLUMNS, padx=1, pady=1)

    def set_thickness_grid(self):
        """One numbered button per width, four to a row."""
        frm_widths = tk.Frame(self)
        frm_widths.pack(padx=4, pady=4)

        for width in range(1, MAX_THICKNESS + 1):
            index = width - 1

            tool = tk.Radiobutton(frm_widths, text=str(width), width=2,
                                  value=width, variable=self.thickness,
                                  indicatoron=False, borderwidth=3,
                                  command=self.on_set_thickness)
            tool.grid(row=index // PANEL_COLUMNS,
                      column=index % PANEL_COLUMNS, padx=1, pady=1)

    def get_swatch(self, colour):
        """A small rectangle of one colour, drawn rather than loaded.

        put() is given a Tcl list of rows of colours, so a name with a
        space in it is read as two colours and "forest green" fails on
        "forest". Tk knows the same colours spelled without the space, so
        the space comes out.
        """
        swatch = tk.PhotoImage(width=SWATCH_WIDTH, height=SWATCH_HEIGHT)
        swatch.put(colour.replace(" ", ""),
                   to=(0, 0, SWATCH_WIDTH, SWATCH_HEIGHT))

        return swatch

    def on_set_colour(self):
        """The variable already holds it, and the old button is already up."""
        self.sketch.set_color(self.colour.get().lower().replace(" ", ""))

    def on_set_thickness(self):
        """Likewise."""
        self.sketch.set_thickness(self.thickness.get())


class Splash(tk.Toplevel):
    """What wx.SplashScreen is, made of a window with no decorations.

    overrideredirect(True) asks the window manager not to give it a title
    bar or a border, which is the whole of what a splash screen is. It
    takes itself away after a while with after().
    """

    def __init__(self, parent, milliseconds=SPLASH_MILLISECONDS):
        super().__init__(parent)

        self.overrideredirect(True)

        lbl_splash = tk.Label(self, text="Sketch!", font=("TkDefaultFont", 32),
                              background="#455481", foreground="white",
                              padx=60, pady=40)
        lbl_splash.pack()

        self.update_idletasks()
        self.set_centred()

        self.after(milliseconds, self.destroy)

    def set_centred(self):
        """In the middle of the screen, which wx does with a style flag."""
        x = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        y = (self.winfo_screenheight() - self.winfo_reqheight()) // 2

        self.geometry("+{}+{}".format(x, y))


class App(tk.Tk):
    """A sketch window with a menu, a toolbar and a status bar."""

    def __init__(self):
        super().__init__()

        self.title("Sketch Frame")
        self.geometry("800x600")

        self.colour = tk.StringVar(value=COLOURS[0])
        self.swatches = {}

        # The file this sketch came from, empty until it has one.
        self.filename = ""

        self.fields = self.get_status_bar()
        self.set_menu_bar()
        self.set_tool_bar()

        frm_main = tk.Frame(self)
        frm_main.pack(fill=tk.BOTH, expand=True)

        self.sketch = SketchWindow(frm_main)
        self.control = ControlPanel(frm_main, self.sketch)

        self.control.pack(side=tk.LEFT, fill=tk.Y)
        self.sketch.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.sketch.bind("<Motion>", self.on_sketch_motion)

        Splash(self)

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
                  ("Save As", "Save sketch file in a new file",
                   self.on_save_as),
                  ("", "", None),
                  ("Quit", "Quit", self.on_close_window))),
                ("Help",
                 (("About...", "Show about window", self.on_about),)),
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
        """Throw the sketch away and start again."""
        self.filename = ""
        self.sketch.set_lines_data([])

    def on_open(self):
        """Ask for a file and read it."""
        filename = filedialog.askopenfilename(parent=self,
                                              title="Open sketch file...",
                                              initialdir=os.getcwd(),
                                              filetypes=WILDCARD)

        if filename:
            self.filename = filename
            self.read_file()

    def on_save(self):
        """Write to the file this sketch came from, or ask for one."""
        if not self.filename:
            self.on_save_as()
        else:
            self.save_file()

    def on_save_as(self):
        """Ask for a name and write to it."""
        filename = filedialog.asksaveasfilename(parent=self,
                                                title="Save sketch as...",
                                                initialdir=os.getcwd(),
                                                defaultextension=".sketch",
                                                filetypes=WILDCARD)

        if filename:
            self.filename = filename
            self.save_file()

    def save_file(self):
        """Write the sketch out.

        A failure here has to be seen. A drawing that silently did not save
        is the worst outcome available, so the error goes in a box and the
        file name is forgotten, because it no longer holds this sketch.
        """
        try:
            with open(self.filename, "wb") as target:
                pickle.dump(self.sketch.get_lines_data(), target)
        except (OSError, pickle.PicklingError) as error:
            self.filename = ""
            messagebox.showerror("Save", "Could not save:\n{}".format(error),
                                 parent=self)

    def read_file(self):
        """Read a sketch in, and say so if it is not one."""
        try:
            with open(self.filename, "rb") as source:
                self.sketch.set_lines_data(pickle.load(source))
        except (OSError, pickle.UnpicklingError, EOFError,
                AttributeError, IndexError) as error:
            self.filename = ""
            messagebox.showerror("Open", "Not a sketch file:\n{}".format(error),
                                 parent=self)

    def on_about(self):
        """The about window, which is a Text and not a page."""
        SketchAbout(self)

    def on_close_window(self):
        """Shut the window."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
