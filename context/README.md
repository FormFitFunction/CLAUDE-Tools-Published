# context

**Type:** mod

## What it is

Shows how full this session's context window is, as one line of text on the Claude desktop app's status line: `context 7% · 72.6k/1M` (the app adds the plugin name as a prefix). For what is inside the window, use the built-in `/context`. A fuller version with an expanded card, chip and `/ctx` command exists but is not published.

## How to use it

Point Claude at the folder. For the desktop app, add to `~/.claude/settings.json` (then start a new Code-tab session):

```json
"env": {
  "CLAUDE_CODE_PLUGIN_DIRS": "<path-to>/context",
  "CLAUDE_CODE_PLUGIN_DIR_WATCH": "1"
}
```

Test with the app's bundled `claude` (the one on PATH may predate `plugin test`), run from the folder that holds the `context` folder:

```
claude plugin test context
claude plugin validate context
```

## Notes

- Design and constraints: `DESIGN.md`.
- Reads `$.session.usage()` with no breakdown, which is free, on session start, turn complete and after compaction. The line is cleared until the window has had its first response.
- The status line's size, position and `context` prefix belong to the app; a mod cannot change them.
- Local sessions only. `tsc` type-checking has not been run (TypeScript not installed).
