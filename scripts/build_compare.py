# Executed by build.py right before build_seo.py (shares its namespace: P, D, layout, e, slug, stars, rankkey,
# PICKS, PAIRS, cslug, words, BLURB, cats, EMAIL).
# Used to write /compare/*, /alternatives/* and /best-for/* pages. Those families were
# thin and near-duplicate (2026-11-21). The worker 301s the old URLs to hubs. This file
# now enriches /p/ pages with similar-plugin lists and writes a single /compare hub.
# Do not start generating those URL batches again.
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
for s1,s2 in sorted(_VSHIT):  # sorted: set order changes per run (PYTHONHASHSEED), which made pages flip between builds
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
for sc,a,b2 in sorted(_pairs.values(),key=lambda t:(-t[0],t[1]["slug"],t[2]["slug"])):
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
# ---------- rendering (2026-11-21): no more /compare/*, /alternatives/*, /best-for/* pages.
# Those URLs 301 to hubs (see worker/index.js). Similar-plugin lists now live on /p/ pages,
# and /compare is a single how-to hub that points at category shelves.
def _stars_line(p):
  bits=[]
  if stars(p)>=0: bits.append(f"★ {stars(p):,}")
  if p.get("pushed_at"): bits.append("pushed "+p["pushed_at"][:10])
  if p.get("license"): bits.append(p["license"])
  return " · ".join(bits)
# Enrich listing pages with similar plugins (catalog facts only; no new URLs).
_enriched=0
for p in P:
  al=_alts(p, n=6)
  if len(al)<3: continue
  f=f"{D}/p/{p['slug']}.html"
  if not os.path.exists(f): continue
  items="".join(
    f'<a class=row href="{q["slug"]}.html"><h3>{e(q["name"])}</h3><p>{e(q["description"])}</p><span class="m mono">{e(_stars_line(q))} · {e(q["category"])}</span></a>'
    for q in al)
  blk=(f'<div class=sec><h2>Similar plugins</h2><span class=mono>Same kind of job, from public descriptions · not reviews</span></div>'
       f'<p style="color:var(--mute);font-size:15px;margin:8px 0 0">These are other listings in the catalog whose descriptions overlap with {e(p["name"])}. We haven\'t tested them. Open each page for the install command, license and last GitHub push, and read the repo before you install.</p>'
       f'<div class=cols style="column-count:2">{items}</div>')
  h=open(f).read()
  h2=h.replace('<div class=sec><h2>Also in',blk+'<div class=sec><h2>Also in',1)
  if h2!=h:
    open(f,"w").write(h2); _enriched+=1
# Compare hub: useful original text + links to kept category hubs. No child URL lists.
_round=f"{len(P)//50*50}+"
_shelf=" · ".join(f'<a href="c/{slug(c)}.html">{e(c)}</a> ({sum(1 for p in P if p["category"]==c)})' for c in cats)
# A few use-case shortlists, inlined on this one page (not their own URLs).
_use_html=""
if "USE_PAGES" in dir() and USE_PAGES:
  shown=0
  for t,m in USE_PAGES:
    if shown>=6: break
    top=[p for p in m if not p.get("archived")][:5]
    if len(top)<5: continue
    _use_html+=f'<h3>{e(t)}</h3><ul class=where>'+"".join(
      f'<li><a href="p/{p["slug"]}.html"><b>{e(p["name"])}</b></a> — {e(p["description"])}'
      +(f' · ★ {p["stars"]:,}' if isinstance(p.get("stars"),int) else "")+'</li>' for p in top)+'</ul>'
    shown+=1
_hb=f'''<div class=prose style="max-width:760px"><span class=mono style="color:var(--acc)">How to compare · public signals only</span>
<h1>How to compare Codex plugins &amp; MCP servers</h1>
<p style="font-size:19px">There is no single best plugin. The useful question is which one fits the job, the host you use, and how much you\'re willing to trust it with your machine.</p>
<p>PickAPlugin lists about {_round} ChatGPT and Codex plugins, plus the MCP servers a lot of them ship with. We don\'t test or audit them, and we don\'t pick a winner. What we do show, on every listing, are facts you can check yourself:</p>
<ul class=where>
<li><b>What the project says it does</b> — the description comes from the public source list or the maker, not from us.</li>
<li><b>GitHub stars and last push</b> — stars measure attention, not quality. A recent push means someone is still touching the repo; an archived repo is read-only.</li>
<li><b>License</b> — MIT and Apache-2.0 are usually straightforward to use; GPL and AGPL are copyleft, so read them before you ship the code inside closed-source work. No license file means reuse rights are unclear.</li>
<li><b>The install command</b> — copied from the project README when we can find one. Check whether it points at a local install or a hosted MCP endpoint, because a hosted endpoint sends data off your machine.</li>
</ul>
<p>A practical way to choose: open the shelf that matches the job, read the first few listings, then open two or three repos and skim the README and the last commits. If a plugin wants credentials or shell access, start it on a throwaway project. Our <a href="guides/vet-a-plugin.html">plugin safety check</a> is the short version of that, the <a href="guides/install-codex-plugin.html">plugin install guide</a> covers plugin commands, and <a href="guides/install-mcp-server-claude-cursor-codex.html">the MCP install guide</a> plus <a href="guides/check-mcp-server-safe.html">the MCP safety checklist</a> cover servers you add by hand.</p>
<p>Each listing also shows similar plugins, when we can find some, based on overlapping descriptions. That\'s a starting point, not a recommendation.</p>
<h2>Compare by shelf</h2>
<p>The category pages are the right place to browse. They\'re ranked with editor\'s picks first, then GitHub stars, and archived repos at the bottom. Paid placements are labelled and never change that order.</p>
<p>{_shelf}</p>
{("<h2>If you have a specific job</h2><p>A few starting lists, drawn from the same catalog. These are the most-starred matches for that wording, not reviews.</p>"+_use_html) if _use_html else ""}
<p style="color:var(--mute);font-size:14px">Data from GitHub and each project\'s README, checked {_ASOF}. Spot a mistake? <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>'''
open(D+"/compare.html","w").write(layout("How to compare Codex plugins & MCP servers — PickAPlugin",_hb,0,
  "How to compare ChatGPT and Codex plugins using public signals: stars, last push, license and install command, plus every category shelf."))
print("compare: similar lists on",_enriched,"listing pages; no thin compare/alternatives/best-for URLs")
