#!/usr/bin/env python3
"""Static site generator: data/plugins.json -> dist/ (Cloudflare Pages output dir)."""
import json, os, html, shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,"dist")
P=json.load(open(os.path.join(ROOT,"data","plugins.json")))
for p in P:
  if p["category"]=="Other": p["category"]="Miscellany"
# TODO(Aaron): paste real Stripe Payment Links here once created in Stripe. Leave "" until then.
# Live Stripe Payment Links (acct_1UUidjAJ19i9R4dz). Sandbox (test-mode) links, for local preview only:
#   featured_monthly: https://buy.stripe.com/test_14AaEZ8TC3vJelQ2ai73G00
#   expedited_review: https://buy.stripe.com/test_bJe5kF4Dmd6j4Lg9CK73G01
# Preview with: STRIPE_PREVIEW=test python3 scripts/build.py   (never deploy that build)
import os as _os
STRIPE={"featured_monthly":"https://buy.stripe.com/aFa14m2Ih7DV2ep15bcQU00","expedited_review":"https://buy.stripe.com/eVqbJ02Ih6zRg5fg05cQU01",
 "top_spot":"https://buy.stripe.com/14A28q82Bgarg5f3djcQU02","belt":"https://buy.stripe.com/00w7sKfv3cYf4mx7tzcQU03",
 "category_sponsor":"https://buy.stripe.com/14A3cu3Mlf6ng5f5lrcQU05","verified":"https://buy.stripe.com/4gMcN45Ute2j1albJPcQU04"}
if _os.environ.get("STRIPE_PREVIEW")=="test":
    STRIPE.update({"featured_monthly":"https://buy.stripe.com/test_14AaEZ8TC3vJelQ2ai73G00","expedited_review":"https://buy.stripe.com/test_bJe5kF4Dmd6j4Lg9CK73G01"})
EMAIL="hello@pickaplugin.com"; e=html.escape
# Editor's picks. Notes paraphrase each project's own README description; not independently audited.
PICKS={"agent-guard":"Hooks that catch secrets before they leak out of an agent session. Local by default, no telemetry. The first thing we'd install.",
 "deja":"Full-text search over the coding sessions already on your disk, across two dozen tools. No model in the loop — just an index.",
 "brooks-lint":"Code review that cites its sources: six classic engineering books, severity labels, and a tech-debt mode.",
 "codex-mem":"Captures and compresses session context so tomorrow's Codex remembers what today's Codex learned.",
 "babeldoc-pdf-translate":"Translates PDFs while keeping the typesetting intact. Bilingual output, your own glossary.",
 "agent-retro":"A weekly slideshow of how you actually use your agents, built locally from your own logs."}
BLURB={"Agent Workflows":"Orchestrators, specialist crews and spec-first pipelines.","Memory & Context":"Things that help an agent remember.",
 "Review & Testing":"Second opinions, test harnesses, gates.","Security & Governance":"Guards, audits and policy.","Usage & Quotas":"Know where your tokens went.",
 "Docs, Content & SEO":"PDFs, transcripts, notes and words.","Design & Frontend":"Pixels, CSS and terminal UIs.","Messaging & Remote":"Reach your agent from your phone.",
 "Deploy & DevOps":"Ship it somewhere.","Data & Backend":"Databases, analytics, telemetry.","Industry Tools":"Niche, specific, often surprising.","Miscellany":"Hard to file, worth a look."}
