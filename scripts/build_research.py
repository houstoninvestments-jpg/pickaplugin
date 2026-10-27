# Executed by build.py before build_seo.py. Writes /research/state-of-codex-plugins-2026 (+ CSV) and /blog index
# from the frozen snapshot research/stats.json (made by research_fetch.py + research_analyze.py). Every number comes from there.
import json as _rj, csv as _rc, io as _rio
_S=_rj.load(open(os.path.join(ROOT,"research","stats.json"))); _n=_S["github_reachable"]
def _p(a,b=None): return f"{100*a/(b or _n):.0f}%"
def _bars(title,items,total,note=""):
  mx=max(v for _,v in items) or 1; h=34*len(items)+64; y=50; out=[]
  for lab,v in items:
    w=round(360*v/mx); out.append(f'<text x="0" y="{y+16}" font-family="Martian Mono,monospace" font-size="12" fill="#14171f">{e(lab)}</text><rect x="200" y="{y}" width="{max(w,2)}" height="22" fill="url(#hatch)" stroke="#14171f" stroke-width="1.2"/><text x="{208+w}" y="{y+16}" font-family="Martian Mono,monospace" font-size="12" fill="#1f3a8a">{v} · {100*v/total:.0f}%</text>'); y+=34
  return f'''<figure style="margin:26px 0;border-top:3px double #14171f;border-bottom:1px solid #14171f;padding:12px 0"><svg viewBox="0 0 680 {h}" width="100%" role="img" aria-label="{e(title)}" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="#f4efe1"/><line x1="0" y1="0" x2="0" y2="6" stroke="#1f3a8a" stroke-width="3"/></pattern></defs><text x="0" y="22" font-family="Newsreader,serif" font-size="21" font-weight="700" fill="#14171f">{e(title)}</text><line x1="200" y1="40" x2="200" y2="{h-6}" stroke="#14171f"/>{"".join(out)}</svg><figcaption class=mono style="font-size:12px;color:var(--mute)">{note or f"n = {total} repos · PickAPlugin, {_S['as_of']} · CC BY 4.0"}</figcaption></figure>'''
