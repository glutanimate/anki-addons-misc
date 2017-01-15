 # -*- coding: utf-8 -*-

"""
Anki Add-on: Custom Tag Editor

Various modifications to the tag editor:

- disable initial popup when entering tag editor
- apply current completion with Enter/Return
- go to next completion with Ctrl+Tab
- show completer with Up/Down arrows

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from aqt.qt import *
from aqt.tagedit import TagEdit

def myFocusInEvent(self, evt):
    # don't show completer by default
    QLineEdit.focusInEvent(self, evt)

def myKeyPressEvent(self, evt):
    if evt.key() in (Qt.Key_Up, Qt.Key_Down):
        # show completer on up/down
        if not self.completer.popup().isVisible():
            self.showCompleter()
        return
    if (evt.key() == Qt.Key_Tab and evt.modifiers() == Qt.ControlModifier
      and self.completer.popup().isVisible()):
        # select next completion
        index = self.completer.currentIndex()
        self.completer.popup().setCurrentIndex(index)
        start = self.completer.currentRow()
        if not self.completer.setCurrentRow(start + 1):
            self.completer.setCurrentRow(0)
        return
    if evt.key() in (Qt.Key_Enter, Qt.Key_Return):
        # set current completion
        popidx = self.completer.popup().currentIndex()
        selected = QCompleter.pathFromIndex(self.completer, popidx)
        if not selected:
            # only apply completion if no list item selected:
            txt = self.text()
            pos = self.cursorPosition()
            pfx = txt[:pos]
            cur = pfx.split()[-1]
            wend = len(pfx)
            wstart = wend - len(cur)
            self.completer.setCompletionPrefix(txt[:pos])
            completion = self.completer.currentCompletion()
            self.setSelection(wstart, wend)
            self.backspace()
            self.insert(completion[wstart:])
        self.hideCompleter()
        QWidget.keyPressEvent(self, evt)
        return
    QLineEdit.keyPressEvent(self, evt)
    if not evt.text():
        # if it's a modifier, don't show
        return
    if evt.key() not in (
        Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Space,
        Qt.Key_Tab, Qt.Key_Backspace, Qt.Key_Delete):
        self.showCompleter()

TagEdit.focusInEvent = myFocusInEvent
TagEdit.keyPressEvent = myKeyPressEvent
