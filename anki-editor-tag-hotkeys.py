# -*- coding: utf-8 -*-

"""
Anki Add-on: Editor Tag Hotkeys

Extends Anki's note editor with hotkeys that toggle specific tags.

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
""" 

from __future__ import unicode_literals

################## USER CONFIGURATION START #####################

# Dictionary of hotkey assignments to tags
tags = {
    "Alt+Shift+1": u"tag1",
    "Alt+Shift+2": u"tag2",
    "Alt+Shift+3": u"tag3",
    "Alt+Shift+4": u"tag4",
    "Alt+Shift+5": u"tag5",
    "Alt+Shift+6": u"tag6",
    "Alt+Shift+7": u"tag7",
    "Alt+Shift+8": u"tag8",
    "Alt+Shift+9": u"tag9",
}
# syntax: {"Hotkey": u"tag1", "Hotkey": u"tag2"}

# List of tags that can only be set one at a time:
unique_tags = ["tag7", "tag8", "tag9"]
# syntax: ["tag1", "tag2"]
#
# (toggling the hotkey for any of these will delete any
# other unique tag found in the current tags)

################## USER CONFIGURATION End #####################

from aqt.qt import *

from aqt.editor import Editor
from anki.hooks import addHook

def toggleTag(self, tag):
    current = self.tags.text().split()
    if tag in current:
        current.remove(tag)
    else:
        current.append(tag)
    if tag in unique_tags:
        intersectedTags = [val for val in unique_tags if val in current]
        if tag in intersectedTags:
            intersectedTags.remove(tag)
        for tag in intersectedTags:
            current.remove(tag)
    self.tags.setText(" ".join(current))
    self.saveTags()

def resetTags(self):
    self.tags.clear()

def onSetupButtons(self):
    s = QShortcut(QKeySequence("Alt+Shift+R"), self.parentWindow)
    s.activated.connect(self.resetTags)

    for hotkey, tag in tags.items():
        s = QShortcut(QKeySequence(hotkey), self.parentWindow)
        s.activated.connect(lambda t=tag: self.toggleTag(t))


addHook("setupEditorButtons", onSetupButtons)
Editor.resetTags = resetTags
Editor.toggleTag = toggleTag