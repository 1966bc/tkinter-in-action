#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.6 - How do I show a tip at startup?
# source:   wxPythonInAction-src/Chapter-09/startup_tip.py
# -----------------------------------------------------------------------------
"""The box of hints that some programs show when they open.

wx has wx.CreateFileTipProvider and wx.ShowTip: a file of lines, one shown
each time, and a box with Next and a "show these at startup" tick.

Tkinter has neither, and neither is much. What is worth taking from this
file is where the answer to the tick box goes: not in a variable, which
lasts as long as the program, but in a file beside the tips, which lasts
longer. A laboratory program that forgets the answer and asks again every
morning has not saved anybody anything.
"""
import os
import random
import tkinter as tk


HERE = os.path.dirname(os.path.abspath(__file__))
TIPS = os.path.join(HERE, "tips.txt")
SETTING = os.path.join(HERE, "tips.setting")


class TipDialog(tk.Toplevel):
    """One hint, with Next, and a tick to stop being shown them."""

    def __init__(self, parent, tips, index=0):
        super().__init__(parent)

        self.title("Tip of the Day")
        self.geometry("420x200")
        self.transient(parent)
        self.resizable(False, False)

        self.tips = tips
        self.index = index

        self.showing = tk.BooleanVar(value=True)

        lbl_title = tk.Label(self, text="Did you know...",
                             font=("TkDefaultFont", 14, "bold"))
        lbl_title.pack(anchor=tk.W, padx=15, pady=(15, 5))

        self.lbl_tip = tk.Label(self, text="", wraplength=380,
                                justify=tk.LEFT, anchor=tk.NW)
        self.lbl_tip.pack(fill=tk.BOTH, expand=True, padx=15)

        chk_showing = tk.Checkbutton(self, text="Show tips at startup",
                                     variable=self.showing)
        chk_showing.pack(anchor=tk.W, padx=15)

        frm_buttons = tk.Frame(self)
        frm_buttons.pack(anchor=tk.E, padx=15, pady=10)

        btn_next = tk.Button(frm_buttons, text="Next tip",
                             command=self.on_next)
        btn_next.pack(side=tk.LEFT, padx=5)

        btn_close = tk.Button(frm_buttons, text="Close",
                              command=self.on_close)
        btn_close.pack(side=tk.LEFT)

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_tip()

    def show_tip(self):
        """The one at the current index, wrapping round at the end."""
        if self.tips:
            self.lbl_tip.config(text=self.tips[self.index % len(self.tips)])

    def on_next(self):
        """The next one."""
        self.index = self.index + 1
        self.show_tip()

    def on_close(self):
        """Remember the answer to the tick before going."""
        set_showing(self.showing.get())
        self.destroy()


def get_tips(path):
    """The lines of the tips file, blank ones and comments left out."""
    tips = []

    if os.path.exists(path):
        for line in open(path, encoding="utf-8"):
            if line.strip() and not line.startswith("#"):
                tips.append(line.strip())

    return tips


def get_showing(path):
    """Whether tips were asked for. True the first time, having no file."""
    showing = True

    if os.path.exists(path):
        showing = open(path, encoding="utf-8").read().strip() != "no"

    return showing


def set_showing(showing):
    """Write the answer down where the next run will find it."""
    answer = "no"

    if showing:
        answer = "yes"

    open(SETTING, "w", encoding="utf-8").write(answer + "\n")


def main():
    """Show a tip, unless somebody said not to."""
    root = tk.Tk()
    root.withdraw()

    tips = get_tips(TIPS)

    if not tips:
        print("no tips in {}".format(TIPS))
    elif not get_showing(SETTING):
        print("tips turned off in {}".format(SETTING))
    else:
        TipDialog(root, tips, random.randrange(len(tips)))
        root.mainloop()


if __name__ == "__main__":
    main()
