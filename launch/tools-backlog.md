# Free tools backlog (after the first 4 shipped 2026-10-27)

Live: /tools, plugin-json-validator, mcp-config-converter, plugin-install-command, agents-md-generator.

Next, roughly best first:
1. **SKILL.md frontmatter checker**: paste a SKILL.md and check name/description frontmatter, length, YAML gotchas. Few web tools; mostly CLIs (skillsaw, codex-plugin-doctor).
2. **OpenAI token and cost calculator**: high search volume, but crowded (tokenestimate.com, apicost.app) and prices change often. Only build it if prices are pulled from OpenAI's pricing page with a "checked on" date, never hardcoded and left to go stale.
3. **marketplace.json generator**: form → .agents/plugins/marketplace.json (policy, category, source types local/url/git-subdir/npm). Pairs with the validator.
4. **mcp.json (Agent Plugins) auth block builder**: oauth / dcr / cimd / api_key `extensions.com.openai.auth`. Docs are dense, and nobody has a tool for it yet.
5. **OpenAPI → GPT Action checker**: validate an OpenAPI spec for GPT Actions (operationId, servers, auth). GPT Actions are older, so demand is falling; check with search before building.
6. **JSON schema validator for tool/function definitions**: crowded generic space; only worth it if focused on OpenAI strict-mode rules (additionalProperties:false, all fields required).
7. **Codex config.toml builder** (model, approval_policy, sandbox, profiles). Moderate demand, few tools.
8. **hooks.json builder** for Codex plugin lifecycle hooks.
