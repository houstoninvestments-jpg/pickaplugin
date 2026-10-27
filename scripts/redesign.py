# Print-style redesign preview. exec'd by build.py when REDESIGN=1; overrides templates only.
import subprocess as _sp, datetime as _dt
BUILD=_dt.date.today(); BUILD_S=BUILD.strftime("%A, %B %-d, %Y")
_ck=sorted({p.get("stars_checked") for p in P if p.get("stars_checked")}); CHECKED=_ck[-1] if _ck else None
CSS="""@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;0,6..72,800;1,6..72,400;1,6..72,600&family=Martian+Mono:wght@400;500&display=swap');
:root{--ink:#14171f;--paper:#f4efe1;--rule:#cfc6ad;--mute:#5b5a52;--acc:#1f3a8a}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.5 Newsreader,Georgia,serif;font-optical-sizing:auto}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:2px}.w{max-width:1180px;margin:auto;padding:0 28px}
.mono{font-family:'Martian Mono',ui-monospace,monospace;font-size:10.5px;letter-spacing:.02em;text-transform:uppercase}
.mast{text-align:center;padding-top:14px}.ear{display:flex;justify-content:space-between;border-bottom:1px solid var(--ink);padding-bottom:8px;color:var(--mute)}
.wm{display:block;font:800 76px/1 Newsreader,serif;letter-spacing:-.045em;text-decoration:none;padding:16px 0 6px}.wm i{font-style:italic;font-weight:600;color:var(--acc)}
.tag{font-style:italic;color:var(--mute);margin:0 0 12px}
.dl{display:flex;justify-content:space-between;border-top:3px solid var(--ink);border-bottom:1px solid var(--ink);padding:6px 0;margin-top:2px}
.nav{display:flex;justify-content:center;gap:26px;border-bottom:1px solid var(--ink);padding:7px 0}.nav a{text-decoration:none}.nav a:hover{color:var(--acc)}
h1,h2,h3{font-family:Newsreader,serif}
.cls{border:1px solid var(--ink);padding:10px 12px 12px;background:#fffdf8;text-decoration:none;display:block}.cls .k{display:block;border-bottom:1px solid var(--ink);padding-bottom:4px;margin-bottom:6px}
.cls b{font-weight:800;font-size:18px}.cls p{margin:2px 0 0;font-size:15px}.cls.open{border-style:dashed;background:transparent}.cls.open .k{border-bottom-style:dashed}.cls:hover{border-color:var(--acc)}
.belt{padding:7px 0;border-bottom:1px solid var(--ink);font-size:14.5px}.belt .lab{color:var(--mute);margin-right:8px}.belt a{text-decoration:none}.belt a:hover{text-decoration:underline}.belt .o{color:var(--acc);font-style:italic}.belt i{color:var(--rule)}
.front{display:grid;grid-template-columns:2fr 1fr;gap:0;border-bottom:1px solid var(--ink)}.front>div{padding:22px 26px 24px 0}.front>div+div{border-left:1px solid var(--ink);padding:22px 0 24px 26px}
.lead h2{font:800 54px/1 Newsreader,serif;letter-spacing:-.03em;margin:8px 0 10px}.lead h2 a{text-decoration:none}.lead p.d{font-size:21px;line-height:1.4;margin:0 0 10px}.lead .k{color:var(--acc)}
.side3 h3{font-size:22px;margin:4px 0 4px}.side3 .it{padding:10px 0;border-bottom:1px solid var(--rule)}.side3 .it:last-child{border:0}.side3 p{margin:0;font-size:15px}
.sec{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid var(--ink);border-top:3px solid var(--ink);padding:6px 0 6px;margin-top:30px}.sec h2{font:600 24px Newsreader,serif;margin:0;font-style:italic}
.cols{column-count:3;column-gap:30px;column-rule:1px solid var(--rule);padding-top:10px}
.row{display:block;break-inside:avoid;padding:8px 0 9px;border-bottom:1px solid var(--rule);text-decoration:none}.row h3{font:600 17px/1.25 Newsreader,serif;margin:0}.row:hover h3{color:var(--acc);text-decoration:underline}
.row p{margin:2px 0 3px;font-size:14.5px;line-height:1.4;color:#2b2823}.row .m{color:var(--mute);font-size:9.5px}
.find{display:grid;grid-template-columns:1fr 2fr;gap:26px;padding:12px 0;border-bottom:1px solid var(--ink)}#q{width:100%;border:0;border-bottom:1px solid var(--ink);background:transparent;font:italic 20px Newsreader,serif;padding:4px 0;outline:none}
.cats{display:flex;flex-wrap:wrap;gap:2px 14px;font-size:15px}.cats button{all:unset;cursor:pointer}.cats button.on{color:var(--acc);text-decoration:underline}.cats sup{color:var(--mute);font-size:10px}
.ads{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding-top:12px}
.doc{display:grid;grid-template-columns:1fr 280px;gap:44px;padding:28px 0 50px}.doc h1{font:800 60px/1 Newsreader,serif;letter-spacing:-.035em;margin:12px 0 14px}.doc .d{font-size:22px;line-height:1.4}
.side{border-top:3px solid var(--ink);padding-top:10px}.side dl{margin:0}.side dt{margin-top:12px;color:var(--mute)}.side dd{margin:2px 0 0}
.btn{display:inline-block;border:1px solid var(--ink);color:var(--ink);padding:8px 14px;text-decoration:none;font:500 11px 'Martian Mono',monospace;text-transform:uppercase;margin-top:16px}.btn:hover{background:var(--ink);color:var(--paper)}
.note{border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);padding:10px 0;margin:22px 0;font-style:italic;font-size:18px}.note:first-letter{color:var(--acc)}
.badge{font:500 10px 'Martian Mono',monospace;text-transform:uppercase;border:1px solid var(--acc);color:var(--acc);padding:1px 5px}
.vchk{font:500 9.5px 'Martian Mono',monospace;text-transform:uppercase;color:#1d5b33;margin-left:6px;white-space:nowrap}.vbig{color:#1d5b33;margin:0 0 10px}
.prose{max-width:700px;padding:30px 0 60px}.prose h1{font:800 50px/1.02 Newsreader,serif;letter-spacing:-.03em;margin:8px 0 18px}.prose h3{font-size:22px;margin:30px 0 4px}.price{font:600 36px Newsreader,serif}
.sig{font-style:italic;margin-top:30px;border-top:1px solid var(--ink);padding-top:10px}
.todo{border:1px dashed var(--acc);padding:10px}.mine{font-size:14px;color:var(--mute)}.mine a{color:var(--acc)}.shelves{display:flex;flex-wrap:wrap;gap:4px 16px;padding:10px 0;font-size:15px}
.fpin{margin:12px 0}.fopen{display:block;margin:12px 0}.spons{margin:12px 0}
.slotstat{display:flex;gap:10px;margin:14px 0}.slotstat span{flex:1;border:1px solid var(--ink);padding:10px;text-align:center}.slotstat .taken{background:var(--ink);color:var(--paper)}
.ladder{border-top:3px solid var(--ink);margin-top:22px}.tier{display:grid;grid-template-columns:1fr 130px 220px;gap:22px;padding:18px 0;border-bottom:1px solid var(--rule)}.tier h3{margin:0 0 4px}.tier .pr{font:600 28px Newsreader,serif}.tier .pr small{display:block;font:400 10px 'Martian Mono',monospace;color:var(--mute);text-transform:uppercase}.tier .st{font-size:14px;color:var(--mute)}.tier.soon{opacity:.6}
.log li{margin:4px 0;list-style:none}.log{padding:0}.log .mono{color:var(--mute);margin-right:10px}
footer{border-top:3px solid var(--ink);margin-top:40px;padding:14px 0 40px;color:var(--mute);font-size:13.5px;display:flex;justify-content:space-between;gap:30px}
.box{border:1px solid var(--ink);background:#fffdf8;padding:14px 16px;margin:22px 0}.box h3{margin:0 0 6px;font-size:21px}.box p{margin:4px 0;font-size:15px}
.box label{display:block;margin-top:8px}.box input,.box textarea{width:100%;border:0;border-bottom:1px solid var(--ink);background:transparent;font:16px Newsreader,serif;padding:4px 0;outline:none}.box textarea{border:1px solid var(--rule);min-height:64px}
.box button,.nl button{border:1px solid var(--ink);background:var(--ink);color:var(--paper);padding:8px 14px;font:500 11px 'Martian Mono',monospace;text-transform:uppercase;cursor:pointer;margin-top:10px}
.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}.cf-turnstile{margin-top:10px}
pre.code{background:#fffdf8;border:1px solid var(--rule);padding:8px;font:12px 'Martian Mono',monospace;white-space:pre-wrap;word-break:break-all;margin:6px 0}
.nl{border-top:3px solid var(--ink);margin-top:40px;padding:14px 0 4px;display:grid;grid-template-columns:1fr 1.2fr;gap:24px}.nl h3{margin:0;font-size:24px;font-style:italic}.nl p{margin:4px 0;color:var(--mute);font-size:14.5px}
.nl form{display:flex;flex-wrap:wrap;gap:8px;align-items:end}.nl input[type=email]{flex:1;min-width:200px;border:0;border-bottom:1px solid var(--ink);background:transparent;font:italic 19px Newsreader,serif;padding:4px 0;outline:none}
@media(max-width:860px){.nl{grid-template-columns:1fr}}
@media(max-width:860px){.cols{column-count:1}.front,.doc,.find,.tier{grid-template-columns:1fr}.front>div+div{border:0;padding-left:0}.ads{grid-template-columns:1fr}.wm{font-size:48px}}
.hero2{text-align:center;padding:64px 0 56px;border-bottom:1px solid var(--ink)}.hero2 h1{font:800 58px/1.04 Newsreader,serif;letter-spacing:-.03em;margin:0 auto 18px;max-width:17ch}.hero2 h1 em{font-weight:600;color:var(--acc)}
.hero2 p{font-size:21px;line-height:1.45;max-width:40ch;margin:0 auto 30px;color:#2b2823}
.hero2 form{display:flex;max-width:560px;margin:0 auto;border:1px solid var(--ink);background:#fffdf8}.hero2 input{flex:1;min-width:0;border:0;background:transparent;font:italic 19px Newsreader,serif;padding:13px 16px!important;outline:none;height:auto}
.hero2 button{border:0;background:var(--ink);color:var(--paper);font:500 11px 'Martian Mono',monospace;text-transform:uppercase;padding:0 20px;cursor:pointer}.hero2 button:hover{background:var(--acc)}
.hero2 .mk{display:block;margin-top:18px;font-size:15px;color:var(--mute)}.hero2 .mk a{color:var(--acc)}
@media(max-width:860px){.ear,.dl{display:none}.nav{justify-content:flex-start;overflow-x:auto;white-space:nowrap;gap:18px}.hero2{padding:36px 0 32px}.hero2 h1{font-size:38px}.hero2 p{font-size:18px}}"""
open(D+"/style.css","w").write(CSS)
def layout(title,body,depth=0,desc="An independent, hand-edited catalog of ChatGPT and Codex plugins."):
  r="../"*depth
  return f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><title>{e(title)}</title>
