#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  5.2 - What is refactoring and why is it worth doing?
# source:   wxPythonInAction-src/Chapter-05/goodExample.py
# -----------------------------------------------------------------------------
"""badExample.py again, with the window described instead of built.

Each kind of widget gets two methods: one that says what there is to make,
and one that makes it. Adding a menu item becomes adding a line of data.
"""
import tkinter as tk


class App(tk.Tk):
    """A window built from its own description."""

    def __init__(self):
        super().__init__()

        self.title("Refactor Example")
        self.geometry("340x200")
        self.protocol("WM_DELETE_WINDOW", self.on_close_window)

        frm_panel = tk.Frame(self, background="white")
        frm_panel.pack(fill=tk.BOTH, expand=True)

        self.entries = {}

        self.set_menu_bar()
        self.set_text_fields(frm_panel)
        self.set_button_bar(frm_panel)

    def get_menu_data(self):
        """The menus, as data: a name, then its items."""
        return (("File",
                 (("Open", self.on_open),
                  ("Quit", self.on_close_window))),
                ("Edit",
                 (("Copy", self.on_copy),
                  ("Cut", self.on_cut),
                  ("Paste", self.on_paste),
                  ("", None),
                  ("Options...", self.on_options))))

    def get_button_data(self):
        """The buttons, as data: a label and what it does."""
        return (("<< PREV", self.on_prev),
                ("NEXT >>", self.on_next))

    def get_text_field_data(self):
        """The fields, as data: a caption and where it goes."""
        return (("First Name", (10, 50)),
                ("Last Name", (10, 80)))

    def set_menu_bar(self):
        """One menu per line of get_menu_data()."""
        mnu_bar = tk.Menu(self)

        for label, items in self.get_menu_data():
            mnu_bar.add_cascade(label=label, underline=0,
                                menu=self.get_menu(mnu_bar, items))

        self.config(menu=mnu_bar)

    def get_menu(self, parent, items):
        """One menu. An item with no label is a separator."""
        menu = tk.Menu(parent, tearoff=0)

        for label, handler in items:
            if label:
                menu.add_command(label=label, underline=0, command=handler)
            else:
                menu.add_separator()

        return menu

    def set_button_bar(self, parent, y_position=0):
        """The buttons in a row, each starting where the last one ended."""
        x_position = 80

        for label, handler in self.get_button_data():
            button = self.get_one_button(parent, label, handler,
                                         x_position, y_position)
            button.update_idletasks()
            x_position = x_position + button.winfo_reqwidth()

    def get_one_button(self, parent, label, handler, x_position, y_position):
        """One button, placed where it was told."""
        button = tk.Button(parent, text=label, command=handler)
        button.place(x=x_position, y=y_position)

        return button

    def set_text_fields(self, parent):
        """One captioned field per line of get_text_field_data()."""
        for label, position in self.get_text_field_data():
            self.set_captioned_text(parent, label, position)

    def set_captioned_text(self, parent, label, position):
        """A caption, and a field to the right of it."""
        x_position, y_position = position

        lbl_caption = tk.Label(parent, text=label, background="white")
        lbl_caption.place(x=x_position, y=y_position)

        entry = tk.Entry(parent, width=14, state="readonly")
        entry.place(x=x_position + 70, y=y_position)

        self.entries[label] = entry

    def on_prev(self):
        """Nothing yet."""
        pass

    def on_next(self):
        """Nothing yet."""
        pass

    def on_open(self):
        """Nothing yet."""
        pass

    def on_copy(self):
        """Nothing yet."""
        pass

    def on_cut(self):
        """Nothing yet."""
        pass

    def on_paste(self):
        """Nothing yet."""
        pass

    def on_options(self):
        """Nothing yet."""
        pass

    def on_close_window(self):
        """Shut the window."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
