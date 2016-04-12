# -*- coding: utf-8 -*-

"""
Anki Add-on: Editor Reverse Toggle

Simple addon to quickly toggle the reverse card for a given note

Hotkey: Alt+Shift+B

(requires setting up the reverse field name below)

Copyright: Glutanimate 2015 (https://github.com/Glutanimate)
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from aqt import editor
from aqt.qt import *
from anki.hooks import addHook

rev_field_name = "Bidirektional"

def toggleReverseField(editor):
    # set  reverse field name here
    if rev_field_name in editor.note:
      if editor.note[rev_field_name] == "y":
        editor.note[rev_field_name] = ""
      else:
        editor.note[rev_field_name] = "y"
      editor.web.eval("""
          if (currentField) {
            saveField("key");
          }
      """)
      editor.loadNote()


# assign hotkey
def onSetupButtons(editor):
    t = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_B), editor.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda : toggleReverseField(editor))

addHook("setupEditorButtons", onSetupButtons)