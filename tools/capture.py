#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Takes a picture of an example running, for the figures in the book.

    python3 tools/capture.py Chapter-11 basicgridsizer
    python3 tools/capture.py Chapter-11            # every example in it

The picture goes in Chapter-NN/figures/ and is referenced from the
chapter's README.md, so it shows both on GitHub and in the PDF.

Figures made this way do not go stale: when an example changes, this is
run again and the picture changes with it.

Which windows belong to the example is decided by looking at the screen
before and after it starts, as tools/side_by_side.py explains - a Tk
window does not set _NET_WM_PID and cannot be found by asking who owns
it. Needs xdotool to find them and ImageMagick's import to capture them.
"""
import os
import shutil
import signal
import subprocess
import sys
import time


HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# How long to let an example settle before taking its picture. Long
# enough for a window to be mapped, drawn and given its final size.
SETTLE = 2.5

PATIENCE = 8.0


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
        time.sleep(SETTLE)
        new = get_visible() - before

    return sorted(new)


def get_capture(window, path):
    """One window, into one file."""
    done = subprocess.run(["import", "-window", window, "-frame", path],
                          capture_output=True, text=True)

    return done.returncode == 0


def capture(chapter, name):
    """Run one example, photograph its windows, and shut it down."""
    source = os.path.join(HERE, chapter, name + ".py")
    figures = os.path.join(HERE, chapter, "figures")

    if not os.path.exists(source):
        print("  {:26} not here".format(name))
        return

    os.makedirs(figures, exist_ok=True)

    before = get_visible()
    started = subprocess.Popen([sys.executable, source],
                               cwd=os.path.dirname(source),
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

    windows = get_new_windows(before)
    written = []

    for index, window in enumerate(windows):
        suffix = ""

        if len(windows) > 1:
            suffix = "-{}".format(index + 1)

        path = os.path.join(figures, "{}{}.png".format(name, suffix))

        if get_capture(window, path):
            written.append(os.path.basename(path))

    started.send_signal(signal.SIGTERM)
    started.wait(timeout=5)

    print("  {:26} {}".format(name, ", ".join(written) or "nothing captured"))


def get_names(chapter):
    """Every example in a chapter, by the name of its file."""
    names = []

    for entry in sorted(os.listdir(os.path.join(HERE, chapter))):
        if entry.endswith(".py"):
            names.append(entry[:-3])

    return names


def main(chapter, name=None):
    """One example, or all of them."""
    if shutil.which("xdotool") is None or shutil.which("import") is None:
        print("needs xdotool and ImageMagick's import", file=sys.stderr)
    elif name is not None:
        capture(chapter, name)
    else:
        for each in get_names(chapter):
            capture(chapter, each)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: capture.py Chapter-NN [example]", file=sys.stderr)
    else:
        main(*sys.argv[1:3])
