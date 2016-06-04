# -*- coding: utf-8 -*-

"""
Anki Add-on: Update browser on adding cards

Updates the browser view on adding a new card.

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

from anki.hooks import wrap
from aqt.addcards import AddCards

def myAddCards(self):
    self.mw.maybeReset()

AddCards.addCards = wrap(AddCards.addCards, myAddCards, "after")