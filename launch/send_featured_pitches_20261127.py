import json, urllib.request, datetime, time, sys, re
R = "/workspace/pickaplugin"
sys.path.insert(0, f"{R}/launch")
from outreach_cooldown import skip_message

KEY = open(f"{R}/.secrets/resend_api_key").read().strip()
TODAY = "2026-11-27"
OFFER = "founding $29/mo for life + first week free"
CHECKOUT = "https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06"
OPT_OUT = 'Not interested? Just reply "no" and I won\'t follow up.'

P = [
    dict(
        to="support@uxpilot.ai",
        name="UX Pilot team",
        tool="UX Pilot Frontend Design Skill",
        slug="uxpilot-frontend-design-skill",
        subject="Your frontend design skill is on PickAPlugin",
        text="""Hi UX Pilot team,

Saw the new Frontend Design skill for Claude Code, Codex and Cursor. Having the agent design on a canvas you can actually edit before it writes any UI is a nice answer to "every AI site looks the same", so I added it to PickAPlugin (750+ Codex, ChatGPT and Claude plugins, skills and MCP servers) as a free listing: https://pickaplugin.com/p/uxpilot-frontend-design-skill

To be upfront: the directory is young and our traffic is still small, a lot smaller than the repo's first two days on GitHub. If you'd still like extra placement, a founding featured spot (top of Design & Frontend, the homepage, and a newsletter mention) is $29/mo for life, first week free, cancel anytime. 0 of 10 founding spots are taken. If you want it: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06

No pressure, the free listing stays either way. If anything on the page is wrong, reply and I'll fix it.

Not interested? Just reply "no" and I won't follow up.

Aaron""",
    ),
    dict(
        to="hello@neuraltrust.ai",
        name="NeuralTrust team",
        tool="TrustGate",
        slug="trustgate",
        subject="TrustGate is listed on PickAPlugin",
        text="""Hi NeuralTrust team,

Saw TrustGate go open source. One gateway that checks who's calling and where LLM, MCP and agent-to-agent calls may go is something a lot of teams running coding agents will need, so I listed it on PickAPlugin for free: https://pickaplugin.com/p/trustgate

Honest heads-up: we're new and traffic is still modest, so think of this as a cheap extra placement, not a big-reach play. If it's useful, a founding featured spot (top of Security & Governance, the homepage, and a newsletter mention) is $29/mo for life with the first week free, cancel anytime. 0 of 10 founding spots are taken. If you want it: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06

Totally optional, the listing stays either way. Happy to tweak the description if you'd put it differently.

Not interested? Just reply "no" and I won't follow up.

Aaron""",
    ),
    dict(
        to="support@clavem.io",
        name="Clavem team",
        tool="Clavem MCP",
        slug="clavem-mcp",
        subject="Clavem's MCP server is on PickAPlugin",
        text="""Hi Clavem team,

Saw that Clavem now runs from Claude. Setting up products, linking Stripe prices and issuing licenses by just asking, with the key scoped to one account, fits the indie developers you're building for, so I added the MCP server to PickAPlugin as a free listing: https://pickaplugin.com/p/clavem-mcp

I'll be straight: the directory is young and traffic is still small. If a little extra placement helps while the MCP server is new, a founding featured spot (top of Industry Tools, the homepage, and a newsletter mention) is $29/mo for life, first week free, cancel anytime. 0 of 10 founding spots are taken. If you want it: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06

No pressure, the free listing stays either way. If anything on the page is off, reply and I'll fix it.

Not interested? Just reply "no" and I won't follow up.

Aaron""",
    ),
]


def redact(s):
    s = str(s)
    if KEY:
        s = s.replace(KEY, "[redacted]")
    s = re.sub(r"Bearer\s+\S+", "Bearer [redacted]", s)
    return s


dnc = json.load(open(f"{R}/launch/do-not-contact.json"))["entries"]
dnc_e = {e.lower() for d in dnc for e in d.get("emails", [])}
dnc_d = {x.lower() for d in dnc for x in d.get("domains", [])}
dnc_s = {x for d in dnc for x in d.get("slugs", [])}
sales = json.load(open(f"{R}/launch/sales-pitches.json"))
log = json.load(open(f"{R}/launch/resend-send-log.json"))
pitched = {p["to"].lower() for p in sales["pitches"]}

results = []
for p in P:
    e = p["to"].lower()
    if e in dnc_e or e.split("@")[1] in dnc_d or p["slug"] in dnc_s:
        print("SKIP do-not-contact", p["to"])
        results.append(("skipped-dnc", p["to"], None))
        continue
    if e in pitched:
        print("SKIP already pitched", p["to"])
        results.append(("skipped-pitched", p["to"], None))
        continue
    hit = skip_message(e, log=log)
    if hit:
        print(hit)
        results.append(("skipped-cooldown", p["to"], None))
        continue
    try:
        code = urllib.request.urlopen(
            urllib.request.Request(
                "https://pickaplugin.com/p/" + p["slug"],
                headers={"User-Agent": "pickaplugin/1.0"},
            ),
            timeout=20,
        ).status
    except Exception as ex:
        code = redact(ex)
    if code != 200:
        print("SKIP listing not live", p["slug"], code)
        results.append(("skipped-not-live", p["to"], None))
        continue
    # no em dashes in body
    assert "\u2014" not in p["text"] and "\u2013" not in p["text"]
    assert "758" not in p["text"]
    assert CHECKOUT in p["text"] and "0 of 10" in p["text"] and "reply \"no\"" in p["text"]
    payload = json.dumps(
        {
            "from": "PickAPlugin <hello@pickaplugin.com>",
            "to": [p["to"]],
            "reply_to": "hello@pickaplugin.com",
            "subject": p["subject"],
            "text": p["text"],
        }
    ).encode()
    rid = None
    err = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=payload,
                headers={
                    "Authorization": "Bearer " + KEY,
                    "Content-Type": "application/json",
                    "User-Agent": "pickaplugin/1.0",
                },
            )
            rid = json.load(urllib.request.urlopen(req, timeout=30))["id"]
            break
        except Exception as ex:
            err = redact(ex)
            time.sleep(3)
    now = datetime.datetime.now().isoformat(timespec="seconds")
    status = "sent" if rid else "failed"
    sales["pitches"].append(
        dict(
            to=p["to"],
            name=p["name"],
            tool=p["tool"],
            listing_url="https://pickaplugin.com/p/" + p["slug"],
            subject=p["subject"],
            resend_id=rid,
            date=TODAY,
            time=now,
            offer=OFFER,
            status=status,
            error=None if rid else err,
        )
    )
    if rid:
        log.append(
            dict(
                key="featured-" + p["slug"],
                to=p["to"],
                email=p["to"],
                subject=p["subject"],
                time=now,
                date=TODAY,
                type="featured-pitch",
                offer=OFFER,
                status="sent",
                id=rid,
            )
        )
    print(status, p["to"], rid or err)
    results.append((status, p["to"], rid or err))
    time.sleep(0.7)

json.dump(sales, open(f"{R}/launch/sales-pitches.json", "w"), indent=2)
json.dump(log, open(f"{R}/launch/resend-send-log.json", "w"), indent=1)
print("DONE", results)
