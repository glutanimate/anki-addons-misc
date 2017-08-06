# -*- coding: utf-8 -*-

"""
Anki Add-on: Browser search hotkeys 

Set up hotkeys for searches in the browser.

Hotkeys follow this scheme: Ctrl+S –> (_modifier_) + _key_
(hit Ctrl+S to start the key sequence, then the key assigned to 
your search, plus an optional modifier.)

You can use keyboard modifiers to control whether to add a term to the 
search, negate it, remove it, or do something else. This follows the same 
logic as the default behaviour in Anki when clicking on a search term in
the sidebar.

For instance, line 2 in the default search_shortcuts dict assigns the search
'added 1' (cards added today) to 'T'. This defines the following key sequences
in the browser:

    Ctrl+S -> T             replace search field with 'added:1'
    Ctrl+S -> Ctrl+T        add 'added:1' to existing search
    Ctrl+S -> Alt+T:        replace search field with '-added:1'
    Ctrl+S -> Ctrl+Alt+T:   add '-added:1' to existing search
    Ctrl+S -> Shift+T:      add 'or added:1' to existing search

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

#============USER CONFIGURATION START===============

# assign hotkeys to searches
search_shortcuts = {
    'A': {'search': ''},            # All together now
    'T': {'search': 'added:1'},     # Today
    'V': {'search': 'rated:1'},     # Viewed
    'G': {'search': 'rated:1:1'},   # aGain today
    'F': {'search': 'card:1'},      # First
    'C': {'search': 'deck:current'},# Current
    'N': {'search': 'is:new'},      # New
    'L': {'search': 'is:learn'},    # Learn
    'R': {'search': 'is:review'},   # Review
    'D': {'search': 'is:due'},      # Due
    'S': {'search': 'is:suspended'},# Suspended
    'B': {'search': 'is:buried'},   # Buried
    'M': {'search': 'tag:marked'},  # Marked
    'E': {'search': 'tag:leech'},   # lEech
}

# define the sequence starter hotkey
sequence_starter = "Ctrl+S"

#==============USER CONFIGURATION END==============

from aqt.qt import *
from aqt.browser import Browser
from anki.hooks import addHook

search_modifiers = {
    '': 'replace',
    'Ctrl+': 'add',
    'Alt+': 'negate',
    'Ctrl+Alt+': 'add-negate',
    'Shift+': 'add-or',
}

def setSearchField(self, search, action):
    cur = self.form.searchEdit.lineEdit().text()
    if action == "replace":
        pass
    elif action == "add":
        search  = cur + " " + search
    elif action == "negate":
        search = "-" + search
    elif action == "add-negate":
        search  = cur + " " + "-" + search
    elif action == "add-or":
        search  = cur + " or " + search
    self.form.searchEdit.lineEdit().setText(search)
    self.onSearch()

def onSetupMenus(self):
    for key, binding in search_shortcuts.items():
        search = binding["search"]
        for modifier, action in search_modifiers.items():
            key_sequence = modifier + key
            a = QShortcut(QKeySequence(sequence_starter + ', ' + key_sequence), self)
            a.activated.connect(lambda c=search,d=action: self.setSearchField(c,d))

addHook("browser.setupMenus", onSetupMenus)
Browser.setSearchField = setSearchField