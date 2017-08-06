"""
Anki Add-on: Puppy Reinforcement

Uses intermittent reinforcement to encourage card review streaks

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

encourage_every = 10 # show encouragement about every n cards; default: 10
max_spread = 5 # max spread around interval
tooltip_color = "#AFFFC5" # HTML color code; default: light green
encouragements = {
    "low": ["Great job!", "Keep it up!", "Way to go!", "Keep up the good work!"],
    "middle": ["You're on a streak!", "You're crushing it!", "Don't stop now!",
            "You're doing great!"],
    "high": ["Fantastic job!", "Wow!", "Beautiful!", "Awesome!", "I'm proud of you!"],
    "max": ["Incredible!", "You're on fire!", "Bravo!", "So many cards..."]
}

##############  USER CONFIGURATION END  ##############

import os
import random

from aqt import mw
from aqt.qt import *
from anki.hooks import wrap

mw.dogs = {
    "cnt": 0,
    "last": 0,
    "enc": None,
    "ivl": encourage_every
}

dogs_dir = os.path.join(mw.pm.addonFolder(), 'puppy_reinforcement')
dogs_imgs = [i for i in os.listdir(dogs_dir) if i.endswith(".jpg")]

_tooltipTimer = None
_tooltipLabel = None

def dogTooltip(msg, image=":/icons/help-hint.png", period=3000, parent=None):
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
<td><img height=128 src="%s"></td>
<td valign="middle">
    <center><b>%i cards done so far!</b><br>%s</center>
</td>
</tr>
</table>""" % (image, mw.dogs["cnt"], msg), aw)
    lab.setFrameStyle(QFrame.Panel)
    lab.setLineWidth(2)
    lab.setWindowFlags(Qt.ToolTip)
    p = QPalette()
    p.setColor(QPalette.Window, QColor(tooltip_color))
    p.setColor(QPalette.WindowText, QColor("#000000"))
    lab.setPalette(p)
    lab.move(
        aw.mapToGlobal(QPoint(0, -260 + aw.height())))
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
    if cards >= 100:
        lst = list(encouragements["max"])
    elif cards >= 50:
        lst = list(encouragements["high"])
    elif cards >= 25:
        lst = list(encouragements["middle"])
    else:
        lst = list(encouragements["low"])
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
    mw.dogs["ivl"] = max(1, encourage_every + random.randint(-max_spread,max_spread))
    mw.dogs["last"] = mw.dogs["cnt"]

mw.reviewer.nextCard = wrap(mw.reviewer.nextCard, showDog)