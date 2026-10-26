"""Spotlight cards for tag posts, same style as make_graphics.py."""
import json,re,os,sys
src=open(os.path.join(os.path.dirname(__file__),"make_graphics.py")).read().split("# parse kit")[0]
exec(src)
from playwright.sync_api import sync_playwright
slugs=sys.argv[1:]
with sync_playwright() as pw:
  b=pw.chromium.launch();pg=b.new_page();pg.set_viewport_size({"width":1200,"height":675})
  for s in slugs:
    x=BY[s];h=card("Spotlight",x["name"],oneline(x["description"]),x["category"],f"pickaplugin.com/p/{s}")
    pg.set_content(f"<html><head>{HEAD}</head><body>{h}</body></html>",wait_until="networkidle");pg.evaluate("document.fonts.ready")
    pg.screenshot(path=f"{G}/tag-{s}.png");print("made",s)
  b.close()
