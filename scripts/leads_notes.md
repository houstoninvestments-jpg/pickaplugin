# Reading PickAPlugin leads (claims + newsletter)

Storage: Cloudflare Workers KV namespace `pickaplugin-leads` (id caf33a408d824dc39e86448463eb97b4), bound to the
`pickaplugin` Worker as `LEADS`. Free tier.
- Listing claims: keys `claim:<ISO time>:<rand>` → `{type,at,email,github,slug,corrections,country}`
- Subscribers:   keys `sub:<email>` → `{type,at,email,from}`

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
Each new claim/subscriber also sends a plain-text email to houstoninvestments@gmail.com through the free
Email Routing `send_email` binding (NOTIFY, verified destination only). Failures are logged and don't block the form.

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
