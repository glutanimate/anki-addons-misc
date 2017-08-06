# -*- coding: utf-8 -*-

"""
Anki Add-on: Search by Edit Date

Adds two new properties to Anki's search module:

"edited:x" – will list all cards edited over the last x days
"editedon:x" – will list all cards edited x days ago

These can be used across all search interfaces that Anki provides
(Browser, Filtered Decks Creation, etc.)

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from anki.find import Finder
from anki.utils import ids2str
from anki.hooks import wrap


def findLastEdited(self, val, exact=False):
    """Find cards by edit date"""
    # self is find.Finder
    try:
        days = int(val[0])
    except ValueError:
        return
    days = max(days, 0)
   
    # first cutoff at x days ago
    cutoff1 = (self.col.sched.dayCutoff - 86400*days)
    
    if exact:
        # second cutoff at x-1 days ago
        cutoff2 = cutoff1 + 86400
        # select notes that were edited on that day
        nids = self.col.db.list(
            "select id from notes where mod between {} and {}".format(
                cutoff1, cutoff2))
    else:
        # select notes that were edited since then
        nids = self.col.db.list(
            "select id from notes where mod > {}".format(cutoff1))

    return ("c.nid in {}".format(ids2str(nids)))


def addFinder(self, col):
    """Add custom finders to search dictionary"""
    self.search["edited"] = self.findLastEdited
    self.search["editedon"] = lambda *x: self.findLastEdited(*x, exact=True)


# Hooks

Finder.findLastEdited = findLastEdited
Finder.__init__ = wrap(Finder.__init__, addFinder, "after")
