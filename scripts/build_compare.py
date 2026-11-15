# Executed by build.py right before build_seo.py (shares its namespace: P, D, layout, e, slug, stars, rankkey,
# PICKS, PAIRS, cslug, words, BLURB, cats, EMAIL).
# Writes data-driven comparison SEO pages from the catalog + cached autocomplete keywords (data/keywords.json,
# refreshed by scripts/fetch_keywords.py):
#   /compare/<a>-vs-<b>      head-to-head (same category, overlapping descriptions)
#   /alternatives/<slug>     "<plugin> alternatives" (only when 4+ real alternatives exist)
#   /best-for/<use-case>     "best MCP servers & plugins for <use case>" (only when 5+ plugins match)
#   /compare                 hub linking all of the above
# New plugins get pages automatically on the next build. Thin-page guards: thresholds below.
import json as _cj, re as _cre, datetime as _cdt, collections as _cc
_KW_PATH=os.path.join(ROOT,"data","keywords.json")
_KW=_cj.load(open(_KW_PATH)) if os.path.exists(_KW_PATH) else {"plugins":{},"use_cases":{}}
_ASOF=max((p.get("stars_checked") or "" for p in P),default="") or _cdt.date.today().isoformat()
_ASOF_D=_cdt.date.fromisoformat(_ASOF)
MAX_COMPARE=150; MAX_ALT=130; MAX_USE=40; MIN_ALTS=4; MIN_USE=5
def _days(p):
  d=p.get("pushed_at")
  try: return (_ASOF_D-_cdt.date.fromisoformat(d[:10])).days
  except Exception: return None
def _kind(p):
  i=(p.get("install") or "").lower(); d=(p["description"]+" "+p["name"]).lower()
  k=[]
  if "mcp add" in i or " mcp " in f" {d} " or "mcp server" in d: k.append("MCP server")
  if "codex plugin" in i or "/plugin" in i or "claude plugin" in i: k.append("plugin")
  if "skills add" in i or "skill" in d: k.append("skills")
  return k or ["plugin"]
def _hosts(p):
  i=(p.get("install") or "").lower(); d=(p["description"]+" "+p["name"]).lower(); h=[]
  if "codex" in i or "codex" in d: h.append("Codex")
  if "claude" in i or "/plugin" in i or "claude" in d: h.append("Claude Code")
  if "chatgpt" in d: h.append("ChatGPT")
  if "cursor" in d: h.append("Cursor")
  return h
def _remote(p):
  i=(p.get("install") or "").lower()
  return "--transport http" in i or "--transport sse" in i or _cre.search(r"https?://\S+/(mcp|sse)\b",i) is not None
_PERM={"MIT","MIT-0","Apache-2.0","BSD-3-Clause","BSD-2-Clause","ISC","CC0-1.0","Unlicense"}
def _lic(p):
  l=p.get("license") or ""
  if not l: return "No license file"
  if l=="NOASSERTION": return "Unrecognized license file"
  return l
def _act(p):
  d=_days(p)
  if d is None: return "unknown"
  if d<=7: return f"pushed {p['pushed_at'][:10]} (this week)"
  if d<=30: return f"pushed {p['pushed_at'][:10]} (last 30 days)"
  return f"pushed {p['pushed_at'][:10]} ({d} days ago)"
def _suits(p):
  out=[]; l=p.get("license") or ""; d=_days(p); h=_hosts(p)
  if h: out.append(f"You use {' or '.join(h)}: the project's own description or install command targets it.")
  if _remote(p): out.append("You're fine with a hosted MCP endpoint (requests go to the maker's server, not just your machine).")
  elif p.get("install"): out.append("You want something you install yourself; the install command doesn't point at a hosted endpoint.")
  if l in _PERM: out.append(f"You need a permissive license ({e(l)}) for work or commercial use.")
  elif l in ("AGPL-3.0","GPL-3.0","MPL-2.0"): out.append(f"You're OK with a copyleft license ({e(l)}); check it before bundling into closed-source work.")
  else: out.append("You're only trying it out: there's no recognized license file, so reuse rights are unclear.")
  if d is not None and d<=14: out.append("You want a project that's actively being worked on right now.")
  elif d is not None and d>90: out.append(f"You don't mind a quiet repo: no push in {d} days.")
  if stars(p)>=500: out.append(f"You'd rather go with a widely watched project ({stars(p):,} stars).")
  elif 0<=stars(p)<20: out.append("You're happy to be an early user of a small project.")
  if p.get("archived"): out=["Archived on GitHub: read-only, so expect no fixes."]+out
  return out
