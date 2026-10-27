# Executed at the end of build.py (shares its namespace: P, D, layout, e, slug, cats, PICKS, PAIRS, ...).
# Writes /best, /compare, /privacy, /terms, robots.txt, sitemap.xml, the IndexNow key file, then rewrites
# every page to clean URLs and adds canonical / Open Graph / JSON-LD tags.
import glob as _glob, posixpath as _pp, datetime as _dt, json as _json
SITE="https://pickaplugin.com"; INDEXNOW_KEY="6375d5cb89838413d1e117374c6ce038"
def fmt(n): return f"{n:,}" if n>=0 else "n/a"
def srow(p,i):
  tags=[]
  if p["slug"] in PICKS: tags.append("Editor's pick")
  if p.get("archived"): tags.append("Archived on GitHub")
  t=f' <span class=vchk style="color:var(--acc);border-color:var(--acc)">{" · ".join(tags)}</span>' if tags else ""
  return f'<a class=row href="../p/{p["slug"]}.html"><span class="no mono">#{i}</span><span><h3>{e(p["name"])}{t}</h3><p>{e(p["description"])}</p></span><span class="c mono">★ {fmt(stars(p))} · by {e(p["maker"])}</span></a>'
INTRO={
"Agent Workflows":"This is the busiest shelf: tools that split work across several agents, enforce a plan-then-build loop, or wrap a whole delivery process. Look for ones that write their plan to files you can read, because that's what makes a long run debuggable.",
"Memory & Context":"These plugins try to give an agent something it lacks by default: memory that survives the session. Check where each one stores what it remembers (local files vs a hosted service) before you trust it with a real codebase.",
"Security & Governance":"Secret scanning, policy hooks, pentest helpers and guardrails. An agent with shell access can read more than you think, so this shelf is worth a look before anything else.",
"Review & Testing":"Plugins that review diffs, write or run tests, or check an agent's work before you merge it. Most are prompts plus scripts, so read what they run.",
"Messaging & Remote":"Ways to reach an agent, or be reached by one, from a phone, Slack, Telegram or Discord. Several route through hosted services, so check what leaves your machine.",
"Design & Frontend":"UI, CSS, image and front-end helpers. Quality varies a lot here, so the project's own screenshots are the best quick signal.",
"Docs, Content & SEO":"Writing, PDFs, transcripts, translation and SEO tooling for agents.",
"Data & Backend":"Database, analytics, dbt and observability helpers. Be careful about giving any of these credentials to production systems.",
"Deploy & DevOps":"Deploys, containers, git hosting and publishing. These touch real infrastructure, so start them on a test project.",
"Usage & Quotas":"Small tools that show how much of your plan or rate limit an agent has used, and when it resets.",
"Industry Tools":"Niche plugins for specific trades and businesses, from CAD to legal research.",
}
os.makedirs(D+"/best",exist_ok=True); os.makedirs(D+"/compare",exist_ok=True)
for c in cats:
  items=sorted([p for p in P if p["category"]==c],key=rankkey)
  checked=max((p.get("stars_checked","") for p in items),default="")
  top=items[0] if items else None
  cmp="".join(f'<li><a href="../compare/{cslug(a,b2)}.html">{e(a["name"])} vs {e(b2["name"])}</a></li>' for a,b2 in PAIRS if a["category"]==c)
  b=f'''<div class=prose style="max-width:900px;padding-bottom:10px"><span class=mono style="color:var(--acc)">Ranked by public signals · not tested by us</span><h1>The best {e(c)} plugins for ChatGPT &amp; Codex</h1>
<p style="font-size:19px">{len(items)} plugins in our {e(c)} shelf ({e(BLURB.get(c,""))}), ordered by what we can actually measure: our editor's picks first, then GitHub stars{f" (checked {checked})" if checked else ""}. Archived repos go to the bottom.</p>
<p>{e(INTRO.get(c,""))}</p>
<p style="color:var(--mute)">Stars measure popularity, not quality or safety. We haven't installed or audited these; every description is the project's own. Read the code before you install anything. Paid placements never affect this order.</p>
{f"<p>Most-starred right now: <a href='../p/{top['slug']}.html'><b>{e(top['name'])}</b></a> by {e(top['maker'])}.</p>" if top else ""}
{f"<h3>Head-to-head</h3><ul class=where>{cmp}</ul>" if cmp else ""}<p><a href="../c/{slug(c)}.html">← Browse the {e(c)} shelf</a></p></div>
<div>{"".join(srow(p,i+1) for i,p in enumerate(items))}</div>'''
  open(f"{D}/best/{slug(c)}.html","w").write(layout(f"Best {c} plugins for ChatGPT & Codex ({len(items)} ranked) — PickAPlugin",b,1,f"The {len(items)} {c} plugins for ChatGPT and Codex in our catalog, ranked by editor's picks and GitHub stars. No paid ordering."))
