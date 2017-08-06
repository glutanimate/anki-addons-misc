# -*- coding: utf-8 -*-

"""
Anki Add-on: Editor Reverse Toggle

Simple addon to quickly toggle the reverse card for a given note

(requires setting up the reverse field name below)

Hotkeys: 

Alt+Shift+B         toggle reverse field
Ctrl+Alt+Shift+B    toggle reverse field and control its frozen state
                    (meant to be used with the Frozen Fields add-on)

Copyright: (c) Glutanimate 2015-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# set reverse field name here
rev_field_name = "Bidirektional"

# set up different field content toggles
key_toggles = {
    "b": "y", # paste "y" into field
    "a": "a" # paste "a" into field
}

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from anki.hooks import addHook

def toggleFrozenState(self, state):
    model = self.note.model()
    for n, f in enumerate(model['flds']):
        fieldName = f['name']
        if fieldName == rev_field_name:
            fieldNr = n
            break
    model['flds'][n]['sticky'] = state

def toggleReverseField(self, toggle, freeze=False):
    if rev_field_name not in self.note:
        return
    if self.note[rev_field_name] == toggle:
        self.note[rev_field_name] = ""
        if freeze:
            toggleFrozenState(self, False)
    else:
        self.note[rev_field_name] = toggle
        if freeze:
            toggleFrozenState(self, True)
    self.web.eval("""
        if (currentField) {
          saveField("key");
        }
    """)
    self.loadNote()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)
    self.web.eval('saveField("key");')


def onSetupButtons(self):
    for key, toggle in list(key_toggles.items()):
        
        t = QShortcut(QKeySequence("Alt+Shift+" + key), self.parentWindow)
        t.activated.connect(
            lambda x=toggle: toggleReverseField(self, x))
        
        t = QShortcut(QKeySequence("Ctrl+Alt+Shift+" + key), self.parentWindow)
        t.activated.connect(
            lambda x=toggle: toggleReverseField(self, x, freeze=True))

addHook("setupEditorButtons", onSetupButtons)