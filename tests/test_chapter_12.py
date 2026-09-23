#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 12: images and drawing.

The claims in this chapter are about what Tk can and cannot do with a
picture, so they are made to say so here rather than taken on trust.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import sys
import tempfile
import tkinter as tk
import unittest

import chapter

HERE = chapter.ROOT


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no images to draw")
class TestChapter12(unittest.TestCase):
    """What a PhotoImage will do, and what a canvas keeps."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-12")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_tk_scales_by_whole_numbers_only(self):
        """Scale(w, h) in wx takes any size. subsample and zoom divide
        and multiply by integers, and there is nothing in between."""
        import images

        self.app = tk.Tk()
        drawing = images.get_drawing(120, 90)

        self.assertEqual((drawing.subsample(2, 2).width(),
                          drawing.subsample(2, 2).height()), (60, 45))
        self.assertEqual(drawing.subsample(3, 3).width(), 40)
        self.assertEqual(drawing.zoom(2, 2).width(), 240)

    def test_tk_writes_only_what_it_reads(self):
        """GIF and PNG. Asking for a JPEG says so rather than guessing."""
        import images

        self.app = tk.Tk()
        drawing = images.get_drawing(40, 30)
        directory = tempfile.mkdtemp(prefix="tkinter-in-action-test-")

        for suffix in images.FORMATS:
            path = os.path.join(directory, "image." + suffix)
            drawing.write(path, format=suffix)

            self.assertTrue(os.path.exists(path))
            self.assertEqual(tk.PhotoImage(file=path).width(), 40)

        self.assertRaises(tk.TclError, drawing.write,
                          os.path.join(directory, "image.jpg"), format="jpeg")

    def test_a_picture_can_be_made_clear_a_pixel_at_a_time(self):
        """What the True at the end of wx's DrawBitmap asks for."""
        import draw_image

        self.app = tk.Tk()
        drawing = draw_image.get_drawing()

        self.assertTrue(drawing.transparency_get(0, 0))
        self.assertFalse(drawing.transparency_get(39, 39))

    def test_fifty_images_are_fifty_objects_the_canvas_keeps(self):
        """In wx they are fifty calls that happened and left no trace."""
        import draw_image

        self.app = draw_image.App()
        self.app.update()

        items = self.app.canvas.find_withtag("drawing")

        self.assertEqual(len(items), draw_image.COUNT + 1)

        # And because they are objects, one can be moved afterwards.
        self.app.canvas.move(items[0], 5, 5)
        self.assertEqual(self.app.canvas.coords(items[0]), [15.0, 15.0])

    def test_each_canvas_item_carries_its_own_appearance(self):
        """No current pen and no current brush: the width belongs to the
        item, so nothing a drawing routine sets can surprise the next."""
        import radargraph

        self.app = radargraph.App()
        self.app.update()
        self.app.graph.draw_graph()

        widths = set()

        for item in self.app.graph.find_all():
            if self.app.graph.type(item) in ("oval", "line"):
                widths.add(int(float(self.app.graph.itemcget(item, "width"))))

        self.assertEqual(widths, {1, 2})

    def test_the_graph_is_rebuilt_rather_than_patched(self):
        """delete("all") and make it again, which on a canvas is the
        right answer and not a lazy one."""
        import radargraph

        self.app = radargraph.App()
        self.app.update()

        before = len(self.app.graph.find_all())
        self.assertGreater(before, len(radargraph.RINGS))

        self.app.graph.set_data([50] * len(radargraph.LABELS))

        self.assertEqual(len(self.app.graph.find_all()), before)

    def test_the_clock_is_cancelled_with_the_window(self):
        """Chapter 7's lesson, applied. A repeating after() outlives its
        window and complains from inside the event loop."""
        import radargraph

        self.app = radargraph.App()
        self.app.update()

        self.assertIsNotNone(self.app.tick)

        self.app.destroy()
        self.assertIsNone(self.app.tick)

        self.app = None


if __name__ == "__main__":
    unittest.main()
