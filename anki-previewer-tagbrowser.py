# -*- coding: utf-8 -*-

"""
Anki Add-on: Previewer Tag Browser

This is an extension to the Advanced Previewer add-on.

Dependencies: Advanced Previewer

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

##### USER CONFIGURATION START #####

TAG_BROWSER_MODE = True

##### USER CONFIGURATION END #####

from aqt.qt import *
from aqt.browser import Browser
from anki.hooks import wrap, addHook

try:
    # requires the add-on folder to follow the default naming
    from advanced_previewer.previewer import Previewer
except ImportError:
    Previewer = None


def onSetupHotkeys(self):
    """Add additional hotkeys to the Previewer window"""
    nextTagCut = QShortcut(QKeySequence(_("Down")), 
            self, activated=lambda: self.b.onTagMove("n"))
    prevTagCut = QShortcut(QKeySequence(_("Up")), 
            self, activated=lambda: self.b.onTagMove("p"))


def onTagMove(self, target):
    """Navigate between tag entries"""
    tree = self.form.tree
    cur = tree.currentItem()
    if target == "n":
        item = tree.itemBelow(cur)
    elif target == "p":
        item = tree.itemAbove(cur)
    self.switchToSidebarItem(item)


def switchToSidebarItem(self, item):
    """Move to entry and select all cards"""
    if not item:
        return
    self.form.tree.setCurrentItem(item)
    item.onclick()
    self.form.tableView.selectAll()


def onSetFilter(self, *args, **kwargs):
    """Invoke Previewer window on tag entry click"""
    _old = kwargs["_old"]
    ret = _old(self, *args)
    if args[0] != "tag":
        return ret
    self.form.tableView.selectAll()
    if not self._previewWindow:
        self._openPreview()
    return ret


def onProfileLoaded():
    """
    Apply modifications to Browser and Previewer
    Needs to be run after all other add-ons have been loaded
    """
    Browser.onTagMove = onTagMove
    Browser.switchToSidebarItem = switchToSidebarItem
    Browser.setFilter = wrap(Browser.setFilter, onSetFilter, "around")
    Previewer.setupHotkeys = wrap(Previewer.setupHotkeys, onSetupHotkeys, "after")

if Previewer and TAG_BROWSER_MODE:
    addHook("profileLoaded", onProfileLoaded)