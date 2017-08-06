# -*- coding: utf-8 -*-

"""
Anki Add-on: Create Filtered Deck from Browser

Creates filtered deck based on current search

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

from aqt.qt import *
from anki.hooks import addHook

def createFilteredDeck(self):
    col = self.mw.col
    search = self.form.searchEdit.lineEdit().text()
    if 'deck:current' in search:
        did = col.conf['curDeck']
        curDeck = col.decks.get(did)['name']
        search = search.replace('deck:current', '"deck:' + curDeck + '"')
    self.mw.onCram(search)
    
def setupMenu(self):
    menu = self.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Create Filtered Deck based on this Search')
    a.setShortcut(QKeySequence("Ctrl+Shift+D"))
    a.triggered.connect(lambda _, b=self: createFilteredDeck(b))

addHook("browser.setupMenus", setupMenu)