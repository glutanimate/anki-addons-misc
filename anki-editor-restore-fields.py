# -*- coding: utf-8 -*-

"""
Anki Add-on: Restore Editor fields

Looks for last created note in the same deck and copies over tags and
values of user-specified fields

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

#============USER CONFIGURATION START===============

history_window_shortcut = "Ctrl+Alt+H"
field_restore_shortcut = "Alt+Z"
partial_restore_shortcut = "Alt+Shift+Z"
full_restore_shortcut = "Ctrl+Alt+Shift+Z"
partial_restore_fields = ["Quellen"]

#==============USER CONFIGURATION END===============

from aqt.qt import *
from aqt.utils import getText
from aqt.tagedit import TagEdit
from anki.hooks import addHook

def myGetField(parent, question, lastValues, **kwargs):
    te = TagEdit(parent, type=1)
    te.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
    if lastValues is not None:
        # set completion list manually
        te.model.setStringList(lastValues)
    ret = getText(question, parent, edit=te, **kwargs)
    te.hideCompleter()
    return ret

def historyRestore(self, mode, sorted_res, model):
    n = self.currentField
    field = model['flds'][n]['name']
    lastValues=[]
    del sorted_res[30:] # limit to a maximum of last 30 results
    for nid in sorted_res:
        oldNote = self.note.col.getNote(nid)
        if field in oldNote:
            value = oldNote[field]
        else:
            try:
                value = oldNote.fields[n]
            except IndexError:
                pass
        if value.strip() and value not in lastValues:
            lastValues.append(value)
    guiTxt="Please select the value you would like to set the field to"
    (val, r) = myGetField(self.widget, guiTxt, lastValues, title="Field history")
    if not r or not val.strip():
        return False
    self.note[field] = val

def quickRestore(self, mode, sorted_res, model):
    # collect old data
    oldNote = self.note.col.getNote(sorted_res[0])
    oldTags = oldNote.stringTags().strip()
    oldModel = oldNote.model()
    # restore fields
    if mode == "field":
        # restore single field
        n = self.currentField
        field = model['flds'][n]['name']
        if field in oldNote:
            self.note[field] = oldNote[field]
        else:
            try:
                self.note.fields[n] = oldNote.fields[n]
            except IndexError:
                pass
    elif mode == "partial":
        # restore defined list of fields
        self.tags.setText(oldTags)
        for field in partial_restore_fields:
            if field in oldNote:
                self.note[field] = oldNote[field]
    elif model == oldModel:
        # restore all fields
        self.tags.setText(oldTags)
        self.note.fields = oldNote.fields
    else:
        return False

def restoreEditorFields(self, mode, history=False):
    # perform search
    did = self.parentWindow.deckChooser.selectedId()
    deck = self.mw.col.decks.nameOrNone(did)
    model = self.note.model()
    if deck:
          query = "deck:'%s'" % ( deck )
          res = self.note.col.findNotes(query)
    if not res:
        return False
    sorted_res = sorted(res, reverse=True)
    if history:
        res = historyRestore(self, mode, sorted_res, model)
    else:
        res = quickRestore(self, mode, sorted_res, model)
    if res == False:
        return False
    # apply changes
    if mode in ["partial", "full"]:
        # save current field
        self.web.eval("""
            if (currentField) {
              saveField("key");
            }
        """)
    self.note.flush()
    self.mw.requireReset()
    self.loadNote()


# assign hotkeys
def onSetupButtons(self):
    t = QShortcut(QKeySequence(full_restore_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a, "full"))
    t = QShortcut(QKeySequence(partial_restore_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a, "partial"))
    t = QShortcut(QKeySequence(field_restore_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a, "field"))
    t = QShortcut(QKeySequence(history_window_shortcut), self.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda a=self: restoreEditorFields(a, "field", history=True))

addHook("setupEditorButtons", onSetupButtons)