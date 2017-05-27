# -*- coding: utf-8 -*-

"""
Anki Add-on: Customize Editor CSS

Allows you to customize the stylesheet of the Editor widget in Anki.

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

import os

from aqt import mw
from aqt import editor

from anki.hooks import addHook

def profileLoaded():
    media_dir = mw.col.media.dir()
    css_path = os.path.join(media_dir, "_editor.css")
    if not os.path.isfile(css_path):
        return False
    with open(css_path, "r") as css_file:
        css = css_file.read()
    if not css:
        return False
    editor_style = "<style>\n{}\n</style>".format(css)
    editor._html = editor._html + editor_style

addHook("profileLoaded", profileLoaded)