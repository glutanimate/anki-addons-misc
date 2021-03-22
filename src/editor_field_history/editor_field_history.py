# -*- coding: utf-8 -*-

"""
Anki Add-on: Editor Field History

Allows you to restore fields to their previous values.

Copyright: (c) 2016-2019 Glutanimate <https://glutanimate.com>
           (c) 2018 zjosua <https://github.com/zjosua>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

# ============USER CONFIGURATION START===============

# These settings only apply to Anki 2.0. For Anki 2.1 please use
# Anki's built-in add-on configuration menu

history_window_shortcut = "Ctrl+Alt+H"
field_restore_shortcut = "Alt+Z"
partial_restore_shortcut = "Alt+Shift+Z"
full_restore_shortcut = "Ctrl+Alt+Shift+Z"
# fields to restore with the partial_restore_shortcut:
partial_restore_fields = ["Quellen"]

# ==============USER CONFIGURATION END===============

from aqt.qt import *
from aqt import mw
from aqt.editor import Editor

from aqt.addcards import AddCards
from aqt.utils import getText, tooltip
from aqt.tagedit import TagEdit

from anki.utils import stripHTML, isMac
from anki.hooks import addHook

from anki import version
ANKI21 = version.startswith("2.1")


if ANKI21:
    config = mw.addonManager.getConfig(__name__)
    history_window_shortcut = config["historyWindowShortcut"]
    field_restore_shortcut = config["fieldRestoreShortcut"]
    partial_restore_shortcut = config["partialRestoreShortcut"]
    full_restore_shortcut = config["fullRestoreShortcut"]
    partial_restore_fields = config["partialRestoreFields"]
    max_notes = config["maxNotes"]

# Ctrl+Alt+H is a global hotkey on macOS
# Hacky solution for anki21. A platform-specific config.json would be
# much preferable, but is not feasible for now
if isMac and history_window_shortcut == "Ctrl+Alt+H":
    history_window_shortcut = "Ctrl+O"


class CustomTextEdit(TagEdit):

    def __init__(self, parent, strings):
        super(CustomTextEdit, self).__init__(parent, type=1)
        self.strings = strings
        self._completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)

    def focusInEvent(self, evt):
        # anki21 TagEdit does not invoke popup by default
        QLineEdit.focusInEvent(self, evt)
        self.showCompleter()

    def showCompleter(self):
        text = self.text()
        if not text:
            filtered = self.strings
        else:
            filtered = [i for i in self.strings if text.lower() in i.lower()]
        self.model.setStringList(filtered)
        self._completer.complete()


def myGetField(parent, question, last_val, **kwargs):
    edit = CustomTextEdit(parent, last_val)
    ret = getText(question, parent, edit=edit, **kwargs)
    return ret


def historyRestore(self, mode, results, model, fld):
    field = model['flds'][fld]['name']
    last_val = {}
    keys = []
    for nid in results[:max_notes]:
        oldNote = self.note.col.getNote(nid)
        if field in oldNote:
            html = oldNote[field]
        else:
            try:
                html = oldNote.fields[fld]
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


def quickRestore(self, mode, results, model, fld):
    # collect old data
    oldNote = self.note.col.getNote(results[0])
    oldTags = oldNote.stringTags().strip()
    oldModel = oldNote.model()
    # restore fields
    if mode == "field":
        # restore single field
        field = model['flds'][fld]['name']
        if field in oldNote:
            self.note[field] = oldNote[field]
        else:
            try:
                self.note.fields[fld] = oldNote.fields[fld]
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


def saveChanges(self, fld):
    self.loadNote()
    self.web.setFocus()
    if fld is not None:
        self.web.eval("focusField(%d);" % fld)
        self.web.eval('saveField("key");')


def restoreEditorFields(self, mode):
    if not self.note:  # catch invalid state
        return

    # Gather note info
    fld = self.currentField
    if fld is None and mode in ("history", "field"):
        # only necessary on anki20
        tooltip("Please select a field whose last entry you want to restore.")
        saveChanges(self, fld)
        return False
    did = self.parentWindow.deck_chooser.selectedId()
    deck = self.mw.col.decks.nameOrNone(did)
    model = self.note.model()

    # Perform search
    if deck:
        query = 'deck:"%s"' % (deck)
        results = self.note.col.findNotes(query)
    if not results:
        tooltip("Could not find any past notes in current deck.<br>"
                "If you just imported a deck you might have to restart Anki.")
        saveChanges(self, fld)
        return False
    results.sort(reverse=True)

    # Get user selection
    if mode == "history":
        ret = historyRestore(self, mode, results, model, fld)
    else:
        ret = quickRestore(self, mode, results, model, fld)
    if ret is False:
        saveChanges(self, fld)
        return False

    # Save changes
    saveChanges(self, fld)


# Assign hotkeys

def onSetupButtons20(editor):
    if not isinstance(editor.parentWindow, AddCards):
        return  # only enable in add cards dialog
    t = QShortcut(QKeySequence(full_restore_shortcut), editor.parentWindow)
    t.activated.connect(lambda: editor.restoreEditorFields("full"))
    t = QShortcut(QKeySequence(partial_restore_shortcut), editor.parentWindow)
    t.activated.connect(lambda: editor.restoreEditorFields("partial"))
    t = QShortcut(QKeySequence(field_restore_shortcut), editor.parentWindow)
    t.activated.connect(lambda: editor.restoreEditorFields("field"))
    t = QShortcut(QKeySequence(history_window_shortcut), editor.parentWindow)
    t.activated.connect(lambda: editor.restoreEditorFields("history"))


def onSetupShortcuts21(cuts, editor):
    if not isinstance(editor.parentWindow, AddCards):
        return  # only enable in AddCards dialog
    added_shortcuts = [
        (full_restore_shortcut,
            lambda: editor.restoreEditorFields("full"), True),
        (partial_restore_shortcut,
            lambda: editor.restoreEditorFields("partial"), True),
        (field_restore_shortcut,
            lambda: editor.restoreEditorFields("field")),
        (history_window_shortcut,
            lambda: editor.restoreEditorFields("history")),
    ]
    cuts.extend(added_shortcuts)


# Hooks and monkey-patches:
Editor.restoreEditorFields = restoreEditorFields

if not ANKI21:
    addHook("setupEditorButtons", onSetupButtons20)
else:
    addHook("setupEditorShortcuts", onSetupShortcuts21)
