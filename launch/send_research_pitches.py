import json, re, sys, os, urllib.request, datetime
DRY = "--dry" in sys.argv
base = "/workspace/pickaplugin/launch"
md = open(f"{base}/research-pitches.md").read()
logp = f"{base}/resend-send-log.json"
log = json.load(open(logp)) if os.path.exists(logp) else []
sent_keys = {e["key"] for e in log if e.get("status") == "sent"}
targets = [("ars", "## 1. Ars Technica", "news@arstechnica.com"),
           ("newstack", "## 2. The New Stack", "frederic@thenewstack.io"),
           ("infoq", "## 3. InfoQ", "editors@infoq.com"),
           ("devclass", "## 4. DevClass", "devclass@sitpub.com"),
           ("console", "## 8. Console.dev", "hello@console.dev")]
key = None if DRY else open("/workspace/pickaplugin/.secrets/resend_api_key").read().strip()
for k, head, to in targets:
    sec = md.split(head, 1)[1]
    sec = re.split(r"\n## |\n---", sec, 1)[0]
    m = re.search(r"^Subject: (.+)$", sec, re.M)
    subject = m.group(1).strip()
    body = sec[m.end():].strip() + "\n"
    if k in sent_keys:
        print("SKIP already sent", k); continue
    if DRY:
        print(f"--- {k} to {to}\nSubject: {subject}\n{body}"); continue
    payload = {"from": "PickAPlugin <hello@pickaplugin.com>", "to": [to], "reply_to": "hello@pickaplugin.com", "subject": subject, "text": body}
    req = urllib.request.Request("https://api.resend.com/emails", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Idempotency-Key": f"pap-research-{k}-20261027", "User-Agent": "pickaplugin/1.0"})
    entry = {"key": k, "to": to, "subject": subject, "time": datetime.datetime.now().isoformat(timespec="seconds")}
    try:
        r = urllib.request.urlopen(req, timeout=30); entry.update(status="sent", id=json.load(r).get("id"))
    except urllib.error.HTTPError as e:
        entry.update(status="error", error=f"{e.code} {e.read().decode()[:300]}")
    log.append(entry); json.dump(log, open(logp, "w"), indent=1)
    print(entry)
