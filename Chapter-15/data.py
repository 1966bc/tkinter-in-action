#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# chapter:  15.1 - The hierarchy the tree examples show
# source:   wxPythonInAction-src/Chapter-15/data.py
# -----------------------------------------------------------------------------
"""Something for the tree examples to show.

The original shows the class hierarchy of wxPython, which is theirs. This
is a laboratory one - sections, benches, instruments, methods - and has
the same shape: a root, branches of uneven depth, and leaves at the end.

A tree example needs a hierarchy that is deep enough in places and shallow
in others, or nothing in it is ever surprising.
"""

ROOT = "Laboratory"

# name, description, children
TREE = (
    ("Clinical Chemistry", "Routine and special chemistry", (
        ("Analyser A", "Main line, two modules", (
            ("Glucose", "Hexokinase, serum and plasma", ()),
            ("Creatinine", "Enzymatic, IDMS traceable", ()),
            ("Albumin", "Bromocresol purple", ()),
        )),
        ("Analyser B", "Backup line", (
            ("Sodium", "Indirect potentiometry", ()),
            ("Potassium", "Indirect potentiometry", ()),
        )),
    )),
    ("Mass Spectrometry", "LC-MS/MS and GC-MS", (
        ("LC-MS/MS", "Triple quadrupole", (
            ("Vitamin D", "25-OH D2 and D3", (
                ("Calibrators", "Six levels", ()),
                ("Controls", "Three levels, two lots", ()),
            )),
            ("Immunosuppressants", "Whole blood", (
                ("Tacrolimus", "", ()),
                ("Ciclosporin", "", ()),
            )),
        )),
        ("GC-MS", "Single quadrupole", (
            ("Organic acids", "Urine, derivatised", ()),
        )),
    )),
    ("Quality", "Everything that checks everything else", (
        ("Internal control", "Daily, per lot", ()),
        ("External assessment", "Four rounds a year", ()),
        ("Method validation", "Before a method is used", (
            ("Linearity", "", ()),
            ("Imprecision", "Within run and between run", ()),
            ("Comparison", "Against the method being replaced", ()),
        )),
    )),
)

COLUMNS = ("Name", "Description")
