# Executed by build.py before build_seo.py (shares its namespace: P, D, layout, e, slug, by, cats).
# Writes free single-purpose tool pages under /tools. Everything runs in the visitor's browser.
import json as _tj
os.makedirs(D+"/tools",exist_ok=True)
TCSS="""<style>
.tool{border-top:3px solid var(--ink);margin:18px 0 8px;padding-top:14px}
.tool label{display:block;font:500 11px 'Martian Mono',monospace;text-transform:uppercase;color:var(--mute);margin:12px 0 4px}
.tool textarea,.tool input,.tool select{width:100%;box-sizing:border-box;border:1px solid var(--ink);background:#fffdf8;font:13.5px/1.5 'Martian Mono',ui-monospace,monospace;padding:9px 10px;color:var(--ink)}
.tool textarea{min-height:220px}
.tool .two{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:760px){.tool .two{grid-template-columns:1fr}}
.tool button{border:1px solid var(--ink);background:var(--ink);color:var(--paper);padding:8px 14px;font:500 11px 'Martian Mono',monospace;text-transform:uppercase;cursor:pointer;margin:10px 8px 0 0}
.tool button.alt{background:transparent;color:var(--ink)}
.tool pre{white-space:pre-wrap;word-break:break-word;border:1px solid var(--rule);background:#fffdf8;padding:10px;font:13px/1.5 'Martian Mono',monospace;min-height:60px;margin:0}
.res{list-style:none;padding:0;margin:10px 0}
.res li{padding:6px 0;border-bottom:1px solid var(--rule);font-size:15.5px}
.res b.err{color:#8a1f1f}.res b.warn{color:#7a5a00}.res b.ok{color:#1d5b33}
.faq2 h3{font-size:19px}
</style>"""
def _faq_ld(qa):
  return '<script type="application/ld+json">'+_tj.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":_re.sub("<[^>]+>","",a)}} for q,a in qa]}).replace("</","<\\/")+'</script>'
def _faq_html(qa): return '<div class=faq2><h2 style="font:700 28px Newsreader,serif;margin-top:40px">Questions people ask</h2>'+"".join(f"<h3>{e(q)}</h3><p>{a}</p>" for q,a in qa)+'</div>'
def _cat_links(cs):
  return " · ".join(f'<a href="../best/{slug(c)}.html">best {e(c)} plugins</a>' for c in cs if c in cats)
def _plinks(slugs):
  ps=[by[s] for s in slugs if s in by]
  return "".join(f'<li><a href="../p/{p["slug"]}.html">{e(p["name"])}</a>: {e(p["description"][:120])}</li>' for p in ps)
TOOLS=[]
def tool(sl,title,h1,desc,intro,ui,js,qa,catsl,plugs,blurb):
  TOOLS.append((sl,h1,blurb))
  body=f'''{TCSS}<div class=prose style="max-width:980px"><span class=mono style="color:var(--acc)">Free tool · runs in your browser</span><h1>{h1}</h1>
<p style="font-size:19px">{intro}</p>
<div class=tool>{ui}</div>
<p style="color:var(--mute);font-size:14.5px">Nothing you paste here gets sent anywhere. It's plain JavaScript in this page. We wrote it, so if it gets something wrong, tell us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
{_faq_html(qa)}
<h3>Related on PickAPlugin</h3><p>{_cat_links(catsl)}</p>{f"<ul class=where>{_plinks(plugs)}</ul>" if _plinks(plugs) else ""}
<p><a href="index.html">← All free tools</a> · <a href="../index.html#catalog">Browse all {len(P)} plugins</a></p></div>
{_faq_ld(qa)}<script>{js}</script>'''
  open(f"{D}/tools/{sl}.html","w").write(layout(title,body,1,desc))

