#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.10 - How do I keep the menu in step with the program?
# source:   wxPythonInAction-src/Chapter-10/update_ui.py
# -----------------------------------------------------------------------------
"""Items that turn themselves off when they have nothing to act on.

wx has EVT_UPDATE_UI: before a menu is shown - and at idle moments - wx
asks each item whether it should be enabled, ticked or renamed, and the
handler answers. The program never has to remember to keep the menu
right, because it is asked.

Tkinter has no such event. What it has is postcommand, a function the
menu calls just before it is posted, and that is the place to put the
same answers. It fires once for the whole menu rather than once per item,
and only when the menu is opened, which is enough: nobody can choose an
item on a menu that is not open. See README.md.
"""
import tkinter as tk


class App(tk.Tk):
    """A window whose Edit menu knows whether there is anything to edit."""

    def __init__(self):
        super().__init__()

        self.title("Update UI Example")
        self.geometry("420x200")

        mnu_bar = tk.Menu(self, tearoff=0)

        # postcommand is the whole of the translation.
        self.menu = tk.Menu(mnu_bar, tearoff=0,
                            postcommand=self.on_update_ui)

        self.menu.add_command(label="Cut", command=self.on_cut)
        self.menu.add_command(label="Clear", command=self.on_clear)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Edit", underline=0, menu=self.menu)
        self.config(menu=mnu_bar)

        lbl_hint = tk.Label(self, justify=tk.LEFT,
                            text="Type something, then open the Edit menu.\n"
                                 "Empty the field and open it again.")
        lbl_hint.pack(pady=10)

        self.ent_text = tk.Entry(self, width=30)
        self.ent_text.pack()

        self.lbl_said = tk.Label(self, text="")
        self.lbl_said.pack(pady=10)

    def on_update_ui(self):
        """Called by the menu, just before it opens.

        Everything the menu needs to know about the state of the program
        is worked out here, in one place, at the one moment it matters.
        """
        state = tk.DISABLED

        if self.ent_text.get():
            state = tk.NORMAL

        self.menu.entryconfig("Cut", state=state)
        self.menu.entryconfig("Clear", state=state)

    def on_cut(self):
        """Take the text and put it on the clipboard."""
        self.clipboard_clear()
        self.clipboard_append(self.ent_text.get())
        self.ent_text.delete(0, tk.END)
        self.lbl_said.config(text="Cut.")

    def on_clear(self):
        """Just take it."""
        self.ent_text.delete(0, tk.END)
        self.lbl_said.config(text="Cleared.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
