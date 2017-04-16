# -*- coding: utf-8 -*-

"""
Anki Add-on: Insert Randomized List

Inserts an unordered list with the 'shuffle' CSS class. 

This can be used to randomize list items when coupled with
a special card template.

Copyright: (c) Glutanimate 2017
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

######## USER CONFIGURATION START ########

HOTKEY_TOGGLE_LIST = "Alt+Shift+L"

######## USER CONFIGURATION END ########

from aqt.qt import *

from aqt import editor
from anki.hooks import wrap

editor_style = """
<style>
ul.shuffle{
    background-color: yellow;
}
</style>
"""

def toggleRandUl(self):
    self.web.eval("""
        document.execCommand('insertUnorderedList');
        var ulElem = window.getSelection().focusNode.parentNode;
        if (ulElem !== null) {
            var setAttrs = true;
            while (ulElem.toString() !== "[object HTMLUListElement]") {
                ulElem = ulElem.parentNode;
                if (ulElem === null) {
                    setAttrs = false;
                    break;
                }
            }
            if (setAttrs) {
                ulElem.style.marginLeft = "20px";
                ulElem.className = "shuffle"
            }
        }
    """)

def setupButtons(self):
    self._addButton("randUlBtn", self.toggleRandUl,
        text=u"RL", 
        tip="Insert randomized unordered list ({})".format(HOTKEY_TOGGLE_LIST),
        key=HOTKEY_TOGGLE_LIST)


editor._html = editor._html + editor_style
editor.Editor.toggleRandUl = toggleRandUl
editor.Editor.setupButtons = wrap(editor.Editor.setupButtons, setupButtons)