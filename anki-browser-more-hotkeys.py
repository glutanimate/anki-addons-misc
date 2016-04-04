# coding: utf-8

"""
Simple Anki addon that adds more hotkeys to the card browser

Copyright: Glutanimate 2015 (https://github.com/Glutanimate)

License: The MIT License (MIT)
"""

from aqt.qt import *
from anki.hooks import addHook

def onBrowserSetupMenus(self):
    c = self.connect; f = self.form; s = SIGNAL("triggered()")
    self.invCut = QShortcut(QKeySequence("Ctrl+Alt+I"), self)
    c(self.invCut, SIGNAL("activated()"), self.invertSelection)

    c = self.connect; f = self.form; s = SIGNAL("triggered()")
    self.schedCut = QShortcut(QKeySequence("Ctrl+R"), self)
    c(self.schedCut, SIGNAL("activated()"), self.reschedule)

addHook("browser.setupMenus", onBrowserSetupMenus)