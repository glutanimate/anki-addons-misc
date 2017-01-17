# -*- coding: utf-8 -*-

"""
Anki Add-on: Create Filtered Deck of All Cards Scheduled for Today

Adds the search term "is:today" to the filtered deck creation dialog
which includes the following cards:

- all cards due for today, according to each deck's review limit
- all new cards "due for today", according to each deck's new card limit

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

import random

from anki.sched import Scheduler
from anki.hooks import wrap

def onUpdateStats(self, card, type, cnt=1):
    """Increment card counts for original decks"""
    # only applies to filtered decks using our special syntax
    key = type+"Today"
    if card.odid:
        conf = self.col.decks.confForDid(card.did)
        if "is:today" not in conf["terms"][0][0]:
            return
        for g in ([self.col.decks.get(card.odid)] +
                  self.col.decks.parents(card.odid)):
            # add
            g[key][1] += cnt
            self.col.decks.save(g)

def myFillDyn(self, deck, _old):
    """Fill filtered deck using custom filter"""
    search, limit, order = deck['terms'][0]
    if search == "is:today":
        ids = self.dynToday(order)
        # move the cards over
        self.col.log(deck['id'], ids)
        self._moveToDyn(deck['id'], ids)
        return ids
    else:  
        return _old(self, deck)


def dynToday(self, order=False):
    """Find all cards that are scheduled for today"""
    dids = self.col.decks.allIds()
    ids = []
    for did in dids:
        newlim = self._deckNewLimit(did)
        revlim = self._deckRevLimit(did)
        # new cards according to deck limits
        ids += self.col.db.list("""
            select id from cards where did = ? and
                queue = 0 order by due limit ?""", did, newlim)
        # due cards according to deck limits
        ids += self.col.db.list("""
            select id from cards where did = %s and
                (queue in (2,3) and due <= %d) or
                (queue = 1 and due <= %d) 
                order by due limit %d""" % (did, self.today, self.dayCutoff, revlim))
    # randomize if option set
    if order == 1:
        random.shuffle(ids)
    return ids

Scheduler.dynToday = dynToday
Scheduler._fillDyn = wrap(Scheduler._fillDyn, myFillDyn, "around")
Scheduler._updateStats = wrap(Scheduler._updateStats, onUpdateStats, "after")