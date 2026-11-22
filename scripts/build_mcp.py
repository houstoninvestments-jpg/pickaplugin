# exec'd by build.py (uses P, PICKS, BLURB, FOUNDING_DATA, slug, layout, e, D, SITE_URL).
# Writes dist/catalog.json (data source for the /mcp endpoint in worker/index.js) and dist/mcp-server.html (docs).
import json as _j, base64 as _b64, urllib.parse as _up
MCP_URL=SITE_URL+"/mcp"
def _claimed_slugs():
  out=set()
  for c in FOUNDING_DATA.get("claimed") or []:
    if isinstance(c,str): out.add(c)
    elif isinstance(c,dict) and c.get("slug"): out.add(c["slug"])
  return out
_CL=_claimed_slugs()
def _tier(p):
  for k in ("top_spot","featured","belt"):
    if p.get(k): return k
  return "featured" if p["slug"] in _CL else None
_cat=[]
for p in P:
  t=_tier(p)
  _cat.append({k:v for k,v in {"slug":p["slug"],"name":p["name"],"summary":p["description"],"category":p["category"],
    "category_slug":slug(p["category"]),"maker":p.get("maker") or None,"repo":p["link"],"homepage":p.get("homepage") or None,"docs":p.get("docs") or None,
    "install":p.get("install") or None,"stars":p.get("stars") if isinstance(p.get("stars"),int) else None,"license":p.get("license") or None,
    "language":p.get("language") or None,"first_seen":p.get("first_seen"),"pushed_at":p.get("pushed_at") or None,"archived":bool(p.get("archived")),
    "featured":bool(t),"featured_tier":t,"editors_pick":p["slug"] in PICKS,"verified":bool(p.get("verified")),
    "url":f'{SITE_URL}/p/{p["slug"]}'}.items() if v is not None})
_cats=sorted({p["category"] for p in P})
_catinfo=[{"name":c,"slug":slug(c),"count":sum(1 for p in P if p["category"]==c),"blurb":BLURB.get(c,""),"url":f"{SITE_URL}/c/{slug(c)}"} for c in _cats]
_j.dump({"generated":__import__("datetime").date.today().isoformat(),"count":len(_cat),"categories":_catinfo,"plugins":_cat},
  open(D+"/catalog.json","w"),separators=(",",":"),ensure_ascii=False)

# ---- docs page ----
def _pre(t): return f'<pre class=code>{e(t)}</pre>'
_cfg_cursor=_j.dumps({"mcpServers":{"pickaplugin":{"url":MCP_URL}}},indent=2)
_cursor_link="cursor://anysphere.cursor-deeplink/mcp/install?name=pickaplugin&config="+_up.quote(_b64.b64encode(_j.dumps({"url":MCP_URL}).encode()).decode())
_vs=_j.dumps({"servers":{"pickaplugin":{"type":"http","url":MCP_URL}}},indent=2)
_vs_link="vscode:mcp/install?"+_up.quote(_j.dumps({"name":"pickaplugin","type":"http","url":MCP_URL},separators=(",",":")))
_cd=_j.dumps({"mcpServers":{"pickaplugin":{"command":"npx","args":["-y","mcp-remote",MCP_URL]}}},indent=2)
_curl=f"""curl -s {MCP_URL} \\
  -H 'content-type: application/json' -H 'accept: application/json, text/event-stream' \\
  -d '{{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{{"name":"search_plugins","arguments":{{"query":"memory","limit":3}}}}}}'"""
_GH="https://github.com/houstoninvestments-jpg/pickaplugin/tree/main/plugin"
open(D+"/mcp-server.html","w").write(layout("PickAPlugin MCP server: search 500+ plugins from your agent — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Free · read-only · no key needed</span><h1>The PickAPlugin MCP server</h1>
<p style="font-size:19px">Ask your agent “find me a plugin for X” and it searches the PickAPlugin catalog: about {len(P)//50*50} ChatGPT, Codex and Claude plugins and MCP servers, sorted into {len(_cats)} categories. It's a remote MCP server, so there's nothing to install or run.</p>
<p><b>Endpoint:</b> <code>{MCP_URL}</code> <span class=mono>(Streamable HTTP, no auth)</span></p>
<h3>Tools</h3><ul class=where>
<li><code>search_plugins(query, category?, limit?)</code>: keyword search across names, descriptions, makers and categories.</li>
<li><code>get_plugin(slug)</code>: full details for one listing, including its install command when we have one.</li>
<li><code>list_categories()</code>: every category with its plugin count.</li>
<li><code>top_plugins(category?, limit?)</code>: our editor's picks first, then the most-starred maintained projects.</li></ul>
<p>Every result has the name, a one-line summary, the category, the repo and homepage links, and its <code>pickaplugin.com/p/&lt;slug&gt;</code> page. Paid featured listings show up first and are always labelled <code>"featured": true</code>, so your agent can tell an ad from a pick.</p>
<h3>Claude Code</h3>{_pre(f"claude mcp add --transport http pickaplugin {MCP_URL}")}
<h3>Claude Desktop / claude.ai</h3><p>Settings → Connectors → <b>Add custom connector</b>, name it PickAPlugin and paste <code>{MCP_URL}</code>. Or, on older versions of Claude Desktop, add this to <code>claude_desktop_config.json</code> (needs Node):</p>{_pre(_cd)}
<h3>Cursor</h3><p><a class=btn href="{e(_cursor_link)}">Add to Cursor</a> or put this in <code>~/.cursor/mcp.json</code>:</p>{_pre(_cfg_cursor)}
<h3>Codex</h3>{_pre(f"codex mcp add pickaplugin --url {MCP_URL}")}<p>Or in <code>~/.codex/config.toml</code>:</p>{_pre(f'[mcp_servers.pickaplugin]{chr(10)}url = "{MCP_URL}"')}
<p>There's also a ready-made Codex plugin (<code>.codex-plugin/plugin.json</code> plus <code>.mcp.json</code>) in <a href="{_GH}">our repo</a>.</p>
<h3>VS Code (GitHub Copilot)</h3><p><a class=btn href="{e(_vs_link)}">Add to VS Code</a> or run:</p>{_pre(f"code --add-mcp '{_j.dumps({'name':'pickaplugin','type':'http','url':MCP_URL},separators=(',',':'))}'")}<p>Or add it to <code>.vscode/mcp.json</code>:</p>{_pre(_vs)}
<h3>ChatGPT</h3><p>With developer mode on: Settings → Apps &amp; Connectors → <b>Create</b>, paste <code>{MCP_URL}</code> and pick “No authentication”.</p>
<h3>Try it with curl</h3>{_pre(_curl)}
<h3>Good to know</h3><ul class=where><li>It's read-only and stores nothing about your queries beyond normal server logs.</li><li>The catalog updates daily. Descriptions are each project's own. We don't test or audit plugins, so check a project before you install it. <a href="guides/install-mcp-server-claude-cursor-codex.html">How to install an MCP server</a> in Claude Desktop, Cursor and Codex, and <a href="guides/check-mcp-server-safe.html">what to check first</a>.</li><li>Please keep it reasonable: up to 25 results per call. Need the whole catalog? It's at <a href="catalog.json">/catalog.json</a>.</li><li>Your plugin missing? <a href="submit.html">Submit it free</a>, then <a href="badge.html">add the badge</a>.</li></ul></div>""",0,
 "Free remote MCP server for Claude, Cursor, Codex, VS Code and ChatGPT: search 500+ AI plugins and MCP servers from your agent. Install snippets inside."))
