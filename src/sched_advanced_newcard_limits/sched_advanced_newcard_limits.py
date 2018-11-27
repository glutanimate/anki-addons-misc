# -*- coding: utf-8 -*-
"""
Anki Add-on: Advanced New Card Limits

Allows you to restrict new cards to less than one per day.

The deck options need to be set to 1 new card per day for
the advanced limits to apply. 

Otherwise, the deck can be given to every deck using the same deck. 

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/> and Arthur Milchior arthur@milchior.fr
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# Syntax: "deck_name": days_between_new_cards
deck_limits = {
    "Default": 2, # show 1 new card every 2 days in "Default" deck
    u"Very Slöw": 7 # deck names with unicode need to be prepended with u
}

option_limits={
    "hard": 5,
    "Chapter": 2,
}
#In ANKI21, you can edit the options in the configuration manager,
#instead of here. Thus, the configurations will be kept when the
#add-on is updated.

##############  USER CONFIGURATION END  ##############
from anki import version as anki_version
import aqt
anki21 = anki_version.startswith("2.1.")
if anki21:
    userOption = aqt.mw.addonManager.getConfig(__name__)
    deck_limits.update(userOption["deck limits"])
    option_limits.update(userOption["option limits"])
    
from anki.sched import Scheduler
from anki.schedv2 import Scheduler as SchedulerV2

def debug(t):
    print(t)
    pass
def myDeckNewLimitSingle(self, g):
    """Limit for deck without parent limits,
    modified to only show cards every n days"""
    debug(f"Calling myDeckNewLimitSingle({g})")
    if g['dyn']:
        return self.reportLimit
    did = g['id']
    c = self.col.decks.confForDid(did)
    cname = c['name']
    deck = self.col.decks.nameOrNone(did)
    per_day = c['new']['perDay']
    lim = max(0, per_day - g['newToday'][1])
    if cname in option_limits:
        our_limit = option_limits[cname]
    elif per_day <= 1 and deck in deck_limits and deck_limits[deck] != 1:
        our_limit = deck_limits[deck]
    else:
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
    if ddays < our_limit:
        lim = 0
    # print ddays
    return lim

Scheduler._deckNewLimitSingle = myDeckNewLimitSingle
SchedulerV2._deckNewLimitSingle = myDeckNewLimitSingle
