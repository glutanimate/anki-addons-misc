# -*- coding: utf-8 -*-

"""
Anki Add-on: More Answer Buttons for New Cards

Adds extra buttons to the answer button area for new cards

Copyright:  (c) 2013 Steve AW <steveawa@gmail.com>
            (c) 2016-2019 Glutanimate <https://glutanimate.com/>
            (c) 2019 ijgnd
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from aqt.reviewer import Reviewer
from anki.hooks import wrap, addHook
from aqt.utils import tooltip
from anki.lang import _
from aqt import mw


def getConfig():
    return mw.addonManager.getConfig(__name__)


#Must be four or less
extra_buttons = getConfig().get("extra_buttons", None)
assert len(extra_buttons) <= 4

#Anki uses a single digit to track which button has been clicked.
#We will use 6 and above to track the extra buttons.
INTERCEPT_EASE_BASE = 6


#todo: brittle. Replaces existing function
def _answerButtons21(self):
    default = self._defaultEase()

    def but(i, label):
        if i == default:
            extra = "id=defease"
        else:
            extra = ""
        due = self._buttonTime(i)
        return '''
<td align=center>%s<button %s title="%s" data-ease="%s" onclick='pycmd("ease%d");'>\
%s</button></td>''' % (due, extra, _("Shortcut key: %s") % i, i, i, label)

    buf = "<center><table cellpading=0 cellspacing=0><tr>"
    for ease, label in self._answerButtonList():
        buf += but(ease, label)

    #################mod start
    #Only for cards in the new queue
    if self.card.type in (0, 1, 3): # New, Learn, Day learning
        #Check that the number of answer buttons is as expected.
        if self.mw.col.sched.name == "std":
            assert self.mw.col.sched.answerButtons(self.card) == 3
        if self.mw.col.sched.name == "std2":
            assert self.mw.col.sched.answerButtons(self.card) == 4

        def my_buttonTime(text):
            if not mw.col.conf['estTimes']:
                return "<div class=spacer></div>"
            return '<span class=nobold>%s</span><br>' % text

        #python lists are 0 based
        extra_buttons = getConfig().get("extra_buttons", None)
        for i, buttonItem in enumerate(extra_buttons):
            j = i + INTERCEPT_EASE_BASE
            due = my_buttonTime(buttonItem["Description"])
            buf +='''<td align=center>%s<button %s title="%s" data-ease="%s" onclick='pycmd("ease%d");'>\
%s</button></td>''' % (due, "", _("Shortcut key: %s") % buttonItem["ShortCut"], j, j, buttonItem["Label"])

    ###################mod end

    buf += "</tr></table>"
    script = """
<script>$(function () { $("#defease").focus(); });</script>"""
    return buf + script



#This wraps existing Reviewer._answerCard function.    
def answer_card_intercepting21(self, actual_ease, _old):
    ease = actual_ease
    #in 2.1 this function is also called when you are in the deck overview screen where self.card does not exit
    if hasattr(self,"card"):
        was_new_card = self.card.type in (0, 1, 3)
        is_extra_button = was_new_card and actual_ease >= INTERCEPT_EASE_BASE
        if is_extra_button:
            #Make sure this is as expected.
            if self.mw.col.sched.name == "std":
                assert self.mw.col.sched.answerButtons(self.card) == 3
                #So this is one of our buttons. First answer the card as if "Easy" clicked.
                ease = 3
            if self.mw.col.sched.name == "std2":
                assert self.mw.col.sched.answerButtons(self.card) == 4
                #So this is one of our buttons. First answer the card as if "Easy" clicked.
                ease = 4
            #We will need this to reschedule it.
            prev_card_id = self.card.id
            #
        ret = _old(self, ease)

        if is_extra_button:
            extra_buttons = getConfig().get("extra_buttons", None)
            buttonItem = extra_buttons[actual_ease - INTERCEPT_EASE_BASE]
            #Do the reschedule.
            self.mw.col.sched.reschedCards([prev_card_id], buttonItem["ReschedMin"], buttonItem["ReschedMax"])
            tooltip("<center>Rescheduled:" + "<br>" + buttonItem["Description"] + "</center>")
        return ret


def addShortcuts21(shortcuts):
    additions = []
    extra_buttons = getConfig().get("extra_buttons", None)
    for i, buttonItem in enumerate(extra_buttons): 
        key = str( buttonItem["ShortCut"] )
        additions.append([key , lambda a=i: mw.reviewer._answerCard(a + INTERCEPT_EASE_BASE)])
    shortcuts += additions
addHook("reviewStateShortcuts", addShortcuts21)


Reviewer._answerButtons = _answerButtons21
Reviewer._answerCard = wrap(Reviewer._answerCard, answer_card_intercepting21, "around")
