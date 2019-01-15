# -*- coding: utf-8 -*-

"""
Anki Add-on: Insert Randomized List

Inserts an unordered list with the 'shuffle' CSS class. 

This can be used to randomize list items when coupled with
a special card template.

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

############## USER CONFIGURATION START ##############

# These settings only apply to Anki 2.0. For Anki 2.1 please use
# Anki's built-in add-on configuration menu

HOTKEY_TOGGLE_LIST = "Alt+Shift+L"

##############  USER CONFIGURATION END  ##############

from aqt import editor, mw
from anki.hooks import wrap, addHook

from anki import version

ANKI21 = version.startswith("2.1")

if ANKI21:
    config = mw.addonManager.getConfig(__name__)
    HOTKEY_TOGGLE_LIST = config["hotkeyToggleList"]

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


def setupButtons20(self):
    self._addButton("randUlBtn", self.toggleRandUl,
                    text="RL",
                    tip="Insert randomized unordered list ({})".format(
                        HOTKEY_TOGGLE_LIST),
                    key=HOTKEY_TOGGLE_LIST)


def setupButtons21(btns, editor):
    btn = editor.addButton(None, "randUlBtn", toggleRandUl,
                           label="RL", keys=HOTKEY_TOGGLE_LIST,
                           tip="Insert randomized unordered list ({})".format(
                               HOTKEY_TOGGLE_LIST))
    btns.append(btn)
    return btns

editor._html = editor._html + editor_style


if not ANKI21:
    editor.Editor.toggleRandUl = toggleRandUl
    editor.Editor.setupButtons = wrap(
        editor.Editor.setupButtons, setupButtons20)
else:
    addHook("setupEditorButtons", setupButtons21)
