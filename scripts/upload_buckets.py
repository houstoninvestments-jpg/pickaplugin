"""Usage: python3 scripts/upload_buckets.py <file with execute result {jwt,buckets}>  -> writes /workspace/code2.js (deploy call)."""
import sys, json, base64, mimetypes, subprocess, os
ACCT = "32b17f59cb6436ea7169a23489541bd8"
t = open(sys.argv[1]).read(); r = json.loads(t[t.index('{'):t.rindex('}') + 1])
m = json.load(open('/workspace/manifest.json')); h2p = {v['hash']: k for k, v in m.items()}
comp = r['jwt'] if not r['buckets'] else None
for b in r['buckets']:
    args = []
    for h in b:
        p = h2p[h]; open('/tmp/' + h, 'w').write(base64.b64encode(open('dist' + p, 'rb').read()).decode())
        args += ['-F', f'{h}=</tmp/{h};type={mimetypes.guess_type(p)[0] or "application/octet-stream"}']
    j = json.loads(subprocess.run(['curl', '-s', '-X', 'POST', f'https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/assets/upload?base64=true', '-H', 'Authorization: Bearer ' + r['jwt']] + args, capture_output=True, text=True).stdout)
    assert j['success'], j
    comp = j['result'].get('jwt') or comp
SEC = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".secrets.json")))  # not committed
EXTRA = [{"type": "kv_namespace", "name": "LEADS", "namespace_id": SEC["kv"]},
         {"type": "secret_text", "name": "TURNSTILE_SECRET", "text": SEC["secret"]},
         {"type": "secret_text", "name": "ADMIN_TOKEN", "text": SEC["admin_token"]},
         {"type": "send_email", "name": "NOTIFY", "destination_address": "houstoninvestments@gmail.com"},
         {"type": "durable_object_namespace", "name": "STATS", "class_name": "Stats"}]  # views/clicks counter (worker/index.js)
_RK = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".secrets", "resend_api_key")  # not committed, never print
if os.path.exists(_RK): EXTRA.append({"type": "secret_text", "name": "RESEND_KEY", "text": open(_RK).read().strip()})
else: print("WARNING: .secrets/resend_api_key missing, newsletter confirmation emails will fail")
js = open('worker/index.js').read().strip()
meta = {"main_module": "index.js", "compatibility_date": "2026-10-01", "assets": {"jwt": comp, "config": {"html_handling": "auto-trailing-slash", "not_found_handling": "404-page", "run_worker_first": ["/p/*", "/advertise", "/advertise.html", "/advertise/", "/go/*"]}}, "bindings": [{"type": "assets", "name": "ASSETS"}] + EXTRA}
# Durable Object migration v1 (class Stats) is sent only if the live script doesn't have it yet.
open('/workspace/code2.js', 'w').write('''async () => { const meta=%s; const js=%s; const b="F"+Date.now();
const cur=(await cloudflare.request({method:"GET",path:`/accounts/${accountId}/workers/scripts`})).result.find(x=>x.id==="pickaplugin");
if(!cur||cur.migration_tag!=="v1") meta.migrations={new_tag:"v1",new_sqlite_classes:["Stats"]};
const body=["--"+b,'Content-Disposition: form-data; name="metadata"',"Content-Type: application/json","",JSON.stringify(meta),"--"+b,'Content-Disposition: form-data; name="index.js"; filename="index.js"',"Content-Type: application/javascript+module","",js,"--"+b+"--"].join("\\r\\n");
const r=await cloudflare.request({method:"PUT",path:`/accounts/${accountId}/workers/scripts/pickaplugin`,body,contentType:"multipart/form-data; boundary="+b,rawBody:true}); return {ok:r.success, migrated:!!meta.migrations}; }''' % (json.dumps(meta), json.dumps(js)))
print("uploaded", len(r['buckets']), "buckets; wrote /workspace/code2.js")
