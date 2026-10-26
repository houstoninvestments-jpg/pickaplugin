# Redeploying pickaplugin.com via the user-Cloudflare connector

Site = Worker `pickaplugin` (static assets) on account 32b17f59cb6436ea7169a23489541bd8,
custom domains pickaplugin.com + www (www → apex 301 via zone redirect rule).
Use this until a CLOUDFLARE_API_TOKEN repo secret exists (then the GitHub Action deploys with wrangler).

1. `cd /workspace/pickaplugin && git pull -q && python3 scripts/refresh.py && python3 scripts/build.py`
   (optionally commit/push data/plugins.json if changed)
2. `python3 scripts/make_manifest.py`  → writes /workspace/code1.js
3. CallDynamicTool user-Cloudflare `execute` with `{"code": "$file:/workspace/code1.js"}` and
   `write_to_file: true` → result file containing `{jwt, buckets}` (upload session, valid 1h).
4. `python3 scripts/upload_buckets.py <that result file>` → curls changed files to
   /workers/assets/upload with the session JWT, writes /workspace/code2.js with the completion JWT.
5. CallDynamicTool user-Cloudflare `execute` with `{"code": "$file:/workspace/code2.js"}` → `{ok:true}`.
6. Verify: `curl -s https://pickaplugin.com/ | grep -o '<title>[^<]*'` and
   `curl -sI https://www.pickaplugin.com/ | head -1` (expect 301).

Hash rule: sha256(base64(file) + extension) hex, first 32 chars. Unchanged files are skipped by Cloudflare.

## Fulfilling Featured Spot orders (daily routine)

Live account: PickAPlugin `acct_1UUidjAJ19i9R4dz`. Read with the **read-only** connector `user-Stripe--account-2`.
(Writes, which are rarely needed, go through `user-Stripe--account-2-74867956`.)

1. List checkout sessions since the last run: Stripe connector list/search of checkout sessions, status `complete`.
   Save the JSON to `/workspace/sessions.json`. Each needs `id, created, mode, status, payment_status,
   subscription, custom_fields` (the `plugin_url` field). Featured = `mode:"subscription"`. The $19 Expedited
   Review is one-time (`mode:"payment"`) and is ignored here; handle those by hand within 24h.
2. List subscriptions (status `all`) → `/workspace/subs.json` (`[{id,status},...]`).
3. `python3 scripts/fulfill.py /workspace/sessions.json /workspace/subs.json --dry-run`, then run it without `--dry-run`.
   - Matches `plugin_url` to `link` (normalized github.com/owner/repo), sets `featured` plus `featured_sub`/`featured_since`.
   - Unknown plugin → minimal entry (`source:"featured-order"`, `needs_review:true`, empty description). Write a real
     description and category from the project's README before deploying. Never make one up.
   - canceled/unpaid/incomplete_expired → `featured:false`. Note that Stripe flips the status to canceled at period end
     when cancel_at_period_end is set, so the slot stays up for the paid period.
   - Warns if more than 3 are active; refund or waitlist the extra (the site only shows 3).
4. If anything changed: `python3 scripts/build.py`, commit `data/plugins.json`, then redeploy (steps above).
   refresh.py keeps `featured_*` fields and `featured-order` entries.
5. Email the buyer from hello@pickaplugin.com once they're live (draft it and have Aaron approve it).
