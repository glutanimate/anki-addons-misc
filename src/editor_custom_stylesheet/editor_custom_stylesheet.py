# -*- coding: utf-8 -*-

"""
Anki Add-on: Customize Editor CSS

Allows you to customize the stylesheet of the Editor widget in Anki.

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

######### USER CONFIGURATION START ##########

# Whether to style editor window by default
DEFAULT_STATE = True # default: True

# Set a custom tag field background color
# If this is set to an empty string no changes are applied
# (e.g. "#F5F6CE" or "")
TAGS_BACKGROUND = "" # default: ""

# Disable custom CSS adjustments when Night Mode add-on active
DISABLE_FOR_NIGHTMODE = True # default: True

######### USER CONFIGURATION END ##########

import os

from aqt.qt import *
from aqt import mw
from aqt import editor

from anki.hooks import addHook, wrap

old_html = editor._html
new_html = old_html

def updateTagsBackground(self):
    """Modify tagEdit background color"""
    nm_state_on = False
    if DISABLE_FOR_NIGHTMODE:
        try:
            from Night_Mode import nm_state_on
        except ImportError:
            pass

    if not mw._styleEditor or nm_state_on:
        return

    if TAGS_BACKGROUND:
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
    editor_style = "<style>\n{}\n</style>".format(css.replace("%","%%"))
    old_html = editor._html
    editor._html = editor._html + editor_style
    new_html = editor._html


def onEditorInit(self, *args, **kwargs):
    """Apply modified Editor HTML"""
    nm_state_on = False
    if DISABLE_FOR_NIGHTMODE:
        try:
            from Night_Mode import nm_state_on
        except ImportError:
            pass
    if not mw._styleEditor or nm_state_on:
        editor._html = old_html
    else:
        editor._html = new_html


def onStylingToggle(checked):
    """Set mw variable that controls styling state"""
    mw._styleEditor = checked


# Menu toggle:

mw._styleEditor = DEFAULT_STATE
action = QAction(mw)
action.setText("Custom Editor Styling")
action.setCheckable(True)
action.setChecked(DEFAULT_STATE)
action.setShortcut(QKeySequence("Shift+E"))
mw.form.menuTools.addAction(action)
action.toggled.connect(onStylingToggle)

# Hooks:

addHook("profileLoaded", profileLoaded)

editor.Editor.__init__ = wrap(editor.Editor.__init__, onEditorInit, "after")
editor.Editor.setupTags = wrap(editor.Editor.setupTags, 
                               updateTagsBackground, "after")
