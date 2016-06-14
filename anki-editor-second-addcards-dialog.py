# -*- coding: utf-8 -*-

"""
Anki Add-on: Second Add Cards Dialog

Hotkey that launches a second AddCards dialog from an existing
AddCards instance. Pressing the hotkey after launching the second
dialog will toggle between the two. 

Hotkey: Ctrl+Shift+A

TODO: support for an arbitrary number of AddCards dialogs

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

#============USER CONFIGURATION START===============

open_editor_hotkey = "Ctrl+Shift+A"

#==============USER CONFIGURATION END===============

from aqt import dialogs, addcards
from aqt.addcards import AddCards
from aqt.qt import *
from anki.hooks import addHook, remHook, wrap
from anki.sound import clearAudioQueue
from aqt.utils import saveGeom, restoreGeom

dialogs._dialogs["AddCards2"] = [addcards.AddCards, None]

def myInit(self, mw):
    curDialogs = dialogs._dialogs
    self.dialogName = "AddCards"
    # existing instance → open second instance
    if curDialogs[self.dialogName][1] != None:
        self.dialogName = "AddCards2"
        self.setWindowTitle(_("Add") + " 2")
        restoreGeom(self, self.dialogName)

def myReject(self):
    if not self.canClose():
        return
    remHook('reset', self.onReset)
    clearAudioQueue()
    self.removeTempNote(self.editor.note)
    self.editor.setNote(None)
    self.modelChooser.cleanup()
    self.deckChooser.cleanup()
    self.mw.maybeReset()
    # save geometry of current dialog
    saveGeom(self, self.dialogName)
    # close dialog
    dialogs.close(self.dialogName)
    QDialog.reject(self)

def switchAddWindow(self):
    curDialogs = dialogs._dialogs
    # toggle between windows
    if curDialogs["AddCards"][1] == self.parentWindow:
        dialogs.open("AddCards2", self.mw)
    else:
        dialogs.open("AddCards", self.mw)

def onSetupButtons(self):
    t = QShortcut(QKeySequence(open_editor_hotkey), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: switchAddWindow(a))

# -----------------HOOKS-------------------- #

AddCards.__init__ = wrap(AddCards.__init__, myInit, "after")
AddCards.reject = myReject
addHook("setupEditorButtons", onSetupButtons)