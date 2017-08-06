# -*- coding: utf-8 -*-

"""
Anki Add-on: Paste Sources into Editor

Use a hotkey to replace / add to the Sources field from your clipboard

Based in part on paste_to_my_field by Mirco Kraenz
(https://github.com/proSingularity/anki2-addons)

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

SHORTCUT_REPLACE_PASTE = "Alt+Shift+V"
SHORTCUT_ADD_PASTE =  "Ctrl+Alt+Shift+V"
SOURCE_FIELD = "Quellen"

##############  USER CONFIGURATION END  ##############

from PyQt4.QtGui import QClipboard

from aqt.qt import *
from anki.hooks import addHook

def pasteIntoField(self, action):
    '''Paste clipboard text to field specified by constant SOURCE_FIELD '''
    mode = QClipboard.Clipboard
    note = self.note
    cb = self.mw.app.clipboard().mimeData(mode=mode)
    if cb.hasText():
        cb_text = cb.text()
    if cb_text and SOURCE_FIELD in note:
        if action == "replace":
            # replace existing contents
            note[SOURCE_FIELD] = cb_text
        elif action == "add":
            # add to existing contents
            curr = note[SOURCE_FIELD]
            new = curr + "<br>" + cb_text
            note[SOURCE_FIELD] = new
        self.web.eval("""
            if (currentField) {
              saveField("key");
            }
        """)
        self.loadNote()

# assign hotkey
def onSetupButtons(self):
    t = QShortcut(QKeySequence(SHORTCUT_REPLACE_PASTE), self.widget)
    t.activated.connect(lambda a=self: pasteIntoField(a, "replace"))
    t = QShortcut(QKeySequence(SHORTCUT_ADD_PASTE), self.widget)
    t.activated.connect(lambda a=self: pasteIntoField(a, "add"))

addHook("setupEditorButtons", onSetupButtons)