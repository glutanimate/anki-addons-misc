# coding: utf-8

"""
Simple Anki addon that adds a suspend hotkey to the card browser

Copyright: Glutanimate 2015 (https://github.com/Glutanimate)

License: The MIT License (MIT)
"""

from aqt.qt import *
from anki.hooks import addHook

def onBrowserSetupMenus(browser):
    c = browser.connect; f = browser.form; s = SIGNAL("triggered()")
    browser.susCut1 = QShortcut(QKeySequence("Ctrl+J"), browser)
    c(browser.susCut1, SIGNAL("activated()"), browser.onSuspend)


addHook("browser.setupMenus", onBrowserSetupMenus)