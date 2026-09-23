# 6. Working with the basic building blocks

Seven files that build one program, Sketch, a layer at a time. It is the
book's running example and the best thing in it: each file is the previous
one plus one idea.

This is also the chapter where the two toolkits draw differently, and the
difference is worth more than the seven files put together.

## A canvas is not a device context

Here is what `example1.py` has to do in wx, and it is most of the file:

```python
def InitBuffer(self):
    size = self.GetClientSize()
    self.buffer = wx.Bitmap(size.width, size.height)
    dc = wx.BufferedDC(None, self.buffer)
    dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
    dc.Clear()
    self.DrawLines(dc)

def OnSize(self, event):
    self.reInitBuffer = True

def OnIdle(self, event):
    if self.reInitBuffer:
        self.InitBuffer()
        self.Refresh(False)

def OnPaint(self, event):
    dc = wx.BufferedPaintDC(self, self.buffer)
```

A wx device context is **immediate**. `DrawLine` puts pixels down and then
forgets; nothing remembers what was drawn. So a window that is covered and
uncovered has lost its picture, and the program keeps a bitmap of its own,
draws into that, and paints it back on every `EVT_PAINT`. Resizing means
making a new bitmap, which is what the idle handler is for, because doing
it during the resize itself is too slow.

A Tk canvas is **retained**. `create_line` makes an object, the canvas
keeps a list of them, and it redraws them itself when it has to. So:

```python
def on_motion(self, event):
    coords = self.position + (event.x, event.y)
    self.current_line.append(coords)
    self.create_line(*coords, fill=self.color, width=self.thickness)
    self.position = (event.x, event.y)
```

`InitBuffer`, `OnSize`, `OnIdle`, `OnPaint` and `DrawLines` have no
translation, because they have no work to do. The buffer, the double
buffering, the flag and the idle handler were all in aid of something Tk
does without being asked.

The list of lines is still kept, for one reason: `example6.py` saves it to
a file. The canvas does not need it to redraw.

**Neither model is better, and the trade is real.** A canvas that remembers
ten thousand lines holds ten thousand objects; a bitmap holds one picture,
whatever is on it. For a sketch, Tk wins outright. For a chart redrawn
every second from a hundred thousand points, the wx arrangement is the one
that does not run out of memory - and in Tkinter one reaches for a
`PhotoImage` written into pixel by pixel, or for a library.

One more thing goes away. wx calls `CaptureMouse()` on the press so that
dragging outside the window keeps reporting, and `ReleaseMouse()` on the
release. Tk grabs the pointer for the duration of a button press by itself.
There is nothing to ask for and nothing to release, and therefore nothing
to leak if an exception is raised in between.

## What each file adds

| file | what arrives |
|---|---|
| `example1.py` | the canvas, and drawing on it |
| `example2.py` | a status bar showing where the pointer is |
| `example3.py` | three fields in it instead of one |
| `example4.py` | a menu built from data, with the colours as radio items |
| `example5.py` | a toolbar, with a swatch per colour |
| `example6.py` | New, Open, Save, and a file on disk |
| `example7.py` | the control panel, the about window, the splash screen |

### The status bar, again

`example3.py` wants three fields with relative widths of one, two and
three. wx says `SetStatusWidths([-1, -2, -3])`.

Tkinter has no status bar, so it is three `Label`s - and they cannot be
packed, because `pack()` has no proportions. They are `grid`ed with
`weight=1`, `weight=2`, `weight=3`, which is the same answer chapter 11
arrives at from the other direction.

### Radio items, and what they save

From `example4.py` on, the colour is chosen in more than one place: a menu,
then a toolbar, then a panel of sixteen swatches. wx gives every button an
id, keeps a dictionary from id to colour, and when one goes down it looks
up the one that was down before and sends it back up by hand:

```python
def OnSetColour(self, event):
    color = self.colorMap[event.GetId()]
    if color != self.sketch.color:
        self.colorButtons[self.sketch.color].SetToggle(False)
    self.sketch.SetColor(color)
```

In Tk they share a variable:

```python
tk.Radiobutton(parent, value=name, variable=self.colour,
               indicatoron=False, command=self.on_set_colour)
```

`indicatoron=False` is what makes a radio button look like a button that
stays down. The old one comes up by itself, the menu item and the toolbar
swatch agree without being introduced, and the two dictionaries and the
bookkeeping are not needed. This is a `StringVar` doing what chapter 5 said
it was for.

### Drawing a swatch

wx makes an empty bitmap, selects it into a memory device context, sets a
brush and clears it. Tkinter:

```python
swatch = tk.PhotoImage(width=16, height=15)
swatch.put(colour, to=(0, 0, 16, 15))
```

With one trap, which cost a run: `put()` is given a **Tcl list of rows of
colours**, so a colour name with a space in it is read as two colours and
`"forest green"` fails on `"forest"`. Tk knows the same colour spelled
`forestgreen`, so the space comes out. All sixteen names in the book's
palette are names Tk knows.

### The splash screen

`wx.SplashScreen` is a class. Tkinter has no such thing, and does not need
one:

```python
self.overrideredirect(True)
self.after(milliseconds, self.destroy)
```

`overrideredirect(True)` asks the window manager for no title bar and no
border, which is the whole of what a splash screen is.

## What does not translate

**The about window.** The original is a page of HTML in a
`wx.html.HtmlWindow`, with a table, a background colour and bold text.
Tkinter has no HTML widget - not a simpler one, none - and this is the
reason chapter 16 of the book is not in this one.

What is here instead is a read-only `Text` with the same words in it. The
information arrives and the formatting does not. A `Text` can be given tags
for bold, colour and spacing, so a determined person can get most of the
way there by hand; nobody is going to parse HTML into it, and if that is
really wanted the answer is an external package.

**The toolbar icons.** `new.bmp`, `open.bmp` and `save.bmp` belong to the
book and are not copied into this repository, and Tk cannot read BMP in any
case. The three tools are words here.
