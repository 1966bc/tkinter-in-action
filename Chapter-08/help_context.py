#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  8.2 - How do I add a context help button?
# source:   wxPythonInAction-src/Chapter-08/help_context.py
# -----------------------------------------------------------------------------
"""The little question mark in the title bar - which is not here.

wx.FRAME_EX_CONTEXTHELP puts a "?" next to the close button; clicking it
and then a widget shows that widget's help. It is a Windows arrangement,
and wx says so: on GTK the flag does nothing at all.

Tkinter cannot ask for it on any platform. What a title bar has on it is
the window manager's business, and the only parts of it Tk can touch are
whether the window can be resized and whether it has decorations at all.

So this file shows what is available instead: a tooltip, which is a
Toplevel with no decorations shown near the pointer, and which nothing in
the standard library provides either.
"""
import tkinter as tk


DELAY = 500


class ToolTip:
    """A little yellow window that appears when the pointer waits.

    Not a widget: a thing that watches one. It has no parent of its own
    and no place in the layout, and it has to take itself away again,
    which is most of the work.
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.window = None
        self.pending = None

        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Button-1>", self.on_leave)

    def on_enter(self, event):
        """Wait a moment before showing, as every tooltip does."""
        self.pending = self.widget.after(DELAY, self.show)

    def on_leave(self, event):
        """Take it away, and cancel it if it has not appeared yet."""
        if self.pending is not None:
            self.widget.after_cancel(self.pending)
            self.pending = None

        if self.window is not None:
            self.window.destroy()
            self.window = None

    def show(self):
        """Put it just below and to the right of the widget."""
        self.pending = None

        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 2

        self.window = tk.Toplevel(self.widget)
        self.window.overrideredirect(True)
        self.window.geometry("+{}+{}".format(x, y))

        lbl_text = tk.Label(self.window, text=self.text, justify=tk.LEFT,
                            background="#ffffe0", relief=tk.SOLID,
                            borderwidth=1, padx=4, pady=2)
        lbl_text.pack()


class App(tk.Tk):
    """A window with no help button and some help anyway."""

    def __init__(self):
        super().__init__()

        self.title("Help Context")
        self.geometry("300x100")

        # What Tk can say about a title bar: this window does not resize.
        # wx turns the minimise and maximise boxes off to make room for
        # the question mark; Tk has no separate word for either box.
        self.resizable(False, False)

        ent_lot = tk.Entry(self, width=20)
        ent_lot.place(x=20, y=35)
        ToolTip(ent_lot, "The lot number, as printed on the box.\n"
                         "Six digits, no letters.")

        lbl_hint = tk.Label(self, text="Rest the pointer on the field.")
        lbl_hint.place(x=20, y=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
