#!/usr/bin/env python3
"""Run after build.py. Checks the 2026-11-21 thin-page cleanup still holds."""
import os, re, json, datetime, collections
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=os.path.join(ROOT,"dist")
SITE="https://pickaplugin.com"
sm=open(os.path.join(D,"sitemap.xml")).read()
urls=re.findall(r"<loc>(.*?)</loc>",sm)
lastmods=dict(re.findall(r"<loc>(.*?)</loc><lastmod>(.*?)</lastmod>",sm))
paths=[u[len(SITE):] or "/" for u in urls]
assert all(u.startswith(SITE+"/") or u==SITE+"/" or u==SITE for u in urls)

def has(prefix):
  return [p for p in paths if p.startswith(prefix) and p!=(prefix[:-1] if prefix.endswith("/") else prefix)]

# Retired programmatic families must not be in the sitemap
for pref,label in (("/compare/","compare children"),("/alternatives/","plugin alternatives"),
                   ("/best/","best-of duplicates"),("/best-for/","best-for pages"),
                   ("/tools/mcp-config-converter/","converter pair pages")):
  bad=has(pref)
  assert not bad, (label, bad[:5], len(bad))

# Thank-you / form pages: noindex, not in sitemap
thank=["claimed","confirm","confirmed","subscribed","unsubscribed","form-error"]
for name in thank:
  assert f"/{name}" not in paths, name
  h=open(os.path.join(D,name+".html")).read()
  assert 'name=robots content="noindex' in h, name

# Hubs we kept
for keep in ("/", "/compare", "/alternatives", "/languages", "/licenses",
             "/c/agent-workflows", "/c/data-backend", "/tools/mcp-config-converter",
             "/guides/install-codex-plugin", "/guides/install-mcp-server-claude-cursor-codex", "/guides/check-mcp-server-safe"):
  assert keep in paths, keep

# /best files must not be generated; /c files must
assert not os.path.isdir(os.path.join(D,"best")) or not os.listdir(os.path.join(D,"best"))
assert not os.path.isdir(os.path.join(D,"compare")) or not os.listdir(os.path.join(D,"compare"))
assert not os.path.isdir(os.path.join(D,"alternatives")) or not os.listdir(os.path.join(D,"alternatives"))
assert not os.path.isdir(os.path.join(D,"best-for")) or not os.listdir(os.path.join(D,"best-for"))
cfiles=sorted(f[:-5] for f in os.listdir(os.path.join(D,"c")) if f.endswith(".html"))
assert len(cfiles)>=10, cfiles
for s in cfiles:
  assert f"/c/{s}" in paths, s
  h=open(os.path.join(D,"c",s+".html")).read()
  assert "Stars measure popularity" in h
  assert 'name=robots content="noindex' not in h

# Language gate: no page with fewer than 10 plugins
for f in os.listdir(os.path.join(D,"language")):
  if not f.endswith(".html"): continue
  h=open(os.path.join(D,"language",f)).read()
  n=int(re.search(r"<title>(\d+) ",h).group(1))
  assert n>=10, (f,n)

# Homepage has the original how-to copy
home=open(os.path.join(D,"index.html")).read()
assert "How to use this catalog" in home
assert "read the code before you install" in home.lower() or "Read the code before you install" in home

# lastmod must not stamp every URL as today (78f80ca behavior)
today=datetime.date.today().isoformat()
todays=sum(1 for d in lastmods.values() if d==today)
assert todays < len(lastmods), (todays, len(lastmods))
# A stable legal page should usually keep its old date unless we edited it this run.
# Don't hard-fail if privacy was actually rewritten; just report.
# Unique metas on previously generic legal/sales pages
for rel,needle in (("featured.html","Paid, clearly labelled featured spots"),
                   ("privacy.html","What data PickAPlugin touches"),
                   ("terms.html","Terms for using PickAPlugin")):
  h=open(os.path.join(D,rel)).read()
  assert needle in h, rel
# Homepage catalog search should not duplicate every description in a data-t attribute
home=open(os.path.join(D,"index.html")).read()
assert " data-t=" not in home
print("ok: sitemap",len(urls),"urls; lastmod today",todays,"of",len(urls),
      "; categories",len(cfiles),"; noindex",",".join(thank))
