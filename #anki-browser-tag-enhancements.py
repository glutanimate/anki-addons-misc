# -*- coding: utf-8 -*-

"""
Anki Add-on: Browser Tag Entry Enhancements

Modifications that should improve tag handling in the browser:

- Ctrl+Shift+T will focus the tags field when only one card is selected
- Preserve tag field focus when switching between cards using Ctrl+N/P

TODO: file a pull request to get these changes integrated into Anki

CAVE: Overwrites a lot of default methods. Might lead to compatibility issues
with other add-ons.

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
from aqt.qt import *
from anki.hooks import addHook, runHook, wrap
from aqt.browser import Browser
from aqt.editor import Editor
from aqt.utils import shortcut, downArrow, getTag

def addTags(self, tags=None, label=None, prompt=None, func=None):
    if not tags and len(self.selectedNotes()) == 1:
        self.editor.tags.setFocus()
        return
    if prompt is None:
        prompt = _("Enter tags to add:")
    if tags is None:
        (tags, r) = getTag(self, self.col, prompt)
    else:
        r = True
    if not r:
        return
    if func is None:
        func = self.col.tags.bulkAdd
    if label is None:
        label = _("Add Tags")
    if label:
        self.mw.checkpoint(label)
    self.model.beginReset()
    func(self.selectedNotes(), tags)
    self.model.endReset()
    self.mw.requireReset()

def onPreviousCard(self):
    tagfocus = self.editor.tags.hasFocus() # preserve tag field focus
    f = self.editor.currentField
    self._moveCur(QAbstractItemView.MoveUp)
    if tagfocus:
        self.editor.tags.setFocus()
    else:
        self.editor.web.setFocus()
        self.editor.web.eval("focusField(%d)" % f)

def onNextCard(self):
    tagfocus = self.editor.tags.hasFocus()
    f = self.editor.currentField
    self._moveCur(QAbstractItemView.MoveDown)
    if tagfocus:
        self.editor.tags.setFocus()
    else:
        self.editor.web.setFocus()
        self.editor.web.eval("focusField(%d)" % f)

def setupButtons(self):
    self._buttons = {}
    # button styles for mac
    if not isMac:
        self.plastiqueStyle = QStyleFactory.create("plastique")
        if not self.plastiqueStyle:
            # plastique was removed in qt5
            self.plastiqueStyle = QStyleFactory.create("fusion")
        self.widget.setStyle(self.plastiqueStyle)
    else:
        self.plastiqueStyle = None
    # icons
    self.iconsBox = QHBoxLayout()
    if not isMac:
        self.iconsBox.setMargin(6)
        self.iconsBox.setSpacing(0)
    else:
        self.iconsBox.setMargin(0)
        self.iconsBox.setSpacing(14)
    self.outerLayout.addLayout(self.iconsBox)
    b = self._addButton
    b("fields", self.onFields, "",
      shortcut(_("Customize Fields")), size=False, text=_("Fields..."),
      native=True, canDisable=False)
    self.iconsBox.addItem(QSpacerItem(6,1, QSizePolicy.Fixed))
    b("layout", self.onCardLayout, _("Ctrl+L"),
      shortcut(_("Customize Cards (Ctrl+L)")),
      size=False, text=_("Cards..."), native=True, canDisable=False)
    # align to right
    self.iconsBox.addItem(QSpacerItem(20,1, QSizePolicy.Expanding))
    b("text_bold", self.toggleBold, _("Ctrl+B"), _("Bold text (Ctrl+B)"),
      check=True)
    b("text_italic", self.toggleItalic, _("Ctrl+I"), _("Italic text (Ctrl+I)"),
      check=True)
    b("text_under", self.toggleUnderline, _("Ctrl+U"),
      _("Underline text (Ctrl+U)"), check=True)
    b("text_super", self.toggleSuper, _("Ctrl+Shift+="),
      _("Superscript (Ctrl+Shift+=)"), check=True)
    b("text_sub", self.toggleSub, _("Ctrl+="),
      _("Subscript (Ctrl+=)"), check=True)
    b("text_clear", self.removeFormat, _("Ctrl+R"),
      _("Remove formatting (Ctrl+R)"))
    but = b("foreground", self.onForeground, _("F7"), text=" ")
    but.setToolTip(_("Set foreground colour (F7)"))
    self.setupForegroundButton(but)
    but = b("change_colour", self.onChangeCol, _("F8"),
      _("Change colour (F8)"), text=downArrow())
    but.setFixedWidth(12)
    but = b("cloze", self.onCloze, _("Ctrl+Shift+C"),
            _("Cloze deletion (Ctrl+Shift+C)"), text="[...]")
    but.setFixedWidth(24)
    s = self.clozeShortcut2 = QShortcut(
        QKeySequence(_("Ctrl+Alt+Shift+C")), self.parentWindow)
    s.connect(s, SIGNAL("activated()"), self.onCloze)
    # fixme: better image names
    b("mail-attachment", self.onAddMedia, _("F3"),
      _("Attach pictures/audio/video (F3)"))
    b("media-record", self.onRecSound, _("F5"), _("Record audio (F5)"))
    b("adv", self.onAdvanced, text=downArrow())
    s = QShortcut(QKeySequence("Ctrl+T, T"), self.widget)
    s.connect(s, SIGNAL("activated()"), self.insertLatex)
    s = QShortcut(QKeySequence("Ctrl+T, E"), self.widget)
    s.connect(s, SIGNAL("activated()"), self.insertLatexEqn)
    s = QShortcut(QKeySequence("Ctrl+T, M"), self.widget)
    s.connect(s, SIGNAL("activated()"), self.insertLatexMathEnv)
    s = QShortcut(QKeySequence("Ctrl+Shift+X"), self.widget)
    s.connect(s, SIGNAL("activated()"), self.onHtmlEdit)
    # tags
    if not isinstance(self.parentWindow, Browser): # let the browser handle this shortcut
        s = QShortcut(QKeySequence("Ctrl+Shift+T"), self.widget)
        s.connect(s, SIGNAL("activated()"), lambda: self.tags.setFocus())
    runHook("setupEditorButtons", self)


Browser.addTags = addTags
Browser.onPreviousCard = onPreviousCard
Browser.onNextCard = onNextCard
Editor.setupButtons = setupButtons