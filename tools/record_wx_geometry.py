#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Records what the wxPython originals measure, as the tests' reference.

The examples in forge/ are run without entering MainLoop and the geometry of
every window is written to tests/wx_geometry.json. The tests then compare the
Tkinter translations against that file and need neither wxPython nor the
book's sources to do it.

    python3 tools/record_wx_geometry.py Chapter-11

Needs wxPython, a display, and forge/wxPythonInAction-src, which is not part
of this repository. Run it again when a chapter is translated, and read the
diff: a number that moves is either a better translation or a worse one, and
either way somebody should look.
"""
import json
import os
import subprocess
import sys


HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(HERE, "forge", "wxPythonInAction-src")
REFERENCE = os.path.join(HERE, "tests", "wx_geometry.json")

# The sizes each example is measured at. None is the window's natural size,
# the one Fit() gives it; the others are there because some examples only
# show what they do once there is space to share out.
SIZES = {"resizegridsizer": [None, (500, 250)],
         "resizeflexgridsizer": [None, (500, 300)],
         "boxsizer": [None, (200, 300)]}


def get_frames(chapter, name):
    """Run one example far enough to have windows, and hand them back."""
    import wx

    wx.App.MainLoop = lambda self: None
    wx.Frame.Show = lambda self, show=True: None

    frames = []
    frame_init = wx.Frame.__init__

    def spy(self, *args, **kwargs):
        frame_init(self, *args, **kwargs)
        frames.append(self)

    wx.Frame.__init__ = spy

    # The originals import each other by bare name, as a program run from
    # its own directory would.
    directory = os.path.join(SOURCES, chapter)
    if directory not in sys.path:
        sys.path.insert(0, directory)

    path = os.path.join(directory, name + ".py")
    source = open(path).read()
    exec(compile(source, path, "exec"), {"__name__": "__main__"})

    return frames


def get_widgets(parent, origin_x, origin_y):
    """Every widget under a window, with coordinates relative to the window."""
    found = []

    for child in parent.GetChildren():
        position = child.GetPosition()
        size = child.GetSize()
        x = origin_x + position[0]
        y = origin_y + position[1]

        found.append({"name": child.GetName(),
                      "x": x, "y": y,
                      "width": size[0], "height": size[1]})
        found.extend(get_widgets(child, x, y))

    return found


def get_measurements(chapter, name):
    """One example, measured at each of the sizes it is asked about."""
    measurements = []

    # Built once, then resized. Building them again for the second size
    # would leave the first set alive in the same process, and
    # wx.FindWindowByName() would start answering with the wrong window.
    # SIZES lists the natural size first, so it is measured before anything
    # is stretched.
    frames = get_frames(chapter, name)

    for size in SIZES.get(name, [None]):
        for frame in frames:
            if size is not None:
                frame.SetClientSize(size)
                frame.Layout()

            client = frame.GetClientSize()
            measurements.append({"asked": size,
                                 "title": frame.GetTitle(),
                                 "width": client[0], "height": client[1],
                                 "widgets": get_widgets(frame, 0, 0)})

    return measurements


def get_names(chapter):
    """The examples of a chapter, by the name of the file that holds them."""
    names = []
    directory = os.path.join(HERE, chapter)

    for entry in sorted(os.listdir(directory)):
        if entry.endswith(".py"):
            names.append(entry[:-3])

    return names


def main(chapter):
    """Measure every example of a chapter and write the reference file."""
    reference = {}

    if os.path.exists(REFERENCE):
        reference = json.load(open(REFERENCE))

    recorded = {}

    for name in get_names(chapter):
        source = os.path.join(SOURCES, chapter, name + ".py")

        if not os.path.exists(source):
            print("  {:24} no wx original, skipped".format(name))
        else:
            # One process per example. The examples leave their windows
            # alive, and wx.FindWindowByName() then finds a widget belonging
            # to whichever example ran before. Measured in one process,
            # mingridsizer reports the window of basicgridsizer.
            done = subprocess.run(
                [sys.executable, os.path.abspath(__file__), chapter, name],
                capture_output=True, text=True)

            if done.returncode != 0:
                print("  {:24} failed:\n{}".format(name, done.stderr.strip()))
            else:
                recorded[name] = json.loads(done.stdout)
                print("  {:24} {} window(s)".format(name,
                                                    len(recorded[name])))

    reference[chapter] = recorded
    json.dump(reference, open(REFERENCE, "w"), indent=1, sort_keys=True)
    print("\n{}".format(os.path.relpath(REFERENCE, HERE)))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        # One example, in a process of its own, answering on stdout.
        print(json.dumps(get_measurements(sys.argv[1], sys.argv[2])))
    else:
        main(sys.argv[1])
