# -*- coding: utf-8 -*-

"""
Anki Add-on: Indentation Formatter

Extends Anki's note editing toolbar with an "indent" and "outdent" button
that insert indented paragraphs.

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
""" 

# USER CONFIGURATION START

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

            if (mode == "in" && !isPE && !isParPE){
                document.execCommand("formatBlock", false, "p");
                var elm = window.getSelection().focusNode;
                if (elm.toString() !== "[object HTMLParagraphElement]") {
                    elm = elm.parentNode;
                }
                var margin = %(step)i
            } else if (isPE || isParPE) {
                if (isParPE) {
                    elm = parent;
                }
                mleft = parseInt(elm.style.marginLeft)
                if (mode == "in"){
                    var margin = mleft + %(step)i
                } else {
                    var margin = Math.max(mleft-%(step)i, 0)
                }
            } else {
                return
            }
            elm.setAttribute("style", "margin: 0; margin-left:" + margin + "px;");
        }
        indent("%(mode)s");
        saveField('key');
        """ % dict(mode=mode, step=INDENTATION_STEP))


def setupButtons(self):
    self._addButton("OutdentBtn", lambda: self.onIndent("out"),
        text=u"←", tip="Outdent (Alt+J)", key="Alt+J")
    self._addButton("IndentBtn", lambda: self.onIndent("in"),
        text=u"→", tip="Indent (Alt+L)", key="Alt+L")
         
Editor.onIndent = onIndent
Editor.setupButtons = wrap(Editor.setupButtons, setupButtons)
