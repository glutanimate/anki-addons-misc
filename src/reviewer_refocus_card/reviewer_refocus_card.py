# -*- coding: utf-8 -*-

"""
Anki Add-on: Refocus Card when Reviewing

Refocuses card during reviews, so that you can use controls like
Page up / Page down.

Copyright:  (c) 2013 Edgar Simo-Serra <bobbens@gmail.com>
            (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from anki.hooks import addHook
from aqt import mw

def refocusInterface():
    mw.web.setFocus()

addHook("showQuestion", refocusInterface)
addHook("showAnswer", refocusInterface)
