# -*- coding: utf-8 -*-

"""
Browse Card creation.

https://ankiweb.net/shared/info/3466942638

Adds commands to the Reviewer "More" menu to open the browser on the selected card.
The browser is configured to sort based on creation date, and select the card.
Enables the card to be viewed in its  "creation context" ie notes that were created
before/after in the same deck

Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Modified by Glutanimate, 2016

Support: Use at your own risk. If you do find a problem please email me
or use one the following forums, however there are certain periods
throughout the year when I will not have time to do any work on
these addons.

Github page:  https://github.com/steveaw/anki_addons
Anki addons: https://groups.google.com/forum/?hl=en#!forum/anki-addons

"""
from PyQt4.QtGui import QApplication
from anki.lang import _
from aqt.reviewer import Reviewer
from aqt.qt import QMenu, QKeySequence, QCursor, SIGNAL
from anki.hooks import wrap, runHook, addHook
from aqt import aqt


def insert_reviewer_more_action(self, m):
    #self is Reviewer
    a = m.addAction('Browse Creation of This Card')
    a.setShortcut(QKeySequence("c"))
    a.connect(a, SIGNAL("triggered()"),
              lambda s=self: browse_this_card(s))
    a = m.addAction('Browse Creation of Last Card')
    a.connect(a, SIGNAL("triggered()"),
              lambda s=self: browse_last_card(s))


def browse_last_card(self):
    #self is Reviewer
    if self.lastCard():
        browse_creation_of_card(self, self.lastCard())
    else:
         QApplication.beep()


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

addHook("Reviewer.contextMenuEvent", insert_reviewer_more_action)
Reviewer._keyHandler = wrap(Reviewer._keyHandler, keyHandler, "around")