def _stars_s(p): return f"{stars(p):,}" if stars(p)>=0 else "n/a"
# ---------- similarity ----------
_LIVE=[p for p in P if not p.get("archived") and p.get("category")!="Miscellany"]
import math as _cm
_STOP=set("with your that from into codex claude code plugin plugins agent agents skills skill tools tool using which their this them they over built build builds fast free open source based works work support supports make makes help helps like also more than when what each other just only into across about such these those then there here have sets full simple small single first does lets turn turns runs running ready best easy uses used made want need while without within every allow allows give gives keep keeps provides provide includes include including server servers openai chatgpt cursor local plus collection pack native project projects".split())
def _toks(p): return [w for w in _cre.findall(r"[a-z][a-z0-9\-]{3,}",(p["name"]+" "+p["description"]).lower()) if w not in _STOP]
_DF=_cc.Counter(w for p in P for w in set(_toks(p))); _NP=len(P)
def _vec(p):
  tf=_cc.Counter(_toks(p)); v={w:(1+_cm.log(c))*_cm.log(_NP/(1+_DF[w])) for w,c in tf.items() if _DF[w]>=2}
  n=_cm.sqrt(sum(x*x for x in v.values())) or 1; return {w:x/n for w,x in v.items()}
_V={p["slug"]:_vec(p) for p in P}
_W={p["slug"]:set(_V[p["slug"]]) for p in P}
def _jac(a,b):
  A,B=_V[a["slug"]],_V[b["slug"]]; return sum(x*B[w] for w,x in A.items() if w in B)
def _sim(a,b): return _jac(a,b)+(0.05 if a["category"]==b["category"] else 0)
def _alts(p,n=8):
  c=[(round(_sim(p,q),3),q) for q in _LIVE if q["slug"]!=p["slug"]]
  c=[t for t in c if t[0]>=0.2]
  c.sort(key=lambda t:(-t[0],-stars(t[1])))
  return [q for _,q in c[:n]]
# ---------- autocomplete demand ----------
def _sugs(entry): return [s.lower() for k in ("vs","alt") for src in ("google","bing") for s in (entry.get(k,{}).get(src) or [])]
_DEMAND={}
for s,ent in _KW.get("plugins",{}).items():
  n=ent["name"]; hits=[x for x in _sugs(ent) if x.startswith(n) and len(x)>len(n)+3]
  _DEMAND[s]=hits
_NAMES={p["name"].strip("/ ").lower():p for p in P if len(p["name"].strip("/ "))>=4}
_VSHIT=set()
for s,hits in _DEMAND.items():
  for h in hits:
    for nm,q in _NAMES.items():
      if q["slug"]!=s and _cre.search(r"\b"+_cre.escape(nm)+r"\b",h[len(_KW["plugins"][s]["name"]):]): _VSHIT.add(tuple(sorted((s,q["slug"]))))
# ---------- pick alternatives pages ----------
_GSC2=["codex-rg-guard","data-product-builder-for-dbt","devin-plugin-cc","burpsuite-mcp-bridge","nightshift","muse4ai","codex-auto-resume","x-twitter-scraper"]
_cand=sorted(_LIVE,key=lambda p:(-(1 if p["slug"] in _GSC2 else 0),-(1 if _DEMAND.get(p["slug"]) else 0),-stars(p)))
ALT_PAGES=[]
for p in _cand:
  if len(ALT_PAGES)>=MAX_ALT: break
  if stars(p)<5 and p["slug"] not in _GSC2: continue
  al=_alts(p)
  if len(al)>=MIN_ALTS: ALT_PAGES.append((p,al))
ALT_SET={p["slug"] for p,_ in ALT_PAGES}
# ---------- pick comparison pairs ----------
_bys={p["slug"]:p for p in P}
_pairs={}
for a,b2 in PAIRS: _pairs[(a["slug"],b2["slug"])]=(9,a,b2)  # keep already-indexed URLs
for s1,s2 in _VSHIT:
  a,b2=_bys[s1],_bys[s2]
  if not a.get("archived") and not b2.get("archived"): _pairs.setdefault((s1,s2),(5,a,b2))
