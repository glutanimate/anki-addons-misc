# -*- coding: utf-8 -*-

"""
Anki Add-on: Editor Field History

Allows you to restore fields to their previous values.

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

#============USER CONFIGURATION START===============

history_window_shortcut = "Ctrl+Alt+H"
field_restore_shortcut = "Alt+Z"
partial_restore_shortcut = "Alt+Shift+Z"
full_restore_shortcut = "Ctrl+Alt+Shift+Z"
# fields to restore with the partial_restore_shortcut:
partial_restore_fields = ["Quellen"]

#==============USER CONFIGURATION END===============

from aqt.qt import *

from aqt.addcards import AddCards
from aqt.utils import getText, tooltip
from aqt.tagedit import TagEdit

from anki.utils import stripHTML, isMac
from anki.hooks import addHook

# Ctrl+Alt+H is a global hotkey on macOS
if isMac and history_window_shortcut == "Ctrl+Alt+H":
    history_window_shortcut = "Ctrl+O"

def showCompleter(self):
    text = self.text()
    if not text:
        filtered = self.strings
    else:
        filtered = [i for i in self.strings if text.lower() in i.lower()]
    self.model.setStringList(filtered)
    self.completer.complete()

def myGetField(parent, question, last_val, **kwargs):
    te = TagEdit(parent, type=1)
    te.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
    te.strings = last_val
    te.showCompleter = lambda te=te: showCompleter(te)
    ret = getText(question, parent, edit=te, **kwargs)
    te.hideCompleter()
    return ret

def historyRestore(self, mode, sorted_res, model):
    n = self.currentField
    field = model['flds'][n]['name']
    last_val = {}
    keys = []
    for nid in sorted_res[:100]:
        oldNote = self.note.col.getNote(nid)
        if field in oldNote:
            html = oldNote[field]
        else:
            try:
                html = oldNote.fields[n]
            except IndexError:
                pass
        if html.strip():
            text = stripHTML(html)
        else:
            text = None
        if text and text not in last_val:
            keys.append(text)
            last_val[text] = html
    if not last_val:
        tooltip("No prior entries for this field found.")
        return False
    txt = "Set field to:"
    (text, ret) = myGetField(self.parentWindow, 
            txt, keys, title="Field History")
    if not ret or not text.strip() or text not in last_val:
        return False
    self.note[field] = last_val[text]

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

def restoreEditorFields(self, mode):
    # perform search
    did = self.parentWindow.deckChooser.selectedId()
    deck = self.mw.col.decks.nameOrNone(did)
    model = self.note.model()
    if deck:
          query = "deck:'%s'" % (deck)
          res = self.note.col.findNotes(query)
    if not res:
        return False
    sorted_res = sorted(res, reverse=True)
    if mode == "history":
        res = historyRestore(self, mode, sorted_res, model)
    else:
        res = quickRestore(self, mode, sorted_res, model)
    if res == False:
        return False
    # apply changes
    self.loadNote()
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)
    self.web.eval('saveField("key");')

# assign hotkeys
def onSetupButtons(self):
    if not isinstance(self.parentWindow, AddCards):
        return # only enable in add cards dialog
    t = QShortcut(QKeySequence(full_restore_shortcut), self.parentWindow)
    t.activated.connect(lambda a=self: restoreEditorFields(a, "full"))
    t = QShortcut(QKeySequence(partial_restore_shortcut), self.parentWindow)
    t.activated.connect(lambda a=self: restoreEditorFields(a, "partial"))
    t = QShortcut(QKeySequence(field_restore_shortcut), self.parentWindow)
    t.activated.connect(lambda a=self: restoreEditorFields(a, "field"))
    t = QShortcut(QKeySequence(history_window_shortcut), self.parentWindow)
    t.activated.connect(lambda a=self: restoreEditorFields(a, "history"))

addHook("setupEditorButtons", onSetupButtons)
