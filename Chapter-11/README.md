# 11. Placing widgets with sizers

A wxPython sizer is an **object**. You build it, hand it children one by one
with `Add()`, give it options per child, attach it to the window with
`SetSizer()` and ask the window to fit itself around it with `Fit()`. The
layout is a thing you can hold, pass around and nest.

Tkinter has no such object. It has three **geometry managers**, and they are
methods called on the child itself: `pack()`, `grid()`, `place()`. The layout
is not a thing, it is an arrangement the parent remembers. Nothing is
created, nothing is attached, and the window sizes itself to its children
without being asked, so `Fit()` has no translation because it has no work to
do.

That is the chapter in one paragraph. Everything else follows from it.

| wxPython | Tkinter |
|---|---|
| `wx.GridSizer` | `grid()`, plus `minsize` to make the cells equal |
| `wx.FlexGridSizer` | `grid()`, plus `weight` on the rows and columns that grow |
| `wx.GridBagSizer` | `grid()` with `row`, `column`, `rowspan`, `columnspan` |
| `wx.BoxSizer` | `pack()` with `side` |
| `wx.StaticBoxSizer` | `ttk.LabelFrame` — the box is a widget, not a sizer |
| `Add(item, proportion, flag, border)` | `weight`, `sticky`, `padx`, `pady` |
| `SetSizer()` then `Fit()` | nothing: it happens |
| `AddGrowableCol(1, 2)` | `grid_columnconfigure(1, weight=2)` |
| `SetSizeHints()` | `minsize()` |
| an empty item of proportion 1 | an empty column with a `weight` |

## 11.2 The grid sizer

### basicgridsizer.py

Nine blocks, three by three, five pixels apart.

`hgap` and `vgap` are the space wx leaves *between* two cells, and nothing
outside the outermost ones. `padx` and `pady` pad a child on *both* sides, so
asking for `padx=GAP` would put the gap around the grid as well and double it
in the middle. The gap is asked for only on the side that faces another cell:
the left of every column but the first, the top of every row but the first.

The other half of what a `wx.GridSizer` promises — that every cell is the
same size whatever is in it — is not asked for here, because with nine
identical blocks the columns come out equal by themselves.

### mingridsizer.py — and the trap in `uniform`

One block is made 150x50 and all nine cells grow with it. This is what a
`wx.GridSizer` is for.

The obvious Tkinter answer is `uniform`: columns naming the same uniform
group are all given the width of the widest. It is the wrong answer, and the
reason is worth the space.

`uniform` measures **the whole column, padding included**. The gap of a
`wx.GridSizer` sits *between* cells, so the first column has none on its left
and asks for five pixels less than the others. `uniform` notices the
difference and levels everything up to the larger — adding a column's worth
of gap that wx never had. Measured, it gives a window of 465 pixels against
the 460 of wx, and the gap between the first two blocks opens to eight while
the next stays at five.

`uniform` and an exact gap cannot both be had. So the cell size is **stated**
with `minsize` rather than inferred, and `sticky=NW` puts the block in the
corner wx would put it in. `uniform` earns its place where there is no exact
gap to preserve.

### prependgridsizer.py

The same nine blocks, put in with `Prepend()` instead of `Add()`, which lays
them out backwards.

There is nothing to translate, and that is the lesson. A wx sizer keeps its
children in an ordered list, and the cell a child ends up in is decided by
where it sits in that list: `Add()` appends, `Prepend()` pushes everything
along, `Insert()` chooses a place. Adding a tenth block would move the other
nine.

Tkinter has no list. `grid()` is told a row and a column, and a child's
neighbours are unaffected. So `Prepend()` does not become a call, it becomes
arithmetic — counting the positions from the end instead of the start.

Neither way is better. wx lets a row be built without counting, which is
convenient until something has to go in the middle of a form and every cell
after it moves. Tkinter makes the position explicit, which means saying it
even when it is obvious.

### bordergridsizer.py

Each block asks for ten pixels of border on some of its sides.

In wx a border is one number and a set of flags saying where to spend it:
`Add(bw, 0, wx.LEFT | wx.RIGHT, 10)`. The flags choose the sides, the number
is the same for all of them, so a child wanting ten on the left and four on
the top has to be added twice or wrapped in another sizer.

Tkinter asks the other way round and has less to explain: `padx` and `pady`
each take a pair, `(left, right)` and `(top, bottom)`, in pixels. There are
no flags because there is nothing to choose, and a ten and a four sit in the
pair as easily as two tens.

The care needed is that the border and the gap end up in the same place, so
the border is added to the gap rather than put somewhere else. And since a
`wx.GridSizer` makes every cell as big as the largest child *including its
border*, the cell here is the block plus two borders.

