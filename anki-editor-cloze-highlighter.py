# -*- coding: utf-8 -*-

"""
Anki Add-on: Highlight All Cloze Sequences

Modifies Anki's default cloze function in order to provide the ability
to target all clozed sequences through user-provided CSS

Usage:

- Use Anki's regular cloze shortcuts as usual
- Update your stylesheet to target the new cloze elements, e.g.:

```CSS
 /* target all clozed elements: */
.clozed {
    color: grey;
}
 /* target first clozed element: */
.clozed.c1 {
    background: yellow;
}
```

Note:

This add-on is incompatible with Cloze Overlapper and any other add-ons
that overwrite the Editor.onCloze method.

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

import re

from aqt.qt import *
from aqt.editor import Editor

from aqt.utils import tooltip, showInfo


def onCloze(self):
    # check that the model is set up for cloze deletion
    if not re.search('{{(.*:)*cloze:',self.note.model()['tmpls'][0]['qfmt']):
        if self.addMode:
            tooltip(_("Warning, cloze deletions will not work until "
            "you switch the type at the top to Cloze."))
        else:
            showInfo(_("""\
To make a cloze deletion on an existing note, you need to change it \
to a cloze type first, via Edit>Change Note Type."""))
            return
    # find the highest existing cloze
    highest = 0
    for name, val in self.note.items():
        m = re.findall("\{\{c(\d+)::", val)
        if m:
            highest = max(highest, sorted([int(x) for x in m])[-1])
    # reuse last?
    if not self.mw.app.keyboardModifiers() & Qt.AltModifier:
        highest += 1
    # must start at 1
    highest = max(1, highest)
    # wrap cloze items in span
    js_cloze = """wrap('<span class="clozed c%d">{{c%d::', '}}</span>');"""
    self.web.eval(js_cloze % (highest, highest))

# Hooks

Editor.onCloze = onCloze