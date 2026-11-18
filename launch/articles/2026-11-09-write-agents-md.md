---
title: "How to write an AGENTS.md for Codex (with a starter template)"
canonical: https://pickaplugin.com/guides/write-agents-md
tags: ai, codex, productivity, tutorial
---

*Disclosure: I run [PickAPlugin](https://pickaplugin.com), an independent catalog of ChatGPT and Codex plugins. This is adapted from our guide on the same topic.*

AGENTS.md is a plain markdown file that Codex reads before it touches your repo. Think of it as the note you'd leave a new teammate on their first day.

## What to put in it

- How to install, run, test and lint, with the exact commands.
- Code style rules that aren't obvious from the code.
- What not to touch: generated files, secrets, migrations.
- How you want PRs and commit messages written.

## A starter template

```markdown
# AGENTS.md

## Setup
- Install: `npm install`
- Dev server: `npm run dev`
- Tests: `npm test` (run before every commit)
- Lint: `npm run lint`

## Style
- TypeScript, strict mode. No `any` unless commented why.
- Prefer small functions and named exports.

## Don't touch
- `dist/` and other generated files
- `.env*` files and anything holding secrets
- `migrations/` unless the task is a migration

## PRs
- One focused change per PR.
- Commit messages: imperative mood, under 72 characters.
```

## Where Codex looks

- `~/.codex/AGENTS.md` holds global defaults.
- Then Codex reads every `AGENTS.md` from the repo root down to your working folder. Closer files win.
- `AGENTS.override.md` beats `AGENTS.md` in the same folder.
- The combined size is capped at 32 KiB by default, so keep it tight.

## Common questions

**Do other tools read AGENTS.md?** Yes, it's an open format. Cursor, Aider, Jules, Zed and others read it too.

**Should I commit it?** Yes, at the repo root, so everyone (and every agent) gets the same rules.

If you'd rather not start from a blank file, there's a free in-browser [AGENTS.md generator](https://pickaplugin.com/tools/agents-md-generator) that builds one from a few questions. The original guide is [here](https://pickaplugin.com/guides/write-agents-md).
