# -*- coding: utf-8 -*-

"""
Anki Add-on: Overview Browser Shortcuts

Specify hotkeys that allow you to go directly from the deck overview
to a specific search in the card browser (e.g. cards added today)

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

menu_items = {
    'Shift+T': {'search': 'added:1', 'label': _('Added Today')},
    'Shift+D': {'search': 'deck:current', 'label': _('Current Deck')},
}

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
import aqt
from aqt import mw
from anki.lang import ngettext

def openBrowserWithSearch(mw, search):
    browser = aqt.dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(search)
    browser.onSearch()

go_menu = QMenu(_("&Go"))
action = mw.menuBar().insertMenu(mw.form.menuTools.menuAction(), go_menu)

for key_sequence, binding in menu_items.iteritems():
    search = binding["search"]
    label = binding["label"]
    a = go_menu.addAction(label)
    a.setShortcut(QKeySequence(key_sequence))
    a.connect(a, SIGNAL("triggered()"), lambda c=search: openBrowserWithSearch(mw, c))
