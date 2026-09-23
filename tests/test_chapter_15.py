#!/usr/bin/python3
# -----------------------------------------------------------------------------
# project:  tkinter-in-action
# authors:  1966bc aka Giuseppe Costanzi
# licence:  MIT, see LICENSE
# -----------------------------------------------------------------------------
"""Chapter 15: trees, and the branch that is not built until it is asked for.

Run them from the project directory:

    python3 -m unittest discover -s tests -v
"""
import os
import sys
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


def count(nodes):
    """How many nodes there are under a branch of the sample data."""
    total = 0

    for name, note, children in nodes:
        total = total + 1 + count(children)

    return total


@unittest.skipUnless(has_display(), "no display, no tree to climb")
class TestChapter15(unittest.TestCase):
    """What is in the tree, and when it got there."""

    def setUp(self):
        """Every test builds and destroys its own window."""
        chapter.use("Chapter-15")
        self.app = None

    def tearDown(self):
        """A Tk instance left alive would be the next test's parent."""
        if self.app is not None:
            self.app.destroy()

    def test_the_whole_hierarchy_is_built_at_once(self):
        """tree_simple does what the original does, which is fine until
        the hierarchy is large."""
        import data
        import tree_simple

        self.app = tree_simple.App()
        self.app.update()

        found = []
        stack = [self.app.root]

        while stack:
            item = stack.pop()
            found.append(item)
            stack.extend(self.app.trv_tree.get_children(item))

        self.assertEqual(len(found), count(data.TREE) + 1)

    def test_the_root_of_a_treeview_is_an_absence(self):
        """"" is not an item. Which is why a Treeview can have several
        top-level items and a wx.TreeCtrl cannot."""
        import tree_simple

        self.app = tree_simple.App()
        self.app.update()

        self.assertEqual(len(self.app.trv_tree.get_children("")), 1)

        self.app.trv_tree.insert("", tk.END, text="Another root")
        self.assertEqual(len(self.app.trv_tree.get_children("")), 2)

    def test_the_icon_is_swapped_by_hand_when_a_branch_opens(self):
        """wx keeps a separate image for the expanded state. A Treeview
        item has one image and no notion of being open."""
        import tree_icons

        self.app = tree_icons.App()
        self.app.update()

        branch = self.app.trv_tree.get_children(self.app.root)[0]
        shut = self.app.trv_tree.item(branch, "image")

        self.app.trv_tree.focus(branch)
        self.app.on_open(None)

        self.assertNotEqual(self.app.trv_tree.item(branch, "image"), shut)

        self.app.on_close(None)
        self.assertEqual(self.app.trv_tree.item(branch, "image"), shut)

    def test_a_tree_with_columns_is_the_same_widget(self):
        """wx needs wx.gizmos.TreeListCtrl for this."""
        import tree_treelist

        self.app = tree_treelist.App()
        self.app.update()

        branch = self.app.trv_tree.get_children(self.app.root)[0]

        self.assertNotEqual(self.app.trv_tree.item(branch, "text"), "")
        self.assertNotEqual(self.app.trv_tree.set(branch, "description"), "")

    def test_a_branch_is_sorted_by_moving_its_children(self):
        """SortChildren, without a comparison method to override."""
        import tree_misc

        self.app = tree_misc.App()
        self.app.update()

        before = [self.app.trv_tree.item(item, "text")
                  for item in self.app.trv_tree.get_children(self.app.root)]

        self.app.trv_tree.focus(self.app.root)
        self.app.on_sort_children()

        after = [self.app.trv_tree.item(item, "text")
                 for item in self.app.trv_tree.get_children(self.app.root)]

        self.assertEqual(after, sorted(before))
        self.assertEqual(sorted(after), sorted(before))

    def test_a_label_is_edited_with_an_entry_put_over_it(self):
        """TR_EDIT_LABELS, built by hand. The same answer as editing a
        cell, which is the second time this book reaches for it."""
        import tree_misc

        self.app = tree_misc.App()
        self.app.update()

        branch = self.app.trv_tree.get_children(self.app.root)[0]
        self.app.trv_tree.focus(branch)
        self.app.trv_tree.selection_set(branch)
        self.app.on_edit_label()

        self.assertIsNotNone(self.app.editor)

        self.app.editor.delete(0, tk.END)
        self.app.editor.insert(0, "Renamed")
        self.app.on_end_edit(branch, True)

        self.assertIsNone(self.app.editor)
        self.assertEqual(self.app.trv_tree.item(branch, "text"), "Renamed")

    def test_escape_throws_the_edit_away(self):
        """Which is the half of in-place editing that is easy to forget."""
        import tree_misc

        self.app = tree_misc.App()
        self.app.update()

        branch = self.app.trv_tree.get_children(self.app.root)[0]
        before = self.app.trv_tree.item(branch, "text")

        self.app.trv_tree.focus(branch)
        self.app.on_edit_label()
        self.app.editor.insert(0, "rubbish")
        self.app.on_end_edit(branch, False)

        self.assertEqual(self.app.trv_tree.item(branch, "text"), before)

    def test_the_virtual_tree_builds_only_what_is_opened(self):
        """Where chapter 13's virtual list had no answer at all. A list
        is flat and has no moment; a tree has an event."""
        import data
        import tree_virtual

        self.app = tree_virtual.App()
        self.app.update()

        self.assertEqual(self.app.built, 1)
        self.assertLess(self.app.built, count(data.TREE))

        self.app.trv_tree.focus(self.app.root)
        self.app.on_open(None)

        self.assertEqual(self.app.built, 1 + len(data.TREE))
        self.assertLess(self.app.built, count(data.TREE))

    def test_an_unfilled_branch_still_looks_like_a_branch(self):
        """The dummy child. Without it the branch looks like a leaf,
        cannot be opened, and the event that would fill it never comes."""
        import tree_virtual

        self.app = tree_virtual.App()
        self.app.update()

        self.app.trv_tree.focus(self.app.root)
        self.app.on_open(None)

        branch = self.app.trv_tree.get_children(self.app.root)[0]
        children = self.app.trv_tree.get_children(branch)

        self.assertEqual(len(children), 1)
        self.assertEqual(self.app.trv_tree.item(children[0], "text"), "")


if __name__ == "__main__":
    unittest.main()
