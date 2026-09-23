#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  9.5 - How do I let somebody pick a picture?
# source:   wxPythonInAction-src/Chapter-09/image_box.py
# -----------------------------------------------------------------------------
"""A file chooser that shows what the file looks like.

wx.lib.imagebrowser is a contributed module: a directory, a list of the
pictures in it, and a preview. Tkinter has no such thing and filedialog
cannot be extended, so this is the whole dialog, and it is not much.

Pillow is not needed here and would be for anything but PNG and GIF, for
the reason chapter 1 gives.
"""
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog


SUFFIXES = (".png", ".gif", ".pgm", ".ppm")

PREVIEW = 260


class ImageDialog(simpledialog.Dialog):
    """A list of the pictures in a directory, with the chosen one shown."""

    def __init__(self, parent, directory):
        self.directory = directory
        self.names = self.get_names(directory)
        self.preview = None
        self.path = None

        super().__init__(parent, "Choose an image")

    def get_names(self, directory):
        """The pictures in a directory that Tk can open without help."""
        found = []

        for name in sorted(os.listdir(directory)):
            if name.lower().endswith(SUFFIXES):
                found.append(name)

        return found

    def body(self, master):
        """The list on the left, the picture on the right."""
        self.lst_names = tk.Listbox(master, width=28, height=14,
                                    exportselection=False)

        for name in self.names:
            self.lst_names.insert(tk.END, name)

        self.lst_names.grid(row=0, column=0, sticky=tk.NS)
        self.lst_names.bind("<<ListboxSelect>>", self.on_select)

        self.lbl_preview = tk.Label(master, width=PREVIEW, height=PREVIEW,
                                    relief=tk.SUNKEN, background="white")
        self.lbl_preview.grid(row=0, column=1, padx=8)

        return self.lst_names

    def on_select(self, event):
        """Show the chosen picture, or say why it cannot be shown."""
        selected = self.lst_names.curselection()

        if selected:
            name = self.names[selected[0]]
            path = os.path.join(self.directory, name)

            try:
                # Held on self, or it is collected before it is drawn.
                self.preview = tk.PhotoImage(file=path)
                self.lbl_preview.config(image=self.preview, text="")
            except tk.TclError as error:
                self.preview = None
                self.lbl_preview.config(image="", text=str(error),
                                        wraplength=PREVIEW - 20)

    def apply(self):
        """On OK only."""
        selected = self.lst_names.curselection()

        if selected:
            self.path = os.path.join(self.directory,
                                     self.names[selected[0]])


def main():
    """Ask for a directory, then for a picture in it."""
    root = tk.Tk()
    root.withdraw()

    directory = filedialog.askdirectory(parent=root,
                                        title="Which directory?",
                                        initialdir=os.getcwd())

    if directory:
        dialog = ImageDialog(root, directory)

        if dialog.path is not None:
            print("You Selected File: {}".format(dialog.path))

    root.destroy()


if __name__ == "__main__":
    main()
