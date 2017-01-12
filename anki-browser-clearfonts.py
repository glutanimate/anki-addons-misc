# -*- coding: utf-8 -*-

"""
Anki Add-on: Clear Template Fonts

Deletes card-specific font and font-size settings in order to 
restore default appearance. This is not possible through the
regular card types dialog.

Also modifies the card types dialog so that font attributes
are only applied if they differ from the defaults (Arial 12).

Setting the attributes to Arial 12 on a card with non-default
font attributes will reset it to the defaults.

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
 
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import tooltip, askUser
from aqt.clayout import CardLayout

def myBrowserDisplayOk(self, f):
    t = self.card.template()
    t['bqfmt'] = f.qfmt.text().strip()
    t['bafmt'] = f.afmt.text().strip()
    bfont = f.font.currentFont().family()
    bsize = f.fontSize.value()
    # only apply settings if defaults changed
    # if set to defaults reset custom attributes
    if bfont != "Arial":
        t['bfont'] = bfont
    elif "bfont" in t and t['bfont'] != "Arial":
        del t['bfont']
    if bsize != 12:
        t['bsize'] = bsize
    elif "bsize" in t and t['bsize'] != 12:
        del t['bsize']

def clearFonts(self):
    q = ("This will reset the browser font attributes for "
        "<b>every single note type</b> in your collection."
        "Are you sure you want to proceed?")
    if not askUser(q, parent=self):
        return
    mw = self.mw
    mm = mw.col.models
    models = mm.all()
    cnt = 0
    for model in models:
        templates = model['tmpls']
        update = False
        for template in templates:
            try:
                del template["bfont"]
                del template["bsize"]
                print "Deleting font attributes"
                update = True
                cnt += 1
            except KeyError:
                print "No font attributes to delete"
        if update:
            mm.update(model)
    tooltip("Deleted font attributes for {0} card template(s)".format(cnt))

def setupMenu(self):
    menu = self.form.menuEdit
    a = menu.addAction('Reset Card Browser Fonts')
    self.connect(a, SIGNAL("triggered()"), lambda b=self: clearFonts(b))


addHook("browser.setupMenus", setupMenu)
CardLayout.onBrowserDisplayOk = myBrowserDisplayOk