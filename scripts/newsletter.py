"""PickAPlugin weekly newsletter: "New MCP servers & plugins, once a week".

  python3 scripts/newsletter.py draft [--date YYYY-MM-DD]      build data/newsletter/<date>.json from real catalog data (no email)
  python3 scripts/newsletter.py preview --date D               write /workspace/newsletter-<date>.html (+ .txt) to look at
  python3 scripts/newsletter.py test --date D --to ADDR        send ONE [TEST] copy (use delivered@resend.dev for a dry run)
  python3 scripts/newsletter.py send --date D --yes            send to CONFIRMED subscribers only, then mark the issue sent
  python3 scripts/newsletter.py subscribers                    counts by status (no addresses printed)
  python3 scripts/newsletter.py sync-log                       copy Worker confirmation sends into launch/resend-send-log.json

Content: plugins whose first_seen falls in the 7 days ending on <date>, the biggest GitHub star gains vs the committed
data/plugins.json from 7 days earlier (git history), and at most ONE sponsored slot, only if a paid featured listing exists.
The web archive (/newsletter, /newsletter/<date>) is built by scripts/build_newsletter.py from data/newsletter/*.json.
Privacy: the repo is public, so subscriber addresses never go in git. Full per-address send state lives in the git-ignored
.secrets/newsletter-sends.json; launch/resend-send-log.json gets masked addresses plus the Resend id.
The Resend key is read from .secrets/resend_api_key and is never printed.
"""
import argparse, datetime as dt, hashlib, html, json, os, subprocess, sys, time, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://pickaplugin.com"
ISSUES = os.path.join(ROOT, "data", "newsletter")
LOG = os.path.join(ROOT, "launch", "resend-send-log.json")
PRIVATE = os.path.join(ROOT, ".secrets", "newsletter-sends.json")
FROM = "PickAPlugin <hello@pickaplugin.com>"
e = lambda s: html.escape(str(s or ""), quote=True)

def plugins(src=None):
    d = json.loads(src) if src else json.load(open(os.path.join(ROOT, "data", "plugins.json")))
    return d if isinstance(d, list) else d["plugins"]

def old_plugins(before):
    c = subprocess.run(["git", "-C", ROOT, "rev-list", "-1", f"--before={before} 23:59:59", "HEAD", "--", "data/plugins.json"], capture_output=True, text=True).stdout.strip()
    if not c: return None, None
    src = subprocess.run(["git", "-C", ROOT, "show", f"{c}:data/plugins.json"], capture_output=True, text=True).stdout
    return plugins(src), c[:7]

def card(p, **extra):
    o = {"slug": p["slug"], "name": p["name"], "summary": p.get("description", ""), "category": p.get("category", ""), "maker": p.get("maker") or "",
         "url": f"{SITE}/p/{p['slug']}", "stars": p["stars"] if isinstance(p.get("stars"), int) else None}
    o.update(extra); return o

def draft(date):
    P = plugins(); d = dt.date.fromisoformat(date); start = d - dt.timedelta(days=7)
    new = sorted([p for p in P if start.isoformat() < p.get("first_seen", "") <= date], key=lambda p: (-(p["stars"] if isinstance(p.get("stars"), int) else -1), p["name"].lower()))
    OLD, commit = old_plugins(start.isoformat())
    movers = []
    if OLD:
        was = {p["slug"]: p.get("stars") for p in OLD if isinstance(p.get("stars"), int)}
        for p in P:
            if isinstance(p.get("stars"), int) and p["slug"] in was and p["stars"] > was[p["slug"]] and not p.get("archived"):
                movers.append(card(p, gained=p["stars"] - was[p["slug"]], was=was[p["slug"]]))
        movers.sort(key=lambda m: -m["gained"]); movers = movers[:5]
    paid = [p for p in P if p.get("featured")]
    spons = None
    if paid:
        p = paid[d.isocalendar()[1] % len(paid)]
        spons = card(p, label="Sponsored · paid featured listing")
    issue = {"date": date, "status": "draft", "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
             "window": [start.isoformat(), date], "catalog_size": len(P), "stars_baseline_commit": commit,
             "subject": f"{len(new)} new MCP servers & plugins this week" if new else "This week in MCP servers & plugins",
             "new_total": len(new), "new": [card(p) for p in new[:15]], "movers": movers, "sponsored": spons}
    os.makedirs(ISSUES, exist_ok=True)
    path = os.path.join(ISSUES, date + ".json")
    if os.path.exists(path) and json.load(open(path)).get("status") == "sent": sys.exit(f"{path} was already sent; not overwriting")
    json.dump(issue, open(path, "w"), indent=1, ensure_ascii=False); open(path, "a").write("\n")
    print(f"draft {path}: {len(new)} new, {len(movers)} movers, sponsored={'yes' if spons else 'none'}")
    return issue