<meta name=description content="{e(desc)}"><link rel=stylesheet href="{r}style.css"><script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script></head><body><div class=w>
<header class=mast><div class="ear mono"><span>Independent · not affiliated with OpenAI</span><span>Hand-sorted, not ranked by an algorithm</span></div>
<a class=wm href="{r}index.html">PickA<i>Plugin</i></a><p class=tag>A catalog of ChatGPT &amp; Codex plugins, sorted by people.</p>
<div class="dl mono"><span>Issue No. 1</span><span>Updated {BUILD_S}</span><span>{len(P)} plugins catalogued</span></div>
<nav class="nav mono"><a href="{r}index.html#catalog">Catalog</a>{"".join(f'<a href="{r}c/{slug(c)}.html">{e(c.split(" ")[0].rstrip(","))}</a>' for c in cats[:6])}<a href="{r}about.html">How we pick</a><a href="{r}tools/index.html">Free tools</a><a href="{r}changelog.html">Changelog</a><a href="{r}advertise.html">Advertise</a></nav></header>
{(body.replace("<!--/hero-->",belt(r),1) if "<!--/hero-->" in body else belt(r)+body)}{nlform("footer")}<footer><span>PickAPlugin is an independent catalog. Not affiliated with, endorsed by, or sponsored by OpenAI. ChatGPT and Codex are trademarks of OpenAI. Listings come from public sources and are not audited. Read the code before you install anything.</span><span><a href="{r}about.html">How we pick</a> · <a href="{r}tools/index.html">Free tools</a> · <a href="{r}black-friday.html">Black Friday deals</a> · <a href="{r}research/state-of-codex-plugins-2026.html">State of Codex Plugins 2026</a> · <a href="{r}blog.html">Blog</a> · <a href="{r}changelog.html">Changelog</a> · <a href="{r}advertise.html">Advertise</a> · <a href="{r}privacy.html">Privacy</a> · <a href="{r}terms.html">Terms</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></span></footer></div></body></html>"""
import json as _json
_SEC=os.path.join(ROOT,"scripts",".secrets.json")
SITEKEY=_json.load(open(_SEC)).get("sitekey") if os.path.exists(_SEC) else "0x4AAAAAAFnRt9YCBHXNJWZZ"
def ts(): return f'<div class=cf-turnstile data-sitekey="{SITEKEY}" data-size="flexible"></div>'
HONEY='<div class=hp aria-hidden=true><label>Leave this empty <input name=website tabindex=-1 autocomplete=off></label></div>'
def nlform(where,title="The PickAPlugin roundup"):
  return f'''<section class=nl><div><h3>{title}</h3><p>A weekly-ish email with new and notable ChatGPT &amp; Codex plugins. No spam. Unsubscribe anytime with one click.</p></div>
<form method=post action="/api/subscribe"><input type=email name=email required placeholder="you@example.com" aria-label="Email address"><input type=hidden name=from value="{where}">{HONEY}<button>Subscribe</button>{ts()}</form></section>'''
def meta(p):
  bits=[num(p),p["category"]]
  if isinstance(p.get("stars"),int): bits.append(f'★ {p["stars"]:,} on {p.get("stars_checked") or "?"}')
  if p.get("archived"): bits.append("archived")
  return " · ".join(e(b) for b in bits)
def row(p,pre="p/"): return f'<a class=row href="{pre}{p["slug"]}.html" data-c="{e(p["category"])}" data-t="{e((p["name"]+" "+p["description"]+" "+p["maker"]).lower())}"><h3>{e(p["name"])}{vmark(p)}</h3><p>{e(p["description"])}</p><span class="m mono">{meta(p)}</span></a>'
def vmark(p): return ' <span class=vchk title="Paid badge: the maker claimed this listing">✓ verified by maker (paid)</span>' if p.get("verified") else ""
def cad(kind,name,desc,href,open_=False): return f'<a class="cls{" open" if open_ else ""}" href="{href}"><span class="k mono">{kind}</span><b>{e(name)}</b><p>{e(desc)}</p></a>'
def pinrow(p,pre): return cad("Advertisement · Featured",p["name"],p["description"][:140],f'{pre}{p["slug"]}.html')
def pinned(cat,pre,r):
  fs=[p for p in FEAT if p["category"]==cat]
  if fs: return '<div class=fpin>'+"".join(pinrow(p,pre) for p in fs)+'</div>'
  if OPEN: return f'<div class=fopen>{cad("Classified · space available","Featured spot open in "+cat,"Pin your plugin above every list in this category. $49/mo.",r+"featured.html",True)}</div>'
  return ""
def belt(r):
  paid=[f'<a href="{r}p/{p["slug"]}.html"><b>{e(p["name"])}</b> — {e(p["description"][:60])}</a>' for p in BELT]
  if BELT_OPEN: paid.append(f'<a class=o href="{r}advertise.html#belt">{BELT_OPEN} of 12 lines open · $19/mo</a>')
  return f'<section class=belt><span class="mono lab">Classifieds (paid, labelled):</span>{" <i>·</i> ".join(paid)}</section>'
def sponsor(c):
  p=SPONS.get(c)
  if p: return f'<div class=spons>{cad("Advertisement · this shelf is presented by",p["name"],p["description"][:120],"../p/"+p["slug"]+".html")}</div>'
  return f'<div class=spons>{cad("Classified · sponsor wanted","Sponsor the "+c+" shelf","One sponsor per category, labelled. $29/mo.","../advertise.html#sponsor",True)}</div>'
def checked(p): return f'<dt class=mono>Checked on</dt><dd>{e(p["stars_checked"])}{" · ★ "+format(p["stars"],",")+" GitHub stars" if isinstance(p.get("stars"),int) else ""}</dd>' if p.get("stars_checked") else ""
def preview_home():
  if TOP:
    p=TOP[0]; k="Advertisement · The Top Spot (paid)"; w=p.get("top_spot_note") or p["description"]
  else:
    p=by[PK[0]]; k="Editor's pick · unpaid"; w=PICKS[p["slug"]]
  lead=f'<div class=lead><span class="k mono">{k}</span><h2><a href="p/{p["slug"]}.html">{e(p["name"])}</a></h2><p class=d>{e(w)}</p><span class="mono" style="color:var(--mute)">by {e(p["maker"])} · {meta(p)}</span><br><a class=btn href="p/{p["slug"]}.html">Read the listing</a></div>'
  others=[s for s in PK if s!=p["slug"]][:3]
  side="<span class=mono>Also picked this issue</span>"+"".join(f'<div class=it><span class="mono" style="color:var(--acc)">Pick · {e(by[s]["category"])}</span><h3><a href="p/{s}.html" style="text-decoration:none">{e(by[s]["name"])}</a></h3><p>{e(PICKS[s])}</p></div>' for s in others)
  ads=[pinrow(x,"p/") for x in FEAT]
  if OPEN: ads.append(cad("Classified · space available",f"Featured: {OPEN} of 3 open","A labelled box on the front page and atop your category. $49/mo.","featured.html",True))
  if not TOP: ads.append(cad("Classified · space available","The Top Spot","The lead story slot above, labelled as paid. $199/mo, one at a time.","advertise.html#top",True))
  ads.append(cad("Classified · always open","Verified by maker","Claim your listing and keep it current. $9/mo.","advertise.html#verified",True))
  rest=[s for s in PK if s!=p["slug"] and s not in others]
  picks2="".join(f'<a class=row href="p/{s}.html"><h3>{e(by[s]["name"])}</h3><p>{e(PICKS[s])}</p><span class="m mono">{meta(by[s])}</span></a>' for s in rest)
  chips='<button class=on data-c="">Everything</button>'+"".join(f'<button data-c="{e(c)}">{e(c)}<sup>{count[c]}</sup></button>' for c in cats)
  hero=f"""<section class=hero2><h1>Hundreds of ChatGPT &amp; Codex plugins, scattered across GitHub. <em>Here they are in one place.</em></h1>
