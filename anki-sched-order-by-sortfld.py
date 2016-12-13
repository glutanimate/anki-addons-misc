 
# -*- coding: utf-8 -*-

"""
Anki Add-on: Sort by sort field order

Allows creating filtered decks by sort field order
Experimental add-on without much use right now.

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

from anki import consts
from anki.sched import Scheduler
from anki.hooks import wrap

DYN_SFLD = 9

def myDynOrderLabels():
    return {
        0: _("Oldest seen first"),
        1: _("Random"),
        2: _("Increasing intervals"),
        3: _("Decreasing intervals"),
        4: _("Most lapses"),
        5: _("Order added"),
        6: _("Order due"),
        7: _("Latest added first"),
        8: _("Relative overdueness"),
        9: _("Sort field order"),
        }

def myDynOrder(self, o, l, _old):
    if o == DYN_SFLD:
        t = "n.sfld collate nocase, c.ord"
        return t + " limit %d" % l
    return _old(self, o, l)

consts.dynOrderLabels = myDynOrderLabels
Scheduler._dynOrder = wrap(Scheduler._dynOrder, myDynOrder, "around")