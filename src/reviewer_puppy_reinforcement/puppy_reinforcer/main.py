# -*- coding: utf-8 -*-
"""
Anki Add-on: Puppy Reinforcement

Uses intermittent reinforcement to encourage card review streaks

Copyright: (c) Glutanimate 2016-2018 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

import os
import random

from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

from .config import local_conf

mw.dogs = {
    "cnt": 0,
    "last": 0,
    "enc": None,
    "ivl": local_conf["encourage_every"]
}

addon_path = os.path.dirname(__file__)
dogs_dir = os.path.join(addon_path, 'images')
dogs_imgs = [i for i in os.listdir(dogs_dir)
             if i.endswith((".jpg", ".jpeg", ".png"))]

_tooltipTimer = None
_tooltipLabel = None

def dogTooltip(msg, image=":/icons/help-hint.png",
               period=local_conf["duration"], parent=None):
    global _tooltipTimer, _tooltipLabel
    class CustomLabel(QLabel):
        def mousePressEvent(self, evt):
            evt.accept()
            self.hide()
    closeTooltip()
    aw = parent or mw.app.activeWindow() or mw
    lab = CustomLabel("""\
<table cellpadding=10>
<tr>
<td><img height=%d src="%s"></td>
<td valign="middle">
    <center><b>%i cards done so far!</b><br>%s</center>
</td>
</tr>
</table>""" % (local_conf["image_height"], image, mw.dogs["cnt"], msg), aw)
    lab.setFrameStyle(QFrame.Panel)
    lab.setLineWidth(2)
    lab.setWindowFlags(Qt.ToolTip)
    p = QPalette()
    p.setColor(QPalette.Window, QColor(local_conf["tooltip_color"]))
    p.setColor(QPalette.WindowText, QColor("#000000"))
    lab.setPalette(p)
    vdiff = (local_conf["image_height"] - 128) / 2
    lab.move(
        aw.mapToGlobal(QPoint(0, -260-vdiff + aw.height())))
    lab.show()
    _tooltipTimer = mw.progress.timer(
        period, closeTooltip, False)
    _tooltipLabel = lab

def closeTooltip():
    global _tooltipLabel, _tooltipTimer
    if _tooltipLabel:
        try:
            _tooltipLabel.deleteLater()
        except:
            # already deleted as parent window closed
            pass
        _tooltipLabel = None
    if _tooltipTimer:
        _tooltipTimer.stop()
        _tooltipTimer = None

def getEncouragement(cards):
    last = mw.dogs["enc"]
    if cards >= local_conf["limit_max"]:
        lst = list(local_conf["encouragements"]["max"])
    elif cards >= local_conf["limit_high"]:
        lst = list(local_conf["encouragements"]["high"])
    elif cards >= local_conf["limit_middle"]:
        lst = list(local_conf["encouragements"]["middle"])
    else:
        lst = list(local_conf["encouragements"]["low"])
    if last and last in lst:
        # skip identical encouragement
        lst.remove(last)
    idx = random.randrange(len(lst))
    mw.dogs["enc"] = lst[idx]
    return lst[idx]

def showDog():
    mw.dogs["cnt"] += 1
    if mw.dogs["cnt"] != mw.dogs["last"] + mw.dogs["ivl"]:
        return
    image_path = os.path.join(dogs_dir, random.choice(dogs_imgs))
    msg = getEncouragement(mw.dogs["cnt"])
    dogTooltip(msg, image=image_path)
    # intermittent reinforcement:
    mw.dogs["ivl"] = max(1, local_conf["encourage_every"] +
                         random.randint(-local_conf["max_spread"],
                                        local_conf["max_spread"]))
    mw.dogs["last"] = mw.dogs["cnt"]

addHook("showQuestion", showDog)
