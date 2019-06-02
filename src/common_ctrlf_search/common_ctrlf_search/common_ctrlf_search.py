# -*- coding: utf-8 -*-

"""
Anki Add-on: Ctrl+F Search

Allows you to search through your cards in the Reviewer
and in Editor instances (AddCards, EditCurrent, Browser).

Default Hotkeys:

- Invoke search: CTRL + F (Ctrl+Alt+Shift+F in the Browser)
- Close search: Esc
- Next result: F3
- Previous result: Shift+F3

Copyright:  (c) 2017-2019 Glutanimate <https://glutanimate.com/>
            (c) 2019 ijgnd

License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

HOTKEY_SEARCH = "Ctrl+F"
# (Browser shortcut will be prepended with Alt+Shift
# to avoid key conflicts)
HOTKEY_NEXT = "F3"
HOTKEY_PREVIOUS = "Shift+F3"

##############  USER CONFIGURATION END  ##############

from aqt.qt import *
from aqt import mw

from aqt.editor import Editor
from aqt.browser import Browser
from anki.hooks import addHook, wrap


from anki import version
anki20 = version.startswith("2.0")


def load_config_21(config):
    global HOTKEY_SEARCH
    global HOTKEY_SEARCH_BROWSER
    global HOTKEY_NEXT
    global HOTKEY_PREVIOUS
    global BROWSER_CONTEXT_MENU
    HOTKEY_SEARCH = config.get("HOTKEY_SEARCH",False)
    HOTKEY_SEARCH_BROWSER = config.get("HOTKEY_SEARCH_BROWSER",False)
    HOTKEY_NEXT = config.get("HOTKEY_NEXT",False)
    HOTKEY_PREVIOUS = config.get("HOTKEY_PREVIOUS",False)
    BROWSER_CONTEXT_MENU = config.get("Show_in_Browser_Context_menu",False)

if not anki20:
    load_config_21(mw.addonManager.getConfig(__name__))
    mw.addonManager.setConfigUpdatedAction(__name__,load_config_21) 




# Reviewer

# TODO: Explore unifying modifications by switching to a
#       widget similar to the one in the Editor

class ReviewerSearchDock(QObject):
    """Creates a search dock for the main window"""
    def __init__(self, mw):
        QObject.__init__(self)
        self.mw = mw
        self.dock = None
        self.shown = False
        self.widget = None

    def setupWidget(self):
        w = QWidget()
        l = QHBoxLayout()
        w.setLayout(l)
        w.searchEdit = QLineEdit()
        w.searchNxt = QPushButton("∨")
        w.searchPrv = QPushButton("∧")
        for i in (w.searchEdit, w.searchNxt, w.searchPrv):
            l.addWidget(i)
        return w

    def setupDock(self):
        dock = QDockWidget("", mw)
        dock.setObjectName("SearchDock")
        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        dock.setFeatures(QDockWidget.DockWidgetClosable)
        dock.setTitleBarWidget(QWidget(dock))
        return dock

    def setupEvents(self):
        self.widget.searchNxt.clicked.connect(
            lambda _: self.findText(0))
        self.widget.searchPrv.clicked.connect(
            lambda _: self.findText(1))
        t = QShortcut(QKeySequence("Esc"), self.dock)
        t.activated.connect(self.hide)
        t = QShortcut(QKeySequence("Return"), self.dock)
        t.activated.connect(self.widget.searchNxt.animateClick)
        t = QShortcut(QKeySequence("Shift+Return"), self.dock)
        t.activated.connect(self.widget.searchNxt.animateClick)
        if HOTKEY_NEXT:
            t = QShortcut(QKeySequence(HOTKEY_NEXT), mw)
            t.activated.connect(self.widget.searchNxt.animateClick)
        if HOTKEY_PREVIOUS:
            t = QShortcut(QKeySequence(HOTKEY_PREVIOUS), mw)
            t.activated.connect(self.widget.searchPrv.animateClick)
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.findText(0))
        self.widget.searchEdit.textEdited.connect(lambda: self.timer.start())

    def showOrFocus(self):
        if not self.shown:
            self.show()
        else:
            self.widget.searchEdit.setFocus()
            self.widget.searchEdit.selectAll()

    def show(self):
        if not self.dock:
            self.dock = self.setupDock()
            self.widget = self.setupWidget()
            self.dock.setWidget(self.widget)
            self.setupEvents()
            mw.addDockWidget(Qt.BottomDockWidgetArea, self.dock)
        self.dock.show()
        self.widget.searchEdit.setFocus()
        self.widget.searchEdit.selectAll()
        self.shown = True

    def hide(self):
        if self.dock:
            self.dock.hide()
            self.shown = False

    def toggle(self):
        if self.shown:
            self.hide()
        else:
            self.show()

    def findText(self, direction):
        text = self.widget.searchEdit.text()
        if anki20:
            options = QWebPage.FindWrapsAroundDocument 
            if direction == 1:
                options = (options | QWebPage.FindBackward)
            mw.web.findText(text, options)
        if not anki20:
            #for an explanation see below at EditorSearchWidget.findText 
            if direction == 1:
                options = ( QWebEnginePage.FindBackward)
                mw.web.findText(text, options)
            else:
                mw.web.findText(text)  

dock = ReviewerSearchDock(mw)
if HOTKEY_SEARCH:
    shortcut = QShortcut(QKeySequence(HOTKEY_SEARCH), mw)
    shortcut.activated.connect(dock.showOrFocus)


# Editor

# We have to create a widget for the Editor because docks
# are only supported for QMainWindows

class EditorSearchWidget(QWidget):
    """Creates a search widget for the Editor"""
    def __init__(self, editor):
        QWidget.__init__(self)
        self.editor = editor
        self.setupWidgets()
        self.setupEvents()
        QWidget.hide(self)

    def setupWidgets(self):
        l = QHBoxLayout()
        self.setLayout(l)
        self.searchEdit = QLineEdit()
        self.searchNxt = QPushButton("∨")
        self.searchPrv = QPushButton("∧")
        for i in (self.searchEdit, self.searchNxt, self.searchPrv):
            l.addWidget(i)

    def setupEvents(self):
        self.searchNxt.clicked.connect(
            lambda _: self.findText(0))
        self.searchPrv.clicked.connect(
            lambda _: self.findText(1))
        t = QShortcut(QKeySequence("Esc"), self)
        t.activated.connect(self.hide)
        t = QShortcut(QKeySequence("Return"), self)
        t.activated.connect(self.searchNxt.animateClick)
        t = QShortcut(QKeySequence("Shift+Return"), self)
        t.activated.connect(self.searchNxt.animateClick)
        if HOTKEY_NEXT:
            t = QShortcut(QKeySequence(HOTKEY_NEXT), self)
            t.activated.connect(self.searchNxt.animateClick)
        if HOTKEY_PREVIOUS:
            t = QShortcut(QKeySequence(HOTKEY_PREVIOUS), self)
            t.activated.connect(self.searchPrv.animateClick)
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.findText(0))
        self.searchEdit.textEdited.connect(lambda: self.timer.start())

    def showOrFocus(self):
        if not self.isVisible():
            self.show()
        self.searchEdit.setFocus()
        self.searchEdit.selectAll()

    def hide(self):
        self.editor.web.setFocus()
        # if called from the Browser menu no field is focused
        if self.editor.currentField: 
            self.editor.web.eval("focusField(%d);" % self.editor.currentField)
        QWidget.hide(self)

    def findText(self, direction):
        text = self.searchEdit.text()
        if anki20:
            options = QWebPage.FindWrapsAroundDocument 
            if direction == 1:
                options = (options | QWebPage.FindBackward)
            self.editor.web.findText(text, options)
        if not anki20:
            # .FindWrapsAroundDocument doesn't seem to be 
            # available anymore (nor is it necessary), see 
            # https://doc.qt.io/qt-5/qwebenginepage.html#FindFlag-enum 
            # vs https://doc.qt.io/archives/qt-5.5/qwebpage.html 
            if direction == 1:
                options = ( QWebEnginePage.FindBackward)
                self.editor.web.findText(text,options)
            else:
                self.editor.web.findText(text)            

def onSetupTags(self):
    """Add search widget after tag widget"""
    self.search = EditorSearchWidget(self)
    self.outerLayout.addWidget(self.search)
Editor.setupTags = wrap(Editor.setupTags, onSetupTags, "after")


if anki20:
    def onSetupButtons(self):
        """Set-up hotkeys"""
        if isinstance(self.parentWindow, Browser):
            hotkey = "Alt+Shift+{}".format(HOTKEY_SEARCH)
        else:
            hotkey = HOTKEY_SEARCH
        shortcut = QShortcut(QKeySequence(hotkey), self.parentWindow)
        shortcut.activated.connect(lambda: self.search.showOrFocus())
    addHook("setupEditorButtons", onSetupButtons)


if not anki20:
    def ctrlfsearch_editor_helper(editor):
        """self.search.showOrFocus is setup after the setupEditorShortcuts is run. Without this helper I would get an error"""
        editor.search.showOrFocus()
    Editor.ctrlfsearch_editor_helper = ctrlfsearch_editor_helper


    #### without Browser Menu entry
    # def SetupShortcuts21(cuts, self):
    #     if isinstance(self.parentWindow, Browser) and HOTKEY_SEARCH_BROWSER:
    #         hotkey = HOTKEY_SEARCH_BROWSER
    #     elif HOTKEY_SEARCH:
    #         hotkey = HOTKEY_SEARCH  
    #     cuts.append( ( hotkey, self.ctrlfsearch_editor_helper )  )
    # addHook("setupEditorShortcuts", SetupShortcuts21)


    #### with Browser Menu entry
    def SetupShortcutsNotBrowser21(cuts, self):
        if HOTKEY_SEARCH and not isinstance(self.parentWindow, Browser):  
            #Add or EditCurrent
            hotkey = HOTKEY_SEARCH
            cuts.append((hotkey, self.ctrlfsearch_editor_helper))
    addHook("setupEditorShortcuts", SetupShortcutsNotBrowser21)

    def setupMenu(browser):
        global myaction
        myaction = QAction(browser)
        myaction.setText("Search through the selected Note (set at the bottom)")
        if HOTKEY_SEARCH_BROWSER:
            myaction.setShortcut(QKeySequence(HOTKEY_SEARCH_BROWSER))
        myaction.triggered.connect(lambda : ctrlfsearch_editor_helper(browser.editor))
        browser.form.menuEdit.addAction(myaction)
    addHook("browser.setupMenus", setupMenu)

    def add_to_table_context_menu(browser, menu):
        menu.addAction(myaction)
    if BROWSER_CONTEXT_MENU:
        addHook("browser.onContextMenu", add_to_table_context_menu)
