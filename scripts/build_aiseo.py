# Executed at the end of build_tools.py (shares build.py's namespace). Writes /guides/*, /faq, /alternatives.
# Answer-style pages for the questions people ask ChatGPT/Bing. Keep claims checkable; competitor facts carry a "checked" date.
os.makedirs(D+"/guides",exist_ok=True)
_CHK="Oct 27, 2026"
def _page(path,depth,title,desc,kicker,h1,intro,body,qa):
  r="../"*depth
  html=f'''{TCSS}<div class=prose style="max-width:860px"><span class=mono style="color:var(--acc)">{kicker}</span><h1>{h1}</h1>
<p style="font-size:19px">{intro}</p>{body}{_faq_html(qa) if qa else ""}
<p style="margin-top:30px"><a href="{r}guides/index.html">All guides</a> · <a href="{r}tools/index.html">Free tools</a> · <a href="{r}faq.html">FAQ</a> · <a href="{r}index.html#catalog">Browse all {len(P)} plugins</a></p></div>{_faq_ld(qa) if qa else ""}'''
  open(f"{D}/{path}","w").write(layout(title,html,depth,desc))
GUIDES=[]
def guide(sl,title,desc,h1,intro,body,qa,updated=None):
  GUIDES.append((sl,h1,desc))
  _page(f"guides/{sl}.html",1,title,desc,"Guide · updated "+(updated or _CHK),h1,intro,body,qa)
def _gbody(name):
  return open(os.path.join(ROOT,"data","guides",name),encoding="utf-8").read()

guide("install-codex-plugin","How to install a Codex plugin (CLI, app and GitHub repos) — PickAPlugin",
 "Step-by-step: install a Codex or ChatGPT plugin from the built-in directory, from a GitHub repo marketplace, or from a local folder. Plain commands, no fluff.",
 "How to install a Codex plugin",
 "There are basically three ways a plugin gets onto your machine: the built-in directory, a GitHub repo that ships a marketplace, or a folder you made yourself. Here's each one, with the commands.",
 '''<h2>1. From the built-in directory (easiest)</h2>
<p>In the Codex app or ChatGPT desktop app, open <b>Plugins</b>, search, open the plugin and hit install. In the CLI, start <code>codex</code> and type <code>/plugins</code>. Plugins in the OpenAI tab are the ones OpenAI curates, so this is the low-risk route.</p>
<h2>2. From a GitHub repo</h2>
<p>Most community plugins live in a repo that has a <code>.agents/plugins/marketplace.json</code> (or the older <code>.claude-plugin/marketplace.json</code>). You add the repo as a marketplace once, then install by name:</p>
<pre>codex plugin marketplace add owner/repo
codex plugin list
codex plugin add plugin-name@marketplace-name</pre>
<p>The marketplace name comes from the <code>name</code> field in that repo's marketplace.json, and <code>codex plugin list</code> shows it.</p>
<p>Point it at the repo, not the raw <code>marketplace.json</code> URL. The command clones a git repo, so a raw file link fails with a 404. Every plugin page on PickAPlugin shows the install line we found in that project's README. If you just have a repo link, paste it into our <a href="../tools/plugin-install-command.html">install command finder</a>.</p>
<h2>3. From a local folder</h2>
<p>Put the plugin in <code>./plugins/my-plugin</code> (repo) or <code>~/.codex/plugins/my-plugin</code> (personal), then list it in <code>.agents/plugins/marketplace.json</code> with <code>"source": {"source": "local", "path": "./plugins/my-plugin"}</code>. Restart the app and it shows up. Check the manifest first with our <a href="../tools/plugin-json-validator.html">plugin.json validator</a>.</p>
<p>Go deeper: <a href="https://www.turboai.dev/docs/codex/plugins" target="_blank" rel="noopener">TurboAI's Codex CLI plugins reference</a> covers the full manifest lookup order if a plugin still doesn't show up.</p>
<h2>Before you install anything from GitHub</h2>
<p>Community plugins can bundle hooks, MCP servers and shell commands. Spend two minutes on the repo: when was the last commit, what does <code>.mcp.json</code> start, are there hooks. We wrote that up in <a href="vet-a-plugin.html">how to tell if a plugin is safe to install</a>. If you're adding the MCP server itself in Claude Desktop, Cursor or Codex, use <a href="install-mcp-server-claude-cursor-codex.html">the MCP install guide</a> and <a href="check-mcp-server-safe.html">the MCP safety checklist</a>.</p>''',
 [("Where do Codex plugins get installed?","Into ~/.codex/plugins/cache/MARKETPLACE/PLUGIN/VERSION/. Local plugins use the version 'local'."),
  ("Do ChatGPT and Codex use the same plugins?","Yes, according to OpenAI's docs they share one plugin directory, and plugins can include skills, connectors (apps) or both."),
  ("How do I remove a plugin?","Run codex plugin remove plugin-name@marketplace, or uninstall it from the Plugins view in the app."),
  ("Why does 'codex plugin marketplace add' give a 404?","Usually because you passed the raw marketplace.json URL. Give it the repo (owner/repo or the .git URL) instead.")])


