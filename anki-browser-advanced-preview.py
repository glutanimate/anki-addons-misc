 # -*- coding: utf-8 -*-

"""
Anki Add-on: Advanced Previewer

Extends the card previewer with the following features:

- Preview multiple cards at the same time
- Option to show both the front and back of your cards
- Customizable preview content styling (by editing the source code)

Copyright: (c) Glutanimate 2016
Commissioned by: Alexander A.

License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

# import modules this add-on depends on
import re

import aqt
from aqt.qt import *
from aqt.browser import Browser
from aqt.webview import AnkiWebView

from aqt.utils import getBase, mungeQA, openLink, saveGeom, restoreGeom
from anki.hooks import wrap
from anki.sound import clearAudioQueue, playFromText, play
from anki.js import browserSel

# support for JS Booster add-on
try:
    from jsbooster.location_hack import getBaseUrlText, stdHtmlWithBaseUrl
    preview_jsbooster = True
except ImportError:
    preview_jsbooster = False


# General preview window styling
preview_css = """
body{
    // body css here
}
"""

# Styling used when previewing multiple cards
multi_preview_css = """
/*Card styling*/
.card{
    margin-top: 0.5em;
    margin-bottom: 0.5em;
    padding-top: 0.5em;
    padding-bottom: 0.5em;
    border-style: solid;
    border-color: #EFEFEF;
    cursor: pointer;
    background-color: #FFFFFF;
}

/*Styling to apply when hovering over cards*/
.card:hover{
    background-color: #F9FFE0;
}

