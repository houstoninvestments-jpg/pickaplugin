#!/usr/bin/env python3
"""Re-crawl public sources and update data/plugins.json. Never invents entries:
every record is parsed from a source list. Keeps first_seen dates across runs."""
import json, re, urllib.request, datetime, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = [("awesome-codex-plugins",
  "https://raw.githubusercontent.com/hashgraph-online/awesome-codex-plugins/main/README.md",
  "https://github.com/hashgraph-online/awesome-codex-plugins")]
CATS = [  # (category, weighted regexes). Highest score wins; ties go to earlier rows.
 ("Security & Governance",[r"\bsecurity\b",r"secret",r"pentest",r"bounty",r"vulnerab",r"governance",r"\bpolicy\b",r"\bctf",r"burp"]),
 ("Usage & Quotas",[r"quota",r"usage limit",r"rate limit",r"token usage",r"\busage\b",r"resets?\b"]),
 ("Review & Testing",[r"\btests?\b",r"\btdd\b",r"\bqa\b",r"code review",r"reviewer",r"\blint",r"verif",r"acceptance"]),
 ("Memory & Context",[r"memory",r"\bcontext\b",r"sessions?\b",r"knowledge graph",r"briefing",r"recall"]),
 ("Messaging & Remote",[r"telegram",r"discord",r"slack",r"iphone",r"\bphone\b",r"\bsms\b",r"\bcalls?\b",r"webhook"]),
 ("Design & Frontend",[r"\bdesign",r"\bcss\b",r"\bui\b",r"frontend",r"\breact\b",r"\bimage",r"sticker",r"\bgif\b",r"terminal ui"]),
 ("Docs, Content & SEO",[r"\bpdf",r"translat",r"\bwrit",r"\bseo\b",r"transcript",r"youtube",r"obsidian",r"\bnotes?\b"]),
 ("Data & Backend",[r"database",r"postgres",r"sql",r"\bdbt\b",r"analytics",r"backend",r"observability",r"telemetry"]),
 ("Deploy & DevOps",[r"deploy",r"hosting",r"docker",r"kubernetes",r"coolify",r"\bpublish",r"bitbucket",r"\bgit\b",r"devops",r"subdomain"]),
 ("Industry Tools",[r"autocad",r"hvac",r"\bcourt",r"legal",r"car rental",r"\bvin",r"contam",r"modding",r"business analysis",r"candidates",r"calendar"]),
 ("Agent Workflows",[r"orchestrat",r"multi-agent",r"workflow",r"pipeline",r"specialist",r"\bsdlc\b",r"spec-",r"\bplanning\b",r"agents?\b"]),
]
OVERRIDES = {  # manual fixes where keyword rules misfire
 "aegis":"Agent Workflows","boss":"Agent Workflows","codex-seo":"Docs, Content & SEO","codex-rg-guard":"Usage & Quotas",
 "data-product-builder-for-dbt":"Data & Backend","contam-tools":"Industry Tools","bgs-modding-superpowers":"Industry Tools",
 "car-rental-business-skills":"Industry Tools","clera":"Industry Tools","burpsuite-mcp-bridge":"Security & Governance",
 "darkmoon":"Security & Governance","damnpdfs":"Docs, Content & SEO","alcove":"Memory & Context","codex-how-to":"Agent Workflows",
 "chatgpt-agent":"Review & Testing","agent-harness-skills":"Agent Workflows","computer-usage-summary":"Data & Backend",
 "aiboarding":"Agent Workflows","aident-loadout":"Agent Workflows","codex-tools-bridge":"Agent Workflows","cometchat":"Messaging & Remote",
}
def cat(t, s=""):
  if s in OVERRIDES: return OVERRIDES[s]
  best,score="Other",0
  for n,pats in CATS:
    sc=sum(len(re.findall(p,t,re.I)) for p in pats)
    if sc>score: best,score=n,sc
  return best
def slug(s): return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")
INSTALL_RX=re.compile(r"^\s*\$?\s*((?:codex|claude)\s+(?:plugin|plugins|mcp)\s+(?:install|add|marketplace add)\s+\S.*|/plugin\s+(?:install|marketplace add)\s+\S.*|npx\s+(?:-y\s+)?skills\s+add\s+\S.*)$")
def install_cmd(readme, link):
  """Return an install command copied verbatim from a fenced code block in the README, or None. Never synthesized."""
  for blk in re.findall(r"```[^\n]*\n(.*?)```", readme, re.S):
    for line in blk.splitlines():
      m=INSTALL_RX.match(line)
      if m and len(m.group(1))<160 and "<" not in m.group(1): return m.group(1).strip()
  return None
