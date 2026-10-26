#!/usr/bin/env python3
"""Apply paid-placement orders from Stripe to data/plugins.json.

Usage: python3 scripts/fulfill.py sessions.json [subscriptions.json] [--dry-run]

sessions.json      checkout sessions from the Stripe connector (a list, or {"data":[...]}).
subscriptions.json optional list of subscriptions ({id,status}); without it, a session's embedded
                   subscription status is used, else a paid+complete session counts as active.

Tier is identified by the payment link (id -> tier map below, or expanded link metadata tier/pickaplugin),
or session metadata. Tiers and the plugin fields they control:
  featured_monthly  featured=True            cap 3   (homepage band, category pins)
  top_spot          top_spot=True            cap 1   (homepage hero banner)
  belt              belt=True                cap 12  (scrolling belt on every page)
  category_sponsor  sponsor_category=<cat>   cap 1 per category ("Presented by" band)
  verified          verified=True            no cap  (checkmark + "Verified by maker")
Each tier also stores <tier>_sub / <tier>_session / <tier>_since; cancellations clear the flag.
Caps are enforced: the earliest active orders win; later ones are NOT turned on and are logged
as "! OVERFLOW ... refund" so Aaron can refund them. expedited_review (one-time) is ignored here.
The "plugin_url" custom field is matched to entries by normalized link (github owner/repo). Unknown plugins
are added as a minimal entry (source "featured-order", needs_review); no description is invented.
"""
import json, re, sys, datetime
DATA = "data/plugins.json"
LIVE = {"active", "trialing", "past_due"}
PLINKS = {
    "plink_1UUj18AJ19i9R4dzs8Ie2Uq4": "featured_monthly",
    "plink_1UUj1AAJ19i9R4dze4Tgzzpx": "expedited_review",
    "plink_1UUjNCAJ19i9R4dz965F509o": "top_spot",
    "plink_1UUjNJAJ19i9R4dz6KFmPJgJ": "belt",
    "plink_1UUjNSAJ19i9R4dzcQ3HgQ1X": "category_sponsor",
    "plink_1UUjNMAJ19i9R4dzXZ9x7H0u": "verified",
}
CAPS = {"featured_monthly": 3, "top_spot": 1, "belt": 12, "category_sponsor": 1, "verified": None}
FLAG = {"featured_monthly": "featured", "top_spot": "top_spot", "belt": "belt", "verified": "verified",
        "category_sponsor": "sponsor_category"}
PREFIX = {"featured_monthly": "featured", "top_spot": "top_spot", "belt": "belt", "verified": "verified",
          "category_sponsor": "sponsor"}
CATS = {"agentworkflows": "Agent Workflows", "databackend": "Data & Backend", "deploydevops": "Deploy & DevOps",
        "designfrontend": "Design & Frontend", "docscontentseo": "Docs, Content & SEO", "industrytools": "Industry Tools",
        "memorycontext": "Memory & Context", "messagingremote": "Messaging & Remote", "reviewtesting": "Review & Testing",
        "securitygovernance": "Security & Governance", "usagequotas": "Usage & Quotas", "miscellany": "Miscellany"}

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
            return (f.get("text") or {}).get("value") or (f.get("dropdown") or {}).get("value") or ""
    return ""

def tier(s):
    pl = s.get("payment_link"); md = s.get("metadata") or {}
    if isinstance(pl, dict):
        t = (pl.get("metadata") or {}).get("tier") or (pl.get("metadata") or {}).get("pickaplugin")
        if t: return t
        pl = pl.get("id")
    if pl in PLINKS: return PLINKS[pl]
    return md.get("tier") or md.get("pickaplugin")

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
    for p in P: idx.setdefault(norm(p.get("link")), p)
    today = datetime.date.today().isoformat(); log = []
    want = {}  # (tier, plugin key) -> latest order
    for s in sorted(sessions, key=lambda s: s.get("created", 0)):
        t = tier(s)
        if t == "expedited_review": continue
        if t not in CAPS:
            if s.get("mode") == "subscription": log.append(f"! {s.get('id')}: subscription with unknown tier, check by hand")
            continue
        url = field(s)
        if not url: log.append(f"! {s.get('id')} ({t}): no plugin_url, handle by hand"); continue
        sid, st = sub_status(s, subs)
        cat = CATS.get(field(s, "category"), field(s, "category")) if t == "category_sponsor" else None
        want[(t, norm(url))] = dict(url=url, sid=sid, st=st, cs=s.get("id"), cat=cat, created=s.get("created", 0))
    # cancellations first, so freed slots can be reused in this same run
    for (t, key), o in want.items():
        p = idx.get(key); f = FLAG[t]; pre = PREFIX[t]
        if p and o["st"] not in LIVE and p.get(f) and p.get(pre + "_sub") in (o["sid"], None):
            p[f] = None if t == "category_sponsor" else False; p[pre + "_ended"] = today
            log.append(f"- {t} off {p['slug']} ({o['st']})")
    for (t, key), o in sorted(want.items(), key=lambda kv: kv[1]["created"]):
        if o["st"] not in LIVE: continue
        f = FLAG[t]; pre = PREFIX[t]; p = idx.get(key)
        val = o["cat"] if t == "category_sponsor" else True
        if t == "category_sponsor" and not o["cat"]:
            log.append(f"! {o['cs']}: category sponsor without a category, handle by hand"); continue
        if p and p.get(f) == val: continue
        holders = [x for x in P if x.get(f) and (t != "category_sponsor" or x.get(f) == val)]
        if CAPS[t] is not None and len(holders) >= CAPS[t]:
            log.append(f"! OVERFLOW {t}{' '+val if t=='category_sponsor' else ''}: {o['url']} (session {o['cs']}, sub {o['sid']}) "
                       f"- cap {CAPS[t]} full; NOT turned on. Refund/cancel or waitlist."); continue
        if not p:
            m = re.match(r"github\.com/([^/]+)/([^/]+)", key)
            name = m[2] if m else key.split("/")[0]
            p = {"slug": slugify(name), "name": name, "description": "", "maker": m[1] if m else "",
                 "link": o["url"] if o["url"].startswith("http") else "https://" + o["url"], "category": "Other",
                 "source": "featured-order", "source_url": "", "source_section": "Paid order",
                 "first_seen": today, "featured": False, "needs_review": True}
            while any(x["slug"] == p["slug"] for x in P): p["slug"] += "-x"
            P.append(p); idx[key] = p; log.append(f"+ added {p['slug']} from {o['url']} (needs description/category review)")
        p[f] = val; p[pre + "_sub"] = o["sid"]; p[pre + "_session"] = o["cs"]; p[pre + "_since"] = today
        log.append(f"* {t} on {p['slug']}{' ('+val+')' if t=='category_sponsor' else ''} ({o['st']})")
    print("\n".join(log) or "no changes")
    for t, f in FLAG.items(): print(f"{t}: {sum(1 for p in P if p.get(f))} active")
    if not dry and log: json.dump(P, open(DATA, "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__": main()
