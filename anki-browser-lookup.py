# coding: utf-8

"""
Anki Add-on: Context Menu Search

Adds context menu entries for searching the card browser and
various online search providers.

You can customize the menu entries for online providers by
editing the SEARCH_PROVIDERS list below.

Based on 'OSX Dictionary Lookup' by Eddie Blundell and 
'Search Google Images' by Steve AW.

Copyright: (c) Glutanimate 2015-2017

License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

"""
Simple addon to quickly look up words in Anki's Browser

Copyright: Glutanimate 2015-2017 (https://github.com/Glutanimate)
Based on 'OSX Dictionary Lookup' by Eddie Blundell <eblundell@gmail.com>:
https://gist.github.com/eddie/ff3d820fb267ae26ca0e

License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

### USER CONFIGURATION START

# list of tuples of search provider names and urls.
# '%s' will be replaced with the search term
SEARCH_PROVIDERS = [
    ("Google", u"https://www.google.com/search?&q=%s"),
    ("Google Images", u"https://www.google.de/search?&tbm=isch&q=%s"),
    ("Wikipedia (en)", u"https://en.wikipedia.org/w/index.php?search=%s"),
    ("Wikipedia (de)", u"https://de.wikipedia.org/w/index.php?search=%s")
]

### USER CONFIGURATION END

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
    openLink(SEARCH_PROVIDERS[idx][1] % text)    

def add_lookup_action(view, menu):
    """Add 'lookup' action to context menu"""
    selected = view.page().selectedText()
    if not selected:
        return
    suffix = (selected[:20] + '..') if len(selected) > 20 else selected
    label = u'Search for "%s" in the Browser' % suffix
    action = menu.addAction(label)
    action.connect(action, SIGNAL('triggered()'),
        lambda t=selected: lookup_browser(t))
    search_menu = menu.addMenu(u'Search for "%s" with...' % suffix)
    for idx, provider in enumerate(SEARCH_PROVIDERS):
        a = search_menu.addAction(provider[0])
        a.connect(a, SIGNAL('triggered()'), 
            lambda i=idx,t=selected: lookup_online(t, i))

addHook("AnkiWebView.contextMenuEvent", add_lookup_action)
addHook("EditorWebView.contextMenuEvent", add_lookup_action)
