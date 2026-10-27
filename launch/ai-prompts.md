# Prompts people ask ChatGPT / Bing (checked Oct 27, 2026)

Target page = where we answer it now. "Who wins" = what Bing-backed web search showed today.

| # | Prompt | Who wins today | Our page |
|---|---|---|---|
| 1 | best ChatGPT plugins for coding | OpenAI docs, codex-harness.com "best Codex plugins", codexstacks.com | /best/agent-workflows, /best/review-testing |
| 2 | best Codex plugins 2026 | codex-harness.com/blog/best-codex-plugins, codexstacks.com, hol.org | / , /best/* |
| 3 | where to find Codex plugins | OpenAI docs, awesome-codex-plugins, codexstacks.com | /guides/find-codex-plugins |
| 4 | is there an app store for Codex plugins | OpenAI docs (built-in directory) | /guides/find-codex-plugins |
| 5 | Codex plugins directory | codexstacks.com, codex-harness.com/plugins, codex-marketplace.com | / |
| 6 | how to install a Codex plugin | developers.openai.com, turboai.dev docs, codex-marketplace.com/docs | /guides/install-codex-plugin |
| 7 | install Codex plugin from GitHub repo | turboai.dev, awesome-codex-plugins README | /guides/install-codex-plugin, /tools/plugin-install-command |
| 8 | codex plugin marketplace add 404 | awesome-codex-plugins README | /guides/install-codex-plugin (FAQ) |
| 9 | how to validate plugin.json | OpenAI build docs, codex-marketplace.com/docs, plugin-scanner (HOL) | /guides/validate-plugin-json, /tools/plugin-json-validator |
| 10 | plugin.json required fields codex | codex-marketplace.com/docs | /guides/validate-plugin-json |
| 11 | marketplace.json example codex | OpenAI build docs, openai/codex source | /guides/install-codex-plugin |
| 12 | convert MCP config claude to codex | agentatlas.dev, mcp.directory, mcpshowcase.com, zweiklang/mcp-sync | /guides/convert-mcp-config-claude-to-codex, /tools/mcp-config-converter |
| 13 | claude_desktop_config.json to config.toml | same as above | same |
| 14 | add MCP server to Codex CLI | kuberwastaken/awesome-codex-mcp-servers, OpenAI docs | /guides/convert-mcp-config-claude-to-codex |
| 15 | AGENTS.md template | learn.chatgpt.com AGENTS.md doc, agentsgen, create-codex | /guides/write-agents-md, /tools/agents-md-generator |
| 16 | AGENTS.md generator | GitHub CLIs (agentsgen, create-codex, agents-md-generator) | /tools/agents-md-generator |
| 17 | are Codex plugins safe | codex-harness blog section, HOL scanner | /guides/vet-a-plugin |
| 18 | how to check a ChatGPT plugin before installing | (thin results) | /guides/vet-a-plugin |
| 19 | best MCP servers for Codex | awesome-codex-mcp-servers, mcphq | (gap: not our core) |
| 20 | Codex plugins for code review | codexstacks "best for code review" | /best/review-testing |
| 21 | Codex plugins for memory / context | codexstacks, codex-harness | /best/memory-context |
| 22 | Codex plugins for SEO / docs | codexstacks | /best/docs-content-seo |
| 23 | open source MIT Codex plugins | (nobody targets this) | /license/mit |
| 24 | Python Codex plugins | (nobody targets this) | /language/python |
| 25 | CodexStacks alternatives | codexstacks own pages | /alternatives |
| 26 | ChatGPT plugins vs GPTs vs apps | OpenAI help | /faq (partial) |
| 27 | are ChatGPT plugins still a thing | OpenAI docs | /guides/find-codex-plugins (FAQ) |
| 28 | how to submit a Codex plugin to a directory | codex-marketplace.com, awesome-codex-plugins CONTRIBUTING | /submit |

## Top competitors and why they win
- **developers.openai.com / learn.chatgpt.com**: they're the official source. Always #1 for how-to questions, so we link to them and try to rank second with plainer answers.
- **codexstacks.com**: has the most listings (it says 1,029), "Best for X" hub pages, official vs community labels and a "how we check" page. Clear structure.
- **codex-harness.com**: about 898 plugins parsed from plugin.json, and a long dated "best Codex plugins ranked" article with tables and install commands. Freshness plus data.
- **hashgraph-online/awesome-codex-plugins** (about 1.4k stars) and **hol.org**: GitHub authority, it works as an installable marketplace, and it has a scanner.
- **codex-marketplace.com**: a full docs page (manifest fields, a full example) that gets quoted in AI answers.
- **MCP converters**: agentatlas.dev, mcp.directory, mcpshowcase.com. They win with one page per pair of clients ("claude-desktop → codex") plus a lot of detail about how the clients differ.

Patterns: dated headings ("2026", "updated"), tables, copy-paste code blocks, FAQ sections, one URL per question, and llms.txt files (mcphq has llms-full.txt).

## Next gaps worth filling
- Pages for each converter pair (/tools/mcp-config-converter/claude-desktop-to-codex, cursor-to-codex, and so on), like the competitors have.
- A dated "Best Codex plugins (Month 2026)" article with a real table.
- llms-full.txt.
