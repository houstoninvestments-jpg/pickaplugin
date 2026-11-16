#!/usr/bin/env python3
"""Submit changed URLs (data/changed_urls.json) to IndexNow (Bing, Yandex, Seznam, Naver...). Run after a deploy."""
import re, json, urllib.request, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY="6375d5cb89838413d1e117374c6ce038"
urls=re.findall(r"<loc>(.*?)</loc>",open(os.path.join(ROOT,"dist","sitemap.xml")).read())
# Default (2026-11-16): submit only URLs whose content changed today, from data/changed_urls.json (written by build_seo.py,
# which also sets real lastmod dates). Bing asks for changed URLs only; resubmitting the whole sitemap daily looks like spam.
# `indexnow.py --all` sends the whole sitemap (rarely needed). Path prefixes, e.g. `indexnow.py /compare`, filter the changed list.
import datetime
args=[a for a in sys.argv[1:] if a!="--all"]
if "--all" not in sys.argv:
  cf=os.path.join(ROOT,"data","changed_urls.json")
  ch=json.load(open(cf)) if os.path.exists(cf) else {"date":"","urls":[]}
  if ch.get("date")!=datetime.date.today().isoformat(): ch["urls"]=[]
  live=set(urls); urls=[u for u in ch["urls"] if u in live]
if args: urls=[u for u in urls if any(u[len("https://pickaplugin.com"):].startswith(a) for a in args)]
if not urls: print("IndexNow: no changed URLs today, nothing sent"); sys.exit(0)
body=json.dumps({"host":"pickaplugin.com","key":KEY,"keyLocation":f"https://pickaplugin.com/{KEY}.txt","urlList":urls}).encode()
req=urllib.request.Request("https://api.indexnow.org/indexnow",body,{"Content-Type":"application/json; charset=utf-8"})
try: r=urllib.request.urlopen(req,timeout=30); print("IndexNow",r.status,len(urls),"urls")
except urllib.error.HTTPError as ex: print("IndexNow",ex.code,ex.read()[:300])
