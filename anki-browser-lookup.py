# coding: utf-8

"""
Simple addon to quickly look up words in Anki's Browser

Copyright: Glutanimate 2015 (https://github.com/Glutanimate)
Based on 'OSX Dictionary Lookup' by Eddie Blundell <eblundell@gmail.com>:
https://gist.github.com/eddie/ff3d820fb267ae26ca0e

License: The MIT License (MIT)
"""


# Anki
import aqt
from anki.hooks import addHook

# Qt
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BrowserLookup:

  def get_selected(self, view):
    """Copy selected text"""
    return view.page().selectedText()

  def lookup_action(self, view):
    browser = aqt.dialogs.open("Browser", aqt.mw)
    browser.form.searchEdit.lineEdit().setText(self.get_selected(view))
    browser.onSearch()

  def add_action(self, view, menu, action):
    """Add 'lookup' action to context menu"""
    if self.get_selected(view):
      action = menu.addAction(action)
      action.connect(action, SIGNAL('triggered()'),
        lambda view=view: self.lookup_action(view))

  def context_lookup_action(self, view, menu):
    """Browser Lookup action"""
    self.add_action(view, menu,
      u'Search Browser for %s...' % self.get_selected(view)[:20])

# Add lookup actions to context menu
browser_lookup = BrowserLookup()
addHook("AnkiWebView.contextMenuEvent", browser_lookup.context_lookup_action)
