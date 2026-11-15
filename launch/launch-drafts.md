# Launch drafts (NOT posted) — 2026-11-15

All numbers from https://pickaplugin.com/reports/2026-11 (data through 2026-11-14). Post from Aaron's own accounts only after he approves. Reply to comments personally for the first couple of hours.

---

## 1. Show HN

**Title:** Show HN: PickAPlugin – search 550 MCP servers and Codex/Claude plugins from your agent

**URL:** https://pickaplugin.com/mcp-server

**Text:**

I kept losing time figuring out which MCP server or Codex/Claude Code plugin to use for something, because the good ones are scattered across a dozen awesome-lists and GitHub searches. So I built a catalog of them, and then put the catalog behind an MCP server so your agent can do the looking.

It's at https://pickaplugin.com/mcp (Streamable HTTP, no auth, read-only):

    claude mcp add --transport http pickaplugin https://pickaplugin.com/mcp
    codex mcp add pickaplugin --url https://pickaplugin.com/mcp

Four tools: search_plugins, get_plugin, list_categories, top_plugins. Ask "find me an MCP server for Postgres migrations" and it returns matching listings with stars, license, last push and the install command from the README. It's also in the official MCP Registry as com.pickaplugin/pickaplugin.

Some numbers from this month's catalog report (https://pickaplugin.com/reports/2026-11), all from public GitHub data:

- 161 new plugins joined in the first two weeks of November (550 total now)
- The median new listing had 2 stars
- 32% of new plugins had no copyable install command in their README
- 54% of non-archived repos got a push in the last 7 days
- claude-seo gained 4,322 stars this month, the most in the catalog

Upfront: it's a side project and traffic is small. There are paid featured listings, and they rank first in results but are always marked featured: true, so you or your agent can ignore them. Everything else is ordered by relevance, not money. Descriptions are written from each project's README. We don't audit plugins, so check one before you install it.

Would love feedback on the search results, missing plugins, or what else the server should expose.

---

## 2. r/mcp

**Title:** I made a remote MCP server for finding other MCP servers (550 indexed, no auth)

**Flair:** Showcase / server (whichever the sub offers for self-made servers)

**Body:**

Small thing I built because I got tired of digging through awesome-lists: a free, read-only remote MCP server that searches a catalog of 550 MCP servers, Codex plugins, Claude Code plugins and agent skills.

Endpoint: `https://pickaplugin.com/mcp` (Streamable HTTP, no auth)

    claude mcp add --transport http pickaplugin https://pickaplugin.com/mcp

Tools:
- `search_plugins(query, category?, limit?)`
- `get_plugin(slug)`: stars, license, last push, install command
- `list_categories()`
- `top_plugins(category?, limit?)`

It's in the official registry as `com.pickaplugin/pickaplugin`. Docs: https://pickaplugin.com/mcp-server

A few things I noticed while building the November report (https://pickaplugin.com/reports/2026-11):
- 161 new servers/plugins showed up in the first two weeks of November
- the median new one has 2 stars
- 32% of new ones have no copy-paste install command in the README, which makes them a lot harder to try
- 23% of new listings install via `mcp add`, 31% are Claude Code plugins

Disclosure: I run the directory. There are paid featured listings. They show first but are always flagged `featured: true`. Free to submit yours at https://pickaplugin.com/submit.

Feedback on result quality is very welcome, and so are bug reports from clients I haven't tested.

---

## 3. r/ClaudeAI

**Title:** Let Claude find MCP servers for you: free remote MCP server that searches 550 of them

**Flair:** use the sub's project/showcase flair. Only pick "Built with Claude" if that's actually how it was built.

**Body:**

If you use Claude Code or Claude Desktop with MCP, you've probably done the "which server should I use for X" hunt across GitHub and five awesome-lists. I built a catalog of 550 MCP servers, Claude Code plugins, Codex plugins and skills, and exposed it as a remote MCP server so Claude can search it directly.

Claude Code:

    claude mcp add --transport http pickaplugin https://pickaplugin.com/mcp

Claude Desktop / claude.ai: add a custom connector with the URL `https://pickaplugin.com/mcp` (no auth).

Then just ask things like "find me a memory MCP server that stores everything locally" or "what are the most-starred Claude Code plugins for code review". It returns stars, license, last push date and the install command.

Free, no signup, read-only, stores nothing beyond normal server logs. Setup notes for each client: https://pickaplugin.com/mcp-server

Some Claude-relevant numbers from this month's report (https://pickaplugin.com/reports/2026-11):
- 50 of the 161 new listings this month (31%) were Claude Code plugins
- claude-seo gained 4,322 GitHub stars this month, the most of anything we track
- 32% of new plugins don't have a copy-paste install command, which is a big reason I wanted the agent to read READMEs for me

Disclosure: it's my project. Paid featured listings exist, show first, and are always labeled `featured: true`.

---

## 4. r/cursor

**Title:** Free MCP server for Cursor that searches 550 other MCP servers and agent plugins

**Flair:** Showcase (or Resources & Tips if Showcase isn't allowed for self-promo that day)

**Body:**

I built a catalog of 550 MCP servers and coding-agent plugins and put a remote MCP server in front of it, so Cursor's agent can look things up instead of you tab-hopping through GitHub.

Add it to `~/.cursor/mcp.json` (or the project's `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "pickaplugin": { "url": "https://pickaplugin.com/mcp" }
  }
}
```

No API key, read-only. Then ask the agent something like "find an MCP server for Playwright testing and show me the install command".

What it returns per listing: description, category, GitHub stars, license, last push and the install command from the README. Docs: https://pickaplugin.com/mcp-server

From this month's report (https://pickaplugin.com/reports/2026-11): 161 new plugins in the first half of November, 54% of tracked repos pushed in the last week, and about a third of new ones ship without a copyable install command.

Disclosure: I run it. There are paid featured listings, always marked `featured: true` in results. Free submissions at https://pickaplugin.com/submit. Happy to hear what breaks.

---

### Posting notes
- Check each sub's current rules and self-promo ratio before posting. r/ClaudeAI and r/cursor both limit self-promotion and require the right flair. Space the posts out (one a day). Don't cross-post the same text.
- Show HN: weekday morning US time. Don't ask anyone to upvote.
- Verify the Cursor mcp.json `url` form works in the current Cursor build before posting.
