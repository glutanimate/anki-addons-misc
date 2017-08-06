# -*- coding: utf-8 -*-

"""
Anki Add-on: Search Through Cards with Ctrl+F

Allows you to search through your cards in the Reviewer.

Hotkeys:

- Invoke search: CTRL + F
- Close search: Esc
- Next result: F3
- Previous result: Shift+F3

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

HOTKEY_SEARCH = "Ctrl+F"
HOTKEY_NEXT = "F3"
HOTKEY_PREVIOUS = "Shift+F3"

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt import mw

# Hooks

class SearchDockWidget(QObject):
    def __init__(self, mw):
        QObject.__init__(self)
        self.mw = mw
        self.dock = None
        self.shown = False
        self.widget = None

    def setupWidget(self):
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        w.searchEdit = QLineEdit()
        w.searchNxt = QPushButton("∨")
        w.searchPrv = QPushButton("∧")
        for i in (w.searchEdit, w.searchNxt, w.searchPrv):
            l.addWidget(i)
        return w

    def setupDock(self):
        dock = QDockWidget("", mw)
        dock.setObjectName("SearchDock")
        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetClosable)
        dock.setTitleBarWidget(QWidget(dock))
        return dock

    def setupEvents(self):
        self.widget.searchNxt.clicked.connect(
            lambda _: self.findText(0))
        self.widget.searchPrv.clicked.connect(
            lambda _: self.findText(1))
        t = QShortcut(QKeySequence("Esc"), self.dock)
        t.activated.connect(self.hide)
        t = QShortcut(QKeySequence(HOTKEY_NEXT), mw)
        t.activated.connect(self.widget.searchNxt.animateClick)
        t = QShortcut(QKeySequence("Return"), self.dock)
        t.activated.connect(self.widget.searchNxt.animateClick)
        t = QShortcut(QKeySequence(HOTKEY_PREVIOUS), mw)
        t.activated.connect(self.widget.searchPrv.animateClick)
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.findText(0))
        self.widget.searchEdit.textEdited.connect(lambda: self.timer.start())

    def showOrFocus(self):
        if not self.shown:
            self.show()
        else:
            self.widget.searchEdit.setFocus()
            self.widget.searchEdit.selectAll()

    def show(self):
        if not self.dock:
            self.dock = self.setupDock()
            self.widget = self.setupWidget()
            self.dock.setWidget(self.widget)
            self.setupEvents()
            mw.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        self.dock.show()
        self.widget.searchEdit.setFocus()
        self.widget.searchEdit.selectAll()
        self.shown = True

    def hide(self):
        if self.dock:
            self.dock.hide()
            self.shown = False

    def toggle(self):
        if self.shown:
            self.hide()
        else:
            self.show()

    def findText(self, direction):
        web = mw.web
        text = self.widget.searchEdit.text()
        options = QWebPage.FindWrapsAroundDocument 
        if direction == 1:
            options = (options | QWebPage.FindBackward)
        web.findText(text, options)


dock = SearchDockWidget(mw)

shortcut = QShortcut(QKeySequence(HOTKEY_SEARCH), mw)
shortcut.activated.connect(dock.showOrFocus)