CSS="""@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root{--ink:#16130f;--paper:#f3efe6;--rule:#cfc6b4;--mute:#6b6457;--acc:#c8381e}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 'IBM Plex Sans',sans-serif}
a{color:inherit}.w{max-width:1160px;margin:auto;padding:0 28px}.mono{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.mast{border-bottom:3px double var(--ink)}.top{display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--ink)}
.brand{display:flex;align-items:baseline;justify-content:space-between;padding:18px 0 14px}.brand a.n{font:800 54px/1 Fraunces,serif;letter-spacing:-.02em;text-decoration:none}
.brand a.n i{color:var(--acc);font-style:normal}nav a{margin-left:22px;text-decoration:none}nav a:hover,.row a:hover h3{color:var(--acc)}
.lede{display:grid;grid-template-columns:1.3fr 1fr;gap:48px;padding:44px 0 36px;border-bottom:1px solid var(--ink)}
.lede h1{font:600 46px/1.08 Fraunces,serif;margin:0;letter-spacing:-.015em}.lede h1 em{color:var(--acc)}.lede p{color:var(--mute);margin:16px 0 0;max-width:46ch}
#q{width:100%;border:0;border-bottom:2px solid var(--ink);background:transparent;font:400 22px Fraunces,serif;padding:10px 0;outline:none}#q::placeholder{color:#a39a88}
.cats{margin-top:18px;display:flex;flex-wrap:wrap;gap:6px 14px}.cats button{all:unset;cursor:pointer;font-size:14px;border-bottom:1px solid transparent}.cats button.on{border-color:var(--acc);color:var(--acc)}.cats sup{color:var(--mute);font-size:10px}
.sec{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--ink);padding:36px 0 8px}.sec h2{font:600 28px Fraunces,serif;margin:0}
.picks{display:grid;grid-template-columns:repeat(3,1fr);border-left:1px solid var(--rule)}.pick{padding:22px 22px 26px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);text-decoration:none}
.pick .no{color:var(--acc)}.pick h3{font:600 22px/1.2 Fraunces,serif;margin:8px 0}.pick p{margin:0;font-size:15px}.pick .by{color:var(--mute);margin-top:12px}
.slots{display:grid;grid-template-columns:repeat(3,1fr);gap:0;border:1px solid var(--ink);margin-top:18px}.slot{padding:18px 20px;border-right:1px solid var(--ink);text-decoration:none}.slot:last-child{border:0}.slot b{font-family:Fraunces,serif;font-size:18px;display:block}.slot span{color:var(--mute);font-size:14px}
.row{display:grid;grid-template-columns:70px 1fr 190px;gap:20px;padding:14px 0;border-bottom:1px solid var(--rule);text-decoration:none;align-items:baseline}
.row h3{font:600 19px Fraunces,serif;margin:0 0 2px}.row p{margin:0;color:#3d382f;font-size:14.5px}.side+x{}.doc .row p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.row .c{text-align:right;color:var(--mute)}.row .no{color:var(--mute)}
.doc{display:grid;grid-template-columns:1fr 300px;gap:56px;padding:40px 0 60px}.doc h1{font:800 56px/1.02 Fraunces,serif;margin:10px 0 18px;letter-spacing:-.02em}.doc .d{font:400 22px/1.45 Fraunces,serif}
.side{border-top:3px solid var(--ink);padding-top:14px}.side dl{margin:0}.side dt{margin-top:14px;color:var(--mute)}.side dd{margin:2px 0 0}
.btn{display:inline-block;background:var(--ink);color:var(--paper);padding:12px 20px;text-decoration:none;font-weight:600;margin-top:22px}.btn:hover{background:var(--acc)}
.note{border-left:3px solid var(--acc);padding:4px 0 4px 16px;margin:26px 0;font-style:italic}
.todo{border:1px dashed var(--acc);color:var(--acc);padding:12px 14px;font-size:14px;margin-top:18px}.prose{max-width:680px;padding:40px 0 70px}.prose h1{font:800 48px/1.05 Fraunces,serif;margin:0 0 20px}.prose h3{font:600 22px Fraunces,serif;margin:34px 0 6px}.price{font:600 40px Fraunces,serif}
footer{border-top:3px double var(--ink);padding:22px 0 40px;color:var(--mute);font-size:13px;display:flex;justify-content:space-between;gap:30px}
.fband{background:var(--ink);color:var(--paper);margin:26px 0 0;padding:26px 26px 28px}.fband .hd{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #4a443a;padding-bottom:12px}
.fband .hd h2{font:600 26px Fraunces,serif;margin:0}.fband .hd a{color:#e9b8ab}.fgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:18px}
.fcard{display:flex;flex-direction:column;background:#211d17;border:1px solid #4a443a;padding:22px;text-decoration:none;color:var(--paper);min-height:230px;transition:border-color .15s}.fcard:hover{border-color:var(--acc)}
.badge{display:inline-block;background:var(--acc);color:#fff;font:500 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;padding:3px 8px;align-self:flex-start}
.fcard h3{font:800 30px/1.08 Fraunces,serif;margin:14px 0 8px;letter-spacing:-.01em}.fcard p{margin:0;color:#d8d0c0;font-size:15px}.fcard .by{margin-top:auto;padding-top:16px;color:#a39a88}
.fcard.open{border-style:dashed;background:transparent}.fcard.open h3{color:#fff}.fcard .cta{margin-top:auto;padding-top:16px;color:#fff;font-weight:600}.fcard .cta b{color:#e9b8ab}
.fpin{border:2px solid var(--ink);margin:14px 0 4px}.fpin .row{border-bottom:0;padding:16px 14px;background:#fbf8f1}.fpin .row+.row{border-top:1px solid var(--rule)}
.fopen{display:flex;justify-content:space-between;gap:16px;align-items:center;border:1px dashed var(--acc);padding:12px 14px;margin:14px 0 4px;font-size:14px;text-decoration:none}.fopen b{color:var(--acc)}
.mine{font-size:13px;color:var(--mute);margin:14px 0 0}.mine a{color:var(--acc)}.shelves{display:flex;flex-wrap:wrap;gap:8px 18px;padding:14px 0 4px;font-size:14px}
.faq h3{margin-top:26px}.where li{margin:6px 0}.slotstat{display:flex;gap:10px;margin:18px 0}.slotstat span{flex:1;border:1px solid var(--ink);padding:12px;text-align:center}.slotstat .taken{background:var(--ink);color:var(--paper)}
@media(max-width:800px){.fgrid{grid-template-columns:1fr}.lede,.doc{grid-template-columns:1fr}.picks,.slots{grid-template-columns:1fr}.row{grid-template-columns:44px 1fr}.side+x{}.doc .row p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.row .c{display:none}.brand a.n{font-size:38px}}
.belt{border-bottom:1px solid var(--ink);background:#ebe5d8;overflow:hidden}.bhd{display:flex;justify-content:space-between;max-width:1160px;margin:auto;padding:7px 28px 0;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}.bhd a{color:var(--acc);text-decoration:none}
.btrack{display:flex;width:max-content;padding:8px 0 12px;animation:belt 70s linear infinite}.belt:hover .btrack,.btrack:focus-within{animation-play-state:paused}
.brow{display:flex;gap:12px;padding-right:12px}@keyframes belt{to{transform:translateX(-50%)}}
.bc{flex:0 0 230px;display:flex;flex-direction:column;gap:2px;padding:10px 14px;border:1px solid var(--ink);background:var(--paper);text-decoration:none;transition:transform .2s,border-color .2s}.bc:hover{transform:translateY(-2px);border-color:var(--acc)}
.bc b{font:600 17px/1.15 Fraunces,serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.bc .bd{font-size:12.5px;color:var(--mute);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bc .bl{font:500 10px 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;align-self:flex-start;padding:1px 6px}
.bc.paid .bl{background:var(--acc);color:#fff}.bc.pk .bl{border:1px solid var(--ink)}.bc.open{border-style:dashed;border-color:var(--acc);background:transparent}.bc.open .bl,.bc.open b{color:var(--acc)}
@media(prefers-reduced-motion:reduce){.btrack{animation:none;overflow-x:auto;width:auto}.brow[aria-hidden]{display:none}}
.hero{display:block;margin-top:26px;padding:34px 34px 30px;border:3px solid var(--ink);background:#fbf8f1;text-decoration:none;position:relative}.hero h2{font:800 52px/1.02 Fraunces,serif;margin:14px 0 10px;letter-spacing:-.02em}.hero h2 a{text-decoration:none}.hero p{font:400 20px/1.45 Fraunces,serif;max-width:62ch;margin:0}.hero .by{display:block;margin-top:14px;color:var(--mute)}
.hbtn{display:inline-block;margin-top:18px;background:var(--ink);color:var(--paper);padding:11px 18px;font-weight:600;text-decoration:none}.hero:hover .hbtn{background:var(--acc)}.hero.open{border-style:dashed;border-color:var(--acc);background:transparent}.hero.open h2{color:var(--ink)}
.spons{display:grid;grid-template-columns:200px 1fr;gap:4px 20px;align-items:baseline;border:2px solid var(--ink);background:#fbf8f1;padding:14px 16px;margin:14px 0 0;text-decoration:none}.spons b{font:600 20px Fraunces,serif}.spons span:last-child{grid-column:2;color:var(--mute);font-size:14px}.spons.open{border:1px dashed var(--acc);background:transparent}.spons.open b{color:var(--acc)}
.vchk{font:500 11px 'IBM Plex Mono',monospace;letter-spacing:.06em;color:#1d6b3a;border:1px solid #1d6b3a;padding:1px 6px;margin-left:8px;vertical-align:middle;white-space:nowrap}.vbig{color:#1d6b3a;font-weight:600;margin:0 0 12px}.vbig .mono{color:var(--mute);font-weight:400;font-size:11px}
.ladder{border-top:3px solid var(--ink);margin-top:26px}.tier{display:grid;grid-template-columns:1fr 150px 230px;gap:24px;padding:22px 0;border-bottom:1px solid var(--rule);align-items:start}.tier h3{margin:0 0 4px !important}.tier .pr{font:600 30px Fraunces,serif}.tier .pr small{display:block;font:400 12px 'IBM Plex Mono',monospace;color:var(--mute);text-transform:uppercase;letter-spacing:.06em}.tier .st{font-size:14px;color:var(--mute)}.tier .btn{margin-top:6px}.tier.soon{opacity:.7}
@media(max-width:800px){.tier{grid-template-columns:1fr}.hero h2{font-size:36px}.spons{grid-template-columns:1fr}.spons span:last-child{grid-column:1}}"""
def layout(title,body,depth=0,desc="An independent, hand-edited catalog of ChatGPT and Codex plugins."):
  r="../"*depth
  return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<meta name=description content="{e(desc)}"><link rel=stylesheet href="{r}style.css"></head><body><div class=w>