guide("install-mcp-server-claude-cursor-codex",
 "How to install an MCP server in Claude Desktop, Cursor and Codex — PickAPlugin",
 "Step-by-step: add the same MCP server in Claude Desktop, Cursor and Codex, with official file paths, JSON and TOML examples, and real listings from the catalog.",
 "How to install an MCP server in Claude Desktop, Cursor and Codex",
 "The server is the same. The config file is not. Here's how to add one in each app, with official file paths, worked examples, and install lines from real PickAPlugin listings.",
 _gbody("install-mcp-server-claude-cursor-codex.html"),
 [("Is claude mcp add the same as Claude Desktop?","No. claude mcp add is the Claude Code CLI. Claude Desktop uses the Extensions directory, a .mcpb package, Connectors for remote URLs, or claude_desktop_config.json."),
  ("Where is Claude Desktop's config file?","macOS: ~/Library/Application Support/Claude/claude_desktop_config.json. Windows: %APPDATA%\\Claude\\claude_desktop_config.json. Linux: ~/.config/Claude/claude_desktop_config.json. Official MCP docs also tell you to fully quit and reopen the app after you save."),
  ("Where does Cursor keep MCP servers?","In ~/.cursor/mcp.json (all projects) and/or .cursor/mcp.json in the repo. The two files are merged; if the same name appears in both, the project file wins."),
  ("Where does Codex keep MCP servers?","In ~/.codex/config.toml, under [mcp_servers.NAME] tables, shared by the ChatGPT desktop app, the CLI and the IDE extension. Trusted projects can also use a project-scoped .codex/config.toml. The CLI command is codex mcp add."),
  ("Can I convert a config instead of rewriting it?","Yes. Paste JSON or TOML into our MCP config converter and copy the result. The server command or URL does not change, only the wrapper.")],
 updated="Nov 22, 2026")

guide("validate-plugin-json","How to validate a plugin.json for Codex and ChatGPT — PickAPlugin",
 "What a valid .codex-plugin/plugin.json needs, the mistakes that break installs, and a free in-browser checker.",
 "How to validate plugin.json",
 "Codex is pretty quiet when a manifest is wrong. The plugin just doesn't show up. Here's what it actually needs and the stuff that trips people up.",
 '''<h2>The quick way</h2><p>Paste it into our free <a href="../tools/plugin-json-validator.html">plugin.json validator</a>. It runs in your browser and flags errors, warnings and nice-to-haves. It also checks <code>marketplace.json</code>.</p>
<h2>What it needs</h2><ul><li><code>name</code>: kebab-case (<code>my-plugin</code>, not <code>My Plugin</code>). It's the id.</li><li><code>version</code>: semver like <code>0.1.0</code>.</li><li><code>description</code>: one clear sentence.</li><li>The file sits at <code>.codex-plugin/plugin.json</code>. Only that file goes in that folder. Skills, <code>.mcp.json</code> and hooks live at the plugin root.</li></ul>
<p>Go deeper: <a href="https://www.turboai.dev/docs/codex/plugins" target="_blank" rel="noopener">TurboAI's Codex CLI plugins reference</a> covers the full manifest lookup order Codex uses.</p>
<h2>The mistakes we see most</h2><ul><li>Paths that don't start with <code>./</code>, or absolute paths like <code>/Users/me/...</code>.</li><li>Paths with <code>..</code> that point outside the plugin.</li><li>Marketplace entries missing <code>source</code> or <code>policy</code>.</li><li>Secrets pasted into the manifest. Use env vars instead.</li></ul>''',
 [("Is there an official plugin.json schema?","OpenAI documents the fields in its plugin build docs, and many manifests reference the agent-plugins.org schema in $schema. Our validator checks the commonly documented rules."),
  ("Does the validator upload my file?","No. It's plain JavaScript in the page, nothing is sent anywhere.")])

guide("convert-mcp-config-claude-to-codex","Convert an MCP config from Claude (JSON) to Codex (config.toml) — PickAPlugin",
 "How to move MCP servers from claude_desktop_config.json or .mcp.json to Codex's ~/.codex/config.toml, with examples and a free converter.",
 "Convert MCP config from Claude to Codex",
 "Claude and Cursor keep MCP servers in JSON. Codex keeps them in TOML. The servers themselves are the same, only the wrapper changes.",
 '''<h2>Side by side</h2><div class=two style="display:grid;grid-template-columns:1fr 1fr;gap:14px"><pre>{"mcpServers": {
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"]
  }
}}</pre><pre>[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]</pre></div>
<p>Each server becomes a <code>[mcp_servers.NAME]</code> table in <code>~/.codex/config.toml</code> (or <code>.codex/config.toml</code> in a trusted project). <code>env</code> becomes an inline table. For a remote server use <code>url</code>, and put headers in <code>http_headers</code>, or better, <code>bearer_token_env_var</code> so the token isn't in the file.</p>
<p>Or skip the typing and use our <a href="../tools/mcp-config-converter.html">MCP config converter</a>. Paste JSON, get TOML (and back). It runs in your browser.</p>
<p>Want the full walkthrough, including Claude Desktop extensions, Cursor's mcp.json, and official file paths? See <a href="install-mcp-server-claude-cursor-codex.html">how to install an MCP server in Claude Desktop, Cursor and Codex</a>.</p>
<h2>Or just use the CLI</h2><pre>codex mcp add context7 -- npx -y @upstash/context7-mcp
codex mcp list</pre>''',
 [("Where is Claude Desktop's config file?","macOS: ~/Library/Application Support/Claude/claude_desktop_config.json. Windows: %APPDATA%\\Claude\\claude_desktop_config.json."),
  ("Where does Codex keep MCP servers?","In ~/.codex/config.toml, under [mcp_servers.NAME] tables. The CLI and IDE extension share it."),
  ("Do I need to change the server itself?","No. Local stdio servers run the same command everywhere. Only the config format changes.")])

