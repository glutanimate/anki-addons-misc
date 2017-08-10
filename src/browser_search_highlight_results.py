# -*- coding: utf-8 -*-

"""
Anki Add-on: Highlight Search Results in Browser

Highlights search results in editor pane of the Browser and adds two
new shortcuts when searching:

- Shift-Return: Jump to result in current list 
- Ctrl-Shift-Return: Select results in current list

Limitations: Searches through entire editor screen,
             field descriptions included

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

from aqt.qt import *
from aqt.browser import Browser
from anki.hooks import wrap

excluded_tags = ("deck:", "tag:", "card:", "note:", "is:", "prop:", "added:",
                "rated:", "nid:", "cid:", "mid:", "seen:")
excluded_vals = ("*", "_", "_*")
operators = ("or", "and", "+")


def onRowChanged(self, current, previous):
    """
    Highlight search results in Editor pane on searching
    """
    txt = self.form.searchEdit.lineEdit().text().strip()
    if not txt:
        return
    tokens = txt.split()
    vals = []
    for token in tokens:
        if (token in operators or token.startswith("-") 
                or token.startswith(excluded_tags)):
            continue
        if ":" in token:
            frags = token.split(":")
            tag = frags[0]
            val = "".join(frags[1:])
            if not val or val in excluded_vals:
                continue
        else:
            val = token
        val = val.strip('''",*;''')
        vals.append(val)
    if not vals:
        return
    for val in vals:
        self.editor.web.findText(val, QWebPage.HighlightAllOccurrences)    


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


def onSetupSearch(self):
    """Add extended search hotkeys"""
    s = QShortcut(QKeySequence(_("Shift+Return")), self.form.searchEdit)
    s.activated.connect(lambda: self.onCustomSearch(True))
    s = QShortcut(QKeySequence(_("Ctrl+Return")), self.form.searchEdit)
    s.activated.connect(self.onCustomSearch)


Browser.onCustomSearch = onCustomSearch
Browser.onRowChanged = wrap(Browser.onRowChanged, onRowChanged, "after")
Browser.setupSearch = wrap(Browser.setupSearch, onSetupSearch, "after")