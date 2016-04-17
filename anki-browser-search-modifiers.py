# -*- coding: utf-8 -*-

"""
Anki Add-on: Browser search modifiers

Adds two checkboxes to the browser search form that, when toggled, modify
searches in the following way:

Deck (Hotkey: Alt+D): Limit results to current deck
Card (Hotkey: Alt+C): Limit results to first card of each note

Based on the following add-ons:

- "Limit searches to current deck" by Damien Elmes
   (https://github.com/dae/ankiplugins/blob/master/searchdeck.py)
- "Ignore accents in browser search" by Houssam Salem
   (https://github.com/hssm/anki-addons)

Original idea by Keven on Anki tenderapp

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QKeySequence, QShortcut, QCheckBox

from aqt import *
from aqt.browser import Browser
from aqt.forms.browser import Ui_Dialog
from anki.hooks import wrap, addHook

default_checkbox_conf = {'deck_check_checked': False,
                         'card_check_checked': False}

def onSearch(self, reset=True):
    """Modify search entry."""

    txt = unicode(self.form.searchEdit.lineEdit().text()).strip()
    if self.form.deckToggleButton.isChecked():
        if "deck:" in txt:
            pass
        elif _("<type here to search; hit enter to show current deck>") in txt:
            pass
        elif "is:current" in txt:
            pass
        elif not txt.strip():
            txt = "deck:*"
        else:
            txt = "deck:current " + txt
    if self.form.cardToggleButton.isChecked():
        if "card:" in txt:
            pass
        elif _("<type here to search; hit enter to show current deck>") in txt:
            pass
        else:
            txt = "card:1 " + txt
    self.form.searchEdit.lineEdit().setText(txt)
   
def mySetupUi(self, mw):
    """Add new items to the browser UI to allow toggling the add-on."""

    # Our UI stuff
    self.deckToggleButton = QCheckBox("Deck", self.widget)
    self.cardToggleButton = QCheckBox("Card", self.widget)
    self.deckToggleButton.setToolTip("Limit results to current deck")
    self.cardToggleButton.setToolTip("Limit results to first card of each note")

    # Restore checked state
    if not 'browser_checkbox_conf' in mw.col.conf:
        mw.col.conf['browser_checkbox_conf'] = default_checkbox_conf
    self.deckToggleButton.setCheckState(
        mw.col.conf['browser_checkbox_conf']['deck_check_checked'])
    self.cardToggleButton.setCheckState(
        mw.col.conf['browser_checkbox_conf']['card_check_checked'])

    # Save state on toggle
    mw.connect(self.deckToggleButton, SIGNAL("stateChanged(int)"), onDeckChecked)
    mw.connect(self.cardToggleButton, SIGNAL("stateChanged(int)"), onCardChecked)
    
    # Add our items to the right of the search box. We do this by moving
    # every widget out of the gridlayout and into a new list. We simply
    # add our stuff in the new list in the right place before moving them
    # back to gridlayout.
    n_items = self.gridLayout.count()
    items= []
    for i in range(0, n_items):
        item = self.gridLayout.itemAt(i).widget()
        items.append(item)
        if item == self.searchEdit:
            items.append(self.deckToggleButton)
            items.append(self.cardToggleButton)
    
    for i, item in enumerate(items):
        self.gridLayout.addWidget(item, 0, i, 1, 1)
        
    
def onDeckChecked(state):
    '''Save the checked state in Anki's configuration.'''
    mw.col.conf['browser_checkbox_conf']['deck_check_checked'] = state
def onCardChecked(state):
    mw.col.conf['browser_checkbox_conf']['card_check_checked'] = state


def onSetupMenus(self):
    '''Toggle state via key bindings.'''
    self.a = QShortcut(QKeySequence("Alt+C"), self)
    self.connect(self.a, SIGNAL("activated()"), lambda c=self: c.form.cardToggleButton.toggle())
    self.a = QShortcut(QKeySequence("Alt+D"), self)
    self.connect(self.a, SIGNAL("activated()"), lambda c=self: c.form.deckToggleButton.toggle())


Ui_Dialog.setupUi = wrap(Ui_Dialog.setupUi, mySetupUi)
Browser.onSearch = wrap(Browser.onSearch, onSearch, "before")
addHook("browser.setupMenus", onSetupMenus)