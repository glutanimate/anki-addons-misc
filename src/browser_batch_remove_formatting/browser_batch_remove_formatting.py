# -*- coding: utf-8 -*-
"""
Anki Add-on: Batch-Remove Field Formatting

Adds a menu entry to the card browser that removes specific
HTML tags from all fields in all selected notes.

The HTML tags to  be removed can be specified in the
user configuration section below this comment header.

Based on "Clear Field Formatting (HTML) in Bulk" by Felix Esch
(https://github.com/Araeos/ankiplugins)

Copyright: (c) Felix Esch 2016 <https://github.com/Araeos>
           (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

############## USER CONFIGURATION START ##############

STRIP_TAGS = ['b', 'i', 'u']  # list of html tags to remove

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt import mw
from aqt.utils import tooltip
from anki.hooks import addHook
from anki import version as anki_version

if anki_version.startswith("2.1"):
    from bs4 import BeautifulSoup
    ANKI21 = True
else:
    from BeautifulSoup import BeautifulSoup
    ANKI21 = False


def stripFormatting(fields):
    """
    Uses BeautifulSoup to remove STRIP_TAGS from each string in
    supplied list.

    Parameters
    ----------
    fields : list of strings
        list containing html of field contents
    Returns
    -------
    stripped_fields : list of strings
        processed list of fields
    """

    stripped_fields = []

    for html in fields:
        soup = BeautifulSoup(html, "html.parser")
        for tag in STRIP_TAGS:
            for match in soup.findAll(tag):
                match.replaceWithChildren()
        text = str(soup) if ANKI21 else unicode(soup)
        stripped_fields.append(text)

    return stripped_fields


def setupMenu(browser):
    """
    Add the button to the browser menu "edit".
    """
    a = browser.form.menuEdit.addAction('Batch-Remove Field Formatting')
    a.setShortcut(QKeySequence("Ctrl+Alt+Shift+R"))
    a.triggered.connect(lambda _, b=browser: onClearFormatting(b))


def onClearFormatting(browser):
    """
    Clears the formatting for every selected note.
    Also creates a restore point, allowing a single undo operation.

    Parameters
    ----------
    browser : Browser
        the anki browser from which the function is called
    """

    nids = browser.selectedNotes()
    if not nids:
        tooltip(_("No cards selected."), period=2000)
        return

    mw.checkpoint("Batch-Remove Field Formatting")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        note.fields = stripFormatting(note.fields)
        note.flush()
    mw.progress.finish()
    mw.reset()

# Hooks

addHook("browser.setupMenus", setupMenu)
