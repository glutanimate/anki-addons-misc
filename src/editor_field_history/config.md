**Important**: These settings do not sync and require a restart to apply.

- `historyWindowShortcut` (string): Hotkey that invokes the history window. Default: `"Ctrl+Alt+H"`.
- `fieldRestoreShortcut` (string): Hotkey that restores current field to last state. Default: `"Alt+Z"`.
- `partialRestoreShortcut` (string): Hotkey that restores fields listed in `partialRestoreFields`. Default: `"Alt+Shift+Z"`.
- `fullRestoreShortcut` (string): Hotkey that restores all fields at once, tags included: `"Ctrl+Alt+Shift+Z"`.
- `partialRestoreFields` (list): List of fields to restore when using `partialRestoreShortcut` (e.g. `["Front", "Sources"]`. Default: `[]`.
- `maxNotes` (int): Maximum number of notes to query when checking field history. Default: `100`
