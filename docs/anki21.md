## Anki 2.1.x Compatibility Status

### Overview

- last modification date: *2018-02-15*
- current conversion ratio: **18**/59
- major blockers outside of Python3/Qt5:
    + Extensive modifications to Reviewer and Editor
    + Extensive modification to Scheduler

### Details

|              Add-on              |        Status        |                                                 Notes / Issues                                                 |
|----------------------------------|----------------------|----------------------------------------------------------------------------------------------------------------|
| browser_batch_edit               | (:white_check_mark:) | cosmetics: attachment icon not working                                                                         |
| browser_batch_remove_formatting  | :x:                  | BeautifulSoup                                                                                                  |
| browser_create_duplicate         | :white_check_mark:   |                                                                                                                |
| browser_create_filtered_deck     | :white_check_mark:   |                                                                                                                |
| browser_external_editor          | :x:                  | SIGNALS, potentially complex Editor changes                                                                    |
| browser_field_to_tags            | :white_check_mark:   |                                                                                                                |
| browser_more_hotkeys             | :x:                  | SIGNALS                                                                                                        |
| browser_refresh                  | :x:                  | Browser.onSearch                                                                                               |
| browser_replace_tag              | :white_check_mark:   |                                                                                                                |
| browser_search_highlight_results | :white_check_mark:   | QWebPage → no highlightAllOccurences(); findText should show all results, but just flickers highlights shortly |
| browser_search_hotkeys           | :x:                  | Browser.onSearch                                                                                               |
| browser_sidebar_tweaks           | :x:                  | PyQt4, complex sidebar changes                                                                                 |
| common_context_search            | (:x:)                | Browser.onSearch; rest working                                                                                 |
| common_ctrlf_search              | :x:                  | QWebPage; Editor.onSetupButtons                                                                                |
| editor_*                         | :x:                  | Editor.onSetupButtons (if applicable)                                                                          |
| editor_custom_stylesheet         | :white_check_mark:   |                                                                                                                |
| editor_preserve_fields_on_switch | :x:                  | Obsolete. Functionality submitted as a PR to dae/anki                                                          |
| editor_sync_html_cursor          | :x:                  | BeautifulSoup                                                                                                  |
| main_fullscreen                  | :grey_question:      |                                                                                                                |
| main_ontop                       | (:white_check_mark:) | Child dialogs appear below main window                                                                         |
| overview_browser_shortcuts       | :x:                  | SIGNALS, Browser.onSearch                                                                                      |
| overview_deck_switcher           | :grey_question:      |                                                                                                                |
| overview_deck_tooltip            | :x:                  | tooltips not appearing, possible JS issue                                                                      |
| overview_refresh_media           | :x:                  | QWebSettings → no clearMemoryCaches()                                                                          |
| previewer_tag_browser            | :x:                  | Depends on Advanced Previewer which has not been converted, yet                                                |
| reviewer_auto_answer             | :white_check_mark:   |                                                                                                                |
| reviewer_auto_rate_hotkey        | :white_check_mark:   |                                                                                                                |
| reviewer_browse_*                | :x:                  | Reviewer._keyHandler, Browser.onFind                                                                           |
| reviewer_card_stats              | (:white_check_mark:) | Uses serif font (badly aliased); observed one segfault. Investigate if also present ankiplugins/cardstats.py   |
| reviewer_file_hyperlinks         | :white_check_mark:   | py.link bridge no longer exists                                                                                |
| reviewer_hide_toolbar            | :x:                  | obsolete, 2.1 has no toolbar                                                                                   |
| reviewer_hint_hotkeys            | :white_check_mark:   |                                                                                                                |
| reviewer_letitsnow               | (:white_check_mark:) | potential display issues with latest betas                                                                     |
| reviewer_more_answer_buttons     | :x:                  | Reviewer._keyHandler, complex changes to answer button methods                                                 |
| reviewer_progress_bar            | :white_check_mark:   |                                                                                                                |
| reviewer_puppy_reinforcement     | :x:                  | Reviewer.nextCard                                                                                              |
| reviewer_track_unseen            | :x:                  | PyQt4, SIGNALS, potentially obsolete                                                                           |
| reviewer_visual_feedback         | :x:                  | Reviewer._keyHandler , Reviewer._linkHandler                                                                   |
| sched_advanced_newcard_limits    | :white_check_mark:   |                                                                                                                |
| sched_deck_orgactions            | :white_check_mark:   |                                                                                                                |
| sched_filter_dailydue            | :grey_question:      |                                                                                                                |
| sched_ignore_lapses_below_ivl    | (:x:)                | Issues with new scheduler anticipated                                                                          |
| sched_sibling_spacing_whitelist  | :x:                  | SIGNALS, potentially other issues                                                                              |
| search_last_edited               | :white_check_mark:   |                                                                                                                |
| stats_true_retention_extended    | :white_check_mark:   |                                                                                                                |
| tagedit_enhancements             | :white_check_mark:   |                                                                                                                |
| tagedit_subtag_completer         | :white_check_mark:   |                                                                                                                |

