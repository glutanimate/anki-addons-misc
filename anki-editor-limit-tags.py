# -*- coding: utf-8 -*-

"""
Anki Add-on: Limit Tag Selection By Deck

Limits tag selection when specific decks are active.

Only supports limiting by topmost deck right now. Only
works when deck in question is active deck. Switching to
a different deck from within the editor will not update
the available tag selection.

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
""" 

TAG_LIMITED_DECKS = ["Medizin"]

from aqt.editor import Editor
from aqt.addcards import AddCards
from aqt.tagedit import TagEdit
from anki.hooks import addHook

def myUpdateTags(self):
    taglist = None
    did = self.parentWindow.deckChooser.selectedId()
    parents = self.mw.col.decks.parents(did)
    if parents:
        # if subdeck use topmost parent deck
        did = parents[0]
    deck = self.mw.col.decks.nameOrNone(did)
    for deckname in TAG_LIMITED_DECKS:
        if deck == deckname:
            taglist = self.mw.col.tags.byDeck(did, children=True)
            break
    self.tags.setCol(self.mw.col, taglist=taglist)
    # if self.tags.col != self.mw.col:
    #     self.tags.setCol(self.mw.col)
    if not self.tags.text() or not self.addMode:
        self.tags.setText(self.note.stringTags().strip())

def mySetCol(self, col, taglist=None):
    self.col = col
    if taglist:
        l = sorted(taglist)
    else:
        if self.type == 0:
            l = sorted(self.col.tags.all())
        else:
            l = sorted(self.col.decks.allNames())
    self.model.setStringList(l)

TagEdit.setCol = mySetCol
Editor.updateTags = myUpdateTags