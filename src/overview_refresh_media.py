# -*- coding: utf-8 -*-

"""
Anki Add-on: Refresh Media References

Adds an entry in the Tools menu that clears the webview cache.
This will effectively refresh all media files used by your cards
and templates, allowing you to display changes to external files
without having to restart Anki.

The add-on will also update the modification time of your media
collection which will force an upload of any updated files
on the next synchronization with AnkiWeb.

Note: Might lead to increased memory consumption if used excessively

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

import os

from aqt import mw
from aqt.utils import tooltip
from aqt.qt import *

def refresh_media():
    # clear QWebView cache
    QWebSettings.clearMemoryCaches()
    # write a dummy file to update collection.media modtime and force sync
    media_dir = mw.col.media.dir()
    fpath = os.path.join(media_dir, "syncdummy.txt")
    if not os.path.isfile(fpath):
        with open(fpath, "w") as f:
            f.write("anki sync dummy")
    os.remove(fpath)
    # reset Anki
    mw.reset()
    tooltip("Media References Updated")

# Set up menus and hooks
refresh_media_action = QAction("Refresh &Media", mw)
refresh_media_action.setShortcut(QKeySequence("Ctrl+Alt+M"))
refresh_media_action.triggered.connect(refresh_media)
mw.form.menuTools.addAction(refresh_media_action)