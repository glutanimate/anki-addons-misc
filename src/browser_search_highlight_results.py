# -*- coding: utf-8 -*-

"""
Anki Add-on: Highlight Search Results in Browser

Highlights search results in editor pane of the Browser

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


Browser.onRowChanged = wrap(Browser.onRowChanged, onRowChanged, "after")