for a,b2 in PAIRS:
  def cell(p): return f'<td style="padding:10px;vertical-align:top;border-bottom:1px solid var(--rule)">'
  rows=[("What it says it does",lambda p:e(p["description"])),("Maker",lambda p:e(p["maker"])),("GitHub stars",lambda p:fmt(stars(p))+(f' <span class=mono>(checked {p.get("stars_checked")})</span>' if p.get("stars_checked") else "")),
        ("Archived",lambda p:"Yes" if p.get("archived") else "No"),("Editor's pick",lambda p:"Yes — "+e(PICKS[p["slug"]]) if p["slug"] in PICKS else "No"),
        ("In our catalog since",lambda p:p["first_seen"]),("Source",lambda p:f'<a href="{e(p["link"])}" rel="nofollow noopener">{e(p["link"].replace("https://",""))}</a>'),("Our page",lambda p:f'<a href="../p/{p["slug"]}.html">{e(p["name"])} →</a>')]
  tbl="".join(f'<tr><th class=mono style="text-align:left;padding:10px;vertical-align:top;border-bottom:1px solid var(--rule);width:170px">{k}</th>{cell(a)}{f(a)}</td>{cell(b2)}{f(b2)}</td></tr>' for k,f in rows)
  more=a if stars(a)>=stars(b2) else b2
  body=f'''<div class=prose style="max-width:980px"><span class=mono style="color:var(--acc)">Compare · {e(a["category"])}</span><h1>{e(a["name"])} vs {e(b2["name"])}</h1>
<p style="font-size:19px">Two {e(a["category"])} plugins that describe overlapping jobs. Here's what each project says about itself and the public numbers, side by side.</p>
<table style="width:100%;border-collapse:collapse;border-top:3px solid var(--ink);margin-top:20px"><tr><th></th><th style="text-align:left;padding:10px;font:600 22px Fraunces,serif">{e(a["name"])}</th><th style="text-align:left;padding:10px;font:600 22px Fraunces,serif">{e(b2["name"])}</th></tr>{tbl}</table>
<h3>So which one?</h3><p>We haven't run both, so we won't pick a winner. On public signals, <b>{e(more["name"])}</b> has more GitHub stars, which tells you more people have looked at it, not that it's better for you. Read both READMEs, check recent commits, and read the code before installing.</p>
<p><a href="../best/{slug(a["category"])}.html">See every {e(a["category"])} plugin, ranked →</a></p></div>'''
  open(f"{D}/compare/{cslug(a,b2)}.html","w").write(layout(f"{a['name']} vs {b2['name']}: {a['category']} plugins compared — PickAPlugin",body,1,f"{a['name']} vs {b2['name']}: what each {a['category']} plugin for ChatGPT/Codex says it does, GitHub stars, maker and source, side by side."))
