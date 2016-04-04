## anki-browser-search-hotkeys.py

**Allows you to set up hotkeys for searches in the browser**

Hotkeys follow this scheme: Ctrl+S –> (Modifier) + Key. I.e.: hit Ctrl+S to start the key sequence, let go of Ctrl+S, then hit the key assigned to  your search, plus an optional modifier.

You can use keyboard modifiers to control whether to add a term to the  search, negate it, remove it, or do something else. This follows the same  logic as the default behaviour in Anki when clicking on a search term in the sidebar.

New hotkeys can be defined in the source file by editing the `search_shortcuts` dictionary. Make sure to follow the existing syntax.

For instance, line 2 in the default `search_shortcuts` dict assigns the search
'added 1' (cards added today) to 'T'. This defines the following key sequences
in the browser:

    Ctrl+S -> T             replace search field with 'added:1'
    Ctrl+S -> Ctrl+T        add 'added:1' to existing search
    Ctrl+S -> Alt+T:        replace search field with '-added:1'
    Ctrl+S -> Ctrl+Alt+T:   add '-added:1' to existing search
    Ctrl+S -> Shift+T:      add 'or added:1' to existing search

The following keys are assigned by default:

    'A': ''
    'C': 'deck:current'
    'N': 'is:new'
    'R': 'is:review'
    'D': 'is:due'
    'M': 'tag:marked'

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).