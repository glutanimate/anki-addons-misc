# -*- coding: utf-8 -*-

"""
Anki Add-on: Deck Organization Actions

Allows users to assign various deck organization tasks
to a simple Tools menu entry that can be invoked via Shift+O.

Copyright: (c) 2017 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# Tuple of task dictionaries describing organization tasks
# to be performed on toggling menu entry
org_tasks = (
    {"action": "move", "orig": "source deck 1", "dest": "destination deck",
        "count": 2, "order": "added", "invert": True},
    {"action": "move", "orig": "source deck 2", "dest": "destination deck",
        "count": 2, "order": "due", "invert": False}
)
# dictinary keys and possible values:
#   "action": "move" (default) # = move new cards, only action so far
#       "orig": string, name of old deck
#       "dest": string, name of new deck
#       "count": integer, number of cards
#       "order": "due" (default) / "added" / "random"
#       "invert": True / False (default) # whether to invert card order

# Whether or not to warn when executing task more than once a day
WARN_ON_MULTIPLE_EXECUTIONS = True

##############  USER CONFIGURATION END  ##############

import time
import random

from aqt.qt import *
from aqt.utils import tooltip, askUser
from aqt import mw

VALID_ACTIONS = ("move")
VALID_ORDERS = ("due", "added", "random")


def moveCardsAction(task):
    """Move cards between decks"""
    orig = task.get("orig", None)
    dest = task.get("dest", None)
    count = task.get("count", None)
    order = task.get("order", "due")
    invert = task.get("invert", False)

    try:
        assert orig and dest and count
        assert order in VALID_ORDERS
    except AssertionError:
        return "invalid"

    orig_did = mw.col.decks.id(orig, create=False)
    if not orig_did:
        return "invalid"

    dest_did = mw.col.decks.id(dest, create=False)

    if dest_did and mw.col.decks.isDyn(dest_did):
        # cards can't be moved into filtered deck
        return "dynamic"


    cids = mw.col.decks.cids(orig_did)
    if not cids:
        return "nocids"
    
    if order in ("random", "added"):
        cmd = "select id from cards where did = ? and type=0 order by id"
    elif order == "due":
        cmd = "select id from cards where did = ? and type=0 order by due"

    scids = mw.col.db.list(cmd, orig_did)

    if order == "random":
        scids = random.sample(scids, count)
    elif invert:
        scids = scids[-count:]
    else:
        scids = scids[:count]

    if not scids:
        return "nocids"

    if not dest_did:
        # create destination deck now
        dest_did = mw.col.decks.id(dest)

    # remove any cards from filtered deck first
    mw.col.sched.remFromDyn(scids)
    # then move into new deck
    mw.col.decks.setDeck(scids, dest_did)


def performDeckOrgActions():
    """Parse org_tasks dictionary for tasks and perform them"""
    returncodes = []

    mw.checkpoint("Deck Organization Tasks")
    
    for task in org_tasks:
        
        action = task.get("action", "move")

        try:
            assert action in VALID_ACTIONS
        except AssertionError:
            print("Invalid task. Skipping")
            returncodes.append("invalid")
            continue

        ret = moveCardsAction(task)
        if ret:
            returncodes.append(ret)

    mw.reset()

    msg = ["Deck organization tasks complete."]
    if "invalid" in returncodes:
        msg.append("Warning: Your task dictionary contained invalid"
            " tasks that had to be skipped.")
    if "dynamic" in returncodes:
        msg.append("Warning: Some of your decks are filtered decks."
            "<br>Moving cards into filtered decks is not supported")
    if "nocids" in returncodes:
        msg.append("Warning: Some of the origin decks did not contain"
            "any transferable cards.<br>Actions were skipped in those"
            " instances.")
    
    info = "<br><br>".join(msg)
    tooltip(info)


def onOrganizeTask():
    """Main function. Invoked on clicking menu entry"""
    conf = mw.col.conf
    today = mw.col.sched.today # today in days since col creation time
   
    if WARN_ON_MULTIPLE_EXECUTIONS:
        # check if we've already performed tasks today:
        last = conf.get("deckOrgLast", None)
        if last and last == today:
            q = ("You have already performed this task today."
                " Are you sure you want to proceed?")
            ret = askUser(q)
            if not ret:
                return False
    
    performDeckOrgActions()
    
    conf["deckOrgLast"] = today
    mw.col.setMod()


# Menu / Hooks

action = QAction(mw)
action.setText("Perform Deck Organization Tasks")
action.setShortcut(QKeySequence("Shift+O"))
mw.form.menuTools.addAction(action)
action.triggered.connect(onOrganizeTask)