_lic=[(k if k!="NOASSERTION" else "Unrecognized file",v) for k,v in _S["license"]]
_lang=_S["lang"][:9]+[("Other",sum(v for _,v in _S["lang"][9:]))]
_lang=[(("None (docs only)" if k=="None" else k),v) for k,v in _lang]
_age=[("Pushed ≤7 days",_S["fresh7"]),("8–30 days",_S["fresh30"]-_S["fresh7"]),("31–89 days",_n-_S["fresh30"]-_S["stale90"]),("90–179 days",_S["stale90"]-_S["stale180"]),("180+ days",_S["stale180"])]
_ERR={"path_bad":"absolute or ../ path","name_not_kebab":"name not kebab-case","no_schema":"no $schema","no_version":"no version","no_displayName":"no displayName","path_no_dot_slash":"path missing ./","no_description":"no description"}
_csvrows=[("metric","value","denominator","percent","notes")]
def _m(k,v,d,note=""): _csvrows.append((k,v,d,f"{100*v/d:.1f}" if d else "",note))
_m("plugins_in_catalog",_S["catalog"],_S["catalog"]); _m("github_repos_analyzed",_n,_S["catalog"],"rest were unreachable or not on GitHub")
for k,v in _S["license"]: _m("license:"+k,v,_n,"NOASSERTION = license file GitHub could not identify")
_m("no_license_file",_S["no_license"],_n); _m("archived",_S["archived"],_n); _m("no_push_90_days",_S["stale90"],_n); _m("no_push_180_days",_S["stale180"],_n)
_m("pushed_last_30_days",_S["fresh30"],_n); _m("pushed_last_7_days",_S["fresh7"],_n); _m("repo_created_2026",_S["created_2026"],_n)
_m("stars_median",_S["stars_median"],_n,"median, not a share"); _m("stars_top10pct_share_of_all_stars",_S["top10pct_share"],100,"percent of all stars held by the top 10% of repos")
for k,v in _S["stars_buckets"]: _m("stars_bucket:"+k,v,_n)
for k,v in _S["lang"]: _m("language:"+k,v,_n,"GitHub primary language")
_m("readme_has_install_command",_S["install"],_n,"fenced code block with codex/claude plugin|mcp install/add, /plugin install, or npx skills add")
_m("readme_mentions_api_key_or_token",_S["apikey"],_n,"keyword heuristic on README")
_m("remote_http_mcp_server",_S["remote_mcp"],_n,"README or .mcp.json configures an http/sse MCP url")
_m("any_plugin_manifest",_S["any_manifest"],_n); _m("codex_manifest",_S["codex_manifest"],_n); _m("claude_manifest",_S["claude_manifest"],_n)
_m("has_AGENTS_md",_S["agents_md"],_n); _m("has_mcp_json",_S["mcp_json"],_n)
_m("plugin_json_checked",_S["pj_n"],_n); _m("plugin_json_invalid_json",_S["pj_invalid_json"],_S["pj_n"]); _m("plugin_json_with_error",_S["pj_with_err"],_S["pj_n"]); _m("plugin_json_no_issues",_S["pj_clean"],_S["pj_n"])
for k,v in _S["pj_err_codes"]: _m("plugin_json_error:"+k,v,_S["pj_n"])
for k,v in _S["pj_warn_codes"]: _m("plugin_json_warning:"+k,v,_S["pj_n"])
for k,v in _S["cat"]: _m("category:"+k,v,_S["catalog"])
_b=_rio.StringIO(); _rc.writer(_b).writerows(_csvrows)
os.makedirs(D+"/research",exist_ok=True)
_CSVN="state-of-codex-plugins-2026.csv"
open(D+"/research/"+_CSVN,"w").write(f"# State of Codex Plugins 2026, PickAPlugin ({SITE_URL}/research/state-of-codex-plugins-2026). Data as of {_S['as_of']}. License: CC BY 4.0, credit PickAPlugin with a link.\n"+_b.getvalue())
_RURL=SITE_URL+"/research/state-of-codex-plugins-2026"
_H1="State of Codex Plugins 2026: what 339 open-source ChatGPT and Codex plugins actually look like"
_pw=_S["pj_n"]-_S["pj_clean"]
_rb=f'''<div class=prose style="max-width:900px"><span class=mono style="color:var(--acc)">Research · data as of {_S["as_of"]} · CC BY 4.0</span>
<h1>{e(_H1)}</h1>
<p style="font-size:19px">We pulled GitHub data for every plugin in the PickAPlugin catalog and ran the same checks we'd run before installing one. Here's what came back. Every number on this page was computed from that pull. Nothing is estimated or surveyed.</p>
<div style="border:1px solid var(--ink);background:#fffdf8;padding:14px 18px;margin:18px 0"><b>The short version</b><ul class=where>
<li>This ecosystem is brand new: <b>{_S["created_2026"]} of {_n}</b> repos ({_p(_S["created_2026"])}) were created in 2026, and {_p(_S["fresh7"])} got a push in the last 7 days.</li>
<li>Attention is wildly lopsided. The median plugin has <b>{_S["stars_median"]:g} stars</b>, {_S["stars_buckets"][0][1]} have zero, and the top 10% of repos hold <b>{_S["top10pct_share"]:.0f}%</b> of all stars.</li>
<li>Licensing is mostly fine: {_p(dict(_S["license"])["MIT"])} are MIT. But {_S["no_license"]} have no license file at all and {_S["other_license"]} have one GitHub can't identify, which is {_p(_S["no_license"]+_S["other_license"])} where reuse rights are unclear.</li>
<li><b>{_n-_S["install"]} repos ({_p(_n-_S["install"])}) have no copyable install command</b> in their README.</li>
<li>{_S["apikey"]} READMEs ({_p(_S["apikey"])}) mention an API key or token, and {_S["remote_mcp"]} ({_p(_S["remote_mcp"])}) wire up a remote MCP server over HTTP.</li>
<li>Manifests are in better shape than we expected: of {_S["pj_n"]} plugin.json files, only {_S["pj_with_err"]} had a hard error, though {_pw} had at least one warning.</li></ul></div>
<h2>1. It's all new</h2><p>{_S["created_2026"]} of the {_n} repos we could reach were created this year. {_S["fresh30"]} ({_p(_S["fresh30"])}) were pushed to in the last 30 days. On the other end, {_S["stale90"]} ({_p(_S["stale90"])}) haven't had a push in 90+ days, {_S["stale180"]} in 180+, and {_S["archived"]} are archived. In a space this young, 90 days without a commit usually means the author moved on.</p>
{_bars("Days since last push",_age,_n)}
<h2>2. Stars: a few giants, a long tail</h2><p>Across {_n} repos there are {_S["stars_total"]:,} stars in total, but the median is {_S["stars_median"]:g}. The top tenth of repos hold {_S["top10pct_share"]:.0f}% of them. Stars measure attention, not quality, and most plugins here are small projects by one person. That's not bad, it just means you should read the code instead of trusting the count.</p>
{_bars("GitHub stars per repo",_S["stars_buckets"],_n)}
<h2>3. Licenses</h2><p>{dict(_S["license"])["MIT"]} repos use MIT and {dict(_S["license"])["Apache-2.0"]} use Apache-2.0. {_S["no_license"]} have no license file GitHub can find, which legally means "all rights reserved". Another {_S["other_license"]} have a license file GitHub couldn't match to a standard license, often a custom or modified text, so check it yourself.</p>
{_bars("License (GitHub detection)",_lic,_n)}
<h2>4. Languages</h2><p>Python and JavaScript lead. {dict(_S["lang"]).get("None",0)} repos have no primary language at all, meaning they're mostly Markdown skills, prompts and config. That's normal for plugins that are really instructions for the agent, not code.</p>
{_bars("Primary language",_lang,_n)}
<h2>5. Can you actually install it?</h2><p>We look for an install command in a fenced code block in the README: <code>codex plugin install</code>, <code>codex/claude mcp add</code>, <code>/plugin install</code>, <code>/plugin marketplace add</code> or <code>npx skills add</code>. {_S["install"]} repos ({_p(_S["install"])}) have one. The other {_n-_S["install"]} may still install fine, but you have to work it out. {_S["any_manifest"]} repos ship some plugin or marketplace manifest. {_S["claude_manifest"]} ({_p(_S["claude_manifest"])}) also ship a Claude Code manifest, so a lot of "Codex plugins" are cross-host. {_S["agents_md"]} have an AGENTS.md at the root.</p>
<h2>6. plugin.json health</h2><p>We ran the rules from our free <a href="../tools/plugin-json-validator.html">plugin.json validator</a> against the {_S["pj_n"]} repos with a manifest at <code>plugin.json</code>, <code>.codex-plugin/plugin.json</code> or <code>.claude-plugin/plugin.json</code> ({dict(_S["pj_loc"]).get("pj_codex",0)} use the <code>.codex-plugin</code> folder). All of them parsed as valid JSON. {_S["pj_clean"]} passed with no notes.</p>
{_bars("plugin.json issues found",[(_ERR.get(k,k),v) for k,v in _S["pj_err_codes"]+_S["pj_warn_codes"]],_S["pj_n"],f"n = {_S['pj_n']} manifests · the first {len(_S['pj_err_codes'])} rows are errors, the rest warnings · CC BY 4.0")}
<h2>7. Network access and API keys</h2><p>This one's a rough signal. {_S["apikey"]} READMEs ({_p(_S["apikey"])}) mention an API key, access token or a <code>SOMETHING_API_KEY</code> style variable. {_S["remote_mcp"]} ({_p(_S["remote_mcp"])}) configure a remote MCP server over HTTP or SSE, so your agent talks to someone else's server. Neither is a red flag on its own, but it's where you should slow down and read what gets sent where.</p>
<h2>8. Categories</h2><p>How we sort the catalog, by hand. Agent workflow tools (orchestration, planning, subagents) are the biggest group by far.</p>
{_bars("Category (PickAPlugin's sorting)",_S["cat"],_S["catalog"],f"n = {_S['catalog']} catalog entries · PickAPlugin, {_S['as_of']} · CC BY 4.0")}
<h2>Methodology</h2><ul class=where><li><b>Population:</b> the {_S["catalog"]} plugins in the PickAPlugin catalog on {_S["as_of"]}, gathered from public lists like awesome-codex-plugins and from maker submissions. {_n} were reachable GitHub repos; {_S["unreachable"]} weren't (deleted, private or not on GitHub) and are left out.</li>
<li><b>Data:</b> one GitHub GraphQL pull on {_S["as_of"]}: stars, archived flag, last push, creation date, license detection, primary language, README.md, and the files plugin.json, .codex-plugin/plugin.json, .claude-plugin/plugin.json, .agents/plugins/marketplace.json, .claude-plugin/marketplace.json, .mcp.json and AGENTS.md at the default branch root.</li>
<li><b>Checks:</b> install commands are matched with a regex on README code blocks. plugin.json rules are a Python port of our public validator. API-key and remote-MCP flags are keyword matches on the README and .mcp.json.</li></ul>
<h2>Limits</h2><ul class=where><li>Our catalog isn't every plugin out there. It leans toward plugins listed on GitHub lists, so it's a sample, not a census.</li>
<li>We only read root-level files. Monorepos or plugins in subfolders can be missed, which undercounts manifests and install commands.</li>
<li>The API-key and network numbers are keyword heuristics. They miss plugins that don't document it, and can count a README that only mentions keys in passing.</li>
<li>"Last push" counts any push, including small doc edits. Stars can be gamed. Licenses are what GitHub detects.</li>
<li>Categories are our own editorial sorting.</li></ul>
<h2>Use the data</h2><p>Download the aggregate numbers: <a href="{_CSVN}" download>state-of-codex-plugins-2026.csv</a>. It's licensed <a href="https://creativecommons.org/licenses/by/4.0/" rel=license>CC BY 4.0</a>. Use it however you like, just credit "PickAPlugin" with a link to this page. Questions or spot an error? Email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p><a href="../index.html#catalog">← Browse all {_S["catalog"]} plugins</a> · <a href="../blog.html">Blog</a> · <a href="../tools/index.html">Free tools</a></p></div>
<script type="application/ld+json">{_rj.dumps([{"@context":"https://schema.org","@type":"Article","headline":_H1,"datePublished":_S["as_of"],"dateModified":_S["as_of"],"url":_RURL,"author":{"@type":"Organization","name":"PickAPlugin","url":SITE_URL+"/"},"publisher":{"@type":"Organization","name":"PickAPlugin","url":SITE_URL+"/"},"image":SITE_URL+"/og.png"},
 {"@context":"https://schema.org","@type":"Dataset","name":"State of Codex Plugins 2026 (aggregate statistics)","description":f"Aggregate statistics on {_n} open-source ChatGPT and Codex plugin repositories: licenses, maintenance, stars, languages, install commands, plugin.json validation, API key and remote MCP use, categories.","url":_RURL,"license":"https://creativecommons.org/licenses/by/4.0/","creator":{"@type":"Organization","name":"PickAPlugin","url":SITE_URL+"/"},"datePublished":_S["as_of"],"temporalCoverage":_S["as_of"],"isAccessibleForFree":True,"keywords":["Codex plugins","ChatGPT plugins","MCP","open source","GitHub"],"distribution":[{"@type":"DataDownload","encodingFormat":"text/csv","contentUrl":SITE_URL+"/research/"+_CSVN}]}]).replace("</","<\\/")}</script>'''
