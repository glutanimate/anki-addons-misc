# -*- coding: utf-8 -*-

"""
Anki Add-on: Duplicate Selected Notes 

Select any number of cards in the card browser and duplicate their notes

To use:

1) Open the card browser
2) Select the desired cards
3) Press CTRL+ALT+C or go to Edit > Duplicate Notes

A few pointers:

- All cards generated by each note will be duplicated alongside the note
- All duplicated cards will end up in the deck of the first selected cards
- The duplicated cards should look exactly like the originals
- Tags are preserved in the duplicated notes
- Review history is NOT duplicated to the new cards (they appear as new cards)
- The notes will be marked as duplicates (because they are!)

This add-on is based on "Create Copy of Selected Cards" by Kealan Hobelmann

Based on: "Create Copy of Selected Cards"
by Kealan Hobelmann (https://ankiweb.net/shared/info/787914845)

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import tooltip
from anki.utils import timestampID

def createDuplicate(self):
    mw = self.mw
    # Get deck of first selected card
    cids = self.selectedCards()
    if not cids:
        tooltip(_("No cards selected."), period=2000)
        return
    did = mw.col.db.scalar(
        "select did from cards where id = ?", cids[0])
    deck = mw.col.decks.get(did)
    if deck['dyn']:
        tooltip(_("Cards can't be duplicated when they are in a filtered deck."), period=2000)
        return
    
    # Set checkpoint
    mw.progress.start()
    mw.checkpoint("Duplicate Notes")
    self.model.beginReset()

    # Copy notes
    for nid in self.selectedNotes():
        # print "Found note: %s" % (nid)
        note = mw.col.getNote(nid)
        model = note._model
        
        # Assign model to deck
        mw.col.decks.select(deck['id'])
        mw.col.decks.get(deck)['mid'] = model['id']
        mw.col.decks.save(deck)

        # Assign deck to model
        mw.col.models.setCurrent(model)
        mw.col.models.current()['did'] = deck['id']
        mw.col.models.save(model)
        
        # Create new note
        note_copy = mw.col.newNote()
        # Copy tags and fields (all model fields) from original note
        note_copy.tags = note.tags
        note_copy.fields = note.fields

        # Refresh note and add to database
        mw.col.addNote(note_copy)
        note_copy.flush()
        
    # Reset collection and main window
    self.model.endReset()
    mw.col.reset()
    mw.reset()
    mw.progress.finish()

    tooltip(_("Notes duplicated."), period=1000)
    
    
def setupMenu(self):
    menu = self.form.menuEdit
    menu.addSeparator()

    a = menu.addAction('Create Duplicate')
    a.setShortcut(QKeySequence("Ctrl+Alt+C"))
    a.triggered.connect(lambda _, b=self: onCreateDuplicate(b))

def onCreateDuplicate(self):
    createDuplicate(self)

addHook("browser.setupMenus", setupMenu)
