# 4. Looking at a program while it runs

This is the chapter that looked, from the file list, as though it would not
translate at all. PyCrust is a wxPython thing: a shell, a namespace browser,
a session log, wrapped in one window and shipped with the toolkit.

It translates, once the right thing is noticed.

**PyCrust is not a feature of wxPython. It is an application written in
wxPython**, living in `wx.py`, which happens to be shipped alongside. The
question is therefore not *what is the Tkinter equivalent of PyCrust* but
*what is the Tkinter application that does this*, and the answer is IDLE:
shipped with Python, written in Tkinter, and older than the book.

So the chapter has two halves and only one of them is a translation.

| wx | Tkinter |
|---|---|
| PyCrust, the application | IDLE, the application |
| `wx.py.shell.ShellFrame` | — |
| `wx.py.filling.FillingFrame` | — |
| `PyWrap.py` | `PyWrap.py`, rewritten |

The middle two are the ones that matter, because the point of the chapter is
not having a shell on the desktop - everybody has one of those. It is having
a shell **inside your own running program**, holding your own window, while
it is open. wx lets you import that. Tkinter does not: IDLE is a program,
not a library, and nothing in it is meant to be put in somebody else's
window.

So `pycrust-foundation.py` builds one, and it is smaller than expected.

## A shell in fifty lines

The language part is already in the standard library:

```python
self.console = code.InteractiveConsole(namespace)
more = self.console.push(source)
```

`code.InteractiveConsole` compiles a line, decides whether the statement is
finished - which is what `push()` returns - keeps the state between lines,
and prints a traceback rather than raising when something goes wrong. It is
what the `>>>` prompt is made of.

What is left is a `Text` to type into, a `<Return>` binding to find out what
was typed, and somewhere for the output to go. Output is the only fiddly
part, because `push()` prints to `sys.stdout`:

```python
with contextlib.redirect_stdout(caught):
    with contextlib.redirect_stderr(caught):
        more = self.console.push(source)
```

The `<Return>` handler returns `"break"`, for the reason chapter 3 gives: the
`Text` would otherwise insert its own newline afterwards, and the prompt
would land on the wrong line.

It works on the running window. Typing `app.title('changed')` in the shell
changes the title of the window behind it, which is the whole point of the
chapter.

## A namespace tree

`wx.py.filling.FillingFrame` shows what is inside things. A `ttk.Treeview`
over `dir()` is the same idea, and the only care needed is not to walk the
whole namespace at once: each row is given one empty child so that it can be
opened, and `<<TreeviewOpen>>` fills it the first time somebody asks.

That is a pattern worth keeping. Any tree over something large - a
filesystem, a database schema, an instrument's settings - is built this way
in Tkinter, and the alternative is a program that stops for several seconds
when a window opens.

## PyWrap

The original is a command line utility: give it a module, and it finds the
`wx.App` class in it, starts it inside a PyCrust window, and puts the
application in the shell's namespace. Nothing in the program being wrapped
has to know.

The Tkinter version does the same and looks for a different thing:

```python
if isinstance(thing, type) and issubclass(thing, tk.Tk):
```

wx looks for a `wx.App` because in wx the application is not a window. Here
they are the same object, so what is looked for is the window class.

    python3 Chapter-04/PyWrap.py Chapter-01/spare.py
    python3 Chapter-04/PyWrap.py Chapter-02/toolbar.py

Both work, and `app.title()` in the shell answers `'Spare'`.

Two things had to be dealt with that the original did not have.

**A file is not always a module.** `pycrust-foundation.py` cannot be
imported by name, because a hyphen is not something Python will accept in
one. `importlib.util.spec_from_file_location` loads a file whatever it is
called, which is also how a program in another directory is reached without
putting it on the path first.

**The shell class is written twice**, once in each file. The conventions of
this project allow that - duplication between examples is deliberate - and
here it is forced anyway, by the book's own choice of file name.

## What is really lost

Not much, and the little there is is worth naming.

PyCrust is **finished**. It has history with the up arrow, completion,
call tips, a session log, and a dozen other things that are the difference
between a shell one can type at and a shell one wants to work in. Fifty
lines gets a prompt that runs statements and shows results. The rest is a
long tail, and IDLE has already walked it - but IDLE cannot be put inside
your window.

So: if the shell is for you, use IDLE and run your program from it. If the
shell has to be inside a program somebody else is using - and for a
laboratory instrument that is sometimes the only way to see what is
happening - this file is where to start.

## The files

| file | what it is for |
|---|---|
| `pycrust-foundation.py` | a window with a shell and a namespace tree on it |
| `PyWrap.py` | runs another program with a shell attached |
| `spare.py` | something for PyWrap to run |
| `images.py` | the toolbar icon, as in chapter 2 |

`spare.py` and `images.py` are repeated from chapters 1 and 2 because the
book repeats them.
