# -*- coding: utf-8 -*-

"""
Anki Add-on: Replace Linebreaks in Clipboard or Selection

Adds hotkeys that remove linebreaks in the clipboard or
currently selected text.

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

# Do not modify the following line:
from __future__ import unicode_literals

############## USER CONFIGURATION START ##############

# KEY ASSIGNMENTS

PASTE_HOTKEY = "Alt+P" # Default: Alt+P
EDIT_SELECTION_HOTKEY = "Alt+Shift+P" # Default: Alt+Shift+P

# OPTIONS

# try to preserve paragraphs (not 100% exact):
PRESERVE_PARAGRAPHS = True # Default: True
# confirm actions with tooltips
TOOLTIP = True # Default: True

##############  USER CONFIGURATION END  ##############

import re

from aqt.qt import *
from aqt.editor import Editor
from aqt.utils import tooltip

from anki.hooks import wrap
from anki import json

if PRESERVE_PARAGRAPHS:
    re_lb_open = "(<div>|<br>|<br\/>|<br \/>)"
    re_lb_close = "(<\/div>)"
else:
    re_lb_open = "(<div>|<p>|<br>|<br\/>|<br \/>)"
    re_lb_close = "(<\/div>|<\/p>)"

js_linebreak_remove = """
function getSelectionHtml() {
    // Based on an SO answer by Tim Down
    var html = "";
    if (typeof window.getSelection != "undefined") {
        var sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            html = document.selection.createRange().htmlText;
        }
    }
    return html;
}
if (typeof window.getSelection != "undefined") {
    // get selected HTML
    var sel = getSelectionHtml();
    // replace linebreak tags
    var sel = sel.replace(/%s/g, " ")
    var sel = sel.replace(/%s/g, "")
    document.execCommand('insertHTML', false, sel);
    saveField('key');
}
""" % (re_lb_open, re_lb_close)


def pasteWithoutLinebreaks(self):
    """Remove linebreaks from clipboard and paste"""
    mime = self.web.mungeClip(mode=QClipboard.Clipboard)
    html = mime.html()
    text = mime.text()

    if not(text or html):
        return
    
    if html:
        content = re.sub(re_lb_open, " ", html)
        content = re.sub(re_lb_close, "", content)
    else:
        if PRESERVE_PARAGRAPHS:
            # remove EOL hyphens:
            content = re.sub(r"-\n(?!\n)", "", text) 
            # skip ends of sentences:
            content = re.sub(r"(?<!\.|\!|\:)\n(?!\n)", " ", content)
            # strip extraneous linebreaks while rejoining with <br> tags
            content = "<br />".join(i.strip() for i in content.split("\n"))
        else:
            content = content.replace("\n", " ")

    self.web.eval("""
        var pasteHTML = function(html) {
            setFormat("inserthtml", html);
        };
        var filterHTML = function(html) {
            // wrap it in <top> as we aren't allowed to change top level elements
            var top = $.parseHTML("<ankitop>" + html + "</ankitop>")[0];
            filterNode(top);
            var outHtml = top.innerHTML;
            // get rid of nbsp
            outHtml = outHtml.replace(/&nbsp;/ig, " ");
            return outHtml;
        };
        pasteHTML(%s);
        """ % json.dumps(content))

    if TOOLTIP:
        tooltip("Pasting without linebreaks", period=500)


def removeLinebreaksInSelection(self):
    """Remove linebreaks from selected text"""
    # here we have to operate on HTML tags instead of newlines
    self.web.eval(js_linebreak_remove)
    if TOOLTIP:
        tooltip("Removing linebreaks", period=500)


def setupButtons(self):
    """Add hotkeys to editor"""
    t = QShortcut(QKeySequence(PASTE_HOTKEY), self.parentWindow)
    t.activated.connect(self.pasteWithoutLinebreaks)
    t = QShortcut(QKeySequence(EDIT_SELECTION_HOTKEY), self.parentWindow)
    t.activated.connect(self.removeLinebreaksInSelection)

# Hooks

Editor.removeLinebreaksInSelection = removeLinebreaksInSelection
Editor.pasteWithoutLinebreaks = pasteWithoutLinebreaks
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
