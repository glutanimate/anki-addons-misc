# -*- coding: utf-8 -*-

"""
Anki Add-on: Quick Field Navigation

Implements shortcuts that allow you to navigate 
through your fields in the card editor.

Copyright: Glutanimate 2015-2020 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from anki.hooks import addHook

def changeFocusTo(self, fldnr):
    fldnr = fldnr - 1
    fldstot = len(self.note.fields) -1
    if fldnr >= fldstot or fldnr < 0:
        # ignore onid field (Note Organizer add-on)
        if self.note.model()['flds'][-1]['name'] == "onid":
            fldnr = fldstot - 1
        else:
            fldnr = fldstot
    elif self.note.model()['flds'][0]['name'] == "ID (hidden)":
        # ignore hidden ID field (Image Occlusion Enhanced)
        fldnr += 1
    self.web.setFocus()
    self.web.eval("focusField(%d);" % int(fldnr))

def onSetupShortcuts(cuts, editor):
    cuts.extend(
        [(f"Ctrl+{i}", lambda f=i: changeFocusTo(editor, f), True) for i in range(10)]
    )
    return cuts

addHook("setupEditorShortcuts", onSetupShortcuts)