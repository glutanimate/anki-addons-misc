# -*- coding: utf-8 -*-

"""
Anki Add-on: Editor Reverse Toggle

Simple addon to quickly toggle the reverse card for a given note

(requires setting up the reverse field name below)

Hotkeys: 

Alt+Shift+B         toggle reverse field
Ctrl+Alt+Shift+B    toggle reverse field and control its frozen state
                    (meant to be used with the Frozen Fields add-on)

Copyright: Glutanimate 2015 (https://github.com/Glutanimate)
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from aqt.qt import *
from anki.hooks import addHook

# set reverse field name here
rev_field_name = "Bidirektional"


def toggleFrozenState(self, state):
    model = self.note.model()
    for n, f in enumerate(model['flds']):
        fieldName = f['name']
        if fieldName == rev_field_name:
            fieldNr = n
            break
    model['flds'][n]['sticky'] = state

def toggleReverseField(self, freezeToggle=False):
    if rev_field_name in self.note:
        if self.note[rev_field_name] == "y":
            self.note[rev_field_name] = ""
            if freezeToggle:
                toggleFrozenState(self, False)
        else:
            self.note[rev_field_name] = "y"
            if freezeToggle:
                toggleFrozenState(self, True)
        self.web.eval("""
            if (currentField) {
              saveField("key");
            }
        """)
        self.loadNote()


def onSetupButtons(self):
    t = QShortcut(QKeySequence("Alt+Shift+B"), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda : toggleReverseField(self))
    t = QShortcut(QKeySequence("Ctrl+Alt+Shift+B"), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda : toggleReverseField(self, freezeToggle=True))

addHook("setupEditorButtons", onSetupButtons)