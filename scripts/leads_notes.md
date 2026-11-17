# Reading PickAPlugin leads (claims + newsletter)

Storage: Cloudflare Workers KV namespace `pickaplugin-leads` (id caf33a408d824dc39e86448463eb97b4), bound to the
`pickaplugin` Worker as `LEADS`. Free tier.
- Listing claims: keys `claim:<ISO time>:<rand>` → `{type,at,email,github,slug,corrections,country}`
- Subscribers:   keys `sub:<email>` → `{type,status,at,email,from,confirm_sent_at,confirm_id,confirmed_at}`.
  Double opt-in: /api/subscribe stores `status:"pending"` and the Worker emails a confirm link via Resend (RESEND_KEY binding,
  from .secrets/resend_api_key). /confirm (static page) POSTs to /api/confirm → `status:"confirmed"`.
  No per-confirm alert is emailed to Aaron; include subscriber counts in the Tuesday newsletter report instead
  (`python3 scripts/newsletter.py report`). Only `confirmed` subscribers get the newsletter. Max 3 confirm emails per address, 15 min apart.

Secrets live in `scripts/.secrets.json` (git-ignored): `admin_token`, Turnstile `sitekey`/`secret`, `kv` id.
upload_buckets.py reads it and attaches the bindings LEADS, TURNSTILE_SECRET, ADMIN_TOKEN, NOTIFY on every deploy.

## Read all leads
    T=$(python3 -c "import json;print(json.load(open('scripts/.secrets.json'))['admin_token'])")
    curl -s "https://pickaplugin.com/api/admin?token=$T"
Each subscriber row includes its personal one-click `unsubscribe` URL (HMAC of the email). Put it in every newsletter.
Delete one entry: `curl -s "https://pickaplugin.com/api/admin?token=$T&delete=<key>"`
(KV list is eventually consistent: a deleted key can still be listed for ~60s; the admin view skips it.)
Also visible in the Cloudflare dashboard → Workers KV → pickaplugin-leads.

## Notifications
Each new listing claim sends a plain-text email to houstoninvestments@gmail.com through the free
Email Routing `send_email` binding (NOTIFY, verified destination only). Failures are logged and don't block the form.
Newsletter confirms do not send an alert; the Tuesday newsletter report prints confirmed/pending/new counts instead.

## Spam protection
Honeypot field `website` (silently accepted, not stored) + Cloudflare Turnstile (free, widget `pickaplugin-forms`).
Owner-only test path: send header `x-admin-token: $T` to skip Turnstile (used for end-to-end tests).

## Handling a claim
1. Check the GitHub handle owns or contributes to the repo on the plugin's page.
2. Apply corrections in data/plugins.json (overrides survive refresh only for featured_/verified fields; description
   fixes need a manual override), rebuild, deploy.
3. Reply from hello@pickaplugin.com (Aaron approves outgoing email). Paid upgrades may be mentioned softly.

## Founding advertisers
/advertise shows "Founding placements so far: N of 10", computed at build time from active paid flags in
data/plugins.json (featured, top_spot, belt, verified, category sponsors). The first 10 subscriptions keep their
Stripe price; never change the price on an existing subscription.

## Weekly newsletter (scripts/newsletter.py)
    python3 scripts/newsletter.py draft --date YYYY-MM-DD    # data/newsletter/<date>.json from catalog + git star history
    python3 scripts/newsletter.py preview --date D           # /workspace/newsletter-<date>.html/.txt
    python3 scripts/newsletter.py test --date D --to delivered@resend.dev
    python3 scripts/newsletter.py send --date D --yes        # confirmed subscribers only; resumable, never double-sends
    python3 scripts/newsletter.py subscribers                # counts by status
    python3 scripts/newsletter.py report                     # confirmed/pending/new-in-last-7-days counts (no addresses)
    python3 scripts/newsletter.py sync-log                   # log Worker confirmation sends (masked) in launch/resend-send-log.json
Then commit data/newsletter/<date>.json, rebuild and deploy so /newsletter lists it. Drafts publish at /newsletter/<date>
with noindex and a "Preview" banner. The repo is public: subscriber addresses never go in git (full send state is in the
git-ignored .secrets/newsletter-sends.json; the public log has masked addresses + Resend ids).

## Views / clicks sent to makers (Durable Object `Stats`, binding STATS)
/p/<slug> views and /go/<slug> clicks are counted in the Worker: browser-like UAs only (bot regex, verified bots,
prefetch and no-Accept-Language requests skipped), once per visitor per slug per day using an HMAC of IP+date
(salted with ADMIN_TOKEN, rotates daily, rows pruned after 2 days; raw IPs never stored). Monthly totals (UTC month).
/p pages show "N views · M clicks to the maker this month" only when views > 0; /advertise shows the site-wide clicks line
only when > 0. Read all counts: `curl -s "https://pickaplugin.com/api/admin?token=$T&stats=1[&month=2026-11]"`.
Counting started 2026-11-15.

## Newsletter first-run setup (2026-11-17)
- DONE: /featured copy now says 'PickAPlugin weekly newsletter' (scripts/build.py), no Substack mention.
- NOT DONE: confirmation email to the 1 legacy unconfirmed subscriber. /api/subscribe is Turnstile-protected (w=captcha), so it can't be driven from a script. Needs a browser submit or Aaron's OK to mint the confirm link directly.
