import sys,subprocess,time
from playwright.sync_api import sync_playwright
d,tag,port=sys.argv[1],sys.argv[2],sys.argv[3]
s=subprocess.Popen(["python3","-m","http.server",port,"-d",d],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
with sync_playwright() as p:
  b=p.chromium.launch(executable_path="/usr/bin/google-chrome");pg=b.new_page(viewport={"width":1280,"height":800})
  for name,u in [("home","index.html"),("plugin","p/agent-guard.html")]:
    pg.goto(f"http://localhost:{port}/{u}");pg.wait_for_timeout(1500);pg.screenshot(path=f"redesign/{tag}-{name}.png")
  b.close()
s.kill()
