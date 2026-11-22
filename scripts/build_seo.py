# Executed at the end of build.py (shares its namespace: P, D, layout, e, slug, cats, PICKS, ...).
# Per-page title overrides from Search Console (one change per page; log each in launch/seo-log.md).
#
# Indexability rules (2026-11-21 thin-page cleanup). Do not reintroduce generated URL batches.
# INDEX: home, /p/*, /c/* (category hubs; old /best/<cat> 301 here), guides, real tool pages,
#   language/license pages that pass the gate, about, faq, research, blog articles, advertise,
#   submit, featured, mcp-server, privacy, terms, changelog, badge, the /compare hub, the
#   /alternatives directory page, languages, licenses, reports, newsletter, black-friday.
# NOINDEX (and omitted from the sitemap): thank-you/form pages (claimed, confirm, confirmed,
#   subscribed, unsubscribed, form-error).
# 301 via worker/index.js (and run_worker_first in wrangler.toml / upload_buckets.py):
#   /best/<cat> -> /c/<cat>
#   /compare/<a>-vs-<b> -> /compare
#   /alternatives/<slug> -> /p/<slug>
#   /best-for/<use> -> /compare
#   /tools/mcp-config-converter/<pair> -> /tools/mcp-config-converter
# lastmod only moves when a page's substantive content changes (see _sig below, commit 78f80ca).
# Writes /privacy, /terms, robots.txt, sitemap.xml, the IndexNow key file, then rewrites
# every page to clean URLs and adds canonical / Open Graph / JSON-LD tags.
import glob as _glob, posixpath as _pp, datetime as _dt, json as _json
SITE="https://pickaplugin.com"; INDEXNOW_KEY="6375d5cb89838413d1e117374c6ce038"
def fmt(n): return f"{n:,}" if n>=0 else "n/a"
def srow(p,i):
  tags=[]
  if p["slug"] in PICKS: tags.append("Editor's pick")
  if p.get("archived"): tags.append("Archived on GitHub")
  t=f' <span class=vchk style="color:var(--acc);border-color:var(--acc)">{" · ".join(tags)}</span>' if tags else ""
  return f'<a class=row href="../p/{p["slug"]}.html"><span class="no mono">#{i}</span><span><h3>{e(p["name"])}{t}</h3><p>{e((p["description"][:137]+"…") if len(p["description"])>140 else p["description"])}</p></span><span class="c mono">★ {fmt(stars(p))} · by {e(p["maker"])}</span></a>'

