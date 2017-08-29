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

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt import mw

def onFullScreen():
    mw.setWindowState(mw.windowState() ^ Qt.WindowFullScreen)
    if mw.windowState() != Qt.WindowFullScreen:
        mw.menuBar().show()
    else:
        mw.menuBar().hide()

QShortcut(QKeySequence(KEY_FULLSCREEN_TOGGLE), mw, 
    activated=onFullScreen)
