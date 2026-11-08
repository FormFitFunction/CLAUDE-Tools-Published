# CLAUDE Tools - Published

A small collection of tools made for Claude Code (or your AI harness of choice). Skills, agents, mods, and patterns. 

## Tools

| Tool | Type | Version | Purpose |
| ---- | ---- | ------- | ------- |
| [context](./Claude%20Mods/context/) | mod | 0.5.0 | Shows how full the session's context window is on the status line. Created for use with the Claude desktop app, after they removed the per-session context window UI element around 10/15/2026. Use this mod for an at-a-glance view, and use Claude's built in `/context` skill to see exact context window breakdown. |
| [phone-qr](./Skills/phone-qr/) | skill | 0.1.0 | Shows a QR code that opens a local dev server on your phone, over Tailscale or home Wi-Fi. Triggers on its own when you want to see something on a real device, and fixes servers that only listen on localhost. |

### Preview: context mod

![context mod showing context window usage on the Claude desktop app status line](./Preview%20Images/context-claude-mod.PNG)

Each tool lives in its own folder, is self-contained, and has its own `README.md` with install and usage instructions.

## Using a tool

Download or clone this repo and copy the tool's folder into your own project or Claude setup, following that tool's README. Copies are snapshots; re-copy to update.

## License

[MIT](./LICENSE). Provided as is, with no warranty or support.
