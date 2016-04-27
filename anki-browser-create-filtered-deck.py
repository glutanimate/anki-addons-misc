# -*- coding: utf-8 -*-

"""
Anki Add-on: Create Filtered Deck from Browser

Creates filtered deck based on current search

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QKeySequence
from anki.hooks import addHook

def createFilteredDeck(self):
    col = self.mw.col
    search = unicode(self.form.searchEdit.lineEdit().text())
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
    self.connect(a, SIGNAL("triggered()"), lambda b=self: createFilteredDeck(b))


addHook("browser.setupMenus", setupMenu)