#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.8 - How do I make a wizard?
# source:   wxPythonInAction-src/Chapter-09/wizard.py
# -----------------------------------------------------------------------------
"""Four pages, Back and Next, and Finish at the end.

wx.wizard is a module: pages are chained with WizardPageSimple_Chain and
RunWizard walks them. Tkinter has nothing of the sort, and a wizard turns
out to be a short thing to write - which is why every toolkit that does
provide one provides a different one.

What is not short is the part this file does not have: a wizard whose
pages depend on the answers to earlier ones. The chain here is a list; in
a real one it is a question asked of the current page, and that is the
point at which a wizard stops being furniture and becomes a program.
"""
import tkinter as tk
from tkinter import ttk


TITLE_FONT = ("TkDefaultFont", 18, "bold")


class TitledPage(tk.Frame):
    """One page: a heading, a rule, and room underneath."""

    def __init__(self, parent, title):
        super().__init__(parent)

        lbl_title = tk.Label(self, text=title, font=TITLE_FONT)
        lbl_title.pack(anchor=tk.CENTER, pady=5)

        rule = ttk.Separator(self, orient=tk.HORIZONTAL)
        rule.pack(fill=tk.X, padx=5, pady=5)


class Wizard(tk.Toplevel):
    """A window showing one page at a time, with Back, Next and Cancel."""

    def __init__(self, parent, title):
        super().__init__(parent)

        self.title(title)
        self.geometry("420x300")
        self.transient(parent)

        self.pages = []
        self.index = 0
        self.finished = False

        self.frm_pages = tk.Frame(self)
        self.frm_pages.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        rule = ttk.Separator(self, orient=tk.HORIZONTAL)
        rule.pack(fill=tk.X)

        frm_buttons = tk.Frame(self)
        frm_buttons.pack(anchor=tk.E, padx=10, pady=10)

        self.btn_back = tk.Button(frm_buttons, text="< Back",
                                  command=self.on_back)
        self.btn_back.pack(side=tk.LEFT, padx=5)

        self.btn_next = tk.Button(frm_buttons, text="Next >",
                                  command=self.on_next)
        self.btn_next.pack(side=tk.LEFT, padx=5)

        btn_cancel = tk.Button(frm_buttons, text="Cancel",
                               command=self.destroy)
        btn_cancel.pack(side=tk.LEFT, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def add_page(self, page):
        """Pages are shown in the order they were added."""
        self.pages.append(page)

        return page

    def show_page(self):
        """Put the current page up and set the buttons to match it."""
        for page in self.pages:
            page.pack_forget()

        self.pages[self.index].pack(fill=tk.BOTH, expand=True)

        state = tk.NORMAL

        if self.index == 0:
            state = tk.DISABLED

        self.btn_back.config(state=state)

        if self.index == len(self.pages) - 1:
            self.btn_next.config(text="Finish")
        else:
            self.btn_next.config(text="Next >")

    def on_back(self):
        """One page back."""
        self.index = self.index - 1
        self.show_page()

    def on_next(self):
        """One page on, or finish if this was the last."""
        if self.index == len(self.pages) - 1:
            self.finished = True
            self.destroy()
        else:
            self.index = self.index + 1
            self.show_page()

    def run(self):
        """Show the first page and wait. True if it reached the end."""
        self.show_page()
        self.grab_set()
        self.wait_window()

        return self.finished


def main():
    """Four pages, and a word about how it went."""
    root = tk.Tk()
    root.withdraw()

    wizard = Wizard(root, "Simple Wizard")

    first = wizard.add_page(TitledPage(wizard.frm_pages, "Page 1"))
    wizard.add_page(TitledPage(wizard.frm_pages, "Page 2"))
    wizard.add_page(TitledPage(wizard.frm_pages, "Page 3"))
    last = wizard.add_page(TitledPage(wizard.frm_pages, "Page 4"))

    lbl_first = tk.Label(first, text="Testing the wizard")
    lbl_first.pack()

    lbl_last = tk.Label(last, text="This is the last page.")
    lbl_last.pack()

    if wizard.run():
        print("Success")

    root.destroy()


if __name__ == "__main__":
    main()
