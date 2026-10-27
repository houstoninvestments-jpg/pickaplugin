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
def guide(sl,title,desc,h1,intro,body,qa):
  GUIDES.append((sl,h1,desc))
  _page(f"guides/{sl}.html",1,title,desc,"Guide · updated "+_CHK,h1,intro,body,qa)

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
<h2>Before you install anything from GitHub</h2>
<p>Community plugins can bundle hooks, MCP servers and shell commands. Spend two minutes on the repo: when was the last commit, what does <code>.mcp.json</code> start, are there hooks. We wrote that up in <a href="vet-a-plugin.html">how to tell if a plugin is safe to install</a>.</p>''',
 [("Where do Codex plugins get installed?","Into ~/.codex/plugins/cache/MARKETPLACE/PLUGIN/VERSION/. Local plugins use the version 'local'."),
  ("Do ChatGPT and Codex use the same plugins?","Yes, according to OpenAI's docs they share one plugin directory, and plugins can include skills, connectors (apps) or both."),
  ("How do I remove a plugin?","Run codex plugin remove plugin-name@marketplace, or uninstall it from the Plugins view in the app."),
  ("Why does 'codex plugin marketplace add' give a 404?","Usually because you passed the raw marketplace.json URL. Give it the repo (owner/repo or the .git URL) instead.")])

guide("validate-plugin-json","How to validate a plugin.json for Codex and ChatGPT — PickAPlugin",
 "What a valid .codex-plugin/plugin.json needs, the mistakes that break installs, and a free in-browser checker.",
 "How to validate plugin.json",
 "Codex is pretty quiet when a manifest is wrong. The plugin just doesn't show up. Here's what it actually needs and the stuff that trips people up.",
 '''<h2>The quick way</h2><p>Paste it into our free <a href="../tools/plugin-json-validator.html">plugin.json validator</a>. It runs in your browser and flags errors, warnings and nice-to-haves. It also checks <code>marketplace.json</code>.</p>
<h2>What it needs</h2><ul><li><code>name</code>: kebab-case (<code>my-plugin</code>, not <code>My Plugin</code>). It's the id.</li><li><code>version</code>: semver like <code>0.1.0</code>.</li><li><code>description</code>: one clear sentence.</li><li>The file sits at <code>.codex-plugin/plugin.json</code>. Only that file goes in that folder. Skills, <code>.mcp.json</code> and hooks live at the plugin root.</li></ul>
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
<li><b>Manifest sanity.</b> Run it through the <a href="../tools/plugin-json-validator.html">validator</a>. Absolute paths or secrets in the manifest are a red flag.</li></ol>''',
 [("Does PickAPlugin test the plugins?","No. We sort and describe them, show last update, license and install command, and link to the source. Read the code before installing anything."),
  ("Are official OpenAI plugins safer?","They're curated by OpenAI, which is a real signal, but it's still worth knowing what you're connecting.")])

guide("find-codex-plugins","Where to find ChatGPT and Codex plugins — PickAPlugin",
 "Every place to find ChatGPT and Codex plugins: the built-in directory, GitHub awesome lists, and independent directories, and when to use each.",
 "Where to find ChatGPT and Codex plugins",
 "Short answer: start in the built-in directory, then look at the community. Here's the honest map.",
 f'''<ul><li><b>The built-in Plugins directory</b> in ChatGPT and the Codex app. Official and workspace plugins. Start here.</li>
<li><b>GitHub awesome lists</b>, like hashgraph-online/awesome-codex-plugins. Curated, and some double as a marketplace you can add.</li>
<li><b>Independent directories</b>: PickAPlugin (us), CodexStacks, Codex Harness, Codex Marketplace and others. See <a href="../alternatives.html">how they compare</a>.</li></ul>
<p>PickAPlugin's angle: {len(P)} plugins, hand-sorted into {len(cats)} categories in plain English, each with last update, license, language and the install command from its README. There are no accounts and no tracking walls. See <a href="../best/agent-workflows.html">best agent workflow plugins</a> or browse <a href="../languages.html">by language</a>.</p>''',
 [("Is there an app store for Codex plugins?","The closest thing is the built-in Plugins directory. Community plugins are spread across GitHub, which is why directories like PickAPlugin exist."),
  ("Are ChatGPT plugins the same as the old 2023 ChatGPT plugins?","No. The 2023 plugin store was retired. Today's plugins are bundles of skills, apps and MCP servers that work in ChatGPT and Codex.")])

