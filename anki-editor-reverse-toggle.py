# -*- coding: utf-8 -*-

"""
Anki Add-on: self Reverse Toggle

Simple addon to quickly toggle the reverse card for a given note

Hotkey: Alt+Shift+B

(requires setting up the reverse field name below)

Copyright: Glutanimate 2015 (https://github.com/Glutanimate)
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from aqt.qt import *
from anki.hooks import addHook

# set reverse field name here
rev_field_name = "Bidirektional"

def toggleReverseField(self):
    if rev_field_name in self.note:
        if self.note[rev_field_name] == "y":
            self.note[rev_field_name] = ""
        else:
            self.note[rev_field_name] = "y"
        self.web.eval("""
            if (currentField) {
              saveField("key");
            }
        """)
        self.loadNote()


def onSetupButtons(self):
    t = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_B), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda : toggleReverseField(self))

addHook("setupEditorButtons", onSetupButtons)