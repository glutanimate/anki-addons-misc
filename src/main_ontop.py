# -*- coding: utf-8 -*-

"""
Anki Add-on: "Always on-top" for all windows

Based on https://ankiweb.net/shared/info/1830523200

Makes all important Anki windows stay on top

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from anki.hooks import wrap

from aqt import dialogs
from aqt import mw, addcards, editcurrent, browser
from aqt.qt import *

def alwaysOnTop(triggered):
    mw._onTop = not mw._onTop
    windows = [mw]
    for dclass, instance in dialogs._dialogs.values():
        if instance:
            windows.append(instance)
    for window in windows:
        windowFlags = window.windowFlags()
        windowFlags ^= Qt.WindowStaysOnTopHint
        window.setWindowFlags(windowFlags)
        window.show()

def onWindowInit(self, *args, **kwargs):
    if mw._onTop:
        windowFlags = self.windowFlags() | Qt.WindowStaysOnTopHint
        self.setWindowFlags(windowFlags)
        self.show()
    
mw._onTop = False
action = QAction("Always on top", mw)
action.setCheckable(True)
action.triggered.connect(alwaysOnTop)
mw.form.menuTools.addAction(action)

addcards.AddCards.__init__ = wrap(
    addcards.AddCards.__init__, onWindowInit, "after")
editcurrent.EditCurrent.__init__ = wrap(
    editcurrent.EditCurrent.__init__, onWindowInit, "after")
browser.Browser.__init__ = wrap(
    browser.Browser.__init__, onWindowInit, "after")