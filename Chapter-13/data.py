#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  13.1 - The rows the list examples show
# source:   wxPythonInAction-src/Chapter-13/data.py
# -----------------------------------------------------------------------------
"""Something for the list examples to show.

The same shape as the original - an identifier, a summary, a date and a
name - so that the examples look like the book's. The rows are not the
book's: the original code stays in forge/ and is not copied here, which
is what the front matter of this book says.

The identifier column is the one that matters for list_report_colsort.py.
Sorted as text, 9 comes after 10, and a column of numbers that sorts as
text is wrong in a way somebody notices late.
"""

COLUMNS = ("Request ID", "Summary", "Date", "Submitted By")

ROWS = (("9", "Listbox does not scroll on its own", "2026-03-02", "bc"),
        ("10", "Treeview headings ignore the theme font", "2026-03-04", "bc"),
        ("104", "after() outlives the window that asked", "2026-04-11", "rm"),
        ("17", "Menu tearoff entry shifts every index", "2026-04-19", "ag"),
        ("212", "PhotoImage collected while still shown", "2026-05-02", "bc"),
        ("3", "grid uniform swallows an exact gap", "2026-05-08", "rm"),
        ("88", "Accelerator label is not a binding", "2026-06-01", "ag"),
        ("150", "No JPEG without Pillow", "2026-06-14", "bc"),
        ("42", "Canvas keeps what a device context forgets", "2026-07-03", "rm"),
        ("7", "Frame cannot be scrolled", "2026-07-21", "ag"),
        ("99", "Virtual event carries no data", "2026-08-05", "bc"),
        ("1001", "No grid widget at all", "2026-08-30", "rm"),
        ("23", "Radio group is a variable, not an order", "2026-09-06", "ag"),
        ("5", "validatecommand refuses, trace apologises", "2026-09-12", "bc"),
        ("310", "Shaped windows are not possible on X11", "2026-09-19", "rm"))

# Which columns hold numbers. Anything not here sorts as text.
NUMERIC = ("Request ID",)