def load(date):
    path = os.path.join(ISSUES, date + ".json")
    if not os.path.exists(path): sys.exit(f"no issue {path}; run draft first")
    return json.load(open(path)), path

def fmt(n): return f"{n:,}"
def nice(date): return dt.date.fromisoformat(date).strftime("%B %-d, %Y")

# ---- rendering (shared by email and the web archive) ----
def body_html(I, web=False):
    """Inline-styled HTML for the issue body. web=True drops the email-only header bits."""
    A = "color:#1f3a8a"; out = []
    if not web:
        out.append(f'<p style="font:600 12px Menlo,monospace;letter-spacing:.04em;text-transform:uppercase;color:#5b5a52;margin:0 0 4px">PickAPlugin weekly · {e(nice(I["date"]))}</p>')
        out.append(f'<h1 style="font:800 28px/1.15 Georgia,serif;margin:0 0 10px">{e(I["subject"])}</h1>')
    out.append(f'<p>Here\'s what joined the PickAPlugin catalog of MCP servers and ChatGPT, Codex &amp; Claude plugins between {e(nice(I["window"][0]))} and {e(nice(I["window"][1]))}. The catalog has {fmt(I["catalog_size"])} listings now. Everything below comes from our catalog data and GitHub. Nothing here is paid except a slot marked <b>Sponsored</b>.</p>')
    if I.get("sponsored"):
        s = I["sponsored"]
        out.append(f'<div style="border:1px solid #1f3a8a;padding:12px 14px;margin:18px 0"><p style="font:600 11px Menlo,monospace;text-transform:uppercase;{A};margin:0 0 4px">{e(s["label"])}</p>'
                   f'<p style="margin:0"><a href="{e(s["url"])}" style="{A};font-weight:700">{e(s["name"])}</a>: {e(s["summary"])}</p></div>')
    out.append('<h2 style="font:700 20px Georgia,serif;margin:22px 0 6px;border-top:3px solid #14171f;padding-top:8px">New this week</h2>')
    if I["new"]:
        out.append('<ul style="padding-left:18px;margin:0">' + "".join(
            f'<li style="margin:0 0 9px"><a href="{e(n["url"])}" style="{A};font-weight:700">{e(n["name"])}</a> <span style="color:#5b5a52;font-size:13px">· {e(n["category"])}{" · ★ " + fmt(n["stars"]) if n.get("stars") is not None else ""}</span><br>{e(n["summary"])}</li>'
            for n in I["new"]) + "</ul>")
        if I["new_total"] > len(I["new"]): out.append(f'<p>…and {I["new_total"] - len(I["new"])} more in the <a href="{SITE}/#catalog" style="{A}">full catalog</a>.</p>')
    else:
        out.append("<p>No new listings this week.</p>")
    if I["movers"]:
        out.append('<h2 style="font:700 20px Georgia,serif;margin:22px 0 6px;border-top:3px solid #14171f;padding-top:8px">Gaining stars fastest</h2>'
                   '<p style="color:#5b5a52;font-size:13px;margin:0 0 6px">GitHub stars gained in the last 7 days, from our daily star checks.</p><ol style="padding-left:20px;margin:0">' + "".join(
            f'<li style="margin:0 0 7px"><a href="{e(m["url"])}" style="{A};font-weight:700">{e(m["name"])}</a> +{fmt(m["gained"])} (now ★ {fmt(m["stars"])})<br><span style="font-size:14px">{e(m["summary"])}</span></li>'
            for m in I["movers"]) + "</ol>")
    out.append(f'<p style="margin-top:22px">Made one of these? Your listing has a free badge for your README. Know a plugin we\'re missing? <a href="{SITE}/submit" style="{A}">Submit it free</a> or just reply to this email.</p>')
    return "\n".join(out)

