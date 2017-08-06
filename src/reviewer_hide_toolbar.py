# -*- coding: utf-8 -*-
"""
Hides the main window's toolbar when reviewing.

The aim of the addon is to free up some vertical screen space while reviewing
cards. For me this is useful as I have many cards that contain diagrams which can
be fairly large. In addition. modern wide screen displays seem to feel more
cramped vertically than horizontally.

The toolbar is made visible again when viewing decks and the overview.

The commands that are usually found on the toolbar are added to a new
main window "Toolbar" menu. Shortcut keys should continue to function

Copyright: Steve AW <steveawa@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Support: Use at your own risk. If you do find a problem please email me
or use one the following forums, however there are certain periods
throughout the year when I will not have time to do any work on
these addons.

Github page:  https://github.com/steveaw/anki_addons
Anki addons: https://groups.google.com/forum/?hl=en#!forum/anki-addons
"""
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QMenu
from anki.hooks import wrap
from aqt import mw
from aqt.main import AnkiQt

__author__ = 'Steve'


def hide_toolbar_reviewing(self, oldState):
    self.toolbar.web.hide()


def show_toolbar_not_reviewing(self, state, *args):
    #Rather than tracking the state of the toolbar's visibility
    #leave it to Qt to handle. m
    self.toolbar.web.show()


AnkiQt._reviewState = wrap(AnkiQt._reviewState, hide_toolbar_reviewing, "after")
AnkiQt.moveToState = wrap(AnkiQt.moveToState, show_toolbar_not_reviewing, "before")

toolbar_menu = QMenu("Tool&bar")
action = mw.menuBar().insertMenu(mw.form.menuTools.menuAction(), toolbar_menu)
#Not really the intended purpose of link_handlers, but good enough
for key, value in iter(sorted(mw.toolbar.link_handlers.items())):
    a = toolbar_menu.addAction(_(key.title()))
    a.connect(a, SIGNAL("triggered()"), value)
