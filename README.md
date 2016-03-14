# Misc Anki Add-ons

This repository contains a number of smaller add-ons I've written for Anki over the years. For more information on each add-on please take a look at the comments in the respective source file

## Overview of the add-ons

- **anki-add-reverse-toggle**: adds a user-defined key-binding that toggles the 'reverse' field in optionally reversible note types (default: Alt+Shift+B)
 
    This one is locale-dependent, so make sure to edit the source file with the name of the 'reverse' field in your note models

- **anki-browser-create-duplicate**: adds a keyboard shortcut and edit menu entry to the browser for duplicating notes. Pressing the shortcut (Ctrl+Alt+C by default) or clicking on the *Duplicate Notes* entry will find all notes belonging to the selected cards and duplicate them in place. Make sure to check out the comments in the source file for more information. 

    Based on ["Create Copy of Selected Cards"](https://ankiweb.net/shared/info/787914845) by Kealan Hobelmann. License: GNU GPL v3.

- **anki-browser-lookup**: adds a context-menu entry to search the card browser for selected words.

- **anki-browser-more-hotkeys**: adds two additional hotkeys to the card browser, CTRL+J for suspending cards and CTRL+E for invoking the "Add note" dialog

- **anki-reviewer-hint-hotkeys**: based on [Hint-peeking Keyboard Bindings](https://ankiweb.net/shared/info/2616209911) by Ben Lickly. Adds two hotkeys to the reviewer: 'H' to reveal hints one by one, 'G' to reveal all hints at once. License: GNU GPL v3.

## License

If not specified otherwise, all of the add-ons in this repository are licensed under the MIT license.