for p,al in ALT_PAGES:
  for q in al[:3]:
    if q["category"]!=p["category"] or stars(q)<0 or stars(p)<0 or _jac(p,q)<0.2: continue
    k=tuple(sorted((p["slug"],q["slug"])))
    if (k[1],k[0]) in _pairs or k in _pairs: continue
    a,b2=(p,q) if stars(p)>=stars(q) else (q,p)
    _pairs[(a["slug"],b2["slug"])]=(_sim(p,q)+min(stars(a),3000)/3000,a,b2)
_cnt=_cc.Counter(); CMP_PAIRS=[]
for sc,a,b2 in sorted(_pairs.values(),key=lambda t:-t[0]):
  if len(CMP_PAIRS)>=MAX_COMPARE: break
  if sc<9 and (_cnt[a["slug"]]>=3 or _cnt[b2["slug"]]>=3): continue
  CMP_PAIRS.append((a,b2)); _cnt[a["slug"]]+=1; _cnt[b2["slug"]]+=1
CMP_SLUGS={cslug(a,b2) for a,b2 in CMP_PAIRS}
CMP_OF=_cc.defaultdict(list)
for a,b2 in CMP_PAIRS: CMP_OF[a["slug"]].append((a,b2)); CMP_OF[b2["slug"]].append((a,b2))
# ---------- use cases from autocomplete ----------
_SEEDS=["best mcp server for","best mcp for","best codex plugin for","best claude code plugin for","best codex skills for","mcp server for","codex plugin for","claude code plugin for"]
_SKIP={"search","word","development","ai coding","coding agents","usage","images","context","claude","claude code","claude desktop","cursor","opencode","antigravity","codex","vscode","vs code","windsurf","developers","beginners","coding","copilot","github copilot","free","mac","windows","linux","reddit","2025","2026","chatgpt","gemini","gemini cli","kiro","zed","jetbrains","intellij","local llm","ollama","lm studio","agents","ai agents","n8n","trae","augment","warp","roo code","cline","kilo code","home assistant","obsidian","excel","notion","gmail","blender","godot","unity","unreal","figma","solibri","revit"}
_SYN={"web search":["web search","search api","search engine","tavily","brave search","google search","serp","crawl","scrap","perplexity","exa "],"ui design":["design","ui","frontend","figma","css"],"frontend":["frontend","ui","css","react","tailwind"],"browser automation":["browser","playwright","puppeteer","chrome"],"testing":["test","tests","testing","e2e","qa"],"code review":["review","code review","diff","lint"],"memory":["memory","remember","recall","persistent"],"documentation":["docs","documentation","readme"],"database":["database","sql","postgres","sqlite","mysql"],"security":["security","secret","vulnerab","pentest","audit"],"seo":["seo"],"devops":["deploy","devops","docker","kubernetes","ci"],"github":["github"],"git":["git ","git,","commit","branch","github"],"python":["python"],"data analysis":["data","analytics","dbt","sql","dataset"],"writing":["writing","write","copy","content"],"research":["research","paper","arxiv","scholar"],"pdf":["pdf"],"marketing":["marketing","seo","ads","social"],"slack":["slack"],"telegram":["telegram"],"image generation":["image","images"],"video":["video","youtube"],"planning":["plan","planning","spec"],"debugging":["debug","bug","error"],"refactoring":["refactor"],"api":["api "," api","openapi","rest"],"product management":["product","prd","roadmap"],"translation":["translat"],"diagrams":["diagram","mermaid"],"token usage":["token","usage","quota","cost"],"rate limits":["limit","quota","usage"],"mobile":["ios","android","mobile","swift"],"design":["design","ui","figma"],"pentesting":["pentest","burp","security"],"scraping":["scrap","crawl"],"youtube":["youtube"],"linkedin":["linkedin"],"twitter":["twitter","x.com"," x "],"email":["email","mail"],"accessibility":["accessib","a11y"],"performance":["performance","perf","speed"],"typescript":["typescript"," ts "],"rust":["rust"],"go":["golang"," go "],"java":["java "],"terraform":["terraform"],"aws":["aws"],"cloudflare":["cloudflare"],"kubernetes":["kubernetes","k8s"],"docker":["docker","container"],"jira":["jira"],"education":["education","teach","student","course"],"finance":["finance","trading","stock","accounting"],"legal":["legal","law","contract"],"writing tests":["test"],"web development":["web","frontend","react","next.js"],"context management":["context"],"multi agent":["multi-agent","multi agent","orchestrat","subagent"],"orchestration":["orchestrat","subagent","multi-agent"]}
_tails=_cc.Counter()
for q,ent in _KW.get("use_cases",{}).items():
  for src in ("google","bing"):
    for s in ent.get(src) or []:
      s=s.lower().strip()
      for seed in _SEEDS:
        if s.startswith(seed+" "):
          t=_cre.sub(r"\b(mcp|server|servers|plugin|plugins|in|with|using|reddit|202\d)\b","",s[len(seed)+1:]).strip(" -")
          t=_cre.sub(r"\s+"," ",t)
          if 2<len(t)<=28 and t not in _SKIP and not t.isdigit(): _tails[t]+=1
          break
