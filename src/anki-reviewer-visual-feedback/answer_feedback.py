# -*- coding: utf-8 -*-
#   License: CC BY-SA 4.0
#  Answer Feedback
# Tested only on Anki 2.0.34
__version__ = "1.0.1"

from aqt.reviewer import Reviewer
from anki.hooks import addHook, wrap
from aqt import mw
from aqt.qt import *
import shutil, os

lapsed = '_ansfeed_lapsed.png'
passed = '_ansfeed_passed.png'
folder = 'answer_feedback'
          
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
            confirm(lapsed, 250)
        elif key in ("2", "3", "4"): 
            confirm(passed, 250)
    _old(self, evt)

def _linkHandler(self, url, _old):
    if url.startswith("ease") and self.state == "answer":
        if int(url[4:]) == 1: 
            confirm(lapsed, 250)
        elif int(url[4:]) in (2, 3, 4): 
            confirm(passed, 250) 
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