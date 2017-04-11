# -*- coding: utf-8 -*-

"""
Anki Add-on: Indentation Formatter

Extends Anki's note editing toolbar with an "indent" and "outdent" button
that insert indented paragraphs.

Copyright: (c) Glutanimate 2017
License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
""" 

# USER CONFIGURATION START

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
            var isPE = elm.toString() == "[object HTMLParagraphElement]"
            var isParPE = parent.toString() == "[object HTMLParagraphElement]"
            var newNode = false

            if (mode == "in" && !isPE && !isParPE){
                document.execCommand("formatBlock", false, "p");
                var elm = window.getSelection().focusNode;
                if (elm.toString() !== "[object HTMLParagraphElement]") {
                    elm = elm.parentNode;
                }
                var marginL = %(step)i
                var newNode = true
            } else if (isPE || isParPE) {
                if (isParPE) {
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
        """ % dict(mode=mode, step=INDENTATION_STEP))


def setupButtons(self):
    self._addButton("OutdentBtn", lambda: self.onIndent("out"),
        text=u"←", tip="Outdent ({})".format(HOTKEY_OUTDENT),
        key=HOTKEY_OUTDENT)
    self._addButton("IndentBtn", lambda: self.onIndent("in"),
        text=u"→", tip="Indent ({})".format(HOTKEY_INDENT),
        key=HOTKEY_INDENT)
         
Editor.onIndent = onIndent
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
