 # -*- coding: utf-8 -*-

"""
Anki Add-on: Browser Sidebar Tweaks

Various customizations and adjustments to the filter tree sidebar in Anki's card browser.

List of changes:

- enabled Hierarchical Tags add-on
  - modified to fix issue where searches would yield results outside of the hierarchy due to
    regex nature of search
- enabled 'Collapse searches by default'
- trimmed sidebar items down
  - placed all note types under a single tree node
  - placed some of the less-used system filters and a 'Status' node
- customized tag tree sort order
  - items with leading _ are sorted first
  - items with leading . are sorted last
  - items with leading capital letter are sorted after leading _, but before the rest

Contains code found in the following add-ons:

- Hierarchical Tags add-on by Patice Neff (https://github.com/pneff/anki-hierarchical-tags)
- Tag Tweaks add-on by Arthaey Angosii (https://github.com/Arthaey/anki-tag-tweaks)

Copyright: (c) Glutanimate 2016-2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

from PyQt4.QtGui import *

from operator import  itemgetter
from anki.lang import ngettext

from aqt.qt import *
from aqt.browser import Browser
from anki.hooks import wrap


# Separator used between hierarchies
TAGS_SEPARATOR = '::'

# custom sort function to override tag order
def sortFn(s):
    # sort tags starting with . last
    if s.startswith('.'):
      return u'\uffff' + s
    # sort tags starting with _ first
    elif s.startswith('_'):
      return u'\u0000' + s
    # then tags starting with #
    elif s.startswith('#'):
      return u'\u0001' + s
    # tags starting with a capital letter come next
    elif s[0].isupper():
      return u'\u0002' + s
    # everything else follows regular order
    else:
      return s


# set filter via custom function to allow for more complex search terms
def setAdvancedFilter(self, txt):
    txt = "( " + txt + " )"
    if self.mw.app.keyboardModifiers() & Qt.AltModifier:
          txt = "-"+txt
    if self.mw.app.keyboardModifiers() & Qt.ControlModifier:
        cur = unicode(self.form.searchEdit.lineEdit().text())
        if cur and cur != \
                _("<type here to search; hit enter to show current deck>"):
                    txt = cur + " " + txt
    elif self.mw.app.keyboardModifiers() & Qt.ShiftModifier:
        cur = unicode(self.form.searchEdit.lineEdit().text())
        if cur:
            txt = cur + " or " + txt
    self.form.searchEdit.lineEdit().setText(txt)
    self.onSearch()


def setTagFormatting(tag, item):
    item.setIcon(0, QIcon(":/icons/anki-tag.png"))
    color = None
    if tag.startswith('.'):
        color = "#8C8C8C"
    elif tag.startswith('_'):
        color = "#00A209"
    elif tag[0].isupper():
        pass
    elif tag.startswith('#'):
        color = "#007F8A"
        # font = item.font(0)
        # font.setWeight(QFont.Bold)
        # item.setFont(0, font)
    else:
        color = "#343434"
    if color is not None:
        item.setForeground(0,QBrush(QColor(color)))


# use hierarchical tags and modify tag sorting order
def _userTagTree(self, root, _old):
    tags = sorted(self.col.tags.all(), key=sortFn)
    tags_tree = {}

    for idx, t in enumerate(tags):
        if t.lower() == "marked" or t.lower() == "leech":
            continue

        components = t.split(TAGS_SEPARATOR)
        try:
            next_tag = tags[idx+1]
        except IndexError:
            pass
        if len(components) == 1 and not next_tag.startswith(t + '::'):
            # regular tag, simple search
            item = self.CallbackItem(
                root, t, lambda t=t: self.setFilter("tag", t))
            setTagFormatting(t, item)
        else:
            # hierarchial tag, advanced search
            for idx, c in enumerate(components):
                partial_tag = TAGS_SEPARATOR.join(components[0:idx + 1])
                if not tags_tree.get(partial_tag):
                    if idx == 0:
                        parent = root
                    else:
                        parent_tag = TAGS_SEPARATOR.join(components[0:idx])
                        parent = tags_tree[parent_tag]

                    # use more complex search term instead of simple *-regex
                    # fixes main issue of hierarchical tags add-on where terms with
                    # with identical prefixes would also come up in search results
                    txt = "tag:" + partial_tag + ' or ' + "tag:" + partial_tag + '::*'
                    item = self.CallbackItem(
                        parent, c, lambda txt=txt: setAdvancedFilter(self, txt))
                    setTagFormatting(t, item)
                    tags_tree[partial_tag] = item


def _modelTree(self, root, _old):
    # group note types under one node
    root = self.CallbackItem(root, _("Note Type"), None)
    root.setExpanded(False)
    root.setIcon(0, QIcon(":/icons/product_design.png"))
    for m in sorted(self.col.models.all(), key=itemgetter("name")):
        mitem = self.CallbackItem(
            root, m['name'], lambda m=m: self.setFilter("mid", str(m['id'])))
        mitem.setIcon(0, QIcon(":/icons/product_design.png"))


def _systemTagTree(self, root, _old):
    # most used filters, put these on root level
    tags = (
        (_("Whole Collection"), "ankibw", ""),
        (_("Current Deck"), "deck16", "deck:current"),
        (_("Added Today"), "view-pim-calendar.png", "added:1"),
        (_("New"), "plus16.png", "is:new"),
        (_("Marked"), "star16.png", "tag:marked"),
        (_("Suspended"), "media-playback-pause.png", "is:suspended"))
    for name, icon, cmd in tags:
        item = self.CallbackItem(
            root, name, lambda c=cmd: self.setFilter(c))
        item.setIcon(0, QIcon(":/icons/" + icon))
    # almost never used, group these under 'Status'
    tags = (
        (_("Studied Today"), "view-pim-calendar.png", "rated:1"),
        (_("Again Today"), "view-pim-calendar.png", "rated:1:1"),
        (_("Learning"), "stock_new_template_red.png", "is:learn"),
        (_("Review"), "clock16.png", "is:review"),
        (_("Due"), "clock16.png", "is:due"),
        (_("Leech"), "emblem-important.png", "tag:leech"))
    status_root = self.CallbackItem(root, _("Status"), None)
    status_root.setExpanded(False)
    status_root.setIcon(0, QIcon(":/icons/clock16.png"))
    for name, icon, cmd in tags:
        item = self.CallbackItem(
            status_root, name, lambda c=cmd: self.setFilter(c))
        item.setIcon(0, QIcon(":/icons/" + icon))
    return root

def _collapseSearchesByDefault(self, root):
    match = root.findItems(_("My Searches"), Qt.MatchFixedString)
    if match:
        searches = match[0]
        root.collapseItem(searches)

Browser._systemTagTree = wrap(Browser._systemTagTree, _systemTagTree, 'around')
Browser._userTagTree = wrap(Browser._userTagTree, _userTagTree, 'around')
Browser._modelTree = wrap(Browser._modelTree, _modelTree, 'around')
Browser._favTree = wrap(Browser._favTree, _collapseSearchesByDefault, "after")