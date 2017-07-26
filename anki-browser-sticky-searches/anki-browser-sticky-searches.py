# -*- coding: utf-8 -*-

"""
Anki Add-on: Sticky Searches

Adds a number of quick-toggles to the Browser search bar that allow
you to preserve specific search parameters across multiple searches,
so that you do not have to type them in repeatedly.

These are either predefined, or dynamically extracted from
the current search.

By default the add-on comes with four toggles:

Static:

- Deck (Hotkey: Alt+D): Limit results to current deck
- Card (Hotkey: Alt+C): Limit results to first card of each note

Dynamic

- Sticky (Hotkey: Alt+S): Will remember the entirety of the current query
- Tags (Hotkey: Alt+T): Limit results to current tag selection

Advanced users can customize these toggles and set up additional ones
by modifying the configuration section below.

Inspired by the following add-ons:

- "Limit searches to current deck" by Damien Elmes
   (https://github.com/dae/ankiplugins/blob/master/searchdeck.py)
- "Ignore accents in browser search" by Houssam Salem
   (https://github.com/hssm/anki-addons)

This add-on was originally known as "Browser Search Modifiers", but has
since been reworked from the ground up with the kind support of a
fellow Anki user.

Copyright: Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPL, version 3 or later; https://www.gnu.org/licenses/agpl-3.0.en.html
"""

# Do not modify the following line
from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# CHECKBOX SETTINGS

# You can set-up additional checkboxes here if you know what you are doing
#
# - checkboxes with an empty "value" entry ("value": None) set their sticky
#   search tokens dynamically, i.e. by parsing the current query for the supplied
#   prefix (e.g. "tag:") and saving all values of that particular prefix
#
# Example of an additional entry for a dynamic "is" checkbox:
#
# "is": {
#     "hotkey": "Alt+I",
#     "label": "I",
#     "icons": "dot",
#     "tooltip": "Limit results to current 'is' state", 
#     "prefix": "is:",
#     "value": None
# },
# Example of an additional entry for a static deck checkbox:
#
# "mydeck": {
#     "hotkey": "Alt+M",
#     "label": "My deck",
#     "icons": "deck",
#     "tooltip": "Limit results to my deck", 
#     "prefix": "deck:",
#     "value": "'my deck'"
# },
checkboxes = {
    "sticky": {
        "hotkey": "Alt+S", # Default: Alt+S
        "icons": "snowflake",
        "tooltip": "Sticky current search", 
        "prefix": None,
        "value": None
    },
    "deck": {
        "hotkey": "Alt+D", # Default: Alt+D
        "icons": "deck",
        "tooltip": "Limit results to current deck", 
        "prefix": "deck:",
        "value": "current"
    },
    "tags": {
        "hotkey": "Alt+T", # Default: Alt+T
        "icons": "tag",
        "tooltip": "Limit results to current tag selection", 
        "prefix": "tag:",
        "value": None
    },
    "card": {
        "hotkey": "Alt+C", # Default: Alt+C
        "icons": "card",
        "tooltip": "Limit results to first card of each note", 
        "prefix": "card:",
        "value": "1"
    },
}

# ENABLED CHECKBOXES

# - any additional checkboxes you set up have to be added to this list
# - all checkboxes will be arranged according to the order of this list
# - entries you remove here will stop being displayed
enabled = ("sticky", "deck", "tags", "card")

# OPTIONS

# whether empty queries should clear all sticky parameters
EMPTY_CLEAR = True # Default: True

##############  USER CONFIGURATION END  ##############

from aqt.qt import *

from aqt import mw
from aqt.browser import Browser
from anki.hooks import wrap

##############  VARIABLES START  ##############

# Disable sticky tokens for the following searches:
empty_queries = (
    _("<type here to search; hit enter to show current deck>"),
    "is:current"
)

# Default preferences dictionary
default_prefs = {
    "state": {},
    "last": {},
}

