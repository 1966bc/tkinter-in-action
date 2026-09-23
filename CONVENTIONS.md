# Tkinter in Action — Conventions

The rules this code is written by.

## The code

- **English in the code**: identifiers, comments, docstrings, interface.
- **PEP 8**: 4 spaces, lines up to 100 columns, `lower_case_with_underscores`
  for functions and variables, `CapWords` for classes. File names would
  follow the same rule, and here they do not: a translated file keeps the
  name the book gave it, `badExample.py` and `customEvent.py` included. The
  mapping to the original is worth more than the spelling, because it is
  what makes a missing file countable.
- **Böhm-Jacopini**: only sequence, `if`, loops and assignments. One exit per
  function: no `return` in the middle, no `break`/`continue`, no
  `x if condition else y`. `raise` is allowed, for real errors only.
- **The simplest thing that still reads in two years.** An example shows one
  thing, and nothing is written for an imagined future.
- `.format()` strings, not f-strings.
- **Nothing deprecated**: `trace_add('write', ...)`, not `trace('w', ...)`.
  An example that teaches a call the interpreter is about to take away
  teaches it twice.
- **Plain text in the source.** No check marks, no crosses, no boxes drawn
  with lines, no arrows. `+/-`, `<=`, `>=`, `->`. A letter with an accent on
  it is a letter and stays - Böhm is spelt Böhm - but a glyph that decorates
  a comment is noise in a diff and a question mark in somebody else's
  terminal.
- **No history in docstrings**: a docstring says what the thing does, not what
  it used to do. The story of a change belongs in its commit message.
- **No capitals for emphasis**, in comments, docstrings or commit messages.
  Capitals are how one shouts, and RFC 1855 - *Netiquette Guidelines*, 1995,
  section 2.1.1 - said so before most of this code existed. Hence
  `1966bc aka Giuseppe Costanzi` in the header, not `AKA`. This says nothing
  about file names: `README`, `LICENSE` and `CONVENTIONS` are capitals for a
  different reason, and it is not emphasis.

## Tkinter

- **`ttk` where a themed widget exists**, `tk` where it does not (`Canvas`,
  `Listbox`, `Text`, `Menu`, `Toplevel`). Not the two mixed inside one window
  without a reason.
- Widget prefixes: `lst_`, `cb_`, `txt_`, `lbl_`, `frm_`, `btn_`, `ent_`,
  `chk_`, `cnv_`, `trv_`.
- **Never assign the result of a geometry manager.** `.grid()`, `.pack()` and
  `.place()` return `None`. `lbl = tk.Label(...).grid(...)` puts `None` in
  `lbl`, and the day somebody reaches for `lbl` the traceback names the wrong
  line. Build the widget, then place it on the line after.

## The examples

- **The file is the unit.** Each example runs on its own and explains itself on
  its own. This is where DRY stops: two examples that build the same listbox
  keep their own copy. A shared helper module would make every file a jump to
  somewhere else, which is what a reader of a book chapter cannot afford.
  Repetition between examples is deliberate; repetition inside one is not.
- **A shebang on every file, and the executable bit with it**: here every file
  is a program, and one that could not be run would not be an example.
- File header block with `project: tkinter-in-action`, `authors: 1966bc aka
  Giuseppe Costanzi`, `licence: MIT, see LICENSE`, and the chapter and file of
  the book the example comes from.
- **No date in the header.** Git keeps the date of every file, exactly, and a
  date written by hand is right on the day it is typed and wrong from the next
  edit that forgets it. A reader who trusts it is worse off than one who has
  none. The one date this project has is the release date, and it lives once,
  in the top-level README.

### The parts of the header, by their names

Their order is fixed by the language, not by taste:

```python
#!/usr/bin/python3                     # shebang
# -*- coding: utf-8 -*-                # encoding declaration, PEP 263
"""project:  tkinter-in-action        # module docstring, PEP 257,
authors:  1966bc aka Giuseppe Costanzi #   holding header fields in the
licence:  MIT, see LICENSE             #   key: value form of RFC 822
chapter:  11.2 - Basic sizers
source:   wxPythonInAction-src/Chapter-11/basicgridsizer.py

What this example shows.
"""
__version__ = "0.1"                    # dunder, module metadata
from __future__ import annotations     # future statement
import tkinter as tk                   # imports
```

- **shebang**, from *hash* + *bang*. Not read by Python: the kernel looks at
  the first two bytes on `execve` and runs the named interpreter on the file.
  It therefore does nothing without the executable bit.
- **encoding declaration**, informally the *coding cookie*. Unnecessary since
  Python 3, where UTF-8 is the default. Not used here.
- **module docstring**. Not a comment but a string, the module's `__doc__`,
  readable at runtime with `help()`. This is why the header fields live inside
  it rather than in comments above it.
- **dunder**, from *double underscore*. PEP 8 puts these after the docstring
  and before the imports, `__future__` excepted.
- **future statement**. Must precede every other import.

## The book

- One directory per chapter, `Chapter-NN`, and **the same file name as the
  original**: `boxsizer.py` translates `Chapter-11/boxsizer.py`. The mapping is
  one to one, so what is missing can be counted.
- **Each chapter carries a `README.md`** saying what was translated, what was
  not, and what Tkinter does instead.
- **A "no" is a result.** A chapter with no Tkinter equivalent - the grid
  control, HTML, the printing framework - is not a hole to be left silent. It
  is written down, with the reason and with what one does in its place.
