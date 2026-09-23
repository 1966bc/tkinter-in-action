#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.2 - How do I make a button with a picture on it?
# source:   wxPythonInAction-src/Chapter-07/bitmap_button.py
# -----------------------------------------------------------------------------
"""Two buttons with a picture instead of a word.

The original loads bitmap.bmp, which belongs to the book and which Tk
cannot read in any case. The picture here is drawn, as in chapter 6.
"""
import tkinter as tk


WIDTH = 40
HEIGHT = 30


class App(tk.Tk):
    """Two picture buttons, both of which close the window."""

    def __init__(self):
        super().__init__()

        self.title("Bitmap Button Example")
        self.geometry("200x150")

        # Held on self, or it is collected and both buttons go blank.
        self.bitmap = self.get_bitmap()

        self.btn_first = tk.Button(self, image=self.bitmap,
                                   default=tk.ACTIVE, command=self.on_click)
        self.btn_first.place(x=10, y=20)

        # The second has style=0 in the original, which means no border.
        self.btn_second = tk.Button(self, image=self.bitmap, relief=tk.FLAT,
                                    borderwidth=0, command=self.on_click)
        self.btn_second.place(x=100, y=20)

        self.bind("<Return>", lambda event: self.btn_first.invoke())
        self.btn_first.focus_set()

    def get_bitmap(self):
        """A small picture, drawn rather than loaded."""
        bitmap = tk.PhotoImage(width=WIDTH, height=HEIGHT)
        bitmap.put("navy", to=(0, 0, WIDTH, HEIGHT))
        bitmap.put("gold", to=(6, 6, WIDTH - 6, HEIGHT - 6))

        return bitmap

    def on_click(self):
        """Either of them shuts the window, as in the original."""
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