guide("write-agents-md","How to write an AGENTS.md for Codex (with a template) — PickAPlugin",
 "What goes in AGENTS.md, where Codex looks for it, and a free generator that builds one from a few answers.",
 "How to write an AGENTS.md",
 "AGENTS.md is a plain markdown file Codex reads before it touches your repo. Think of it as the note you'd leave a new teammate.",
 '''<h2>What to put in it</h2><ul><li>How to install, run, test and lint (the exact commands).</li><li>Code style rules that aren't obvious from the code.</li><li>What not to touch: generated files, secrets, migrations.</li><li>How you want PRs and commit messages written.</li></ul>
<h2>Where Codex looks</h2><p><code>~/.codex/AGENTS.md</code> for global defaults, then every <code>AGENTS.md</code> from the repo root down to your working folder. Closer files win. <code>AGENTS.override.md</code> beats <code>AGENTS.md</code> in the same folder. The combined size is capped at 32 KiB by default, so keep it tight.</p>
<p>Want a head start? Our <a href="../tools/agents-md-generator.html">AGENTS.md generator</a> builds one from a few questions, in your browser.</p>''',
 [("Do other tools read AGENTS.md?","Yes, it's an open format. Cursor, Aider, Jules, Zed and others read it too."),
  ("Should I commit AGENTS.md?","Yes, commit it at the repo root so everyone, and every agent, gets the same rules.")])

guide("vet-a-plugin","How to tell if a ChatGPT or Codex plugin is safe to install — PickAPlugin",
 "A two-minute checklist for community plugins: maintenance, what it runs, hooks, MCP servers, permissions and license.",
 "How to tell if a plugin is worth installing (and safe)",
 "Nobody, us included, audits every community plugin. But you can catch most of the bad ones in about two minutes.",
 '''<ol><li><b>Is it alive?</b> Look at the last commit and open issues. Every PickAPlugin listing shows when the repo was last updated and whether it's archived.</li>
<li><b>What does it run?</b> Open <code>.mcp.json</code> and any <code>hooks.json</code>. Hooks and MCP servers run code on your machine.</li>
<li><b>What does it ask for?</b> Tokens, filesystem access, network. Does that match what it says it does?</li>
<li><b>Who made it?</b> A known company or an active maintainer is a better bet than a fresh account.</li>
<li><b>License.</b> If there's none, you technically can't reuse the code. Browse <a href="../licenses.html">plugins by license</a>.</li>
<li><b>Manifest sanity.</b> Run it through the <a href="../tools/plugin-json-validator.html">validator</a>. Absolute paths or secrets in the manifest are a red flag.</li></ol>
<p>Adding a raw MCP server in Claude Desktop, Cursor or Codex is a slightly different trust decision (a local stdio process runs as you; a remote URL sends data off the machine). That's <a href="check-mcp-server-safe.html">how to check if an MCP server is safe before installing</a>.</p>''',
 [("Does PickAPlugin test the plugins?","No. We sort and describe them, show last update, license and install command, and link to the source. Read the code before installing anything."),
  ("Are official OpenAI plugins safer?","They're curated by OpenAI, which is a real signal, but it's still worth knowing what you're connecting.")])


guide("check-mcp-server-safe",
 "How to check if an MCP server is safe before installing — PickAPlugin",
 "A practical checklist before you install an MCP server: publisher, exact package name, pinned versions, credentials, filesystem access, and what a local stdio server can do on your machine.",
 "How to check if an MCP server is safe before you install it",
 "A listing, including one on this site, is not a safety review. Official MCP docs say the same. Here's what to look at before a server runs on your machine, or before you point an agent at a remote one.",
 _gbody("check-mcp-server-safe.html"),
 [("Does PickAPlugin audit MCP servers?","No. We list them, show last update, license and the install command we found, and link to the source. Descriptions are each project's own. Read the repo and the command before you install."),
  ("Is a local MCP server sandboxed?","Not by the protocol. Official MCP local-server docs treat a stdio server as an ordinary process your app starts as you, with access to files, environment variables and the network unless you isolate it yourself (for example in a container)."),
  ("Are stars or a directory listing a safety signal?","Stars measure popularity. A listing, here or elsewhere, is not an endorsement. Official MCP docs say curated catalogs reduce risk, they don't take responsibility for what you run."),
  ("What's the difference between this and the plugin checklist?","The plugin guide is for ChatGPT and Codex plugin packages (marketplace.json, hooks, bundled MCP). This guide is for the MCP server itself, including servers you add by hand in Claude Desktop, Cursor or Codex.")],
 updated="Nov 22, 2026")

guide("find-codex-plugins","Where to find ChatGPT and Codex plugins — PickAPlugin",
 "Every place to find ChatGPT and Codex plugins: the built-in directory, GitHub awesome lists, and independent directories, and when to use each.",
 "Where to find ChatGPT and Codex plugins",
 "Short answer: start in the built-in directory, then look at the community. Here's the honest map.",
 f'''<ul><li><b>The built-in Plugins directory</b> in ChatGPT and the Codex app. Official and workspace plugins. Start here.</li>
<li><b>GitHub awesome lists</b>, like hashgraph-online/awesome-codex-plugins. Curated, and some double as a marketplace you can add.</li>
<li><b>Making an MCP server?</b> See <a href="where-to-submit-mcp-server.html">where to submit your MCP server</a>.</li>
<li><b>Independent directories</b>: PickAPlugin (us), CodexStacks, Codex Harness, Codex Marketplace and others. See <a href="../alternatives.html">how they compare</a>.</li></ul>
<p>PickAPlugin's angle: {len(P)} plugins, hand-sorted into {len(cats)} categories in plain English, each with last update, license, language and the install command from its README. There are no accounts and no tracking walls. See <a href="../c/agent-workflows.html">best agent workflow plugins</a> or browse <a href="../languages.html">by language</a>.</p>''',
 [("Is there an app store for Codex plugins?","The closest thing is the built-in Plugins directory. Community plugins are spread across GitHub, which is why directories like PickAPlugin exist."),
  ("Are ChatGPT plugins the same as the old 2023 ChatGPT plugins?","No. The 2023 plugin store was retired. Today's plugins are bundles of skills, apps and MCP servers that work in ChatGPT and Codex.")])

