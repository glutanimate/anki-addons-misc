"""
Anki Add-on: Puppy Reinforcement

Uses intermittent reinforcement to encourage card review streaks

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# Appearance

# duration in msec; default: 3000 (=3 sec.)
DURATION = 3000
# image height in px, tooltip is automatically scaled; default: 128
IMAGE_HEIGHT = 128
# HTML color code; default: #AFFFC5 (light green)
TOOLTIP_COLOR = "#AFFFC5"


# Behavior

# show encouragement about every n cards; default: 10
ENCOURAGE_EVERY = 10
# max spread around interval; default: 5
MAX_SPREAD = 5
# lowe card limits for encouragement levels (defaults: 100, 50, 25)
LIMIT_MAX = 100
LIMIT_HIGH = 50
LIMIT_MIDDLE = 25
# encouragements by level
ENCOURAGEMENTS = {
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
    "ivl": ENCOURAGE_EVERY
}

dogs_dir = os.path.join(mw.pm.addonFolder(), 'puppy_reinforcement')
dogs_imgs = [i for i in os.listdir(dogs_dir) if i.endswith(".jpg")]

_tooltipTimer = None
_tooltipLabel = None

def dogTooltip(msg, image=":/icons/help-hint.png", period=DURATION, parent=None):
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
</table>""" % (IMAGE_HEIGHT, image, mw.dogs["cnt"], msg), aw)
    lab.setFrameStyle(QFrame.Panel)
    lab.setLineWidth(2)
    lab.setWindowFlags(Qt.ToolTip)
    p = QPalette()
    p.setColor(QPalette.Window, QColor(TOOLTIP_COLOR))
    p.setColor(QPalette.WindowText, QColor("#000000"))
    lab.setPalette(p)
    vdiff = IMAGE_HEIGHT - 128
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
    if cards >= LIMIT_MAX:
        lst = list(ENCOURAGEMENTS["max"])
    elif cards >= LIMIT_HIGH:
        lst = list(ENCOURAGEMENTS["high"])
    elif cards >= LIMIT_MIDDLE:
        lst = list(ENCOURAGEMENTS["middle"])
    else:
        lst = list(ENCOURAGEMENTS["low"])
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
    mw.dogs["ivl"] = max(1, ENCOURAGE_EVERY + random.randint(-MAX_SPREAD,MAX_SPREAD))
    mw.dogs["last"] = mw.dogs["cnt"]

mw.reviewer.nextCard = wrap(mw.reviewer.nextCard, showDog)