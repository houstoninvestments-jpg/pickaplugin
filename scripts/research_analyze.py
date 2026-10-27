# Computes every number in the State of Codex Plugins report from data/plugins.json + research/raw.json.
import json,re,datetime,collections as C
P=json.load(open("data/plugins.json")); R=json.load(open("research/raw.json")); RR=R["repos"]
AS_OF=datetime.date.fromisoformat(R["fetched"][:10])
def vpath(v):
  if not isinstance(v,str): return None
  if v=="": return "err"
  if re.match(r"^https?:|^data:",v): return None
  if v.startswith("/") or re.match(r"^[A-Za-z]:\\",v): return "err"
  if ".." in v.split("/"): return "err"
  if not v.startswith("./"): return "warn"
def check(j):
  """Python port of the /tools/plugin-json-validator plugin() rules. Returns list of (level,code)."""
  r=[]
  if not isinstance(j,dict): return [("err","not_object")]
  if not j.get("name"): r.append(("err","name_missing"))
  elif not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$",str(j["name"])): r.append(("err","name_not_kebab"))
  if not j.get("version"): r.append(("warn","no_version"))
  elif not re.match(r"^\d+\.\d+\.\d+([-+].*)?$",str(j["version"])): r.append(("warn","version_not_semver"))
  if not j.get("description"): r.append(("warn","no_description"))
  elif len(str(j["description"]))<20: r.append(("warn","short_description"))
  if not j.get("$schema") and "interface" not in j and not j.get("skills"): r.append(("warn","no_schema"))
  a=j.get("author")
  if a is not None and not isinstance(a,str) and not (isinstance(a,dict) and a.get("name")): r.append(("err","bad_author"))
  o=(j.get("extensions") or {}).get("com.openai") if isinstance(j.get("extensions"),dict) else None
  o=o if isinstance(o,dict) else j
  for k in ["skills","apps","hooks","onboardingSkill"]+(["mcpServers"] if isinstance(o.get("mcpServers"),str) else []):
    v=o.get(k); vs=v if isinstance(v,list) else [v]
    for x in vs:
      l=vpath(x)
      if l: r.append((l,"path_"+("bad" if l=="err" else "no_dot_slash")))
  f=o.get("interface")
  if f is not None:
    if not isinstance(f,dict): r.append(("warn","interface_not_object"))
    else:
      for k in ["composerIcon","logo","logoDark"]:
        l=vpath(f.get(k)); 
        if l: r.append((l,"path_"+("bad" if l=="err" else "no_dot_slash")))
      if not f.get("displayName"): r.append(("warn","no_displayName"))
  if re.search(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|clientSecret)",json.dumps(j)): r.append(("err","secret_like"))
  return r
rows=[]
for p in P:
  g=RR.get(p["slug"])
  d=dict(slug=p["slug"],category=p["category"],source=p["source"],reachable=bool(g))
  if g:
    li=g.get("licenseInfo") or {}
    d["license"]=li.get("spdxId") if li else None   # None = GitHub found no license file
    d["archived"]=g["isArchived"]; d["stars"]=g["stargazerCount"]; d["lang"]=(g.get("primaryLanguage") or {}).get("name")
    d["pushed"]=g["pushedAt"][:10]; d["created"]=g["createdAt"][:10]
    d["days"]=(AS_OF-datetime.date.fromisoformat(d["pushed"])).days
    rm=((g.get("rm") or {}).get("text") or "")
    d["has_readme"]=bool(g.get("rm"))
    d["install"]=bool(p.get("install"))
    low=rm.lower()
    d["apikey"]=bool(re.search(r"api[ _-]?key|[A-Z][A-Z0-9]+_(API_KEY|TOKEN|SECRET)\b|access token|personal access token",rm,re.I))
    d["remote_mcp"]=bool(re.search(r"--transport\s+(http|sse)|\"type\"\s*:\s*\"(http|sse)\"|\"url\"\s*:\s*\"https://",rm+((g.get("mcp") or {}).get("text") or "")))
    pj=None; d["pj"]=None
    for k in ("pj_root","pj_codex","pj_claude"):
      if g.get(k): pj=(k,g[k].get("text") or ""); break
    d["any_manifest"]=any(g.get(k) for k in ("pj_root","pj_codex","pj_claude","mk_agents","mk_claude"))
    d["codex_manifest"]=bool(g.get("pj_root") or g.get("pj_codex") or g.get("mk_agents"))
    d["claude_manifest"]=bool(g.get("pj_claude") or g.get("mk_claude"))
    d["agents_md"]=bool(g.get("agents_md")); d["skill_md_root"]=bool(g.get("skill_md")); d["mcp_json"]=bool(g.get("mcp"))
    if pj:
      d["pj"]=pj[0]
      try: res=check(json.loads(pj[1])); d["pj_parse"]=True
      except Exception: res=[("err","invalid_json")]; d["pj_parse"]=False
      d["pj_err"]=sorted({c for l,c in res if l=="err"}); d["pj_warn"]=sorted({c for l,c in res if l=="warn"})
  rows.append(d)