def email_html(I, unsub):
    return (f'<!doctype html><html><body style="margin:0;background:#f4efe1"><div style="max-width:600px;margin:0 auto;padding:22px 20px;font:16px/1.5 Georgia,serif;color:#14171f;background:#fffdf8">'
            f'{body_html(I)}<hr style="border:0;border-top:1px solid #cfc6ad;margin:24px 0 10px">'
            f'<p style="font-size:12.5px;color:#5b5a52">You get this because you subscribed and confirmed at pickaplugin.com. <a href="{e(unsub)}" style="color:#5b5a52">Unsubscribe in one click</a> · '
            f'<a href="{SITE}/newsletter/{I["date"]}" style="color:#5b5a52">View in browser</a><br>PickAPlugin is independent and not affiliated with OpenAI or Anthropic.</p></div></body></html>')

def email_text(I, unsub):
    L = [f'PickAPlugin weekly · {nice(I["date"])}', I["subject"], "", f'New in the catalog ({nice(I["window"][0])} to {nice(I["window"][1])}). Nothing is paid except a slot marked Sponsored.', ""]
    if I.get("sponsored"): s = I["sponsored"]; L += [f'[{s["label"]}] {s["name"]}: {s["summary"]}', s["url"], ""]
    L.append("NEW THIS WEEK")
    L += [f'- {n["name"]} ({n["category"]}): {n["summary"]}\n  {n["url"]}' for n in I["new"]] or ["No new listings this week."]
    if I["new_total"] > len(I["new"]): L.append(f'...and {I["new_total"] - len(I["new"])} more: {SITE}/#catalog')
    if I["movers"]: L += ["", "GAINING STARS FASTEST (last 7 days)"] + [f'- {m["name"]} +{m["gained"]:,} (now {m["stars"]:,}): {m["url"]}' for m in I["movers"]]
    L += ["", f"Submit a plugin: {SITE}/submit", f"View in browser: {SITE}/newsletter/{I['date']}", f"Unsubscribe: {unsub}"]
    return "\n".join(L)

# ---- sending ----
def secrets():
    return json.load(open(os.path.join(ROOT, "scripts", ".secrets.json")))

def subscribers():
    tok = secrets()["admin_token"]
    req = urllib.request.Request(f"{SITE}/api/admin?token={urllib.parse.quote(tok)}", headers={"user-agent": "pickaplugin-newsletter"})
    return json.load(urllib.request.urlopen(req, timeout=60))["subscribers"]

def mask(a):
    u, _, d = a.partition("@"); return (u[:1] + "***@" + d[:1] + "***." + d.rsplit(".", 1)[-1]) if d else "***"

def resend_send(to, subject, html_, text, unsub):
    key = open(os.path.join(ROOT, ".secrets", "resend_api_key")).read().strip()
    body = {"from": FROM, "to": [to], "subject": subject, "html": html_, "text": text, "reply_to": "hello@pickaplugin.com",
            "headers": {"List-Unsubscribe": f"<{unsub}>", "List-Unsubscribe-Post": "List-Unsubscribe=One-Click"}}
    req = urllib.request.Request("https://api.resend.com/emails", data=json.dumps(body).encode(), method="POST",
                                 headers={"authorization": "Bearer " + key, "content-type": "application/json", "user-agent": "pickaplugin-newsletter"})
    return json.load(urllib.request.urlopen(req, timeout=60)).get("id")

