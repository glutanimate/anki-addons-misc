# -*- coding: utf-8 -*-

"""
Anki Add-on: Convert Field to Tags

Provides a new Edit menu entry in the Browser that allows you
to convert the contents of a specific field to tags.

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

HOTKEY = "Ctrl+Alt+M"
SEPARATOR = "_" # whitespace will be replaced with this character

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt.browser import Browser
from aqt.utils import askUser, tooltip, restoreGeom, saveGeom

from anki import find
from anki.hooks import addHook
from anki.utils import stripHTML


def getField(browser, fields):
    """Invoke field selection dialog and return field"""
    d = QDialog(browser)
    l = QVBoxLayout(d)
    d.label = QLabel(
        "Please select the field you would like to convert to tags", d)
    d.fieldSel = QComboBox(d)
    d.fieldSel.addItems(fields)
    d.buttonBox = QDialogButtonBox(d)
    d.buttonBox.setOrientation(Qt.Horizontal)
    d.buttonBox.setStandardButtons(
        QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
    d.buttonBox.accepted.connect(d.accept)
    d.buttonBox.rejected.connect(d.reject)
    l.addWidget(d.label)
    l.addWidget(d.fieldSel)
    l.addWidget(d.buttonBox)
    d.setWindowModality(Qt.WindowModal)
    d.setWindowTitle("Field to Tags")
    restoreGeom(d, "fieldtotags")
    r = d.exec_()
    saveGeom(d, "fieldtotags")
    if not r:
        return None

    idx = d.fieldSel.currentIndex()
    field = fields[idx]

    return field


def fieldToTags(self, nids, field):
    """Add field contents to to note tags"""
    edited = 0
    for nid in nids:
        note = self.mw.col.getNote(nid)
        if field not in note:
            continue
        html = note[field]
        text = stripHTML(html).strip()
        if not text:
            continue
        tag = SEPARATOR.join(text.split())
        if note.hasTag(tag):
            continue
        note.addTag(tag)
        note.flush()
        edited += 1
    return edited


def onFieldToTags(self, _):
    """Main function"""
    nids = self.selectedNotes()
    count = len(nids)
    if not nids:
        tooltip("Please select some cards.")
        return
    fields = sorted(find.fieldNames(self.col, downcase=False))
    if not fields:
        tooltip("No fields found."
            "Something might be wrong with your collection")
        return
    
    field = getField(self, fields)

    if not field:
        return

    q = ("Are you sure you want to convert the <b>'{}'</b> field "
        "to tags in <b>{}</b> selected notes?".format(field, count))
    ret = askUser(q, parent=self, title="Please confirm your choice")
    if not ret:
        return

    self.mw.checkpoint("Find and Replace")
    self.mw.progress.start()
    self.model.beginReset()

    edited = self.fieldToTags(nids, field)
    
    self.model.endReset()
    self.mw.progress.finish()
    tooltip("{} out of {} notes updated.".format(edited, count))


# Hooks

def setupMenu(self):
    menu = self.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Convert Field to Tags...')
    a.setShortcut(QKeySequence(HOTKEY))
    a.triggered.connect(self.onFieldToTags)

addHook("browser.setupMenus", setupMenu)
Browser.onFieldToTags = onFieldToTags
Browser.fieldToTags = fieldToTags