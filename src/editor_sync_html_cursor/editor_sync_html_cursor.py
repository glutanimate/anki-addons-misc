# -*- coding: utf-8 -*-
"""
Anki Add-on: Sync Cursor Position to HTML Editor

Will sync cursor position between current field and HTML Editor
(CTRL+SHIFT+X)

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

import re
from BeautifulSoup import BeautifulSoup

import aqt
from aqt.qt import *
from aqt import editor

from aqt.utils import openHelp

####### USER CONFIGURATION START #######

# HTML Editor window dimensions in px:
DIALOG_SIZE = (800,480)

# Whether or not to add cosmetic newlines between HTML tags
# that correspond to linebreaks in the rendered text
# (disabled by default because AnkiDroid interprets these as
# actual linebreaks)
COSMETIC_NEWLINES = False


####### USER CONFIGURATION END #######

# remove second caretToEnd call to support custom cursor positioning:
html_override = """
<script>
function onFocus(elem) {
    currentField = elem;
    py.run("focus:" + currentField.id.substring(1));
    // don't adjust cursor on mouse clicks
    if (mouseDown) { return; }
    caretToEnd();
    // scroll if bottom of element off the screen
    function pos(obj) {
        var cur = 0;
        do {
          cur += obj.offsetTop;
         } while (obj = obj.offsetParent);
        return cur;
    }
    var y = pos(elem);
    if ((window.pageYOffset+window.innerHeight) < (y+elem.offsetHeight) ||
        window.pageYOffset > y) {
        window.scroll(0,y+elem.offsetHeight-window.innerHeight);
    }
}
</script>
"""

# based on SO posts by Tim Down / B T (http://stackoverflow.com/q/16095155)
js_move_cursor = """
function findHiddenCharacters(node, beforeCaretIndex) {
    var hiddenCharacters = 0
    var lastCharWasWhiteSpace=true
    for(var n=0; n-hiddenCharacters<beforeCaretIndex &&n<node.length; n++) {
        if([' ','\\n','\\t','\\r'].indexOf(node.textContent[n]) !== -1) {
            if(lastCharWasWhiteSpace)
                hiddenCharacters++
            else
                lastCharWasWhiteSpace = true
        } else {
            lastCharWasWhiteSpace = false   
        }
    }

    return hiddenCharacters
}

var setSelectionByCharacterOffsets = null;

if (window.getSelection && document.createRange) {
    setSelectionByCharacterOffsets = function(containerEl, position) {
        var charIndex = 0, range = document.createRange();
        range.setStart(containerEl, 0);
        range.collapse(true);
        var nodeStack = [containerEl], node, foundStart = false, stop = false;

        while (!stop && (node = nodeStack.pop())) {
            if (node.nodeType == 3) {
                var hiddenCharacters = findHiddenCharacters(node, node.length)
                var nextCharIndex = charIndex + node.length - hiddenCharacters;

                if (position >= charIndex && position <= nextCharIndex) {
                    var nodeIndex = position - charIndex
                    var hiddenCharactersBeforeStart = findHiddenCharacters(node, nodeIndex)
                    range.setStart(node, nodeIndex + hiddenCharactersBeforeStart );
                    range.setEnd(node, nodeIndex + hiddenCharactersBeforeStart);
                    stop = true;
                }
                charIndex = nextCharIndex;
            } else {
                var i = node.childNodes.length;
                while (i--) {
                    nodeStack.push(node.childNodes[i]);
                }
            }
        }

        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }
} else if (document.selection) {
    setSelectionByCharacterOffsets = function(containerEl, start, end) {
        var textRange = document.body.createTextRange();
        textRange.moveToElementText(containerEl);
        textRange.collapse(true);
        textRange.moveEnd("character", end);
        textRange.moveStart("character", start);
        textRange.select();
    };
}
setSelectionByCharacterOffsets(currentField, %s)
"""


def myHtmlEdit(self):
    self.saveNow()
    # Get field cursor position by using temporary marker
    html = self.web.page().mainFrame().evaluateJavaScript("""
        // need to collapse selection to prevent losing selected text:
        window.getSelection().collapseToStart();
        // use placeholder to mark current cursor position
        document.execCommand("insertText", false, "|-|c|-|");
        function retHtml(){return currentField.innerHTML};
        retHtml();
        """)
    if html:
        self.web.eval("""
            currentField.innerHTML = currentField.innerHTML.replace("|-|c|-|", "")
            saveField("key");
            """)
        pos = len(html.split("|-|c|-|")[0])

        txt = html.replace("|-|c|-|", "")
        if COSMETIC_NEWLINES:
            txt = re.sub(r"(</(div|p|br|li|ul|ol|blockquote)>)([^\n])", r"\1\n\3", txt)
    else:
        txt = self.note.fields[self.currentField]
        pos = len(txt)

    d = QDialog(self.widget)
    form = aqt.forms.edithtml.Ui_Dialog()
    form.setupUi(d)
    d.resize(*DIALOG_SIZE)
    form.buttonBox.helpRequested.connect(lambda: openHelp("editor"))
    form.textEdit.setPlainText(txt)
    cursor = form.textEdit.textCursor()
    cursor.setPosition(pos)
    form.textEdit.setTextCursor(cursor)
    d.exec_()

    # Get html cursor position
    curpos = form.textEdit.textCursor().position()
    html = form.textEdit.toPlainText()
    before, after = html[:curpos], html[curpos:]

    # Move cursor out of tag
    dlms = {"<": ">", "&": ";"}
    dlm = None
    for idx, c in enumerate(before):
        if dlm and c == dlms[dlm]:
            dlm = None
        elif c in dlms:
            dlm = c
    if dlm:
        tag_snips = before.split(dlm)
        tag_pre = dlm.join(tag_snips[0:-1])
        tag_post = tag_snips[-1]
        before = tag_pre
        after = dlm + tag_post + after

    html = before + "|-|c|-|" + after
    
    # filter html through beautifulsoup so we can strip out things like a
    # leading </div>
    html = unicode(BeautifulSoup(html))
    self.note.fields[self.currentField] = html
    self.loadNote()
    # focus field so it's saved
    self.web.setFocus()
    self.web.eval("focusField(%d);" % self.currentField)
    # Get cursor position in rendered text via marker
    text = self.web.page().mainFrame().evaluateJavaScript("""
        function retTxt(){return currentField.innerText};
        retTxt();
        """)
    pos = len(text.replace("\n", "").split("|-|c|-|")[0])
    # Remove temporary marker
    self.web.eval("""
        currentField.innerHTML = currentField.innerHTML.replace("|-|c|-|", "");
        saveField("key");
    """)
    # Move cursor to new position
    self.web.page().mainFrame().evaluateJavaScript(js_move_cursor % pos)


editor._html = editor._html + html_override
editor.Editor.onHtmlEdit = myHtmlEdit