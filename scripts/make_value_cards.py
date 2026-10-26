"""Render X graphics for @PickAPlugin (HTML -> PNG via playwright)."""
import base64,json,re,os,html,collections
from playwright.sync_api import sync_playwright
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)));G=f"{R}/launch/graphics";KIT=f"{R}/launch/x-kit.md"
P=json.load(open(f"{R}/data/plugins.json"));BY={p["slug"]:p for p in P}
def slug(c): return "".join(ch if ch.isalnum() else "-" for ch in c.lower()).replace("--","-").replace("--","-").strip("-")
CATS=collections.defaultdict(list)
for p in P: CATS[slug(p["category"])].append(p)
e=html.escape
U=lambda fn:'data:image/png;base64,'+base64.b64encode(open(f'{G}/{fn}','rb').read()).decode()
def oneline(d,n=165):
  s=re.split(r"(?<=[.;])\s",d.strip())[0].rstrip(".;")
  if len(s)<=n: return s
  return s[:n].rsplit(" ",1)[0].rstrip(",;:")+"…"
HEAD="""<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel=stylesheet>
<style>:root{--ink:#16130f;--paper:#f3efe6;--rule:#cfc6b4;--mute:#6b6457;--acc:#c8381e}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:'IBM Plex Sans'}
.mono{font-family:'IBM Plex Mono';letter-spacing:.08em;text-transform:uppercase}.f{font-family:Fraunces}i{font-style:normal;color:var(--acc)}</style>"""
LOGO="""<div style="width:400px;height:400px;background:var(--ink);display:flex;align-items:center;justify-content:center;position:relative">
<div style="width:300px;height:300px;border-radius:50%;border:3px solid var(--paper);display:flex;align-items:center;justify-content:center">
<span class=f style="font-weight:800;font-size:230px;line-height:1;color:var(--paper);margin-top:-18px;letter-spacing:-.04em">P<i style="font-size:230px">.</i></span></div></div>"""
HEADER="""<div style="width:1500px;height:500px;position:relative;overflow:hidden;border-bottom:6px double var(--ink)">
<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent 0 47px,#e6dfd0 47px 48px)"></div>
<div style="position:absolute;left:470px;right:70px;top:70px">
<div class=mono style="font-size:20px;color:var(--mute);border-bottom:2px solid var(--ink);padding-bottom:12px;display:flex;justify-content:space-between"><span>Vol. 1 · The catalog</span><span>343 plugins · 12 shelves</span></div>
<div class=f style="font-weight:800;font-size:148px;line-height:1;letter-spacing:-.03em;margin-top:26px">Pick<i>A</i>Plugin</div>
<div class=f style="font-size:38px;margin-top:20px">An independent catalog of <i>ChatGPT &amp; Codex</i> plugins</div>
<div class=mono style="font-size:24px;margin-top:30px;color:var(--acc);font-weight:500">pickaplugin.com →</div></div></div>"""
def card(kind,title,line,shelf,url,extra=""):
  return f"""<div style="width:1200px;height:675px;padding:56px 70px;display:flex;flex-direction:column;position:relative">
<div class=mono style="display:flex;justify-content:space-between;font-size:20px;border-bottom:2px solid var(--ink);padding-bottom:14px"><span class=f style="font-weight:800;font-size:30px;text-transform:none;letter-spacing:-.01em">Pick<i>A</i>Plugin</span><span style="color:var(--mute)">{e(kind)} · <span style="color:var(--acc)">{e(shelf)}</span></span></div>
<div class=f style="font-weight:800;font-size:{96 if len(title)<18 else 74}px;line-height:1.02;letter-spacing:-.025em;margin-top:52px">{e(title)}</div>
<div class=f style="font-size:36px;line-height:1.3;margin-top:26px;max-width:28em;border-left:5px solid var(--acc);padding-left:24px">{e(line)}</div>{extra}
<div style="margin-top:auto;display:flex;justify-content:space-between;align-items:end;border-top:3px double var(--ink);padding-top:16px"><span class=mono style="font-size:24px;font-weight:500;text-transform:none;letter-spacing:.02em">{e(url)}</span><span class=mono style="font-size:17px;color:var(--mute)">Free to browse</span></div></div>"""

def stat(rows,title,kicker):
  r="".join(f'<div style="display:flex;align-items:center;margin:5px 0"><div class=mono style="width:330px;font-size:22px;text-transform:none;letter-spacing:.01em">{e(a)}</div><div style="height:24px;width:{int(b/mx*640)}px;background:var(--acc)"></div><div class=f style="font-size:24px;font-weight:600;margin-left:14px">{b}</div></div>' for a,b in rows for mx in [max(x for _,x in rows)])
  return f"""<div style="width:1200px;height:675px;padding:50px 70px;display:flex;flex-direction:column">
<div class=mono style="display:flex;justify-content:space-between;font-size:20px;border-bottom:2px solid var(--ink);padding-bottom:14px"><span class=f style="font-weight:800;font-size:30px;text-transform:none">Pick<i>A</i>Plugin</span><span style="color:var(--mute)">{e(kicker)}</span></div>
<div class=f style="font-weight:800;font-size:50px;line-height:1.05;margin:18px 0 10px">{e(title)}</div>{r}
<div style="margin-top:auto;border-top:3px double var(--ink);padding-top:14px" class=mono><span style="font-size:20px;text-transform:none">pickaplugin.com · data: our catalog of 343 plugins</span></div></div>"""
C=collections.Counter(p["category"] for p in P)
J=[("v-shelves.png",stat([(k,v) for k,v in C.most_common() if k!="Other"],"Plugins per shelf","Catalog data")),
("v-pains.png",stat([("Memory & Context",C["Memory & Context"]),("Usage & Quotas",C["Usage & Quotas"]),("Security & Governance",C["Security & Governance"])],"What builders are fighting","Catalog data")),
("v-catalog.png",card("Catalog","343 plugins","Sorted by what they do. Every entry links to its source.","12 shelves","pickaplugin.com"))]
with sync_playwright() as pw:
  b=pw.chromium.launch();pg=b.new_page()
  for fn,h in J:
    pg.set_viewport_size({"width":1200,"height":675});pg.set_content(f"<html><head>{HEAD}</head><body>{h}</body></html>",wait_until="networkidle");pg.evaluate("document.fonts.ready");pg.screenshot(path=f"{G}/{fn}")
