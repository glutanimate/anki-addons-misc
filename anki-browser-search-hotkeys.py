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

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""

#============USER CONFIGURATION START===============

# assign hotkeys to searches
search_shortcuts = {
    'A': {'search': ''},
    'T': {'search': 'added:1'},
    'C': {'search': 'deck:current'},
    'N': {'search': 'is:new'},
    'L': {'search': 'is:learn'},
    'R': {'search': 'is:review'},
    'D': {'search': 'is:due'},
    'S': {'search': 'is:suspended'},
    'M': {'search': 'tag:marked'},
}

# define the sequence starter hotkey
sequence_starter = "Ctrl+S"

#==============USER CONFIGURATION END==============

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QKeySequence, QShortcut
from anki.hooks import addHook

search_modifiers = {
    '': 'replace',
    'Ctrl+': 'add',
    'Alt+': 'negate',
    'Ctrl+Alt+': 'add-negate',
    'Shift+': 'add-or',
}

def setSearchField(self, search, action):
    cur = unicode(self.form.searchEdit.lineEdit().text())
    if action == "replace":
        pass
    elif action == "add":
        search  = cur + " " + search
    elif action == "negate":
        search = "-" + search
    elif action == "add-negate":
        search  = cur + " " + "-" + search
    elif action == "add-or":
        search  = cur + "or" + search
    self.form.searchEdit.lineEdit().setText(search)
    self.onSearch()

def onSetupMenus(self):
    for key, binding in search_shortcuts.iteritems():
        search = binding["search"]
        for modifier, action in search_modifiers.iteritems():
            key_sequence = modifier + key
            self.a = QShortcut(QKeySequence(sequence_starter + ', ' + key_sequence), self)
            self.connect(self.a, SIGNAL("activated()"), lambda c=search,d=action: setSearchField(self,c,d))

addHook("browser.setupMenus", onSetupMenus)