<header class=mast><div class="top mono"><span>Independent · not affiliated with OpenAI</span><span>{len(P)} plugins catalogued</span></div>
<div class=brand><a class=n href="{r}index.html">PickA<i>Plugin</i></a><nav><a href="{r}index.html#catalog">Catalog</a><a href="{r}submit.html">Submit</a><a href="{r}featured.html" style="color:var(--acc);font-weight:600">Get featured</a><a href="{r}advertise.html">Advertise</a><a href="{r}about.html">About</a></nav></div></header></div>
{belt(r)}<div class=w>
{body}<footer><span>PickAPlugin is an independent catalog. Not affiliated with, endorsed by, or sponsored by OpenAI. ChatGPT and Codex are trademarks of OpenAI. Listings come from public sources — read the code before you install anything.</span><span><a href="{r}advertise.html">Advertise</a> · <a href="{r}privacy.html">Privacy</a> · <a href="{r}terms.html">Terms</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span></footer></div></body></html>"""
idx={p["slug"]:i+1 for i,p in enumerate(P)}
def num(p): return f"No.{idx[p['slug']]:03d}"
def row(p,pre="p/"): return f'<a class=row href="{pre}{p["slug"]}.html" data-c="{e(p["category"])}" data-t="{e((p["name"]+" "+p["description"]+" "+p["maker"]).lower())}"><span class="no mono">{num(p)}</span><span><h3>{e(p["name"])}{vmark(p)}</h3><p>{e(p["description"])}</p></span><span class="c mono">{e(p["category"])}</span></a>'
def slug(c): return "".join(ch if ch.isalnum() else "-" for ch in c.lower()).replace("--","-").replace("--","-").strip("-")
def pinrow(p,pre): return f'<a class=row style="grid-template-columns:110px 1fr" href="{pre}{p["slug"]}.html"><span class=badge>Featured</span><span><h3>{e(p["name"])}</h3><p>{e(p["description"])}</p></span></a>'
def pinned(cat,pre,r):
  fs=[p for p in FEAT if p["category"]==cat]
  if fs: return '<div class=fpin>'+"".join(pinrow(p,pre) for p in fs)+'</div>'
  if OPEN: return f'<a class=fopen href="{r}featured.html"><span><b>Featured spot open in {e(cat)}.</b> Pin your plugin here, above every list in this category.</span><span class=mono>$49/mo →</span></a>'
  return ""
def pay(key,label,price):
  if STRIPE[key]: return f'<a class=btn href="{STRIPE[key]}">{label} — {price}</a>'
  return f'<div class=todo>TODO: Stripe Payment Link for “{label}” ({price}) isn\'t connected yet, so payments aren\'t live. Until then, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</div>'
shutil.rmtree(D,ignore_errors=True); os.makedirs(D+"/p"); open(D+"/style.css","w").write(CSS)
FEAT=[p for p in P if p.get("featured")][:3]; OPEN=3-len(FEAT)
by={p["slug"]:p for p in P}; cats=sorted({p["category"] for p in P},key=lambda c:(c=="Miscellany",c))
count={c:sum(p["category"]==c for p in P) for c in cats}
# ---- paid placements beyond Featured (see scripts/fulfill.py) ----
TOP=[p for p in P if p.get("top_spot")][:1]
BELT=[p for p in P if p.get("belt")][:12]; BELT_OPEN=12-len(BELT)
SPONS={}
for p in P:
  if p.get("sponsor_category") and p["sponsor_category"] not in SPONS: SPONS[p["sponsor_category"]]=p
def vmark(p): return ' <span class=vchk title="Verified by maker (paid badge)">✓ Verified by maker</span>' if p.get("verified") else ""
PK=[x for x in PICKS if x in by]
def belt(r):
  paid=[f'<a class="bc paid" href="{r}p/{p["slug"]}.html"><span class=bl>On the Belt</span><b>{e(p["name"])}</b><span class=bd>{e(p["description"][:70])}</span></a>' for p in BELT]
  ps={p["slug"] for p in BELT}
  picks=[f'<a class="bc pk" href="{r}p/{s}.html"><span class=bl>Editor\'s pick, unpaid</span><b>{e(by[s]["name"])}</b><span class=bd>{e(by[s]["category"])}</span></a>' for s in PK if s not in ps][:max(0,BELT_OPEN-1) if BELT_OPEN else 0]
  opens=[f'<a class="bc open" href="{r}advertise.html#belt"><span class=bl>Open slot</span><b>Your plugin here</b><span class=bd>$19/mo · labelled “On the Belt”</span></a>'] if BELT_OPEN else []
  t="".join(paid+picks+opens)
  return f'<div class=belt aria-label="On the Belt: paid placements (labelled) and unpaid editor\'s picks"><div class=bhd mono><span>On the Belt</span><a href="{r}advertise.html#belt">Put your plugin on the belt · $19/mo</a></div><div class=btrack><div class=brow>{t}</div><div class=brow aria-hidden=true>{t}</div></div></div>'
def topspot():
  if TOP:
    p=TOP[0]; w=p.get("top_spot_note") or p["description"]
    return f'<section class=hero><span class=badge>The Top Spot · Paid placement</span><h2><a href="p/{p["slug"]}.html">{e(p["name"])}</a></h2><p>{e(w)}</p><span class="mono by">by {e(p["maker"])} · {e(p["category"])}</span><a class=hbtn href="p/{p["slug"]}.html">See the plugin →</a></section>'
  p=by[PK[0]]
  return f'<section class=hero><span class=badge>Editor\'s pick · unpaid</span><h2><a href="p/{p["slug"]}.html">{e(p["name"])}</a></h2><p>{e(PICKS[p["slug"]])}</p><span class="mono by">by {e(p["maker"])} · {e(p["category"])}</span><a class=hbtn href="p/{p["slug"]}.html">See the plugin →</a><a href="advertise.html#top" style="display:block;margin-top:10px;font-size:12px;opacity:.7;color:inherit">This spot is available →</a></section>'
def sponsor(c):
  p=SPONS.get(c)
  if p: return f'<a class=spons href="../p/{p["slug"]}.html"><span class=mono>Presented by · sponsor</span><b>{e(p["name"])}</b><span>{e(p["description"][:120])}</span></a>'
  return f'<a class="spons open" href="../advertise.html#sponsor"><span class=mono>Presented by · open</span><b>Sponsor the {e(c)} shelf</b><span>One sponsor per category, labelled. $29/mo →</span></a>'
picks="".join(f'<a class=pick href="p/{s}.html"><span class="no mono">Pick {i+1:02d} · {e(by[s]["category"])}</span><h3>{e(by[s]["name"])}</h3><p>{e(n)}</p><div class="by mono">by {e(by[s]["maker"])}</div></a>' for i,(s,n) in enumerate(PICKS.items()) if s in by)
feat=FEAT
slots="".join(f'<a class=slot href="p/{p["slug"]}.html"><span class=mono>Featured</span><b>{e(p["name"])}</b><span>{e(p["description"][:90])}</span></a>' for p in feat)+(f'<a class=slot href="featured.html" style="grid-column:span {3-len(feat)}"><span class=mono>Sponsored · {3-len(feat)} of 3 slots open</span><b>Built a plugin? Put it here for $49 a month.</b><span>Clearly labelled, never touches our picks or the catalog order. Cancel anytime.</span></a>' if len(feat)<3 else "")
def fband(r):
  cards="".join(f'<a class=fcard href="{r}p/{p["slug"]}.html"><span class=badge>Featured</span><h3>{e(p["name"])}</h3><p>{e(p["description"][:150])}</p><span class="by mono">by {e(p["maker"])} · {e(p["category"])}</span></a>' for p in FEAT)
  fs={p["slug"] for p in FEAT}; top=None if TOP else PK[0]
  fill=[s for s in PK if s not in fs and s!=top][:max(0,OPEN-1)]
  cards+="".join(f'<a class=fcard href="{r}p/{s}.html"><span class=badge>Editor\'s pick · unpaid</span><h3>{e(by[s]["name"])}</h3><p>{e(PICKS[s][:150])}</p><span class="by mono">by {e(by[s]["maker"])} · {e(by[s]["category"])}</span></a>' for s in fill)
  if OPEN: cards+=f'<a class="fcard open" href="{r}featured.html"><span class="mono" style="color:#e9b8ab">Featured slot · open</span><h3>Feature your<br>plugin here.</h3><p>The first thing every visitor sees, plus the top of your category page and every related list.</p><span class=cta>Claim this slot · <b>$49/mo</b> →</span></a>'
  return f'<section class=fband><div class=hd><h2>Featured</h2><span class=mono>Paid placements labelled “Featured” · picks are unpaid · <a href="{r}featured.html">how it works</a></span></div><div class=fgrid>{cards}</div></section>'
dates=sorted({p["first_seen"] for p in P}); new=[p for p in P if len(dates)>1 and p["first_seen"]>dates[0]][-10:]
newsec=f'<div class=sec><h2>Fresh in the catalog</h2><span class=mono>added since {dates[0]}</span></div>'+"".join(row(p) for p in new) if new else ""
chips='<button class=on data-c="">Everything</button>'+"".join(f'<button data-c="{e(c)}">{e(c)}<sup>{count[c]}</sup></button>' for c in cats)
shelves='<div class=shelves><span class=mono>Shelves:</span>'+"".join(f'<a href="c/{slug(c)}.html">{e(c)}</a>' for c in cats)+'</div>'
home=topspot()+fband("")+f"""<section class=lede><div><span class="mono" style="color:var(--acc)">The catalog · Issue 01</span><h1>Plugins for ChatGPT &amp; Codex, <em>sorted by a person</em>, not a leaderboard.</h1>
<p>We read the lists so you don't have to. Every plugin here links back to its source. A few we'd actually install are marked as picks.</p></div>
<div><label class=mono for=q>Search {len(P)} plugins</label><input id=q placeholder="memory, PDF, secret scanning…"><div class=cats>{chips}</div></div></section>
<div class=sec><h2>Editor's picks</h2><span class=mono>Chosen from each project's own description · not audited</span></div><div class=picks>{picks}</div>
{newsec}
<div class=sec id=catalog><h2>The full catalog</h2><span class=mono id=n></span></div>{shelves}<div id=list>{"".join(row(p) for p in P)}</div>
<script>let c="",q=document.getElementById('q'),rs=[...document.querySelectorAll('#list .row')];function f(){{let t=q.value.toLowerCase(),n=0;rs.forEach(x=>{{let ok=(!c||x.dataset.c==c)&&x.dataset.t.includes(t);x.style.display=ok?'':'none';n+=ok}});document.getElementById('n').textContent=n+' of {len(P)} shown'}}
q.oninput=f;document.querySelectorAll('.cats button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.cats button').forEach(z=>z.classList.remove('on'));b.classList.add('on');c=b.dataset.c;f();document.getElementById('catalog').scrollIntoView({{behavior:'smooth'}})}});f()</script>"""
open(D+"/index.html","w").write(layout("PickAPlugin — an independent catalog of ChatGPT & Codex plugins",home))
for p in P:
  same=[x for x in P if x["category"]==p["category"] and x["slug"]!=p["slug"] and not x.get("featured")][:4]
  isf=p.get("featured")
  note=f'<p class=note>Editor\'s note: {e(PICKS[p["slug"]])}</p>' if p["slug"] in PICKS else ""
  rel="".join(f'<a class=row style="grid-template-columns:70px 1fr" href="{x["slug"]}.html"><span class="no mono">{num(x)}</span><span><h3>{e(x["name"])}</h3><p>{e(x["description"])}</p></span></a>' for x in same)
  b=f"""<article class=doc><div><a class=mono href="../index.html#catalog" style="text-decoration:none">← Catalog</a> <span class=mono>/</span> <a class=mono href="../c/{slug(p["category"])}.html" style="text-decoration:none">{e(p["category"])}</a>{'<div style="margin-top:14px"><span class=badge>Featured</span></div>' if isf else ""}<h1>{e(p["name"])}</h1>{'<p class=vbig>✓ Verified by maker <span class=mono>· paid badge: the maker claimed this listing and keeps it current</span></p>' if p.get("verified") else ""}<p class=d>{e(p["description"])}</p>{note}
