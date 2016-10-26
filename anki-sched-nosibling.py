#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
Anki Add-on: Skip sibling burying for notes with an "-ns" suffix

This won't influence scheduling on any other Anki client, such
as AnkiWeb, AnkiMobile, or AnkiDroid.

Copyright: Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

from anki.hooks import addHook, wrap
from aqt import *

def myBurySiblings(self, card, _old):
    model = card.note().model()['name']
    if model.endswith("-ns"):
        print "Skipping burying for %s" % model
        return
    _old(self,card)

def profileLoaded():
    # add scheduler
    anki.sched.Scheduler._burySiblings = wrap(
        anki.sched.Scheduler._burySiblings,myBurySiblings, "around")

addHook("profileLoaded", profileLoaded)
