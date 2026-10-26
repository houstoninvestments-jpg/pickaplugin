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
# parse kit
posts=[];day=None;cur=None
for ln in open(KIT).read().split("## 3.")[0].splitlines():
  m=re.match(r"### Day (\d+)",ln)
  if m: day=int(m[1]);continue
  m=re.match(r"\*\*(\d+)\.\*\*",ln)
  if m and day: cur={"day":day,"n":int(m[1]),"links":[]};posts.append(cur)
  if cur: cur["links"]+=re.findall(r"pickaplugin\.com/([pc])/([a-z0-9-]+)",ln)
jobs=[]
for p in posts:
  L=[l for l in p["links"] if l[0]=="p" and l[1] in BY] or [l for l in p["links"] if l[0]=="c" and l[1] in CATS]
  if not L: continue
  k,s=L[0];fn=f"day{p['day']:02d}-post{p['n']}.png"
  if k=="p":
    x=BY[s];h=card("Plugin",x["name"],oneline(x["description"]),x["category"],f"pickaplugin.com/p/{s}")
  else:
    items=CATS[s];c=items[0]["category"];names=" · ".join(e(i["name"]) for i in items[:4])
    h=card("Shelf",c,f"{len(items)} {c} plugins for ChatGPT & Codex, hand-sorted.",f"{len(items)} plugins",f"pickaplugin.com/c/{s}",
      f'<div class=mono style="font-size:19px;color:var(--mute);margin-top:30px;text-transform:none;letter-spacing:.02em">On this shelf: {names} …</div>')
  p["img"]=fn;jobs.append((fn,h,1200,675,p,k,s))
with sync_playwright() as pw:
  b=pw.chromium.launch();pg=b.new_page()
  def shot(fn,body,w,h):
    pg.set_viewport_size({"width":w,"height":h});pg.set_content(f"<html><head>{HEAD}</head><body>{body}</body></html>",wait_until="networkidle")
    pg.evaluate("document.fonts.ready");pg.screenshot(path=f"{G}/{fn}")
  shot("logo.png",LOGO,400,400);shot("header.png",HEADER,1500,500)
  for fn,h,w,hh,*_ in jobs: shot(fn,h,w,hh)
  thumbs="".join(f'<img src="{U(j[0])}" style="width:380px;border:1px solid #16130f">' for j in jobs[:9])
  pg.set_viewport_size({"width":1240,"height":1400})
  pg.goto("about:blank");pg.set_content(f"<html><head>{HEAD}</head><body style='padding:20px'><div style='display:flex;gap:20px;align-items:center'><img src='{U("logo.png")}' style='width:180px;border-radius:50%'><img src='{U("header.png")}' style='width:1000px'></div><div style='display:grid;grid-template-columns:repeat(3,380px);gap:20px;margin-top:20px'>{thumbs}</div></body></html>",wait_until="networkidle")
  pg.screenshot(path=f"{G}/contact.png",full_page=True);b.close()
# index + kit annotations
with open(f"{G}/index.md","w") as f:
  f.write("# @PickAPlugin graphics\n\n- logo.png: 400x400 avatar\n- header.png: 1500x500 header\n- contact.png: contact sheet\n\n| Post | Image | Links to |\n|---|---|---|\n")
  for fn,_,_,_,p,k,s in jobs: f.write(f"| Day {p['day']} post {p['n']} | {fn} | pickaplugin.com/{k}/{s} |\n")
t=open(KIT).read();out=[];day=None;pend=None
done={(p["day"],p["n"]):p.get("img") for p in posts}
for ln in t.splitlines():
  m=re.match(r"### Day (\d+)",ln)
  if m: day=int(m[1])
  m2=re.match(r"\*\*(\d+)\.\*\*",ln)
  if (m or m2 or ln.startswith("## ")) and pend: out.append(f"_Image: launch/graphics/{pend}_\n");pend=None
  if m2 and day: pend=done.get((day,int(m2[1])))
  if ln.startswith("_Image:"): continue
  out.append(ln)
open(KIT,"w").write(re.sub(r"\n{3,}","\n\n","\n".join(out))+"\n")
print(len(jobs),"cards")
