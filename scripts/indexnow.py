#!/usr/bin/env python3
"""Submit every URL in dist/sitemap.xml to IndexNow (Bing, Yandex, Seznam, Naver...). Run after a deploy."""
import re, json, urllib.request, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY="6375d5cb89838413d1e117374c6ce038"
urls=re.findall(r"<loc>(.*?)</loc>",open(os.path.join(ROOT,"dist","sitemap.xml")).read())
body=json.dumps({"host":"pickaplugin.com","key":KEY,"keyLocation":f"https://pickaplugin.com/{KEY}.txt","urlList":urls}).encode()
req=urllib.request.Request("https://api.indexnow.org/indexnow",body,{"Content-Type":"application/json; charset=utf-8"})
try: r=urllib.request.urlopen(req,timeout=30); print("IndexNow",r.status,len(urls),"urls")
except urllib.error.HTTPError as ex: print("IndexNow",ex.code,ex.read()[:300])
