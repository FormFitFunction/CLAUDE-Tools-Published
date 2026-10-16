# context: design

A Claude Code mod that shows how full this session's context window is, as one line on the Claude desktop app's status line. Local Code-tab sessions only.

## Decisions

| Topic | Decision |
| --- | --- |
| Display | `$.ui.status("7% · 72.6k/1M")`: percent of the window, then tokens out of the window. The app draws it on its own row, prefixed with the plugin name (hence the name `context`). |
| Data | `$.session.usage()` with no arguments: `context.tokens` (input tokens of the last response) and `context.window`. No breakdown is requested, so a refresh is free. |
| When | `session.start`, `turn.complete`, and after `session.compact`. The line is cleared (`undefined`) while `context.tokens` is absent: a fresh or just-compacted window. A failed read keeps the last line. |
| State | None. The status line is the only output, so there are no atoms, no `types/` contract and no render hooks. |
| Details | The built-in `/context` shows what is in the window. |

## Structure

```
.claude-plugin/plugin.json
hooks/hooks.json
hooks/register.ts      the three refresh hooks
hooks/format.ts        fmtTokens and statusLabel (pure)
hooks/usage-fixture.ts a SessionUsage for tests
hooks/*.test.ts        tests
```

## What the app does not let a mod do

Confirmed while building the fuller version, kept as `context-mod-full`:

- The `AbovePrompt` band is drawn in a grey rounded frame whatever sits in it, so a chip there is boxed. A `Button` and a Markdown link both were.
- `SessionMode` footer labels are not drawn by the desktop.
- A mod cannot set a font size, hide the status line's plugin-name prefix, or add to the app's own usage ring.

## Tests

TDD, red first. `format.test.ts` covers the token formatting and the label (percent, window size, no reading yet, over 100%). `status.test.ts` covers the line being set on session start, turn complete and compaction, cleared when there is nothing to show, left alone when usage cannot be read, and never asking for a breakdown. Run with `claude plugin test` from the folder that holds the mod folder, using the app's bundled `claude`.