### resizegridsizer.py

Nine blocks, each told what to do with a cell bigger than itself. At the
window's natural size every cell fits its block exactly and none of it shows;
resize the window to see it.

Two separate questions are answered here, and wx answers both with the same
argument while Tkinter keeps them apart.

*Does the cell grow with the window?* A `wx.GridSizer` always divides all the
space it is given. A Tkinter row or column grows only if it was given a
`weight`, and equal weights share the spare space equally.

*Where does the block sit in a cell bigger than itself?*

| wx | Tkinter | |
|---|---|---|
| `wx.ALIGN_BOTTOM` | `sticky=SW` | wx aligns the bottom and leaves the horizontal at its default, which is left. Tkinter centres what `sticky` does not name, so the `W` must be said out loud. |
| `wx.ALIGN_CENTER` | `sticky=""` | nothing named, centred both ways |
| `wx.ALIGN_RIGHT` | `sticky=NE` | |
| `wx.EXPAND` | `sticky=NSEW` | held to all four sides, so it fills |
| no flag | `sticky=NW` | the wx default |
| `wx.SHAPED` | — | see below |

## 11.3 The other sizer types

### basicflexgridsizer.py

The same grid with the same enlarged block, laid out by a
`wx.FlexGridSizer`. Only the middle row and the middle column grow: each row
takes the height of its own tallest child and each column the width of its
own widest.

Which is what `grid()` already does, with nothing asked for. No `minsize`, no
`uniform`, no option at all — this file is `basicgridsizer.py` with one block
made bigger.

That turns the chapter around. The sizer that looks like the simple one,
`wx.GridSizer`, is the one that needs work in Tkinter, because *every cell
the same* is a promise Tk does not make. The one that sounds more elaborate,
`wx.FlexGridSizer`, is what `grid()` does when nothing is asked of it.

### resizeflexgridsizer.py

The flex grid told which rows and columns may grow and by how much. wx names
them one at a time, `AddGrowableCol(1, 2)`; Tkinter calls the share `weight`
and puts it where every other row and column option lives,
`grid_columnconfigure(1, weight=2)`. The same numbers and the same
arithmetic.

The only difference is bookkeeping: wx keeps a list of the growable ones, Tk
keeps an option on each. So nothing corresponds to `RemoveGrowableCol` — a
weight of nought is the removal.

### gridbagsizer.py

A `wx.GridBagSizer` is the flex grid with the list thrown away. Each child is
told where it goes, `Add(bw, pos=(row, col), span=(rows, cols))`, and may
cover more than one cell.

Which is what `grid()` has been doing all along. This is the sizer Tkinter
matches without arranging anything: `pos` is `row` and `column`, `span` is
`rowspan` and `columnspan`.

The wx original adds the nine blocks column by column rather than row by row.
It changes nothing, and it is there to make the point: with positions given
by hand, the order of the calls stops mattering.

### boxsizer.py

Four windows, one per question a box sizer answers. A box sizer puts its
children in a single row or column, and for the first three windows that is
`pack()` with nothing lost:

| wx | Tkinter |
|---|---|
| `wx.BoxSizer(wx.VERTICAL)` | `pack(side=TOP)` |
| `wx.BoxSizer(wx.HORIZONTAL)` | `pack(side=LEFT)` |
| `flag=wx.EXPAND` | fill across the other axis: `fill=X` in a column, `fill=Y` in a row |
| `proportion=1` | `expand=True` |

The fourth window is where `pack()` stops. wx gives each child a
**proportion**, a number: one share against two means a third and two thirds
of the free space. `pack()` has `expand`, which is a **boolean** — a child
either takes a share or it does not, and everybody who takes one takes the
same. There is no way to ask `pack()` for two thirds.

So the fourth window is built with `grid()`, where the share is a number
again and is called `weight`.

This is the useful thing to carry out of the chapter. `pack()` and `grid()`
are not the easy one and the serious one: `pack()` is a box sizer and
`grid()` is a grid sizer, and a layout that needs proportions needs `grid()`
even when it is a single column and looks like a job for `pack()`.

### staticboxsizer.py

Three labelled boxes side by side. Two things are shown at once.

One is that a sizer can hold other sizers, which is how any real window is
built. Tkinter does this without a word, because a frame is a widget like any
other and there is no separate kind of object to nest.

