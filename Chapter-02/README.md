# 2. Giving your program a solid foundation

Chapter 1 showed that `tk.Tk()` is the application and the first window at
once. This chapter is about what that costs, because a wxPython application
object is not only a place to start: it is a place to stand.

## Four places to stand, and two

wx gives an application four moments of its own.

| wx | when | Tkinter |
|---|---|---|
| `App.__init__` | before anything exists | `App.__init__`, before `super()` |
| `OnInit()` | build the first window, return True or refuse to start | the rest of `App.__init__` |
| `MainLoop()` | run | `mainloop()` |
| `OnExit()` | after the last window has gone | — |

The one with no translation is `OnInit()` returning `False`. wx lets a
program decide, after looking around, that it is not going to start: no
licence, no database, wrong version, and the application simply does not
come up. Tkinter has no such gate. `Tk()` has already put a window on the
screen by the time any code of yours runs, so refusing to start means
withdrawing the window you already have, or checking before you make it.

`OnExit()` has no real translation either. `protocol("WM_DELETE_WINDOW")` is
close and is used here, but it is not the same thing: it fires when a window
is closed, not when the program ends, and a program that ends by any other
route does not pass through it.

## Where the output goes

`wx.App(redirect=True)` opens a window and puts `stdout` and `stderr` in it.
One argument. It is the sort of thing that is easy to miss until a program
is double-clicked rather than started from a terminal, and everything it
prints goes nowhere.

Tkinter has nothing of the kind, so `startup.py` builds it, and it is most
of the file: a `Toplevel` with a `Text` in it, and `sys.stdout` replaced by
an object with `write()` and `flush()`. Anything with those two methods is a
file as far as `print()` is concerned, so the whole of the machinery is:

```python
def write(self, text):
    self.txt_output.insert(tk.END, text)
    self.txt_output.see(tk.END)
```

There is a reason wx can offer this as an argument to its application object
and Tkinter cannot. A `wx.App` is not a window, so it can make one whenever
it likes. `Tk()` *is* the window, and until it has run there is nothing to
put a `Toplevel` on. So in wx redirection is set up before the first window,
and in Tkinter it can only be set up after.

Run `startup.py` from a terminal and the order is visible: `App __init__`
arrives before the redirection is in place and lands in the terminal, and
everything after it lands in the window.

## A program with no main window

`dialog_scratch.py` asks three questions and never opens a window behind
them. In wx that follows from the application object not being a window: the
dialogs are made in `OnInit()` with `None` as their parent.

Tkinter needs the root to exist, and needs it not to be seen:

```python
self.withdraw()
```

Which is the whole translation, and worth knowing, because a Tkinter program
that opens a dialog without doing it shows an empty grey window behind it.

| wx | Tkinter |
|---|---|
| `wx.MessageDialog(..., wx.YES_NO)` | `messagebox.askyesno()` |
| `wx.TextEntryDialog` | `simpledialog.askstring()` |
| `wx.SingleChoiceDialog` | — |

**The list to choose one thing from is not there.** It is the commonest
dialog in a laboratory program - which instrument, which lot, which method -
and Tkinter has a message box and a string box and nothing else.

What it does have is `simpledialog.Dialog`, which supplies the modal window,
the OK and Cancel, the escape key and the waiting. Two methods are left to
write: `body()` fills the window and returns the widget that takes the
focus, `apply()` is called if OK was pressed and not if it was not. The
whole of `SingleChoiceDialog` in this chapter is a `Listbox` and those two
methods.

That is the shape of most of this book's answers. Not *no*, but *not
included, and here is what it costs*: about twenty-five lines, once.

## Closing a window

`insert.py` is about the difference between two wx methods.

`Close()` raises `EVT_CLOSE`, which a handler may refuse. `Destroy()` takes
the window away and cannot be argued with. That is how *save before
quitting?* is asked, and it is why the original binds both.

Tkinter has only `destroy()`. What stands in for `EVT_CLOSE` is a message
from the window manager:

```python
self.protocol("WM_DELETE_WINDOW", self.on_close_window)
```

The handler takes no arguments, and refusing means not calling `destroy()`.
The difference in practice: in wx anything that calls `Close()` goes through
the handler, including your own code; in Tkinter only the title bar does,
and your own code calling `destroy()` walks straight past it.

## The furniture

`toolbar.py` wants a toolbar, a menu bar and a status bar. wx makes two of
them with a method call:

```python
statusBar = self.CreateStatusBar()
toolbar = self.CreateToolBar()
```

Tkinter has `tk.Menu` and nothing else.

**A toolbar** is a `Frame` with `relief=RAISED`, packed at the top, holding
`Button`s with `relief=FLAT`. That is all a toolbar is, and once written it
behaves like the rest of the window, which the wx one does not always.

**A status bar** is a `Label` with `relief=SUNKEN`, `anchor=W`, packed at
the bottom with `fill=X`.

**Long help** - the string wx shows in the status bar when the pointer rests
on a tool - has nowhere to go, because there is no tool and no status bar to
put it in. Here it is shown in a message box instead, which is not the same
thing and is not pretending to be.

## The icon in the source

`images.py` is generated code in the original: the PNG written out as a
Python byte string, turned into a stream, then an image, then a bitmap.

```python
def getNewBitmap():
    return BitmapFromImage(getNewImage())

def getNewImage():
    stream = cStringIO.StringIO(getNewData())
    return ImageFromStream(stream)
```

Three calls and a `cStringIO`, because wx distinguishes a `wx.Image`, which
is data one can manipulate, from a `wx.Bitmap`, which is something the
platform can draw.

Tkinter does not make the distinction. A `PhotoImage` is both, it takes
base64 directly, and since Tk 8.6 it reads PNG - so this file carries the
same bytes the book embeds, and the three functions become one:

```python
def get_new_image():
    return tk.PhotoImage(data=NEW_PNG)
```

One condition, and it is the same one as chapter 1: a `PhotoImage` lives
inside a Tk interpreter, so there must be a `Tk()` before this is called,
and something must keep the result alive afterwards.

## The files

| file | what it is for |
|---|---|
| `startup.py` | the order things happen in, and where output goes |
| `dialog_scratch.py` | three dialogs and no window; one of them built by hand |
| `insert.py` | closing a window, and being asked first |
| `toolbar.py` | a toolbar and a status bar, neither of which exists |
| `images.py` | the icon, carried in the source |

`images.py` is imported by `toolbar.py` and is not a program, the same
exception the conventions of this project make for `blockwindow.py` in
chapter 11, and for the same reason: the book has the file, so this has the
file.

The original is `startup.py`; this repository had it as `start_up.py` from
2019, which broke the one-to-one mapping with the book. Renamed.