# Checkbox styling
icon_path = os.path.join(mw.pm.addonFolder(), "sticky_searches")

def image2url(name):
    path = os.path.join(icon_path, "{}.png".format(name))
    qurl = QUrl.fromLocalFile(path).toString()
    return qurl.replace("file://", "")

iconsets = {
    "snowflake": (
        image2url("sticky"),
        image2url("unsticky"),
    ),
    "dot": (
        image2url("active"),
        image2url("inactive"),
    ),
    "tag": (
        image2url("tag_active"),
        image2url("tag_inactive"),
    ),
    "deck": (
        image2url("deck_active"),
        image2url("deck_inactive"),
    ),
    "card": (
        image2url("card_active"),
        image2url("card_inactive"),
    ),
}

cb_stylesheet = """
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
}}
QCheckBox::indicator:checked {{
    image: url({0});
}}
QCheckBox::indicator:unchecked {{
    image: url({1});
}}
QCheckBox::indicator:checked:hover {{
    image: url({0});
}}
QCheckBox::indicator:unchecked:hover {{
    image: url({1});
}}
QCheckBox::indicator:checked:pressed {{
    image: url({0});
}}
QCheckBox::indicator:unchecked:pressed {{
    image: url({1});
}}
QCheckBox::indicator:checked:disabled {{
    image: url({0});
}}
QCheckBox::indicator:unchecked:disabled {{
    image: url({0});
}}
"""
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
            elif token:
                # quotes are allowed to start directly after a :
                inQuote = c
            else:
                inQuote = c
            token += c
        # separator (space and ideographic space)
        elif c in (" ", u'\u3000'):
            if inQuote:
                token += c
            elif token:
                # space marks token finished
                tokens.append(token)
                token = ""
        # nesting - modified not to tokenize inside bracket
        elif c in ("(", ")"):
            if inQuote:
                if c == inQuote:
                    inQuote = False
            elif token:
                # brackets are allowed to start directly after a " "
                if token[-1] in (" ", u'\u3000'):
                    inQuote = c
            else:
                inQuote = ")"
            token += c
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


def sortTokens(s):
    """Custom sort function to override token order"""
    if s.startswith("deck:"):
        return 1
    elif s.startswith("tag:"):
        return 2
    elif s.startswith("is:"):
        return 3
    elif s.startswith("card:"):
        return 4
    else:
        return s


def onSearch(self, _old=None, reset=True):
    """Intercept search and modify query with our tokens"""
    query = unicode(self.form.searchEdit.lineEdit().text()).strip()
    sticky = self.cbPrefs["last"].get("sticky", "")
    cb_state = self.cbPrefs["state"]

    # empty query or all checkboxes inactive
    if (query in empty_queries or (EMPTY_CLEAR and query == "")
            or not any(i for i in cb_state.values()) ):
        return _old(self, reset)
    
    # prepare query
    if sticky:
        query = query.replace(sticky, "")
    
    # apply tokens and sticky prefix to query
    cur_tokens = tokenize(query)
    new_tokens = uniqueList(self.cbTokens + cur_tokens)
    new_query = " ".join([sticky] + new_tokens)
    
    self.form.searchEdit.lineEdit().setText(new_query)

    return _old(self, reset)


