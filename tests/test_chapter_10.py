#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 10: menus, which can be opened and read without a person.

A menu is one of the few things in a window that can be inspected
properly: how many entries, of what kind, with what labels and in what
state. So this chapter is tested closely.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import sys
import tkinter as tk
import unittest

import chapter

HERE = chapter.ROOT

EXAMPLES = ("add_items", "create_just_menu", "create_simple_menu",
            "disable_item", "fancy_items", "find_item", "popupmenu",
            "sub_menu", "toggle_items", "update_ui", "with_accelerator")


def has_display():
    """Whether a window can be opened at all. On X11, what DISPLAY says."""
    available = True

    if sys.platform.startswith("linux"):
        available = bool(os.environ.get("DISPLAY"))

    return available


@unittest.skipUnless(has_display(), "no display, no menus to open")
class TestChapter10(unittest.TestCase):
    """What is on a menu, and what it does."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-10")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_every_example_builds(self):
        """Eleven windows, one at a time."""
        for name in EXAMPLES:
            module = __import__(name)
            app = module.App()
            app.update_idletasks()
            app.destroy()

    def test_an_item_is_turned_off_by_its_label(self):
        """wx reaches an item by id from anywhere. Here the menu must be
        in hand and the label is the address."""
        import disable_item

        self.app = disable_item.App()
        self.app.update()

        self.assertTrue(self.app.get_enabled())
        self.assertEqual(self.app.btn_toggle.cget("text"), "Disable Item")

        self.app.on_toggle()

        self.assertFalse(self.app.get_enabled())
        self.assertEqual(self.app.btn_toggle.cget("text"), "Enable Item")

    def test_postcommand_is_what_update_ui_becomes(self):
        """It fires when the menu opens, which is the only moment the
        answer matters, and that is enough for menus and nothing else."""
        import update_ui

        self.app = update_ui.App()
        self.app.update()

        self.app.on_update_ui()
        self.assertEqual(str(self.app.menu.entrycget("Cut", "state")),
                         "disabled")

        self.app.ent_text.insert(0, "something")
        self.app.on_update_ui()
        self.assertEqual(str(self.app.menu.entrycget("Cut", "state")),
                         "normal")

    def test_an_accelerator_is_only_a_label_unless_it_is_bound(self):
        """The trap of the chapter. The option draws Ctrl-A on the menu
        and does not make it happen; the binding is what makes it happen.

        The claim is tested by looking for the binding and then running
        it, rather than by sending a synthetic Control-a. A key event has
        to be delivered by the X server to a window that has the focus,
        and under a headless display it is not - which was found by
        watching this pass here and fail in the workflow.
        """
        import with_accelerator

        self.app = with_accelerator.App()
        self.app.update()

        self.assertNotEqual(self.app.bind_all("<Control-a>"), "")

        self.app.tk.call("event", "generate", self.app, "<Control-a>",
                         "-when", "now")
        self.app.update()

        self.assertIn("Accelerated", self.app.lbl_said.cget("text"))

    def test_each_item_knows_which_one_it_is(self):
        """The lambda default argument. Without it all three items report
        the last one, and the menu works and lies."""
        import find_item

        self.app = find_item.App()
        self.app.update()

        self.app.menu.invoke(0)
        self.assertIn("First", self.app.lbl_said.cget("text"))

        self.app.menu.invoke(1)
        self.assertIn("Second", self.app.lbl_said.cget("text"))

    def test_a_menu_grows_above_the_exit_item(self):
        """insert_command and not add_command, or the new items land
        underneath Exit."""
        import add_items

        self.app = add_items.App()
        self.app.update()

        self.assertEqual(self.app.menu.index("end"), 0)

        self.app.ent_label.delete(0, tk.END)
        self.app.ent_label.insert(0, "Fresh")
        self.app.on_add()

        self.assertEqual(self.app.menu.index("Fresh"), 0)
        self.assertEqual(self.app.menu.index("Exit"), 1)

    def test_check_and_radio_items_keep_their_state_in_variables(self):
        """Held on the window, or collected and forgotten. And the radio
        items are a group because they share one, not because they are
        next to each other."""
        import toggle_items

        self.app = toggle_items.App()
        self.app.update()

        self.assertEqual(self.app.chosen.get(), toggle_items.RADIOS[0])

        self.app.checked["Check Item 2"].set(True)
        self.app.chosen.set(toggle_items.RADIOS[2])
        self.app.on_toggle()

        said = self.app.lbl_state.cget("text")
        self.assertIn("Check Item 2", said)
        self.assertIn(toggle_items.RADIOS[2], said)

    def test_a_menu_entry_takes_a_font_and_a_picture(self):
        """wx needs a wx.MenuItem for this and gets it on Windows only."""
        import fancy_items

        self.app = fancy_items.App()
        self.app.update()

        self.assertIn("bold",
                      str(self.app.menu.entrycget("Bold and blue", "font")))
        self.assertEqual(str(self.app.menu.entrycget("Bold and blue",
                                                     "foreground")), "navy")
        self.assertNotEqual(str(self.app.menu.entrycget("With a picture",
                                                        "image")), "")

    def test_the_same_class_is_bar_menu_and_popup(self):
        """One widget class and four uses, which is the chapter."""
        import popupmenu
        import sub_menu

        self.app = sub_menu.App()
        self.app.update()

        bar = self.app.nametowidget(self.app.cget("menu"))
        self.assertIsInstance(bar, tk.Menu)
        self.assertEqual(str(bar.type(0)), "cascade")

        self.app.destroy()

        self.app = popupmenu.App()
        self.assertIsInstance(self.app.popup, tk.Menu)


if __name__ == "__main__":
    unittest.main()
