# -*- coding: utf-8 -*-
# Copyright: 2015 Glutanimate <https://github.com/Glutanimate>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Anki Editor Tag Hotkeys add-on for Anki (http://ankisrs.net/)

from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

# list of tags that can only be set one at a time
# toggling the hotkey for any of these will delete any
# other unique tag found in the current tags
uniqueTags = [
    "subject-a", "subject-b"
]

def toggleTag(editor, toggledTag):
  toggledTag = toggledTag.decode('utf-8')
  currentTags = editor.tags.text().split()
  if toggledTag in currentTags:
    currentTags.remove(toggledTag)
  else:
    currentTags.append(toggledTag)
  if toggledTag in uniqueTags:
    intersectedTags = [val for val in uniqueTags if val in currentTags]
    if toggledTag in intersectedTags:
      intersectedTags.remove(toggledTag)
    for tag in intersectedTags:
      currentTags.remove(tag)
  editor.tags.setText(" ".join(currentTags))
  editor.saveTags()

def resetTags(editor):
  editor.tags.clear()

def onSetupButtons(editor):
    s = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_R), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : resetTags(editor))

    s = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_1), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleTag(editor, "toggled-tag1"))

    s = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_2), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleTag(editor, "toggled-tag2"))

    s = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_3), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleTag(editor, "toggled-tag3"))

    s = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_4), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleTag(editor, "toggled-tag4"))

    s = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_5), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleTag(editor, "subject-a"))

    s = QShortcut(QKeySequence(Qt.ALT + Qt.SHIFT + Qt.Key_6), editor.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : toggleTag(editor, "subject-b"))


addHook("setupEditorButtons", onSetupButtons)
