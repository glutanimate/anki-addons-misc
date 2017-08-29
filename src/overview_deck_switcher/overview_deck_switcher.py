# -*- coding: utf-8 -*-

"""
Anki Add-on: Overview Deck Switcher

Switch between decks in the deck overview screen.

Hotkeys:
Ctrl + (Shift) + Tab : Switch to next/previous deck

Options:
See below under USER CONFIGURATION

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# possible values: True False

deck_switcher_skip_filtered = True # skip filtered decks
deck_switcher_skip_empty = True # skip empty decks

# possible values: valid key sequences

deck_switcher_key_forward = "Ctrl+Tab"
deck_switcher_key_backward = "Ctrl+Shift+Tab"

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt import mw

def quickSwitchDeck(drc):
    # get info on current decks
    oldid = mw.col.decks.current()["id"]
    dl = mw.col.sched.deckDueList()
    cnt = mw.col.decks.count()
    # find index of current deck in duelist
    for i, deck in enumerate(dl):
        if deck[1] == oldid:
            idx = i
            break
    i = idx + drc
    newid = oldid
    # iterate through decks and skip based on configuration
    while (i != idx):
        if i == cnt:
            # reached end of list
            i = 0
        did = dl[i][1]
        crds = dl[i][2] + dl[i][3] + dl[i][4]
        i += drc
        if deck_switcher_skip_filtered and mw.col.decks.isDyn(did):
            continue
        if crds > 0 or not deck_switcher_skip_empty:
            newid = did
            break
    # set new did
    mw.col.decks.select(newid)
    # uncollapse parent decks if applicable
    parents = mw.col.decks.parents(newid)
    for parent in parents:
        if parent["collapsed"]:
            mw.col.decks.collapse(parent["id"])
    # refresh view
    if mw.state == "deckBrowser":
        mw.deckBrowser.refresh()
    else:
        mw.onOverview()

# Set up menu entries and hotkeys
action = QAction(mw)
action.setText("Next deck")
action.setShortcut(QKeySequence(deck_switcher_key_forward))
mw.form.menuEdit.addAction(action)
action.triggered.connect(lambda _: quickSwitchDeck(1))

action = QAction(mw)
action.setText("Previous deck")
action.setShortcut(QKeySequence(deck_switcher_key_backward))
mw.form.menuEdit.addAction(action)
action.triggered.connect(lambda _: quickSwitchDeck(-1))