json.dump({"as_of":R["fetched"],"rows":rows},open("research/rows.json","w"),indent=0)
G=[r for r in rows if r["reachable"]]; n=len(G)
def pct(a,b): return round(100*a/b,1) if b else 0
S={"as_of":R["fetched"][:10],"catalog":len(P),"github_reachable":n}
S["license"]=C.Counter(r["license"] or "None found" for r in G).most_common()
S["no_license"]=sum(1 for r in G if not r["license"]); S["other_license"]=sum(1 for r in G if r["license"]=="NOASSERTION")
S["archived"]=sum(r["archived"] for r in G)
S["stale90"]=sum(1 for r in G if r["days"]>=90); S["stale180"]=sum(1 for r in G if r["days"]>=180)
S["fresh30"]=sum(1 for r in G if r["days"]<=30); S["fresh7"]=sum(1 for r in G if r["days"]<=7)
S["created_2026"]=sum(1 for r in G if r["created"]>="2026-01-01")
st=sorted(r["stars"] for r in G); S["stars_median"]=st[n//2] if n%2 else (st[n//2-1]+st[n//2])/2
S["stars_total"]=sum(st); top10=sum(sorted(st)[-max(1,n//10):]); S["top10pct_share"]=pct(top10,sum(st))
B=[(0,0,"0"),(1,9,"1–9"),(10,99,"10–99"),(100,999,"100–999"),(1000,9999,"1k–10k"),(10000,10**9,"10k+")]
S["stars_buckets"]=[(l,sum(1 for s in st if a<=s<=b)) for a,b,l in B]
S["lang"]=C.Counter(r["lang"] or "None" for r in G).most_common()
S["install"]=sum(r["install"] for r in G); S["has_readme"]=sum(r["has_readme"] for r in G)
S["apikey"]=sum(r["apikey"] for r in G); S["remote_mcp"]=sum(r["remote_mcp"] for r in G)
S["any_manifest"]=sum(r["any_manifest"] for r in G); S["codex_manifest"]=sum(r["codex_manifest"] for r in G); S["claude_manifest"]=sum(r["claude_manifest"] for r in G)
S["agents_md"]=sum(r["agents_md"] for r in G); S["mcp_json"]=sum(r["mcp_json"] for r in G)
PJ=[r for r in G if r["pj"]]; S["pj_n"]=len(PJ); S["pj_loc"]=C.Counter(r["pj"] for r in PJ).most_common()
S["pj_invalid_json"]=sum(1 for r in PJ if not r["pj_parse"])
S["pj_with_err"]=sum(1 for r in PJ if r["pj_err"]); S["pj_clean"]=sum(1 for r in PJ if not r["pj_err"] and not r["pj_warn"])
S["pj_err_codes"]=C.Counter(c for r in PJ for c in r["pj_err"]).most_common(); S["pj_warn_codes"]=C.Counter(c for r in PJ for c in r["pj_warn"]).most_common()
S["cat"]=C.Counter(r["category"] for r in rows).most_common()
S["unreachable"]=len(P)-n
json.dump(S,open("research/stats.json","w"),indent=1)
print(json.dumps(S,indent=0))