def add_stars(out, old):
  """Real GitHub star counts via GraphQL (needs GITHUB_TOKEN or GH_TOKEN). Keeps old values if unavailable."""
  for s,p in out.items():
    for k in ("stars","stars_checked","archived"):
      if k in old.get(s,{}) and k not in p: p[k]=old[s][k]
    for k in ("pushed_at","license","language","install"):
      if k in old.get(s,{}) and k not in p: p[k]=old[s][k]
  tok=os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
  if not tok:
    try:
      import subprocess; tok=subprocess.run(["gh","auth","token"],capture_output=True,text=True,timeout=10).stdout.strip()
    except Exception: tok=""
  if not tok: print("no GitHub token: star counts not refreshed"); return
  items=[]
  for s,p in out.items():
    m=re.match(r"https://github\.com/([^/]+)/([^/#?]+)",p["link"])
    if m: items.append((s,m.group(1),m.group(2).removesuffix(".git")))
  today=datetime.date.today().isoformat(); n=0
  for i in range(0,len(items),25):
    chunk=items[i:i+25]
    q="query{"+" ".join(f'r{j}:repository(owner:{json.dumps(o)},name:{json.dumps(r)}){{stargazerCount isArchived pushedAt licenseInfo{{spdxId name}} primaryLanguage{{name}} rm:object(expression:\"HEAD:README.md\"){{... on Blob{{text}}}}}}' for j,(_,o,r) in enumerate(chunk))+"}"
    try:
      req=urllib.request.Request("https://api.github.com/graphql",json.dumps({"query":q}).encode(),{"Authorization":"bearer "+tok,"Content-Type":"application/json"})
      d=json.load(urllib.request.urlopen(req,timeout=60)).get("data") or {}
    except Exception as ex: print("star fetch failed:",ex); continue
    for j,(s,_,_) in enumerate(chunk):
      r=d.get(f"r{j}")
      if r:
        p=out[s]; p["stars"]=r["stargazerCount"]; p["archived"]=r["isArchived"]; p["stars_checked"]=today; n+=1
        p["pushed_at"]=(r.get("pushedAt") or "")[:10] or None
        li=r.get("licenseInfo") or {}; p["license"]=(li.get("spdxId") if li.get("spdxId") not in (None,"NOASSERTION") else None)
        p["language"]=(r.get("primaryLanguage") or {}).get("name")
        p["install"]=install_cmd(((r.get("rm") or {}).get("text") or ""), p["link"])
  print(f"stars refreshed for {n}/{len(items)} repos")
def main():
  path=os.path.join(ROOT,"data","plugins.json")
  old={p["slug"]:p for p in json.load(open(path))} if os.path.exists(path) else {}
  today=datetime.date.today().isoformat(); out={}
  for name,url,home in SOURCES:
    md=urllib.request.urlopen(url,timeout=30).read().decode()
    m=re.search(r"## Official Plugins(.*?)## Plugin Development",md,re.S)
    sec="Official list"
    for line in m.group(1).splitlines():
      if line.startswith("## Community"): sec="Community list"
      r=re.match(r"- \[(.+?)\]\((https?://[^)]+)\)\s*[-–—]\s*(.+)",line)
      if not r: continue
      n,link,desc=r.groups()
      mk=re.match(r"https://github\.com/([^/]+)",link)
      s=slug(n)
      if s in out: continue
      out[s]={"slug":s,"name":n,"description":desc.strip(),"maker":mk.group(1) if mk else "",
        "link":link,"category":cat(n+" "+desc, s),"source":name,"source_url":home,"source_section":sec,
        "first_seen":old.get(s,{}).get("first_seen",today),"featured":old.get(s,{}).get("featured",False)}
  for s,p in out.items():  # keep fulfillment fields (featured_sub, featured_since...)
    for k,v in old.get(s,{}).items():
      if k.startswith(("featured_","top_spot","belt","verified","sponsor_")): p[k]=v
  for s,p in old.items():  # paid listings added by fulfill.py aren't in any source list
    if s not in out and p.get("source")=="featured-order": out[s]=p
  add_stars(out, old)
  data=sorted(out.values(),key=lambda p:p["name"].lower())
  json.dump(data,open(path,"w"),indent=1,ensure_ascii=False)
  print(f"{len(data)} plugins written ({len(set(out)-set(old))} new)")
if __name__=="__main__": main()
