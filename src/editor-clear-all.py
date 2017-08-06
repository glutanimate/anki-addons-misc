# -*- coding: utf-8 -*-

"""
Anki Add-on: Reset Editor fields

Adds hotkeys to reset the editor by various degrees.

Based on Clear All Editor Fields add-on by Mirco Kraenz
(https://github.com/proSingularity/anki2-addons)

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""


from anki.hooks import addHook
from aqt.qt import *
from aqt import mw, browser

excluded_from_clearing = ["Quellen"]

clear_all_shortcut = "Ctrl+Alt+Shift+R"
clear_most_shortcut = "Ctrl+Shift+R"
    
def clear_all_editor_fields(self, mode):
    u'''Remove text from fields in editor. '''
    note = self.note
    # enumerate all fieldNames of the current note
    for c, field_name in enumerate(self.mw.col.models.fieldNames(note.model())):
        if mode == "most" and field_name in excluded_from_clearing:
            continue
        note[field_name] = ''
    self.loadNote()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)
    self.web.eval('saveField("key");')


def onSetupButtons(self):
    if not isinstance(self.parentWindow, browser.Browser):
        # avoid shortcut conflicts in browser
        t = QShortcut(QKeySequence(clear_all_shortcut), self.parentWindow)
        t.connect(t, SIGNAL("activated()"),
                  lambda a=self: clear_all_editor_fields(a, "all"))
        t = QShortcut(QKeySequence(clear_most_shortcut), self.parentWindow)
        t.connect(t, SIGNAL("activated()"),
                  lambda a=self: clear_all_editor_fields(a, "most"))

addHook("setupEditorButtons", onSetupButtons)
