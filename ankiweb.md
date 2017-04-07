# Add-on descriptions

<!-- MarkdownTOC -->

- [Published on Ankiweb](#published-on-ankiweb)
    - [anki-browser-search-hotkeys.py](#anki-browser-search-hotkeyspy)
    - [anki-browser-search-modifiers.py](#anki-browser-search-modifierspy)
    - [anki-browser-create-duplicate.py](#anki-browser-create-duplicatepy)
    - [anki-web-contextsearch.py](#anki-web-contextsearchpy)
    - [anki-editor-field-navigation.py](#anki-editor-field-navigationpy)
    - [anki-editor-tag-hotkeys.py](#anki-editor-tag-hotkeyspy)
    - [anki-editor-autocomplete-whitelist.py](#anki-editor-autocomplete-whitelistpy)
    - [anki-editor-restore-fields.py](#anki-editor-restore-fieldspy)
    - [anki-browser-refresh.py](#anki-browser-refreshpy)
    - [anki-browser-replace-tag.py](#anki-browser-replace-tagpy)
    - [anki-browser-create-filtered-deck.py](#anki-browser-create-filtered-deckpy)
    - [anki-overview-deck-switcher.py](#anki-overview-deck-switcherpy)
    - [anki-reviewer-puppy-reinforcement.py](#anki-reviewer-puppy-reinforcementpy)
    - [anki-browser-batch-edit.py](#anki-browser-batch-editpy)
    - [anki-reviewer-card-stats.py](#anki-reviewer-card-statspy)
    - [anki-editor-custom-tagedit.py](#anki-editor-custom-tageditpy)
    - [anki-overview-refreshmedia.py](#anki-overview-refreshmediapy)
    - [anki-browser-external-editor.py](#anki-browser-external-editorpy)
    - [anki-stats-true-retention-extended.py](#anki-stats-true-retention-extendedpy)
    - [anki-editor-sync-cursor-position.py](#anki-editor-sync-cursor-positionpy)
    - [anki-sched-advanced-newcard-limits.py](#anki-sched-advanced-newcard-limitspy)
- [Yet to be published](#yet-to-be-published)
- [The rest](#the-rest)

<!-- /MarkdownTOC -->


## Published on Ankiweb

### anki-browser-search-hotkeys.py

**Browser search hotkeys**

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

    'A': {'search': ''},            # All together now
    'T': {'search': 'added:1'},     # Today
    'V': {'search': 'rated:1'},     # Viewed
    'G': {'search': 'rated:1:1'},   # aGain today
    'F': {'search': 'card:1'},      # First
    'C': {'search': 'deck:current'},# Current
    'N': {'search': 'is:new'},      # New
    'L': {'search': 'is:learn'},    # Learn
    'R': {'search': 'is:review'},   # Review
    'D': {'search': 'is:due'},      # Due
    'S': {'search': 'is:suspended'},# Suspended
    'B': {'search': 'is:buried'},   # Buried
    'M': {'search': 'tag:marked'},  # Marked
    'E': {'search': 'tag:leech'},   # lEech

**Changes**

2016-04-27 - Implemented hotkeys for more searches. Thanks to ankitest!

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-browser-search-modifiers.py

**Browser search modifiers**

**Checkbox toggles that modify how the browser search behaves**

Adds two checkboxes to the browser search form that, when toggled, modify searches in the following way:

**Deck** (Hotkey: Alt+D): Limit results to current deck
**Card** (Hotkey: Alt+C): Limit results to first card of each note

![screenshot](screenshots/anki-browser-search-modifiers.png)

Based on the following add-ons:

- "Limit searches to current deck" by Damien Elmes
   (https://github.com/dae/ankiplugins/blob/master/searchdeck.py)
- "Ignore accents in browser search" by Houssam Salem
   (https://github.com/hssm/anki-addons)

Original idea by Keven on the [Anki support forums](https://anki.tenderapp.com/discussions/ankidesktop/17918-add-on-or-anki-feature-suggestion-show-only-front-card-in-browser-checkbox).

Special thanks to ankitest for testing and improving this add-on.

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-browser-create-duplicate.py

**Duplicate selected Notes**

**Overview**

This add-on supplements the card browser by adding a keyboard shortcut and menu entry for creating duplicates of notes.

Pressing the shortcut (Ctrl+Alt+C by default) or clicking on the 'Create Duplicate' entry in the Edit menu will find all notes belonging to the selected cards and duplicate them in place.

**A few pointers**

- **Important**: All cards generated by each note will be duplicated alongside the note
- All duplicated cards will end up in the deck of the first selected card
- The duplicated cards should look exactly like the originals
- Tags are preserved in the duplicated notes
- Review history is NOT duplicated to the new cards (they appear as new cards)
- The notes will be marked as duplicates (because they are!)

**Changes**

2016-04-30 - duplications can now be undone via CTRL+Z (using Anki's default restoration points)

**Credits, license, and source code**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

This add-on is based on "[Create Copy of Selected Cards](https://ankiweb.net/shared/info/787914845)" by Kealan Hobelmann

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-web-contextsearch.py

**Context Menu Search**

A simple Anki add-on that adds context-menu entries to search the card browser and various online search providers for selected words. The entries will appear both in the Reviewer and Card Editor. This add-on was formerly known as "Search Browser for Selected Words".

**Search Providers**

Currently supported are Google, Google Images, and Wikipedia. You can add new providers by editing the source code and modifying the *SEARCH_PROVIDERS* list. Just make sure to follow the syntax of the other entries.

**Changelog**

2016-01-26 – Only create a submenu when needed
2017-01-17 – Rewrote add-on, added support for online search providers
2016-04-19 – double-quote phrases when searching

**License**

*Copyright (c) 2015-2017 [Glutanimate](https://github.com/Glutanimate)*

Based on 'OSX Dictionary Lookup' by Eddie Blundell and 'Search Google Images' by Steve AW.

The code for this add-on is hosted in my [misc add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-editor-field-navigation.py

**Quick Field Navigation Add-on for Anki**

**Quickly navigate through your entry fields in the card editor**

This add-on provides the following shortcuts:

**Ctrl** + **1-9**: Switch focus to field 1-9
**Ctrl** + **0**: Switch focus to last field
**Alt** + **Shift** + **F**: Switch focus back to note fields from tag field (to complement Anki's inbuilt Ctrl + Shift + T) hotkey to switch to the tags field)

Note: In their current implementation the hotkeys will not work when the tag suggestions drop-down box is active. I am [still looking for a fix for this](https://anki.tenderapp.com/discussions/add-ons/4725-dd-on-development-unable-to-switch-editor-focus-back-to-web-view-when-tags-completer-is-active).

**Changelog**

2016-04-19 – Reworked the add-on from scratch to have a much leaner footprint
2015-09-04 – Initial release

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-editor-tag-hotkeys.py

**Editor Tag Hotkeys Add-on for Anki**

This is a very simple add-on for [Anki](http://ankisrs.net/) that adds a few hotkey toggles for user-defined tags. It also includes a hotkey that clears the tags field (<kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>R</kbd> by default)

**Usage**

*Adding a tag hotkey*

Edit `anki-editor-tag.hotkeys.py` and modify the `onSetupButtons` function with your custom hotkeys and tags. For instance, to add a toggle for the tag *important* and assign it to <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>I</kbd> you would replace the following block:

```python
s = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_1), editor.parentWindow)
s.connect(s, SIGNAL("activated()"),
          lambda : toggleTag(editor, "toggled-tag1"))
```

with:

```python
s = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_I), editor.parentWindow)
s.connect(s, SIGNAL("activated()"),
          lambda : toggleTag(editor, "important"))
```

You can add as many toggles as you want by placing additional blocks of this type under the `def onSetupButtons(editor):` line. Make sure to preserve the indenting!

For a list of all possible key assignments check here:

- [keys](http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/doc/html/qt.html#Key-enum)
- [modifiers](http://ftp.ics.uci.edu/pub/centos0/ics-custom-build/BUILD/PyQt-x11-gpl-4.7.2/doc/html/qt.html#Modifier-enum)

*Defining a unique tag*

Sometimes you might want to quickly toggle between several different tags. For this purpose I've implemented a configuration option called uniqueTags. Any items added to this list will cause their respective hotkeys to delete all other instances of unique tags aside from the one currently being triggered. 

For instance, if you set up hotkeys for "subject-a" and "subject-b" and add these tags to `uniqueTags`, hitting the hotkey for "subject-a" will delete "subject-b" from the tags list and vice-versa.

To add a unique tag, simply update the following excerpt in the script:

```python
uniqueTags = [
    "subject-a", "subject-b"
]
```

Please make sure to preserve the formatting and quoting while doing so!

**License**

*Copyright 2015 [Glutanimate](https://github.com/Glutanimate)*

Anki Editor Tag Hotkeys add-on for Anki is licensed under the [GNU GPLv3](http://www.gnu.de/documents/gpl-3.0.en.html).


### anki-editor-autocomplete-whitelist.py

**Overview**

This is a modified version of the [Editor Autocomplete add-on for Anki](https://github.com/sartak/anki-editor-autocomplete). Instead of checking against a blacklist of non-autocompleted fields this implementation of the add-on will only enable autocomplete on fields you specify.

Fields to enable autocomplete on can be specified by modifying the `AutocompleteFields` array at the beginning of the script, e.g.:

```python
AutocompleteFields = [ "sources", "additional-info" ]
```

This version of the add-on also includes a hotkey that saves you the trouble of clicking on the autocomplete suggestion. It's set to <kbd>Alt</kbd> + <kbd>Return</kbd> by default.

All credit for the original add-on goes to Shawn M Moore ([@sartak](https://github.com/sartak/)).


### anki-editor-restore-fields.py

**Editor Field History**

**Overview**

This add-on enhances Anki's note editor with the following:

- hotkeys that copy over tags and field values of the last note in the same deck
- a history window that provides a list of last used values for the current field

Overview of all available hotkeys:

*Ctrl + Alt + H* – Invoke history window
*Alt+Z* – Copy over current field from last note
*Alt+Shift+Z* – Copy over a a number of user-defined fields (see below)
*Ctrl+Alt+Shift+Z* – Copy over all fields

**Configuration**

You can edit the add-on's source code to modify the following:

`history_window_shortcut`: controls the hotkey for invoking the history window
`field_restore_shortcut`: controls "Restore current field hotkey"
`partial_restore_shortcut`: controls "Restore a number of user-defined fields" hotkey
`full_restore_shortcut`: controls "Restore all fields" hotkey
`partial_restore_fields`: list of fields that are restored by the `partial_restore_shortcut`. Needs to be formatted as a python list (e.g. `["field1", "field2", "field3"]`).

**Changelog**

2017-03-11 – Ensure that the add-on can only be run in the Add Cards screen
2016-12-13 – Fixed a rare bug that caused empty notes to appear
2016-06-04 – Added history window to the add-on (invoked via Ctrl+Alt+H)
2016-05-27 – Initial release

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).


### anki-browser-refresh.py

**F5 to Refresh the Browser**

Adds a hotkey to the browser that refreshes the current view. Useful when you've added new cards and want to repeat an existing search. Note: cards are sorted by creation time when refreshing the view.

Hotkey: *F5*

**Changelog**

2016-05-27 – Initial release

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).


### anki-browser-replace-tag.py

**Search and Replace Tags**

**Overview**

Adds a "Replace Tag" dialog to the card browser that prompts for a tag and its replacement and then replaces the tag in all selected notes.

Hotkey: *Ctrl+Alt+Shift+T*

**Changelog**

2016-06-04 – Switch to title case for menu entries
2016-05-27 – Initial release

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).


### anki-browser-create-filtered-deck.py

**Create Filtered Deck from the Browser**

Adds a hotkey and menu item to the browser that launches a filtered deck creation dialog based on the current search.

Hotkey: *Ctrl+Shift+D*

The dialog will be placed above Anki's main window (this is a limitation of the deck creation dialog).

**Changelog**

2016-05-28 – Initial release

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-overview-deck-switcher.py

**Switch Between Decks on the Main Screen**

Adds the following hotkeys to Anki's main deck browser screen:

Ctrl + Tab: Switch to next deck
Ctrl + Shift + Tab: Switch to previous deck

These also work in the detailed view of each deck and in the reviewer.

**Configuration**

By default the hotkeys will skip decks that don't have any cards that are due or new. Filtered decks and custom study sessions are also ignored. You can change this by editing the add-on and setting the variables defined in the USER CONFIGURATION section at the top.

**Changelog**

2016-07-30 – Initial release

**Compatibility**

Only works with Anki releases 2.0.x for now, i.e. the Anki 2.1.x alpha/beta is not yet supported.

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-reviewer-puppy-reinforcement.py

**Puppy Reinforcement**

**Overview**

Uses intermittent reinforcement with cute puppies to encourage card review streaks.

Based on "Show Cute Dogs" (https://ankiweb.net/shared/info/1125592690).

![](https://raw.githubusercontent.com/Glutanimate/anki-addons-misc/master/screenshots/anki-reviewer-puppy-reinforcement.png)

**What's new in this version**

- Uses tooltips instead of a separate window
- The puppies are spread intermittently through your reviews. By default they will appear around every 10 cards (some take longer than others). You can customize this by editing the add-on)
- Customizable encouragement messages that change based on the card tally
- Removed cats and other non-puppies

**Other notes**

- The add-on comes with around 50 puppies by default, but you can add more by placing additional images in the puppy_reinforcement folder next to the add-on
- the tooltip will appear slightly higher than tooltips in Anki usually do. This is to prevent overlapping with other tooltips (e.g. the ones produced by the answer confirmation add-on)

**Credits**

(c) 2015 mbertolacci (https://github.com/mbertolacci)
(c) 2016 Glutanimate (https://github.com/Glutanimate)

Source code: https://github.com/Glutanimate/anki-addons-misc/blob/master/anki-reviewer-puppy-reinforcement.py

### anki-browser-batch-edit.py

**Batch Note Editing**

**Overview**

Adds a new menu item to the card browser that allows you to:

- batch-add information/media to a specific field
- batch-replace the contents of a specific field

The changes will be applied to all selected notes that feature the selected field.

**Demo**

Here's a quick demo video that showcases these features:

[![YouTube: Anki add-on demo: Batch Note Editing](https://i.ytimg.com/vi/iCZzcSnAeH4/mqdefault.jpg)](https://youtu.be/iCZzcSnAeH4)

**Other Remarks**

The add-on uses the first selected note to generate the field list you're presented with. So please make sure to select a note with the right fields.

**Changelog**

2016-12-11 – Support for adding text before existing content (thanks to @luminousspice for the idea)
2016-12-08 – Initial release

**License**

*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

All credit for the original idea for this add-on goes to [/u/TryhardasaurusRex on Reddit](https://www.reddit.com/user/TryhardasaurusRex) who commissioned its development.

The code is also hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-reviewer-card-stats.py

**Extended Card Stats During Review**

Based on [Card Info During Review](https://ankiweb.net/shared/info/2179254157) by Damien Elmes and [Reviewer Show Cardinfo](https://github.com/steveaw/anki_addons/blob/master/reviewer_show_cardinfo.py) by Steve AW. Extends Damien's add-on with a review log table similar to the one found in the Browser.

**Screenshot**

![](https://raw.githubusercontent.com/Glutanimate/anki-addons-misc/master/screenshots/anki-reviewer-card-stats.png)

**License**

*Copyright (c) 2012 Damien Elmes*
*Copyright (c) 2013 Steve AW*
*Copyright (c) 2016 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).

### anki-editor-custom-tagedit.py

**Tag Entry Enhancements**

A number of enhancements meant to improve keyboard navigation in Anki's tag entry field:

- adds *Return/Enter* as a hotkey to apply the first suggested tag
- adds *Ctrl+Tab* as a hotkey to move through the list of suggestions
- disables initial suggestion box popup when entering the field
- allows using ↑/↓ to invoke the tag suggestion box

**Changelog**

2017-01-15 – Tags completed via *Enter* now follow the suggestion's capitalization; automatically append space to quick-completed tags
2016-12-28 – Initial release

**License**

*Copyright (c) 2016-2017 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted in my [misc Anki add-ons repository](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).


### anki-overview-refreshmedia.py

**Refresh Media References**

Adds an entry in the Tools menu that clears the webview cache (hotkey: Ctrl+Alt+M). This will effectively refresh all media files used by your cards and templates, allowing you to display changes to external files without having to restart Anki.

The add-on will also update the modification time of your media collection which will force an upload of any updated files on the next synchronization with AnkiWeb.

Note: Might lead to increased memory consumption if used excessively

**Changelog**

2017-01-29 – Initial release

**License**

*Copyright (c) 2017 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted [on GitHub](https://github.com/Glutanimate/anki-addons-misc).

### anki-browser-external-editor.py

**External Note Editor for the Browser**

Extends the card browser with a shortcut and menu action that launches an external editor window for the current note (`CTRL`+`ALT`+`E`).

Here's a quick video demonstration:

[![YouTube: Anki add-on: External Note Editor for the Card Browser](https://i.ytimg.com/vi/dEL8204lOq4/mqdefault.jpg)](https://youtu.be/dEL8204lOq4)

**Changelog**

2017-02-21 – Initial release

**License**

*Copyright (c) 2017 [Glutanimate](https://github.com/Glutanimate)*

The code for this add-on is hosted [on GitHub](https://github.com/Glutanimate/anki-addons-misc).

Licensed under the [GNU GPL v3](http://www.gnu.de/documents/gpl-3.0.en.html).


### anki-stats-true-retention-extended.py

**True Retention by Card Maturity**

This is a slightly modified version of the [True Retention add-on](https://ankiweb.net/shared/info/613684242) by Strider that breaks the retention statistics up by card maturity:

![](https://raw.githubusercontent.com/Glutanimate/anki-addons-misc/master/screenshots/anki-stats-true-retention-extended.png)

In addition to this, the add-on also allows you to define a custom card maturity threshold (`MATURE_IVL` at the top of the source code). This is set to 21 days by default.

**Credits and License**

All credit for the original True Retention add-on goes to Strider. This modified version is based on a [post on the Anki support forums](https://anki.tenderapp.com/discussions/add-ons/8986-true-retention-how-to-change-value-of-mature-cards-extracted-from-21-to-90-days) by peter19220.

*Copyright 2016 Strider*

*Copyright 2017 [Glutanimate](https://github.com/Glutanimate)*

I wasn't able to find any licensing information for the original add-on, but since it reuses parts of Anki's code I think it's fair to assume that it's licensed under the same license as Anki itself (GNU GPLv3).

### anki-editor-sync-cursor-position.py

**Sync Cursor Position Between Editor and HTML Window**

Preserves the cursor position when switching back and forth between the note editor and HTML editing window (CTRL+SHIFT+X).

**CREDITS AND LICENSE**

*Copyright © 2017 [Glutanimate](https://github.com/Glutanimate)*

This add-on was commissioned by a fellow Anki user who would like to remain anonymous. All credit for the original idea goes to them.

I'm always happy for new add-on commissions. If you have an idea for an add-on or new feature, please feel free to reach out to me on [Twitter](https://twitter.com/glutanimate), or at glutanimate [αt] gmail . com.

Licensed under the [GNU AGPL v3](https://www.gnu.org/licenses/agpl.html). The source code for this add-on is available on [GitHub](https://github.com/Glutanimate/anki-addons-misc).

### anki-sched-advanced-newcard-limits.py

**Advanced New Cards Limits**

Allows you to restrict the number of new cards for specific decks to less than one per day.

**CONFIGURATION**

Please edit the configuration section at the top of the source code to define the card limits. The syntax for setting up limits for a specific deck is as follows:

    deck_limits = {
        u"My deck name": 3
    }

where "3" corresponds to one new card every three days.

These settings will only apply to decks that have their new card limit set to "1" within Anki, so please make sure to do so before using this add-on.

**SUPPORTED PLATFORMS**

Like all add-ons that modify scheduling this add-on will only work on the desktop releases.

**CREDITS AND LICENSE**

*Copyright © 2017 [Glutanimate](https://github.com/Glutanimate)*

This add-on was commissioned by a fellow Anki user who would like to remain anonymous. All credit for the original idea goes to them.

I'm always happy for new add-on commissions. If you have an idea for an add-on or new feature, please feel free to reach out to me on [Twitter](https://twitter.com/glutanimate), or at glutanimate [αt] gmail . com.

Licensed under the [GNU AGPL v3](https://www.gnu.org/licenses/agpl.html). The source code for this add-on is available on [GitHub](https://github.com/Glutanimate/anki-addons-misc).

-------------------------------

## Yet to be published

- **anki-browser-more-hotkeys**: adds two additional hotkeys to the card browser, CTRL+R for rescheduling cards and CTRL+ALT+I for inverting the selection.

- **anki-reviewer-hint-hotkeys**: based on [Hint-peeking Keyboard Bindings](https://ankiweb.net/shared/info/2616209911) by Ben Lickly. Adds two hotkeys to the reviewer: 'H' to reveal hints one by one, 'G' to reveal all hints at once.

- **anki-sibling-spacing-whitelist**: based on [Sibling Spacing](https://ankiweb.net/shared/info/2951410923) by Andreas Klauer. Modified to follow a whitelist approach when choosing which note types to enable on. Check the comments in the source file for more information.

------------------------

## The rest

If an add-on doesn't appear in this document there's a very good chance it's not ready for general use, yet.
