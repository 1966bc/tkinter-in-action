#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  4.2 - What is PyCrust and what can it do for me?
# source:   wxPythonInAction-src/Chapter-04/images.py
# -----------------------------------------------------------------------------
"""The toolbar icon, carried in the source instead of in a file.

The same sixteen by fifteen pixels the book embeds, and the same PNG bytes.
See README.md for what the wx original needs three calls to do.
"""
import tkinter as tk


# base64 of the PNG. The wx original writes the raw bytes and decodes them
# at run time; Tk wants base64 and reads PNG itself since 8.6.
NEW_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAPCAYAAADtc08vAAAABHNCSVQICAgIfAhkiAAA"
    "AFlJREFUeJzt0zEKQCEMA9Ck/vvfWOPwl1KlKC4OZhPkNaKSVnCSzy/UqrLNtMIUAABp"
    "bpCEWlVEbKmnw2PLLYD8h3tkOEI2PULbDWZ5wA3A8A78Ha+Ep7+xA+EsGSaTmtKXAAAA"
    "AElFTkSuQmCC"
)


def get_new_image():
    """The icon, as a PhotoImage.

    There must be a Tk instance before this is called: a PhotoImage lives in
    a Tk interpreter and cannot be made without one.
    """
    return tk.PhotoImage(data=NEW_PNG)
