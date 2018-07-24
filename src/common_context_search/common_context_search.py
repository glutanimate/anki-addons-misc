# coding: utf-8

"""
Anki Add-on: Context Menu Search

Adds context menu entries for searching the card browser and
various online search providers.

You can customize the menu entries for online providers by
editing the SEARCH_PROVIDERS list below.

Based on 'OSX Dictionary Lookup' by Eddie Blundell and 
'Search Google Images' by Steve AW.

Copyright: Glutanimate 2015-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# list of tuples of search provider names and urls.
# '%s' will be replaced with the search term
SEARCH_PROVIDERS = [
    ("&Google (with Image))", [u"https://www.google.com/search?&q=%s",
                               u"https://www.google.com/search?&tbm=isch&q=%s")
                              ],
    ("&Wikipedia (en)", [u"https://en.wikipedia.org/w/index.php?search=%s")],
    ("Wikipedia (&de)", [u"https://de.wikipedia.org/w/index.php?search=%s"])
]

# (Advanced) Use custom context menu style sheet, somewhat buggy
USE_CUSTOM_STYLESHEET = False 

##############  USER CONFIGURATION END  ##############

stylesheet = """
QMenu::item {
    padding-top: 15px;
    padding-bottom: 15px;
    padding-right: 10px;
    padding-left: 10px;
}
QMenu::item:selected {
    color: black;
    background-color: #D9CD6D;
}
"""

import urllib

import aqt
from aqt.qt import *
from aqt.utils import openLink
from anki.hooks import addHook

def lookup_browser(text):
    browser = aqt.dialogs.open("Browser", aqt.mw)
    query = '"' + text + '"'
    browser.form.searchEdit.lineEdit().setText(query)
    browser.onSearch()

def lookup_online(text, idx):
    text = " ".join(text.split())
    for url in SEARCH_PROVIDERS[idx][1]:
        openLink(url % text)    

def add_lookup_action(view, menu):
    """Add 'lookup' action to context menu"""
    if USE_CUSTOM_STYLESHEET:
        menu.setStyleSheet(stylesheet)
    selected = view.page().selectedText()
    if not selected:
        return
    
    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = u'Search for "%s" in Card &Browser' % suffix
    menu.addSeparator()
    a = menu.addAction(label)
    a.triggered.connect(lambda _, t=selected: lookup_browser(t))

    search_menu = None
    if len(SEARCH_PROVIDERS) > 10:  
        search_menu = menu.addMenu(u'&Search for "%s" with...' % suffix)

    for idx, provider in enumerate(SEARCH_PROVIDERS):
        if search_menu:
            label = provider[0]
            menu = search_menu
        else:
            label = u'Search for "%s" on %s' % (suffix, provider[0])
        a = menu.addAction(label)
        a.triggered.connect(lambda _, i=idx,t=selected: lookup_online(t, i))

addHook("AnkiWebView.contextMenuEvent", add_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_lookup_action)
