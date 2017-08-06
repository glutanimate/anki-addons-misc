# -*- coding: utf-8 -*-

"""
Anki Add-on: Open 'Added Today' from Reviewer.

Adds a menu item into the "History" menu of the "Add" notes dialog that
opens a Browser on the 'Added Today' view.

Copyright:  (c) Steve AW 2013 <steveawa@gmail.com>
            (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from anki.lang import _

from aqt.qt import *
from aqt.addcards import AddCards
from anki.hooks import wrap, runHook, addHook
import aqt


def insert_open_browser_action(self, m):
    m.addSeparator()
    a = m.addAction("Open Browser on 'Added &Today'")
    a.connect(a, SIGNAL("triggered()"),
              lambda self=self: show_browser_on_added_today(self))


def show_browser_on_added_today(self):
    browser = aqt.dialogs.open("Browser", self.mw)
    browser.form.searchEdit.lineEdit().setText("added:1")
    browser.onSearch()
    if u'noteCrt' in browser.model.activeCols:
        col_index = browser.model.activeCols.index(u'noteCrt')
        browser.onSortChanged(col_index, True)
    browser.form.tableView.selectRow(0)


def mySetupButtons(self):
    self.historyButton.setEnabled(True)

AddCards.showBrowserOnAddedToday = show_browser_on_added_today
AddCards.setupButtons = wrap(AddCards.setupButtons, mySetupButtons, "after")
addHook("AddCards.onHistory", insert_open_browser_action)