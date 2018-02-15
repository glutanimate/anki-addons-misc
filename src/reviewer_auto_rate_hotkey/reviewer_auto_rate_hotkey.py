# -*- coding: utf-8 -*-

"""
Anki Add-on: Hotkey to Auto-rate Based on Elapsed Time

Main module, hooks add-on methods into Anki.

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

HOTKEY_AUTORATE = "r"         # Anki 2.0 only supports single-key
                              # assignments in the reviewer

DEFAULT_LIMITS = (30, 10, 2)  # Default time limits.
                              # No need to adjust this.

##############  USER CONFIGURATION END  ##############

import time

from aqt.qt import *
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.deckconf import DeckConf
from aqt.forms import dconf
from aqt.utils import tooltip

from anki.hooks import wrap, addHook

from anki import version as anki_version
anki21 = anki_version.startswith("2.1.")


# Config related methods and hooks

def setupUi(self, Dialog):

    # Create spinbox grid:

    grid = QGridLayout()

    idx = 0
    for rating in ("Hard", "Good", "Easy"):
        lb_rating = QLabel(self.tab_5)
        lb_rating.setText("{}:".format(rating))
        sb_rating = QSpinBox(self.tab_5)
        sb_rating.setMinimum(0)
        sb_rating.setMaximum(3600)
        setattr(self, "autoRate{}".format(rating), sb_rating)
        grid.addWidget(lb_rating, 0, idx, 1, 1)
        grid.addWidget(sb_rating, 0, idx+1, 1, 1)
        idx += 2

    spacerItem = QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
    grid.addItem(spacerItem, 0, idx+1, 1, 1)
    
    # Add widgets to tab layout:

    self.line = QFrame(self.tab_5)
    self.line.setFrameShape(QFrame.HLine)
    self.line.setFrameShadow(QFrame.Sunken)
    lb_main = QLabel(self.tab_5)
    lb_main.setText("Upper answer time limits for auto rate hotkey (sec):")
    self.line2 = QFrame(self.tab_5)
    self.line2.setFrameShape(QFrame.HLine)
    self.line2.setFrameShadow(QFrame.Sunken)

    self.verticalLayout_6.insertWidget(1, self.line)
    self.verticalLayout_6.insertWidget(2, lb_main)
    self.verticalLayout_6.insertLayout(3, grid)
    self.verticalLayout_6.insertWidget(4, self.line2)


def loadConf(self):
    limits = self.conf.get('autoRate', DEFAULT_LIMITS)
    for idx, rating in enumerate(("Hard", "Good", "Easy")):
        sb_rating = getattr(self.form, "autoRate{}".format(rating), None)
        if not sb_rating:
            # should never happen
            continue
        sb_rating.setValue(limits[idx])


def saveConf(self):
    new_limits = []
    for idx, rating in enumerate(("Hard", "Good", "Easy")):
        sb_rating = getattr(self.form, "autoRate{}".format(rating), None)
        if not sb_rating:
            # should never happen
            continue
        new_limits.append(sb_rating.value())
    
    self.conf["autoRate"] = tuple(new_limits)


dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setupUi)
DeckConf.loadConf = wrap(DeckConf.loadConf, loadConf)
DeckConf.saveConf = wrap(DeckConf.saveConf, saveConf, 'before')

# Rating related methods and hooks

def saveAnswerTime(self):
    elapsed = round(time.time() - self.card.timerStarted, 1)
    self._autoRateElapsed = elapsed


Reviewer.saveAnswerTime = saveAnswerTime
addHook("showAnswer", mw.reviewer.saveAnswerTime)


def autoRate(self):
    conf = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    limits = conf.get('autoRate', DEFAULT_LIMITS)

    elapsed = getattr(mw.reviewer, "_autoRateElapsed", None)
    if elapsed is None:
        tooltip("Error: Elapsed time not registered. This should not have happened.")
        return False

    ease = 0

    for upper_limit in limits:
        ease += 1
        if elapsed > upper_limit:
            break
    else:  # easy
        ease += 1

    # limit ease to maximum button count
    # (should no longer be necessary once experimental scheduler in Anki 2.1
    # becomes the default)
    count = self.mw.col.sched.answerButtons(self.card)
    ease = min(ease, count)

    answer_buttons = self._answerButtonList()
    rating = answer_buttons[ease - 1][1]

    tooltip("Answer time: {} s<br>Rating: <b>{}</b>".format(elapsed, rating))

    self._answerCard(ease)


Reviewer.autoRate = autoRate


# Key handler related methods and hooks

if anki21:
    def _addShortcuts(shortcuts):
        """Add shortcuts on Anki 2.1.x"""
        shortcuts.append((HOTKEY_AUTORATE, mw.reviewer.autoRate))

    addHook("reviewStateShortcuts", _addShortcuts)

else:
    def _newKeyHandler(self, evt, _old):
        """Add shortcuts on Anki 2.0.x"""
        if evt.key() == QKeySequence(HOTKEY_AUTORATE)[0]:
            if self.state == "question":
                self._showAnswerHack()
            elif self.state == "answer":
                self.autoRate()
            return
        return _old(self, evt)

    Reviewer._keyHandler = wrap(
        Reviewer._keyHandler, _newKeyHandler, "around")
