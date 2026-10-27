# python3 scripts/test_collections.py  (run after build.py) - checks gate wiring for /language and /license
import json,os,re,glob
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D=ROOT+"/dist"
P=json.load(open(ROOT+"/data/plugins.json"))
def slug(c): return "".join(ch if ch.isalnum() else "-" for ch in c.lower()).replace("--","-").replace("--","-").strip("-")
ns={"P":P,"slug":slug,"os":os}; exec(open(ROOT+"/scripts/build_collections.py").read(),ns)
fake=[{"language":"JS"},{"language":"javascript"},{"language":"JavaScript"},{"language":"Go"},{"language":"Go"}]
g=ns["resolve_indexable"]("language",fake); assert list(g)==["javascript"] and len(g["javascript"]["items"])==3, g
sm=open(D+"/sitemap.xml").read()
for fam,cfg in ns["FAMILIES"].items():
  gated=set(ns["GATED"][fam]); files={os.path.basename(f)[:-5] for f in glob.glob(f"{D}/{fam}/*.html")}
  assert files==gated,(fam,files,gated)
  assert set(re.findall(rf"pickaplugin.com/{fam}/([^<]+)</loc>",sm))==gated
  hub=open(f"{D}/{cfg['hub']}.html").read(); assert set(re.findall(rf'href="/{fam}/([^"]+)"',hub))==gated
  for f in glob.glob(f"{D}/{fam}/*.html"):
    h=open(f).read(); n=int(re.search(r"<title>(\d+) ",h).group(1))
    assert n==len(re.findall(r'class=row href="/p/',h)),f
    assert "aggregateRating" not in h
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',h): json.loads(b)
    assert set(re.findall(rf'href="/{fam}/([^"/]+)"',h))<=gated
chips=set()
for f in glob.glob(D+"/p/*.html"): chips|=set(re.findall(r'href="/((?:language|license)/[^"]+)"',open(f).read()))
assert all(os.path.exists(f"{D}/{c}.html") for c in chips) and not any(c.count("/")>1 for c in chips)
print("ok:",{f:len(v) for f,v in ns["GATED"].items()},"chips:",len(chips))
