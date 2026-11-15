# PickAPlugin MCP server: directory submissions

Server: https://pickaplugin.com/mcp (Streamable HTTP, no auth, read-only). Docs: https://pickaplugin.com/mcp-server
All free. Skip anything that asks for payment (note it here, don't pay).

## Status log

| Directory | How | Status (2026-11-15) | Link |
|---|---|---|---|
| Official MCP Registry | mcp-publisher, DNS auth (apex TXT `v=MCPv1; k=ed25519; ...` added in Cloudflare, record id 9ef268a5201f9ae3a934eff4cf92cca6) | **LIVE** as `com.pickaplugin/pickaplugin` v1.0.0, status active | https://registry.modelcontextprotocol.io/v0/servers?search=pickaplugin |
| jaw9c/awesome-remote-mcp-servers | GitHub PR | PR open (#2359) | https://github.com/jaw9c/awesome-remote-mcp-servers/pull/2359 |
| docker/mcp-registry | GitHub PR (servers/pickaplugin, remote, no OAuth) | PR open (#7167) | https://github.com/docker/mcp-registry/pull/7167 |
| punkpeye/awesome-remote-mcp-servers | GitHub PR | **Blocked until Glama connector exists**. Their rules require a Glama connector badge. Glama connector IDs mirror registry names, so check https://glama.ai/mcp/connectors/com.pickaplugin/pickaplugin (404 today). Once it's 200, PR the entry below under "Aggregators". | |
| punkpeye/awesome-mcp-servers | n/a | Not eligible (remote-only servers go to the remote list above) | |
| PulseMCP, other registry mirrors | auto-ingest from the official registry | Watch, nothing to submit | https://www.pulsemcp.com/servers?q=pickaplugin |
| Smithery | browser | TODO | https://smithery.ai/new |
| Glama | browser | TODO (may auto-import from registry, check first) | https://glama.ai/mcp/servers |
| mcp.so | browser | TODO | https://mcp.so/submit |
| MCP Market | browser | TODO | https://mcpmarket.com/submit |
| mcpservers.org | browser (form, free option only) | TODO | https://mcpservers.org/submit |
| cursor.directory | browser (GitHub sign-in) | TODO | https://cursor.directory/mcp/new |
| LobeHub | browser | TODO | https://lobehub.com/mcp |
| HOL (hashgraph-online) | browser / their registry form | TODO (they already link us in awesome-codex-plugins) | https://hol.org |

Entry for punkpeye/awesome-remote-mcp-servers (Aggregators), once the Glama badge works:
```
- [PickAPlugin](https://pickaplugin.com/mcp-server) `https://pickaplugin.com/mcp`
  [![PickAPlugin MCP connector](https://glama.ai/mcp/connectors/com.pickaplugin/pickaplugin/badges/score.svg)](https://glama.ai/mcp/connectors/com.pickaplugin/pickaplugin)
  🔓 - Searches a catalog of 550+ MCP servers, Codex/Claude plugins and agent skills, with stars and install commands.
```

## Fields for the browser forms (copy exactly)

- **Name:** PickAPlugin
- **Server URL / endpoint:** https://pickaplugin.com/mcp
- **Transport:** Streamable HTTP (remote). **Auth:** none
- **Website / docs:** https://pickaplugin.com/mcp-server
- **GitHub repo:** https://github.com/houstoninvestments-jpg/pickaplugin (subfolder `plugin/`)
- **Official registry name:** com.pickaplugin/pickaplugin
- **Short description (≤100 chars):** Search a directory of 550+ MCP servers, Codex/ChatGPT/Claude plugins and agent skills.
- **Long description:** PickAPlugin is a free, read-only remote MCP server for finding other MCP servers and agent plugins. Ask your agent things like "find me a Postgres MCP server" and it searches a hand-sorted catalog of 550+ MCP servers, Codex plugins, Claude Code plugins and skills, refreshed daily from GitHub. Each result includes the description, category, GitHub stars, license, last push and the install command from the README. No API key, no signup. Paid featured listings rank first and are always marked featured: true.
- **Tools:** `search_plugins(query, category?, limit?)`, `get_plugin(slug)`, `list_categories()`, `top_plugins(category?, limit?)`
- **Install lines:**
  - `claude mcp add --transport http pickaplugin https://pickaplugin.com/mcp`
  - `codex mcp add pickaplugin --url https://pickaplugin.com/mcp`
  - Cursor `mcp.json`: `{"mcpServers":{"pickaplugin":{"url":"https://pickaplugin.com/mcp"}}}`
- **Category:** Search (fallbacks: Developer Tools, Aggregators/Directories)
- **Tags:** mcp-directory, search, plugins, codex, claude-code, developer-tools, remote, no-auth
- **Logo:** /workspace/pickaplugin/plugin/assets/logo.png (128×128 PNG). Hosted copy: https://raw.githubusercontent.com/houstoninvestments-jpg/pickaplugin/main/plugin/assets/logo.png
- **Contact:** hello@pickaplugin.com
- **License:** none declared on the repo. Leave blank or "Proprietary/free to use" if forced. Don't claim MIT.
- **Pricing:** Free

## Registry upkeep
- Key: /workspace/pickaplugin/.secrets/mcp_registry_key.pem (+ .hex). Git-ignored, never print.
- Re-publish: bump `version` in plugin/server.json, then `cd plugin && mcp-publisher login dns --domain pickaplugin.com --private-key "$(cat ../.secrets/mcp_registry_key.hex)" && mcp-publisher publish`.
  (The installed CLI has no --private-key-file flag.)
- Keep the apex TXT record. Removing it blocks future publishes but doesn't unlist the current one.