# ---------- 1. plugin.json validator ----------
tool("plugin-json-validator","plugin.json validator for ChatGPT & Codex plugins — PickAPlugin",
 "Check your plugin.json before you ship it",
 "Free plugin.json checker for ChatGPT and Codex plugins. Paste a root plugin.json, .codex-plugin/plugin.json or marketplace.json and see what's missing or broken.",
 "Paste your <code>plugin.json</code>, <code>.codex-plugin/plugin.json</code> or <code>.agents/plugins/marketplace.json</code> and it'll tell you what's broken, what's missing, and what's just a nice-to-have. It checks the stuff that trips people up most: the name format, paths that don't start with <code>./</code>, and marketplace entries missing their policy.",
 '''<label for=pj>Your JSON</label><textarea id=pj spellcheck=false placeholder='{"name": "my-plugin", ...}'></textarea>
<button onclick=run()>Check it</button><button class=alt onclick=ex()>Load an example</button><ul class=res id=out></ul>''',
 r'''
const $=id=>document.getElementById(id);
function ex(){$("pj").value=JSON.stringify({"$schema":"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json","name":"My Plugin","version":"0.1","description":"Does a thing","extensions":{"com.openai":{"apps":".app.json","interface":{"displayName":"My Plugin","logo":"../logo.png"}}}},null,2);run()}
function path(r,k,v){if(typeof v!=="string")return;if(v==="")r.push(["err",k+" is an empty string."]);else if(/^https?:|^data:/.test(v))return;else if(v.startsWith("/")||/^[A-Za-z]:\\/.test(v))r.push(["err",k+" is an absolute path ("+v+"). Use a path relative to the plugin root, like ./"+v.replace(/^\/+/,"")]);else if(v.split("/").includes(".."))r.push(["err",k+" uses .. and points outside the plugin root ("+v+")."]);else if(!v.startsWith("./"))r.push(["warn",k+" should start with ./ (got "+v+")."])}
function plugin(j,r){
 if(!j.name)r.push(["err","name is missing. It's the one field every host needs."]);
 else if(!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(j.name))r.push(["err","name should be kebab-case, like "+String(j.name).toLowerCase().replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"")+". Hosts use it as the plugin id."]);
 else r.push(["ok","name looks good: "+j.name]);
 if(!j.version)r.push(["warn","No version. Not strictly required, but you'll want one before anyone installs it."]);
 else if(!/^\d+\.\d+\.\d+([-+].*)?$/.test(j.version))r.push(["warn","version \""+j.version+"\" isn't semver (like 0.1.0). Allowed, but semver is recommended."]);
 if(!j.description)r.push(["warn","No description. This is what people see when deciding whether to install."]);
 else if(j.description.length<20)r.push(["warn","description is really short. One clear sentence about what it does helps a lot."]);
 if(!j["$schema"]&&!("interface" in j)&&!j.skills)r.push(["warn","No $schema. Portable manifests usually start with \"$schema\": \"https://agent-plugins.org/schemas/1.0.0/plugin.schema.json\"."]);
 if(j.author!==undefined&&typeof j.author!=="string"&&(typeof j.author!=="object"||!j.author.name))r.push(["err","author should be a string or an object with a name."]);
 const o=(j.extensions&&j.extensions["com.openai"])||j;
 const pre=o===j?"":"extensions.com.openai.";
 ["skills","apps","hooks","onboardingSkill"].forEach(k=>{const v=o[k];if(Array.isArray(v))v.forEach((x,i)=>path(r,pre+k+"["+i+"]",x));else path(r,pre+k,v)});
 if(typeof o.mcpServers==="string")path(r,pre+"mcpServers",o.mcpServers);
 if(o.interface!==undefined){if(typeof o.interface!=="object")r.push(["warn",pre+"interface should be an object."]);else{const f=o.interface;
  ["composerIcon","logo","logoDark"].forEach(k=>path(r,pre+"interface."+k,f[k]));(f.screenshots||[]).forEach((x,i)=>path(r,pre+"interface.screenshots["+i+"]",x));
  if(!f.displayName)r.push(["warn","interface.displayName is missing, so the name shown in the app falls back to something less friendly."]);
  if(f.brandColor&&!/^#[0-9a-fA-F]{6}$/.test(f.brandColor))r.push(["warn","brandColor should be a hex color like #10A37F."]);
  ["websiteURL","privacyPolicyURL","termsOfServiceURL"].forEach(k=>{if(f[k]&&!/^https:\/\//.test(f[k]))r.push(["warn","interface."+k+" should be an https:// URL."])});
  if(f.defaultPrompt&&!Array.isArray(f.defaultPrompt))r.push(["warn","interface.defaultPrompt is usually an array of example prompts."]);}}
 if(JSON.stringify(j).match(/(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|clientSecret)/))r.push(["err","This looks like it contains a secret or a clientSecret field. Keep credentials out of the manifest."]);
}
function market(j,r){
 if(!j.name)r.push(["err","Marketplace has no top-level name."]);
 if(!j.interface||!j.interface.displayName)r.push(["warn","No interface.displayName, so the marketplace title in the app won't be what you want."]);
 if(!Array.isArray(j.plugins)||!j.plugins.length){r.push(["err","plugins should be a non-empty array."]);return}
 j.plugins.forEach((p,i)=>{const t="plugins["+i+"] ("+(p.name||"no name")+")";
  if(!p.name)r.push(["err",t+": missing name."]);
  if(!p.source)r.push(["err",t+": missing source."]);else if(typeof p.source==="string")path(r,t+" source",p.source);
  else{const s=p.source.source;if(s==="local")path(r,t+" source.path",p.source.path);else if(s==="url"||s==="git-subdir"){if(!p.source.url)r.push(["err",t+": git source needs a url."]);if(s==="git-subdir")path(r,t+" source.path",p.source.path)}else if(s==="npm"){if(!p.source.package)r.push(["err",t+": npm source needs a package."]);if(p.source.registry&&!/^https:\/\//.test(p.source.registry))r.push(["err",t+": registry must be https."])}else r.push(["warn",t+": source.source is \""+s+"\". Expected local, url, git-subdir or npm."])}
  if(!p.policy||!p.policy.installation)r.push(["err",t+": missing policy.installation (AVAILABLE, INSTALLED_BY_DEFAULT or NOT_AVAILABLE)."]);
  else if(!["AVAILABLE","INSTALLED_BY_DEFAULT","NOT_AVAILABLE"].includes(p.policy.installation))r.push(["warn",t+": policy.installation \""+p.policy.installation+"\" isn't one of the documented values."]);
  if(!p.policy||!p.policy.authentication)r.push(["err",t+": missing policy.authentication (like ON_INSTALL)."]);
  if(!p.category)r.push(["err",t+": missing category."]);});
 r.push(["ok",j.plugins.length+" plugin entr"+(j.plugins.length===1?"y":"ies")+" checked."]);
}
function run(){const r=[];let j;const t=$("pj").value.trim();
 if(!t){$("out").innerHTML="<li>Paste something first.</li>";return}
 try{j=JSON.parse(t)}catch(x){$("out").innerHTML="<li><b class=err>Not valid JSON.</b> "+x.message.replace(/</g,"&lt;")+". Trailing commas and comments are the usual culprits.</li>";return}
 if(typeof j!=="object"||Array.isArray(j)){$("out").innerHTML="<li><b class=err>Expected a JSON object at the top level.</b></li>";return}
 if(Array.isArray(j.plugins)){r.push(["ok","This looks like a marketplace.json."]);market(j,r)}else{r.push(["ok","This looks like a plugin manifest."]);plugin(j,r)}
 const n={err:0,warn:0};r.forEach(x=>n[x[0]]!==undefined&&n[x[0]]++);
 r.unshift([n.err?"err":"ok",n.err?n.err+" thing"+(n.err>1?"s":"")+" to fix, "+n.warn+" suggestion"+(n.warn===1?"":"s")+".":"No blocking problems found"+(n.warn?", "+n.warn+" suggestion"+(n.warn>1?"s":"")+".":".")]);
 const L={err:"Fix",warn:"Heads up",ok:"OK"};
 $("out").innerHTML=r.map(x=>"<li><b class="+x[0]+">"+L[x[0]]+":</b> "+x[1].replace(/</g,"&lt;")+"</li>").join("")}
''',
 [("Where does plugin.json go?","For a portable plugin, put <code>plugin.json</code> at the plugin root. Older Codex plugins use <code>.codex-plugin/plugin.json</code>, which OpenAI still supports as a fallback. This checker handles both."),
  ("What fields does a Codex plugin.json need?","<code>name</code> is the one that really matters, and it should be kebab-case. <code>version</code> and <code>description</code> are strongly recommended. OpenAI-specific stuff like <code>interface</code>, <code>apps</code> and <code>hooks</code> lives under <code>extensions.com.openai</code>."),
  ("Why does every path need to start with ./?","Paths are resolved from the plugin root. OpenAI's docs say to keep them relative and starting with <code>./</code>. Absolute paths or anything with <code>..</code> can point outside the package and break once it's installed."),
  ("Does this check my marketplace.json too?","Yes. If your JSON has a <code>plugins</code> array, it's treated as a marketplace and each entry is checked for a source, <code>policy.installation</code>, <code>policy.authentication</code> and <code>category</code>."),
  ("Is this the official validator?","No. It's a quick check we wrote based on OpenAI's published docs. It catches the common mistakes but it doesn't replace testing your plugin in Codex or the ChatGPT app.")],
 ["Agent Workflows","Review & Testing"],[],
 "Paste a plugin.json or marketplace.json and see what's broken.")

