# -*- coding: utf-8 -*-

"""
Anki Add-on: Preserve fields on note model switch

Copies values of identically named fields over to corresponding
fields in new note type.

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

"""
 
from anki.hooks import wrap
from aqt.addcards import AddCards

def newOnReset(self, _old, model=None, keep=False):
  # return _old(self, model=None, keep=False)
  note = self.setupNewNote(set=False)
  modelName = note.model()['name']
  oldNote = self.editor.note
  if oldNote:
    oldModelName = oldNote.model()['name']
  if oldNote and oldModelName != modelName:
    oldFieldList = oldNote.keys()
    newFieldList = note.keys()
    sharedFieldList = [val for val in newFieldList if val in oldFieldList]
    for n, f in enumerate(note.model()['flds']):
      fieldName = f['name']
      try:
        oldFieldName = oldNote.model()['flds'][n]['name']
      except IndexError:
        oldFieldName = None
      if fieldName in oldFieldList:
        note[fieldName] = oldNote[fieldName]
      elif oldFieldName not in sharedFieldList:
        try:
          note.fields[n] = oldNote.fields[n]
        except IndexError:
          pass
      else:
        pass

    self.editor.currentField = 0
    self.editor.setNote(note, focus=True)
    # return _old(self, model=None, keep=False)
  else:
    return _old(self, model=None, keep=False)


AddCards.onReset = wrap(AddCards.onReset, newOnReset, "around")
