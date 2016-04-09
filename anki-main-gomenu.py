# -*- coding: utf-8 -*-

"""
Anki Add-on: Main window browser hotkeys

Specify hotkeys that allow you to go directly from the deck overview
to a specific search in the card browser (e.g. cards added today)

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QMenu, QKeySequence
from aqt import mw, dialogs
from anki.lang import ngettext

menu_items = {
    'Shift+T': {'search': 'added:1', 'label': 'Added today'},
    'Shift+D': {'search': 'deck:current', 'label': 'Current deck'},
}


def openBrowserWithSearch(mw, search):
    browser = dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(search)
    browser.onSearch()


go_menu = QMenu(_("&Go"))
action = mw.menuBar().insertMenu(mw.form.menuTools.menuAction(), go_menu)

for key_sequence, binding in menu_items.iteritems():
    search = binding["search"]
    label = binding["label"]
    a = go_menu.addAction(label)
    a.setShortcut(QKeySequence(key_sequence))
    a.connect(a, SIGNAL("triggered()"), lambda c=search: openBrowserWithSearch(mw, c))
