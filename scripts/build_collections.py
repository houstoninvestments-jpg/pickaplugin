# Programmatic SEO collection pages: /language/<slug> and /license/<slug>.
# Exec'd by build.py right after `by=` (defines the gate); build_seo.py calls build_collections().
# ONE gate per family (resolve_indexable) feeds the route (file exists or not), the sitemap,
# the hub, related links and the chips on plugin pages. Below the gate = no file = 404.
import statistics as _st, datetime as _cdt, json as _cj
COLL_MIN=3
LANG_ALIAS={"c#":"csharp","c++":"cpp","f#":"fsharp","javascript":"javascript","js":"javascript","typescript":"typescript","ts":"typescript","golang":"go"}
LIC_ALIAS={"mit license":"mit","apache 2.0":"apache-2.0","apache-2":"apache-2.0"}
FAMILIES={
 "language":{"field":"language","hub":"languages","alias":LANG_ALIAS,"noun":"written in"},
 "license":{"field":"license","hub":"licenses","alias":LIC_ALIAS,"noun":"under"},
}
LIC_NOTE={"mit":"MIT is a short permissive license: you can use, change and ship the code, as long as you keep the copyright notice.",
 "apache-2-0":"Apache-2.0 is permissive like MIT, but it also includes an explicit patent grant and asks you to note changes you make.",
 "agpl-3-0":"AGPL-3.0 is copyleft: if you modify the code and let people use it over a network, you have to share your changes under the same license.",
 "gpl-3-0":"GPL-3.0 is copyleft: if you distribute a modified version, it has to stay GPL too."}
def coll_slug(fam,val):
  k=(val or "").strip().lower()
  return FAMILIES[fam]["alias"].get(k) or slug(k)
def resolve_indexable(fam,plugins=None,min_n=COLL_MIN):
  """slug -> {label, items}. Aliases are folded before counting. The only gate for this family."""
  f=FAMILIES[fam]["field"]; groups={}
  for p in (plugins if plugins is not None else P):
    v=p.get(f)
    if not v: continue
    s=coll_slug(fam,v); g=groups.setdefault(s,{"labels":{},"items":[]})
    g["labels"][v]=g["labels"].get(v,0)+1; g["items"].append(p)
  out={}
  for s,g in groups.items():
    if len(g["items"])>=min_n:
      out[s]={"label":max(g["labels"],key=g["labels"].get),"items":g["items"]}
  return dict(sorted(out.items(),key=lambda kv:(-len(kv[1]["items"]),kv[0])))
GATED={fam:resolve_indexable(fam) for fam in FAMILIES}
def coll_href(fam,val,depth=1):
  """Chip link for a plugin page, or None if the term doesn't pass the gate."""
  s=coll_slug(fam,val)
  return ("../"*depth)+f"{fam}/{s}.html" if s in GATED[fam] else None
