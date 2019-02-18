# -*- coding: utf-8 -*-

# Context Menu Search Add-on for Anki
#
# Copyright (C) 2015-2019  Aristotelis P. <https//glutanimate.com/>
#           (C) 2015  Eddie Blundell <https://github.com/eddie>
#           (C) 2013  Steve AW <https://github.com/steveaw>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the accompanied license file.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# Any modifications to this file must keep this entire header intact.

"""
Adds context menu entries for searching the card browser and
various online search providers.

Based on 'OSX Dictionary Lookup' by Eddie Blundell
and 'Search Google Images' by Steve AW.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import aqt
from aqt.qt import *
from aqt.utils import openLink
from anki.hooks import addHook

from .config import config

# Local search

def lookupLocal(text):
    browser = aqt.dialogs.open("Browser", aqt.mw)
    browser.form.searchEdit.lineEdit().setText('"{}"'.format(text))
    if ANKI20:
        browser.onSearch()
    else:
        browser.onSearchActivated()

# Online search

def lookupOnline(text, idx):
    text = " ".join(text.strip().split())
    for url in SEARCH_PROVIDERS[idx][1]:
        # opt for using custom formatter to avoid errors with user URLs:
        url = url.replace("%s", "text")
        openLink(url)


# Context menu

def addToContextMenu(view, menu):
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

# Hooks / patches

addHook("AnkiWebView.contextMenuEvent", addToContextMenu)
addHook("EditorWebView.contextMenuEvent", addToContextMenu)