# ---------- 2. MCP config converter ----------
tool("mcp-config-converter","MCP config converter: JSON to Codex config.toml and back — PickAPlugin",
 "Convert MCP server config between Claude, Cursor, VS Code and Codex",
 "Free MCP config converter. Turn an mcpServers JSON block from Claude Desktop, Cursor or VS Code into Codex config.toml, or go the other way. Runs in your browser.",
 "Every app wants its MCP servers written a little differently. Claude Desktop and Cursor use an <code>mcpServers</code> JSON object, VS Code uses <code>servers</code>, and Codex wants TOML tables in <code>~/.codex/config.toml</code>. Paste one, pick where it's going, and copy the result.",
 '''<div class=two><div><label for=src>Paste your config (JSON or Codex TOML)</label><textarea id=src spellcheck=false></textarea></div>
<div><label for=to>Convert to</label><select id=to><option value=codex>Codex (~/.codex/config.toml)</option><option value=claude>Claude Desktop / Claude Code / Cursor (mcpServers JSON)</option><option value=vscode>VS Code (.vscode/mcp.json)</option></select>
<label>Result</label><pre id=res></pre></div></div>
<button onclick=conv()>Convert</button><button class=alt onclick=cp()>Copy result</button><button class=alt onclick=ex()>Load an example</button><ul class=res id=msg></ul>''',
 r'''
const $=id=>document.getElementById(id);
function ex(){$("src").value=JSON.stringify({mcpServers:{filesystem:{command:"npx",args:["-y","@modelcontextprotocol/server-filesystem","/Users/you/Documents"]},github:{command:"npx",args:["-y","@modelcontextprotocol/server-github"],env:{GITHUB_TOKEN:"your-token-here"}},docs:{type:"http",url:"https://example.com/mcp",headers:{Authorization:"Bearer your-token"}}}},null,2);conv()}
function q(s){return JSON.stringify(String(s))}
function key(k){return /^[A-Za-z0-9_-]+$/.test(k)?k:q(k)}
function inl(o){return "{ "+Object.entries(o).map(([k,v])=>key(k)+" = "+q(v)).join(", ")+" }"}
// tiny TOML reader for [mcp_servers.x] tables only
function readToml(t){const out={};let cur=null,sub=null;
 t.split(/\r?\n/).forEach(line=>{line=line.replace(/^\s+|\s+$/g,"");if(!line||line[0]==="#")return;
  let m=line.match(/^\[mcp_servers\.("?)([^"\]]+)\1(?:\.(env|http_headers))?\]$/);
  if(m){cur=out[m[2]]=out[m[2]]||{};sub=m[3]?(cur[m[3]]=cur[m[3]]||{}):null;return}
  if(line[0]==="["){cur=null;return}
  m=line.match(/^("?)([^"=]+?)\1\s*=\s*(.+)$/);if(!m||!cur)return;
  let v=m[3].trim().replace(/^\{(.*)\}$/,(a,b)=>"{"+b.replace(/([A-Za-z0-9_-]+)\s*=/g,'"$1":')+"}");
  try{v=JSON.parse(v)}catch(x){v=m[3].trim()}
  (sub||cur)[m[2].trim()]=v});
 return out}
function norm(src){const t=src.trim();let j;
 if(t[0]==="{"){j=JSON.parse(t);const s=j.mcpServers||j.servers||j.mcp_servers||(j.mcp&&j.mcp.servers);if(!s)throw new Error("Couldn't find mcpServers or servers in that JSON.");return s}
 const s=readToml(t);if(!Object.keys(s).length)throw new Error("Couldn't find any [mcp_servers.name] tables in that TOML.");
 Object.values(s).forEach(v=>{if(v.http_headers){v.headers=v.http_headers;delete v.http_headers}});return s}
function conv(){const msg=[];let s;
 try{s=norm($("src").value)}catch(x){$("res").textContent="";$("msg").innerHTML="<li><b class=err>Couldn't read that:</b> "+x.message.replace(/</g,"&lt;")+"</li>";return}
 const to=$("to").value;let o="";
 if(to==="codex"){for(const[n,v]of Object.entries(s)){o+="[mcp_servers."+key(n)+"]\n";
   if(v.url){o+="url = "+q(v.url)+"\n";if(v.headers&&Object.keys(v.headers).length){o+="http_headers = "+inl(v.headers)+"\n";if(JSON.stringify(v.headers).match(/Bearer /i))msg.push(["warn",n+": you've got a token pasted in. Codex can read it from an environment variable instead with bearer_token_env_var."])}}
   else{if(v.command)o+="command = "+q(v.command)+"\n";if(v.args&&v.args.length)o+="args = ["+v.args.map(q).join(", ")+"]\n";if(v.env&&Object.keys(v.env).length)o+="env = "+inl(v.env)+"\n"}
   if(v.cwd)o+="cwd = "+q(v.cwd)+"\n";o+="\n"}
  msg.push(["ok","Paste this into ~/.codex/config.toml (or .codex/config.toml in a trusted project)."])}
 else{const vs=to==="vscode",r={};
  for(const[n,v]of Object.entries(s)){const e={};
   if(v.url){e.type=vs?"http":(v.type&&v.type!=="streamable-http"?v.type:"http");e.url=v.url;if(v.headers)e.headers=v.headers}
   else{if(vs)e.type="stdio";e.command=v.command;if(v.args)e.args=v.args;if(v.env)e.env=v.env}
   if(v.cwd)e.cwd=v.cwd;r[n]=e}
  o=JSON.stringify(vs?{servers:r}:{mcpServers:r},null,2);
  msg.push(["ok",vs?"Save as .vscode/mcp.json in your workspace.":"Claude Desktop: claude_desktop_config.json. Claude Code: .mcp.json in your project. Cursor: .cursor/mcp.json. Claude Desktop adds remote (url) servers through Settings > Connectors instead."])}
 if(JSON.stringify(s).match(/(sk-[A-Za-z0-9]{10,}|ghp_[A-Za-z0-9]{10,})/))msg.push(["warn","That config has what looks like a real API key in it. Fine for your own machine, but don't commit it."]);
 $("res").textContent=o.trim();$("msg").innerHTML=msg.map(x=>"<li><b class="+x[0]+">"+(x[0]==="ok"?"Where it goes":"Heads up")+":</b> "+x[1]+"</li>").join("")}
function cp(){navigator.clipboard.writeText($("res").textContent)}
''',
 [("How do I add an MCP server to Codex?","Add a <code>[mcp_servers.name]</code> table to <code>~/.codex/config.toml</code> with a <code>command</code> and <code>args</code> for a local server, or a <code>url</code> for a remote one. You can also run <code>codex mcp add</code>. This page writes the TOML for you."),
  ("How do I convert claude_desktop_config.json to Codex config.toml?","Paste the whole file (or just the <code>mcpServers</code> part) on the left, choose Codex, and hit Convert. Each server becomes its own TOML table, with <code>env</code> and headers as inline tables."),
  ("Why does VS Code use servers instead of mcpServers?","That's just how VS Code's <code>.vscode/mcp.json</code> is defined. It also wants a <code>type</code> on every entry, so the converter adds <code>stdio</code> or <code>http</code>."),
  ("Does it handle Codex-only settings like startup_timeout_sec?","It keeps the common fields: command, args, env, cwd, url and headers. Codex-only extras like timeouts or <code>bearer_token_env_var</code> you'll need to add by hand after converting."),
  ("Is my config uploaded anywhere?","No. The conversion is a few dozen lines of JavaScript in this page. Your keys stay in your browser.")],
 ["Agent Workflows","Data & Backend","Deploy & DevOps"],["codex-reset","codex-rg-guard","token-optimizer"],
 "Turn mcpServers JSON into Codex config.toml, or back again.")