COLL_LASTMOD={}
def build_collections():
  today=_cdt.date.today()
  def _ld(o): return '<script type="application/ld+json">'+_cj.dumps(o).replace("</","<\\/")+'</script>'
  for fam,cfg in FAMILIES.items():
    g=GATED[fam]; hub=cfg["hub"]; shutil.rmtree(f"{D}/{fam}",ignore_errors=True); os.makedirs(f"{D}/{fam}",exist_ok=True)
    famname="Language" if fam=="language" else "License"
    for s,info in g.items():
      items=sorted(info["items"],key=rankkey); info["items"]=items; lab=info["label"]; n=len(items)
      st=[stars(p) for p in items if stars(p)>=0]; med=int(_st.median(st)) if st else None
      recent=sum(1 for p in items if p.get("pushed_at") and (today-_cdt.date.fromisoformat(p["pushed_at"])).days<=30)
      arch=sum(1 for p in items if p.get("archived"))
      cc={}
      for p in items: cc[p["category"]]=cc.get(p["category"],0)+1
      topc=sorted(cc.items(),key=lambda kv:-kv[1])[:3]
      names=[p["name"] for p in items[:3]]
      checked=max((p.get("stars_checked","") for p in items),default="")
      lm=max(max(p.get("first_seen",""),p.get("pushed_at") or "") for p in items); COLL_LASTMOD[f"{fam}/{s}"]=lm
      what=(f"{n} plugins written mostly in {lab}" if fam=="language" else f"{n} plugins released under {lab}")
      share=round(100*n/len(P))
      intro=(f"We list {what}, about {share}% of our {len(P)}-plugin catalog. They're ordered by editor's picks, then GitHub stars"
             +(f" (checked {checked})" if checked else "")+"."
             +(f" The median one has {med:,} stars" if med is not None else "")
             +(f", and {recent} of them got a push in the last 30 days." if med is not None else f" {recent} got a push in the last 30 days."))
      intro2=f"Most-starred: {', '.join(e(x) for x in names)}. Biggest shelves here: "+", ".join(f"{e(c)} ({k})" for c,k in topc)+"."
      if arch: intro2+=f" {arch} {'is' if arch==1 else 'are'} archived on GitHub and sit at the bottom."
      lang_note=("The language is what GitHub detects as the repo's main one, so a plugin can still ship scripts in other languages." if fam=="language" else LIC_NOTE.get(s,""))
      faq=[(f"How many {lab} plugins are on PickAPlugin?",f"{n} plugins in our catalog are {'written mostly in' if fam=='language' else 'released under'} {lab}, as of {checked or today.isoformat()}."),
           (f"What's the most popular {lab} plugin for ChatGPT or Codex?",f"By GitHub stars it's {items[0]['name']} by {items[0]['maker']}"+(f", with {stars(items[0]):,} stars." if stars(items[0])>=0 else ".") if not items[0]["slug"] in PICKS else f"Our editor's pick {items[0]['name']} by {items[0]['maker']} is listed first; after picks, plugins are ordered by GitHub stars."),
           ("How is this list ranked?","Editor's picks first, then GitHub stars, with archived repos last. Paid placements don't change the order, and we haven't tested these plugins ourselves."),
           ("Why don't some " + ("languages" if fam=="language" else "licenses") + " have a page?",f"We only make a page when at least {COLL_MIN} plugins share it. Smaller groups are still in the main catalog.")]
      rel=[(k,v) for k,v in g.items() if k!=s][:8]
      relhtml=" · ".join(f'<a href="{k}.html">{e(v["label"])} ({len(v["items"])})</a>' for k,v in rel)
      body=f'''<div class=prose style="max-width:900px;padding-bottom:10px"><span class=mono style="color:var(--acc)"><a href="../index.html">Home</a> / <a href="../{hub}.html">{famname}s</a> / {e(lab)}</span><h1>{e(lab)} plugins for ChatGPT &amp; Codex</h1>
<p style="font-size:19px">{intro}</p><p>{intro2}</p>{f"<p>{e(lang_note)}</p>" if lang_note else ""}
<p style="color:var(--mute)">Stars measure popularity, not quality or safety. Descriptions are each project's own. Read the code before you install anything.</p>
{f"<p class=mono>Other {famname.lower()}s: {relhtml}</p>" if relhtml else ""}</div>
<div>{"".join(srow(p,i+1) for i,p in enumerate(items))}</div>
<div class=prose style="max-width:900px"><h3>Questions</h3>{"".join(f"<p><b>{e(q)}</b><br>{e(a)}</p>" for q,a in faq)}</div>'''
      title=f"{n} {lab} ChatGPT & Codex Plugins ({today.year})"
      if len(title)>60: title=f"{n} {lab} Codex Plugins ({today.year})"
      url=f"{SITE}/{fam}/{s}"
      ld=_ld({"@context":"https://schema.org","@type":"CollectionPage","name":title,"url":url,"description":intro})+_ld({"@context":"https://schema.org","@type":"ItemList","numberOfItems":n,"itemListElement":[{"@type":"ListItem","position":i+1,"url":SITE+"/p/"+p["slug"],"name":p["name"]} for i,p in enumerate(items)]})\
        +_ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"PickAPlugin","item":SITE+"/"},{"@type":"ListItem","position":2,"name":famname+"s","item":f"{SITE}/{hub}"},{"@type":"ListItem","position":3,"name":lab,"item":url}]})\
        +_ld({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
      h=layout(title,body,1,f"{intro[:150].rsplit(' ',1)[0]}.")
      open(f"{D}/{fam}/{s}.html","w").write(h.replace("</head>",ld+"</head>",1))
    # hub
    rows="".join(f'<a class=row href="{fam}/{s}.html"><span class="no mono">{len(v["items"])}</span><span><h3>{e(v["label"])}</h3><p>Most-starred: {", ".join(e(p["name"]) for p in v["items"][:3])}</p></span><span class="c mono">{len(v["items"])} plugins</span></a>' for s,v in g.items())
    tot=sum(len(v["items"]) for v in g.values())
    unk=sum(1 for p in P if not p.get(cfg["field"]))
    htitle=f"ChatGPT & Codex Plugins by {famname} ({today.year})"
    hb=f'''<div class=prose style="max-width:900px;padding-bottom:10px"><span class=mono style="color:var(--acc)"><a href="index.html">Home</a> / {famname}s</span><h1>Plugins by {famname.lower()}</h1>
<p style="font-size:19px">{len(g)} {famname.lower()}s cover {tot} of our {len(P)} plugins. {g[next(iter(g))]["label"]} leads with {len(next(iter(g.values()))["items"])}. {unk} plugins don't list a {"main language" if fam=="language" else "license"} on GitHub, and {famname.lower()}s with fewer than {COLL_MIN} plugins don't get their own page.</p></div><div>{rows}</div>'''
    hld=_ld({"@context":"https://schema.org","@type":"CollectionPage","name":htitle,"url":f"{SITE}/{hub}"})+_ld({"@context":"https://schema.org","@type":"ItemList","numberOfItems":len(g),"itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{SITE}/{fam}/{s}","name":v["label"]} for i,(s,v) in enumerate(g.items())]})\
      +_ld({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"PickAPlugin","item":SITE+"/"},{"@type":"ListItem","position":2,"name":famname+"s","item":f"{SITE}/{hub}"}]})
    open(f"{D}/{hub}.html","w").write(layout(htitle,hb,0,f"Browse {tot} ChatGPT and Codex plugins by {famname.lower()}: {', '.join(v['label'] for v in list(g.values())[:4])} and more.").replace("</head>",hld+"</head>",1))
    COLL_LASTMOD[hub]=max(COLL_LASTMOD[f"{fam}/{s}"] for s in g)