def _match(terms,p):
  t=" "+(p["name"]+" "+p["description"]).lower()+" "
  for x in terms:
    if x!=x.strip() or not x.replace(" ","").isalpha():
      if x in t: return True
    elif _cre.search(r"\b"+_cre.escape(x)+(r"\b" if len(x)<=3 else ""),t): return True
  return False
USE_PAGES=[]; _seen=[]
for t,cnt in sorted(_tails.items(),key=lambda kv:(-kv[1],kv[0])):
  if len(USE_PAGES)>=MAX_USE: break
  terms=_SYN.get(t,[t])
  m=sorted([p for p in _LIVE if _match(terms,p)],key=rankkey)
  if len(m)<MIN_USE: continue
  ss={p["slug"] for p in m[:12]}
  if any(len(ss&o)/max(1,len(ss|o))>0.6 for o in _seen): continue
  _seen.append(ss); USE_PAGES.append((t,m))
USE_OF=_cc.defaultdict(list)
for t,m in USE_PAGES:
  for p in m[:12]: USE_OF[p["slug"]].append(t)
# ---------- rendering ----------
_TD='style="padding:9px;vertical-align:top;border-bottom:1px solid var(--rule)"'
_TH='class=mono style="text-align:left;padding:9px;vertical-align:top;border-bottom:1px solid var(--rule);width:160px"'
def _inst(p): return f'<code style="font-size:12px;word-break:break-all">{e(p["install"])}</code>' if p.get("install") else '<span style="color:var(--mute)">No copyable command in the README</span>'
def _src(p): return f'<a href="{e(p["link"])}" rel="nofollow noopener">{e(p["link"].replace("https://",""))}</a>'
def _ul(xs): return '<ul class=where>'+"".join(f"<li>{x}</li>" for x in xs)+'</ul>'
_CATLINK=lambda c,r="../":f'<a href="{r}c/{slug(c)}.html">{e(c)} plugins</a> · <a href="{r}best/{slug(c)}.html">best {e(c)} plugins, ranked</a>'
def _note(): return f'<p style="color:var(--mute);font-size:14px">Data from GitHub and each project\'s README, checked {_ASOF}. We haven\'t installed or audited these, and stars measure attention, not quality. Paid placements never change this page. Spot a mistake? <a href="mailto:{EMAIL}">{EMAIL}</a></p>'
def _verdict(a,b2):
  x=[]
  sa,sb=stars(a),stars(b2)
  if sa>=0 and sb>=0 and max(sa,sb)>0:
    hi,lo=(a,b2) if sa>=sb else (b2,a)
    x.append(f"<b>Attention:</b> {e(hi['name'])} has {_stars_s(hi)} GitHub stars to {e(lo['name'])}'s {_stars_s(lo)}"+(f" (about {stars(hi)/max(1,stars(lo)):.0f}×)." if stars(lo)>0 and stars(hi)/max(1,stars(lo))>=2 else "."))
  da,db=_days(a),_days(b2)
  if da is not None and db is not None:
    if abs(da-db)<=3: x.append(f"<b>Activity:</b> both got a push within days of each other ({a['pushed_at'][:10]} and {b2['pushed_at'][:10]}).")
    else:
      fr,st=(a,b2) if da<db else (b2,a); x.append(f"<b>Activity:</b> {e(fr['name'])} was pushed more recently ({fr['pushed_at'][:10]} vs {st['pushed_at'][:10]}).")
  la,lb=_lic(a),_lic(b2)
  x.append(f"<b>License:</b> {'both '+e(la) if la==lb else e(a['name'])+' is '+e(la)+', '+e(b2['name'])+' is '+e(lb)}."+(" Check the copyleft terms before shipping it inside closed-source work." if any(l in ("AGPL-3.0","GPL-3.0") for l in (la,lb)) else ""))
  ra,rb=_remote(a),_remote(b2)
  if ra!=rb: hs=a if ra else b2; x.append(f"<b>Where it runs:</b> {e(hs['name'])}'s install points at a hosted MCP endpoint; the other installs locally.")
  ka,kb=", ".join(_kind(a)),", ".join(_kind(b2))
  if ka!=kb: x.append(f"<b>Packaging:</b> {e(a['name'])} ships as {ka}; {e(b2['name'])} as {kb}.")
  return x
