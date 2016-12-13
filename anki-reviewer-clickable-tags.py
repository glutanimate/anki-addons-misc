#-*- coding: utf-8 -*-

"""
Anki Add-on: Clickable Tags

Adds clickable tags to the Reviewer

- regular click: search for tag in deck
(- shift+click: search for tag in complete collection) currently disabled

Simplified version of  "Clickable Tags on Reviewer" by amsaravi
(https://bitbucket.org/amsaravi/ankiaddons)

Copyright: Glutanimate 2016
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""

import re

import aqt
from aqt.reviewer import Reviewer
from anki.template import Template
from anki.hooks import wrap

# tag_links_js = """
# <script type="text/javascript">
# function onTagClick(event, tag) {
#     if (event.shiftKey) {py.link("tagall " + tag)} else {py.link("tagdeck " + tag)};
# }
# </script>
# """

def myLinkHandler(self, url, _old):
    # self is reviewer instance
    if url.startswith("tag"):
        tag = url.split()[1]
        search = "tag:" + tag
        if url.startswith("tagdeck"):
            deck = self.mw.col.decks.name(self.card.did)
            search += ' deck:"{0}"'.format(deck)
        browser = aqt.dialogs.open("Browser", self.mw)
        # not using setfilter because it grabs keyboard modifiers
        browser.form.searchEdit.lineEdit().setText(search)
        browser.onSearch()
    else:
        return _old(self, url)

def myRender(self, _old, template=None, context=None, encoding=None):
    # self is template instance
    template = template or self.template
    context = context or self.context
    if context is not None:
        tags = context['Tags'].split()
        f = ("""<span style="cursor: pointer;" class="tags" onclick='py.link("tagdeck {0}")'>{0}</span>""")
        tagstr = " ".join(f.format(tag) for tag in tags)
        template = re.sub("{{Tags}}", tagstr, template)
    return _old(self, template, context, encoding)

Reviewer._linkHandler = wrap(Reviewer._linkHandler, myLinkHandler, "around")
Template.render = wrap(Template.render, myRender, "around")