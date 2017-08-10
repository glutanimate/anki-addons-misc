# -*- coding: utf-8 -*-

"""
Anki Add-on: Browse Card creation.

Adds commands to the Reviewer "More" menu to open the browser on the selected card.
The browser is configured to sort based on creation date, and select the card.
Enables the card to be viewed in its  "creation context" ie notes that were created
before/after in the same deck

Copyright:  (c) Steve AW 2013 <steveawa@gmail.com>
            (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# also show options in right-click context menu?
SHOW_IN_CONTEXT_MENU = False

##############  USER CONFIGURATION END  ##############

from aqt.qt import *

import aqt
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.utils import tooltip

from anki.lang import _
from anki.hooks import wrap, runHook, addHook


def insert_reviewer_more_action(self, m):
    #self is Reviewer
    if mw.state != "review":
        return
    a = m.addAction('Browse Creation of This Card')
    a.setShortcut(QKeySequence("c"))
    a.triggered.connect(lambda _, s=mw.reviewer: browse_this_card(s))
    a = m.addAction('Browse Creation of Last Card')
    a.triggered.connect(lambda _, s=mw.reviewer: browse_last_card(s))

def browse_last_card(self):
    #self is Reviewer
    if self.lastCard():
        browse_creation_of_card(self, self.lastCard())
    else:
        tooltip("Last card not available yet.")


def browse_this_card(self):
    #self is Reviewer
    browse_creation_of_card(self, self.card)


def browse_creation_of_card(self, target_card):
    #self is Reviewer
    #Follow pattern in AddCards.editHistory()
    browser = aqt.dialogs.open("Browser", self.mw)
    deck_name = self.card.col.decks.get(target_card.did)['name']
    browser.form.searchEdit.lineEdit().setText("deck:'%s'" % deck_name)
    browser.onSearch()
    if u'noteCrt' in browser.model.activeCols:
        col_index = browser.model.activeCols.index(u'noteCrt')
        browser.onSortChanged(col_index, False)
    browser.focusCid(target_card.id)

def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if key == "c":
        browse_this_card(self)
    else:
        return _old(self, evt)

if SHOW_IN_CONTEXT_MENU:
    addHook("AnkiWebView.contextMenuEvent", insert_reviewer_more_action) 
addHook("Reviewer.contextMenuEvent", insert_reviewer_more_action)
Reviewer._keyHandler = wrap(Reviewer._keyHandler, keyHandler, "around")