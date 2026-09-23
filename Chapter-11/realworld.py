#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  11.4 - Can I see a real-world example of sizers in action?
# source:   wxPythonInAction-src/Chapter-11/realworld.py
# -----------------------------------------------------------------------------
"""An account form: a heading, a rule, six labelled fields, two buttons.

Nested sizers become nested frames. The three empty wx items that
space the buttons become three empty grid columns with a weight.
"""
import tkinter as tk
from tkinter import ttk


# The borders of the original: 5 around the heading and inside the field
# grid, 10 around the grid itself and under the buttons.
SMALL_BORDER = 5
BIG_BORDER = 10

# wx asks for its city, state and zip fields in pixels, 150, 50 and 70.
# A ttk.Entry counts characters, which is the more useful unit for a form:
# a postcode is five digits whatever the font.
STATE_WIDTH = 4
ZIP_WIDTH = 7

FILL_X = tk.E + tk.W

# The six rows of the form. An empty label is the second address line, which
# in the original is an empty 10x10 spacer in the left hand column.
FIELDS = ("Name:", "Address:", "", "City, State, Zip:", "Phone:", "Email:")


class App(tk.Tk):
    """A form for an account, laid out with nested frames."""

    def __init__(self):
        super().__init__()

        self.title("Real World Test")

        style = ttk.Style(self)
        style.configure("Heading.TLabel", font=("TkDefaultFont", 18, "bold"))

        lbl_top = ttk.Label(self, text="Account Information",
                            style="Heading.TLabel")
        lbl_top.grid(row=0, column=0, sticky=tk.W, padx=SMALL_BORDER,
                     pady=SMALL_BORDER)

        rule = ttk.Separator(self, orient=tk.HORIZONTAL)
        rule.grid(row=1, column=0, sticky=FILL_X, pady=SMALL_BORDER)

        frm_fields = self.build_fields()
        frm_fields.grid(row=2, column=0, sticky=FILL_X, padx=BIG_BORDER,
                        pady=BIG_BORDER)

        frm_buttons = self.build_buttons()
        frm_buttons.grid(row=3, column=0, sticky=FILL_X, pady=(0, BIG_BORDER))

        self.grid_columnconfigure(0, weight=1)

        # What SetSizeHints() does: the window may grow but not shrink below
        # the size its contents asked for.
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())

    def build_fields(self):
        """The two column grid of labels and entries."""
        frm_fields = ttk.Frame(self)

        for row, text in enumerate(FIELDS):
            lbl_field = ttk.Label(frm_fields, text=text)
            lbl_field.grid(row=row, column=0, sticky=tk.E,
                           padx=(0, SMALL_BORDER), pady=SMALL_BORDER)

            if text == "City, State, Zip:":
                field = self.build_city(frm_fields)
            else:
                field = ttk.Entry(frm_fields)

            field.grid(row=row, column=1, sticky=FILL_X, pady=SMALL_BORDER)

        # The column of fields takes the width, the column of labels does not.
        frm_fields.grid_columnconfigure(1, weight=1)

        return frm_fields

    def build_city(self, parent):
        """City, state and postcode in one row, the city taking the width."""
        frm_city = ttk.Frame(parent)

        ent_city = ttk.Entry(frm_city)
        ent_city.grid(row=0, column=0, sticky=FILL_X)

        ent_state = ttk.Entry(frm_city, width=STATE_WIDTH)
        ent_state.grid(row=0, column=1, padx=SMALL_BORDER)

        ent_zip = ttk.Entry(frm_city, width=ZIP_WIDTH)
        ent_zip.grid(row=0, column=2)

        frm_city.grid_columnconfigure(0, weight=1)

        return frm_city

    def build_buttons(self):
        """Two buttons with elastic space before, between and after them."""
        frm_buttons = ttk.Frame(self)

        btn_save = ttk.Button(frm_buttons, text="Save")
        btn_save.grid(row=0, column=1)

        btn_cancel = ttk.Button(frm_buttons, text="Cancel")
        btn_cancel.grid(row=0, column=3)

        # The spacers. Columns 0, 2 and 4 hold nothing and share the width
        # equally, which is what the three empty wx items of proportion 1 do.
        for column in (0, 2, 4):
            frm_buttons.grid_columnconfigure(column, weight=1)

        return frm_buttons


if __name__ == "__main__":
    app = App()
    app.mainloop()
