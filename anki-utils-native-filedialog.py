# -*- coding: utf-8 -*-

"""
Workaround for using Nautilus file chooser instead of the default qt dialog
"""

from aqt.qt import *
import os
import aqt
from aqt.editor import Editor
from anki.hooks import wrap

def myGetFile(parent, title, cb, filter="*.*", dir=None, key=None):
    "Ask the user for a file."
    assert not dir or not key
    if not dir:
        dirkey = key+"Directory"
        dir = aqt.mw.pm.profile.get(dirkey, "")
    else:
        dirkey = None
    sel_file = QFileDialog.getOpenFileName(parent, title, dir, filter)
    if not os.path.isfile(sel_file):
        return None
    if dirkey:
        dir = os.path.dirname(sel_file)
        aqt.mw.pm.profile[dirkey] = dir
    if cb:
        cb(sel_file)
    return sel_file

def myAddMedia(self):
    key = (_("Media") +
               " (*.jpg *.png *.gif *.tiff *.svg *.tif *.jpeg "+
               "*.mp3 *.ogg *.wav *.avi *.ogv *.mpg *.mpeg *.mov *.mp4 " +
               "*.mkv *.ogx *.ogv *.oga *.flv *.swf *.flac)")
    def accept(file):
        self.addMedia(file, canDelete=True)
    file = myGetFile(self.widget, _("Add Media"), accept, key, key="media")
    self.parentWindow.activateWindow()

Editor.onAddMedia = myAddMedia