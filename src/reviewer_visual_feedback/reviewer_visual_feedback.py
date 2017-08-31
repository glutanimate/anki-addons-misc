# -*- coding: utf-8 -*-
"""
Anki Add-on: Visual Feedback for Reviews

Provides feedback for reviews by flashing a small transparent image
at the center of your screen that varies between lapses and passed cards.

Copyright:  (c) Unknown author (nest0r/Ja-Dark?) 2017
            (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# feedback duration in ms
duration = 250 # default: 250

# Images need to be located in add-on directory
#(visual_feedback folder):

# image for lapsed cards
lapsed = '_ansfeed_lapsed.png'
# image for passed cards
passed = '_ansfeed_passed.png'

##############  USER CONFIGURATION END  ##############

__version__ = "1.1.0"

from aqt.reviewer import Reviewer
from anki.hooks import addHook, wrap
from aqt import mw
from aqt.qt import *
import shutil, os

folder = 'visual_feedback'
          
def imgLoad():
    lp = [lapsed, passed]
    for p in lp:
        pth = os.path.join(mw.col.media.dir(), p)
        if not os.path.exists(pth):
            shutil.copy(os.path.join(mw.pm.addonFolder(), folder, p), p)    
            
addHook("profileLoaded", imgLoad)
          
def _keyHandler(self, evt, _old):
    key = str(evt.text())
    if self.state == "answer":
        if key == "1": 
            confirm(lapsed, duration)
        elif key in ("2", "3", "4"): 
            confirm(passed, duration)
    _old(self, evt)

def _linkHandler(self, url, _old):
    if url.startswith("ease") and self.state == "answer":
        if int(url[4:]) == 1: 
            confirm(lapsed, duration)
        elif int(url[4:]) in (2, 3, 4): 
            confirm(passed, duration) 
    _old(self, url)
        
_lab = None
_timer = None

def closeConfirm():
    global _lab, _timer
    if _lab:
        try:
            _lab.deleteLater()
        except:
            pass
        _lab = None
    if _timer:
        _timer.stop()
        _timer = None            
            
def confirm(msg, period):
    global _timer, _lab
    parent = mw.web
    closeConfirm()
    lab = QLabel('<img src="%s" align="center">' % msg, parent)
    centr = (parent.frameGeometry().center() - lab.frameGeometry().center())
    qp = QPoint( lab.width() * .25, lab.height() * .25 )
    lab.move(centr - qp)
    lab.show() 
    _timer = mw.progress.timer(period, closeConfirm, False)
    _lab = lab
    
Reviewer._keyHandler = wrap(Reviewer._keyHandler, _keyHandler, "around")
Reviewer._linkHandler = wrap(Reviewer._linkHandler, _linkHandler, "around")