guide("where-to-submit-mcp-server","Where to submit your MCP server (2026): every registry and directory — PickAPlugin",
 "Where to list an MCP server in 2026: the official MCP Registry, mcpmarket, mcpservers.org, mcp.so, Smithery, Docker MCP Catalog, LobeHub, Glama, cursor.directory, awesome-mcp-servers and more. How to submit, and what's free.",
 "Where to submit your MCP server (2026)",
 "You built an MCP server. Now people need to find it. Here's every place worth listing it, how each one takes submissions, and which ones cost money. Submit paths checked "+_CHK+".",
 '''<p>Traffic numbers below come from <a href="https://x.com/marckohlbrugge/status/2115106902841397750" rel=nofollow>Marc Kohlbrugge's post (Oct 2026)</a>. We didn't measure them ourselves, and where we have no sourced number we don't give one.</p>
<h2>0. PickAPlugin (us): free</h2><p>We list ChatGPT and Codex plugins and the MCP servers they bundle. Listing is free: see the <a href="../submit.html">submit page</a> (email the repo link, or get in automatically if you're in a list we read). Want more eyes? A <a href="../featured.html">featured spot</a> is clearly labelled as paid and never changes the ranking.</p>
<h2>1. Official MCP Registry: free, do this first</h2><p><a href="https://registry.modelcontextprotocol.io" rel=nofollow>registry.modelcontextprotocol.io</a> is the community registry run by the MCP project. Other directories and clients pull from it, so one entry here spreads. You publish with the <code>mcp-publisher</code> CLI: add a <code>server.json</code>, log in (GitHub or DNS proves the namespace), then <code>mcp-publisher publish</code>. Your package (npm, PyPI, Docker, etc.) has to exist first.</p>
<h2>2. MCP Market (mcpmarket.com): free, or $29 to skip the queue</h2><p>About 81k visits a month, per Marc Kohlbrugge (Oct 2026). Submit the GitHub repo URL at <a href="https://mcpmarket.com/submit" rel=nofollow>mcpmarket.com/submit</a>. A one-time $29 option lists you within 24 hours with a badge.</p>
<h2>3. mcpservers.org: free, or $39 premium</h2><p>About 45k visits a month, per Marc Kohlbrugge (Oct 2026). Form at <a href="https://mcpservers.org/submit" rel=nofollow>mcpservers.org/submit</a>. Free review takes up to two weeks; $39 one-time gets a 24-hour review.</p>
<h2>4. mcp.so: free, or $39 paid</h2><p>About 18k visits a month, per Marc Kohlbrugge (Oct 2026). Submit at <a href="https://mcp.so/submit" rel=nofollow>mcp.so/submit</a>. The $39 one-time option publishes right away with a verified badge and featured placement.</p>
<h2>5. Smithery (smithery.ai): free</h2><p>A registry and hosting layer for MCP servers. Sign in and add your server from <a href="https://smithery.ai/new" rel=nofollow>smithery.ai/new</a>; you can point it at a repo or a hosted URL.</p>
<h2>6. Docker MCP Catalog (hub.docker.com/mcp): free, by PR</h2><p>Docker's catalog of containerised and remote servers, shown in Docker Desktop's MCP Toolkit. You add an entry by pull request to <a href="https://github.com/docker/mcp-registry" rel=nofollow>docker/mcp-registry</a>. Local servers need a Dockerfile in your repo.</p>
<h2>7. LobeHub MCP (lobehub.com/mcp): free</h2><p>The MCP marketplace inside LobeChat. Use the submit button on <a href="https://lobehub.com/mcp" rel=nofollow>lobehub.com/mcp</a> with your repo.</p>
<h2>8. Glama (glama.ai/mcp/servers): free</h2><p>A big searchable index with quality, license and maintenance scores. It's synced with awesome-mcp-servers, and you can also use "Add Server" on <a href="https://glama.ai/mcp/servers" rel=nofollow>glama.ai/mcp/servers</a>.</p>
<h2>9. cursor.directory: free</h2><p>Community directory for Cursor rules and MCP servers. Sign in and submit from <a href="https://cursor.directory/mcp" rel=nofollow>cursor.directory/mcp</a>. Good if your server is aimed at Cursor users.</p>
<h2>10. awesome-mcp-servers (GitHub): free, by PR</h2><p>About 97k GitHub stars, per Marc Kohlbrugge (Oct 2026). Open a PR to <a href="https://github.com/punkpeye/awesome-mcp-servers" rel=nofollow>punkpeye/awesome-mcp-servers</a> adding one line in the right category, in alphabetical order. It's only for servers with a public repo you install yourself; hosted-only servers go to awesome-remote-mcp-servers.</p>
<h2>11. HOL Plugins (hol.org/plugins): free</h2><p>A free directory with trust scores, from the team behind awesome-codex-plugins. If your server ships as a Codex plugin, see <a href="https://hol.org/plugins" rel=nofollow>hol.org/plugins</a>.</p>
<h2>A sensible order</h2><ol><li>Official MCP Registry (others copy from it).</li><li>awesome-mcp-servers PR (feeds Glama too).</li><li>The free forms: MCP Market, mcpservers.org, mcp.so, Smithery, LobeHub, cursor.directory, PickAPlugin.</li><li>Docker MCP Catalog if you ship a container.</li></ol><p>Before you submit, make sure the README has a one-line description and a copy-paste install command. Our <a href="../tools/mcp-config-converter.html">MCP config converter</a> helps you show both JSON and TOML configs, and <a href="install-mcp-server-claude-cursor-codex.html">the install guide</a> shows the file paths for Claude Desktop, Cursor and Codex.</p>''',
 [("Where should I submit my MCP server first?","The official MCP Registry at registry.modelcontextprotocol.io. Several directories and clients read from it, so it's the one listing that spreads on its own."),
  ("Is it free to list an MCP server?","Yes, every place on this page has a free option. MCP Market ($29), mcpservers.org ($39) and mcp.so ($39) also sell one-time paid options for faster review or badges. You don't need them to get listed."),
  ("Which MCP directory gets the most traffic?","Of the sites Marc Kohlbrugge compared in Oct 2026, MCP Market had the most (about 81k visits a month), then mcpservers.org (about 45k) and mcp.so (about 18k). The awesome-mcp-servers GitHub list had about 97k stars."),
  ("Do I need a public GitHub repo?","For most directories and for awesome-mcp-servers, yes. Hosted-only servers can still go in the official registry, Smithery and awesome-remote-mcp-servers."),
  ("How do I get my MCP server onto PickAPlugin?",'Submit it free on our <a href="../submit.html">submit page</a>. If it ships as a ChatGPT or Codex plugin and sits in a list we read, it shows up automatically.')])

