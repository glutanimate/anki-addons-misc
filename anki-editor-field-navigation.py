# -*- coding: utf-8 -*-
# Copyright: 2015 Glutanimate <https://github.com/Glutanimate>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Quick Field Navigation add-on for Anki (http://ankisrs.net/)

from aqt.qt import *
from anki.hooks import addHook

def changeFocusTo(self, fldnr):
    fldnr = fldnr - 1
    fldstot = len(self.note.fields) -1
    if fldnr >= fldstot or fldnr < 0:
      fldnr = fldstot
    self.web.setFocus()
    self.web.eval("focusField(%d);" % int(fldnr))

def onSetupButtons(self):
    for i in range(0,10):
      s = QShortcut(QKeySequence("Ctrl" + "+" + str(i)), self.parentWindow)
      s.connect(s, SIGNAL("activated()"),
                lambda f=i : changeFocusTo(self, f))

    s = QShortcut(QKeySequence("Alt+Shift+F"), self.parentWindow)
    s.connect(s, SIGNAL("activated()"),
              lambda : self.web.setFocus())


addHook("setupEditorButtons", onSetupButtons)