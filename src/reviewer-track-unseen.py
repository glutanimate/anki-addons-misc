# -*- coding: utf-8 -*-

"""
Anki Add-on: Track Unseen Cards

Original Description:

I am using this in conjunction with cramming. It uses tags (nsN,ns1,ns2,nsX where X is 
the card's ordinal number) to identify a set of cards, and then as the cards are viewed, 
it automatically removes that card's tag from its note. The idea behind it is: Say I have 
an exam in a week. My goal is to review all my cards that relate to the exam over the 
coming week, doing bits and pieces wherever I can. In reality, I often don't get the time 
to do all of them, but if each day I can do a random smattering of 50-100 extra cards, 
that is generally good enough.

I never found a good way, with the inbuilt cramming/study more tools,
to reliably keep track of what cards had been crammed when cramming across 
multiple sessions (the changed field/ "Last reviewed" gets updated when cards are added 
to dynamic decks which makes it useless for my needs). This addon allows me to add the 
tags to those cards I want to see. I can then create dynamic decks for those tags 
(tag:ns*), and the tags only get removed from cards that are seen. It gives me confidence 
that I am not re-cramming a card, and also allows me to see how many are still "unseen". 
I will see how it goes this semester, but I think it is going to finally give me a good 
way to systematically cram.

Copyright:  (c) Steve AW 2013 <steveawa@gmail.com>
            (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QMenu, QKeySequence
from anki.hooks import addHook, wrap
from anki.sched import Scheduler
from aqt.reviewer import Reviewer
from aqt.utils import tooltip


__author__ = 'Steve'

unseen_tag = ".unseen"

def add_unseen_tags_to_selected(self):
    #self is browser
    selected_cids = self.selectedCards()
    if not selected_cids:
        tooltip(_("No cards selected."), period=2000)
        return
    self.mw.progress.start()
    self.mw.checkpoint("Add Unseen Tags")
    self.model.beginReset()
    for cid in selected_cids:
        unseen_card = self.col.getCard(cid)
        unseen_note = unseen_card.note()
        unseen_note.addTag(unseen_tag)
        unseen_note.flush()
    self.model.endReset()
    self.mw.requireReset()
    self.mw.progress.finish()
    tooltip("Added " + unseen_tag + " to notes")


def remove_unseen_tags_from_selected(self):
    #self is browser
    selected_cids = self.selectedCards()
    if not selected_cids:
        tooltip(_("No cards selected."), period=2000)
        return
    self.mw.progress.start()
    self.mw.checkpoint("Remove Unseen Tags")
    self.model.beginReset()
    for cid in selected_cids:
        unseen_card = self.col.getCard(cid)
        unseen_note = unseen_card.note()
        unseen_note.delTag(unseen_tag)
        unseen_note.flush()
    self.model.endReset()
    self.mw.requireReset()
    self.mw.progress.finish()
    tooltip("Removed " + unseen_tag + " from notes")


def change_background_color(self):
    pot_unseen_card = self.card
    pot_unseen_note = pot_unseen_card.note()
    if pot_unseen_note.hasTag(unseen_tag):
        #We have to remove this, and play nicely with other addons that may fiddle with background
        self.web.eval('document.body.style.backgroundColor = "#FFFBBF"')

def wipe_background_for_nextCard(self):
    #do this early enough so that any addon applying colour changes
    #does it after
    self.web.eval('document.body.style.backgroundColor = "#FFFFFF"')

def _remove_unseen_tags_for_card_and_note(pot_unseen_card, pot_unseen_note):
    if pot_unseen_note.hasTag(unseen_tag):
        pot_unseen_note.delTag(unseen_tag)
        pot_unseen_note.flush()


def _remove_unseen_tags(self):
    pot_unseen_card = self.card
    pot_unseen_note = pot_unseen_card.note()
    _remove_unseen_tags_for_card_and_note(pot_unseen_card, pot_unseen_note)


def answer_card_removing_unseen_tags(self, ease):
    #self is reviewer
    #Keep these guards in place ... not sure why?
    if self.mw.state != "review":
        return
    if self.state != "answer":
        return
    _remove_unseen_tags(self)


def suspend_cards_removing_unseen_tags(self, ids):
    #self is Scheduler
    for cid in ids:
        sus_card = self.col.getCard(cid)
        sus_note = sus_card.note()
        _remove_unseen_tags_for_card_and_note(sus_card, sus_note)


def show_all_unseen_cards(self):
    #self is browser
    self.form.searchEdit.lineEdit().setText("tag:" + unseen_tag)
    self.onSearch()


def setup_browser_menu(self):
    #self is browser
    try:
        # used by multiple add-ons, so we check for its existence first
        menu = self.menuTags
    except:
        self.menuTags = QMenu(_("Tags"))
        action = self.menuBar().insertMenu(self.mw.form.menuTools.menuAction(), self.menuTags)
    menu = self.menuTags
    menu.addSeparator()
    unseen_menu = menu.addMenu("Unseen Card Tracking")
    a = unseen_menu.addAction('Add "Unseen" Tags to Selected Cards')
    a.setShortcut(QKeySequence("Ctrl+U"))
    self.connect(a, SIGNAL("triggered()"), lambda b=self: add_unseen_tags_to_selected(b))
    a = unseen_menu.addAction('Remove "Unseen" Tags from Selected Cards')
    a.setShortcut(QKeySequence("Ctrl+Shift+U"))
    self.connect(a, SIGNAL("triggered()"), lambda b=self: remove_unseen_tags_from_selected(b))
    a = unseen_menu.addAction('Show all Unseen Cards')
    a.setShortcut(QKeySequence("Ctrl+Alt+U"))
    self.connect(a, SIGNAL("triggered()"), lambda b=self: show_all_unseen_cards(b))

#todo: menu action to set search string to show all
addHook("browser.setupMenus", setup_browser_menu)
Reviewer._answerCard = wrap(Reviewer._answerCard, answer_card_removing_unseen_tags, "before")
Reviewer._showQuestion = wrap(Reviewer._showQuestion, change_background_color, "after")
# have to call this again on the answer side because of JS Booster add-on
Reviewer._showAnswer = wrap(Reviewer._showAnswer, change_background_color, "after")

Reviewer.nextCard = wrap(Reviewer.nextCard, wipe_background_for_nextCard, "before")

#By wrapping this, we cover suspending cards/notes etc
Scheduler.suspendCards = wrap(Scheduler.suspendCards, suspend_cards_removing_unseen_tags, "before")
