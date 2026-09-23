#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  10.8 - How do I add a keyboard shortcut?
# source:   wxPythonInAction-src/Chapter-10/with_accelerator.py
# -----------------------------------------------------------------------------
"""Ctrl-A on the menu, and Ctrl-A actually working.

The trap of the chapter, and the same shape as the default button of
chapter 7: Tk's accelerator option **draws** the shortcut on the menu and
does not make it happen. It is a label. Pressing Ctrl-A does nothing at
all unless the key is bound separately.

wx has an accelerator table, which is a list of key, modifier and menu id,
handed to the frame. It is more ceremony and it cannot fall out of step
with what the menu says, because the menu id is in the table. Here the
label and the binding are written twice, and the day one is changed and
the other is not, the menu lies. See README.md.
"""
import tkinter as tk


class App(tk.Tk):
    """A window with a shortcut that is both shown and bound."""

    def __init__(self):
        super().__init__()

        self.title("Accelerator Example")
        self.geometry("380x140")

        mnu_bar = tk.Menu(self, tearoff=0)
        menu = tk.Menu(mnu_bar, tearoff=0)

        self.set_item(menu, "Accelerated", "Ctrl-A", "<Control-a>",
                      self.on_accelerated)
        self.set_item(menu, "Not accelerated", "", "", self.on_plain)

        menu.add_separator()
        menu.add_command(label="Exit", command=self.destroy)

        mnu_bar.add_cascade(label="Menu", underline=0, menu=menu)
        self.config(menu=mnu_bar)

        self.lbl_said = tk.Label(self, text="Try Ctrl-A, and the menu.")
        self.lbl_said.pack(expand=True)

    def set_item(self, menu, label, shown, sequence, handler):
        """One item, with its shortcut drawn and bound in one place.

        Writing them together is the answer to the trap: the label and
        the binding cannot disagree if they are arguments to the same
        call.
        """
        menu.add_command(label=label, accelerator=shown, command=handler)

        if sequence:
            # bind_all, not bind: the shortcut should work wherever the
            # keyboard focus is in the window, and bind on the window
            # alone is not reached once a widget has the focus.
            self.bind_all(sequence, lambda event: handler())

    def on_accelerated(self):
        """The accelerated one."""
        self.lbl_said.config(text="Accelerated item chosen.")

    def on_plain(self):
        """The other one."""
        self.lbl_said.config(text="Plain item chosen.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
