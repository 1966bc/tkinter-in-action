# Tkinter in Action

The source code of *wxPython in Action* rewritten in Tkinter, chapter by
chapter and file by file — and a record of what came across, what needed
three options where there was one, and what did not arrive at all.

![Tkinter in Action](.github/social-preview.png)

## What this is

Thirteen chapters of examples, translated one to one: every file here
keeps the name of the file it translates, so the two can be read side by
side.

It is not a comparison and neither toolkit wins. Where they differ, the
difference is measured and written down, and that is all it is.

## Measured, not remembered

wxPython 4.2 still runs the book's code, twenty years on. So nothing here
is translated from the printed page: **each example is executed beside its
original and the two windows are compared by their geometry** — window
size, and the position and size of every widget in them.

`Chapter-11/basicgridsizer.py` returns a window of 310x85 with its
children at (0,0), (105,0), (210,0) and so on, and `wx.GridSizer` returns
the same numbers.

Matching numbers are not the point. Rounding differs, themes differ, fonts
differ. The numbers are for noticing when something differs by **more**
than that — because then there is a mechanism underneath, and that is the
interesting part. Three times in this project a claim that seemed obvious
turned out to be wrong when measured, and the chapters say so.

## Gallery

The three windows above are on the cover. These are the rest of the range,
each one an example in this repository, photographed by `tools/capture.py`
while it was running.

<table>
<tr>
<td width="50%" align="center">
<img src="Chapter-06/figures/example7.png" width="100%"><br>
<sub><b>chapter 6</b> — Sketch: a canvas, a control panel and a toolbar of
drawn swatches, with none of wx's double buffering because a canvas keeps
what is on it</sub>
</td>
<td width="50%" align="center">
<img src="Chapter-04/figures/pycrust-foundation-3.png" width="100%"><br>
<sub><b>chapter 4</b> — a Python prompt holding the window open beside it.
Fifty lines, on <code>code.InteractiveConsole</code></sub>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="Chapter-13/figures/list_report_etc.png" width="100%"><br>
<sub><b>chapter 13</b> — report mode, striped with a tag, which is what a
Treeview has instead of the rules a wx.ListCtrl can be asked for</sub>
</td>
<td width="50%" align="center">
<img src="Chapter-07/figures/generic_button.png" width="100%"><br>
<sub><b>chapter 7</b> — nine buttons that in wx come from two different
families and here are one widget with different options</sub>
</td>
</tr>
<tr>
<td width="50%" align="center">
<img src="Chapter-18/figures/worker_threads.png" width="100%"><br>
<sub><b>chapter 18</b> — workers reporting through a queue, because only
the thread that made the widgets may touch them</sub>
</td>
<td width="50%" align="center">
<img src="Chapter-08/figures/splitter.png" width="100%"><br>
<sub><b>chapter 8</b> — two panes and a bar between them; a
<code>ttk.PanedWindow</code> cannot be turned, so the menu that splits the
other way builds a new one</sub>
</td>
</tr>
</table>


## The chapters

| | chapter | files | notes |
|---|---|---|---|
| 1 | Welcome | 5/5 | no JPEG without Pillow; the image must be kept alive |
| 2 | A solid foundation | 5/5 | the output window, the choice dialog and the toolbar all built |
| 3 | Events | 4/4 | virtual events; `event.data` does not exist |
| 4 | Looking at a running program | 4/4 | a shell in fifty lines, on `code.InteractiveConsole` |
| 5 | Your blueprint | 7/11 | `StringVar` is the observer Tkinter already had |
| 6 | The building blocks | 7/7 | a canvas keeps what a device context forgets |
| 7 | The basic controls | 15/15 | `wx.lib.buttons` has nothing to translate to |
| 8 | Putting widgets in frames | 10/10 | no MDI, no shaped windows, no scrollable frame |
| 9 | Dialogs | 15/15 | Tk has a font chooser Python does not offer |
| 10 | Menus | 11/11 | an accelerator is a label, not a binding |
| 11 | Sizers | 12/12 | `uniform` cannot hold an exact gap |
| 12 | Images and drawing | 3/3 | scaling is by whole numbers |
| 13 | List controls | 4/8 | everything is text, and text sorts 10 before 9 |
| 15 | Tree controls | 6/6 | a virtual tree is easy where a virtual list was impossible |
| 18 | Other functionality | 3/8 | a queue in place of `wx.CallAfter` |

## Why some examples are missing

The counts above are not effort running out, and they are not a list of
holes in Tkinter. They are what happens when two toolkits are built on
different ideas.

**wxPython wraps the platform's widgets and ships one for every job.** A
grid, an HTML window, a printing framework, a wizard, a splash screen, a
progress dialog, MDI, and a second family of buttons for when the
platform's own cannot be restyled. The book has a chapter per widget
because there is a widget per chapter.

**Tk draws everything itself, from a smaller set of parts.** A canvas, a
text widget, a tree, three geometry managers, tags, variables, virtual
events. There are fewer of them and they are unusually deep — a `Text` has
tags on every platform where wx has to ask its platform nicely, a canvas
item is an object that can be moved and bound to a click, and a `Treeview`
is a table and a tree at once.

So the untranslated files fall into two kinds, and only one of them is a
gap.

**Where wx ships a widget and Tk expects you to assemble one**, the
example is here, because it was assembled: the wizard, the progress
dialog, the toolbar, the status bar, the tip of the day, the single-choice
dialog, the tooltip, the scrolled frame, the shell. Tens of lines each,
once. The real cost is not the lines — it is that wx ships one wizard and
every wxPython program has the same one, while here everybody writes their
own and no two are alike.