open(D+"/privacy.html","w").write(layout("Privacy — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Plain English</span><h1>Privacy</h1>
<p>PickAPlugin is a catalog of ChatGPT and Codex plugins, run by Aaron Houston. This page says what data the site touches and why. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h3>Browsing</h3><p>You don't need an account and we don't set cookies. We don't run ad trackers. The site is hosted on Cloudflare, which processes standard request data (like IP address, browser and the page requested) to serve and protect the site. Fonts load from Google Fonts, so Google sees those requests too. Links to plugin projects take you to GitHub or other sites with their own policies.</p>
<h3>Paying for a placement</h3><p>Paid placements (Featured, Top Spot, On the Belt, Category Sponsor, Verified badge, Expedited review) are paid through Stripe. Stripe collects your card details. We never see or store your full card number. We receive what Stripe shares with sellers: your name, email, billing country, what you bought, and the plugin URL you enter at checkout. We use it to set up your placement, contact you about it, and keep the records we need for tax and accounting. See <a href="https://stripe.com/privacy">Stripe's privacy policy</a>.</p>
<h3>Email</h3><p>If you email us, we keep the conversation so we can reply and follow up. We don't sell or share your email, and we don't add you to a mailing list without asking.</p>
<h3>Your choices</h3><p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> to ask what we hold about you, to correct it, or to delete it. We keep payment records only as long as the law requires.</p>
<h3>Changes</h3><p>If this changes, we'll update this page. Last updated 2026-10-26.</p></div>""",0,"What data PickAPlugin touches and why: no accounts or tracking cookies, Cloudflare and Google Fonts request data, and Stripe for paid placements."))
open(D+"/terms.html","w").write(layout("Terms — PickAPlugin",f"""<div class=prose><span class=mono style="color:var(--acc)">Plain English</span><h1>Terms</h1>
<p>PickAPlugin (pickaplugin.com) is run by Aaron Houston. By using the site or buying a placement, you agree to these terms. Questions: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h3>The catalog</h3><p>Listings come from public sources and each project's own description. We don't test, audit or endorse the plugins, and rankings use public signals like GitHub stars. Install anything at your own risk and read the code first. PickAPlugin isn't affiliated with, endorsed by, or sponsored by OpenAI. ChatGPT and Codex are trademarks of OpenAI, and project names belong to their owners. Makers can ask for corrections or removal at any time.</p>
<h3>Paid placements</h3><ul class=where><li>Payments go through Stripe. Monthly placements renew each month until you cancel.</li>
<li>Cancel anytime by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. Your placement stays up until the end of the period you've paid for. We don't give partial refunds for unused time.</li>
<li>Every paid placement is labelled. Payment never changes editor's picks, catalog order or the category rankings.</li>
<li>We can turn down or remove a placement for a plugin that's broken, malicious, misleading or illegal. If we turn you down, or your slot fills up before your payment lands, we refund you in full.</li>
<li>Expedited review buys a decision within 24 hours, not a yes. If we pass, you get a refund.</li>
<li>We don't promise any amount of traffic, clicks or installs.</li></ul>
<h3>No warranty</h3><p>The site is provided as is. To the extent the law allows, we aren't liable for losses from using it or from any plugin listed on it. Our total liability for a paid placement is limited to what you paid us for it.</p>
<h3>Changes</h3><p>We may update these terms and will post the changes here. Last updated 2026-10-26.</p></div>""",0,"Terms for using PickAPlugin and buying a labelled placement. We don't test or endorse listed plugins; install at your own risk."))
build_collections()
# ---- clean URLs, canonical, OG/Twitter, JSON-LD ----
def _url(rel):
  rel=rel.replace(os.sep,"/")
  if rel=="index.html": rel=""
  elif rel.endswith("/index.html"): rel=rel[:-11]
  elif rel.endswith(".html"): rel=rel[:-5]
  return SITE+"/"+rel
def _fix(m,base):
  h=m.group(1)
  if _re.match(r"^(https?:|mailto:|#|data:)",h) or not (".html" in h): return m.group(0)
  path,_,frag=h.partition("#")
  p=_pp.normpath(_pp.join(base,path))
  if p in ("index.html","./index.html"): p=""
  elif p.endswith("/index.html"): p=p[:-11]
  elif p.endswith(".html"): p=p[:-5]
  return f'href="/{p.lstrip("./")}{"#"+frag if frag else ""}"'.replace('href="/"','href="/"')
URLS=[]
# Real lastmod (2026-11-16, tightened 2026-11-18): a page's lastmod only moves when its substantive
# content changes. Signature = page text with scripts, the newspaper dateline, weekday/month names,
# digits (star counts, ISO dates, counters) and whitespace removed. The dateline in scripts/redesign.py
# is "Updated Wednesday, November 18, 2026" (today's typographic date on every page). Stripping digits
# alone left the weekday/month, so every daily build looked like a content change and stamped lastmod
# as today. State in data/lastmod.json; URLs whose signature changed in this run go to
# data/changed_urls.json, which indexnow.py submits by default (Bing asks for changed URLs only).
import hashlib as _hl
_PAGE_SIG={}
_WEEKDAY=r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
_MONTH=r"(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)"
def _sig(h):
  t=_re.sub(r"(?is)<script.*?</script>","",h)
  t=_re.sub(r'(?is)<div class="dl mono">.*?</div>',"",t)
  t=_re.sub(r"(?i)\b"+_WEEKDAY+r"\b","",t)
  t=_re.sub(r"(?i)\b"+_MONTH+r"\b","",t)
  t=_re.sub(r"\d+","",t); t=_re.sub(r"\s+"," ",t)
  return _hl.sha256(t.encode()).hexdigest()[:20]
exec(open(os.path.join(ROOT,"scripts","seo_overrides.py")).read())
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
  rel=os.path.relpath(f,D); base=_pp.dirname(rel.replace(os.sep,"/")); url=_url(rel)
  h=open(f).read()
  if 'name=robots content="noindex' not in h: URLS.append(url)
  h=_re.sub(r'href="([^"]*)"',lambda m:_fix(m,base),h)
  h=h.replace('href="../style.css"','href="/style.css"').replace('href="style.css"','href="/style.css"')
  _dd=DESCS.get(rel)
  if _dd: h=_re.sub(r'<meta name=description content="[^"]*">','<meta name=description content="'+_dd+'">',h,1)
  h=_apply_overrides(rel,h)
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
  if url in URLS: _PAGE_SIG[url]=_sig(h)
open(D+"/robots.txt","w").write("User-agent: *\nAllow: /\nDisallow: /go/\n\nSitemap: "+SITE+"/sitemap.xml\n")
today=_dt.date.today().isoformat()
_LMF=os.path.join(ROOT,"data","lastmod.json")
_LM=_json.load(open(_LMF)) if os.path.exists(_LMF) else {}
_seed=not _LM
_keep=os.environ.get("RESTORE_LASTMOD")=="1"
def _seed_date(u):
  k=u[len(SITE)+1:]
  if k.startswith("p/") and by.get(k[2:],{}).get("first_seen"): return min(by[k[2:]]["first_seen"][:10],today)
  if k.split("/")[0] in ("compare","alternatives","best-for") and "/" in k: return "2026-11-14"
  return COLL_LASTMOD.get(k) or today
_chg=[]
for _u,_sg in _PAGE_SIG.items():
  _old=_LM.get(_u)
  if not _old:
    _LM[_u]={"sig":_sg,"date":_seed_date(_u) if _seed else today}
    if not _seed: _chg.append(_u)
  elif _old["sig"]!=_sg:
    if _keep:
      _LM[_u]={"sig":_sg,"date":_old["date"]}
    else:
      _LM[_u]={"sig":_sg,"date":today}
      _chg.append(_u)
# Drop URLs that are no longer indexable (retired compare/alternatives pages, etc.).
_LM={u:d for u,d in _LM.items() if u in _PAGE_SIG}
_json.dump(dict(sorted(_LM.items())),open(_LMF,"w"),indent=0)
_chg=sorted(_chg)
_json.dump({"date":today,"urls":_chg},open(os.path.join(ROOT,"data","changed_urls.json"),"w"),indent=1)
print("seo: lastmod changed today:",len(_chg),"of",len(URLS),"(seed run)" if _seed else ("(sig-only restore)" if _keep else ""))
LASTMOD={u:_LM.get(u,{}).get("date",today) for u in URLS}
open(D+"/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{u}</loc><lastmod>{LASTMOD[u]}</lastmod></url>\n" for u in URLS)+"</urlset>\n")
_cats={}
for x in by.values(): _cats.setdefault(x["category"],[]).append(x)
_l=["# PickAPlugin","","> An independent, hand-sorted catalog of ChatGPT and Codex plugins collected from public GitHub sources. Free to browse. Not affiliated with OpenAI. Descriptions are each project's own; we do not test or audit plugins.","",
 "## Key pages",f"- [Home / catalog]({SITE}/)",f"- [How we pick]({SITE}/about)",f"- [Changelog]({SITE}/changelog)",f"- [Submit a plugin]({SITE}/submit)",f"- [MCP server: search this catalog from Claude, Cursor, Codex or VS Code]({SITE}/mcp-server) (endpoint {SITE}/mcp, JSON catalog {SITE}/catalog.json)",f"- [Advertise]({SITE}/advertise)",f"- [Sitemap]({SITE}/sitemap.xml)",f"- [FAQ]({SITE}/faq)",f"- [Alternatives / other directories]({SITE}/alternatives)",""]+["## Guides"]+[f"- [{h}]({SITE}/guides/{s}): {d}" for s,h,d in GUIDES]+["","## Articles",f"- [State of Codex Plugins 2026]({SITE}/research/state-of-codex-plugins-2026): original data on 339 plugin repos (CSV, CC BY 4.0)",f"- [Best Codex plugins (November 2026)]({SITE}/blog/best-codex-plugins-november-2026): top 3 maintained plugins per category, with install commands","","## MCP config conversions",f"- [MCP config converter]({SITE}/tools/mcp-config-converter): convert MCP server config between Claude, Codex, Cursor and VS Code","","## Free tools"]+[f"- [{h}]({SITE}/tools/{s}): {b}" for s,h,b in TOOLS]+[""]
for c in sorted(_cats):
  _l.append("## "+c)
  for x in sorted(_cats[c],key=lambda x:-(x.get("stars") or 0))[:15]: _l.append(f"- [{x['name']}]({SITE}/p/{x['slug']}): {x['description'][:160]}")
  _l.append("")
_l.insert(3,f"Full catalog for agents: {SITE}/llms-full.txt\n")
open(D+"/llms.txt","w").write("\n".join(_l))
_f=_l[:]
_f.append("# Full catalog\n")
for x in sorted(by.values(),key=lambda x:(x["category"],-(x.get("stars") or 0))):
  _f+= [f"## {x['name']}",f"- Page: {SITE}/p/{x['slug']}",f"- Source: {x['link']}",f"- Category: {x['category']}",f"- Maker: {x.get('maker') or 'unknown'}",f"- Stars: {x.get('stars')}  Last commit: {(x.get('pushed_at') or '')[:10]}  License: {x.get('license') or 'none'}  Language: {x.get('language') or 'n/a'}"+("  ARCHIVED" if x.get("archived") else ""),f"- What it does: {x['description']}"]+([f"- Install (from README): {x['install']}"] if x.get("install") else [])+[""]
open(D+"/llms-full.txt","w").write("\n".join(_f))
open(f"{D}/{INDEXNOW_KEY}.txt","w").write(INDEXNOW_KEY)
print("seo:",len(URLS),"indexable urls")
# Bing Webmaster verification (file + homepage meta)
import shutil as _sh
_sh.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)),"BingSiteAuth.xml"),D+"/BingSiteAuth.xml")
_hp=D+"/index.html"; _h=open(_hp).read()
_mv='<meta name="msvalidate.01" content="64C98C3E1DCFAFF92857E6DFEB8AE54D" />'
if _mv not in _h: open(_hp,"w").write(_h.replace("<head>","<head>\n"+_mv,1))