def onCbStateChanged(self, state, key):
    """Update persistent search tokens and search bar"""

    if state == Qt.Checked:
        mode = "add"
    else:
        mode = "remove"

    # Tokenize search and get existing sticky tokens
    query = self.form.searchEdit.lineEdit().text().strip()
    cb_tokens = self.cbTokens
    sticky = self.cbPrefs["last"].get("sticky", "")
    
    if query not in empty_queries or (EMPTY_CLEAR and query != ""):
        query_tokens = tokenize(query)
    else:
        query_tokens = []
    uniq_tokens = list(set(query_tokens) - set(cb_tokens))
    
    # Update tokens and sticky prefix
    prefix = checkboxes[key].get("prefix", None)
    value = checkboxes[key].get("value", None)
    if value:
        # static checkbox
        token = prefix + value
        if mode == "add" and token not in cb_tokens:
            cb_tokens.append(token)
        elif mode == "remove" and token in cb_tokens:
            cb_tokens.remove(token)
    elif prefix:
        # dynamic checkbox
        prefixes = (prefix, "-" + prefix)
        if mode == "add":
            to_add = [t for t in query_tokens if t.startswith(prefixes)]
            if to_add:
                self.cbPrefs["last"][key] = to_add
            else:
                to_add = self.cbPrefs["last"].get(key, None)
            if to_add:
                cb_tokens = list(set(cb_tokens + to_add))
        elif mode == "remove":
            cb_tokens = [t for t in cb_tokens if not t.startswith(prefixes)]
    elif key == "sticky":
        # sticky search toggle
        if mode == "add":
            sticky = query
            for token in cb_tokens:
                sticky.replace(token, "")
            query = query.replace(sticky, "")
        else:
            query = query.replace(sticky, "")
            sticky = ""
    else:
        # should not happen
        return False

    # Save tokens or sticky prefix and update search bar
    if key != "sticky": 
        if query_tokens:
            new_query_tokens = uniqueList(cb_tokens + uniq_tokens)
            self.form.searchEdit.lineEdit().setText(" ".join(new_query_tokens))
        self.cbTokens = sorted(cb_tokens, key=sortTokens)
    else:
        self.form.searchEdit.lineEdit().setText(sticky + " " + query)
        self.cbPrefs["last"]["sticky"] = sticky

    # Save checkbox state and reset
    self.cbPrefs["state"][key] = state
    self.onReset()

    # DEBUG
    print("{} is {}. New tokens:[{}]. New sticky: {}".format(
        key, state, ", ".join(cb_tokens), sticky))


def onSetupSearch(self):
    """Add new items to the browser UI to allow toggling the add-on."""
    
    layout = self.form.gridLayout
    widget = self.form.widget

    prefs = mw.pm.profile.get("browserCbs", None)
    if not prefs:
        prefs = default_prefs
    for key in default_prefs:
        if key not in prefs:
            prefs[key] = default_prefs[key]

    # Create check buttons and hotkeys
    idx = 1
    new_btns = []
    tokens = []
    
    for key in enabled:
        cb = checkboxes[key]

        # Set up tokens
        state = prefs["state"].get(key, None)
        if not state:
            state = prefs["state"]["key"] = Qt.Unchecked
        prefix = cb["prefix"]
        value = cb["value"]
        if state:
            if prefix and value:
                token = prefix + value
                tokens.append(token)
            elif prefix:
                last = prefs["last"].get(key, None)
                if last:
                    tokens += last
        
        # Set up buttons and hotkeys
        hotkey = cb["hotkey"]
        if not hotkey: # disable checkbutton
            continue
        label = cb.get("label", "")
        tooltip = cb.get("tooltip", "")
        icons = cb.get("icons", None)
        
        b = QCheckBox(label, widget)
        b.setToolTip(tooltip)
        b.setFocusPolicy(Qt.NoFocus)
        
        if icons:
            iconset = iconsets[icons]
            stylesheet = cb_stylesheet.format(*iconset)
            b.setStyleSheet(stylesheet)

        b.setCheckState(state)
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

    self.cbPrefs = prefs
    self.cbTokens = tokens


def onCloseEvent(self, evt):
    """Save configuration on Browser exit"""
    mw.pm.profile["browserCbs"] = self.cbPrefs


Browser.onCbStateChanged = onCbStateChanged
Browser.setupSearch = wrap(Browser.setupSearch, onSetupSearch, "after")
Browser.closeEvent = wrap(Browser.closeEvent, onCloseEvent, "before")
Browser.onSearch = wrap(Browser.onSearch, onSearch, "around")