<p>We gather them, sort them by hand, and show the real details (last update, license, install command) so you can tell what's worth installing. Free to browse.</p>
<form onsubmit="event.preventDefault();document.getElementById('catalog').scrollIntoView({{behavior:'smooth'}})" role=search><input id=q type=search placeholder="memory, PDF, secrets…" aria-label="Search plugins"><button>Browse plugins</button></form>
<span class=mk>Made a plugin? <a href="submit.html">List it free</a> or claim your listing. Running a sale? <a href="black-friday.html">Black Friday deals</a>. New: <a href="research/state-of-codex-plugins-2026.html">State of Codex Plugins 2026</a>, our data on 339 plugin repos.</span></section><!--/hero-->"""
  return hero+f"""<section class=front><div>{lead}</div><div class=side3>{side}</div></section>
{nlform("home","Get the roundup by email")}<div class=sec><h2>Ads &amp; open space</h2><span class=mono>Paid placements are labelled. They never change picks or catalog order.</span></div><div class=ads>{ads and "".join(ads[:3])}</div>
{f'<div class=sec><h2>More picks</h2><span class=mono>Our opinion, from each project&#39;s own docs · not audited</span></div><div class=cols>{picks2}</div>' if picks2 else ""}
<div class=sec id=catalog><h2>The full catalog</h2><span class=mono id=n></span></div>
<div class=find style="grid-template-columns:1fr"><div class=cats>{chips}</div></div>
<p class="mono" style="color:var(--mute);margin:10px 0 0">Stars pulled from GitHub on {CHECKED or "—"}. Listed in catalog order.</p>
<div id=list class=cols>{"".join(row(x) for x in P)}</div>
<script>let c="",q=document.getElementById('q'),rs=[...document.querySelectorAll('#list .row')];function f(){{let t=q.value.toLowerCase(),n=0;rs.forEach(x=>{{let ok=(!c||x.dataset.c==c)&&x.dataset.t.includes(t);x.style.display=ok?'':'none';n+=ok}});document.getElementById('n').textContent=n+' of {len(P)} shown'}}
q.oninput=f;document.querySelectorAll('.cats button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.cats button').forEach(z=>z.classList.remove('on'));b.classList.add('on');c=b.dataset.c;f()}});f()</script>"""
def preview_pages():
  srcs=sorted({(p["source"],p["source_url"]) for p in P})
  open(D+"/about.html","w").write(layout("How we pick — PickAPlugin",f"""<div class=prose><span class="mono" style="color:var(--acc)">About · How we pick</span><h1>How this catalog is made</h1>
