#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  7.2 - What are the generic buttons for?
# source:   wxPythonInAction-src/Chapter-07/generic_button.py
# -----------------------------------------------------------------------------
"""The chapter's longest file in wx, and its shortest answer in Tkinter.

wx.lib.buttons exists because a wx.Button is the platform's button: it
looks like the rest of the desktop and cannot be told to be navy with
white letters, because the platform does not offer that. So wxPython
ships a set of buttons drawn in Python - GenButton, GenBitmapButton,
GenToggleButton, GenBitmapTextButton - which look the same everywhere and
can be styled.

A tk.Button is drawn by Tk on every platform already. Colour, font, bezel
width, a picture, a picture and a word together, staying down when
pressed: all of it is an option on the one widget, and the module has
nothing to add. See README.md.
"""
import tkinter as tk


GAP = 20

BIG_FONT = ("Helvetica", 20, "bold")


class App(tk.Tk):
    """Nine buttons, which in wx come from two different families."""

    def __init__(self):
        super().__init__()

        self.title("Generic Button Example")
        self.geometry("560x380")

        self.bitmap = self.get_bitmap()
        self.toggled = tk.BooleanVar()
        self.pressed = tk.BooleanVar()

        for column in range(3):
            self.grid_columnconfigure(column, weight=1)

        self.set_buttons()

    def get_bitmap(self):
        """A small picture, drawn rather than loaded."""
        bitmap = tk.PhotoImage(width=32, height=24)
        bitmap.put("navy", to=(0, 0, 32, 24))
        bitmap.put("gold", to=(4, 4, 28, 20))

        return bitmap

    def get_button_data(self):
        """Every button in the original, and what it is showing off."""
        return ((tk.Button(self, text="A tk.Button", default=tk.ACTIVE),
                 "the default one"),
                (tk.Button(self, text="non-default tk.Button"),
                 "an ordinary one"),
                (tk.Button(self, text="disabled", state=tk.DISABLED),
                 "GenButton with Enable(False)"),
                (tk.Button(self, text="bigger", font=BIG_FONT,
                           background="navy", foreground="white",
                           activebackground="navy",
                           activeforeground="white", borderwidth=5),
                 "GenButton restyled, which is why wx.lib.buttons exists"),
                (tk.Button(self, image=self.bitmap),
                 "GenBitmapButton"),
                (tk.Checkbutton(self, image=self.bitmap, indicatoron=False,
                                variable=self.toggled),
                 "GenBitmapToggleButton"),
                (tk.Button(self, image=self.bitmap, text="Bitmapped Text",
                           compound=tk.LEFT, width=175, height=75),
                 "GenBitmapTextButton: compound says where the word goes"),
                (tk.Checkbutton(self, text="Toggle Button", indicatoron=False,
                                variable=self.pressed),
                 "GenToggleButton"))

    def set_buttons(self):
        """Three to a row, with the same gaps as the original."""
        for index, entry in enumerate(self.get_button_data()):
            button, explanation = entry

            button.grid(row=index // 3, column=index % 3,
                        padx=GAP, pady=GAP)


if __name__ == "__main__":
    app = App()
    app.mainloop()
