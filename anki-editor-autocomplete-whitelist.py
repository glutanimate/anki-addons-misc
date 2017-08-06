# -*- coding: utf8 -*-
"""
Anki Add-on: Editor Autocomplete Whitelist

This is a slightly modified versions of Editor Autocomplete by
Sartak that switches out the field blacklist with a whitelist.

Copyright: (c) Sartak 2013 <https://github.com/sartak/anki-editor-autocomplete>
           (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from aqt import mw, editor
from aqt.qt import *
from anki.hooks import wrap, addHook
from anki.utils import splitFields, stripHTMLMedia, json
import urllib2

# Modify the following line to add the fields you would like to
# enable autocomplete on (e.g. [ "field1", "field2" ] )
AutocompleteFields = [ ]

def mySetup(self, note, hide=True, focus=False):
    self.prevAutocomplete = ""

    # only initialize the autocompleter on Add Cards not in browser
    if self.note and self.addMode:
        self.web.eval("""
            document.styleSheets[0].addRule('.autocomplete', 'margin: 0.3em 0 1.0em 0; color: blue; text-decoration: underline; cursor: pointer;');

            // every second send the current state over
            setInterval(function () {
                if (currentField) {
                    var r = {
                        text: currentField.innerHTML,
                    };

                    py.run("autocomplete:" + JSON.stringify(r));
                }
            }, 1000);
        """)

def myBridge(self, str, _old=None):
    if str.startswith("autocomplete"):
        (type, jsonText) = str.split(":", 1)
        result = json.loads(jsonText)
        text = self.mungeHTML(result['text'])

        # bail out if the user hasn't actually changed the field
        previous = "%d:%s" % (self.currentField, text)
        if self.prevAutocomplete == previous:
            return
        self.prevAutocomplete = previous

        if text == "" or len(text) > 500 or self.note is None:
            self.web.eval("$('.autocomplete').remove();");
            return

        field = self.note.model()['flds'][self.currentField]

        if not field['name'] in AutocompleteFields:
            field['no_autocomplete'] = True
            return

        # find a value from the same model and field whose
        # prefix is what the user typed so far
        query = "'note:%s' '%s:%s*'" % (
            self.note.model()['name'],
            field['name'],
            text)

        col = self.note.col
        res = col.findCards(query, order=True)

        if len(res) == 0:
            self.web.eval("$('.autocomplete').remove();");
            return

        # pull out the full value
        value = col.getCard(res[0]).note().fields[self.currentField]

        escaped = json.dumps(value)

        self.web.eval("""
            $('.autocomplete').remove();

            if (currentField) {
                $('<div class="autocomplete">' + %s + '</div>').click(function () {
                    currentField.focus();
                    currentField.innerHTML = %s;
                    saveField("key");
                }).insertAfter(currentField)
            }
        """
        % (escaped, escaped))
    else:
        _old(self, str)

# XXX must figure out how to add noAutocomplete checkbox to form
def myLoadField(self, idx):
    fld = self.model['flds'][idx]
    f = self.form
    if 'no_autocomplete' in fld.keys():
        f.noAutocomplete.setChecked(fld['no_autocomplete'])

def mySaveField(self):
    # not initialized yet?
    if self.currentIdx is None:
        return
    idx = self.currentIdx
    fld = self.model['flds'][idx]
    f = self.form
    fld['no_autocomplete'] = f.noAutocomplete.isChecked()

# apply autocomplete on hotkey toggle
def applyAutocomplete(editor):
    editor.web.eval("""
      if ($('.autocomplete').text()) {
        currentField.focus();
        currentField.innerHTML = $('.autocomplete').text();
        saveField("key");
      }
    """)

# assign hotkey
def onSetupButtons(editor):
    # default: Alt + Return
    # insert custom key sequences here:
    t = QShortcut(QKeySequence(Qt.ALT + Qt.Key_Return), editor.parentWindow)
    t.connect(t, SIGNAL("activated()"),
              lambda : applyAutocomplete(editor))

addHook("setupEditorButtons", onSetupButtons)

editor.Editor.bridge = wrap(editor.Editor.bridge, myBridge, 'around')
editor.Editor.setNote = wrap(editor.Editor.setNote, mySetup, 'after')
