# -*- coding: utf-8 -*-

"""
Anki Add-on: More Answer Buttons for New Cards

Adds extra buttons to the answer button area for new cards

Copyright:  (c) Steve AW 2013 <steveawa@gmail.com>
            (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# Setup data:
#
# List of dicts, where each item of the list (a dict) is the data for a new button.
# This can be edited to suit, but there can not be more than 4 buttons.
#     Description ... appears above the button
#     Label ... the label of the button
#     ShortCut ... the shortcut key for the button
#     ReschedMin ... same as the lower number in the Browser's "Edit/Rescedule" command
#     ReschedMax ... same as the higher number in the Browser's "Edit/Rescedule" command

extra_buttons = [{"Description": "3-4d", "Label": "3-4", "ShortCut": "5",
                        "ReschedMin": 3, "ReschedMax": 4},
                 {"Description": "5-7d", "Label": "5-7", "ShortCut": "6",
                        "ReschedMin": 5, "ReschedMax": 7},
                 {"Description": "8-15d", "Label": "8-15", "ShortCut": "7",
                        "ReschedMin": 8, "ReschedMax": 15}]

##############  USER CONFIGURATION END  ##############

#Must be four or less
assert len(extra_buttons) <= 4

from aqt.reviewer import Reviewer
from anki.hooks import wrap
from aqt.utils import tooltip

#Anki uses a single digit to track which button has been clicked.
#We will use 6 and above to track the extra buttons.
INTERCEPT_EASE_BASE = 6

#todo: brittle. Replaces existing function
def _answerButtons(self):
    times = []
    default = self._defaultEase()

    def but(i, label):
        if i == default:
            extra = "id=defease"
        else:
            extra = ""
        due = self._buttonTime(i)
        return '''
<td align=center>%s<button %s title="%s" onclick='py.link("ease%d");'>\
%s</button></td>''' % (due, extra, _("Shortcut key: %s") % i, i, label)

    buf = "<center><table cellpading=0 cellspacing=0><tr>"
    for ease, label in self._answerButtonList():
        buf += but(ease, label)
        #swAdded start ====>
    #Only for cards in the new queue
    if self.card.type in (0, 1, 3): # New, Learn, Day learning
        #Check that the number of answer buttons is as expected.
        assert self.mw.col.sched.answerButtons(self.card) == 3
        #python lists are 0 based
        for i, buttonItem in enumerate(extra_buttons):
            buf += '''
<td align=center><span class=nobold>%s</span><br><button title="Short key: %s" onclick='py.link("ease%d");'>\
%s</button></td>''' % (buttonItem["Description"], buttonItem["ShortCut"], i + INTERCEPT_EASE_BASE, buttonItem["Label"])
            #swAdded end
    buf += "</tr></table>"
    script = """
<script>$(function () { $("#defease").focus(); });</script>"""
    return buf + script

#This wraps existing Reviewer._answerCard function.    
def answer_card_intercepting(self, actual_ease, _old):
    ease = actual_ease
    was_new_card = self.card.type in (0, 1, 3)
    is_extra_button = was_new_card and actual_ease >= INTERCEPT_EASE_BASE
    if is_extra_button:
        #Make sure this is as expected.
        assert self.mw.col.sched.answerButtons(self.card) == 3
        #So this is one of our buttons. First answer the card as if "Easy" clicked.
        ease = 3
        #We will need this to reschedule it.
        prev_card_id = self.card.id
        #
    ret = _old(self, ease)

    if is_extra_button:
        buttonItem = extra_buttons[actual_ease - INTERCEPT_EASE_BASE]
        #Do the reschedule.
        self.mw.col.sched.reschedCards([prev_card_id], buttonItem["ReschedMin"], buttonItem["ReschedMax"])
        tooltip("<center>Rescheduled:" + "<br>" + buttonItem["Description"] + "</center>")
    return ret

#Handle the shortcut. Used changekeys.py addon as a guide     
def keyHandler(self, evt, _old):
    key = unicode(evt.text())
    if self.state == "answer":
        for i, buttonItem in enumerate(extra_buttons):
            if key == buttonItem["ShortCut"]:
                #early exit ok in python?
                return self._answerCard(i + INTERCEPT_EASE_BASE)
    return _old(self, evt)


Reviewer._keyHandler = wrap(Reviewer._keyHandler, keyHandler, "around")
Reviewer._answerButtons = _answerButtons
Reviewer._answerCard = wrap(Reviewer._answerCard, answer_card_intercepting, "around")
