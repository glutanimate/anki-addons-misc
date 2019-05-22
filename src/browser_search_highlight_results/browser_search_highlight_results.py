# -*- coding: utf-8 -*-

"""
Anki Add-on: Highlight Search Results in Browser

Highlights search results in Editor pane of the Browser and adds two
new shortcuts when searching:

- Shift-Return: Jump to result in current list
- Ctrl-Shift-Return: Select results in current list

Search result highlighting may be turned off via the provided View
menu entry, or its associated hotkey (Ctrl+T, H).

Limitations: Searches through entire editor screen,
             field descriptions included

Copyright (C)  2017-2019 Aristotelis P. <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

HIGHLIGHT_BY_DEFAULT = True
HOTKEY_HIGHLIGHT_TOGGLE = "Ctrl+T, H"

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt.browser import Browser
from anki.hooks import wrap, addHook
from anki.find import Finder

from anki import version as anki_version
ANKI20 = anki_version.startswith("2.0")

if ANKI20:
    find_flags = QWebPage.HighlightAllOccurrences
else:
    import unicodedata
    unicode = str
    find_flags = QWebEnginePage.FindFlags(0)


# ignore search token specifiers, search operators, and wildcard characters
excluded_tags = ("deck:", "tag:", "card:", "note:", "is:", "prop:", "added:",
                 "rated:", "nid:", "cid:", "mid:", "seen:")
excluded_vals = ("*", "_", "_*")
operators = ("or", "and", "+")


def onRowChanged(self, current, previous):
    """
    Highlight search results in Editor pane on searching
    """
    if not self._highlightResults:
        return
    txt = unicode(self.form.searchEdit.lineEdit().text())
    if not ANKI20:
        txt = unicodedata.normalize("NFC", txt)
    if not txt:
        return
    tokens = Finder(self.col)._tokenize(txt)
    print("tokens", tokens)
    vals = []
    for token in tokens:
        if (token in operators or token.startswith("-") or
                token.startswith(excluded_tags)):
            continue
        if ":" in token:
            val = "".join(token.split(":")[1:])
            if not val or val in excluded_vals:
                continue
        else:
            val = token
        val = val.strip('''",*;''')
        vals.append(val)
    if not vals:
        return
    print("vals", vals)
    for val in vals:
        self.editor.web.findText(val, find_flags)


def onCustomSearch(self, onecard=False):
    """Extended search functions"""
    txt = self.form.searchEdit.lineEdit().text().strip()
    cids = self.col.findCards(txt, order=True)

    if onecard:
        # jump to next card, while wrapping around at the end
        if self.card:
            cur = self.card.id
        else:
            cur = None

        if cur and cur in cids:
            idx = cids.index(cur) + 1
        else:
            idx = None

        if not idx or idx >= len(cids):
            idx = 0
        cids = cids[idx:idx+1]

    self.form.tableView.selectionModel().clear()
    self.model.selectedCards = {cid: True for cid in cids}
    self.model.restoreSelection()


def toggleSearchHighlights(self, checked):
    """Toggle search highlights on or off"""
    self._highlightResults = checked
    if not checked:
        # clear highlights
        self.editor.web.findText("", find_flags)
    else:
        onRowChanged(self, None, None)


def onSetupSearch(self):
    """Add extended search hotkeys"""
    s = QShortcut(QKeySequence(_("Shift+Return")), self.form.searchEdit)
    s.activated.connect(lambda: self.onCustomSearch(True))
    s = QShortcut(QKeySequence(_("Ctrl+Return")), self.form.searchEdit)
    s.activated.connect(self.onCustomSearch)


def onSetupMenus(self):
    """Setup menu entries and hotkeys"""
    self._highlightResults = HIGHLIGHT_BY_DEFAULT
    try:
        # used by multiple add-ons, so we check for its existence first
        menu = self.menuView
    except:
        self.menuView = QMenu(_("&View"))
        self.menuBar().insertMenu(
            self.mw.form.menuTools.menuAction(), self.menuView)
        menu = self.menuView
    menu.addSeparator()
    a = menu.addAction('Highlight Search Results')
    a.setCheckable(True)
    a.setChecked(HIGHLIGHT_BY_DEFAULT)
    a.setShortcut(QKeySequence(HOTKEY_HIGHLIGHT_TOGGLE))
    a.toggled.connect(self.toggleSearchHighlights)


if ANKI20:
    Browser.onRowChanged = wrap(Browser.onRowChanged, onRowChanged, "after")
else:
    Browser._onRowChanged = wrap(Browser._onRowChanged, onRowChanged, "after")

addHook("browser.setupMenus", onSetupMenus)
Browser.onCustomSearch = onCustomSearch
Browser.toggleSearchHighlights = toggleSearchHighlights
Browser.setupSearch = wrap(Browser.setupSearch, onSetupSearch, "after")