<p>PickAPlugin is an independent catalog of plugins for ChatGPT and Codex. It is <b>not affiliated with, endorsed by, or sponsored by OpenAI</b>.</p>
<h3>1. The catalog comes from public lists</h3><p>Every day a script re-reads public GitHub lists of plugins and adds anything new. Today that's {len(srcs)} source{"s" if len(srcs)!=1 else ""}: {", ".join(f'<a href="{e(u)}">{e(s)}</a>' for s,u in srcs)}. Each listing links straight to the original project, and we don't host any plugin code.</p>
<h3>2. Signals are pulled, not invented</h3><p>GitHub star counts and archived status come from the GitHub API, and each listing shows the date we last checked (most recently {CHECKED or "—"}). Stars measure attention, not quality, so we don't sort the catalog by them.</p>
<h3>3. Picks are a human call</h3><p>An editor reads each project's own description and README and marks the handful we'd actually try, with a one-line reason. Picks are opinion. We haven't audited the code, and a plugin can run commands on your machine, so read it first.</p>
<h3>4. Paid placements are always labelled</h3><p>Featured, the Top Spot, On the Belt, category sponsors and the Verified badge are paid. Each one is marked as an advertisement or paid badge wherever it appears. Money never changes the picks or the catalog order. Rates are on the <a href="advertise.html">advertise</a> page.</p>
<h3>5. Corrections</h3><p>Wrong description, dead link, want something removed? Email <a href="mailto:{EMAIL}">{EMAIL}</a>. Every change we ship is in the <a href="changelog.html">changelog</a>.</p>
<p class=sig>The PickAPlugin editors</p></div>"""))
  try: lg=_sp.run(["git","-C",ROOT,"log","--date=short","--format=%ad\t%s"],capture_output=True,text=True).stdout.strip().splitlines()
  except Exception: lg=[]
  items="".join(f'<li><span class=mono>{e(l.split(chr(9))[0])}</span>{e(l.split(chr(9),1)[1])}</li>' for l in lg if chr(9) in l)
  open(D+"/changelog.html","w").write(layout("Changelog — PickAPlugin",f"""<div class=prose style="max-width:820px"><span class="mono" style="color:var(--acc)">Changelog</span><h1>What changed, and when</h1><p>Generated from the site's git history at build time ({BUILD_S}).</p><ul class=log>{items}</ul><p class=sig>The PickAPlugin editors</p></div>"""))
