#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  5.3 - How do I separate the model from the view?
# source:   wxPythonInAction-src/Chapter-05/abstractmodel.py
# -----------------------------------------------------------------------------
"""A model that tells whoever asked to be told when it changes.

Fifteen lines, no toolkit, and it is the whole of the pattern. Nothing here
imports tkinter, which is the point: a model that knows what a window is is
not a model.
"""


class AbstractModel:
    """Something that holds data and says when it has changed.

    Whoever wants to know calls add_listener with a function. When the data
    changes, update() calls every one of them with the model itself, and
    they go and look at what they need.
    """

    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        """Ask to be told. The listener is anything that can be called."""
        self.listeners.append(listener)

    def remove_listener(self, listener):
        """Stop being told, which a window must do before it is destroyed."""
        self.listeners.remove(listener)

    def update(self):
        """Tell everybody. The model does not know who they are."""
        for listener in self.listeners:
            listener(self)
