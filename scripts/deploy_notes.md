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
