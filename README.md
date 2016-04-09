# Misc Anki Add-ons

This repository contains a number of smaller add-ons I've written for Anki over time. For more information on each add-on please take a look at the comments in the respective source file. N.B.: If an add-on doesn't appear in this README there's a very good chance it's not ready for general use, yet.

## Overview of the add-ons

- **anki-add-reverse-toggle**: adds a user-defined key-binding that toggles the 'reverse' field in optionally reversible note types (default: Alt+Shift+B)
 
    This one is locale-dependent, so make sure to edit the source file with the name of the 'reverse' field in your note models

- **anki-browser-create-duplicate**: adds a keyboard shortcut and edit menu entry to the browser for duplicating notes. Pressing the shortcut (Ctrl+Alt+C by default) or clicking on the *Duplicate Notes* entry will find all notes belonging to the selected cards and duplicate them in place. Make sure to check out the comments in the source file for more information. 

    Based on ["Create Copy of Selected Cards"](https://ankiweb.net/shared/info/787914845) by Kealan Hobelmann.

- **anki-browser-lookup**: adds a context-menu entry to search the card browser for selected words.

- **anki-browser-more-hotkeys**: adds two additional hotkeys to the card browser, CTRL+R for rescheduling cards and CTRL+ALT+I for inverting the selection.

- **anki-reviewer-hint-hotkeys**: based on [Hint-peeking Keyboard Bindings](https://ankiweb.net/shared/info/2616209911) by Ben Lickly. Adds two hotkeys to the reviewer: 'H' to reveal hints one by one, 'G' to reveal all hints at once.

- **anki-card-stats**: based on [Card Info During Review](https://ankiweb.net/shared/info/2179254157) by Damien Elmes and [reviewer_show_cardinfo](https://github.com/steveaw/anki_addons/blob/master/reviewer_show_cardinfo.py) by Steve AM. Extends Damien's add-on with the review log table that can also be found in the Browser.

- **anki-sibling-spacing-whitelist**: based on [Sibling Spacing](https://ankiweb.net/shared/info/2951410923) by Andreas Klauer. Modified to follow a whitelist approach when choosing which note types to enable on. Check the comments in the source file for more information.

- **anki-browser-search-hotkeys**: adds user-configurable key sequences to the browser that are assigned to specific searches. The behavior of each key sequence imitates that of the tag sidebar in that keyboard modifiers decide on whether to replace the current search, add to it, or use a negation. Please read the header in the source file for more information.

## License

Most of the add-ons in this repository are licensed under the same license as Anki, the [GNU GPL, version 3 or later](http://www.gnu.org/copyleft/gpl.html). Please check the comments in the header for more details on the licensing of each add-on.