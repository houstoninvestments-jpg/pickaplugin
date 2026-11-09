# Exec'd by build_seo.py before the clean-URL pass. Per-page fixes from the Monday GSC review.
# RULE: at most one title change per page. Log every entry (date, why, check date) in launch/seo-log.md.
# _TITLE_OVR: rel path -> new <title>. _INJECT: (rel path, mode, marker, html) with clean absolute hrefs.
#   mode "before": insert html before the first occurrence of marker (plain string)
#   mode "after_re": insert html after the first regex match of marker
_ROUND=f"{len(P)//50*50}+"
_TITLE_OVR={
 # 2026-11-09: home 190 impr, pos 7.9, CTR 0.53%. Query-first, count promise, year, brand last.
 "index.html":f"Codex & ChatGPT Plugin Directory (2026): {_ROUND} plugins — PickAPlugin",
 # 2026-11-09: "codex auto resume" 22 impr pos 8.6 (+ "codex autoresume", "codex-auto-resume")
 "p/codex-auto-resume.html":"Codex Auto Resume: continue Codex after usage limits reset (Windows) — PickAPlugin",
 # 2026-11-09: "data product builder" 33 impr pos 20.4
 "p/data-product-builder-for-dbt.html":"Data Product Builder for dbt: Codex & Claude Code skills — PickAPlugin",
 # 2026-11-09: "devin plugins" 6 impr pos 9.2, "devin plugin" pos 10.5
 "p/devin-plugin-cc.html":"Devin Plugin CC: Devin plugins for Codex & Claude Code — PickAPlugin",
 # 2026-11-09: "mcp server directory" 8 impr pos 23
 "guides/where-to-submit-mcp-server.html":"MCP server directory list (2026): where to submit your MCP server — PickAPlugin",
}
_DESC_OVR={
 "index.html":f"A free, independent directory of {_ROUND} Codex plugins, ChatGPT apps and the MCP servers they bundle, hand-sorted by category with last update, license and install command for each.",
}
_P_AFTER=r'<p class=d>.*?</p>(?:<p class=note>.*?</p>)?'
_INJECT=[
 # --- quick win: "best backend for openai codex" (title already changed 2026-11-02, so content + links only)
 ("best/data-backend.html","before",'<p style="color:var(--mute)">Stars measure popularity',
  '<h2>What is the best backend for OpenAI Codex?</h2><p>It depends on what "backend" means for your project. From the plugins in our catalog:</p><ul class=where>'
  '<li><b>A backend the agent can set up for you</b> (hosting, Postgres, email, storage): <a href="/p/cohesivity">Cohesivity</a>, or <a href="/p/host0">host0</a> for publishing an app with a shared database.</li>'
  '<li><b>A web search and scraping API</b> the agent calls as an MCP server: <a href="/p/crw">crw</a>, the most-starred plugin on this shelf.</li>'
  '<li><b>A data warehouse and dbt</b>: <a href="/p/dex">Dex</a> for exploring and modeling, or the <a href="/p/data-product-builder-for-dbt">data product builder for dbt</a> if you use data contracts.</li>'
  '<li><b>Postgres extensions</b>: <a href="/p/villagesql-skills">VillageSQL skills</a>.</li></ul>'
  '<p>We haven\'t tested any of these. Give an agent a test database before you give it production credentials.</p>'),
 ("c/data-backend.html","after_re",r'<p class=shelves><span class=mono>Ranked:</span>.*?</p>',
  '<p>Picking one? Start with our ranked list of the <a href="/best/data-backend">best backend plugins for OpenAI Codex</a>. Working in dbt? See the <a href="/p/data-product-builder-for-dbt">data product builder for dbt</a> and <a href="/p/dex">Dex</a>.</p>'),
 # --- quick win: "codex auto resume"
 ("p/codex-auto-resume.html","after_re",_P_AFTER,
  '<h2>How Codex auto resume works</h2><ul class=where>'
  '<li>When the Codex desktop app on Windows stops at a usage limit (the 5-hour or the weekly one), it waits for the reset time Codex itself reports, not a fixed timer.</li>'
  '<li>Then it sends one continuation message to that exact conversation, found by its thread ID, through Codex\'s own <code>codex queue</code> command. It never types into the Codex window.</li>'
  '<li>It also retries temporary failures it can name (HTTP 429 rate limits, network errors, timeouts, 5xx errors). It never retries cancellations, permission or policy refusals, or anything it can\'t classify.</li>'
  '<li>Limits, per its README: Windows 10/11 only, the conversation has to be open in Codex for the resume to land, and the installer isn\'t code-signed.</li></ul>'
  '<p style="color:var(--mute)">Summarized from the project\'s README. We haven\'t tested it. Other <a href="/c/usage-quotas">Codex usage and quota tools</a>.</p>'),
 ("c/usage-quotas.html","after_re",r'<p class=shelves><span class=mono>Ranked:</span>.*?</p>',
  '<p>Codex stopped at the 5-hour limit overnight? <a href="/p/codex-auto-resume">Codex Auto Resume</a> picks the same conversation back up when the limit resets (Windows).</p>'),
 ("best/usage-quotas.html","before",'<p style="color:var(--mute)">Stars measure popularity',
  '<p>Need Codex to carry on by itself after a limit? <a href="/p/codex-auto-resume">Codex auto resume</a> waits for the reset and continues the same task.</p>'),
 # --- quick win: "data product builder"
 ("p/data-product-builder-for-dbt.html","after_re",_P_AFTER,
  '<h2>What this data product builder does</h2><p>It\'s a set of seven agent skills from Entropy Data for building data products on dbt, for Codex, Claude Code, GitHub Copilot CLI or any agent that reads AGENTS.md:</p><ul class=where>'
  '<li><b>Bootstrap</b> a new dbt data product (project file, model layout, README).</li>'
  '<li><b>Implement</b> the dbt models from the input and output data contracts.</li>'
  '<li><b>Example data</b>: pull sample rows, drop PII columns, upload the scrubbed sample.</li>'
  '<li><b>Edit and test data contracts</b> (ODCS) in plain language, and run <code>datacontract test</code> against live data.</li>'
  '<li><b>Sync</b> an existing dbt project with Entropy Data, including a GitHub Actions workflow, and pick an owning team.</li></ul>'
  '<p>It needs an Entropy Data account and API key, and <code>uv</code> for the CLIs. Install in Codex: <code>codex plugin marketplace add https://github.com/entropy-data/dataproduct-builder-dbt</code>, then <code>codex plugin add dataproduct-builder-dbt@dataproduct-builder-dbt</code>.</p>'
  '<p style="color:var(--mute)">Summarized from the project\'s README. Not tested by us. More: <a href="/best/data-backend">best backend and data plugins for Codex</a>.</p>'),
 # --- quick win: "devin plugins"
 ("p/devin-plugin-cc.html","after_re",_P_AFTER,
  '<h2>Devin plugins for Codex and Claude Code</h2><p>This open-source plugin brings Devin into your terminal agent. Per its README it can:</p><ul class=where>'
  '<li>Run a read-only Devin <b>code review</b> of your working tree or branch diff, plus an adversarial review of design choices.</li>'
  '<li><b>Delegate</b> a bounded coding task to Devin, with sessions you can resume.</li>'
  '<li>Hand off to a <b>cloud Devin session</b> at app.devin.ai with your repo, branch and uncommitted diff.</li>'
  '<li>Run a "Fusion" setup where your main agent leads and Devin does the mechanical or test-heavy work.</li></ul>'
  '<p>You need the Devin CLI signed in (or a <code>DEVIN_API_KEY</code> for cloud handoffs), Node.js 18.18+ and git. Install in Codex: <code>codex plugin marketplace add TheOnlyFusionCube/devin-plugin-cc</code>, then <code>codex plugin add devin@devin-plugin-cc</code>. Claude Code users run <code>claude plugin install devin@devin-plugin-cc</code> after adding the same marketplace.</p>'
  '<p style="color:var(--mute)">Summarized from the project\'s README. Not tested by us. More <a href="/c/agent-workflows">agent workflow plugins</a>.</p>'),
 # --- quick win: "mcp server directory"
 ("alternatives.html","before",'<p style="margin-top:30px">',
  '<p>Listing an MCP server rather than looking for one? Our <a href="/guides/where-to-submit-mcp-server">MCP server directory list</a> has every registry and how to submit.</p>'),
 ("guides/publish-codex-plugin.html","before",'<p style="margin-top:30px">',
  '<p>Does your plugin bundle an MCP server? List it in each <a href="/guides/where-to-submit-mcp-server">MCP server directory</a> too.</p>'),
 # --- page-two giant: /c/agent-workflows (122 impr, pos 14.5) -> answer + exact-anchor internal links
 ("c/agent-workflows.html","after_re",r'<p class=shelves><span class=mono>Ranked:</span>.*?</p>',
  '<p>Agent workflow plugins split work across several agents, enforce a plan-then-build loop, or wrap a whole delivery process for Codex and Claude Code. The ones worth trying keep their plan in files you can open, so a long run is easy to check. This shelf also has <a href="/p/devin-plugin-cc">Devin plugins for Codex</a>. Want a shortlist? See the <a href="/best/agent-workflows">best agent workflow plugins, ranked</a>.</p>'),
 ("best/agent-workflows.html","before",'<p style="color:var(--mute)">Stars measure popularity',
  '<p>Browse every one of the <a href="/c/agent-workflows">agent workflow plugins</a> on the shelf, newest first.</p>'),
 ("guides/install-codex-plugin.html","before",'<p style="margin-top:30px">',
  '<p>Looking for something to install? Most people start with <a href="/c/agent-workflows">agent workflow plugins</a>, then <a href="/c/review-testing">review and testing</a>.</p>'),
 ("faq.html","before",'<p style="margin-top:30px">',
  '<h2>Where should I start?</h2><p>The biggest shelf is <a href="/c/agent-workflows">agent workflow plugins</a>: orchestrators, specialist crews and spec-first pipelines. Then try <a href="/c/review-testing">review and testing</a> and <a href="/c/security-governance">security</a>.</p>'),
 ("guides/index.html","before",'</div><div style="border-top:3px solid var(--ink)">',
  '<p>New to plugins? Browse <a href="/c/agent-workflows">agent workflow plugins</a> first, it\'s the biggest shelf.</p>'),
]
_INJ_BY={}
for _r,_m,_k,_h in _INJECT: _INJ_BY.setdefault(_r,[]).append((_m,_k,_h))
def _apply_overrides(rel,h):
  rel=rel.replace(os.sep,"/")
  if rel in _TITLE_OVR: h=_re.sub(r"<title>.*?</title>","<title>"+e(_TITLE_OVR[rel])+"</title>",h,1)
  if rel in _DESC_OVR: h=_re.sub(r'<meta name=description content="[^"]*">','<meta name=description content="'+e(_DESC_OVR[rel])+'">',h,1)
  for _m,_k,_h in _INJ_BY.get(rel,[]):
    if _m=="before":
      if _k not in h: raise SystemExit(f"seo_overrides: marker not found in {rel}: {_k[:40]}")
      h=h.replace(_k,_h+_k,1)
    else:
      mm=_re.search(_k,h,_re.S)
      if not mm: raise SystemExit(f"seo_overrides: regex marker not found in {rel}: {_k[:40]}")
      h=h[:mm.end()]+_h+h[mm.end():]
  return h
