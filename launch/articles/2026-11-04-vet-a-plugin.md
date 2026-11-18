---
title: "How I vet a Codex plugin or MCP server in about two minutes"
canonical: https://pickaplugin.com/guides/vet-a-plugin
tags: ai, mcp, security, codex
---

Plugins and MCP servers are easy to install, and that's the problem. A plugin can bundle hooks and MCP servers, and both run code on your machine. Nobody audits every community plugin (we don't either), so here's the quick check I run before installing anything.

*Disclosure: I run [PickAPlugin](https://pickaplugin.com), an independent, hand-sorted catalog of ChatGPT and Codex plugins. This checklist is adapted from our guide, and it works no matter where you found the plugin.*

## 1. Is it alive?

Look at the last commit, the open issues, and whether the repo is archived. A plugin that hasn't been touched in a long time may still work, but you'll be on your own when something in the host app changes.

## 2. What does it actually run?

Open `.mcp.json` and any `hooks.json` before you install. These are the parts that execute:

- **MCP servers** start a process (often `npx`, `uvx`, or a binary) that your agent talks to.
- **Hooks** run commands on events like tool calls or session start.

If you can't tell what a command does, look it up before letting it run.

## 3. What does it ask for?

Tokens, filesystem access, network access. Then ask whether that matches what it says it does. A Markdown formatter that wants your GitHub token deserves a closer look.

I boil this down to three questions:

1. What can it read?
2. What can it write or send?
3. Where does my data go?

If the README can't answer those on one screen, I usually skip it.

## 4. Who made it?

A known company or a maintainer with a history of active projects is a better bet than a brand-new account with one repo. It's not proof of anything, just a signal.

## 5. Is there a license?

No license means you technically can't reuse the code. It also tells you how much thought went into publishing it.

## 6. Is the manifest sane?

Check `plugin.json` for absolute paths, hardcoded secrets, or fields pointing somewhere unexpected. Those are red flags. We built a free [plugin.json validator](https://pickaplugin.com/tools/plugin-json-validator) that catches the common problems in the browser.

## What about official plugins?

Plugins in the built-in directory are curated by OpenAI, which is a real signal. It's still worth knowing what you're connecting, especially anything that touches email, files, or deploys.

## The short version

Alive, what it runs, what it asks for, who made it, license, manifest. Two minutes, and you'll skip most of the sketchy stuff. The full checklist lives at [pickaplugin.com/guides/vet-a-plugin](https://pickaplugin.com/guides/vet-a-plugin).

What's on your own checklist? I'd like to hear what I'm missing.