open(D+"/privacy.html","w").write(layout("Privacy — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Plain English</span><h1>Privacy</h1>
<p>PickAPlugin is a catalog of ChatGPT and Codex plugins, run by Aaron Houston. This page says what data the site touches and why. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h3>Browsing</h3><p>You don't need an account and we don't set cookies. We don't run ad trackers. The site is hosted on Cloudflare, which processes standard request data (like IP address, browser and the page requested) to serve and protect the site. Fonts load from Google Fonts, so Google sees those requests too. Links to plugin projects take you to GitHub or other sites with their own policies.</p>
<h3>Paying for a placement</h3><p>Paid placements (Featured, Top Spot, On the Belt, Category Sponsor, Verified badge, Expedited review) are paid through Stripe. Stripe collects your card details. We never see or store your full card number. We receive what Stripe shares with sellers: your name, email, billing country, what you bought, and the plugin URL you enter at checkout. We use it to set up your placement, contact you about it, and keep the records we need for tax and accounting. See <a href="https://stripe.com/privacy">Stripe's privacy policy</a>.</p>
<h3>Email</h3><p>If you email us, we keep the conversation so we can reply and follow up. We don't sell or share your email, and we don't add you to a mailing list without asking.</p>
<h3>Your choices</h3><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> to ask what we hold about you, to correct it, or to delete it. We keep payment records only as long as the law requires.</p>
<h3>Changes</h3><p>If this changes, we'll update this page. Last updated 2026-10-26.</p></div>"""))
open(D+"/terms.html","w").write(layout("Terms — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Plain English</span><h1>Terms</h1>
<p>PickAPlugin (pickaplugin.com) is run by Aaron Houston. By using the site or buying a placement, you agree to these terms. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h3>The catalog</h3><p>Listings come from public sources and each project's own description. We don't test, audit or endorse the plugins, and rankings use public signals like GitHub stars. Install anything at your own risk and read the code first. PickAPlugin isn't affiliated with, endorsed by, or sponsored by OpenAI. ChatGPT and Codex are trademarks of OpenAI, and project names belong to their owners. Makers can ask for corrections or removal at any time.</p>
<h3>Paid placements</h3><ul class=where><li>Payments go through Stripe. Monthly placements renew each month until you cancel.</li>
<li>Cancel anytime by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. Your placement stays up until the end of the period you've paid for. We don't give partial refunds for unused time.</li>
<li>Every paid placement is labelled. Payment never changes editor's picks, catalog order or the best-of rankings.</li>
<li>We can turn down or remove a placement for a plugin that's broken, malicious, misleading or illegal. If we turn you down, or your slot fills up before your payment lands, we refund you in full.</li>
<li>Expedited review buys a decision within 24 hours, not a yes. If we pass, you get a refund.</li>
<li>We don't promise any amount of traffic, clicks or installs.</li></ul>
<h3>No warranty</h3><p>The site is provided as is. To the extent the law allows, we aren't liable for losses from using it or from any plugin listed on it. Our total liability for a paid placement is limited to what you paid us for it.</p>
<h3>Changes</h3><p>We may update these terms and will post the changes here. Last updated 2026-10-26.</p></div>"""))
# ---- clean URLs, canonical, OG/Twitter, JSON-LD ----
def _url(rel):
  rel=rel.replace(os.sep,"/")
  if rel.endswith("index.html"): rel=rel[:-10]
  elif rel.endswith(".html"): rel=rel[:-5]
  return SITE+"/"+rel
def _fix(m,base):
  h=m.group(1)
  if _re.match(r"^(https?:|mailto:|#|data:)",h) or not (".html" in h): return m.group(0)
  path,_,frag=h.partition("#")
  p=_pp.normpath(_pp.join(base,path))
  if p.endswith("index.html"): p=p[:-10]
  elif p.endswith(".html"): p=p[:-5]
  return f'href="/{p.lstrip("./")}{"#"+frag if frag else ""}"'.replace('href="/"','href="/"')
URLS=[]
_N=len(PL) if "PL" in dir() else None
DESCS={"index.html":"Hundreds of ChatGPT and Codex plugins are scattered across GitHub. PickAPlugin gathers them in one free, hand-sorted catalog with last update, license and install command for each.",
 "about.html":"How PickAPlugin finds, sorts and lists ChatGPT and Codex plugins, what our editor's picks mean, and how paid placements are labelled.",
 "changelog.html":"Every change to the PickAPlugin catalog and site, generated from the git history at build time.",
 "advertise.html":"Advertise a ChatGPT or Codex plugin on PickAPlugin. Clearly labelled placements; paid spots never change the ranking order.",
 "submit.html":"Submit a ChatGPT or Codex plugin to the PickAPlugin catalog for free."}
_ORG={"@context":"https://schema.org","@type":"Organization","name":"PickAPlugin","url":SITE+"/","logo":SITE+"/og.png","sameAs":["https://x.com/PickAPlugin"]}
_ogsrc=os.path.join(ROOT,"launch","graphics","header.png")
if os.path.exists(_ogsrc): shutil.copy(_ogsrc,D+"/og.png")
for f in sorted(_glob.glob(D+"/**/*.html",recursive=True)):
  rel=os.path.relpath(f,D); base=_pp.dirname(rel.replace(os.sep,"/")); url=_url(rel); URLS.append(url)
  h=open(f).read()
  h=_re.sub(r'href="([^"]*)"',lambda m:_fix(m,base),h)
  h=h.replace('href="../style.css"','href="/style.css"').replace('href="style.css"','href="/style.css"')
  _dd=DESCS.get(rel)
  if _dd: h=_re.sub(r'<meta name=description content="[^"]*">','<meta name=description content="'+_dd+'">',h,1)
  t=_re.search(r"<title>(.*?)</title>",h).group(1); dm=_re.search(r'<meta name=description content="(.*?)">',h); d=dm.group(1) if dm else ""
  img=SITE+"/og.png"
  meta=(f'<link rel=canonical href="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="PickAPlugin">'
        f'<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:url" content="{url}">'
        f'<meta property="og:image" content="{img}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:site" content="@PickAPlugin">'
        f'<meta name="twitter:title" content="{t}"><meta name="twitter:description" content="{d}"><meta name="twitter:image" content="{img}">')
  if rel=="index.html":
    _pl=sorted(by.values(),key=lambda x:-(x.get("stars") or 0))[:50]
    for _o in (_ORG,{"@context":"https://schema.org","@type":"WebSite","name":"PickAPlugin","url":SITE+"/"},
               {"@context":"https://schema.org","@type":"ItemList","name":"ChatGPT and Codex plugins","numberOfItems":len(_pl),
                "itemListElement":[{"@type":"ListItem","position":i+1,"url":SITE+"/p/"+x["slug"],"name":x["name"]} for i,x in enumerate(_pl)]}):
      meta+='<script type="application/ld+json">'+_json.dumps(_o).replace("</","<\\/")+'</script>'
  if rel in ("about.html","changelog.html"):
    meta+='<script type="application/ld+json">'+_json.dumps(_ORG)+'</script>'
  if rel.startswith("p"+os.sep):
    p=by.get(_pp.basename(rel)[:-5])
    if p:
      ld={"@context":"https://schema.org","@type":"SoftwareApplication","name":p["name"],"description":p["description"],"url":url,
          "applicationCategory":"DeveloperApplication","operatingSystem":"Cross-platform","sameAs":p["link"],
          "author":{"@type":"Person" ,"name":p["maker"]} if p["maker"] else None,"isAccessibleForFree":True}
      ld={k:v for k,v in ld.items() if v is not None}
      meta+='<script type="application/ld+json">'+_json.dumps(ld).replace("</","<\\/")+'</script>'
      _bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"PickAPlugin","item":SITE+"/"},{"@type":"ListItem","position":2,"name":p["name"],"item":url}]}
      meta+='<script type="application/ld+json">'+_json.dumps(_bc).replace("</","<\\/")+'</script>'
  h=h.replace("</title>","</title>"+meta,1)
  open(f,"w").write(h)
open(D+"/robots.txt","w").write("User-agent: *\nAllow: /\n\nSitemap: "+SITE+"/sitemap.xml\n")
today=_dt.date.today().isoformat()
open(D+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in URLS)+"</urlset>\n")
_cats={}
for x in by.values(): _cats.setdefault(x["category"],[]).append(x)
_l=["# PickAPlugin","","> An independent, hand-sorted catalog of ChatGPT and Codex plugins collected from public GitHub sources. Free to browse. Not affiliated with OpenAI. Descriptions are each project's own; we do not test or audit plugins.","",
 "## Key pages",f"- [Home / catalog]({SITE}/)",f"- [How we pick]({SITE}/about)",f"- [Changelog]({SITE}/changelog)",f"- [Submit a plugin]({SITE}/submit)",f"- [Advertise]({SITE}/advertise)",f"- [Sitemap]({SITE}/sitemap.xml)",""]
for c in sorted(_cats):
  _l.append("## "+c)
  for x in sorted(_cats[c],key=lambda x:-(x.get("stars") or 0))[:15]: _l.append(f"- [{x['name']}]({SITE}/p/{x['slug']}): {x['description'][:160]}")
  _l.append("")
open(D+"/llms.txt","w").write("\n".join(_l))
open(f"{D}/{INDEXNOW_KEY}.txt","w").write(INDEXNOW_KEY)
print("seo:",len(URLS),"urls,",len(PAIRS),"comparisons")
