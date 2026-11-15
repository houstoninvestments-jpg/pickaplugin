# PickAPlugin plugin (Codex / Claude Code)

Search the [PickAPlugin](https://pickaplugin.com) catalog of ChatGPT, Codex and Claude plugins and MCP servers from your agent.
It wraps the free, read-only remote MCP server at `https://pickaplugin.com/mcp` (Streamable HTTP, no auth).

Tools: `search_plugins(query, category?, limit?)`, `get_plugin(slug)`, `list_categories()`, `top_plugins(category?, limit?)`.
Paid featured listings rank first and are always marked `featured: true`.

Just want the server? See https://pickaplugin.com/mcp-server for one-line installs:

```
claude mcp add --transport http pickaplugin https://pickaplugin.com/mcp
codex mcp add pickaplugin --url https://pickaplugin.com/mcp
```

[![Listed on PickAPlugin](https://pickaplugin.com/badge/listed.svg)](https://pickaplugin.com)
