# -*- coding: utf-8 -*-

"""
Anki Add-on: Automatically show answer and rate after X seconds

Based on "Automatically show answer after X seconds"
(https://ankiweb.net/shared/info/648362761)

The original author of this add-on is unknown, sadly,
but all credit for the original idea goes to them.

Copyright: (c) 2017 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from aqt.qt import *
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.deckconf import DeckConf
from aqt.forms import dconf
from anki.hooks import addHook, wrap

from anki import version as anki_version
anki21 = anki_version.startswith("2.1.")

pycmd = "pycmd" if anki21 else "py.link"

def append_html(self, _old):
    return _old(self) + """
        <script>
            var autoAnswerTimeout = 0;
            var autoAgainTimeout = 0;

            var setAutoAnswer = function(ms) {
                clearTimeout(autoAnswerTimeout);
                autoAnswerTimeout = setTimeout(function () { %s('ans') }, ms);
            }
            var setAutoAgain = function(ms) {
                clearTimeout(autoAgainTimeout);
                autoAgainTimeout = setTimeout(function () { %s("ease1"); }, ms);
            }
        </script>
        """ % (pycmd, pycmd)


def set_answer_timeout(self):
    c = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    if c.get('autoAnswer', 0) > 0:
        self.bottom.web.eval("setAutoAnswer(%d);" % (c['autoAnswer'] * 1000))


def set_again_timeout(self):
    c = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    if c.get('autoAgain', 0) > 0:
        self.bottom.web.eval("setAutoAgain(%d);" % (c['autoAgain'] * 1000))


def clear_answer_timeout():
    mw.reviewer.bottom.web.eval("""
        if (typeof autoAnswerTimeout !== 'undefined') {
            clearTimeout(autoAnswerTimeout);
        }
    """)


def clear_again_timeout():
    mw.reviewer.bottom.web.eval("""
        if (typeof autoAgainTimeout !== 'undefined') {
            clearTimeout(autoAgainTimeout);
        }
    """)


def setup_ui(self, Dialog):
    self.maxTaken.setMinimum(3)

    grid = QGridLayout()
    label1 = QLabel(self.tab_5)
    label1.setText(_("Automatically show answer after"))
    label2 = QLabel(self.tab_5)
    label2.setText(_("seconds"))
    self.autoAnswer = QSpinBox(self.tab_5)
    self.autoAnswer.setMinimum(0)
    self.autoAnswer.setMaximum(3600)
    grid.addWidget(label1, 0, 0, 1, 1)
    grid.addWidget(self.autoAnswer, 0, 1, 1, 1)
    grid.addWidget(label2, 0, 2, 1, 1)
    self.verticalLayout_6.insertLayout(1, grid)

    grid = QGridLayout()
    label1 = QLabel(self.tab_5)
    label1.setText(_("Automatically rate 'again' after"))
    label2 = QLabel(self.tab_5)
    label2.setText(_("seconds"))
    self.autoAgain = QSpinBox(self.tab_5)
    self.autoAgain.setMinimum(0)
    self.autoAgain.setMaximum(3600)
    grid.addWidget(label1, 0, 0, 1, 1)
    grid.addWidget(self.autoAgain, 0, 1, 1, 1)
    grid.addWidget(label2, 0, 2, 1, 1)
    self.verticalLayout_6.insertLayout(2, grid)


def load_conf(self):
    f = self.form
    c = self.conf
    f.autoAnswer.setValue(c.get('autoAnswer', 0))
    f.autoAgain.setValue(c.get('autoAgain', 0))


def save_conf(self):
    f = self.form
    c = self.conf
    c['autoAnswer'] = f.autoAnswer.value()
    c['autoAgain'] = f.autoAgain.value()


# Hooks

Reviewer._bottomHTML = wrap(Reviewer._bottomHTML, append_html, 'around')
Reviewer._showAnswerButton = wrap(
    Reviewer._showAnswerButton, set_answer_timeout)
Reviewer._showEaseButtons = wrap(Reviewer._showEaseButtons, set_again_timeout)
addHook("showAnswer", clear_answer_timeout)
addHook("showQuestion", clear_again_timeout)
dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setup_ui)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
