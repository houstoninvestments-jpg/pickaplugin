---
title: "Why your Codex plugin doesn't show up: a plugin.json checklist"
canonical: https://pickaplugin.com/guides/validate-plugin-json
tags: ai, codex, tutorial, debugging
---

*Disclosure: I run [PickAPlugin](https://pickaplugin.com), an independent catalog of ChatGPT and Codex plugins. This is adapted from our guide on the same topic.*

Codex is pretty quiet when a manifest is wrong. The plugin just doesn't show up, and there's no error to chase. Here's what the manifest needs and the mistakes that trip people up most.

## What it needs

- `name`: kebab-case (`my-plugin`, not `My Plugin`). It's the id.
- `version`: semver, like `0.1.0`.
- `description`: one clear sentence.
- The file lives at `.codex-plugin/plugin.json`. Only that file goes in that folder. Skills, `.mcp.json` and hooks live at the plugin root.

A minimal manifest:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Does one useful thing for your agent."
}
```

## The mistakes we see most

1. Paths that don't start with `./`, or absolute paths like `/Users/me/...`.
2. Paths with `..` that point outside the plugin.
3. Marketplace entries missing `source` or `policy`.
4. Secrets pasted into the manifest. Use environment variables instead.

## Check it quickly

We keep a free [plugin.json validator](https://pickaplugin.com/tools/plugin-json-validator). It runs in your browser (nothing is uploaded) and flags errors, warnings and nice-to-haves. It also checks marketplace.json.

## Is there an official schema?

OpenAI documents the fields in its plugin build docs, and many manifests reference the agent-plugins.org schema in `$schema`. The validator checks the commonly documented rules.

The full guide is at [pickaplugin.com/guides/validate-plugin-json](https://pickaplugin.com/guides/validate-plugin-json).
