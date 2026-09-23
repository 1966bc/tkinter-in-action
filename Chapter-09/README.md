# 9. Giving users choices with dialogs

Fifteen files. Six of the dialogs are in the standard library, six are not
and are built here, and three are about checking what was typed, which the
two toolkits do in genuinely different ways.

| wx | Tkinter |
|---|---|
| `wx.MessageDialog`, `wx.MessageBox` | `messagebox.askyesno` and its family |
| `wx.TextEntryDialog` | `simpledialog.askstring` |
| `wx.ColourDialog` | `colorchooser.askcolor` |
| `wx.DirDialog` | `filedialog.askdirectory` |
| `wx.FileDialog` | `filedialog.askopenfilename` |
| `wx.FontDialog` | `tk fontchooser`, which Python does not offer |
| `wx.SingleChoiceDialog` | — built on `simpledialog.Dialog` |
| `wx.ProgressDialog` | — built on `ttk.Progressbar` |
| `wx.lib.imagebrowser` | — built on a `Listbox` and a preview |
| `wx.ShowTip` | — built on a `Toplevel` |
| `wx.wizard` | — built on a `Toplevel` |
| `wx.Dialog` subclass | `simpledialog.Dialog` subclass |
| `wx.Validator` | `validatecommand`, which is not the same idea |

## The font dialog Tkinter has and does not offer

There is no `tkinter.fontchooser`, and every answer on the internet says
Tkinter has no font dialog.

It has one. Tk grew a font chooser in 8.6 and Python never wrapped it, so
it is reached through the interpreter:

```python
root.tk.call("tk", "fontchooser", "configure",
             "-parent", root, "-command", root.register(on_font))
root.tk.call("tk", "fontchooser", "show")
```

Asked on this machine it reports its options as `-parent`, `-title`,
`-font`, `-command` and `-visible`, and on a desktop that has a native one
it uses it.

But it is **not a modal dialog**, and that is the difference that matters.
`wx.FontDialog` is shown, blocks, and returns a code; the Tk chooser opens
and stays open, and announces a font by calling back - possibly several
times, as the person tries one and then another. The program has to be
written to accept a font at any moment rather than to ask for one and
wait. `font_box.py` changes a label each time it is told, which is what
the arrangement is for.

## wx.Sleep has no translation, and the reason matters

The progress dialog is the most useful file in the chapter, and not
because of the bar.

The wx original counts to a hundred in a loop with `wx.Sleep(1)` in it.
That works because `wx.Sleep` lets the event loop run while it waits, so
the dialog redraws and its Cancel button can be pressed.

Tkinter has nothing like it. `time.sleep()` in a handler stops the whole
program: the window does not redraw, the button cannot be pressed, and the
desktop greys it out and offers to kill it. So the loop has to be turned
inside out:

```python
def on_step(self):
    self.count = self.count + 1
    keep_going = self.box.update_to(self.count)

    if keep_going and self.count < MAXIMUM:
        self.after(MILLISECONDS, self.on_step)
```

Do a little, ask to be called again, let the window breathe. **This is the
shape of every long job in a Tkinter program** - reading a file, walking a
directory, talking to an instrument - and it is the single most useful
thing in this chapter for anybody writing one.

The alternative is a thread, which is chapter 18.

## Two kinds of not-quite-the-same

**Cancel does not answer the same way twice.** `askstring` returns `None`,
`askdirectory` returns `""`, `askcolor` returns a pair of `None`s. The
tkinter dialogs were written by different hands at different times and it
shows; each one has to be checked for what it actually returns.

**A wildcard is a list, not a string.** wx takes one string with pipes in
it, alternating description and pattern. Tkinter takes a list of pairs,
and a pair may hold several patterns. The Tk form can be read at a glance
and the wx form cannot.

## Validators: two different ideas with the same name

This is the part of the chapter worth the most.

A `wx.Validator` is an **object attached to a widget**. It has `Clone()`,
`Validate()`, `TransferToWindow()` and `TransferFromWindow()`, and the
dialog calls them at the right moments. One validator class can be reused
on every field that has the same rule, which is a real saving in a form of
thirty fields.

Tkinter has three different answers, one for each of the three things wx's
one object does.

**Checking on OK** is `validate()` on `simpledialog.Dialog`: one method,
called once, returning false to keep the dialog open. It lives on the
dialog rather than on the field, which is the right place when the rule is
about the form - *a start date before an end date* has no field to belong
to.

**Moving data in and out** is a `StringVar`. `TransferToWindow` is the
constructor and `TransferFromWindow` is `get()`, and in between the
variable *is* the field, continuously, in both directions. There is no
transfer because there is nothing to transfer.

**Refusing a character as it is typed** is where Tkinter is built for the
job and wx is not. wx binds `EVT_CHAR`, decides, and calls `Skip()` or does
not - the same opt-in to carrying on that chapter 3 describes. Tk has
`validatecommand`, whose entire purpose is to be asked before an edit and
to be allowed to say no:

```python
entry.config(validate="key",
             validatecommand=(self.register(rule), "%P"))
```

`%P` is what the field would say **if the edit were allowed**. Return false
and the field is left exactly as it was - nothing to undo, nothing to
correct afterwards, and the cursor does not move. Measured: typing `0a6`
into the no-letters field leaves it empty, because the `a` was refused and
so the rest never arrived.

There are other substitutions - `%S` for the text being inserted, `%d` for
whether it is an insertion or a deletion, `%s` for the value before, `%W`
for the widget - and they cover everything one wants. The awkward part is
that they are single-letter Tcl codes passed as strings, which is not
something anybody would design today.

A warning found by reading the 2019 translation this replaced: the older
way is `trace_add("write", ...)` and correcting the value after it has
been typed. It works and it fights the cursor, because setting the
variable from inside its own trace moves the insertion point. `validate`
refuses the edit instead, which is the difference between preventing and
apologising.

## The six that had to be built

`choice_box.py`, `progress_box.py`, `image_box.py`, `startup_tip.py`,
`wizard.py`, and the single-choice dialog inside `choice_box.py`. None of
them is long. The wizard is eighty lines, the tip box sixty, the progress
box a hundred with both clocks in it.

What is missing is not capability but **agreement**. wx ships one wizard
and every wxPython program has the same one; in Tkinter everybody writes
their own and no two are alike. For a laboratory that is not much of a
loss - the wizard belongs to the program, not to the desktop - and for
somebody learning it means there is no wizard to learn, only a Toplevel
and some buttons.

`startup_tip.py` has one thing in it worth keeping, and it is not code:
the answer to *show these at startup* goes in a file beside the tips, not
in a variable. A program that forgets the answer and asks again every
morning has saved nobody anything.
