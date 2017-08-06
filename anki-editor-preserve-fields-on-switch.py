# -*- coding: utf-8 -*-

"""
Anki Add-on: Preserve editor fields on note model switch

Copies values of identically named fields over to corresponding fields 
in new note type.

Should be implemented by default in the next Anki release.

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""
 
from anki.hooks import wrap
from aqt.addcards import AddCards

def newOnReset(self, _old, model=None, keep=False):
    # return _old(self, model=None, keep=False)
    oldNote = self.editor.note
    note = self.setupNewNote(set=False)
    modelName = note.model()['name']
    flds = note.model()['flds']
    if oldNote:
        oldModelName = oldNote.model()['name']
        if oldModelName != modelName:
            # model changed
            oldFields = oldNote.keys()
            newFields = note.keys()
            for n, f in enumerate(note.model()['flds']):
                fieldName = f['name']
                try:
                    oldFieldName = oldNote.model()['flds'][n]['name']
                except IndexError:
                    oldFieldName = None
                # copy identical fields
                if fieldName in oldFields:
                    note[fieldName] = oldNote[fieldName]
                # set non-identical fields by field index
                elif oldFieldName and oldFieldName not in newFields:
                    try:
                        note.fields[n] = oldNote.fields[n]
                    except IndexError:
                        pass
        else:
            # model identical
            if not keep:
                self.removeTempNote(oldNote)
            for n in range(len(note.fields)):
                try:
                    if not keep or flds[n]['sticky']:
                        note.fields[n] = oldNote.fields[n]
                    else:
                        note.fields[n] = ""
                except IndexError:
                    break
    self.editor.currentField = 0
    self.editor.setNote(note, focus=True)


AddCards.onReset = wrap(AddCards.onReset, newOnReset, "around")