The other is what the labelled box **is**, and here the two toolkits really
differ. In wx a `wx.StaticBox` is a widget and a `wx.StaticBoxSizer` is a
sizer that draws it behind whatever it lays out. The blocks are not inside
the box: they are made with `BlockWindow(self.panel, ...)`, siblings of the
box in the same panel, and the box is painted behind them. Nothing but the
sizer connects the two, and moving the box would leave the blocks where they
are.

In Tkinter the labelled box is `ttk.LabelFrame`, a real container. The blocks
are made with `BlockWindow(frm_box, ...)` and are its children. Move it, hide
it, destroy it, and they follow, because they are in it rather than on top of
it.

## 11.4 A real window

### realworld.py

An account form: a heading, a rule, six labelled fields and two buttons. The
chapter's closing example, and the first that looks like a window somebody
would actually be given.

Four sizers are nested in the original, and each becomes a frame or a set of
grid options. A sizer is added to a sizer; a frame is added to a frame. The
nesting is the same, and what changes is that in Tkinter the container is
visible in the widget tree rather than living beside it.

The one idiom with no counterpart is the **spacer**. wx centres the two
buttons by adding three empty items of proportion 1, one before, one between
and one after:

```python
btnSizer.Add((20, 20), 1)
btnSizer.Add(saveBtn)
btnSizer.Add((20, 20), 1)
```

An invisible child that exists only to take up room. Tkinter has no such
object, and does not need one: an empty grid column exists whether or not
anything is put in it, and giving it a weight makes it the spacer. Three
empty columns with a weight, two buttons in the columns between them.

## What does not translate

**`wx.SHAPED`** fills a cell like `wx.EXPAND` but keeps the child's
proportions, so block *eight*, 100x25 and therefore four to one, comes out
163x40 in a cell 163 wide. `sticky` names sides, and a widget held to all
four sides is the size of the cell, ratio or no ratio. Tkinter would need the
size recomputed by hand on every `<Configure>` event, which is a different
lesson in a different chapter. Block *eight* is left at its natural size in
`resizegridsizer.py`.

**`wx.BoxSizer` proportions are not `grid` weights.** wx divides the free
space *itself* in the given ratio and pays no attention to what the children
asked for. Tkinter divides only the **surplus** — what is left after every
child has had the size it requested — and adds each share on top. Measured,
in a window 300 tall holding four fixed blocks of 30:

| | first | second |
|---|---|---|
| wx | 60 | 120 | 
| Tkinter | 70 | 110 |

wx splits the 180 of free space one to two. Tkinter gives each its natural
30, then splits the 120 of surplus one to two. The two agree exactly only
where the proportional children request no size of their own, and Tkinter's
ratio approaches one to two as the window grows without ever arriving. The
same shows at the smallest size: wx opens the window 210 tall, having already
paid the double share, and Tkinter opens it 180 with every block at its
natural height.

Neither is a bug. wx proportions are a division of the leftovers; grid
weights are a bias on the leftovers.

## The files

Same names as `wxPythonInAction-src/Chapter-11/`, one to one.

| file | measured against wx |
|---|---|
| `blockwindow.py` | the block the others lay out |
| `basicgridsizer.py` | identical |
| `mingridsizer.py` | identical |
| `prependgridsizer.py` | identical |
| `bordergridsizer.py` | identical |
| `resizegridsizer.py` | 7 cells of 9 identical; `wx.SHAPED`, and 1 px of rounding |
| `basicflexgridsizer.py` | identical |
| `resizeflexgridsizer.py` | identical |
| `gridbagsizer.py` | identical |
| `boxsizer.py` | 3 windows of 4 identical; proportions as above |
| `staticboxsizer.py` | same arrangement; the theme draws 4 px wider |
| `realworld.py` | arrangement only: wx counts pixels, `ttk.Entry` counts characters |

`blockwindow.py` is imported by every other file in the chapter, which the
conventions of this project would normally forbid. It is kept because the
book keeps it, because the mapping to the original stays one to one, and
because it is not a convenience helper but the thing being laid out. The
exception stops at the edge of the chapter.

## Checked against wx

Nothing here is translated from the printed page. wxPython 4.2 still runs the
book's code, so each example is executed beside its original and the two are
compared by geometry — window size, and the position and size of every widget
in it.

`basicgridsizer.py` returns a window of 310x85 with its children at (0,0),
(105,0), (210,0) and so on; `wx.GridSizer` returns the same numbers, pixel
for pixel. Where they differ, the difference is measured and written down.

The book's own code needed one repair to run at all. `blockwindow.py` line 18
passes `(sz.width-w)/2` to `DrawText()`. In 2006 that division gave an
integer; from Python 3.0 it gives a float, and wxPython 4 refuses it. `//`
fixes it, and the same fix is needed in chapters 12 and 18.