os.makedirs(D+"/compare",exist_ok=True)
for a,b2 in CMP_PAIRS:
  rows=[("What it says it does",lambda p:e(p["description"])),("Maker",lambda p:e(p["maker"] or "unknown")),("GitHub stars",lambda p:_stars_s(p)),
        ("Last push",lambda p:e(_act(p))),("License",lambda p:e(_lic(p))),("Language",lambda p:e(p.get("language") or "n/a")),
        ("Packaged as",lambda p:e(", ".join(_kind(p)))),("Works with",lambda p:e(", ".join(_hosts(p)) or "not stated")),
        ("Install",_inst),("Editor's pick",lambda p:"Yes: "+e(PICKS[p["slug"]]) if p["slug"] in PICKS else "No"),
        ("In our catalog since",lambda p:p["first_seen"]),("Source",_src),("Our page",lambda p:f'<a href="../p/{p["slug"]}.html">{e(p["name"])} →</a>')]
  tbl="".join(f'<tr><th {_TH}>{k}</th><td {_TD}>{f(a)}</td><td {_TD}>{f(b2)}</td></tr>' for k,f in rows)
  common=[w for w,_ in sorted(((w,_V[a["slug"]][w]*_V[b2["slug"]][w]) for w in _W[a["slug"]]&_W[b2["slug"]]),key=lambda t:-t[1])][:6]
  more=[]
  for s in (a["slug"],b2["slug"]):
    if s in ALT_SET: more.append(f'<a href="../alternatives/{s}.html">{e(_bys[s]["name"])} alternatives</a>')
  others=[(x,y) for x,y in CMP_OF[a["slug"]]+CMP_OF[b2["slug"]] if cslug(x,y)!=cslug(a,b2)][:6]
  more+=[f'<a href="../compare/{cslug(x,y)}.html">{e(x["name"])} vs {e(y["name"])}</a>' for x,y in others]
  body=f'''<div class=prose style="max-width:980px"><span class=mono style="color:var(--acc)">Compare · {e(a["category"])} · data checked {_ASOF}</span><h1>{e(a["name"])} vs {e(b2["name"])}</h1>
<p style="font-size:19px">Two {e(a["category"])} tools whose own descriptions overlap{(" (shared terms: "+e(", ".join(common))+")") if common else ""}. Here's what each project says it does and the public numbers, side by side, so you can pick one in a minute instead of reading two READMEs.</p>
<table style="width:100%;border-collapse:collapse;border-top:3px solid var(--ink);margin-top:20px;table-layout:fixed"><tr><th style="width:160px"></th><th style="text-align:left;padding:9px;font:600 22px Fraunces,serif">{e(a["name"])}</th><th style="text-align:left;padding:9px;font:600 22px Fraunces,serif">{e(b2["name"])}</th></tr>{tbl}</table>
<h2>The differences that matter</h2>{_ul(_verdict(a,b2))}
<h2>Who each one suits</h2><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px"><div><h3>{e(a["name"])}, if…</h3>{_ul(_suits(a))}</div><div><h3>{e(b2["name"])}, if…</h3>{_ul(_suits(b2))}</div></div>
<h3>So which one?</h3><p>We haven't run both, so we won't crown a winner. Use the list above to rule one out, then read its README and recent commits before installing. Anything that runs commands on your machine deserves a look at the code.</p>
{f"<h3>Related</h3><p>{' · '.join(more)}</p>" if more else ""}<p>More: {_CATLINK(a["category"])} · <a href="../compare.html">all comparisons</a></p>{_note()}</div>'''
  open(f"{D}/compare/{cslug(a,b2)}.html","w").write(layout(f"{a['name']} vs {b2['name']} ({_ASOF[:4]}): {a['category']} compared — PickAPlugin",body,1,
    f"{a['name']} vs {b2['name']}: features, license, GitHub stars, last push and install command side by side, plus who each one suits."))
