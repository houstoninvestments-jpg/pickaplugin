#!/usr/bin/env python3
"""Static site generator: data/plugins.json -> dist/ (Cloudflare Pages output dir)."""
import json, os, html, shutil
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=os.path.join(ROOT,"dist")
P=json.load(open(os.path.join(ROOT,"data","plugins.json")))
for p in P:
  if p["category"]=="Other": p["category"]="Miscellany"
# TODO(Aaron): paste real Stripe Payment Links here once created in Stripe. Leave "" until then.
# Live Stripe Payment Links go here. Sandbox (test-mode) links, for local preview only:
#   featured_monthly: https://buy.stripe.com/test_14AaEZ8TC3vJelQ2ai73G00
#   expedited_review: https://buy.stripe.com/test_bJe5kF4Dmd6j4Lg9CK73G01
# Preview with: STRIPE_PREVIEW=test python3 scripts/build.py   (never deploy that build)
import os as _os
STRIPE={"featured_monthly":"","expedited_review":""}
if _os.environ.get("STRIPE_PREVIEW")=="test":
    STRIPE={"featured_monthly":"https://buy.stripe.com/test_14AaEZ8TC3vJelQ2ai73G00","expedited_review":"https://buy.stripe.com/test_bJe5kF4Dmd6j4Lg9CK73G01"}
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
@media(max-width:800px){.lede,.doc{grid-template-columns:1fr}.picks,.slots{grid-template-columns:1fr}.row{grid-template-columns:44px 1fr}.side+x{}.doc .row p{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}.row .c{display:none}.brand a.n{font-size:38px}}"""
def layout(title,body,depth=0,desc="An independent, hand-edited catalog of ChatGPT and Codex plugins."):
  r="../"*depth
  return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<meta name=description content="{e(desc)}"><link rel=stylesheet href="{r}style.css"></head><body><div class=w>
<header class=mast><div class="top mono"><span>Independent · not affiliated with OpenAI</span><span>{len(P)} plugins catalogued</span></div>
<div class=brand><a class=n href="{r}index.html">PickA<i>Plugin</i></a><nav><a href="{r}index.html#catalog">Catalog</a><a href="{r}submit.html">Submit</a><a href="{r}featured.html">Advertise</a><a href="{r}about.html">About</a></nav></div></header>
{body}<footer><span>PickAPlugin is an independent catalog. Not affiliated with, endorsed by, or sponsored by OpenAI. ChatGPT and Codex are trademarks of OpenAI. Listings come from public sources — read the code before you install anything.</span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></footer></div></body></html>"""
idx={p["slug"]:i+1 for i,p in enumerate(P)}
def num(p): return f"No.{idx[p['slug']]:03d}"
def row(p): return f'<a class=row href="p/{p["slug"]}.html" data-c="{e(p["category"])}" data-t="{e((p["name"]+" "+p["description"]+" "+p["maker"]).lower())}"><span class="no mono">{num(p)}</span><span><h3>{e(p["name"])}</h3><p>{e(p["description"])}</p></span><span class="c mono">{e(p["category"])}</span></a>'
def pay(key,label,price):
  if STRIPE[key]: return f'<a class=btn href="{STRIPE[key]}">{label} — {price}</a>'
  return f'<div class=todo>TODO: Stripe Payment Link for “{label}” ({price}) isn\'t connected yet, so payments aren\'t live. Until then, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</div>'
