# -*- coding: utf-8 -*-

"""
Anki Add-on: Toggle Full Screen Extended

Adds the ability to toggle full-screen mode. Based on Damien's
original add-on and extended with the following new features:

- Hide menu bar when in full screen mode
- Configurable shortcut

Copyright: (c) Damien Elmes 2012 <anki@ichi2.net>
           (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

KEY_FULLSCREEN_TOGGLE = "F11"
HIDE_MENU_BAR = True

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt import mw
from anki.lang import _


def onFullScreen():
    if not mw.isFullScreen():
        mw.setWindowState(mw.windowState() | Qt.WindowFullScreen)
        if HIDE_MENU_BAR:
            mw.menuBar().hide()
        custom_undo.setEnabled(True)
    else:
        mw.setWindowState(mw.windowState() ^ Qt.WindowFullScreen)
        mw.menuBar().show()
        custom_undo.setEnabled(False)
    
def myUndo():
    try:
        mw.onUndo()
    except TypeError: # no more steps back
        pass


# Restore undo shortcut that would otherwise be disabled
# due to removing the menu
custom_undo = QShortcut(QKeySequence(_("Ctrl+Z")), mw,
    activated=myUndo)
custom_undo.setEnabled(False)


QShortcut(QKeySequence(KEY_FULLSCREEN_TOGGLE), mw, 
    activated=onFullScreen)
