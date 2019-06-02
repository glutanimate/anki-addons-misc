# -*- coding: utf-8 -*-

# Speed Focus Mode Add-on for Anki
#
# Copyright (C) 2017-2019  Aristotelis P. <https://glutanimate.com/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version, with the additions
# listed at the end of the license file that accompanied this program.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# NOTE: This program is subject to certain additional terms pursuant to
# Section 7 of the GNU Affero General Public License.  You should have
# received a copy of these additional terms immediately following the
# terms and conditions of the GNU Affero General Public License that
# accompanied this program.
#
# If not, please request a copy through one of the means of contact
# listed here: <https://glutanimate.com/contact/>.
#
# Any modifications to this file must keep this entire header intact.

"""
Initializes add-on components.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import os

from aqt.qt import *
from aqt import mw
from aqt.reviewer import Reviewer
from aqt.deckconf import DeckConf
from aqt.forms import dconf
from aqt.utils import tooltip

from anki.hooks import addHook, wrap
from anki.sound import play
from anki.lang import _

# Anki 2.1 support
from anki import version as anki_version
ANKI20 = anki_version.startswith("2.0.")
pycmd = "py.link" if ANKI20 else "pycmd"


# determine sound file path
sys_encoding = sys.getfilesystemencoding()

if not ANKI20:
    addon_path = os.path.dirname(__file__)
else:
    addon_path = os.path.dirname(__file__).decode(sys_encoding)

alert_path = os.path.join(addon_path, "sounds", "alert.mp3")



def append_html(self, _old):
    return _old(self) + """
        <script>
            var autoAnswerTimeout = 0;
            var autoAgainTimeout = 0;
            var autoAlertTimeout = 0;

            var setAutoAnswer = function(ms) {
                clearTimeout(autoAnswerTimeout);
                autoAnswerTimeout = setTimeout(function () { %s('ans') }, ms);
            }
            var setAutoAgain = function(ms) {
                clearTimeout(autoAgainTimeout);
                autoAgainTimeout = setTimeout(function () { %s("ease1"); }, ms);
            }
            var setAutoAlert = function(ms) {
                clearTimeout(autoAlertTimeout);
                autoAlertTimeout = setTimeout(function () { %s("autoalert"); }, ms);
            }
        </script>
        """ % (pycmd, pycmd, pycmd)


# set timeouts for auto-alert and auto-reveal
def set_answer_timeout(self):
    c = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    if c.get('autoAnswer', 0) > 0:
        self.bottom.web.eval("setAutoAnswer(%d);" % (c['autoAnswer'] * 1000))
    if c.get('autoAlert', 0) > 0:
        self.bottom.web.eval("setAutoAlert(%d);" % (c['autoAlert'] * 1000))

# set timeout for auto-again
def set_again_timeout(self):
    c = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    if c.get('autoAgain', 0) > 0:
        self.bottom.web.eval("setAutoAgain(%d);" % (c['autoAgain'] * 1000))



# clear timeouts for auto-alert and auto-reveal, run on answer reveal
def clear_answer_timeout():
    mw.reviewer.bottom.web.eval("""
        if (typeof autoAnswerTimeout !== 'undefined') {
            clearTimeout(autoAnswerTimeout);
        }
        if (typeof autoAlertTimeout !== 'undefined') {
            clearTimeout(autoAlertTimeout);
        }
    """)

# clear timeout for auto-again, run on next card
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
    label1.setText(_("Automatically play alert after"))
    label2 = QLabel(self.tab_5)
    label2.setText(_("seconds"))
    self.autoAlert = QSpinBox(self.tab_5)
    self.autoAlert.setMinimum(0)
    self.autoAlert.setMaximum(3600)
    grid.addWidget(label1, 0, 0, 1, 1)
    grid.addWidget(self.autoAlert, 0, 1, 1, 1)
    grid.addWidget(label2, 0, 2, 1, 1)
    self.verticalLayout_6.insertLayout(1, grid)

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
    self.verticalLayout_6.insertLayout(2, grid)

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
    self.verticalLayout_6.insertLayout(3, grid)


def load_conf(self):
    f = self.form
    c = self.conf
    f.autoAlert.setValue(c.get('autoAlert', 0))
    f.autoAnswer.setValue(c.get('autoAnswer', 0))
    f.autoAgain.setValue(c.get('autoAgain', 0))


def save_conf(self):
    f = self.form
    c = self.conf
    c['autoAlert'] = f.autoAlert.value()
    c['autoAnswer'] = f.autoAnswer.value()
    c['autoAgain'] = f.autoAgain.value()


# Sound playback

def linkHandler(self, url, _old):
    if not url.startswith("autoalert"):
        return _old(self, url)
    if not self.mw.col:
        # collection unloaded, e.g. when called during pre-exit sync
        return
    play(alert_path)
    c = self.mw.col.decks.confForDid(self.card.odid or self.card.did)
    timeout = c.get('autoAlert', 0)
    tooltip("Wake up! You have been looking at <br>"
            "the question for <b>{}</b> seconds!".format(timeout),
            period=1000)


# Hooks

Reviewer._bottomHTML = wrap(Reviewer._bottomHTML, append_html, 'around')
Reviewer._showAnswerButton = wrap(
    Reviewer._showAnswerButton, set_answer_timeout)
Reviewer._showEaseButtons = wrap(Reviewer._showEaseButtons, set_again_timeout)
Reviewer._linkHandler = wrap(Reviewer._linkHandler, linkHandler, "around")
addHook("showAnswer", clear_answer_timeout)
addHook("showQuestion", clear_again_timeout)

dconf.Ui_Dialog.setupUi = wrap(dconf.Ui_Dialog.setupUi, setup_ui)
DeckConf.loadConf = wrap(DeckConf.loadConf, load_conf)
DeckConf.saveConf = wrap(DeckConf.saveConf, save_conf, 'before')