shutil.rmtree(D,ignore_errors=True); os.makedirs(D+"/p"); open(D+"/style.css","w").write(CSS)
by={p["slug"]:p for p in P}; cats=sorted({p["category"] for p in P},key=lambda c:(c=="Miscellany",c))
count={c:sum(p["category"]==c for p in P) for c in cats}
picks="".join(f'<a class=pick href="p/{s}.html"><span class="no mono">Pick {i+1:02d} · {e(by[s]["category"])}</span><h3>{e(by[s]["name"])}</h3><p>{e(n)}</p><div class="by mono">by {e(by[s]["maker"])}</div></a>' for i,(s,n) in enumerate(PICKS.items()) if s in by)
feat=[p for p in P if p.get("featured")][:3]
slots="".join(f'<a class=slot href="p/{p["slug"]}.html"><span class=mono>Featured</span><b>{e(p["name"])}</b><span>{e(p["description"][:90])}</span></a>' for p in feat)+(f'<a class=slot href="featured.html" style="grid-column:span {3-len(feat)}"><span class=mono>Sponsored · {3-len(feat)} of 3 slots open</span><b>Built a plugin? Put it here for $49 a month.</b><span>Clearly labelled, never touches our picks or the catalog order. Cancel anytime.</span></a>' if len(feat)<3 else "")
dates=sorted({p["first_seen"] for p in P}); new=[p for p in P if len(dates)>1 and p["first_seen"]>dates[0]][-10:]
newsec=f'<div class=sec><h2>Fresh in the catalog</h2><span class=mono>added since {dates[0]}</span></div>'+"".join(row(p) for p in new) if new else ""
chips='<button class=on data-c="">Everything</button>'+"".join(f'<button data-c="{e(c)}">{e(c)}<sup>{count[c]}</sup></button>' for c in cats)
home=f"""<section class=lede><div><span class="mono" style="color:var(--acc)">The catalog · Issue 01</span><h1>Plugins for ChatGPT &amp; Codex, <em>sorted by a person</em>, not a leaderboard.</h1>
<p>We read the lists so you don't have to. Every plugin here links back to its source. A few we'd actually install are marked as picks.</p></div>
<div><label class=mono for=q>Search {len(P)} plugins</label><input id=q placeholder="memory, PDF, secret scanning…"><div class=cats>{chips}</div></div></section>
<div class=sec><h2>Editor's picks</h2><span class=mono>Chosen from each project's own description · not audited</span></div><div class=picks>{picks}</div>
<div class=slots>{slots}</div>{newsec}
<div class=sec id=catalog><h2>The full catalog</h2><span class=mono id=n></span></div><div id=list>{"".join(row(p) for p in P)}</div>
<script>let c="",q=document.getElementById('q'),rs=[...document.querySelectorAll('#list .row')];function f(){{let t=q.value.toLowerCase(),n=0;rs.forEach(x=>{{let ok=(!c||x.dataset.c==c)&&x.dataset.t.includes(t);x.style.display=ok?'':'none';n+=ok}});document.getElementById('n').textContent=n+' of {len(P)} shown'}}
q.oninput=f;document.querySelectorAll('.cats button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.cats button').forEach(z=>z.classList.remove('on'));b.classList.add('on');c=b.dataset.c;f();document.getElementById('catalog').scrollIntoView({{behavior:'smooth'}})}});f()</script>"""
open(D+"/index.html","w").write(layout("PickAPlugin — an independent catalog of ChatGPT & Codex plugins",home))
for p in P:
  same=[x for x in P if x["category"]==p["category"] and x["slug"]!=p["slug"]][:4]
  note=f'<p class=note>Editor\'s note: {e(PICKS[p["slug"]])}</p>' if p["slug"] in PICKS else ""
  rel="".join(f'<a class=row style="grid-template-columns:70px 1fr" href="{x["slug"]}.html"><span class="no mono">{num(x)}</span><span><h3>{e(x["name"])}</h3><p>{e(x["description"])}</p></span></a>' for x in same)
  b=f"""<article class=doc><div><a class=mono href="../index.html#catalog" style="text-decoration:none">← Catalog / {e(p["category"])}</a><h1>{e(p["name"])}</h1><p class=d>{e(p["description"])}</p>{note}
<a class=btn href="{e(p["link"])}" rel="nofollow noopener" target=_blank>Open the project ↗</a>
<div class=sec><h2>Also in {e(p["category"])}</h2><span class=mono>{BLURB.get(p["category"],"")}</span></div>{rel}</div>
<aside class=side><span class=mono>{num(p)}</span><dl><dt class=mono>Maker</dt><dd>{e(p["maker"] or "Unknown")}</dd><dt class=mono>Category</dt><dd>{e(p["category"])}</dd>
<dt class=mono>Listed via</dt><dd><a href="{e(p["source_url"])}">{e(p["source"])}</a></dd><dt class=mono>In our catalog since</dt><dd>{p["first_seen"]}</dd></dl>
<p style="font-size:14px;color:var(--mute);margin-top:24px">Made this? You can <a href="../featured.html">feature it</a> or <a href="mailto:{EMAIL}?subject=Listing%20fix:%20{e(p['name'])}">ask for a correction</a>.</p></aside></article>"""
  open(f'{D}/p/{p["slug"]}.html',"w").write(layout(f'{p["name"]} — PickAPlugin',b,1,p["description"][:155]))
open(D+"/submit.html","w").write(layout("Submit a plugin — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Free, always</span><h1>Submit a plugin</h1>
<p>Listing costs nothing. We re-read our public sources every day, so if your plugin is public and in a list like <a href="https://github.com/hashgraph-online/awesome-codex-plugins">awesome-codex-plugins</a>, it'll show up on its own.</p>
<p>Not in a list yet? Email <a href="mailto:{EMAIL}?subject=Submit%20a%20plugin">{EMAIL}</a> with the repo link and one sentence on what it does. We read every one.</p>
<h3>In a hurry?</h3><p class=price>$19 <span class=mono>one-time</span></p><p>Expedited review: a decision within 48 hours. Paying buys speed, not a yes — if we pass, you get a refund.</p>{pay("expedited_review","Expedited review","$19")}</div>"""))
open(D+"/featured.html","w").write(layout("Advertise — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Three slots, no more</span><h1>Get your plugin in front of people who are choosing one</h1>
<p class=price>$49 <span class=mono>per month</span></p><ul><li>One of three featured slots on the homepage</li><li>Pinned to the top of your category</li><li>Always labelled “Featured” — it never changes the catalog order or our picks</li><li>Monthly, cancel anytime</li></ul>
{pay("featured_monthly","Featured slot","$49/month")}<p style="color:var(--mute);font-size:14px;margin-top:20px">We don't promise traffic or installs. We do promise not to feature anything broken.</p></div>"""))
open(D+"/about.html","w").write(layout("About — PickAPlugin",f"""<div class=prose><h1>About</h1><p>PickAPlugin is an independent catalog of plugins for ChatGPT and Codex. It is <b>not affiliated with, endorsed by, or sponsored by OpenAI</b>.</p>
<p>Listings are collected daily from public sources and link straight to the original project. We don't host plugin code and we haven't audited it — a plugin can run commands on your machine, so read it first.</p>
<p>Editor's picks are our opinion, based on what each project says about itself. Featured slots are paid and always labelled.</p><p>Corrections, removals, hellos: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>"""))
print("built",len(P),"pages")
