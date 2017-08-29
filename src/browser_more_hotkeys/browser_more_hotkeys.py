# coding: utf-8

"""
Simple Anki addon that adds more hotkeys to the card browser

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from aqt.qt import *
from anki.hooks import addHook

def onBrowserSetupMenus(self):
    c = self.connect; f = self.form; s = SIGNAL("triggered()")
    self.invCut = QShortcut(QKeySequence("Ctrl+Alt+I"), self)
    c(self.invCut, SIGNAL("activated()"), self.invertSelection)

    c = self.connect; f = self.form; s = SIGNAL("triggered()")
    self.schedCut = QShortcut(QKeySequence("Ctrl+Alt+Shift+R"), self)
    c(self.schedCut, SIGNAL("activated()"), self.reschedule)

addHook("browser.setupMenus", onBrowserSetupMenus)