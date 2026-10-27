# One-off GitHub fetch for the State of Codex Plugins report. Writes research/raw.json (cache, not deployed).
import json,re,subprocess,urllib.request,datetime
P=json.load(open("data/plugins.json"))
tok=subprocess.run(["gh","auth","token"],capture_output=True,text=True).stdout.strip()
FILES={"pj_root":"plugin.json","pj_codex":".codex-plugin/plugin.json","pj_claude":".claude-plugin/plugin.json",
 "mk_agents":".agents/plugins/marketplace.json","mk_claude":".claude-plugin/marketplace.json","mcp":".mcp.json","agents_md":"AGENTS.md","skill_md":"SKILL.md"}
items=[]
for p in P:
  m=re.match(r"https://github\.com/([^/]+)/([^/#?]+)",p["link"])
  if m: items.append((p["slug"],m.group(1),m.group(2).removesuffix(".git")))
out={}
for i in range(0,len(items),20):
  ch=items[i:i+20]
  def blob(k,path): return f'{k}:object(expression:{json.dumps("HEAD:"+path)}){{... on Blob{{text byteSize}}}}'
  q="query{"+" ".join(f'r{j}:repository(owner:{json.dumps(o)},name:{json.dumps(r)}){{stargazerCount forkCount isArchived isFork pushedAt createdAt licenseInfo{{spdxId name}} primaryLanguage{{name}} repositoryTopics(first:20){{nodes{{topic{{name}}}}}} rm:object(expression:"HEAD:README.md"){{... on Blob{{text}}}} '+" ".join(blob(k,v) for k,v in FILES.items())+'}' for j,(_,o,r) in enumerate(ch))+"}"
  req=urllib.request.Request("https://api.github.com/graphql",json.dumps({"query":q}).encode(),{"Authorization":"bearer "+tok,"Content-Type":"application/json"})
  d=json.load(urllib.request.urlopen(req,timeout=120))
  for j,(s,_,_) in enumerate(ch):
    out[s]=(d.get("data") or {}).get(f"r{j}")
  print(i,len(out),sum(1 for v in out.values() if v))
json.dump({"fetched":datetime.datetime.now().astimezone().isoformat(timespec="minutes"),"repos":out},open("research/raw.json","w"))