os.makedirs(D+"/alternatives",exist_ok=True)
for p,al in ALT_PAGES:
  rows="".join(f'<tr><td {_TD}><a href="../p/{q["slug"]}.html"><b>{e(q["name"])}</b></a><br><span style="font-size:14px">{e(q["description"])}</span></td><td {_TD} class=mono>★ {_stars_s(q)}</td><td {_TD} class=mono>{e(_lic(q))}</td><td {_TD} class=mono>{e((q.get("pushed_at") or "n/a")[:10])}</td><td {_TD} class=mono>{e(", ".join(_kind(q)))}</td></tr>' for q in al)
  cmpl=[f'<a href="../compare/{cslug(x,y)}.html">{e(x["name"])} vs {e(y["name"])}</a>' for x,y in CMP_OF[p["slug"]]]
  why=[]
  perm=[q for q in al if (q.get("license") or "") in _PERM]
  fresh=sorted([q for q in al if (_days(q) or 999)<=14],key=lambda q:_days(q))
  if p.get("license") not in _PERM and perm: why.append(f"Need a permissive license? {', '.join(e(q['name']) for q in perm[:3])} {'is' if len(perm[:3])==1 else 'are'} {e(perm[0]['license'])}{' or similar' if len(perm)>1 else ''}, while {e(p['name'])} is {e(_lic(p))}.")
  if fresh: why.append(f"Want active development? {', '.join(e(q['name']) for q in fresh[:3])} got a push in the last two weeks.")
  big=max(al,key=stars)
  if stars(big)>stars(p): why.append(f"Want the most-watched option? {e(big['name'])} has {_stars_s(big)} stars to {e(p['name'])}'s {_stars_s(p)}.")
  loc=[q for q in al if not _remote(q) and q.get("install")]
  if _remote(p) and loc: why.append(f"Prefer local over hosted? {e(p['name'])} installs as a hosted endpoint; {', '.join(e(q['name']) for q in loc[:3])} install locally.")
  nohost=[q for q in al if set(_hosts(q))-set(_hosts(p))]
  if nohost: q=nohost[0]; why.append(f"On a different tool? {e(q['name'])} mentions {e(', '.join(sorted(set(_hosts(q))-set(_hosts(p)))))}.")
  body=f'''<div class=prose style="max-width:980px"><span class=mono style="color:var(--acc)">Alternatives · {e(p["category"])} · data checked {_ASOF}</span><h1>{e(p["name"])} alternatives</h1>
<p style="font-size:19px">{e(p["name"])} by {e(p["maker"] or "unknown")}: {e(p["description"])} Here are {len(al)} plugins in our catalog that describe a similar job, with the numbers you'd check before switching.</p>
<div style="border:1px solid var(--ink);background:#fffdf8;padding:12px 16px;margin:16px 0"><b>{e(p["name"])} at a glance:</b> ★ {_stars_s(p)} · {e(_lic(p))} · {e(_act(p))} · {e(", ".join(_kind(p)))}{(" · works with "+e(", ".join(_hosts(p)))) if _hosts(p) else ""} · <a href="../p/{p["slug"]}.html">full listing →</a></div>
{f"<h2>Why you might look elsewhere</h2>{_ul(why)}" if why else ""}
<h2>{len(al)} alternatives, side by side</h2><div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;border-top:3px solid var(--ink)"><tr><th {_TH} style="text-align:left">Plugin</th><th {_TH}>Stars</th><th {_TH}>License</th><th {_TH}>Last push</th><th {_TH}>Packaged as</th></tr>{rows}</table></div>
<p style="font-size:14px;color:var(--mute)">Picked by overlap between each project's own description and {e(p["name"])}'s, same category first. Ordered by that overlap, not by stars or payment.</p>
{f"<h3>Head-to-head</h3><p>{' · '.join(cmpl)}</p>" if cmpl else ""}<p>More: {_CATLINK(p["category"])} · <a href="../compare.html">all comparisons</a></p>{_note()}</div>'''
  open(f"{D}/alternatives/{p['slug']}.html","w").write(layout(f"{len(al)} {p['name']} alternatives ({_ASOF[:4]}): similar {p['category']} plugins — PickAPlugin",body,1,
    f"{len(al)} alternatives to {p['name']} for Codex, Claude Code and ChatGPT, compared by GitHub stars, license, last push and packaging."))
