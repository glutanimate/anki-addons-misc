# -*- coding: utf-8 -*-

"""
Anki Add-on: Restore Editor fields

Looks for last created note in the same deck and copies over tags and
values of user-specified fields

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

#============USER CONFIGURATION START===============

field_restore_shortcut = "Alt+Z"
partial_restore_shortcut = "Alt+Shift+Z"
full_restore_shortcut = "Ctrl+Alt+Shift+Z"
partial_restore_fields = ["Quellen"]

#==============USER CONFIGURATION END===============

from aqt.qt import *
from anki.hooks import addHook


def restoreEditorFields(self, mode):
    # perform search
    did = self.parentWindow.deckChooser.selectedId()
    deck = self.mw.col.decks.nameOrNone(did)
    model = self.note.model() 
    if deck:
          query = "deck:'%s'" % ( deck )
          col = self.note.col
          res = col.findNotes(query)
    if not res:
        return False
    sorted_res = sorted(res, reverse=True)
    # collect old data
    oldNote = col.getNote(sorted_res[0])
    oldTags = oldNote.stringTags().strip()
    oldModel = oldNote.model()
    # restore fields
    if mode == "field":
        # restore single field
        n = self.currentField
        field = model['flds'][n]['name']
        if field in oldNote:
            self.note[field] = oldNote[field]
        else:
            try:
                self.note.fields[n] = oldNote.fields[n]
            except IndexError:
                pass
    elif mode == "partial":
        # restore defined list of fields
        self.tags.setText(oldTags)
        for field in partial_restore_fields:
            if field in oldNote:
                self.note[field] = oldNote[field]
    elif model == oldModel:
        # restore all fields
        self.tags.setText(oldTags)
        self.note.fields = oldNote.fields
    else:
        return False
    # apply changes
    if mode in ["partial", "full"]:
        # save current field
        self.web.eval("""
            if (currentField) {
              saveField("key");
            }
        """)
    self.note.flush()
    self.mw.requireReset()
    self.loadNote()


# assign hotkeys
def onSetupButtons(self):
    t = QShortcut(QKeySequence(full_restore_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a, "full"))
    t = QShortcut(QKeySequence(partial_restore_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a, "partial"))
    t = QShortcut(QKeySequence(field_restore_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a, "field"))

addHook("setupEditorButtons", onSetupButtons)