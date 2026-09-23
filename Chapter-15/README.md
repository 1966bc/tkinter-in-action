# 15. Climbing the tree control

Six files, five of them translated, and the sixth is the interesting one.

| wx | Tkinter |
|---|---|
| `wx.TreeCtrl` | `ttk.Treeview` |
| `AddRoot` | `insert("", ...)` — the root is the empty string |
| `AppendItem(parent, text)` | `insert(parent, tk.END, text=text)` |
| an image list and indices | `image=` on the item |
| a different image when open | — swapped by hand |
| `wx.gizmos.TreeListCtrl` | the same `ttk.Treeview` |
| `SortChildren` | `move()`, as in chapter 13 |
| `TR_EDIT_LABELS` | — an `Entry` put over the row |
| six events | three |
| a virtual tree | a virtual tree, and it is easy |

## The root is an absence

`wx.TreeCtrl.AddRoot` makes the one item everything else hangs from. A
`Treeview` has no such call: `insert("", ...)` inserts at the top level,
and `""` is not an item but the absence of a parent.

So a Treeview can have **several** top-level items, which a wx tree
cannot, and a tree that wants one visible root has to make it like any
other item. Chapter 13's table is the same widget with nothing at the top
level but rows - which is why one widget serves both chapters.

## A tree with columns costs nothing

wx needs a different widget for this. `wx.gizmos.TreeListCtrl` is a
contributed control, with its own `AddColumn` and its own
`SetItemText(item, text, column)`, and it is not the tree from the rest of
the chapter.

A `ttk.Treeview` is already both. The tree lives in column `#0` and any
other columns are given when the widget is made:

```python
self.trv_tree = ttk.Treeview(frm_main, columns=("description",))
self.trv_tree.insert(parent, tk.END, text=name, values=(note,))
```

`text` is the tree column and `values` are all the others. That is the
whole of `tree_treelist.py`.

## Three events where wx has six

wx raises `EVT_TREE_ITEM_EXPANDING`, `EXPANDED`, `COLLAPSING`,
`COLLAPSED`, `SEL_CHANGED`, `ITEM_ACTIVATED` and
`BEGIN_LABEL_EDIT`. Tk raises `<<TreeviewOpen>>`, `<<TreeviewClose>>` and
`<<TreeviewSelect>>`.

Three things are therefore missing.

**Nothing can be refused.** wx's *expanding* and *collapsing* events happen
before the thing does and can be vetoed. Tk's happen after.

**There is no activation event.** A double click is a binding, and
`<Return>` must be bound as well, because a tree that answers the mouse
and not the keyboard is half a tree.

**Labels cannot be edited.** `TR_EDIT_LABELS` lets a label be typed over
in place. A Treeview has nothing of the kind, so `tree_misc.py` builds it:
`bbox(item, "#0")` gives the rectangle the label occupies, an `Entry` is
placed exactly over it, and `<Return>` keeps what was typed while
`<Escape>` and `<FocusOut>` throw it away.

That is the same answer as editing a cell in chapter 5, and the same fifty
lines. Worth noticing that it is the *second* time in this book the answer
has been *put an Entry over the thing*: it is the standard Tkinter reply to
anything that wants editing in place, and once written it can be used for
both.

And one small thing: **the event does not say which item.** `focus()` does.
Every handler here starts by asking the widget what was just acted on.

## Where a virtual tree works and a virtual list does not

Chapter 13 says `LC_VIRTUAL` has no answer in Tkinter. This chapter builds
a virtual tree in forty lines. The difference is worth seeing, because it
is about the widgets and not about the effort.

**A list is flat.** Nothing happens between one row and the next. There is
no moment at which a program could be asked for row nine hundred thousand,
so a widget either holds the rows or it does not.

**A tree has an event.** A branch is opened, and that *is* the moment. So:

```python
item = self.trv_tree.insert(parent, tk.END, text=name)

if children:
    self.trv_tree.insert(item, tk.END, text="")   # the dummy
    self.pending[item] = children
```

The dummy child is what makes the expander appear. Without it a branch
that has not been filled yet looks like a leaf, cannot be opened, and the
event that would fill it never comes. `<<TreeviewOpen>>` then deletes the
dummy and puts the real children in, each with a dummy of its own.

`tree_virtual.py` counts what it has actually built, and it is worth
opening it to watch the number: the hierarchy in `data.py` has twenty-five
nodes and the window starts with one.

This is the same pattern as the namespace tree in chapter 4 - and it is
the one Tkinter pattern in this book worth learning by heart. Any tree
over something large - a filesystem, a database schema, an instrument's
settings, a hierarchy of methods - is built this way, and the alternative
is a window that takes several seconds to open and holds everything it
has ever shown.

## The hierarchy

The original shows the class hierarchy of wxPython, which is theirs. The
one in `data.py` is a laboratory: sections, benches, instruments, methods.
It has the same shape - a root, branches of uneven depth, leaves at the
end - which is what a tree example needs, because a hierarchy that is the
same depth everywhere never surprises anybody.

## The files

| file | state |
|---|---|
| `data.py` | a hierarchy of our own |
| `tree_simple.py` | translated |
| `tree_icons.py` | translated, with the open and shut icons swapped by hand |
| `tree_misc.py` | translated, with label editing built |
| `tree_treelist.py` | translated, and free |
| `tree_virtual.py` | translated, and easier than the list was |