**Where the underlying idea is absent there is nothing to assemble from.**
Those are left out and named:

- **chapter 14, the grid control.** No widget shows a rectangular array of
  editable cells. A `Treeview` shows rows and columns and nothing in it
  can be typed into; an `Entry` placed over a cell is what everybody
  writes instead, and it is not a grid.
- **chapter 16, HTML.** No HTML widget, so `wx.html.HtmlWindow` has
  nowhere to go.
- **chapter 17, printing.** No printing framework. `Canvas.postscript()`
  writes out what is on a canvas, and that is all of it.
- and inside translated chapters, the files about those same things: the
  four grid files in chapter 5, icon and list and virtual mode in chapter
  13, drag and drop and sound and XRC in chapter 18.

The rule followed throughout is that **a file that could only be
translated by pretending is left out and named**. A recorded *no*, with
the reason and with what one does instead, is worth more than a file that
looks like an answer and is not — and it is what somebody choosing between
the two actually needs.

Each chapter's `README.md` has the list for that chapter.


## The other side of it: a widget is easy to build

The section above is only half an argument. The other half is that when
Tkinter has not got something, **making it is unusually cheap** — and that
is not a consolation, it follows from the same design.

A Tk widget is a `Frame` with things in it. There is no widget class
hierarchy to join, no platform whose conventions have to be satisfied, no
paint cycle to implement, no resource to register. A new widget composes
existing ones and inherits their behaviour for nothing: the keyboard
works, the theme applies, `place`, `pack` and `grid` accept it, and it can
be bound to like anything else.

This repository is the evidence rather than the claim. About twenty
widgets and dialogs were built in the course of translating the book,
none of them long:

| | where |
|---|---|
| `RadioBox`, `SimpleCombo` | chapter 7, where `wx.RadioBox` and `CB_SIMPLE` have no counterpart |
| `ScrolledWindow`, `MiniFrame`, `ToolTip` | chapter 8 |
| `ProgressBox`, `SingleChoiceDialog`, `ImageDialog`, `TipDialog`, `Wizard` | chapter 9 |
| `ShellWindow`, `NamespaceWindow` | chapter 4 — a Python prompt inside a running program |
| `OutputWindow` | chapter 2 — where `print()` goes when there is no terminal |
| `ControlPanel`, `Splash`, `SketchWindow` | chapter 6 |
| `RadarGraph` | chapter 12 |

The wizard is eighty lines. The tooltip is fifty. The shell is fifty, and
it runs statements against the window that is open beside it.

And a real one, in use rather than in a book:
[**Calendarium**](https://github.com/1966bc/Calendarium), a date picker.
The standard library has no calendar widget, so this is one — small,
self-contained, and used in the author's laboratory programs.

**The cost is agreement, not capability.** wxPython ships one wizard and
every wxPython program has the same one; wx.lib is full of contributed
widgets that everybody shares. Here, everybody's wizard is their own, no
two calendars are alike, and there is no equivalent body of agreed extra
widgets to draw on. Whether that is a price or a freedom depends on
whether you would rather learn somebody else's widget or write your own —
and in Tkinter, writing your own is genuinely a morning's work.


## Running it

Every file is a program and runs on its own:

```
python3 Chapter-06/example7.py
python3 Chapter-11/realworld.py
```

The tests need a display and nothing else:

```
python3 -m unittest discover -s tests -v
```

110 of them. They are not a formality: they found a silent module clash
across chapters, a repeating `after()` that outlived its window, and a
menu index that was off by one because of a tear-off line.

## Tools

| | |
|---|---|
| `tools/side_by_side.py` | opens an example and its wx original next to each other |
| `tools/record_wx_geometry.py` | records what the originals measure, as the tests' reference |
| `tools/capture.py` | takes the pictures used as figures |

Each chapter's `README.md` is written to be read straight through as well
as beside the code.

`side_by_side.py` needs wxPython and the book's own sources, which are not
part of this repository.

## What does not translate

Worth knowing before choosing a toolkit, and collected here from the
chapters that found it:

- **No grid control.** No widget displays a rectangular array of editable
  cells. A `Treeview` shows rows and columns and nothing in it can be
  typed into.
- **No MDI**, and no way to put one window inside another.
- **No scrollable frame.** A `Scrollbar` talks to a `Listbox`, a `Text`, a
  `Canvas`, a `Treeview` and an `Entry`. A `Frame` is not one of them.
- **No HTML widget**, and therefore no chapter 16.
- **No printing**, and therefore no chapter 17.
- **No shaped windows** on X11, and no context help button anywhere.
- **No drag and drop** in the standard library.
- **No JPEG, no BMP**, without Pillow.

And the other way round, things Tkinter has that wxPython does not: an
observable value in `StringVar`, text tags on every platform where wx asks
its platform nicely, `validatecommand` that refuses an edit before it
happens, and `invoke()`, which makes every button in this repository
testable in one line.

## Source and attribution

Rappin, Noel and Robin Dunn, *wxPython in Action*, Manning Publications,
2006.

The example code that accompanies the book is its authors'. **Nothing of
theirs is reproduced here** — not the code, not the sample data, not the
artwork. Where an example needs rows in a table or a picture on a button,
this repository has its own: the data has the same shape and different
contents, and the pictures are drawn in the source. The rows and the
pictures were never the lesson.

What is faithful in a translation is the code — the same calls, the same
structure, the same file names, the same behaviour — and that is followed
as closely as two different toolkits allow.

## Conventions

`CONVENTIONS.md`. Read it before adding a file.

## Licence

MIT, see `LICENSE`.

---

*autumnus MMXXVI*