# ---------- 3. install command finder ----------
_idx=[{"s":p["slug"],"n":p["name"],"l":p["link"].lower().rstrip("/"),"i":p.get("install") or "","c":p["category"]} for p in P]
tool("plugin-install-command","Codex plugin install command finder — PickAPlugin",
 "Find the install command for any Codex plugin",
 f"Paste a GitHub link and get the command to install that Codex plugin or marketplace. We check it against the {len(P)} plugins in our catalog first.",
 f"Got a GitHub link for a plugin and no idea what to type? Paste it here. If it's one of the {len(P)} plugins we track, you get the install line we pulled from its README. If not, you get the standard <code>codex plugin marketplace add</code> command, plus what to check first.",
 '''<label for=u>GitHub link or owner/repo</label><input id=u placeholder="https://github.com/owner/repo" onkeydown="if(event.key==='Enter')go()">
<label for=ref>Pin to a branch or tag (optional)</label><input id=ref placeholder="main, v1.2.0 ...">
<button onclick=go()>Get the command</button><div id=o style="margin-top:14px"></div>''',
 "const IDX="+_tj.dumps(_idx).replace("</","<\\/")+r''';
const $=id=>document.getElementById(id);const H=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
function go(){let v=$("u").value.trim().replace(/\.git$/,"").replace(/\/+$/,"");const ref=$("ref").value.trim();
 let m=v.match(/github\.com[/:]([^/\s]+)\/([^/\s#?]+)/i)||v.match(/^([A-Za-z0-9_.-]+)\/([A-Za-z0-9_.-]+)$/);
 if(!m){$("o").innerHTML="<p>That doesn't look like a GitHub repo. Try something like <code>owner/repo</code>.</p>";return}
 const or=m[1]+"/"+m[2],key="https://github.com/"+or.toLowerCase();
 const hits=IDX.filter(p=>p.l===key||p.l.startsWith(key+"/"));
 const std="codex plugin marketplace add "+or+(ref?" --ref "+ref:"");
 let h="";
 if(hits.length){h+="<p><b>We have "+(hits.length>1?hits.length+" plugins from this repo":"this one")+" in the catalog.</b></p>";
  hits.forEach(p=>{h+="<div class=box><h3><a href='../p/"+p.s+".html'>"+H(p.n)+"</a></h3><p class=mono>"+H(p.c)+"</p>"+(p.i?"<p>From its README:</p><pre>"+H(p.i)+"</pre>":"<p>Its README doesn't show a one-line install, so try the standard command below.</p>")+"</div>"})}
 else h+="<p>This repo isn't in our catalog yet. If it's a plugin, you can <a href='../submit.html'>submit it</a> for free.</p>";
 h+="<label>Standard Codex command</label><pre>"+H(std)+"</pre><button class=alt onclick='navigator.clipboard.writeText("+H(JSON.stringify(std))+")'>Copy</button>";
 h+="<p style='font-size:15px'>That works when the repo has a marketplace file at <code>.agents/plugins/marketplace.json</code> (or the older <code>.claude-plugin/marketplace.json</code>). After adding it, open the Plugins Directory in the ChatGPT desktop app or run <code>codex plugin marketplace list</code> to see what it added. Have a quick look at the code before you install anything.</p>";
 $("o").innerHTML=h}
''',
 [("How do I install a Codex plugin from GitHub?","Run <code>codex plugin marketplace add owner/repo</code>. That adds the repo as a marketplace. Then install the plugin from the Plugins Directory in the ChatGPT desktop app. Add <code>--ref</code> if you want to pin a branch or tag."),
  ("Why didn't the command work for my repo?","The repo needs a marketplace file, usually <code>.agents/plugins/marketplace.json</code>. Some plugins are installed a different way, like <code>npx skills add</code> or <code>codex mcp add</code>, which is why we show the README's own command when we have it."),
  ("How do I see or remove marketplaces I've added?","<code>codex plugin marketplace list</code> shows them, <code>codex plugin marketplace upgrade</code> refreshes them, and <code>codex plugin marketplace remove name</code> takes one off."),
  ("Where do your install commands come from?","From each project's README, pulled by our daily catalog script. We don't run them ourselves, so give the code a look before you install.")],
 ["Agent Workflows","Memory & Context","Usage & Quotas"],[],
 f"Paste a GitHub link, get the install command. Checks our {len(P)} plugins first.")