guide("publish-codex-plugin","How to publish a Codex or ChatGPT plugin (2026): submit it and get it listed — PickAPlugin",
 "How to publish and submit a Codex or ChatGPT plugin in 2026: the OpenAI plugin submission portal, a GitHub repo marketplace, and the free directories that list community plugins.",
 "How to publish a Codex or ChatGPT plugin (2026)",
 "You've built a plugin. There are three ways to get it in front of people: submit it to OpenAI's Plugins Directory, publish it from your own GitHub repo as a marketplace, and list it in the community directories. Most makers do all three. Checked Nov 2, 2026.",
 '''<h2>1. The official Plugins Directory (OpenAI review)</h2>
<p>ChatGPT and Codex share one public plugin directory. On July 9, 2026 OpenAI moved the old ChatGPT app directory into it, so "submit a ChatGPT app" now means submitting a plugin. A plugin can be skills only, an MCP-backed app, or both.</p>
<p>You submit through the plugin submission portal on the OpenAI Platform. Per <a href="https://learn.chatgpt.com/docs/submit-plugins" rel=nofollow>OpenAI's submit guide</a> and <a href="https://developers.openai.com/plugins/deploy/submission" rel=nofollow>upload and submit docs</a>:</p>
<ul><li>Upload the built package as a ZIP and fix any required setup or validation errors the automated checks find.</li>
<li>If it connects to an MCP server, include five positive test cases, three negative test cases, a video walkthrough and release notes. If sign-in is needed, give reviewers a test account that works without MFA or email codes.</li>
<li>Fill in the listing details (name, logo, description, company and privacy policy URLs) and the policy attestations, then submit for review.</li>
<li>OpenAI says review timelines vary. Once you're approved, you choose when to publish, and then it shows up in the directory in both ChatGPT and Codex.</li></ul>
<h2>2. Your own GitHub repo marketplace (no review, works today)</h2>
<p>You don't need OpenAI's approval to share a plugin. Put a <code>.agents/plugins/marketplace.json</code> in your repo that lists the plugin, and anyone can install it:</p>
<pre>codex plugin marketplace add owner/repo
codex plugin add plugin-name@marketplace-name</pre>
<p>Put those two lines at the top of your README. Workspace admins can also import and sync a GitHub marketplace for their team. Before you push, run your manifest through our <a href="../tools/plugin-json-validator.html">plugin.json validator</a>, and test the install from a clean machine with the steps in <a href="install-codex-plugin.html">how to install a Codex plugin</a>.</p>
<h2>3. Community directories (free listings)</h2>
<ul><li><b>PickAPlugin (us).</b> Listing is free: send the repo on the <a href="../submit.html">submit page</a>. If you're already in a list we read, you show up automatically. Listed makers can add a <a href="../badge.html">"Listed on PickAPlugin" badge</a> to their README.</li>
<li><b>awesome-codex-plugins</b> (hashgraph-online on GitHub). An awesome list that's also an installable marketplace. It requires a scanner score to get in.</li>
<li><b>HOL Plugins</b> (<a href="https://hol.org/plugins" rel=nofollow>hol.org/plugins</a>). A free directory with trust scores, from the same team.</li>
<li><b>CodexStacks, Codex Harness, Codex Marketplace.</b> Independent catalogs. Some pick up public repos on their own, and Codex Marketplace has a submit flow. See <a href="../alternatives.html">how the directories compare</a>.</li></ul>
<p>If your plugin bundles an MCP server, list the server too. Here's <a href="where-to-submit-mcp-server.html">every place to submit an MCP server</a>.</p>
<h2>What helps people actually install it</h2>
<ul><li>One plain sentence at the top of the README saying what it does and who it's for.</li>
<li>A copy-paste install line. Most directories, ours included, lift it straight from the README.</li>
<li>A license file. Without one, a lot of people won't touch it.</li>
<li>Recent commits. Directories show the last update date, and stale repos get skipped.</li>
<li>Say what it can read and write. If it runs hooks or shell commands, say so up front. That's the first thing careful users check (<a href="vet-a-plugin.html">here's what they look for</a>).</li></ul>''',
 [("How do I submit a plugin to the ChatGPT and Codex Plugins Directory?","Through the plugin submission portal on the OpenAI Platform. Upload your package as a ZIP, fix the automated findings, add review info (test cases, a video walkthrough and release notes if it uses an MCP server), and submit for review. After approval you choose when to publish."),
  ("Can I still submit a ChatGPT app?","Apps are now submitted and published as plugins. OpenAI moved the app directory into the Plugins Directory on July 9, 2026."),
  ("How long does OpenAI's plugin review take?","OpenAI doesn't promise a timeline. Its docs say review times vary as it scales the process."),
  ("Can people install my Codex plugin without OpenAI approval?","Yes. Publish a marketplace.json in your GitHub repo and people can run codex plugin marketplace add owner/repo, then install it by name."),
  ("Is listing on PickAPlugin free?",'Yes. Send the repo on the <a href="../submit.html">submit page</a>. Paid featured spots exist, but they\'re always labelled and never change the ranking.')])

