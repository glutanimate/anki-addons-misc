# -*- coding: utf-8 -*-

"""
Anki Add-on: Advanced New Card Limits

Allows you to restrict new cards to less than one per day.

The deck options need to be set to 1 new card per day for
the advanced limits to apply.

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# Syntax: "deck_name": days_between_new_cards
deck_limits = {
    "Default": 2, # show 1 new card every 2 days in "Default" deck
    u"Very Slöw": 7 # deck names with unicode need to be prepended with u
}

##############  USER CONFIGURATION END  ##############

from anki.sched import Scheduler

def myDeckNewLimitSingle(self, g):
    """Limit for deck without parent limits,
    modified to only show cards every n days"""
    if g['dyn']:
        return self.reportLimit
    did = g['id']
    c = self.col.decks.confForDid(did)
    deck = self.col.decks.nameOrNone(did)
    per_day = c['new']['perDay']
    lim = max(0, per_day - g['newToday'][1])
    if per_day > 1 or deck not in deck_limits or deck_limits[deck] == 1:
        return lim

    dsel = "cid in (select id from cards where did = %s)" % did
    last = self.col.db.scalar(
        "select id from revlog where type = 0 and ivl > 0 and %s order by id desc limit 1" % dsel)
    if not last:
        return lim
    last_new = last/1000
    last_cutoff = self.dayCutoff - 86400
    # days between last graduation and yesterday's cutoff:
    ddays = -(-(last_cutoff - last_new) // 86400.0) # ceil
    if ddays < deck_limits[deck]:
        lim = 0
    # print ddays
    return lim

Scheduler._deckNewLimitSingle = myDeckNewLimitSingle