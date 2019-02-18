**Important**: These settings do not sync and require a restart to apply.

- `onlineSearchProviders` (dict): Dictionary of search providers to add to the context menu. Each entry consists of a key, the name of the entry, and a value. 

    The value may either be:
      - a single string, denoting the URL to open (e.g. `"name": "url"`),
      - a list of multiple URLs to open at once (e.g. `"name": ["url1", "url2"]`),
      - a subdictionary to group multiple menu entries under a separate submenu (e.g. `"submenu": {"name1": "url1", "name2": "url2"}`)

    Any occurences of the placeholder `%s` in your URLs will be replaced with the actual search term.

    For examples on all of the variations above, please refer to the default configuration of the add-on.

- `localSearchEnabled` (true/false): Whether to show menu entry for searching in card browser. Default: `true`.
- `useCustomStylesheet` (true/false): Whether to use alternate, more compact, menu styling. Might be buggy, so better left off. Default: `false`.

Created with ❤️ by [Glutanimate](https://glutanimate.com/). If you enjoy this add-on please consider **[supporting me on Patreon](https://www.patreon.com/bePatron?u=7522179)**. Thanks!