<a class=btn href="{e(p["link"])}" rel="nofollow noopener" target=_blank>Open the project ↗</a>{"" if isf else '<p class=mine>Is this your plugin? <a href="../featured.html">Get featured</a>'+("" if p.get("verified") else ' or <a href="../advertise.html#verified">get a Verified badge ($9/mo)</a>')+' →</p>'}
<div class=sec><h2>Also in {e(p["category"])}</h2><span class=mono>{BLURB.get(p["category"],"")}</span></div>{pinned(p["category"],"",  "../")}{rel}</div>
<aside class=side><span class=mono>{num(p)}</span><dl><dt class=mono>Maker</dt><dd>{e(p["maker"] or "Unknown")}</dd><dt class=mono>Category</dt><dd>{e(p["category"])}</dd>
<dt class=mono>Listed via</dt><dd><a href="{e(p["source_url"])}">{e(p["source"])}</a></dd><dt class=mono>In our catalog since</dt><dd>{p["first_seen"]}</dd></dl>
<p style="font-size:14px;color:var(--mute);margin-top:24px">Made this? You can <a href="../featured.html">feature it</a> or <a href="mailto:{EMAIL}?subject=Listing%20fix:%20{e(p['name'])}">ask for a correction</a>.</p></aside></article>"""
  open(f'{D}/p/{p["slug"]}.html',"w").write(layout(f'{p["name"]} — PickAPlugin',b,1,p["description"][:155]))
os.makedirs(D+"/c",exist_ok=True)
# ---- best-of rankings + comparisons (real signals only: GitHub stars, editor's picks) ----
import re as _re
def stars(p): return p.get("stars") if isinstance(p.get("stars"),int) else -1
def rankkey(p): return (p.get("archived") is True, -(1 if p["slug"] in PICKS else 0), -stars(p), p["name"].lower())
def words(p): return {w for w in _re.findall(r"[a-z]{4,}",p["description"].lower())}-{"with","your","that","from","into","codex","claude","code","plugin","plugins","agent","agents","skills","skill","tools","using","which","their","this","them","they","over"}
PAIRS=[]
for c in cats:
  if c=="Miscellany": continue
  top=sorted([p for p in P if p["category"]==c and not p.get("archived") and stars(p)>=0],key=rankkey)[:25]
  for i,a in enumerate(top):
    for b2 in top[i+1:]:
      PAIRS.append((len(words(a)&words(b2))/max(1,len(words(a)|words(b2))),a,b2))
_sel=[]; _used=set(); _per={}
for j,a,b2 in sorted(PAIRS,key=lambda t:-t[0]):
  if len(_sel)==10 or j<0.12: break
  if a["slug"] in _used or b2["slug"] in _used or _per.get(a["category"],0)>=2: continue
  _sel.append((a,b2)); _used|={a["slug"],b2["slug"]}; _per[a["category"]]=_per.get(a["category"],0)+1
PAIRS=_sel
def cslug(a,b2): return f"{a['slug']}-vs-{b2['slug']}"
def catlinks(c):
  cmp=[(a,b2) for a,b2 in PAIRS if a["category"]==c]
  x=f'<p class=shelves><span class=mono>Ranked:</span><a href="../best/{slug(c)}.html">Best {e(c)} plugins, ranked by GitHub stars →</a>'
  x+="".join(f' <a href="../compare/{cslug(a,b2)}.html">{e(a["name"])} vs {e(b2["name"])}</a>' for a,b2 in cmp)
  return x+'</p>'
for c in cats:
  items=[p for p in P if p["category"]==c]
  b=f'''<div class=sec style="padding-top:40px"><h2 style="font-size:44px">{e(c)}</h2><span class=mono>{len(items)} plugins · {e(BLURB.get(c,""))}</span></div>{catlinks(c)}{sponsor(c)}{pinned(c,"../p/","../")}<div>{"".join(row(p,"../p/") for p in items)}</div>'''
  open(f"{D}/c/{slug(c)}.html","w").write(layout(f"{c} plugins for ChatGPT & Codex — PickAPlugin",b,1,f"{len(items)} {c} plugins for ChatGPT and Codex, hand-sorted."))
open(D+"/submit.html","w").write(layout("Submit a plugin — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Free, always</span><h1>Submit a plugin</h1>
<p>Listing costs nothing. We re-read our public sources every day, so if your plugin is public and in a list like <a href="https://github.com/hashgraph-online/awesome-codex-plugins">awesome-codex-plugins</a>, it'll show up on its own.</p>
<p>Not in a list yet? Email <a href="mailto:{EMAIL}?subject=Submit%20a%20plugin">{EMAIL}</a> with the repo link and one sentence on what it does. We read every one.</p>
<h3>In a hurry?</h3><p class=price>$19 <span class=mono>one-time</span></p><p>Expedited review: a decision within 24 hours. Paying buys speed, not a yes — if we pass, you get a refund.</p>{pay("expedited_review","Expedited review","$19")}</div>"""))
stat="".join(f'<span class=taken>Slot {k+1:02d}<br><b>{e(p["name"])}</b></span>' for k,p in enumerate(FEAT))+"".join(f'<span>Slot {len(FEAT)+k+1:02d}<br><b>Open</b></span>' for k in range(OPEN))
avail=f"{OPEN} of 3 open right now" if OPEN else "All 3 slots are taken right now"
cta=pay("featured_monthly","Claim a featured slot","$49/month") if OPEN else f'<p><b>All three slots are taken.</b> Email <a href="mailto:{EMAIL}?subject=Featured%20waitlist">{EMAIL}</a> and we\'ll tell you the moment one frees up.</p>'
open(D+"/featured.html","w").write(layout("Get featured — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Three slots. That's the whole inventory.</span><h1>Put your plugin where people pick plugins.</h1>
<p style="font-size:19px">PickAPlugin is a hand-sorted catalog of {len(P)} ChatGPT &amp; Codex plugins. Featured gets three slots, so each one actually stands out. (Other placements are on the <a href="advertise.html">advertise</a> page.)</p>
<p class=price>$49 <span class=mono>per month · cancel anytime</span></p>
<div class=slotstat>{stat}</div><p class=mono style="margin-top:-6px">{avail}</p>
{cta}
<h3>Where you appear</h3><ul class=where>
<li><b>Top of the homepage</b>: a large card in the Featured band, above the search and editor's picks.</li>
<li><b>Top of your category page</b>: pinned above every other plugin in that category.</li>
<li><b>“Also in” lists</b>: pinned first on the page of every other plugin in your category.</li>
<li><b>Your own page</b> gets a Featured badge.</li></ul>
<h3>What you get</h3><ul class=where><li>A clear “Featured” label. We don't disguise ads as picks, which is why readers trust the rest of the page.</li><li>Your own name, description and link. Want different copy? Email us.</li><li>Live within 24 hours of payment.</li><li>Month to month. Email us to cancel any time, no questions asked.</li></ul>
<div class=faq><h3>How do I get set up?</h3><p>Click the button and pay with Stripe. Put your plugin's URL (GitHub repo or homepage) in the “Plugin URL” box. If it isn't in the catalog yet, we'll add it.</p>
<h3>Will this get me installs?</h3><p>We don't promise traffic numbers, and we'll never invent any. What you get is the most visible spot on a site built for people who are choosing a plugin.</p>
<h3>Does paying change your picks or the catalog order?</h3><p>No. Editor's picks and the numbered catalog are never for sale.</p>
<h3>Can you turn me down?</h3><p>Yes. If a plugin is broken, malicious or misleading, we'll refund you and pass.</p>
<h3>What happens when I cancel?</h3><p>Your slot stays up until the end of the period you've paid for, then opens for someone else.</p>
<h3>Questions?</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<p style="margin-top:30px">{cta if OPEN else ""}</p></div>"""))
open(D+"/about.html","w").write(layout("About — PickAPlugin",f"""<div class=prose><h1>About</h1><p>PickAPlugin is an independent catalog of plugins for ChatGPT and Codex. It is <b>not affiliated with, endorsed by, or sponsored by OpenAI</b>.</p>
<p>Listings are collected daily from public sources and link straight to the original project. We don't host plugin code and we haven't audited it — a plugin can run commands on your machine, so read it first.</p>
<p>Editor's picks are our opinion, based on what each project says about itself. Featured slots are paid and always labelled.</p><p>Corrections, removals, hellos: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>"""))

def tier(id_,name,price,per,what,status,key):
  btn=pay(key,f"Buy {name}",price) if key and STRIPE.get(key) else '<span class="mono st">Coming soon · not on sale yet</span>'
  return f'<div class="tier{" soon" if not key else ""}" id={id_}><div><h3>{name}</h3><p style="margin:0">{what}</p></div><div class=pr>{price}<small>{per}</small></div><div><p class=st style="margin:0">{status}</p>{btn}</div></div>'
spon_open=len(cats)-sum(1 for c in cats if c in SPONS)
ladder="".join([
 tier("top","The Top Spot","$199","per month",f"One plugin, one bold banner at the very top of the homepage, plus a short write-up on why it's worth a look. Labelled as paid.",f"{'1 of 1 open' if not TOP else '0 of 1 open · taken'}","top_spot" if not TOP else None),
 tier("featured","Featured","$49","per month","A large card in the Featured band on the homepage, pinned at the top of your category page and the “Also in” lists, plus a Featured badge on your page.",f"{OPEN} of 3 open","featured_monthly" if OPEN else None),
 tier("belt","On the Belt","$19","per month","A card on the slow-scrolling belt across the top of every page, labelled “On the Belt”. Up to 12 plugins share it.",f"{BELT_OPEN} of 12 open","belt" if BELT_OPEN else None),
 tier("sponsor","Category Sponsor","$29","per month",f"A “Presented by” band at the top of one category page. One sponsor per category; you pick the category at checkout.",f"{spon_open} of {len(cats)} categories open"+(f" · taken: {', '.join(e(c) for c in SPONS)}" if SPONS else ""),"category_sponsor" if spon_open else None),
 tier("verified","Verified badge","$9","per month","A “✓ Verified by maker” mark on your listing and plugin page. It says you claimed the listing and keep it current. We confirm you maintain the project before turning it on.",f"{sum(1 for p in P if p.get('verified'))} verified so far · no cap","verified"),
 tier("newsletter","Newsletter slot","$39","per send","A labelled sponsor slot in the weekly PickAPlugin email. The newsletter hasn't launched yet, so this isn't for sale.","Coming soon",None)])
open(D+"/advertise.html","w").write(layout("Advertise — PickAPlugin",f"""<div class=prose style="max-width:900px"><span class=mono style="color:var(--acc)">Advertise · every paid spot is labelled</span><h1>Put your plugin in front of people choosing plugins.</h1>
<p style="font-size:19px">PickAPlugin is a hand-sorted catalog of {len(P)} ChatGPT &amp; Codex plugins. Here's everything that's for sale, with live counts of what's still open. Pay with Stripe, put your plugin's URL in the “Plugin URL” box, and you're live within 24 hours.</p>
<div class=ladder>{ladder}</div>
<div class=faq><h3>The honest bits</h3><ul class=where><li>We don't publish traffic numbers yet and won't invent any. You're buying a clearly labelled spot, not a guaranteed number of installs.</li>
<li>Editor's picks and the catalog order are never for sale. On the belt, unpaid picks are labelled “Pick” and paid cards “On the Belt”.</li>
<li>Monthly, cancel anytime by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. Your spot stays up until the paid period ends.</li>
<li>If a spot fills up before your payment lands, or your plugin is broken, malicious or misleading, we refund you in full.</li></ul>
<h3>Questions?</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>"""))
exec(open(os.path.join(ROOT,"scripts","build_seo.py")).read())
print("built",len(P),"pages")
