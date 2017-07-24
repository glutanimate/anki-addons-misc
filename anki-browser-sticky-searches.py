# -*- coding: utf-8 -*-

"""
Anki Add-on: Sticky Searches

Adds a configurable number of checkboxes to the browser search form that, 
when toggled, add sticky query parameters to your search.

By default the add-on comes with four checkboxes:

Deck (Hotkey: Alt+D): Limit results to current deck
Tags (Hotkey: Alt+T): Limit results to current tag selection
Card (Hotkey: Alt+C): Limit results to first card of each note
State (Hotkey: Alt+S): Limit results to current card state (disabled)

Advanced users can set up additional checkboxes by modifying the VARIABLES
section below.

Inspired by the following add-ons:

- "Limit searches to current deck" by Damien Elmes
   (https://github.com/dae/ankiplugins/blob/master/searchdeck.py)
- "Ignore accents in browser search" by Houssam Salem
   (https://github.com/hssm/anki-addons)

Original idea by Keven on Anki tenderapp

Copyright: Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

# Do not modify the following line
from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# HOTKEYS

# (set to "" to disable both the corresponding checkbox and hotkey)
DECK_TOGGLE_HOTKEY = "Alt+D" # Default: Alt+D
TAGS_TOGGLE_HOTKEY = "Alt+T" # Default: Alt+T
CARD_TOGGLE_HOTKEY = "Alt+C" # Default: Alt+C
STATE_TOGGLE_HOTKEY = "" # Deafult: "" (disabled)

# OPTIONS

# whether empty queries should clear all sticky parameters
EMPTY_CLEAR = True # Default: True

# Note: If you are familiar with Python and know what you are doing 
#       you can also modify the VARIABLES section below
#       for more advanced customization

##############  USER CONFIGURATION END  ##############

from aqt.qt import *

from aqt import *
from aqt.browser import Browser
from anki.hooks import wrap

##############  VARIABLES START  ##############

# You can set-up additional checkboxes here if you know what you are doing
# please do not use any of the following as dictionary keys: tokens, last
checkboxes = {
    "deck": {
        "hotkey": DECK_TOGGLE_HOTKEY,
        "label": "D",
        "tooltip": "Limit results to current deck", 
        "default": Qt.Unchecked,
        "prefix": "deck:",
        "value": "current"
    },
    "tags": {
        "hotkey": TAGS_TOGGLE_HOTKEY,
        "label": "T",
        "tooltip": "Limit results to current tag selection", 
        "default": Qt.Unchecked,
        "prefix": "tag:",
        "value": None
    },
    "state": {
        "hotkey": STATE_TOGGLE_HOTKEY,
        "label": "S",
        "tooltip": "Limit results to current card state", 
        "default": Qt.Unchecked,
        "prefix": "is:",
        "value": None
    },
    "card": {
        "hotkey": CARD_TOGGLE_HOTKEY,
        "label": "C",
        "tooltip": "Limit results to first card of each note", 
        "default": Qt.Unchecked,
        "prefix": "card:",
        "value": "1"
    },
}
# Any checkboxes you add will also have to be appended to the following tuple:
order = ("deck", "tags", "card", "state")

# Disable sticky tokens for the following searches:
empty_queries = (
    _("<type here to search; hit enter to show current deck>"),
    "is:current"
)

default_prefs = {key: checkboxes[key]["default"] for key in order}
# FIXME: more elegant implementation for 'tokens' and 'last' storage
default_prefs["tokens"] = []
default_prefs["last"] = {}

##############  VARIABLES END  ##############

def tokenize(query):
    """Tokenize search query, adapted from anki.find.Finder"""
    inQuote = False
    tokens = []
    token = ""
    for c in query:
        # quoted text
        if c in ("'", '"'):
            if inQuote:
                if c == inQuote:
                    inQuote = False
                else:
                    token += c
            elif token:
                # quotes are allowed to start directly after a :
                if token[-1] == ":":
                    inQuote = c
                else:
                    token += c
            else:
                inQuote = c
        # separator (space and ideographic space)
        elif c in (" ", u'\u3000'):
            if inQuote:
                token += c
            elif token:
                # space marks token finished
                tokens.append(token)
                token = ""
        # nesting
        elif c in ("(", ")"):
            if inQuote:
                token += c
            else:
                if c == ")" and token:
                    tokens.append(token)
                    token = ""
                tokens.append(c)
        # negation
        elif c == "-":
            if token:
                token += c
            elif not tokens or tokens[-1] != "-":
                tokens.append("-")
        # normal character
        else:
            token += c
    # if we finished in a token, add it
    if token:
        tokens.append(token)
    return tokens


def uniqueList(seq):
    """Returns unique list while preserving order"""
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def onSearch(self, reset=True):
    """Intercept search and modify query with our tokens"""
    
    query = unicode(self.form.searchEdit.lineEdit().text()).strip()
    if query in empty_queries or (EMPTY_CLEAR and query == ""):
        return
    cur_tokens = tokenize(query)
    new_tokens = uniqueList(self.cbState["tokens"] + cur_tokens)
    new_query = " ".join(new_tokens)
    self.form.searchEdit.lineEdit().setText(new_query)

    # # filter out conflicting tokens
    # for key, cb in checkboxes.items():
    #     prefix = cb["prefix"]
    #     if cb["value"]:
    #         term = prefix + cb["value"]
    #         if term in cur_tokens:
    #             cur_tokens.remove(term)
    #     if not self.cbState[key] or not cb.get("unique", False):
    #         continue
    #     dupes = cb.get("dupes", [])
    #     cur_tokens = [t for t in cur_tokens
    #                   if not t in dupes or t.startswith(prefix)]


def onCbStateChanged(self, state, key):
    """Update persistent search tokens and search bar"""

    # Tokenize search and get existing sticky tokens
    query = self.form.searchEdit.lineEdit().text().strip()
    cb_tokens = self.cbState["tokens"]
    if query not in empty_queries or (EMPTY_CLEAR and query != ""):
        query_tokens = tokenize(query)
    else:
        query_tokens = []
    uniq_tokens = list(set(query_tokens) - set(cb_tokens))
    
    if state == Qt.Checked:
        mode = "add"
    else:
        mode = "remove"

    # Update sticky tokens
    prefix = checkboxes[key].get("prefix", None)
    value = checkboxes[key].get("value", None)
    if value:
        token = prefix + value
        if mode == "add" and token not in cb_tokens:
            cb_tokens.append(token)
        elif mode == "remove" and token in cb_tokens:
            cb_tokens.remove(token)
    elif prefix:
        if mode == "add":  
            to_add = [t for t in query_tokens if t.startswith(prefix)]
            if to_add:
                self.cbState["last"][key] = to_add
            else:
                to_add = self.cbState["last"].get(key, [])
            cb_tokens = list(set(cb_tokens + to_add))
        elif mode == "remove":
            cb_tokens = [t for t in cb_tokens if not t.startswith(prefix)]
    else:
        return False

    # Update search bar
    if query_tokens:
        new_query_tokens = uniqueList(cb_tokens + uniq_tokens)
        self.form.searchEdit.lineEdit().setText(" ".join(new_query_tokens))

    # Save state and reset
    self.cbState[key] = state
    self.cbState["tokens"] = cb_tokens
    self.onReset()

    # DEBUG
    print("{} is {}. New sticky tokens: ".format(key, state))
    print(cb_tokens)



def onSetupSearch(self):
    """Add new items to the browser UI to allow toggling the add-on."""
    
    layout = self.form.gridLayout
    widget = self.form.widget

    prefs = mw.pm.profile.get("browserCbs", None)
    if not prefs:
        prefs = default_prefs
    self.cbState = prefs

    # Create check buttons and hotkeys
    idx = 1
    new_btns = []
    for key in order:
        cb = checkboxes[key]
        if not cb["hotkey"]: # disable checkbutton
            continue
        b = QCheckBox(cb["label"], widget)
        b.setToolTip(cb["tooltip"])
        b.setCheckState(prefs.get(key, Qt.Unchecked))
        b.stateChanged.connect(lambda a, k=key:self.onCbStateChanged(a, k))
        new_btns.append(b)
        s = QShortcut(QKeySequence(_(cb["hotkey"])), 
                self, activated=b.toggle)
        idx += 1

    # Add widgets to gridlayout while restructuring it
    items = []
    for i in range(0, layout.count()):
        item = layout.itemAt(i).widget()
        items.append(item)
        if item == self.form.searchEdit:
            # position our items ofter the search bar
            items += new_btns
    
    for i, item in enumerate(items):
        layout.addWidget(item, 0, i, 1, 1)


def onCloseEvent(self, evt):
    """Save configuration on Browser exit"""
    mw.pm.profile["browserCbs"] = self.cbState


Browser.setupSearch = wrap(Browser.setupSearch, onSetupSearch, "after")
Browser.closeEvent = wrap(Browser.closeEvent, onCloseEvent, "before")
Browser.onCbStateChanged = onCbStateChanged
Browser.onSearch = wrap(Browser.onSearch, onSearch, "before")
