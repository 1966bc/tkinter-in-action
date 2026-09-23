#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  4.2 - What is PyCrust and what can it do for me?
# source:   wxPythonInAction-src/Chapter-04/pycrust-foundation.py
# -----------------------------------------------------------------------------
"""A window, and a Python prompt looking at it while it runs.

wxPython ships PyCrust, which is an application written in wxPython. Python
ships IDLE, which is an application written in Tkinter. Neither is a feature
of the toolkit, and neither can be imported into your own window - so this
is a small one that can. See README.md.
"""
import code
import contextlib
import io
import tkinter as tk
from tkinter import ttk

import images


BANNER = "The window is called app. Try: app.title('changed')"

# What not to show in the namespace tree: it is long, it is the same in
# every program, and none of it is what anybody opened the tree to look at.
HIDDEN = ("__builtins__", "__loader__", "__spec__")


class ShellWindow(tk.Toplevel):
    """A Python prompt, with a namespace given to it from outside.

    code.InteractiveConsole does the language part - compiling, deciding
    whether a statement is finished, keeping the state between lines. What
    is left is a Text to type in and somewhere to put what comes back.
    """

    def __init__(self, parent, namespace, banner=""):
        super().__init__(parent)

        self.title("Shell")
        self.geometry("560x320")

        self.console = code.InteractiveConsole(namespace)

        self.txt_shell = tk.Text(self, wrap=tk.WORD, background="white",
                                 insertbackground="black")
        self.txt_shell.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self, command=self.txt_shell.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_shell.config(yscrollcommand=scrollbar.set)

        self.txt_shell.bind("<Return>", self.on_return)

        if banner:
            self.write(banner + "\n")

        self.write(">>> ")

    def write(self, text):
        """Put text at the end and keep it in view."""
        self.txt_shell.insert(tk.END, text)
        self.txt_shell.see(tk.END)

    def get_last_line(self):
        """What was typed after the prompt on the line the cursor is on."""
        line = self.txt_shell.get("insert linestart", "insert lineend")
        source = line

        if line.startswith(">>> ") or line.startswith("... "):
            source = line[4:]

        return source

    def on_return(self, event):
        """Run the line and show what it said.

        "break" is returned because the Text would otherwise insert its own
        newline afterwards, and the prompt would end up on the wrong line.
        """
        source = self.get_last_line()
        self.write("\n")

        caught = io.StringIO()
        more = False

        try:
            with contextlib.redirect_stdout(caught):
                with contextlib.redirect_stderr(caught):
                    more = self.console.push(source)
        except SystemExit:
            self.write("(exit ignored in a window)\n")

        self.write(caught.getvalue())

        if more:
            self.write("... ")
        else:
            self.write(">>> ")

        return "break"


class NamespaceWindow(tk.Toplevel):
    """What PyCrust calls Filling: the namespace, as a tree.

    wx.py.filling.FillingFrame walks the objects it is given and shows what
    is in them. A Treeview over dir() is the same idea, filled a level at a
    time as branches are opened, because a namespace is deep enough that
    walking it all at once is not a good idea.
    """

    def __init__(self, parent, namespace):
        super().__init__(parent)

        self.title("Namespace")
        self.geometry("420x360")

        self.namespace = namespace

        self.trv_names = ttk.Treeview(self, columns=("value",))
        self.trv_names.heading("#0", text="name")
        self.trv_names.heading("value", text="value")
        self.trv_names.column("#0", width=180)
        self.trv_names.pack(fill=tk.BOTH, expand=True)

        self.trv_names.bind("<<TreeviewOpen>>", self.on_open)

        for name in sorted(namespace):
            if name not in HIDDEN:
                self.add_node("", name, namespace[name])

    def add_node(self, parent, name, value):
        """One row, with a dummy child so that it can be opened."""
        node = self.trv_names.insert(parent, tk.END, text=name,
                                     values=(repr(value)[:80],))

        if not isinstance(value, (int, float, str, bytes, bool, type(None))):
            self.trv_names.insert(node, tk.END, text="")

        return node

    def get_object(self, node):
        """The thing a row stands for, found by following the names down."""
        names = []
        walker = node

        while walker:
            names.insert(0, self.trv_names.item(walker, "text"))
            walker = self.trv_names.parent(walker)

        found = self.namespace.get(names[0])

        for name in names[1:]:
            found = getattr(found, name, None)

        return found

    def on_open(self, event):
        """Fill a branch the first time it is asked for."""
        node = self.trv_names.focus()
        children = self.trv_names.get_children(node)

        if len(children) == 1 and not self.trv_names.item(children[0], "text"):
            self.trv_names.delete(children[0])
            found = self.get_object(node)

            for name in sorted(dir(found)):
                if not name.startswith("__"):
                    self.add_node(node, name, getattr(found, name, None))


class App(tk.Tk):
    """The window of chapter 2, with a shell and a namespace watching it."""

    def __init__(self):
        super().__init__()

        self.title("Toolbars")
        self.geometry("300x200")

        self.images = {"new": images.get_new_image()}

        self.set_menu()
        self.set_toolbar()
        self.set_status_bar()

        namespace = {"app": self, "tk": tk}

        self.shell = ShellWindow(self, namespace, BANNER)
        self.names = NamespaceWindow(self, namespace)

    def set_menu(self):
        """File and Edit, as in the original."""
        mnu_bar = tk.Menu(self)

        mnu_file = tk.Menu(mnu_bar, tearoff=0)
        mnu_bar.add_cascade(label="File", underline=0, menu=mnu_file)

        mnu_edit = tk.Menu(mnu_bar, tearoff=0)
        mnu_bar.add_cascade(label="Edit", underline=0, menu=mnu_edit)

        mnu_edit.add_command(label="Copy", underline=0)
        mnu_edit.add_command(label="Cut", underline=1)
        mnu_edit.add_command(label="Paste", underline=0)
        mnu_edit.add_separator()
        mnu_edit.add_command(label="Options...", underline=0)

        self.config(menu=mnu_bar)

    def set_toolbar(self):
        """A Frame of flat buttons, as in chapter 2."""
        frm_toolbar = tk.Frame(self, borderwidth=1, relief=tk.RAISED)

        btn_new = tk.Button(frm_toolbar, image=self.images["new"],
                            relief=tk.FLAT)
        btn_new.pack(side=tk.LEFT, padx=2, pady=2)

        frm_toolbar.pack(side=tk.TOP, fill=tk.X)

    def set_status_bar(self):
        """A sunken Label, as in chapter 2."""
        lbl_status = tk.Label(self, text="Copy in status bar", borderwidth=1,
                              relief=tk.SUNKEN, anchor=tk.W)
        lbl_status.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    app = App()
    app.mainloop()
