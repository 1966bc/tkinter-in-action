# Tkinter in Action

The source code of *wxPython in Action* rewritten in Tkinter, chapter by
chapter, file by file.

![alt tag](https://user-images.githubusercontent.com/5463566/65474496-5d0db080-de7c-11e9-8b88-a778727a2b92.png)

### ...where it was possible....;)

That line was a joke when this repository started. From chapter 11 on it is
the subject.

The first ten chapters translate almost mechanically: a frame is a frame, a
button is a button. After that the two toolkits stop agreeing. wxPython has a
grid control, an HTML window and a printing framework, and Tkinter has none
of the three. It has `pack`, `grid` and `place` where wx has sizer objects,
and a `Canvas` that remembers what was drawn on it where wx has a device
context that does not.

So the answer is not always a file. Sometimes it is a paragraph explaining
what Tkinter does instead, or that it does nothing and why. **A "no" is a
result**, and every chapter carries a `README.md` that records both.

## How it is checked

wxPython 4.2 still runs the book's code, so nothing here is translated from
memory or from the printed page. Each example is executed beside its
original and the two are compared by their geometry - window size, and the
position and size of every widget in it.

`Chapter-11/basicgridsizer.py` returns a window of 310x85 with its children
at (0,0), (105,0), (210,0) and so on; `wx.GridSizer` returns the same
numbers, pixel for pixel. Where they differ, the difference is measured and
written down rather than smoothed over.

## Source

Rappin, Noel and Robin Dunn, *wxPython in Action*, Manning Publications,
2006. The example code that accompanies the book is its authors'; this
repository holds a translation of it and keeps the original file names so the
two can be read side by side.

## Conventions

`CONVENTIONS.md`. Read it before adding a file.

## Licence

MIT, see `LICENSE`.

---

*autumnus MMXXVI*
