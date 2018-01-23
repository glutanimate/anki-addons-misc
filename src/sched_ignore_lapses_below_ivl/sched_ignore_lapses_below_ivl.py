# -*- coding: utf-8 -*-

"""
Anki Add-on: Ignore Lapses Below Interval

Copyright: (c) 2018 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

IVL_THRESHOLD = 4  # Interval threshold in days [integer].
                   # Only lapses above this interval will
                   # be registered as such.

##############  USER CONFIGURATION END  ##############

import time
from heapq import *
from anki.sched import Scheduler


def myRescheduleLapse(self, card):
    conf = self._lapseConf(card)
    card.lastIvl = card.ivl
    if self._resched(card):
        # ==== MODIFICATIONS START ==== 
        if card.lastIvl > IVL_THRESHOLD:
            card.lapses += 1
        # ==== MODIFICATIONS END ==== 
        card.ivl = self._nextLapseIvl(card, conf)
        card.factor = max(1300, card.factor-200)
        card.due = self.today + card.ivl
        # if it's a filtered deck, update odue as well
        if card.odid:
            card.odue = card.due
    # if suspended as a leech, nothing to do
    delay = 0
    if self._checkLeech(card, conf) and card.queue == -1:
        return delay
    # if no relearning steps, nothing to do
    if not conf['delays']:
        return delay
    # record rev due date for later
    if not card.odue:
        card.odue = card.due
    delay = self._delayForGrade(conf, 0)
    card.due = int(delay + time.time())
    card.left = self._startingLeft(card)
    # queue 1
    if card.due < self.dayCutoff:
        self.lrnCount += card.left // 1000
        card.queue = 1
        heappush(self._lrnQueue, (card.due, card.id))
    else:
        # day learn queue
        ahead = ((card.due - self.dayCutoff) // 86400) + 1
        card.due = self.today + ahead
        card.queue = 3
    return delay

# Hooks

Scheduler._rescheduleLapse = myRescheduleLapse