def log(entry):
    L = json.load(open(LOG)) if os.path.exists(LOG) else []
    L.append(entry); json.dump(L, open(LOG, "w"), indent=1, ensure_ascii=False)

def send(date, test_to=None):
    I, path = load(date)
    if test_to:
        unsub = f"{SITE}/unsubscribe?e=test&t=test"
        rid = resend_send(test_to, "[TEST] " + I["subject"], email_html(I, unsub), email_text(I, unsub), unsub)
        log({"key": f"newsletter-test-{date}", "to": test_to, "subject": "[TEST] " + I["subject"], "time": dt.datetime.now().isoformat(timespec="seconds"),
             "date": dt.date.today().isoformat(), "type": "newsletter-test", "status": "sent", "id": rid})
        print("test sent, id", rid); return
    if I["status"] == "sent": sys.exit("issue already marked sent")
    priv = json.load(open(PRIVATE)) if os.path.exists(PRIVATE) else {}
    done = set(priv.get(date, []))
    subs = [s for s in subscribers() if s.get("status") == "confirmed"]
    print(f"{len(subs)} confirmed subscribers; {len(done)} already sent for {date}")
    n = 0
    for s in subs:
        a = s["email"]
        if a in done: continue
        rid = resend_send(a, I["subject"], email_html(I, s["unsubscribe"]), email_text(I, s["unsubscribe"]), s["unsubscribe"])
        done.add(a); priv[date] = sorted(done); json.dump(priv, open(PRIVATE, "w"))
        log({"key": f"newsletter-{date}", "to": mask(a), "subject": I["subject"], "time": dt.datetime.now().isoformat(timespec="seconds"),
             "date": dt.date.today().isoformat(), "type": "newsletter", "status": "sent", "id": rid})
        n += 1; time.sleep(0.6)  # Resend free tier: 2 req/s
    I.update(status="sent", sent_at=dt.datetime.now().isoformat(timespec="seconds"), recipients=len(done))
    json.dump(I, open(path, "w"), indent=1, ensure_ascii=False); open(path, "a").write("\n")
    print(f"sent {n} now, {len(done)} total. Rebuild + deploy to publish /newsletter/{date} in the archive list.")

def sync_log():
    L = json.load(open(LOG)) if os.path.exists(LOG) else []
    have = {x.get("id") for x in L}; n = 0
    for s in subscribers():
        if s.get("confirm_id") and s["confirm_id"] not in have:
            log({"key": "newsletter-confirm", "to": mask(s["email"]), "subject": "Confirm your PickAPlugin subscription", "time": s.get("confirm_sent_at", "")[:19],
                 "date": s.get("confirm_sent_at", "")[:10], "type": "newsletter-confirm", "status": "sent", "id": s["confirm_id"], "via": "worker"}); n += 1
    print("logged", n, "confirmation sends")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["draft", "preview", "test", "send", "subscribers", "sync-log"])
    ap.add_argument("--date", default=dt.date.today().isoformat()); ap.add_argument("--to"); ap.add_argument("--yes", action="store_true")
    a = ap.parse_args()
    if a.cmd == "draft": draft(a.date)
    elif a.cmd == "preview":
        I, _ = load(a.date); u = f"{SITE}/unsubscribe?e=preview&t=preview"
        open(f"/workspace/newsletter-{a.date}.html", "w").write(email_html(I, u)); open(f"/workspace/newsletter-{a.date}.txt", "w").write(email_text(I, u))
        print(f"wrote /workspace/newsletter-{a.date}.html and .txt")
    elif a.cmd == "test":
        if not a.to: sys.exit("--to required")
        send(a.date, test_to=a.to)
    elif a.cmd == "send":
        if not a.yes: sys.exit("refusing to send without --yes (sends to every confirmed subscriber)")
        send(a.date)
    elif a.cmd == "subscribers":
        from collections import Counter; print(dict(Counter(s.get("status", "legacy-unconfirmed") for s in subscribers())))
    elif a.cmd == "sync-log": sync_log()
