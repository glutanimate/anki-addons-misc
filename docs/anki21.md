## Anki 2.1.x Compatibility Status

### Overview

- last modification date: *2017-08-23*
- current conversion ratio: **14**/37
- major show-stoppers outside of python3/Qt5: Extensive modifications to Reviewer and Editor

### Details

|              Add-on              |        Status        |                                                 Notes / Issues                                                 |
|----------------------------------|----------------------|----------------------------------------------------------------------------------------------------------------|
| editor_random_list               | ?                    |                                                                                                                |
| reviewer_puppy_reinforcement     | ?                    |                                                                                                                |
| reviewer_visual_feedback         | ?                    |                                                                                                                |
| browser_batch_edit               | (:white_check_mark:) | cosmetics: attachment icon not working                                                                         |
| browser_create_duplicate         | :white_check_mark:   |                                                                                                                |
| browser_create_filtered_deck     | :white_check_mark:   |                                                                                                                |
| browser_external_editor          | :x:                  | SIGNALS, potentially complex Editor changes                                                                    |
| browser_field_to_tags            | :white_check_mark:   |                                                                                                                |
| browser_more_hotkeys             | :x:                  | SIGNALS                                                                                                        |
| browser_refresh                  | :x:                  | Browser.onSearch                                                                                               |
| browser_replace_tag              | :white_check_mark:   |                                                                                                                |
| browser_search_highlight_results | :x:                  | QWebPage → no highlightAllOccurences(); findText should show all results, but just flickers highlights shortly |
| browser_search_hotkeys           | :x:                  | Browser.onSearch                                                                                               |
| browser_sidebar_tweaks           | :x:                  | PyQt4, complex sidebar changes                                                                                 |
| common_context_search            | (:x:)                | Browser.onSearch; rest working                                                                                 |
| common_ctrlf_search              | :x:                  | QWebPage; Editor.onSetupButtons                                                                                |
| editor_*                         | :x:                  | Editor.onSetupButtons (if applicable)                                                                          |
| editor_custom_stylesheet         | :white_check_mark:   |                                                                                                                |
| editor_sync_html_cursor          | :x:                  | BeautifulSoup                                                                                                  |
| main_ontop                       | (:white_check_mark:) | Child dialogs appear below main window                                                                         |
| overview_browser_shortcuts       | :x:                  | SIGNALS, Browser.onSearch                                                                                      |
| overview_deck_tooltip            | :x:                  | tooltips not appearing, possible JS issue                                                                      |
| overview_refresh_media           | :x:                  | QWebSettings → no clearMemoryCaches()                                                                          |
| previewer_tag_browser            | :x:                  | Depends on Advanced Previewer which has not been converted, yet                                                |
| reviewer_browse_*                | :x:                  | Reviewer._keyHandler, Browser.onFind                                                                           |
| reviewer_card_stats              | (:white_check_mark:) | Uses serif font (badly aliased); observed one segfault. Investigate if also present ankiplugins/cardstats.py   |
| reviewer_file_hyperlinks         | :x:                  | py.link bridge no longer exists                                                                                |
| reviewer_hide_toolbar            | :x:                  | obsolete, 2.1 has no toolbar                                                                                   |
| reviewer_hint_hotkeys            | :white_check_mark:   |                                                                                                                |
| reviewer_more_answer_buttons     | :x:                  | Reviewer._keyHandler, complex changes to answer button methods                                                 |
| reviewer_progress_bar            | :white_check_mark:   |                                                                                                                |
| reviewer_track_unseen            | :x:                  | PyQt4, SIGNALS, potentially obsolete                                                                           |
| sched_sibling_spacing_whitelist  | :x:                  | SIGNALS, potentially other issues                                                                              |
| search_last_edited               | :white_check_mark:   |                                                                                                                |
| stats_true_retention_extended    | :white_check_mark:   |                                                                                                                |
| tagedit_enhancements             | :white_check_mark:   |                                                                                                                |
| tagedit_subtag_completer         | :white_check_mark:   |                                                                                                                |

