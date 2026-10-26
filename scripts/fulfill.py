#!/usr/bin/env python3
"""Apply Featured Spot orders from Stripe to data/plugins.json.

Usage: python3 scripts/fulfill.py sessions.json [subscriptions.json] [--dry-run]

sessions.json      checkout sessions as returned by the Stripe connector (a list, or {"data":[...]}).
subscriptions.json optional list of subscriptions ({id,status}); without it, a session's embedded
                   subscription object/status is used, else a paid+complete session counts as active.

A session is a Featured order if mode == "subscription" (the only recurring product) or its
metadata/payment-link metadata says featured_monthly. The "plugin_url" custom field is matched to
entries by normalized link (github owner/repo). Unknown plugins are added as a minimal entry
(source "featured-order", needs_review) built only from the URL; no description is invented.
Canceled/unpaid/expired subscriptions unset the flag. Exits 0; prints a summary of changes.
"""
import json, re, sys, datetime
DATA = "data/plugins.json"; CAP = 3
LIVE = {"active", "trialing", "past_due"}

def load(path):
    d = json.load(open(path))
    if isinstance(d, dict): d = d.get("data", d.get("sessions", [d]))
    return d

def norm(u):
    u = (u or "").strip().lower()
    u = re.sub(r"^https?://", "", u); u = re.sub(r"^www\.", "", u)
    u = u.split("#")[0].split("?")[0].rstrip("/")
    u = re.sub(r"\.git$", "", u)
    m = re.match(r"github\.com/([^/]+)/([^/]+)", u)
    return f"github.com/{m[1]}/{m[2]}" if m else u

def field(sess, key="plugin_url"):
    for f in sess.get("custom_fields") or []:
        if f.get("key") == key:
            return (f.get("text") or {}).get("value") or ""
    return ""

def is_featured(s):
    md = (s.get("metadata") or {}); pl = s.get("payment_link")
    plmd = pl.get("metadata", {}) if isinstance(pl, dict) else {}
    return s.get("mode") == "subscription" or "featured_monthly" in (md.get("pickaplugin"), plmd.get("pickaplugin"))

def sub_status(s, subs):
    sub = s.get("subscription")
    sid = sub.get("id") if isinstance(sub, dict) else sub
    if sid and sid in subs: return sid, subs[sid]
    if isinstance(sub, dict) and sub.get("status"): return sid, sub["status"]
    if s.get("status") == "complete" and s.get("payment_status") == "paid": return sid, "active"
    return sid, "incomplete"

def slugify(x): return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", x.lower())).strip("-")

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]; dry = "--dry-run" in sys.argv
    sessions = load(args[0])
    subs = {x["id"]: x.get("status") for x in load(args[1])} if len(args) > 1 else {}
    P = json.load(open(DATA)); idx = {}
    for p in P:
        for u in (p.get("link"),): idx.setdefault(norm(u), p)
    today = datetime.date.today().isoformat(); log = []
    # latest state per plugin wins (sessions sorted by created)
    want = {}
    for s in sorted(sessions, key=lambda s: s.get("created", 0)):
        if not is_featured(s): continue
        url = field(s)
        if not url: log.append(f"! {s.get('id')}: no plugin_url, handle by hand"); continue
        sid, st = sub_status(s, subs)
        want[norm(url)] = (url, sid, st, s.get("id"))
    for key, (url, sid, st, cs) in want.items():
        live = st in LIVE; p = idx.get(key)
        if not p and live:
            m = re.match(r"github\.com/([^/]+)/([^/]+)", key)
            name = m[2] if m else key.split("/")[0]
            p = {"slug": slugify(name), "name": name, "description": "", "maker": m[1] if m else "",
                 "link": url if url.startswith("http") else "https://" + url, "category": "Other",
                 "source": "featured-order", "source_url": "", "source_section": "Featured order",
                 "first_seen": today, "featured": False, "needs_review": True}
            while any(x["slug"] == p["slug"] for x in P): p["slug"] += "-x"
            P.append(p); idx[key] = p; log.append(f"+ added {p['slug']} from {url} (needs description/category review)")
        if not p: continue
        if live and not p.get("featured"):
            p.update(featured=True, featured_sub=sid, featured_session=cs, featured_since=today); log.append(f"* featured {p['slug']} ({st})")
        elif not live and p.get("featured") and p.get("featured_sub") in (sid, None):
            p["featured"] = False; p["featured_ended"] = today; log.append(f"- unfeatured {p['slug']} ({st})")
    n = sum(1 for p in P if p.get("featured"))
    if n > CAP: log.append(f"! {n} featured but only {CAP} slots: site shows the first {CAP}; refund/waitlist the extra")
    print("\n".join(log) or "no changes"); print(f"{n} featured")
    if not dry and log: json.dump(P, open(DATA, "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__": main()
