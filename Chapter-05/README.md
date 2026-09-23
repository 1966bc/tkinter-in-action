# 5. Creating your blueprint

The chapter where the book stops showing widgets and starts arguing about
how to arrange a program. Almost none of it is about wxPython, which is why
almost all of it translates.

## Two windows that look the same

`badExample.py` and `goodExample.py` put the same window on the screen. The
first builds it in its constructor, one line per widget, the menu spelled
out item by item. The second describes it:

```python
def get_menu_data(self):
    return (("File",
             (("Open", self.on_open),
              ("Quit", self.on_close_window))),
            ("Edit",
             (("Copy", self.on_copy),
              ...
```

and then walks the description. Adding a menu item becomes adding a line of
data instead of adding four lines among forty.

Nothing about this is a translation - the wx and the Tkinter versions
differ only in the widget calls - but it is the most useful pattern in the
chapter, and it is the one that survives into real programs. A window
described by data can be built, checked, reordered and tested without
touching the code that builds it.

## The model

`abstractmodel.py` is fifteen lines and imports nothing:

```python
class AbstractModel:
    def add_listener(self, listener):
        self.listeners.append(listener)

    def update(self):
        for listener in self.listeners:
            listener(self)
```

`modelExample.py` puts it to work. Four buttons, two fields, and the
buttons do not write in the fields. They set the model; the model says it
has changed; the window, which asked to be told, goes and reads it.

### What Tkinter already has, and why this is still worth writing

wxPython has nothing like this, which is why the book has to build it.
Tkinter does:

```python
name = tk.StringVar()
name.trace_add("write", lambda *args: print("changed"))

ent_name = tk.Entry(self, textvariable=name)
lbl_name = tk.Label(self, textvariable=name)
```

A `StringVar` is an observable value. Set it and every widget showing it
redraws; `trace_add` puts a function on the change. The label and the entry
above stay in step without a line of code between them, and for two text
fields that is the whole of `modelExample.py` in four lines.

So why keep the model?

Because a `StringVar` observes **a value** and a model observes **a
thing**. `SimpleName` sets a first and a last name and calls `update()`
once, after both, so nobody ever sees a window with the new first name and
the old last one. Two `StringVar`s fire twice, in the order they happen to
be written, and a listener runs in between.

And because the model is where the rules go. A lot number that must exist
in the database, a result that is invalid until its control has passed, a
date that has to be a working day. None of that belongs to a widget, and a
`StringVar` has nowhere to put it.

The honest summary: use `StringVar` to keep a widget and a value in step,
which it does better than anything wx has. Use a model when there is
something to be right about.

### One small Tkinter awkwardness

The fields are read-only, which the book does with `wx.TE_READONLY`. Tk's
equivalent, `state="readonly"`, refuses `insert()` as firmly as it refuses
the keyboard - including when the program is the one writing. So writing to
one is three lines:

```python
entry.config(state="normal")
entry.delete(0, tk.END)
entry.insert(0, value)
entry.config(state="readonly")
```

A `Label` with `textvariable=` would have been simpler and is what one
would write if the book were not being followed.

## Testing a window

`testExample.py` calls the handler and asks the model what it holds. It
needs no window on the screen and is the reward for having separated the
two - which is the chapter's argument, made by the book itself rather than
asserted.

`testEventExample.py` goes further and presses the button. This is where wx
works hardest and Tkinter does least:

```python
# wx
event = wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wilma.GetId())
wilma.GetEventHandler().ProcessEvent(event)

# Tkinter
self.get_button("Wilmafy").invoke()
```

`invoke()` runs a widget's command exactly as a press would. There is no
event to build, no type to name and no id to find. Every test in this
project that presses something uses it.

One test was added that the book does not have, because it is the one that
proves the pattern rather than the plumbing: after pressing *Bettify*,
nothing wrote to the fields, and the fields say Betty Rubble anyway.

## The grid

Five files in this chapter are about `wx.grid`: `gridNoModel.py`,
`gridGeneric.py`, `gridModel.py`, `generictable.py`, `lineuptable.py`. They
are the chapter's second argument - that a grid without a table model is
built cell by cell and a grid with one is built row by row - and they are
the reason chapter 14 is not in this book.

**Tkinter has no grid widget.** Not a smaller one, not a different one:
there is no widget that displays a rectangular array of editable cells.

`gridNoModel.py` is translated anyway, because it only *shows* nine rows,
and showing rows is what a `ttk.Treeview` does. It is not a grid: the cells
cannot be typed in, a column cannot be given an editor, and there is no cell
cursor. It is a list with columns, which is the honest name for it.

The other four are about the table model - `wx.grid.PyGridTableBase`,
`GetValue`, `SetValue`, `GetNumberRows` - and there is nothing to attach
one to. They are left untranslated, and chapter 14 with them.

What one does instead, for a laboratory program that needs editable cells:
a `Treeview` for the rows, and an `Entry` placed over the cell that is
being edited, moved and filled on a double click and taken away when it
loses the focus. It works, everybody writes it, and it is fifty lines that
`wx.grid` does not ask for.

## The files

| file | state |
|---|---|
| `abstractmodel.py` | translated; no toolkit in it at all |
| `badExample.py` | translated |
| `goodExample.py` | translated |
| `modelExample.py` | translated |
| `gridNoModel.py` | translated as a `Treeview`, which is not a grid |
| `testExample.py` | translated |
| `testEventExample.py` | translated, with one test added |
| `generictable.py` | no: a `wx.grid` table model |
| `gridGeneric.py` | no |
| `gridModel.py` | no |
| `lineuptable.py` | no |

The file names keep the book's spelling, `badExample.py` and all. The
conventions of this project would write `bad_example.py`, and the mapping to
the original is worth more than the spelling: it is what makes a missing
file countable.
