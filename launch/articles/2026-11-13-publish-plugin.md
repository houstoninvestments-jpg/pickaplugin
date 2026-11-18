---
title: "How to publish a Codex or ChatGPT plugin: three routes, no guesswork"
canonical: https://pickaplugin.com/guides/publish-codex-plugin
tags: ai, codex, tutorial, opensource
---

*Disclosure: I run [PickAPlugin](https://pickaplugin.com), an independent catalog of ChatGPT and Codex plugins. This is adapted from our guide on the same topic.*

You've built a plugin. There are three ways to get it in front of people, and most makers end up doing all three.

## 1. The official Plugins Directory (OpenAI review)

ChatGPT and Codex share one public plugin directory. On July 9, 2026 OpenAI moved the old ChatGPT app directory into it, so "submit a ChatGPT app" now means submitting a plugin. A plugin can be skills only, an MCP-backed app, or both.

You submit through the plugin submission portal on the OpenAI Platform:

- Upload the built package as a ZIP and fix any setup or validation errors the automated checks find.
- If it connects to an MCP server, include five positive test cases, three negative test cases, a video walkthrough and release notes. If sign-in is needed, give reviewers a test account that works without MFA or email codes.
- Fill in the listing details (name, logo, description, company and privacy policy URLs) and the policy attestations, then submit.

OpenAI says review timelines vary. After approval you choose when to publish.

## 2. Your own GitHub repo marketplace (no review)

You don't need approval to share a plugin. Put a `.agents/plugins/marketplace.json` in your repo that lists the plugin, and anyone can install it:

```bash
codex plugin marketplace add owner/repo
codex plugin add plugin-name@marketplace-name
```

Put those two lines at the top of your README. Test the install from a clean machine before you announce it.

## 3. Community directories

- **PickAPlugin** (ours): free listing, send the repo on the [submit page](https://pickaplugin.com/submit).
- **awesome-codex-plugins**: an awesome list that's also an installable marketplace; it requires a scanner score.
- **HOL Plugins** (hol.org/plugins): free directory with trust scores.
- Independent catalogs like CodexStacks, Codex Harness and Codex Marketplace.

## What helps people actually install it

- One plain sentence at the top of the README on what it does and who it's for.
- A copy-paste install line.
- A license file.
- Recent commits, since directories show the last update date.
- A clear statement of what it can read and write, especially if it runs hooks or shell commands.

The full version, with FAQ, is at [pickaplugin.com/guides/publish-codex-plugin](https://pickaplugin.com/guides/publish-codex-plugin).
