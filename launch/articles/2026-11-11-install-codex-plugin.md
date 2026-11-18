---
title: "How to install a Codex plugin: CLI, app and GitHub repos"
canonical: https://pickaplugin.com/guides/install-codex-plugin
tags: ai, codex, tutorial, productivity
---

*Disclosure: I run [PickAPlugin](https://pickaplugin.com), an independent catalog of ChatGPT and Codex plugins. This is adapted from our guide on the same topic.*

There are basically three ways a plugin gets onto your machine: the built-in directory, a GitHub repo that ships a marketplace, or a folder you made yourself. Here's each one.

## 1. From the built-in directory (easiest)

In the Codex app or ChatGPT desktop app, open Plugins, search, open the plugin and hit install. In the CLI, start `codex` and type `/plugins`. Plugins in the OpenAI tab are the ones OpenAI curates, so this is the low-risk route.

## 2. From a GitHub repo

Most community plugins live in a repo that has a `.agents/plugins/marketplace.json` (or the older `.claude-plugin/marketplace.json`). You add the repo as a marketplace once, then install by name:

```bash
codex plugin marketplace add owner/repo
codex plugin list
codex plugin add plugin-name@marketplace-name
```

The marketplace name comes from the `name` field in that repo's marketplace.json, and `codex plugin list` shows it.

Point it at the repo, not the raw marketplace.json URL. The command clones a git repo, so a raw file link fails with a 404.

## 3. From a local folder

Put the plugin in `./plugins/my-plugin` (repo) or `~/.codex/plugins/my-plugin` (personal), then list it in `.agents/plugins/marketplace.json` with `"source": {"source": "local", "path": "./plugins/my-plugin"}`. Restart the app and it shows up.

## Before you install anything from GitHub

Community plugins can bundle hooks, MCP servers and shell commands. Spend two minutes on the repo: when was the last commit, what does `.mcp.json` start, are there hooks.

## Quick answers

- **Where do plugins get installed?** Into `~/.codex/plugins/cache/MARKETPLACE/PLUGIN/VERSION/`. Local plugins use the version `local`.
- **How do I remove one?** `codex plugin remove plugin-name@marketplace`, or uninstall from the Plugins view in the app.
- **Why a 404 on `marketplace add`?** Usually a raw marketplace.json URL. Give it the repo instead.

The full guide, with an install command finder, is at https://pickaplugin.com/guides/install-codex-plugin
