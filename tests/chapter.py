#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Makes `import images` mean this chapter's images, and not another's.

The book gives the same name to different files in different chapters:
images.py is in chapters 2, 4 and 8, spare.py is in 1 and 4, and the
examples import each other by bare name because each was meant to be run
from its own directory.

One test run is one process, and Python keeps modules by name. So the
first images.py imported is the one every later chapter gets, silently,
and the failures that follow are about attributes that exist in the wrong
file. Eleven of them, the first time chapter 8 was added.

Calling use() in setUp puts this chapter's directory first and forgets any
example module loaded from a different one.
"""
import os
import sys


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = os.path.join(ROOT, "Chapter-")


def use(chapter):
    """Make a chapter's directory the one that a plain import finds."""
    directory = os.path.join(ROOT, chapter)

    while directory in sys.path:
        sys.path.remove(directory)

    sys.path.insert(0, directory)

    for name, module in list(sys.modules.items()):
        origin = getattr(module, "__file__", None) or ""

        if origin.startswith(CHAPTERS):
            if not origin.startswith(directory + os.sep):
                del sys.modules[name]
