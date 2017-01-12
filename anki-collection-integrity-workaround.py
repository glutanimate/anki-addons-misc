 # -*- coding: utf-8 -*-

"""
Anki Add-on: Collection Integrity Workaround

Quick workaround designed to bridge the gap until I figure out
why my collection keeps ending up with notes without cards.

Copyright: (c) Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
import os
import stat

from anki.consts import *
from anki.utils import ids2str, intTime
from anki.lang import _, ngettext

from anki.collection import _Collection

def myFixIntegrity(self):
    "Fix possible problems and rebuild caches."
    problems = []
    no_schema_mod = False
    self.save()
    oldSize = os.stat(self.path)[stat.ST_SIZE]
    if self.db.scalar("pragma integrity_check") != "ok":
        return (_("Collection is corrupt. Please see the manual."), False)
    # note types with a missing model
    ids = self.db.list("""
select id from notes where mid not in """ + ids2str(self.models.ids()))
    if ids:
        problems.append(
            ngettext("Deleted %d note with missing note type.",
                     "Deleted %d notes with missing note type.", len(ids))
                     % len(ids))
        self.remNotes(ids)
    # for each model
    for m in self.models.all():
        for t in m['tmpls']:
            if t['did'] == "None":
                t['did'] = None
                problems.append(_("Fixed AnkiDroid deck override bug."))
                self.models.save(m)
        if m['type'] == MODEL_STD:
            # model with missing req specification
            if 'req' not in m:
                self.models._updateRequired(m)
                problems.append(_("Fixed note type: %s") % m['name'])
            # cards with invalid ordinal
            ids = self.db.list("""
select id from cards where ord not in %s and nid in (
select id from notes where mid = ?)""" %
                               ids2str([t['ord'] for t in m['tmpls']]),
                               m['id'])
            if ids:
                problems.append(
                    ngettext("Deleted %d card with missing template.",
                             "Deleted %d cards with missing template.",
                             len(ids)) % len(ids))
                self.remCards(ids)
        # notes with invalid field count
        ids = []
        for id, flds in self.db.execute(
                "select id, flds from notes where mid = ?", m['id']):
            if (flds.count("\x1f") + 1) != len(m['flds']):
                ids.append(id)
        if ids:
            problems.append(
                ngettext("Deleted %d note with wrong field count.",
                         "Deleted %d notes with wrong field count.",
                         len(ids)) % len(ids))
            self.remNotes(ids)
    # delete any notes with missing cards
    ids = self.db.list("""
select id from notes where id not in (select distinct nid from cards)""")
    if ids:
        cnt = len(ids)
        problems.append(
            ngettext("Deleted %d note with no cards.",
                     "Deleted %d notes with no cards.", cnt) % cnt)
        self._remNotes(ids)
        no_schema_mod = True # don't force one-directional-sync since we didn't
                             # modify the db schema
    # cards with missing notes
    ids = self.db.list("""
select id from cards where nid not in (select id from notes)""")
    if ids:
        cnt = len(ids)
        problems.append(
            ngettext("Deleted %d card with missing note.",
                     "Deleted %d cards with missing note.", cnt) % cnt)
        self.remCards(ids)
    # cards with odue set when it shouldn't be
    ids = self.db.list("""
select id from cards where odue > 0 and (type=1 or queue=2) and not odid""")
    if ids:
        cnt = len(ids)
        problems.append(
            ngettext("Fixed %d card with invalid properties.",
                     "Fixed %d cards with invalid properties.", cnt) % cnt)
        self.db.execute("update cards set odue=0 where id in "+
            ids2str(ids))
    # cards with odid set when not in a dyn deck
    dids = [id for id in self.decks.allIds() if not self.decks.isDyn(id)]
    ids = self.db.list("""
select id from cards where odid > 0 and did in %s""" % ids2str(dids))
    if ids:
        cnt = len(ids)
        problems.append(
            ngettext("Fixed %d card with invalid properties.",
                     "Fixed %d cards with invalid properties.", cnt) % cnt)
        self.db.execute("update cards set odid=0, odue=0 where id in "+
            ids2str(ids))
    # tags
    self.tags.registerNotes()
    # field cache
    for m in self.models.all():
        self.updateFieldCache(self.models.nids(m))
    # new cards can't have a due position > 32 bits
    self.db.execute("""
update cards set due = 1000000, mod = ?, usn = ? where due > 1000000
and queue = 0""", intTime(), self.usn())
    # new card position
    self.conf['nextPos'] = self.db.scalar(
        "select max(due)+1 from cards where type = 0") or 0
    # reviews should have a reasonable due #
    ids = self.db.list(
        "select id from cards where queue = 2 and due > 10000")
    if ids:
        problems.append("Reviews had incorrect due date.")
        self.db.execute(
            "update cards set due = 0, mod = ?, usn = ? where id in %s"
            % ids2str(ids), intTime(), self.usn())
    # and finally, optimize
    self.optimize()
    newSize = os.stat(self.path)[stat.ST_SIZE]
    txt = _("Database rebuilt and optimized.")
    ok = not problems
    problems.append(txt)
    # if any problems were found, force a full sync
    if not ok and not no_schema_mod:
        self.modSchema(check=False)
    self.save()
    return ("\n".join(problems), ok)


_Collection.fixIntegrity = myFixIntegrity