_gl="".join(f'<a class=row style="grid-template-columns:1fr" href="{s}.html"><span><h3>{e(h)}</h3><p>{e(d)}</p></span></a>' for s,h,d in GUIDES)
open(D+"/guides/index.html","w").write(layout("ChatGPT & Codex plugin guides — PickAPlugin",f'''<div class=prose style="max-width:860px"><span class=mono style="color:var(--acc)">Guides</span><h1>Plain-English guides to ChatGPT and Codex plugins</h1><p style="font-size:19px">Short, practical answers to the stuff people actually get stuck on.</p></div><div style="border-top:3px solid var(--ink)">{_gl}</div>''',1,"Practical guides: install a Codex plugin, validate plugin.json, convert MCP configs, write AGENTS.md, and vet a plugin before installing."))

# ---- FAQ ----
_FAQ=[("What is PickAPlugin?",f"An independent, free directory of {len(P)} ChatGPT and Codex plugins gathered from public GitHub sources, hand-sorted into categories with last update, license, language and install command for each."),
 ("Is PickAPlugin affiliated with OpenAI?","No. It's an independent site. ChatGPT and Codex are trademarks of OpenAI."),
 ("Is it free?","Yes, browsing and the tools are free. Makers can pay for clearly labelled featured spots. Those never change the ranking order."),
 ("How do I install a plugin I found here?",'Each plugin page shows the install command from its README. See <a href="guides/install-codex-plugin.html">how to install a Codex plugin</a>.'),
 ("Do you test or audit plugins?",'No. Descriptions are each project\'s own. Read the code first. Here\'s <a href="guides/vet-a-plugin.html">a two-minute checklist</a>.'),
 ("How do I get my plugin listed?",'Submit it free on the <a href="submit.html">submit page</a>.'),
 ("How often is the catalog updated?",'It rebuilds daily, and star counts and last-update dates come from GitHub. See the <a href="changelog.html">changelog</a>.'),
 ("What free tools do you have?",'A <a href="tools/plugin-json-validator.html">plugin.json validator</a>, an <a href="tools/mcp-config-converter.html">MCP config converter</a>, an <a href="tools/plugin-install-command.html">install command finder</a> and an <a href="tools/agents-md-generator.html">AGENTS.md generator</a>. All of them run in your browser.'),
 ("How is this different from the built-in plugin directory?",'The built-in one is mostly official and workspace plugins. We cover community plugins on GitHub. See <a href="alternatives.html">how we compare to other directories</a>.')]
_page("faq.html",0,"PickAPlugin FAQ: ChatGPT & Codex plugin directory questions","Answers about PickAPlugin: what it is, whether it's free, how listings work, installing plugins and our free tools.","FAQ","Frequently asked questions","Quick answers about the site and about plugins in general.","",_FAQ)

# ---- alternatives (facts from each site's own homepage, checked date shown) ----
_ALT=[("OpenAI's built-in Plugins directory","https://developers.openai.com/codex/plugins","Inside ChatGPT and the Codex app. Official, workspace and personal plugins.","You want the officially curated ones, installed in one click. Start here."),
 ("CodexStacks","https://codexstacks.com/","Its homepage says 1,029 listings: 65 official and 964 community repos that pass its filter.","You want a big Codex-only list with 'best for' pages."),
 ("Codex Harness","https://codex-harness.com/plugins/","Says it indexes about 898 plugins parsed from plugin.json, and shows bundled skills and MCP servers.","You want to sort by skill count or see what a plugin bundles."),
 ("awesome-codex-plugins (hashgraph-online)","https://github.com/hashgraph-online/awesome-codex-plugins","A GitHub awesome list that's also an installable marketplace, and it requires a scanner score to get in.","You want to add one marketplace in Codex and install from it."),
 ("Codex Marketplace","https://www.codex-marketplace.com/","A community catalog with docs and its own npx installer.","You like a store-style site with a submit flow.")]