_gl="".join(f'<a class=row style="grid-template-columns:1fr" href="{s}.html"><span><h3>{e(h)}</h3><p>{e(d)}</p></span></a>' for s,h,d in GUIDES)
open(D+"/guides/index.html","w").write(layout("ChatGPT & Codex plugin guides — PickAPlugin",f'''<div class=prose style="max-width:860px"><span class=mono style="color:var(--acc)">Guides</span><h1>Plain-English guides to ChatGPT and Codex plugins</h1><p style="font-size:19px">Practical answers to the stuff people actually get stuck on: installing a plugin or an MCP server, checking it before you install, and the builder tools around that.</p></div><div style="border-top:3px solid var(--ink)">{_gl}</div>''',1,"Practical guides: install a Codex plugin or an MCP server in Claude Desktop, Cursor and Codex, validate plugin.json, convert MCP configs, write AGENTS.md, and vet a plugin or MCP server before installing."))

# ---- FAQ ----
_FAQ=[("What is PickAPlugin?",f"An independent, free directory of {len(P)} ChatGPT and Codex plugins gathered from public GitHub sources, hand-sorted into categories with last update, license, language and install command for each."),
 ("Is PickAPlugin affiliated with OpenAI?","No. It's an independent site. ChatGPT and Codex are trademarks of OpenAI."),
 ("Is it free?","Yes, browsing and the tools are free. Makers can pay for clearly labelled featured spots. Those never change the ranking order."),
 ("How do I install a plugin I found here?",'Each plugin page shows the install command from its README. See <a href="guides/install-codex-plugin.html">how to install a Codex plugin</a>.'),
 ("How do I install an MCP server in Claude, Cursor or Codex?",'The server is the same, the config file is not. Step by step, with official file paths and examples: <a href="guides/install-mcp-server-claude-cursor-codex.html">how to install an MCP server in Claude Desktop, Cursor and Codex</a>. If you only need to change the format, use the <a href="tools/mcp-config-converter.html">MCP config converter</a>.'),
 ("Do you test or audit plugins?",'No. Descriptions are each project\'s own. Read the code first. Here\'s <a href="guides/vet-a-plugin.html">a two-minute checklist</a> for plugins, and <a href="guides/check-mcp-server-safe.html">how to check an MCP server before installing</a>.'),
 ("How do I get my plugin listed?",'Submit it free on the <a href="submit.html">submit page</a>.'),
 ("How do I publish my Codex or ChatGPT plugin?",'Submit it to OpenAI\'s Plugins Directory through the plugin submission portal, publish a marketplace.json from your GitHub repo, and list it in free directories. Step by step: <a href="guides/publish-codex-plugin.html">how to publish a Codex or ChatGPT plugin</a>.'),
 ("Where else should I submit my MCP server?",'Start with the official MCP Registry, then the big directories. We keep a list with submit links and prices in <a href="guides/where-to-submit-mcp-server.html">where to submit your MCP server</a>.'),
 ("How often is the catalog updated?",'It rebuilds daily, and star counts and last-update dates come from GitHub. See the <a href="changelog.html">changelog</a>.'),
 ("What free tools do you have?",'A <a href="tools/plugin-json-validator.html">plugin.json validator</a>, an <a href="tools/mcp-config-converter.html">MCP config converter</a>, an <a href="tools/plugin-install-command.html">install command finder</a> and an <a href="tools/agents-md-generator.html">AGENTS.md generator</a>. All of them run in your browser.'),
 ("How is this different from the built-in plugin directory?",'The built-in one is mostly official and workspace plugins. We cover community plugins on GitHub. See <a href="alternatives.html">how we compare to other directories</a>.')]
_page("faq.html",0,"PickAPlugin FAQ: ChatGPT & Codex plugin directory questions","Answers about PickAPlugin: what it is, whether it's free, how listings work, installing plugins and our free tools.","FAQ","Frequently asked questions","Quick answers about the site and about plugins in general.","",_FAQ)

