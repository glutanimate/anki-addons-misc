# -*- coding: utf-8 -*-

"""
Anki Add-on: Indentation Formatter

Extends Anki's note editing toolbar with an "indent" and "outdent" button
that insert indented paragraphs.

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
""" 

# USER CONFIGURATION START

# Default html tag to apply when there is no
# pre-existing formatting (e.g. div, p, blockquote)
HTML_TAG = "p"

# Whether or not to indent existing tags instead of applying
# the tag above
USE_EXISTING_TAGS = False

# Hotkeys
HOTKEY_INDENT = "Alt+L"
HOTKEY_OUTDENT = "Alt+J"

# Indentation steps in px (default: 40)
INDENTATION_STEP = 40

# USER CONFIGURATION END

from aqt.editor import Editor
from anki.hooks import wrap


js_indent = """
function indent(mode){
    var elm = window.getSelection().focusNode;
    var parent = window.getSelection().focusNode.parentNode;
    if (%(exst)s){
        var isElm = parent.isContentEditable && elm.toString() !== "[object Text]";
        var isParElm = parent.isContentEditable && parent.parentNode.isContentEditable;
    } else {
        var isElm = elm.tagName == "%(tag)s" 
            && parent.isContentEditable;
        var isParElm = parent.tagName == "%(tag)s"
            && parent.parentNode.isContentEditable;
    }
    var newNode = false

    if (mode == "in" && !isElm && !isParElm){
        document.execCommand("formatBlock", false, "%(tag)s");
        var elm = window.getSelection().focusNode;
        if (elm.tagName !== "%(tag)s") {
            elm = elm.parentNode;
        }
        var marginL = %(step)i
        var newNode = true
    } else if (isElm || isParElm) {
        if (!isElm) {
            elm = parent;
        }
        mleft = parseInt(elm.style.marginLeft)
        if (isNaN(mleft)){
            mleft = 0;
        }
        if (mode == "in"){
            var marginL = mleft + %(step)i
        } else {
            var marginL = Math.max(mleft-%(step)i, 0)
        }
    } else {
        return
    }

    if (newNode) {
        elm.style.margin = "0px";
    }
    elm.style.marginLeft = marginL + "px";
    
}
indent("%%s");
saveField('key');
""" % dict(exst=str(USE_EXISTING_TAGS).lower(), tag=HTML_TAG.upper(), 
            step=INDENTATION_STEP)


def onIndent(self, mode):
    self.web.eval(js_indent % mode)

def setupButtons(self):
    self._addButton("OutdentBtn", lambda: self.onIndent("out"),
        text=u"←", tip="Outdent ({})".format(HOTKEY_OUTDENT),
        key=HOTKEY_OUTDENT)
    self._addButton("IndentBtn", lambda: self.onIndent("in"),
        text=u"→", tip="Indent ({})".format(HOTKEY_INDENT),
        key=HOTKEY_INDENT)
         
Editor.onIndent = onIndent
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
