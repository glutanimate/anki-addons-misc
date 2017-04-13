# -*- coding: utf-8 -*-

"""
Anki Add-on: Indentation Formatter

Extends Anki's note editing toolbar with an "indent" and "outdent" button
that insert indented paragraphs.

Copyright: (c) Glutanimate 2017
License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
""" 

# USER CONFIGURATION START

# default html tag to apply when there is no
# pre-existing formatting (e.g. div, p, blockquote)
HTML_TAG = "p"

# hotkeys
HOTKEY_INDENT = "Alt+L"
HOTKEY_OUTDENT = "Alt+J"

# indentation steps in px (default: 40)
INDENTATION_STEP = 40

# USER CONFIGURATION END

from aqt.editor import Editor
from anki.hooks import wrap

def onIndent(self, mode):
    self.web.eval("""
        function indent(mode){
            var elm = window.getSelection().focusNode;
            var parent = window.getSelection().focusNode.parentNode;
            var isElm = parent.toString() !== "[object HTMLTableCellElement]" && elm.toString() !== "[object Text]";
            var isParElm = parent.toString() !== "[object HTMLTableCellElement]" && parent.parentNode.toString() !== "[object HTMLTableCellElement]";
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
        indent("%(mode)s");
        saveField('key');
        """ % dict(tag=HTML_TAG.upper(), mode=mode, step=INDENTATION_STEP))


def setupButtons(self):
    self._addButton("OutdentBtn", lambda: self.onIndent("out"),
        text=u"←", tip="Outdent ({})".format(HOTKEY_OUTDENT),
        key=HOTKEY_OUTDENT)
    self._addButton("IndentBtn", lambda: self.onIndent("in"),
        text=u"→", tip="Indent ({})".format(HOTKEY_INDENT),
        key=HOTKEY_INDENT)
         
Editor.onIndent = onIndent
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
