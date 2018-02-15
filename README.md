# Miscellaneous Anki Add-ons

This repository contains most of the smaller Anki add-ons I have written over the years. For more information on each add-on please take a look at the comments in the respective source file, or at its [AnkiWeb description](docs/descriptions.md).

<!-- MarkdownTOC -->

- [Generic Installation Instructions](#generic-installation-instructions)
- [Naming Scheme](#naming-scheme)
- [Credits](#credits)
- [License](#license)
- [Other Anki-related Projects](#other-anki-related-projects)

<!-- /MarkdownTOC -->

## Generic Installation Instructions

**Installation from AnkiWeb**

Most add-ons in this repository have been published on [AnkiWeb](https://ankiweb.net/shared/addons/) and may be comfortably installed via Anki's own add-on management system. To correlate each source file with its listing on AnkiWeb please refer to the add-on titles in their [AnkiWeb descriptions](docs/descriptions.md).

**Manual Installation**

1. Open Anki's add-on folder by navigating  to *Tools* -> *Add-ons* -> *Open add-ons folder* from Anki's main screen
2. Download a copy of the [full repository zip archive](https://github.com/glutanimate/anki-addons-misc/archive/master.zip)
3. Locate the add-ons you want to install in the `src/` directory
4. Copy the add-on files to Anki's add-on directory
    
    - in case of *Anki 2.0*: For each of the add-ons, copy all files its folder aside from `__init__.py` into the top-most level of Anki's add-on directory (e.g. for `reviewer_auto_rate_hotkey` you would only copy `reviewer_auto_rate_hotkey.py`)
    - in case of *Anki 2.1*: For each of the add-ons, copy the entire add-on folder into the top-most level of Anki's add-on directory (e.g. for `reviewer_auto_rate_hotkey` you would copy the entire `reviewer_auto_rate_hotkey` folder). **Note:** Not all add-ons in this repository have been transitioned to Anki 2.1, yet. To learn more about the compatibility status of each add-on please see [here](docs/anki21.md).

5. Restart Anki to see the changes

## Naming Scheme

The source file naming describes which part of Anki each add-on interacts with. As such, the names do not always correspond with their listings on AnkiWeb. 

Add-on file names also have an impact on their loading order. Files with a leading special character are designed to be imported after most other add-ons have been loaded, as they might interact with them.

## Credits

Some of the add-ons found in this repository were either adopted from earlier works by other authors or simply constitute re-uploads of add-ons that disappeared from AnkiWeb, with no original code repository to be found. I have tried to document the development history of each of these add-ons in their source code header, but more detailed information may also be found [here](docs/credits.md).

## License

Most of the add-ons in this repository are licensed under the same license as Anki, the [GNU AGPL, version 3 or later](https://www.gnu.org/licenses/agpl.html). Please check the source code comments for more details on the licensing of each add-on.

## Other Anki-related Projects

Make sure to also check out my larger Anki projects:

- [Image Occlusion Enhanced](https://github.com/Glutanimate/image-occlusion-enhanced)
- [Cloze Overlapper](https://github.com/glutanimate/cloze-overlapper)
- [Review Heatmap](https://github.com/Glutanimate/review-heatmap)
- [Advanced Previewer](https://github.com/glutanimate/advanced-previewer)
- [Sticky Searches](https://github.com/glutanimate/sticky-searches)
- [Note Organizer](https://github.com/glutanimate/note-organizer)
- [Sequence Inserter](https://github.com/glutanimate/sequence-inserter)
- [HTML Cleaner](https://github.com/glutanimate/html-cleaner)
- [Unified Remote for Anki](https://github.com/Glutanimate/unified-remote-anki)