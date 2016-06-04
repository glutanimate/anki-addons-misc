# -*- coding: utf-8 -*-

"""
Anki Add-on: Replace tag

Replace tag in selected notes. Combines tag 'add' and 'remove' dialogs
in one workflow.

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QMenu, QKeySequence

from aqt.utils import getText, tooltip
from aqt.tagedit import TagEdit
from anki.hooks import addHook


def myGetTag(parent, deck, question, tags="user", taglist=None, **kwargs):
    te = TagEdit(parent)
    te.setCol(deck)
    if taglist is not None:
        # set tag list manually
        te.model.setStringList(taglist)
    ret = getText(question, parent, edit=te, **kwargs)
    te.hideCompleter()
    return ret

def replaceTag(self):
    mw = self.mw
    selected = self.selectedNotes()
    if not selected:
        tooltip("No cards selected.", period=2000)
        return
    
    firstNote =  mw.col.getNote(selected[0])
    msg = "Which tag would you like to replace?<br>Please select just one."
    (oldTag, r) = myGetTag(self, mw.col, msg, taglist=firstNote.tags, title="Choose tag")
    if not r or not oldTag.strip():
        return
    oldTag = oldTag.split()[0]

    msg = "Which tag would you like to replace %s with?" % oldTag
    (newTag, r) = myGetTag(self, mw.col, msg, title="Replace Tag", default=oldTag)
    if not r or not newTag.strip():
        return

    mw.checkpoint("replace tag")
    mw.progress.start()
    self.model.beginReset()
    for nid in selected:
        note = mw.col.getNote(nid)
        if note.hasTag(oldTag):
            note.delTag(oldTag)
            note.addTag(newTag)
            note.flush()
    self.model.endReset()
    mw.requireReset()
    mw.progress.finish()
    mw.reset()
    tooltip("Tag replaced. <br>Use 'Check Database' to remove unused tags.")

def setupMenu(self):
    try:
        # used by multiple add-ons, so we check for its existence first
        menu = self.menuTags
    except:
        self.menuTags = QMenu(_("&Tags"))
        action = self.menuBar().insertMenu(self.mw.form.menuTools.menuAction(), self.menuTags)
    menu = self.menuTags
    menu.addSeparator()
    a = menu.addAction('Replace Tag...')
    a.setShortcut(QKeySequence("Ctrl+Alt+Shift+T"))
    self.connect(a, SIGNAL("triggered()"), lambda b=self: replaceTag(b))


addHook("browser.setupMenus", setupMenu)