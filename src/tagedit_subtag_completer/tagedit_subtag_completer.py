# -*- coding: utf-8 -*-

"""
Anki Add-on: TagEdit Subtag Completion

Modifies the tag entry's autocompletion behaviour.

Allows for substring matching (either free-form or limited 
to tag boundaries as defined by the delimiters used in the
Hierarchical tags add-on).

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# Limit matches to tag hierarchy instead of arbitrary substrings
LIMIT_TO_HIERARCHY = False # Default: False
# Hierarchical tag delimiter 
HIERARCHICHAL_DELIMITER = "::" # Default: "::"
# Use substring highlight workaround
# - needed for autocompleter entries to show up properly on some
#   Linux systems that seem to suffer from a Qt bug
# - enabled by default for now. Disable this if you'd like your
#   autocompleter to look a bit nicer (if it works for you)
HIGHLIGHT_WORKAROUND = True # Default: True

##############  USER CONFIGURATION END  ##############

import re

from aqt.qt import *
from aqt import tagedit
from anki import version as anki_version

OldTagEdit = tagedit.TagEdit
OldTagCompleter = tagedit.TagCompleter

if anki_version.startswith("2.0."):
    QSOViewItem = QStyleOptionViewItemV4
else:
    QSOViewItem = QStyleOptionViewItem


class HTMLDelegate(QStyledItemDelegate):
    """
    Custom item delegate for QCompleter popup that
    allows us to render rich text
    """

    def __init__(self, *args):
        QStyledItemDelegate.__init__(self, *args)
        self.prefix = None

    def paint(self, painter, option, index):
        options = QSOViewItem(option)
        self.initStyleOption(options, index)
        if options.widget is None:
            style = QApplication.style()
        else:
            style = options.widget.style()

        # highlight search term
        prefix = self.prefix
        if prefix:
            text = options.text
            pfx = re.escape(prefix.lower())
            
            if not LIMIT_TO_HIERARCHY:
                re_match = r"({})".format(pfx)
                re_replace = r"<b>\1</b>"
                text = re.sub(re_match, re_replace, text, flags=re.I)
            else:     
                re_match = r"({1})({0})".format(pfx, HIERARCHICHAL_DELIMITER)
                re_replace = r"{0}<b>\2</b>".format(HIERARCHICHAL_DELIMITER)
                text = re.sub(re_match, re_replace, text, flags=re.I)

                re_match = "^({0})".format(pfx)
                re_replace = r"<b>\1</b>"
                text = re.sub(re_match, re_replace, text, flags=re.I)

            options.text = text
        
        doc = QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(option.rect.width())
        doc.setDocumentMargin(0) # fix lines being cut off

        options.text = ""
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        ctx = QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected
        if options.state & QStyle.State_Selected:
            ctx.palette.setColor(QPalette.Text,
                                 options.palette.color(QPalette.Active,
                                                       QPalette.HighlightedText))

        textRect = style.subElementRect(QStyle.SE_ItemViewItemText,
                                        options)
        painter.save()
        painter.translate(textRect.topLeft())
        if not HIGHLIGHT_WORKAROUND:
            painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)
        painter.restore()


class CustomTagEdit(OldTagEdit):

    """
    Custom Tag Edit Widget with support
    for custom Tag Completer
    """

    def __init__(self, parent, type=0):
        OldTagEdit.__init__(self, parent, type=type)
        self.type = type
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        # TODO: find a way to use filtered PopupCompletion 
        # (cf. https://stackoverflow.com/q/5129211/1708932)

    def setCol(self, col):
        "Set the current col, updating list of available tags."
        self.col = col
        if self.type == 0:
            l = sorted(self.col.tags.all())
        else:
            l = sorted(self.col.decks.allNames())
        self.model.setStringList(l)
        self.completer.strings = l

    def showCompleter(self):
        if self.type == 0: # tag selection
            self.completer.update(self.text())
        else: # deck selection
            self.completer.setCompletionPrefix(self.text())
        self.completer.complete()


class CustomTagCompleter(OldTagCompleter):

    """
    Custom Tag Completer that performs substring matches
    and highlights results
    """

    def __init__(self, model, parent, edit, *args):
        OldTagCompleter.__init__(self, model, parent, edit, *args)
        self.strings = []
        self.delegate = HTMLDelegate()

    
    def update(self, prefix):
        if not self.tags:
            return
        
        prefix = [self.tags[self.cursor or 0]][0]
        pfx = prefix.lower()
        hpfx = "{}{}".format(HIERARCHICHAL_DELIMITER, pfx)
        strings = self.strings
        
        if not pfx:
            filtered = strings
        else:
            if not LIMIT_TO_HIERARCHY:
                filtered = [s for s in strings if pfx in s.lower()]
            else:
                filtered = [s for s in strings
                    if hpfx in s.lower() or s.lower().startswith(pfx)]
        self.model().setStringList(filtered)
        
        self.delegate.prefix = prefix
        self.popup().setItemDelegate(self.delegate)


# Hooks
tagedit.TagEdit = CustomTagEdit
tagedit.TagCompleter = CustomTagCompleter