_ab="".join(f'<h2>{e(n)}</h2><p>{e(w)} <a href="{u}" rel=nofollow>{e(u)}</a></p><p><b>Pick it if:</b> {e(f)}</p>' for n,u,w,f in _ALT)
_page("alternatives.html",0,"PickAPlugin alternatives: other ChatGPT & Codex plugin directories compared","An honest look at where else to find ChatGPT and Codex plugins (OpenAI's directory, CodexStacks, Codex Harness, awesome-codex-plugins) and when each is the better pick.",
 "Compared · checked "+_CHK,"PickAPlugin vs other plugin directories",
 "We'd rather you find the right plugin than stay on our site. Here's where else to look, and when each one is the better pick. Counts are what each site says about itself as of "+_CHK+".",
 f'''<h2>PickAPlugin (us)</h2><p>{len(P)} plugins, hand-sorted into {len(cats)} plain-English categories, with pages by <a href="languages.html">language</a> and <a href="licenses.html">license</a>, "best of" pages like <a href="best/review-testing.html">best review and testing plugins</a>, and free browser tools. There's no sign-up. We're smaller than some of the lists below on purpose: we leave out repos that are dead or only half work.</p><p><b>Pick it if:</b> you want a quick, readable shortlist with the install command right there.</p>{_ab}''',
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
os.makedirs(D+"/tools/mcp-config-converter",exist_ok=True)
CONV=[]
for a,b in _PAIRS:
  A,fa,pa=_APPS[a]; B,fb,pb=_APPS[b]; sl=f"{a}-to-{b}"; CONV.append((sl,A,B))
  others=" · ".join(f'<a href="{x}-to-{y}.html">{_APPS[x][0]} → {_APPS[y][0]}</a>' for x,y in _PAIRS if (x,y)!=(a,b) and (x==a or y==b))
  body=f'''<h2>Where each file lives</h2><ul><li><b>{A}:</b> <code>{e(pa)}</code></li><li><b>{B}:</b> <code>{e(pb)}</code></li></ul>
<h2>Before and after</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:14px"><div><span class=mono>{A}</span><pre>{e(_EX[fa])}</pre></div><div><span class=mono>{B}</span><pre>{e(_EX[fb])}</pre></div></div>
<h2>What changes</h2><p>{_NOTE[(fa,fb)]}</p>
<p style="font-size:18px"><a href="/tools/mcp-config-converter?to={fb}"><b>Open the converter set to {B} →</b></a> Paste your {A} config, copy the result. It runs in your browser and nothing gets uploaded.</p>
<p>Double-check before you paste the result anywhere: if your config has tokens in it, they'll be in the output too.</p>
<h3>Other conversions</h3><p>{others}</p>'''
  qa=[(f"How do I convert an MCP config from {A} to {B}?",f"Paste the {A} config into PickAPlugin's free MCP config converter with the target set to {B}, then save the result to {pb}."),
      (f"Do I need to change the MCP server itself?","No. A local server runs the same command in every app. Only the config format around it changes.")]
  _page(f"tools/mcp-config-converter/{sl}.html",2,f"Convert MCP config from {A} to {B} (free, in-browser) — PickAPlugin",
   f"Move MCP servers from {A} to {B}: file locations, a before/after example, what changes, and a free converter that runs in your browser.",
   "Free tool · MCP config · updated "+_CHK,f"Convert MCP servers from {A} to {B}",
   f"Got MCP servers working in {A} and want the same ones in {B}? The servers don't change, only the config wrapper does. Here's exactly what to change.",body,qa)
_cv=D+"/tools/mcp-config-converter.html"
_h=open(_cv).read()
_pl="".join(f'<li><a href="mcp-config-converter/{s}.html">{A} → {B}</a></li>' for s,A,B in CONV)
_h=_h.replace("<h3>Related on PickAPlugin</h3>",f'<h3>Step-by-step for each pair</h3><ul>{_pl}</ul><h3>Related on PickAPlugin</h3>',1)
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
