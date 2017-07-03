# -*- coding: utf-8 -*-

"""
Anki Add-on: Customize Editor CSS

Allows you to customize the stylesheet of the Editor widget in Anki.

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

######### USER CONFIGURATION START ##########

TAGS_BACKGROUND = "#F5F6CE"
DISABLE_FOR_NIGHTMODE = True

######### USER CONFIGURATION END ##########

import os

from aqt import mw
from aqt import editor

from anki.hooks import addHook, wrap

old_html = editor._html
new_html = old_html

def updateTagsBackground(self):
    """Modify tagEdit background color"""
    if DISABLE_FOR_NIGHTMODE:
        try:
            from Night_Mode import nm_state_on
            if nm_state_on:
                return
        except ImportError:
            pass

    self.tags.setStyleSheet(
        """QLineEdit {{ background: {}; }}""".format(
            TAGS_BACKGROUND))

def profileLoaded():
    """Import modified CSS code into editor"""
    global old_html
    global new_html
    media_dir = mw.col.media.dir()
    css_path = os.path.join(media_dir, "_editor.css")
    if not os.path.isfile(css_path):
        return False
    with open(css_path, "r") as css_file:
        css = css_file.read()
    if not css:
        return False
    editor_style = "<style>\n{}\n</style>".format(css)
    old_html = editor._html
    editor._html = editor._html + editor_style
    new_html = editor._html

def onSetNote(self, *args, **kwargs):
    if DISABLE_FOR_NIGHTMODE:
        try:
            from Night_Mode import nm_state_on
            if nm_state_on:
                editor._html = old_html
            else:
                editor._html = new_html
        except ImportError:
            pass


addHook("profileLoaded", profileLoaded)

editor.Editor.setNote = wrap(editor.Editor.setNote, onSetNote, "before")
editor.Editor.setupTags = wrap(editor.Editor.setupTags, 
                               updateTagsBackground, "after")