os.makedirs(D+"/best-for",exist_ok=True)
def _uslug(t): return slug(t)
for t,m in USE_PAGES:
  top=m[:12]; T=t.title() if t.islower() and len(t)>3 else t
  cats_=_cc.Counter(p["category"] for p in m).most_common(3)
  perm=sum(1 for p in top if (p.get("license") or "") in _PERM); fresh=sum(1 for p in top if (_days(p) or 999)<=30)
  rem=sum(1 for p in top if _remote(p))
  rows="".join(f'<div style="border-top:1px solid var(--rule);padding:14px 0"><h3 style="margin:0">{i+1}. <a href="../p/{p["slug"]}.html">{e(p["name"])}</a>{" <span class=mono style=\'font-size:12px;color:var(--acc)\'>Editor\'s pick</span>" if p["slug"] in PICKS else ""}</h3><p style="margin:6px 0">{e(p["description"])}</p><p class=mono style="font-size:12px;color:var(--mute);margin:0">★ {_stars_s(p)} · {e(_lic(p))} · {e(_act(p))} · {e(", ".join(_kind(p)))} · by {e(p["maker"] or "unknown")}{" · <a href=\'../alternatives/"+p["slug"]+".html\'>alternatives</a>" if p["slug"] in ALT_SET else ""}</p>{("<p style=\'margin:6px 0 0\'>"+_inst(p)+"</p>") if p.get("install") else ""}</div>' for i,p in enumerate(top))
  cm=[(x,y) for x,y in CMP_PAIRS if x in top and y in top][:6]
  body=f'''<div class=prose style="max-width:900px"><span class=mono style="color:var(--acc)">Best for · {e(t)} · data checked {_ASOF}</span><h1>Best MCP servers &amp; Codex plugins for {e(t)}</h1>
<p style="font-size:19px">{len(m)} plugins in our catalog say they help with {e(t)}. Here are the top {len(top)}, editor's picks first, then by GitHub stars. Most of them sit in {" and ".join(f'<a href="../c/{slug(c)}.html">{e(c)}</a>' for c,_ in cats_[:2])}.</p>
<div style="border:1px solid var(--ink);background:#fffdf8;padding:12px 16px;margin:16px 0"><b>Quick read on these {len(top)}:</b> {perm} have a permissive license, {fresh} got a push in the last 30 days, {rem} install as a hosted MCP endpoint.</div>
<h2>How to choose</h2>{_ul(["Match the host first: Codex and Claude Code install commands differ, and the install line below shows which one each project targets.","Check where it runs. Hosted MCP endpoints are quicker to set up but send your requests to someone else's server.","Prefer a recent push and a real license (MIT or Apache-2.0) for anything you'll use at work.","Stars tell you how many people looked, not whether it works. Read the code before you install."])}
<h2>The list</h2>{rows}
{("<h3>Head-to-head</h3><p>"+" · ".join(f'<a href="../compare/{cslug(x,y)}.html">{e(x["name"])} vs {e(y["name"])}</a>' for x,y in cm)+"</p>") if cm else ""}
<p style="font-size:14px;color:var(--mute)">Matched by keywords in each project's own name and description. The topic comes from what people actually type into Google and Bing search boxes.</p><p><a href="../compare.html">All comparisons and use cases →</a></p>{_note()}</div>'''
  open(f"{D}/best-for/{_uslug(t)}.html","w").write(layout(f"Best MCP servers & Codex plugins for {t} ({_ASOF[:4]}) — PickAPlugin",body,1,
    f"The best MCP servers and Codex/Claude Code plugins for {t}: {len(m)} matches, top {len(top)} compared by stars, license, last push and install command."))
