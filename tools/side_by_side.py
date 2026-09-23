#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Opens an example and its wxPython original next to each other.

    python3 tools/side_by_side.py Chapter-11 boxsizer
    python3 tools/side_by_side.py Chapter-01 hello

The translation goes on the left, the book's own program on the right, both
running at once, so the two can be looked at rather than read about. Ctrl-C
in the terminal closes both.

Windows are moved into place with xdotool where it is installed; without it
they open wherever the window manager puts them, which is no worse than
starting them by hand.

Which windows belong to which program is decided by looking at the screen
before and after each one starts, and not by asking who owns a window. A wx
window answers that question - it sets _NET_WM_PID - and a Tk window does
not, so half of the comparison would never be found.

The wx side needs wxPython and forge/wxPythonInAction-src, which is not part
of this repository. Without it only the translation opens, and it says so.
"""
import os
import shutil
import signal
import subprocess
import sys
import time


HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(HERE, "forge", "wxPythonInAction-src")

LEFT = 40
RIGHT = 700
TOP = 80

# Down the screen, for an example that opens more than one window.
STEP = 70

# How long to wait for a window to appear, and how long to go on waiting
# afterwards for the others an example may be opening behind it.
PATIENCE = 8.0
SETTLE = 1.0


def get_visible():
    """Every window on the screen at this moment."""
    done = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "."],
                          capture_output=True, text=True)

    return set(done.stdout.split())


def get_new_windows(before):
    """The windows that have appeared since that list was taken."""
    new = set()
    deadline = time.time() + PATIENCE

    while not new and time.time() < deadline:
        new = get_visible() - before

        if not new:
            time.sleep(0.2)

    if new:
        # An example that opens four windows does not open them at once.
        time.sleep(SETTLE)
        new = get_visible() - before

    return sorted(new)


def place(windows, x):
    """Put a program's windows down one side of the screen."""
    for index, window in enumerate(windows):
        subprocess.run(["xdotool", "windowmove", window,
                        str(x), str(TOP + index * STEP)],
                       capture_output=True)


def start(path, x, moving):
    """Run one example, and move its windows to their side."""
    started = None

    if not os.path.exists(path):
        print("not here: {}".format(path))
    else:
        before = set()

        if moving:
            before = get_visible()

        started = subprocess.Popen([sys.executable, path],
                                   cwd=os.path.dirname(path))

        if moving:
            place(get_new_windows(before), x)

    return started


def close(running):
    """Shut both programs down. They are children, not grandchildren."""
    for started in running:
        if started.poll() is None:
            started.send_signal(signal.SIGTERM)


def main(chapter, name):
    """Open both, place them, and wait until they are closed."""
    moving = shutil.which("xdotool") is not None

    if not moving:
        print("no xdotool: the window manager decides where they go")

    ours = start(os.path.join(HERE, chapter, name + ".py"), LEFT, moving)
    theirs = start(os.path.join(SOURCES, chapter, name + ".py"), RIGHT, moving)

    running = [started for started in (ours, theirs) if started is not None]

    if not running:
        print("nothing to open")
    else:
        # Without this a killed terminal leaves both programs on the screen
        # with nothing left to close them.
        signal.signal(signal.SIGTERM, lambda number, frame: close(running))

        print("tkinter on the left, wxPython on the right."
              " Ctrl-C closes both.")

        try:
            for started in running:
                started.wait()
        except KeyboardInterrupt:
            close(running)
            print("\nclosed")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
