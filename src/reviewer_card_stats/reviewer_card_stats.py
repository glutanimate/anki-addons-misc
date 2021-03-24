# -*- coding: utf-8 -*-

"""
Anki Add-on: Card Stats

Displays stats in a sidebar while reviewing.

For the most part based on the following add-ons:

- Card Info During Review by Damien Elmes (https://ankiweb.net/shared/info/2179254157)
- reviewer_show_cardinfo by Steve AW (https://github.com/steveaw/anki_addons/)

This version of Card Stats combines the sidebar in Damien's add-on with the extra
review log info found in Steve AW's add-on.

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from anki.hooks import addHook
from aqt import mw
from aqt.qt import *
from aqt.webview import AnkiWebView
import aqt.stats
import time
import datetime
from anki.lang import _
from anki.utils import fmtTimeSpan
from anki.stats import CardStats


class StatsSidebar(object):
    def __init__(self, mw):
        self.mw = mw
        self.shown = False
        addHook("showQuestion", self._update)
        addHook("deckClosing", self.hide)
        addHook("reviewCleanup", self.hide)

    def _addDockable(self, title, w):
        class DockableWithClose(QDockWidget):
            closed = pyqtSignal()
            def closeEvent(self, evt):
                self.closed.emit()
                QDockWidget.closeEvent(self, evt)
        dock = DockableWithClose(title, mw)
        dock.setObjectName(title)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetClosable)
        dock.setWidget(w)
        if mw.width() < 600:
            mw.resize(QSize(600, mw.height()))
        mw.addDockWidget(Qt.RightDockWidgetArea, dock)
        return dock

    def _remDockable(self, dock):
        mw.removeDockWidget(dock)

    def show(self):
        if not self.shown:
            class ThinAnkiWebView(AnkiWebView):
                def sizeHint(self):
                    return QSize(200, 100)
            self.web = ThinAnkiWebView()
            self.shown = self._addDockable(_("Card Info"), self.web)
            self.shown.closed.connect(self._onClosed)

        self._update()

    def hide(self):
        if self.shown:
            self._remDockable(self.shown)
            self.shown = None
            #actionself.mw.form.actionCstats.setChecked(False)

    def toggle(self):
        if self.shown:
            self.hide()
        else:
            self.show()

    def _onClosed(self):
        # schedule removal for after evt has finished
        self.mw.progress.timer(100, self.hide, False)


    def _update(self):
        if not self.shown:
            return
        txt = ""
        r = self.mw.reviewer
        d = self.mw.col
        cs = CardStats(d, r.card)
        cc = r.card
        if cc:
            txt += _("<h3>Current</h3>")
            txt += d.card_stats(cc.id, 1)
        lc = r.lastCard()
        if lc:
            txt += _("<h3>Last</h3>")
            txt += d.card_stats(lc.id, 1)
        if not txt:
            txt = _("No current card or last card.")
        style = self._style()
        self.web.setHtml("""
<html><head>
</head><style>%s</style>
<body><center>%s</center></body></html>"""% (style, txt))
                
    def _style(self):
        from anki import version
        if version.startswith("2.0."):
            return ""
        return "td { font-size: 80%; }"

_cs = StatsSidebar(mw)

def cardStats(on):
    _cs.toggle()

action = QAction(mw)
action.setText("Card Stats")
action.setCheckable(True)
action.setShortcut(QKeySequence("Shift+C"))
mw.form.menuTools.addAction(action)
action.toggled.connect(cardStats)