# hub
_hb=f'''<div class=prose style="max-width:980px"><span class=mono style="color:var(--acc)">Compare · {len(CMP_PAIRS)} head-to-heads · {len(ALT_PAGES)} alternatives lists · {len(USE_PAGES)} use cases</span><h1>Compare Codex plugins &amp; MCP servers</h1>
<p style="font-size:19px">Side-by-side pages built from public data: GitHub stars, last push, license, packaging and install command. Updated every time the catalog refreshes.</p>
<h2>Best for…</h2><p>{" · ".join(f'<a href="best-for/{_uslug(t)}.html">{e(t)}</a>' for t,_ in sorted(USE_PAGES))}</p>
<h2>Alternatives</h2><p>{" · ".join(f'<a href="alternatives/{p["slug"]}.html">{e(p["name"])}</a>' for p,_ in sorted(ALT_PAGES,key=lambda t:t[0]["name"].lower()))}</p>
<h2>Head-to-head</h2>'''
for c in cats:
  xs=[(a,b2) for a,b2 in CMP_PAIRS if a["category"]==c]
  if xs: _hb+=f'<h3>{e(c)}</h3><p>{" · ".join(f"<a href=\"compare/{cslug(a,b2)}.html\">{e(a['name'])} vs {e(b2['name'])}</a>" for a,b2 in xs)}</p>'
_hb+=f'<p>Ranked lists: {" · ".join(f"<a href=\"best/{slug(c)}.html\">{e(c)}</a>" for c in cats)}</p></div>'
open(D+"/compare.html","w").write(layout("Compare Codex plugins & MCP servers: alternatives and head-to-heads — PickAPlugin",_hb,0,
  f"{len(CMP_PAIRS)} side-by-side comparisons, {len(ALT_PAGES)} alternatives lists and {len(USE_PAGES)} best-for pages for Codex plugins, Claude Code plugins and MCP servers."))
# internal links from each plugin page and category page
for s in set(ALT_SET)|set(CMP_OF)|set(USE_OF):
  f=f"{D}/p/{s}.html"
  if not os.path.exists(f): continue
  ln=[]
  if s in ALT_SET: ln.append(f'<a href="../alternatives/{s}.html">{e(_bys[s]["name"])} alternatives</a>')
  ln+=[f'<a href="../compare/{cslug(x,y)}.html">{e(x["name"])} vs {e(y["name"])}</a>' for x,y in CMP_OF.get(s,[])[:4]]
  ln+=[f'<a href="../best-for/{_uslug(t)}.html">best for {e(t)}</a>' for t in USE_OF.get(s,[])[:3]]
  h=open(f).read(); blk=f'<p class=shelves><span class=mono>Compare:</span> {" · ".join(ln)}</p>'
  h2=h.replace('<div class=sec><h2>Also in',blk+'<div class=sec><h2>Also in',1)
  if h2!=h: open(f,"w").write(h2)
for c in cats:
  f=f"{D}/c/{slug(c)}.html"
  if not os.path.exists(f): continue
  xs=[(a,b2) for a,b2 in CMP_PAIRS if a["category"]==c]
  al=[p for p,_ in ALT_PAGES if p["category"]==c][:8]
  if not xs and not al: continue
  blk=f'<p class=shelves><span class=mono>Compare:</span>'+"".join(f' <a href="../alternatives/{p["slug"]}.html">{e(p["name"])} alternatives</a>' for p in al)+f' <a href="../compare.html">all comparisons →</a></p>'
  h=open(f).read(); i=h.find('<p class=shelves><span class=mono>Ranked:')
  if i>=0:
    j=h.index('</p>',i)+4; h=h[:j]+blk+h[j:]; open(f,"w").write(h)
print("compare:",len(CMP_PAIRS),"head-to-heads,",len(ALT_PAGES),"alternatives,",len(USE_PAGES),"best-for pages")