# ---------- 4. AGENTS.md generator ----------
tool("agents-md-generator","AGENTS.md generator for Codex (free, no signup) — PickAPlugin",
 "Write an AGENTS.md for your repo in a couple of minutes",
 "Free AGENTS.md generator for Codex and other coding agents. Fill in your commands and rules, copy the Markdown, commit it. Runs in your browser.",
 "<code>AGENTS.md</code> is the file Codex reads before it touches your code. It's where you tell it how to install, test and lint, and what not to touch. Fill in what you know, skip what you don't, and copy the result into your repo root.",
 '''<div class=two><div>
<label for=nm>Project name</label><input id=nm placeholder="my-app">
<label for=ds>What it is, in a sentence</label><input id=ds placeholder="A Next.js storefront with a Postgres database">
<label for=st>Stack (one per line)</label><textarea id=st style="min-height:70px" placeholder="TypeScript, Next.js 15&#10;Postgres via Prisma"></textarea>
<label for=cm>Commands (one per line, like: test: npm test)</label><textarea id=cm style="min-height:90px">install: npm install
dev: npm run dev
test: npm test
lint: npm run lint</textarea>
<label for=sy>Code style (one per line)</label><textarea id=sy style="min-height:70px"></textarea>
<label for=nv>Never do (one per line)</label><textarea id=nv style="min-height:70px">Don't edit generated files in dist/
Don't add new dependencies without asking</textarea>
<label for=pr>Before you finish / PR rules (one per line)</label><textarea id=pr style="min-height:70px">Run the tests and lint and make sure they pass
Keep changes small and focused</textarea>
</div><div><label>Your AGENTS.md</label><pre id=md style="min-height:520px"></pre>
<button onclick=cp()>Copy</button><button class=alt onclick=dl()>Download</button></div></div>''',
 r'''
const $=id=>document.getElementById(id);const ids=["nm","ds","st","cm","sy","nv","pr"];
const L=id=>$(id).value.split("\n").map(s=>s.trim()).filter(Boolean);
function gen(){let o="";const n=$("nm").value.trim(),d=$("ds").value.trim();
 o+="# "+(n||"AGENTS.md")+"\n\n";if(d)o+=d+"\n\n";
 if(L("st").length)o+="## Stack\n\n"+L("st").map(x=>"- "+x).join("\n")+"\n\n";
 if(L("cm").length){o+="## Commands\n\n";L("cm").forEach(x=>{const m=x.match(/^([^:]{1,30}):\s*(.+)$/);o+=m?"- "+m[1].trim()+": `"+m[2].trim()+"`\n":"- `"+x+"`\n"});o+="\n"}
 if(L("sy").length)o+="## Code style\n\n"+L("sy").map(x=>"- "+x).join("\n")+"\n\n";
 if(L("nv").length)o+="## Don't\n\n"+L("nv").map(x=>"- "+x).join("\n")+"\n\n";
 if(L("pr").length)o+="## Before you finish\n\n"+L("pr").map(x=>"- "+x).join("\n")+"\n";
 $("md").textContent=o.trim()+"\n"}
ids.forEach(i=>$(i).addEventListener("input",gen));gen();
function cp(){navigator.clipboard.writeText($("md").textContent)}
function dl(){const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([$("md").textContent],{type:"text/markdown"}));a.download="AGENTS.md";a.click()}
''',
 [("What is AGENTS.md?","A plain Markdown file in your repo that tells coding agents how to work on the project: what it is, how to build and test it, and the rules to follow. Codex reads it, and so do a lot of other agents. The format is described at agents.md."),
  ("Where do I put AGENTS.md?","In the root of your repo. Codex also picks up AGENTS.md files in subfolders, and the one closest to the file being edited wins, so big monorepos can have one per package."),
  ("What should go in it?","The commands an agent should run (install, test, lint), anything unusual about your stack, and the things it must not do. Short and specific beats long and vague. If you'd tell a new teammate on day one, it belongs here."),
  ("Do I need CLAUDE.md as well?","Claude Code reads CLAUDE.md. A common trick is a one-line CLAUDE.md that just says <code>@AGENTS.md</code>, so you only keep one file up to date."),
  ("Does this use AI to write the file?","No. It just turns what you type into tidy Markdown. Nothing leaves your browser.")],
 ["Agent Workflows","Review & Testing","Docs, Content & SEO"],[],
 "Fill in your commands and rules, get a ready-to-commit AGENTS.md.")

# ---------- index ----------
_rows="".join(f'<a class=row href="{s}.html"><span><h3>{e(h)}</h3><p>{e(b)}</p></span></a>' for s,h,b in TOOLS)
open(D+"/tools/index.html","w").write(layout("Free tools for ChatGPT & Codex plugin builders — PickAPlugin",
 f'''<div class=prose style="max-width:900px"><span class=mono style="color:var(--acc)">Free tools · no signup</span><h1>Small tools for people building and installing plugins</h1>
<p style="font-size:19px">Things we kept needing while sorting {len(P)} plugins, so we made them pages. They're free, they run in your browser, and nothing you paste gets sent to us.</p>
<div style="border-top:3px solid var(--ink)">{_rows}</div>
<p style="margin-top:24px">Want a tool that isn't here? Email <a href="mailto:{EMAIL}">{EMAIL}</a>. Or <a href="../index.html#catalog">browse the catalog</a>.</p></div>''',1,
 "Free browser tools for ChatGPT and Codex plugin builders: plugin.json validator, MCP config converter, install command finder and AGENTS.md generator."))
print("tools:",len(TOOLS))