# ---- alternatives (facts from each site's own homepage, checked date shown) ----
_ALT=[("OpenAI's built-in Plugins directory","https://developers.openai.com/codex/plugins","Inside ChatGPT and the Codex app. Official, workspace and personal plugins.","You want the officially curated ones, installed in one click. Start here."),
 ("CodexStacks","https://codexstacks.com/","Its homepage says 1,029 listings: 65 official and 964 community repos that pass its filter.","You want a big Codex-only list with 'best for' pages."),
 ("Codex Harness","https://codex-harness.com/plugins/","Says it indexes about 898 plugins parsed from plugin.json, and shows bundled skills and MCP servers.","You want to sort by skill count or see what a plugin bundles."),
 ("awesome-codex-plugins (hashgraph-online)","https://github.com/hashgraph-online/awesome-codex-plugins","A GitHub awesome list that's also an installable marketplace, and it requires a scanner score to get in.","You want to add one marketplace in Codex and install from it."),
 ("Codex Marketplace","https://www.codex-marketplace.com/","A community catalog with docs and its own npx installer.","You like a store-style site with a submit flow."),
 ("SkillMaxx install-test results","https://skillmaxx.gilventures.ai/reports/latest/","Not a directory: it installs agent skills and MCP servers every night and publishes which ones break and why.","You've picked a plugin and want to know whether it installs cleanly today.")]
_ab="".join(f'<h2>{e(n)}</h2><p>{e(w)} <a href="{u}"{"" if "skillmaxx" in u else " rel=nofollow"}>{e(u)}</a></p><p><b>Pick it if:</b> {e(f)}</p>' for n,u,w,f in _ALT)
_page("alternatives.html",0,"PickAPlugin alternatives: other ChatGPT & Codex plugin directories compared","An honest look at where else to find ChatGPT and Codex plugins (OpenAI's directory, CodexStacks, Codex Harness, awesome-codex-plugins) and when each is the better pick.",
 "Compared · checked "+_CHK,"PickAPlugin vs other plugin directories",
 "We'd rather you find the right plugin than stay on our site. Here's where else to look, and when each one is the better pick. Counts are what each site says about itself as of "+_CHK+".",
 f'''<h2>PickAPlugin (us)</h2><p>{len(P)} plugins, hand-sorted into {len(cats)} plain-English categories, with pages by <a href="languages.html">language</a> and <a href="licenses.html">license</a>, ranked shelves like <a href="c/review-testing.html">best review and testing plugins</a>, and free browser tools. There's no sign-up. We're smaller than some of the lists below on purpose: we leave out repos that are dead or only half work.</p><p><b>Pick it if:</b> you want a quick, readable shortlist with the install command right there.</p>{_ab}''',
 [("Which Codex plugin directory is the biggest?","By their own counts, CodexStacks and Codex Harness list the most (roughly 900–1,000+ as of "+_CHK+"). Bigger isn't always better, so check what filter each uses."),
  ("Can I use more than one?","Sure. They're all free to browse, and the install command is the same wherever you find a plugin.")])
print("aiseo:",len(GUIDES),"guides + hub, faq, alternatives")

# ---- MCP converter pair pages (only formats our converter handles: mcpServers JSON, VS Code servers JSON, Codex TOML) ----
_APPS={"claude-desktop":("Claude Desktop","claude","claude_desktop_config.json (macOS: ~/Library/Application Support/Claude/, Windows: %APPDATA%\\Claude\\)"),
 "claude-code":("Claude Code","claude",".mcp.json in the project, or ~/.claude.json"),
 "cursor":("Cursor","claude",".cursor/mcp.json in the project, or ~/.cursor/mcp.json"),
 "vscode":("VS Code","vscode",".vscode/mcp.json in the workspace"),
 "codex":("Codex","codex","~/.codex/config.toml (or .codex/config.toml in a trusted project)")}
_EX={"claude":'{\n  "mcpServers": {\n    "context7": {\n      "command": "npx",\n      "args": ["-y", "@upstash/context7-mcp"],\n      "env": {"API_KEY": "..."}\n    }\n  }\n}',
 "vscode":'{\n  "servers": {\n    "context7": {\n      "type": "stdio",\n      "command": "npx",\n      "args": ["-y", "@upstash/context7-mcp"],\n      "env": {"API_KEY": "..."}\n    }\n  }\n}',
 "codex":'[mcp_servers.context7]\ncommand = "npx"\nargs = ["-y", "@upstash/context7-mcp"]\nenv = { API_KEY = "..." }'}
_NOTE={("claude","codex"):"JSON becomes TOML. Each entry under <code>mcpServers</code> turns into its own <code>[mcp_servers.NAME]</code> table, and <code>env</code> becomes an inline table. For remote servers, use <code>url</code> plus <code>http_headers</code>, or <code>bearer_token_env_var</code> so the token stays out of the file.",
 ("vscode","codex"):"Drop the <code>type</code> field and turn each entry under <code>servers</code> into a <code>[mcp_servers.NAME]</code> TOML table. VS Code's <code>${env:NAME}</code> and <code>${input:...}</code> variables don't carry over, so put the real env var names in Codex's <code>env</code> or <code>env_vars</code>.",
 ("codex","claude"):"Each <code>[mcp_servers.NAME]</code> table becomes a key under <code>mcpServers</code>. Inline tables like <code>env = {...}</code> become plain JSON objects. Codex-only fields such as <code>startup_timeout_sec</code> or <code>bearer_token_env_var</code> have no direct match, so you'll have to handle them yourself.",
 ("codex","vscode"):"Tables go under <code>servers</code>, and VS Code wants a <code>type</code> on each one (<code>stdio</code> for a command, <code>http</code> for a URL).",
 ("claude","vscode"):"Rename the root key from <code>mcpServers</code> to <code>servers</code> and add a <code>type</code> to each entry. Everything else carries straight over.",
 ("vscode","claude"):"Rename <code>servers</code> to <code>mcpServers</code> and you can drop <code>type</code>. Swap any <code>${input:...}</code> prompts for real values or env vars."}
