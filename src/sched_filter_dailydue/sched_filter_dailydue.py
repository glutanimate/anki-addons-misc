# -*- coding: utf-8 -*-

"""
Anki Add-on: Create Filtered Deck of All Cards Scheduled for Today

Adds the search term "is:today" to the filtered deck creation dialog
which includes the following cards:

- all cards due for today, according to each deck's review limit
- all new cards "due for today", according to each deck's new card limit

Also supports limiting to / excluding specific decks by combining
"is:today" with "deck:" phrases.

Copyright: (c) 2017 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
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
    if "is:today" in search:
        ids = self.dynToday(search, order=order)
        # move the cards over
        self.col.log(deck['id'], ids)
        self._moveToDyn(deck['id'], ids)
        return ids
    else:  
        return _old(self, deck)

def dynToday(self, search, order=False):
    """Find all cards that are scheduled for today"""
    tokens = search.split()
    dids = [int(i) for i in self.col.decks.allIds()]
    idids = []
    sdids = []
    for t in tokens:
        # set decks according to search phrase
        if t.startswith("-deck:"):
            l = idids
        elif t.startswith("deck:"):
            l = sdids
        else:
            continue
        name = ":".join(t.split(":")[1:]).replace('"', '').replace("'", "")
        deck = self.col.decks.byName(name)
        if not deck:
            continue
        did = deck["id"]
        if did not in l:
            l += [did] + [a[1] for a in self.col.decks.children(did)]
    if sdids:
        dids = sdids
    if idids:
        dids = [did for did in dids if did not in idids]
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