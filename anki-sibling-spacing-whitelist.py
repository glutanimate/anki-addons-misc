#!/usr/bin/python
#-*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Sibling Spacing is an addon for Anki 2 - http://ankisrs.net
# ---------------------------------------------------------------------------
# Original Author:      Andreas Klauer (Andreas Klauer@metamorpher.de)
# Modified by:          Glutanimate 2016 (https://github.com/Glutanimate)
# Version:              0.02 (2016-03-17)
# License:              GPL
# ---------------------------------------------------------------------------
# 
# This modified version of the Sibling Spacing add-on follows a whitelist
# approach when adjusting scheduling of siblings. Only note models defined in
# the 'enabledModels' list will be processed.

# --- Imports: ---

from anki.hooks import addHook, wrap
from aqt import *
from aqt.utils import showInfo, tooltip

# --- Globals: ---

enabled = True
debug = True

# edit this list with the note models you want to enable
# sibling spacing on
enabledModels = [ "Erweitert - Mehrzweck", "Kunst - Bildende Kunst" ]

# --- Functions: ---

def siblingIvl(self, card, idealIvl, _old):
    origIvl = _old(self, card, idealIvl)

    if not enabled:
        return origIvl

    modelName = card.model()["name"]

    if modelName not in enabledModels:
        # if debug:
        #     print "Sibling Spacing not enabled for %s. No adjustment." % modelName
        return origIvl

    ivl = origIvl

    # Penalty
    minIvl = self.col.db.scalar('''SELECT MIN(ivl) FROM cards WHERE ivl > 0 AND nid = ? AND id != ? AND queue = 2''',
                                card.nid, card.id)

    while minIvl and minIvl > 0 and ivl > minIvl*4:
        ivl = max(1, int(ivl/2.0))

    # Boost
    delta = max(1, int(ivl * 0.15))
    boost = max(1, int(ivl * 0.5))

    siblings = True

    while siblings:
        siblings = self.col.db.scalar('''SELECT count() FROM cards WHERE due >= ? AND due <= ? AND nid = ? AND id != ? AND queue = 2''',
                                      self.today + ivl - delta, self.today + ivl + delta, card.nid, card.id)
        if siblings:
            ivl += boost

    if debug:
        if minIvl and minIvl > 0:
            print "Sibling Spacing %d%+d = %d days for card %d (sibling has %d days)" % (origIvl,ivl-origIvl,ivl,card.id,minIvl,)
            tooltip("Sibling Spacing:<center>%d<b>%+d</b> days</center>" % (origIvl,ivl-origIvl))
        else:
            print "Sibling Spacing == %d (orig:%d) days for card %d without visible siblings" % (ivl,origIvl,card.id,)

    return ivl

def toggle():
    global enabled

    enabled = not enabled

    if enabled:
        showInfo("Sibling Spacing is now ON")
    else:
        showInfo("Sibling Spacing is now OFF")

def toggle_debug():
    global debug

    debug = not debug

    if debug:
        showInfo("Sibling Spacing Debug is now ON")
    else:
        showInfo("Sibling Spacing Debug is now OFF")

def siblingMenu():
    '''Extend the addon menu with toggle.'''
    m = None

    for action in mw.form.menuPlugins.actions():
        menu = action.menu()
        if menu and menu.title() == "anki-sibling-spacing-whitelist":
            m = menu
            break

    if not m:
        return

    a = QAction(_("Toggle ON/OFF..."), mw)
    mw.connect(a, SIGNAL("triggered()"), toggle)
    m.addAction(a)
    a = QAction(_("Debug ON/OFF..."), mw)
    mw.connect(a, SIGNAL("triggered()"), toggle_debug)
    m.addAction(a)

def profileLoaded():
    # add menu entry
    mw.addonManager.rebuildAddonsMenu = wrap(mw.addonManager.rebuildAddonsMenu,
                                             siblingMenu)
    mw.addonManager.rebuildAddonsMenu()

    # add scheduler
    anki.sched.Scheduler._adjRevIvl = wrap(anki.sched.Scheduler._adjRevIvl,
                                           siblingIvl, "around")

# --- Hooks: ---

addHook("profileLoaded", profileLoaded)

# --- End of file. ---