_PAIRS=[(a,b) for a in _APPS for b in _APPS if a!=b and (_APPS[a][1],_APPS[b][1]) in _NOTE]
# Pair-specific notes live on the converter hub. Old /tools/mcp-config-converter/<pair>
# URLs 301 to that hub (worker/index.js). Do not generate those thin pages again.
CONV=[]
_notes=[]
for a,b in _PAIRS:
  A,fa,pa=_APPS[a]; B,fb,pb=_APPS[b]; sl=f"{a}-to-{b}"; CONV.append((sl,A,B))
  _notes.append(f"<h3>{e(A)} → {e(B)}</h3><p><b>Files:</b> {e(A)} at <code>{e(pa)}</code> · {e(B)} at <code>{e(pb)}</code></p><p>{_NOTE[(fa,fb)]}</p>")
_cv=D+"/tools/mcp-config-converter.html"
_h=open(_cv).read()
_pl="".join(f'<li><a href="/tools/mcp-config-converter?to={_APPS[b][1]}">{A} → {B}</a></li>' for (_,A,B), (a,b) in zip(CONV,_PAIRS))
_notes_html="<h3>What changes between apps</h3>"+"".join(_notes)
_h=_h.replace("<h3>Related on PickAPlugin</h3>",_notes_html+"<h3>Jump to a conversion</h3><ul>"+_pl+"</ul><h3>Related on PickAPlugin</h3>",1)
_h=_h.replace("</body>",'<script>(function(){var t=new URLSearchParams(location.search).get("to"),s=document.getElementById("to");if(t&&s&&[].some.call(s.options,function(o){return o.value==t}))s.value=t})()</script></body>',1)
open(_cv,"w").write(_h)

# ---- Best Codex plugins (November 2026), from catalog data ----
import datetime as _ddt
def _fresh(p):
  try: return (_ddt.date.today()-_ddt.date.fromisoformat((p.get("pushed_at") or "")[:10])).days<=60
  except: return False
_best=[]
for c in sorted(cats):
  if c=="Other": continue
  ps=[p for p in P if p["category"]==c and p.get("install") and not p.get("archived") and _fresh(p)]
  ps.sort(key=lambda p:-(p.get("stars") or 0))
  if ps: _best.append((c,ps[:3]))
_n=sum(len(x) for _,x in _best)
_rows="".join(f'<tr><td style="padding:8px;border-bottom:1px solid var(--rule)">{e(c)}</td><td style="padding:8px;border-bottom:1px solid var(--rule)"><a href="../p/{p["slug"]}.html">{e(p["name"])}</a><br><span style="color:var(--mute);font-size:14px">{e(p["description"][:110])}</span></td><td style="padding:8px;border-bottom:1px solid var(--rule)" class=mono>{(p.get("stars") or 0):,}</td><td style="padding:8px;border-bottom:1px solid var(--rule)" class=mono>{e((p.get("pushed_at") or "")[:10])}</td><td style="padding:8px;border-bottom:1px solid var(--rule)" class=mono>{e(p.get("license") or "none")}</td></tr>' for c,ps in _best for p in ps)
_cmds="".join(f'<h3>{e(c)}</h3>'+"".join(f'<p style="margin:6px 0"><a href="../p/{p["slug"]}.html"><b>{e(p["name"])}</b></a></p><pre>{e(p["install"])}</pre>' for p in ps) for c,ps in _best)
os.makedirs(D+"/blog",exist_ok=True)
_page("blog/best-codex-plugins-november-2026.html",1,"Best Codex plugins (November 2026): top picks by category with install commands — PickAPlugin",
 f"The {_n} most-starred, still-maintained Codex and ChatGPT plugins in each category, from PickAPlugin's {len(P)}-plugin catalog. Table, stars, last update, license and copyable install commands.",
 "Data pulled "+_CHK+" · for November 2026",f"Best Codex plugins (November 2026)",
 f"No vibes, just a filter anyone can check. From our {len(P)}-plugin catalog we kept plugins that have an install command in their README, aren't archived, and got a commit in the last 60 days. Then we took the 3 most-starred in each category. Stars tell you a plugin is popular, not that it's good or safe, so read the repo before you install.",
 f'''<h2>The table</h2><div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:15px"><tr class=mono style="text-align:left"><th style="padding:8px">Category</th><th style="padding:8px">Plugin</th><th style="padding:8px">Stars</th><th style="padding:8px">Last commit</th><th style="padding:8px">License</th></tr>{_rows}</table></div>
<h2>Install commands</h2><p>These are copied from each project's README. Some are written for Claude Code or a skills installer rather than for <code>codex plugin</code>. When that's the case, our <a href="../guides/install-codex-plugin.html">install guide</a> shows the Codex route.</p>{_cmds}
<h2>How we picked</h2><p>Stars and last-commit dates come from GitHub on our last refresh. Nobody paid to be on this list, and featured placements don't affect it. Want the full list? <a href="../index.html#catalog">Browse all {len(P)}</a> or check <a href="../guides/vet-a-plugin.html">the 2-minute safety check</a>.</p>''',
 [("What's the best Codex plugin?","It depends on the job. This list shows the most-starred plugins in each category that are still maintained. Start with the category you need and read the repo."),
  ("How was this list made?","From PickAPlugin's catalog: plugins with an install command that aren't archived and had a commit in the last 60 days, sorted by GitHub stars, top 3 per category. Nobody paid to be on it.")])
print("aiseo: +",len(CONV),"converter pairs, best list",_n)
