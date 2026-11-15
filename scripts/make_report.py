#!/usr/bin/env python3
"""Monthly 'State of MCP & Codex Plugins' snapshot.
  python3 scripts/make_report.py 2026-11      # writes data/reports/2026-11.json
Re-run any time during the month (numbers are 'through <as_of>'); run once more on the 1st for the final month.
Sources: data/plugins.json now, and data/plugins.json as committed just before the month started (git history)
for the star baseline. The build (scripts/build_reports.py) renders /reports/<yyyy-mm> from the JSON."""
import json, os, sys, subprocess, datetime as dt, collections as cc
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
month=sys.argv[1] if len(sys.argv)>1 else dt.date.today().strftime("%Y-%m")
y,m=map(int,month.split("-")); start=dt.date(y,m,1); end=dt.date(y+(m==12),m%12+1,1)
def git(*a): return subprocess.run(["git",*a],cwd=ROOT,capture_output=True,text=True,check=True).stdout
P=json.load(open(os.path.join(ROOT,"data","plugins.json")))
base_commit=git("log","-1","--format=%H %cI","--before="+start.isoformat()+"T00:00:00-08:00","--","data/plugins.json").split()
B=json.loads(git("show",base_commit[0]+":data/plugins.json")) if base_commit else []
bs={p["slug"]:p for p in B}
asof=max((p.get("stars_checked") or "" for p in P),default=dt.date.today().isoformat())
asof=min(asof,(end-dt.timedelta(days=1)).isoformat())
def st(p): return p.get("stars") if isinstance(p.get("stars"),int) else None
def kind(p):
  i=(p.get("install") or "").lower()
  if "mcp add" in i: return "MCP server (mcp add)"
  if "/plugin" in i or "claude plugin" in i: return "Claude Code plugin"
  if "codex plugin" in i: return "Codex plugin"
  if "skills add" in i: return "Skills (npx skills add)"
  return "No install command in README"
new=[p for p in P if start.isoformat()<=p["first_seen"]<end.isoformat()]
live=[p for p in P if not p.get("archived")]
def days(p):
  try: return (dt.date.fromisoformat(asof)-dt.date.fromisoformat(p["pushed_at"][:10])).days
  except Exception: return None
growth=[]
for p in P:
  b=bs.get(p["slug"]); s1=st(p); s0=st(b) if b else None
  if s1 is not None and s0 is not None: growth.append({"slug":p["slug"],"name":p["name"],"category":p["category"],"maker":p["maker"],"from":s0,"to":s1,"gain":s1-s0,"pct":round(100*(s1-s0)/s0,1) if s0 else None})
weeks=cc.Counter()
for p in new:
  d=dt.date.fromisoformat(p["first_seen"]); wk=start+dt.timedelta(days=7*((d-start).days//7)); weeks[wk.isoformat()]+=1
def top(c,n=12): return [[k,v] for k,v in c.most_common(n)]
R={"month":month,"as_of":asof,"generated":dt.date.today().isoformat(),"complete":asof>=(end-dt.timedelta(days=1)).isoformat(),
 "baseline_commit":base_commit[0][:7] if base_commit else None,"baseline_date":base_commit[1][:10] if base_commit else None,
 "catalog_start":len(B),"catalog_now":len(P),"new_count":len(new),
 "new_by_category":top(cc.Counter(p["category"] for p in new)),
 "catalog_by_category":top(cc.Counter(p["category"] for p in P)),
 "new_by_week":sorted([[k,v] for k,v in weeks.items()]),
 "new_by_license":top(cc.Counter(p.get("license") or "No license file" for p in new)),
 "new_by_language":top(cc.Counter(p.get("language") or "n/a" for p in new),8),
 "new_by_packaging":top(cc.Counter(kind(p) for p in new)),
 "catalog_by_packaging":top(cc.Counter(kind(p) for p in P)),
 "new_with_stars":sum(1 for p in new if st(p) is not None),
 "new_median_stars":sorted(st(p) for p in new if st(p) is not None)[len([p for p in new if st(p) is not None])//2] if any(st(p) is not None for p in new) else None,
 "pushed_7d":sum(1 for p in live if (days(p) is not None and days(p)<=7)),"pushed_30d":sum(1 for p in live if (days(p) is not None and days(p)<=30)),
 "live_with_push_data":sum(1 for p in live if days(p) is not None),
 "archived":sum(1 for p in P if p.get("archived")),
 "stars_tracked":len(growth),"stars_total_start":sum(g["from"] for g in growth),"stars_total_now":sum(g["to"] for g in growth),
 "gained_any":sum(1 for g in growth if g["gain"]>0),"lost_any":sum(1 for g in growth if g["gain"]<0),
 "fastest_abs":sorted(growth,key=lambda g:-g["gain"])[:10],
 "fastest_pct":sorted([g for g in growth if g["from"]>=25],key=lambda g:-(g["pct"] or 0))[:10],
 "notable_new":[{"slug":p["slug"],"name":p["name"],"category":p["category"],"maker":p["maker"],"stars":st(p),"first_seen":p["first_seen"],"license":p.get("license"),"description":p["description"]} for p in sorted(new,key=lambda p:-(st(p) or -1))[:12]],
 "license_share_catalog":top(cc.Counter(p.get("license") or "No license file" for p in P),6)}
os.makedirs(os.path.join(ROOT,"data","reports"),exist_ok=True)
json.dump(R,open(os.path.join(ROOT,"data","reports",month+".json"),"w"),indent=1)
print("report",month,"as of",asof,":",len(new),"new,",len(growth),"star-tracked; baseline",R["baseline_commit"],R["baseline_date"])
