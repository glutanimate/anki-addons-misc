## Anki 2.1.x Compatibility Status

### Overview

- last modification date: *2017-08-23*
- current conversion ratio: **14**/37
- major show-stoppers outside of python3/Qt5: Extensive modifications to Reviewer and Editor

### Details

|              Add-on              | Status |                                                 Notes / Issues                                                 |
|----------------------------------|--------|----------------------------------------------------------------------------------------------------------------|
| editor_random_list               | ?      |                                                                                                                |
| reviewer_puppy_reinforcement     | ?      |                                                                                                                |
| reviewer_visual_feedback         | ?      |                                                                                                                |
| browser_batch_edit               | (✔)    | cosmetics: attachment icon not working                                                                         |
| browser_create_duplicate         | ✔      |                                                                                                                |
| browser_create_filtered_deck     | ✔      |                                                                                                                |
| browser_external_editor          | ✘      | SIGNALS, potentially complex Editor changes                                                                    |
| browser_field_to_tags            | ✔      |                                                                                                                |
| browser_more_hotkeys             | ✘      | SIGNALS                                                                                                        |
| browser_refresh                  | ✘      | Browser.onSearch                                                                                               |
| browser_replace_tag              | ✔      |                                                                                                                |
| browser_search_highlight_results | ✘      | QWebPage → no highlightAllOccurences(); findText should show all results, but just flickers highlights shortly |
| browser_search_hotkeys           | ✘      | Browser.onSearch                                                                                               |
| browser_sidebar_tweaks           | ✘      | PyQt4, complex sidebar changes                                                                                 |
| common_context_search            | (✘)    | Browser.onSearch; rest working                                                                                 |
| common_ctrlf_search              | ✘      | QWebPage; Editor.onSetupButtons                                                                                |
| editor_*                         | ✘      | Editor.onSetupButtons (if applicable)                                                                          |
| editor_custom_stylesheet         | ✔      |                                                                                                                |
| editor_sync_html_cursor          | ✘      | BeautifulSoup                                                                                                  |
| main_ontop                       | (✔)    | Child dialogs appear below main window                                                                         |
| overview_browser_shortcuts       | ✘      | SIGNALS, Browser.onSearch                                                                                      |
| overview_deck_tooltip            | ✘      | tooltips not appearing, possible JS issue                                                                      |
| overview_refresh_media           | ✘      | QWebSettings → no clearMemoryCaches()                                                                          |
| previewer_tag_browser            | ✘      | Depends on Advanced Previewer which has not been converted, yet                                                |
| reviewer_browse_*                | ✘      | Reviewer._keyHandler, Browser.onFind                                                                           |
| reviewer_card_stats              | (✔)    | Uses serif font (badly aliased); observed one segfault. Investigate if also present ankiplugins/cardstats.py   |
| reviewer_file_hyperlinks         | ✘      | py.link bridge no longer exists                                                                                |
| reviewer_hide_toolbar            | ✘      | obsolete, 2.1 has no toolbar                                                                                   |
| reviewer_hint_hotkeys            | ✔      |                                                                                                                |
| reviewer_more_answer_buttons     | ✘      | Reviewer._keyHandler, complex changes to answer button methods                                                 |
| reviewer_progress_bar            | ✔      |                                                                                                                |
| reviewer_track_unseen            | ✘      | PyQt4, SIGNALS, potentially obsolete                                                                           |
| sched_sibling_spacing_whitelist  | ✘      | SIGNALS, potentially other issues                                                                              |
| search_last_edited               | ✔      |                                                                                                                |
| stats_true_retention_extended    | ✔      |                                                                                                                |
| tagedit_enhancements             | ✔      |                                                                                                                |
| tagedit_subtag_completer         | ✔       |                                                                                                                |

