# Changelog

All notable changes to this tool. Newest first. Bump `VERSION` with each entry.
Uses semver: MAJOR (breaking), MINOR (additive), PATCH (fix/no-behavior-change).

## [0.5.0] - 2026-10-14

- Slimmed to the status line only. The card, `/ctx`, the paged lists, the per-session state and the breakdown request are gone, so a refresh no longer estimates anything. The full version lives on as `context-mod-full`.

## [0.4.0] - 2026-10-14

- Renamed the plugin from `ctx-meter` to `context` (the app prefixes the status line with the plugin name). Removed the unused footer label.

## [0.3.0] - 2026-10-14

- Adds the meter to the prompt footer's mode labels (`SessionMode`), and shortens the label to `7% · 72.6k/1M` for it and the status line. The card and `/ctx` stay, dormant.

## [0.2.0] - 2026-10-14

- The meter moves to the status line (plain text, no framed band). `/ctx` toggles the expanded card; the collapsed band draws nothing. Removes the chip, its colours and the Markdown experiment.

## [0.1.2] - 2026-10-14

- Chip is a Markdown link instead of a `Button`, to avoid the desktop's native button box. Experimental: not yet seen drawing.

## [0.1.1] - 2026-10-14

- Chip text is muted (`dimColor`); colour only on the ring, in soft amber and red.
- Ring fills against the window and rounds to the nearest glyph, so it agrees with the percent (24% no longer draws a half ring).

## [0.1.0] - 2026-10-14

- Initial version: ring chip above the prompt, `/context`-style card with stacked bar, category rows and paged MCP tool, memory file and skill lists. Not yet seen drawing in the desktop app.
