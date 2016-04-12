# -*- coding: utf-8 -*-

"""
Anki Add-on: Restore Editor fields

Looks for last created note in the same deck and copies over tags and
values of user-specified fields

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

from aqt.qt import *
from anki.hooks import addHook

restore_fields_shortcut = "Alt+Shift+Z"
fields_to_restore = ["Quellen"]


def restoreEditorFields(self):
    did = self.parentWindow.deckChooser.selectedId()
    deck = self.mw.col.decks.nameOrNone(did)
    if deck:
      query = "deck:'%s'" % ( deck )
      col = self.note.col
      res = col.findNotes(query)
      if res:
        sorted_res = sorted(res, reverse=True)
        last_note = col.getNote(sorted_res[0])
        last_tags = last_note.stringTags().strip()
        self.tags.setText(last_tags)
        for field in fields_to_restore:
            if field in last_note:
                self.note[field] = last_note[field]
        self.web.eval("""
            if (currentField) {
              saveField("key");
            }
        """)
        self.loadNote()



# assign hotkey
def onSetupButtons(self):
    t = QShortcut(QKeySequence(restore_fields_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a))

addHook("setupEditorButtons", onSetupButtons)