open(D+"/research/state-of-codex-plugins-2026.html","w").write(layout("State of Codex Plugins 2026: data on 339 open-source ChatGPT & Codex plugins — PickAPlugin",_rb,1,
 f"Original data on {_n} open-source ChatGPT and Codex plugins: {_p(_S['no_license']+_S['other_license'])} with unclear licenses, {_p(_n-_S['install'])} with no install command, median {_S['stars_median']:g} stars. Methodology and CC BY CSV."))
_bl=[("research/state-of-codex-plugins-2026.html","State of Codex Plugins 2026","Original data on "+str(_n)+" plugin repos: licenses, maintenance, stars, install commands and plugin.json health. CSV included.",_S["as_of"]),
 ("blog/best-codex-plugins-november-2026.html","Best Codex plugins (November 2026)","The most-starred, still-maintained plugins in each category, with install commands.","2026-10-27")]
open(D+"/blog.html","w").write(layout("Blog & research — PickAPlugin",'<div class=prose style="max-width:900px"><span class=mono style="color:var(--acc)">Blog &amp; research</span><h1>Writing and data from PickAPlugin</h1><div style="border-top:3px solid var(--ink)">'+"".join(f'<a class=row style="grid-template-columns:1fr" href="{u}"><span><h3>{e(t)}</h3><p>{e(d)} <span class=mono style="color:var(--mute)">{dt}</span></p></span></a>' for u,t,d,dt in _bl)+'</div></div>',0,"Articles and original research on ChatGPT and Codex plugins from PickAPlugin."))
print("research: report + csv + blog index")
