# -*- coding: utf-8 -*-

"""
Anki Add-on: External Note Editor for the Browser

Extends the card browser with a shortcut and menu action that
launches an external editor window for the current note.

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from aqt.qt import *
import aqt.editor
from aqt.utils import saveGeom, restoreGeom
from anki.hooks import addHook, remHook, wrap
from anki.utils import isMac

from aqt.browser import Browser
from aqt import dialogs

class BrowserEditCurrent(QDialog):
    """Based on editcurrent.EditCurrent"""
    def __init__(self, mw, browser):
        if isMac:
            # use a separate window on os x so we can a clean menu
            QDialog.__init__(self, None, Qt.Window)
        else:
            QDialog.__init__(self, mw)
        QDialog.__init__(self, None, Qt.Window)
        self.mw = mw
        self.browser = browser
        self.form = aqt.forms.editcurrent.Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(_("Edit Current"))
        self.setMinimumHeight(400)
        self.setMinimumWidth(500)
        self.connect(self,
                     SIGNAL("rejected()"),
                     self.onSave)
        self.form.buttonBox.button(QDialogButtonBox.Close).setShortcut(
                QKeySequence("Ctrl+Return"))
        self.editor = aqt.editor.Editor(self.mw, self.form.fieldsArea, self)
        self.editor.setNote(self.browser.card.note())
        restoreGeom(self, "browsereditcurrent")
        addHook("reset", self.onReset)
        self.mw.requireReset()
        self.show()
        # reset focus after open
        self.editor.web.setFocus()

    def onReset(self):
        # lazy approach for now: throw away edits
        try:
            n = self.browser.card.note()
            n.load()
        except:
            # card's been deleted
            remHook("reset", self.onReset)
            self.editor.setNote(None)
            self.mw.reset()
            aqt.dialogs.close("BrowserEditCurrent")
            self.close()
            return
        self.editor.setNote(n)

    def onSave(self):
        remHook("reset", self.onReset)
        self.editor.saveNow()
        self.browser.externalNid = None
        self.browser.form.splitter.widget(1).setVisible(True)
        self.browser.editor.setNote(self.browser.card.note(reload=True))
        saveGeom(self, "browsereditcurrent")
        aqt.dialogs.close("BrowserEditCurrent")

    def canClose(self):
        return True

def onDeleteNotes(self):
    """Close window before deleting notes"""
    nids = self.selectedNotes()
    if nids and self.externalNid in nids:
        self.editCurrent.close()

def onRowChanged(self, current, previous):
    """Disable inbuilt editor for externally edited note"""
    nids = self.selectedNotes()
    if nids and nids[0] == self.externalNid:
        self.form.splitter.widget(1).setVisible(False)
        self.editor.setNote(None)

def onEditWindow(self):
    """Launch BrowserEditCurrent instance"""
    nids = self.selectedNotes()
    if len(nids) != 1:
        return
    self.form.splitter.widget(1).setVisible(False)
    self.editor.setNote(None)
    self.externalNid = nids[0]
    self.editCurrent = aqt.dialogs.open("BrowserEditCurrent", self.mw, self)

def onSetupMenus(self):
    """Create menu entry and set attributes up"""
    menu = self.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Edit in New Window')
    a.setShortcut(QKeySequence("Ctrl+Alt+E"))
    a.triggered.connect(lambda _, o=self: onEditWindow(o))
    self.externalNid = None
    self.editCurrent = None

# Register new dialog in DialogManager:
dialogs._dialogs["BrowserEditCurrent"] = [BrowserEditCurrent, None]

# Hook into menu setup
addHook("browser.setupMenus", onSetupMenus)

# Modify existing methods
Browser.onRowChanged = wrap(Browser.onRowChanged, onRowChanged, "after")
Browser.deleteNotes = wrap(Browser.deleteNotes, onDeleteNotes, "before")
