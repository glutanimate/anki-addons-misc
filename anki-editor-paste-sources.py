# -*- coding: utf-8 -*-

"""
Anki Add-on: Paste Sources into Editor

Use a hotkey to replace / add to the Sources field from your clipboard

Based in part on paste_to_my_field by Mirco Kraenz (https://github.com/proSingularity/anki2-addons)

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

paste_replace_shortcut = "Alt+Shift+V"
paste_add_shortcut =  "Ctrl+Alt+Shift+V"

source_field_name = "Quellen"

from PyQt4.QtGui import QClipboard
from aqt.qt import *
from aqt import mw
from anki.hooks import addHook

def paste_to_my_field(self, action):
    u'''Paste clipboard text to field specified by constant source_field_name '''
    mode = QClipboard.Clipboard
    note = self.note
    cb = self.mw.app.clipboard().mimeData(mode=mode)
    if cb.hasText():
        cb_text = cb.text()
    if cb_text and source_field_name in note:
        if action == "replace":
          # replace existing contents
          note[source_field_name] = cb_text
        elif action == "add":
          # add to existing contents
          curr = note[source_field_name]
          new = curr + "<br>" + cb_text
          note[source_field_name] = new
        self.web.eval("""
            if (currentField) {
              saveField("key");
            }
        """)
        self.note.flush()
        self.mw.requireReset()
        self.loadNote()

# assign hotkey
def onSetupButtons(self):
    t = QShortcut(QKeySequence(paste_replace_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: paste_to_my_field(a, "replace"))
    t = QShortcut(QKeySequence(paste_add_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: paste_to_my_field(a, "add"))

addHook("setupEditorButtons", onSetupButtons)