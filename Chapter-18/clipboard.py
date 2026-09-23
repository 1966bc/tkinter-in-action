#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  18.1 - How do I use the clipboard?
# source:   wxPythonInAction-src/Chapter-18/clipboard.py
# -----------------------------------------------------------------------------
"""Copy from one field, paste into another, through the clipboard.

wx opens the clipboard, puts a wx.TextDataObject in it and closes it
again, and the opening and closing matter: a clipboard left open is a
clipboard nobody else can use.

Tkinter has three methods on any widget and no opening at all. What it
does have is one surprise, and it is on the paste. See README.md.
"""
import tkinter as tk


class App(tk.Tk):
    """Two fields and the clipboard between them."""

    def __init__(self):
        super().__init__()

        self.title("Clipboard")
        self.geometry("420x200")

        lbl_from = tk.Label(self, text="Copy from here:")
        lbl_from.pack(anchor=tk.W, padx=15, pady=(15, 0))

        self.ent_from = tk.Entry(self, width=44)
        self.ent_from.insert(0, "QC-2201 glucose 5.31 mmol/L")
        self.ent_from.pack(padx=15)

        frm_buttons = tk.Frame(self)
        frm_buttons.pack(pady=10)

        btn_copy = tk.Button(frm_buttons, text="Copy", command=self.on_copy)
        btn_copy.pack(side=tk.LEFT, padx=5)

        btn_paste = tk.Button(frm_buttons, text="Paste",
                              command=self.on_paste)
        btn_paste.pack(side=tk.LEFT, padx=5)

        lbl_to = tk.Label(self, text="Paste into here:")
        lbl_to.pack(anchor=tk.W, padx=15)

        self.ent_to = tk.Entry(self, width=44)
        self.ent_to.pack(padx=15)

        self.lbl_said = tk.Label(self, anchor=tk.W, relief=tk.SUNKEN,
                                 borderwidth=1)
        self.lbl_said.pack(side=tk.BOTTOM, fill=tk.X)

    def on_copy(self):
        """Put the text on the clipboard.

        clear then append, in that order: append adds to what is already
        there, so without the clear a second copy would give both.
        """
        self.clipboard_clear()
        self.clipboard_append(self.ent_from.get())

        self.lbl_said.config(text="Copied.")

    def on_paste(self):
        """Take the text off the clipboard, if there is any.

        clipboard_get() raises TclError when the clipboard is empty or
        holds something that is not text - a picture from a browser, for
        instance. It does not return an empty string, so a paste button
        that does not catch this is a traceback waiting for a Tuesday.
        """
        try:
            text = self.clipboard_get()
        except tk.TclError:
            self.lbl_said.config(text="Nothing on the clipboard to paste.")
        else:
            self.ent_to.delete(0, tk.END)
            self.ent_to.insert(0, text)
            self.lbl_said.config(text="Pasted.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
