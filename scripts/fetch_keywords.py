#!/usr/bin/env python3
"""Pull free Google + Bing autocomplete suggestions for comparison/alternatives/use-case keywords.
Writes data/keywords.json (cached; the build reads it, never the network). Re-run weekly-ish:
  python3 scripts/fetch_keywords.py            # top plugins + use-case seeds
No paid APIs: suggestqueries.google.com (client=firefox) and api.bing.com/qsonhs.aspx."""
import json, os, time, urllib.parse, urllib.request, string, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,"data","keywords.json")
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) PickAPlugin keyword research"}
def get(url):
  try: return urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=15).read().decode("utf-8","replace")
  except Exception as ex: return ""
def google(q):
  t=get("https://suggestqueries.google.com/complete/search?client=firefox&q="+urllib.parse.quote(q))
  try: return json.loads(t)[1]
  except Exception: return []
def bing(q):
  t=get("https://api.bing.com/qsonhs.aspx?type=cb&q="+urllib.parse.quote(q))
  try: return [s["Txt"] for r in json.loads(t)["AS"].get("Results",[]) for s in r["Suggests"]]
  except Exception: return []
def both(q):
  r={"google":google(q),"bing":bing(q)}; time.sleep(0.35); return r
old=json.load(open(OUT)) if os.path.exists(OUT) else {}
P=json.load(open(os.path.join(ROOT,"data","plugins.json")))
top=sorted([p for p in P if isinstance(p.get("stars"),int)],key=lambda p:-p["stars"])[:int(sys.argv[1]) if len(sys.argv)>1 else 220]
# GSC page-two plugins (positions 11-20) get queried too, whatever their stars.
GSC=["codex-rg-guard","data-product-builder-for-dbt","devin-plugin-cc","burpsuite-mcp-bridge","nightshift","muse4ai","codex-auto-resume","zcode-bridge","damnpdfs","reviewable-html-workbench","x-twitter-scraper","agent-guard","hotl-plugin"]
by={p["slug"]:p for p in P}; top+= [by[s] for s in GSC if s in by and by[s] not in top]
plug={}
for p in top:
  n=p["name"].strip("/ ").lower()
  if len(n)<3: continue
  plug[p["slug"]]={"name":n,"vs":both(n+" vs"),"alt":both(n+" alternative")}
SEEDS=["best mcp server for","best mcp for","best codex plugin for","best claude code plugin for","best codex skills for","mcp server for","codex plugin for","claude code plugin for"]
use={}
for s in SEEDS:
  use[s]=both(s)
  for ch in string.ascii_lowercase: use[s+" "+ch]=both(s+" "+ch)
json.dump({"fetched":time.strftime("%Y-%m-%d"),"plugins":plug,"use_cases":use},open(OUT,"w"),indent=0)
print("keywords:",len(plug),"plugins,",len(use),"use-case seeds ->",OUT)
