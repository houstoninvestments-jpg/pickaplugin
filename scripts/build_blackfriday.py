# Executed by build.py before build_seo.py. Writes /black-friday from data/black_friday.json.
# Only add a deal after checking it on the vendor's own page. Each deal: name, what, offer, ends, url, checked.
import json as _bj
_BF=_bj.load(open(os.path.join(ROOT,"data","black_friday.json")))
_ck=_BF["checked"]; _deals=_BF["deals"]
def _bfdate(s):
  import datetime as _d; return _d.date.fromisoformat(s).strftime("%b %-d, %Y")
if _deals:
  _dl='<div style="border-top:3px solid var(--ink)">'+"".join(f'<a class=row href="{e(d["url"])}" rel=nofollow><span><h3>{e(d["name"])}: {e(d["offer"])}</h3><p>{e(d["what"])}. Ends {e(d.get("ends","when the vendor says"))}. Checked {_bfdate(d["checked"])} on the vendor\'s page.</p></span></a>' for d in _deals)+'</div>'
else:
  _dl=f'''<div class=prose style="border:1px solid var(--ink);background:#fffdf8;padding:14px 18px;margin:14px 0"><p style="margin:0"><b>Nothing verified yet.</b> As of {_bfdate(_ck)}, none of the AI coding tools, MCP tools or paid plugins we track has announced a 2026 Black Friday offer on its own site. Most vendors announce in mid to late November. We'll add deals as they go live, each with a link to the vendor's page and the date we checked it.</p></div>'''
_wl="".join(f'<li><a href="{e(u)}" rel=nofollow>{e(n)}</a>: {e(w)}</li>' for n,w,u in _BF["watch"])
_qa=[("When is Black Friday 2026?","Friday, November 27, 2026. Cyber Monday is November 30."),
 ("Do ChatGPT Plus or Claude Pro go on sale for Black Friday?","Historically, no. The model makers haven't run Black Friday discounts on their consumer plans. Deals tend to come from tools built on top of them."),
 ("Are the plugins on PickAPlugin free?","Most plugins in the catalog are open source and free to install. This page is for paid tools and paid plugins that run a real discount."),
 ("How do I get my deal listed?",f"Email {EMAIL} with the offer, the end date and a link to the page where it's shown. We check it on your site before it goes up. Listing a real deal is free.")]
_bfbody=f'''{TCSS}<div class=prose style="max-width:900px"><span class=mono style="color:var(--acc)">Black Friday 2026 · last checked {_bfdate(_ck)}</span>
<h1>Black Friday 2026 deals on AI coding tools, ChatGPT and Codex plugins</h1>
<p style="font-size:19px">Real discounts only. Every deal here gets checked on the maker's own page, with a link and the date we looked. No coupon spam, no "ends in 3 hours" countdowns.</p>
<h2>Verified deals</h2>{_dl}
<h2>Tools we're watching</h2><p>These are the paid AI coding and dev tools people ask us about most. None has a 2026 Black Friday deal yet. The links go to their normal pricing pages, so you'll know the regular price if a deal does show up.</p><ul class=where>{_wl}</ul>
<h2>Make a plugin or dev tool? Send us your deal</h2>
<p>If you're running a Black Friday or Cyber Monday offer on a ChatGPT or Codex plugin, an MCP server, or a dev tool, email <a href="mailto:{EMAIL}?subject=Black%20Friday%20deal">{EMAIL}</a> with the offer, the dates and the link. It's free to list, we just check it's real first.</p>
<p>Want more eyes on it? A <a href="featured.html">featured spot</a> pins your plugin above its category for the month ($49/mo, labelled as paid). Not on PickAPlugin yet? <a href="submit.html">List it free</a>.</p>
{_faq_html(_qa)}
<p><a href="index.html#catalog">← Browse all {len(P)} plugins</a> · <a href="tools/index.html">Free tools</a></p></div>
{_faq_ld(_qa)}<script type="application/ld+json">{_bj.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"Black Friday 2026 deals on AI coding tools, ChatGPT and Codex plugins","url":SITE_URL+"/black-friday","dateModified":_ck,"isPartOf":{"@type":"WebSite","name":"PickAPlugin","url":SITE_URL+"/"},"mainEntity":{"@type":"ItemList","name":"Verified Black Friday 2026 deals","numberOfItems":len(_deals),"itemListElement":[{"@type":"ListItem","position":i+1,"name":d["name"]+": "+d["offer"],"url":d["url"]} for i,d in enumerate(_deals)]}}).replace("</","<\\/")}</script>'''
open(D+"/black-friday.html","w").write(layout("Black Friday 2026 deals on AI coding tools, ChatGPT & Codex plugins — PickAPlugin",_bfbody,0,
 "Verified Black Friday 2026 deals on AI coding tools, MCP and dev tools, and paid ChatGPT and Codex plugins. Each deal links to its source with the date we checked it."))
print("black-friday: deals",len(_deals))
