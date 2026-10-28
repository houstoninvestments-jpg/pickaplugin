# Usage: python3 send_backlink_outreach.py [--send] [key ...]   (default: dry run, prints only)
import json, sys, os, urllib.request, urllib.error, datetime
base = "/workspace/pickaplugin/launch"
SEND = "--send" in sys.argv
only = [a for a in sys.argv[1:] if not a.startswith("--")]
drafts = json.load(open(f"{base}/backlink-drafts-2026-10-27.json"))
bp, lp = f"{base}/backlink-outreach.json", f"{base}/resend-send-log.json"
bl = json.load(open(bp)) if os.path.exists(bp) else []
rl = json.load(open(lp)) if os.path.exists(lp) else []
sent_md = "\n".join(l for l in open(f"{base}/outreach-sent.md").read().lower().splitlines() if "not sent" not in l)
used = {e.get("to", e.get("email", "")).lower() for e in rl + bl}
used_dom = {a.split("@")[-1] for a in used}
today_sent = sum(1 for e in rl + bl if e.get("status") == "sent" and str(e.get("time", e.get("date", ""))).startswith(datetime.date.today().isoformat()))
key = open("/workspace/pickaplugin/.secrets/resend_api_key").read().strip() if SEND else None
for d in drafts:
    if only and d["key"] not in only: continue
    to = d["to"].lower(); dom = to.split("@")[-1]
    if to in used or (dom != "gmail.com" and dom in used_dom) or to in sent_md:
        print("SKIP duplicate", to); continue
    if today_sent >= 10: print("STOP daily cap 10 reached"); break
    if not SEND: print(f"--- DRY {d['key']} to {to}\nSubject: {d['subject']}\n{d['text']}"); continue
    payload = {"from": "PickAPlugin <hello@pickaplugin.com>", "to": [d["to"]], "reply_to": "hello@pickaplugin.com", "subject": d["subject"], "text": d["text"]}
    req = urllib.request.Request("https://api.resend.com/emails", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Idempotency-Key": f"pap-backlink-{d['key']}-20261027", "User-Agent": "pickaplugin/1.0"})
    now = datetime.datetime.now().isoformat(timespec="seconds")
    e = {"key": f"backlink-{d['key']}", "site": d["site"], "to": d["to"], "email": d["to"], "subject": d["subject"], "time": now, "date": now[:10], "target_page": d["target_page"], "link": d["link"]}
    ok = True
    try:
        r = urllib.request.urlopen(req, timeout=30); e.update(status="sent", id=json.load(r).get("id"))
    except urllib.error.HTTPError as err:
        e.update(status="error", error=f"{err.code} {err.read().decode()[:300]}"); ok = False
    except Exception as err:
        e.update(status="error", error=str(err)[:300]); ok = False
    bl.append(e); rl.append(e)
    json.dump(bl, open(bp, "w"), indent=1); json.dump(rl, open(lp, "w"), indent=1)
    with open(f"{base}/outreach-sent.md", "a") as f:
        f.write(f"{now[:16].replace('T',' ')} PT: backlink outreach to {d['site']} <{d['to']}> \"{d['subject']}\" -> {e['status']} {e.get('id', e.get('error',''))}\n")
    print(e)
    if not ok: print("STOP: send failed, not retrying"); break
    today_sent += 1; used.add(to); used_dom.add(dom)
