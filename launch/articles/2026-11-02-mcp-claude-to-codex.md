Full disclosure up front: I run [PickAPlugin](https://pickaplugin.com), a free directory of ChatGPT and Codex plugins, and I built a small converter while doing this move myself. You don't need it, though. Everything below works by hand.

## Same servers, different wrapper

Claude Desktop and Cursor keep MCP servers in JSON. Codex keeps them in TOML, in `~/.codex/config.toml` (or `.codex/config.toml` inside a trusted project). The servers themselves don't change at all. Only the config format does.

Here's a server in Claude's JSON:

```json
{"mcpServers": {
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"]
  }
}}
```

And the same server in Codex's TOML:

```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

Each server becomes its own `[mcp_servers.NAME]` table. The CLI and the IDE extension both read the same file.

## Things that bit me

- **`env` becomes an inline table.** So `"env": {"API_KEY": "..."}` turns into `env = { API_KEY = "..." }`.
- **Remote servers use `url`.** Put any headers in `http_headers`.
- **Keep tokens out of the file.** For remote servers, `bearer_token_env_var` points Codex at an environment variable instead of pasting the token into `config.toml`.
- **You don't have to touch the server.** Local stdio servers run the same command everywhere.

## Or skip the file and use the CLI

```bash
codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp list
```

## Where the old config lives

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## If you have a lot of them

Converting one or two by hand is fine. If you've got ten, I put a paste-and-convert page here: [MCP config converter](https://pickaplugin.com/tools/mcp-config-converter). It runs in your browser and nothing gets uploaded. It goes the other way too, TOML back to JSON.

The longer version of this guide is on [pickaplugin.com](https://pickaplugin.com/guides/convert-mcp-config-claude-to-codex).
