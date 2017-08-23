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

    #copy and paste from Browser
    #Added IntDate column
    def _revlogData(self, card, cs):
        entries = self.mw.col.db.all(
            "select id/1000.0, ease, ivl, factor, time/1000.0, type "
            "from revlog where cid = ?", card.id)
        if not entries:
            return ""
        s = "<table width=100%%><tr><th align=left>%s</th>" % _("Date")
        s += ("<th align=right>%s</th>" * 6) % (
            _("Type"), _("Rating"), _("Interval"), "IntDate", _("Ease"), _("Time"))
        cnt = 0
        for (date, ease, ivl, factor, taken, type) in reversed(entries):
            cnt += 1
            s += "<tr><td>%s</td>" % time.strftime(_("<b>%Y-%m-%d</b> @ %H:%M"),
                                                   time.localtime(date))
            tstr = [_("Learn"), _("Review"), _("Relearn"), _("Filtered"),
                    _("Resched")][type]
            import anki.stats as st

            fmt = "<span style='color:%s'>%s</span>"
            if type == 0:
                tstr = fmt % (st.colLearn, tstr)
            elif type == 1:
                tstr = fmt % (st.colMature, tstr)
            elif type == 2:
                tstr = fmt % (st.colRelearn, tstr)
            elif type == 3:
                tstr = fmt % (st.colCram, tstr)
            else:
                tstr = fmt % ("#000", tstr)
            if ease == 1:
                ease = fmt % (st.colRelearn, ease)
                ####################
            int_due = "na"
            if ivl > 0:
                int_due_date = time.localtime(date + (ivl * 24 * 60 * 60))
                int_due = time.strftime(_("%Y-%m-%d"), int_due_date)
                ####################
            if ivl == 0:
                ivl = _("0d")
            elif ivl > 0:
                ivl = fmtTimeSpan(ivl * 86400, short=True)
            else:
                ivl = cs.time(-ivl)

            s += ("<td align=right>%s</td>" * 6) % (
                tstr,
                ease, ivl,
                int_due
                ,
                "%d%%" % (factor / 10) if factor else "",
                cs.time(taken)) + "</tr>"
        s += "</table>"
        if cnt < card.reps:
            s += _("""\
Note: Some of the history is missing. For more information, \
please see the browser documentation.""")
        return s

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
            txt += d.cardStats(cc)
            txt += "<p>"
            txt += self._revlogData(cc, cs)
        lc = r.lastCard()
        if lc:
            txt += _("<h3>Last</h3>")
            txt += d.cardStats(lc)
            txt += "<p>"
            txt += self._revlogData(lc, cs)
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