/*Styling to apply when card is selected*/
.card.active{
    background-color: #EFEFEF;
}
"""

# JS function that applies active styling to selected card
multi_preview_js = """
function toggleActive(elm) {
    otherElms = document.getElementsByClassName("card");
    for (var i = 0; i < otherElms.length; i++) {
        otherElms[i].classList.remove("active");
    }
    elm.classList.add("active")
}
"""

def onTogglePreview(self):
    # only used to set the link handler after loading the preview window
    # (required in order to be compatible with "Replay Buttons on Card")
    if self._previewWindow:
        self._previewWeb.setLinkHandler(self._previewLinkHandler)

def openPreview(self):
    """Creates and launches the preview window"""
    # Initialize a number of variables used by the add-on:
    try:
        self._previewBoth
    except AttributeError:
        # controls the default preview mode
        # Set to True and "answer" to show front and back by default
        self._previewBoth = False
        self._previewState = "question"
    self._previewCurr = [] # list of currently previewed card ids
    self._previewLinkClicked = False # indicates whether user clicked on card in preview
    # Set up window and layout:
    c = self.connect
    self._previewWindow = QDialog(None, Qt.Window)
    self._previewWindow.setWindowTitle(_("Preview"))
    c(self._previewWindow, SIGNAL("finished(int)"), self._onPreviewFinished)
    vbox = QVBoxLayout()
    vbox.setMargin(0)
    self._previewWeb = AnkiWebView()
    self._previewWeb.setLinkHandler(self._previewLinkHandler) # set up custom link handler
    vbox.addWidget(self._previewWeb)
    bbox = QDialogButtonBox()
    # Set up buttons:
    self._previewToggle = bbox.addButton(_("Show Both Sides"), QDialogButtonBox.ActionRole)
    self._previewToggle.setCheckable(True)
    self._previewToggle.setChecked(self._previewBoth)
    self._previewToggle.setAutoDefault(False)
    self._previewToggle.setShortcut(QKeySequence("B"))
    self._previewToggle.setToolTip(_("Shortcut key: %s" % "B"))
    self._previewReplay = bbox.addButton(_("Replay Audio"), QDialogButtonBox.ActionRole)
    self._previewReplay.setAutoDefault(False)
    self._previewReplay.setShortcut(QKeySequence("R"))
    self._previewReplay.setToolTip(_("Shortcut key: %s" % "R"))
    self._previewPrev = bbox.addButton("<", QDialogButtonBox.ActionRole)
    self._previewPrev.setAutoDefault(False)
    self._previewPrev.setShortcut(QKeySequence("Left"))
    self._previewPrev.setToolTip(_("Shortcut key: Right arrow"))
    self._previewNext = bbox.addButton(">", QDialogButtonBox.ActionRole)
    self._previewNext.setToolTip(_("Shortcut key: Right arrow or Enter"))
    self._previewNext.setAutoDefault(True)
    self._previewNext.setShortcut(QKeySequence("Right"))
    c(self._previewToggle, SIGNAL("clicked()"), self._onPreviewModeToggle)
    c(self._previewPrev, SIGNAL("clicked()"), self._onPreviewPrev)
    c(self._previewNext, SIGNAL("clicked()"), self._onPreviewNext)
    c(self._previewReplay, SIGNAL("clicked()"), self._onReplayAudio)
    # Set up window and launch preview
    vbox.addWidget(bbox)
    self._previewWindow.setLayout(vbox)
    restoreGeom(self._previewWindow, "preview")
    self._previewWindow.show()
    self._renderPreview(True)

def onPreviewModeToggle(self):
    """Switches between preview modes ('front' vs 'back and front')"""
    self._previewBoth = self._previewToggle.isChecked()
    if self._previewBoth:
        self._previewState = "answer"
    else:
        self._previewState = "question"
    self._renderPreview()

def previewLinkHandler(self, url):
    """Executed when clicking on a card"""
    if url.startswith("focus"):
        # bring card into focus
        cid = int(url.split()[1])
        self._previewLinkClicked = True
        self.focusCid(cid)
    elif url.startswith("tagdeck"):
        # support for anki-reviewer-clickable-tags
        tag = url.split()[1]
        deck = self.mw.col.decks.name(self.card.did)
        search = 'tag:{0} deck:"{1}"'.format(tag, deck)
        browser = aqt.dialogs.open("Browser", self.mw)
        # not using setfilter because it grabs keyboard modifiers
        browser.form.searchEdit.lineEdit().setText(search)
        browser.onSearch()
    elif url.startswith("ankiplay"):
        # support for 'Replay Buttons on Card' add-on
        clearAudioQueue() # stop current playback
        play(url[8:])
    else:
        # handle regular links with the default link handler
        openLink(url)

def scrollToPreview(self, cid):
    """Adjusts preview window scrolling position to show supplied card"""
    self._previewWeb.eval("""
        const elm = document.getElementById('%i');
        const elmRect = elm.getBoundingClientRect();
        const absElmTop = elmRect.top + window.pageYOffset;
        const elmHeight = elmRect.top - elmRect.bottom
        const middle = absElmTop - (window.innerHeight/2) - (elmHeight/2);
        window.scrollTo(0, middle);
        toggleActive(elm);
        """ % cid)

def renderPreview(self, cardChanged=False):
    """Generates the preview window content"""
    if not self._previewWindow:
        return
    cids = self.selectedCards()
    oldfocus = None
    multi = len(cids) > 1 # multiple cards selected?
    if not cids:
        txt = "Please select one or more cards"
        self._previewWeb.stdHtml(txt)
        self._updatePreviewButtons()
        return
    if cardChanged and not self._previewBoth:
        self._previewState = "question"
    if not multi and cids[0] in self._previewCurr:
        # moved focus to another previously selected card
        if cardChanged:
            # focus changed without any edits
            if not self._previewLinkClicked and len(self._previewCurr) > 1:
                # only scroll when coming from browser and multiple cards shown
                self.scrollToPreview(cids[0])
            self._previewLinkClicked = False
            return
        else:
            # focus changed on card edit
            oldfocus = cids[0]
            cids = self._previewCurr
            multi = len(cids) > 1   
    txt = ""
    css = self.mw.reviewer._styles() + preview_css
    html = u"""<div id="{0}" class="card card{1}">{2}</div>"""
    # RegEx to remove multiple imports of external JS/CSS (JS-Booster-specific)
    jspattern = r"""(<script type=".*" src|<style>@import).*(</script>|</style>)"""
    scriptre = re.compile(jspattern)
    js = browserSel
    if multi:
        # only apply custom CSS and JS when previewing multiple cards
        html = u"""<div id="{0}" onclick="py.link('focus {0}');toggleActive(this);" \
               class="card card{1}">{2}</div>"""
        css += multi_preview_css
        js += multi_preview_js
    for idx, cid in enumerate(cids):
        # add contents of each card to preview
        c = self.col.getCard(cid)
        if self._previewState == "answer":
            ctxt = c.a()
        else:
            ctxt = c.q()
        # Remove subsequent imports of external JS/CSS
        if idx >= 1:
            ctxt = scriptre.sub("", ctxt)
        txt += html.format(cid, c.ord+1, ctxt)
    txt = re.sub("\[\[type:[^]]+\]\]", "", txt)
    ti = lambda x: x
    base = getBase(self.mw.col)
    if preview_jsbooster:
        # JS Booster available
        baseUrlText = getBaseUrlText(self.mw.col) + "__previewer__.html"
        stdHtmlWithBaseUrl(self._previewWeb,
            ti(mungeQA(self.col, txt)), baseUrlText,
            css, head=base, js=browserSel + multi_preview_js)
    else:
        # fall back to default
        self._previewWeb.stdHtml(
            ti(mungeQA(self.col, txt)), css, head=base, js=js)
    if oldfocus and multi:
        self.scrollToPreview(oldfocus)
    self._previewCurr = cids
    if multi:
        self._previewPrev.setEnabled(False)
        self._previewNext.setEnabled(False)
    else:
        self._updatePreviewButtons()
    clearAudioQueue()
    if not multi and self.mw.reviewer.autoplay(c):
        playFromText(txt)

# Monkey patch Anki's default preview methods
Browser.onTogglePreview = wrap(Browser.onTogglePreview, onTogglePreview)
Browser._renderPreview = renderPreview
Browser._onPreviewModeToggle = onPreviewModeToggle
Browser._previewLinkHandler = previewLinkHandler
Browser.scrollToPreview = scrollToPreview
Browser._openPreview = openPreview