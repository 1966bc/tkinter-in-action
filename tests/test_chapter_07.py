#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 7: fifteen widgets, and the four that needed a decision.

Every file is checked to build. Beyond that, what is tested is the handful
of places where Tkinter does not simply hand over the same widget.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import sys
import tkinter as tk
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "Chapter-07"))

EXAMPLES = ("bitmap_button", "button", "checkbox", "choice", "combo_box",
            "gauge", "generic_button", "list_box", "radio", "radio_box",
            "slider", "spinner", "static_text", "text_ctrl",
            "text_ctrl_multiple")


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no widgets to build")
class TestChapter07(unittest.TestCase):
    """The widgets, and the four that are not simply there."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_every_example_builds(self):
        """Fifteen windows, one at a time. A widget option that Tk does
        not know raises when the widget is made, so this catches a great
        deal for what it is."""
        for name in EXAMPLES:
            module = __import__(name)
            app = module.App()
            app.update_idletasks()
            app.destroy()

    def test_a_checkbox_keeps_its_state_in_a_variable_you_hold(self):
        """wx keeps it inside the widget. Tk keeps it in a variable, and
        one held in a local is collected and takes the state with it."""
        import checkbox

        self.app = checkbox.App()

        self.assertEqual(sorted(self.app.values), ["Alpha", "Beta", "Gamma"])
        self.assertFalse(self.app.values["Beta"].get())

        self.app.values["Beta"].set(True)
        self.assertTrue(self.app.values["Beta"].get())

    def test_radio_buttons_are_grouped_by_their_variable(self):
        """Not by the order they were made in, which is what RB_GROUP
        relies on. Choosing one enables its field and disables the rest."""
        import radio

        self.app = radio.App()
        self.app.update()

        self.assertEqual(str(self.app.entries["Elmo"].cget("state")), "normal")
        self.assertEqual(str(self.app.entries["Bert"].cget("state")),
                         "disabled")

        self.app.chosen.set("Bert")
        self.app.on_radio()

        self.assertEqual(str(self.app.entries["Elmo"].cget("state")),
                         "disabled")
        self.assertEqual(str(self.app.entries["Bert"].cget("state")), "normal")

    def test_the_radio_box_is_assembled_and_answers(self):
        """wx.RadioBox is one widget. Here it is a LabelFrame and a grid,
        and it has to behave like the one widget it stands in for."""
        import radio_box

        self.app = radio_box.App()
        self.app.update()

        self.assertEqual(self.app.box_labelled.get(), "zero")

        self.app.box_labelled.value.set("five")
        self.assertEqual(self.app.box_labelled.get(), "five")
        self.assertEqual(self.app.box_plain.get(), "zero")

    def test_the_simple_combo_keeps_its_field_in_step(self):
        """wx.CB_SIMPLE has no equivalent, so this one is made of two
        widgets and the joining up is the part that can be wrong."""
        import combo_box

        self.app = combo_box.App()
        self.app.update()

        simple = self.app.cb_simple
        simple.lst_values.selection_set(4)
        simple.on_select(None)

        self.assertEqual(simple.get(), "four")

    def test_a_slider_has_ticks_which_the_themed_one_cannot(self):
        """The one place in the book where tk is chosen over ttk on
        purpose. If ttk.Scale ever grows tickinterval, this can change."""
        import slider

        self.app = slider.App()
        self.app.update()

        self.assertEqual(int(self.app.scl_across.cget("tickinterval")), 25)
        self.assertEqual(self.app.scl_across.get(), slider.START)

        self.assertRaises(tk.TclError, tk.ttk.Scale, self.app,
                          tickinterval=25)

    def test_text_tags_do_what_TE_RICH2_asks_the_platform_for(self):
        """And do it everywhere. The tag covers the range it was given,
        and can be asked which ranges those are, which wx cannot."""
        import text_ctrl_multiple

        self.app = text_ctrl_multiple.App()
        self.app.update()

        ranges = self.app.txt_rich.tag_ranges("reversed")

        self.assertEqual(len(ranges), 2)
        self.assertEqual(self.app.txt_rich.get(*ranges), "reversed")

    def test_a_password_field_hides_and_does_not_conceal(self):
        """show="*" is about the screen. The text is in the widget in the
        clear and get() returns it, which is worth knowing before one is
        used for something that matters."""
        import text_ctrl

        self.app = text_ctrl.App()
        self.app.update()

        self.assertEqual(self.app.ent_password.cget("show"), "*")
        self.assertEqual(self.app.ent_password.get(), text_ctrl.PASSWORD)


if __name__ == "__main__":
    unittest.main()
