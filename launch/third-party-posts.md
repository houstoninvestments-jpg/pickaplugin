# Third-party posts (drafts, NOT posted)

Where they could go for free without a phone number (as far as I know, needs a re-check when signing up):
- **dev.to**: sign up with GitHub or email, no phone. You can set a canonical URL. Tags: #ai #openai #codex #mcp.
- **Hashnode**: email, GitHub or Google sign-in, no phone needed for a personal blog.
- **Medium**: email or Google sign-in, no phone needed to publish (but distribution is weak without publications).
- Also: GitHub Discussions / a gist, and Indie Hackers (email).
Disclose in each one that it's my own site.

---

## 1. dev.to: "I moved my MCP servers from Claude to Codex. Here's the cheat sheet"

Full disclosure up front: I run PickAPlugin, a free directory of ChatGPT/Codex plugins, and I built a converter while doing this. But the cheat sheet below works without it.

Claude Desktop and Cursor keep MCP servers in JSON. Codex keeps them in TOML at `~/.codex/config.toml`. Same servers, different wrapper.

```json
{"mcpServers": {"context7": {"command": "npx", "args": ["-y", "@upstash/context7-mcp"]}}}
```
becomes
```toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
```

Things that bit me:
- `env` turns into an inline table: `env = { API_KEY = "..." }`. Better: use `bearer_token_env_var` for remote servers so the token isn't sitting in the file.
- Remote servers use `url` plus `http_headers`.
- If you're lazy like me: `codex mcp add context7 -- npx -y @upstash/context7-mcp`.

If you've got 10 of them, I put a paste-and-convert page here (it runs in your browser, nothing gets uploaded): https://pickaplugin.com/tools/mcp-config-converter
Longer write-up: https://pickaplugin.com/guides/convert-mcp-config-claude-to-codex

---

## 2. Hashnode: "Your Codex plugin isn't showing up? Check these 5 things in plugin.json"

(I run pickaplugin.com, a directory of these plugins. I've read a few hundred manifests by now.)

1. `name` has to be kebab-case. `My Plugin` won't work, `my-plugin` will.
2. Only `plugin.json` goes in `.codex-plugin/`. Skills, `.mcp.json` and hooks go at the plugin root.
3. Paths start with `./`. No `/Users/you/...`, no `..`.
4. In a marketplace.json, every entry needs a `source` (and you'll want a `policy`).
5. When you add a repo with `codex plugin marketplace add`, give it the repo, not the raw marketplace.json URL. Otherwise you get a 404.

Free in-browser checker if you want it: https://pickaplugin.com/tools/plugin-json-validator

---

## 3. Medium: "There are 1,000+ Codex plugins now. Here's how I pick one in 2 minutes"

Honest map of where to look:
- **Built-in Plugins directory** in ChatGPT/Codex: start here for official ones.
- **awesome-codex-plugins** on GitHub: curated, and you can add it as a marketplace.
- **CodexStacks / Codex Harness**: the biggest indexes, good if you want to see everything.
- **PickAPlugin** (mine): smaller and hand-sorted into plain categories, with last update, license and install command on every listing. https://pickaplugin.com

Then the 2-minute check: last commit, what `.mcp.json` and hooks run, what it asks for, who made it, the license. Checklist: https://pickaplugin.com/guides/vet-a-plugin
