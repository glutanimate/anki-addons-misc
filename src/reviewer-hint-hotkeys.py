# -*- coding: utf-8 -*-
# Author:  Ben Lickly <blickly at berkeley dot edu>
#          modified by Glutanimate 2016 (github.com/Glutanimate)
#
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   Hint-peeking add-on
#
# This add-on allows peeking at some of the fields in a flashcard
# before seeing the answer. This can be used to peek at word context,
# example sentences, word pronunciation (especially useful for
# Chinese/Japanese/Korean), and much more.
#
# Modified by Glutanimate to add gradual hint reveal

from PyQt4.QtCore import Qt

########################### Settings #######################################
# The following settings can be changed to suit your needs. Lines
# starting with a pound sign (#) are comments and are ignored.

# SHOW_HINT_KEY defines the key that will reveal the hint fields one by one.
SHOW_HINT_KEY=Qt.Key_H
# SHOW_ALL_HINTS_KEY defines the key that will reveal the hint fields all at once.
SHOW_ALL_HINTS_KEY=Qt.Key_G
# A list of possible key values can be found at:
#       http://opendocs.net/pyqt/pyqt4/html/qt.html#Key-enum


######################### End of Settings ##################################

from anki.hooks import wrap
from aqt.reviewer import Reviewer

def newKeyHandler(self, evt, _old):
    """Show hint when the SHOW_HINT_KEY is pressed."""
    if evt.key() == SHOW_HINT_KEY:
        self._showHint("one")
    elif evt.key() == SHOW_ALL_HINTS_KEY:
        self._showHint("all")
    return _old(self, evt)


def _showHint(self, unhideMode):
    """To show hint, simply click all show hint buttons."""
    self.web.eval("""
     var unhideMode = "%s";
     var customEvent = document.createEvent('MouseEvents');
     customEvent.initEvent('click', false, true);
     var arr = document.getElementsByTagName('a');
     for (var i=0; i<arr.length; i++) {
        var l=arr[i];
        if (l.style.display === 'none') {
          continue;
        }
        if (l.href.charAt(l.href.length-1) === '#') {
          l.dispatchEvent(customEvent);
          if (unhideMode === 'one') {
            break;
          }
        }
     }
     """ % unhideMode)

Reviewer._showHint = _showHint
Reviewer._keyHandler = wrap(Reviewer._keyHandler, newKeyHandler, "around")

