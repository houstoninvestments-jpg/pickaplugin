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
js = open('worker/index.js').read().strip()
meta = {"main_module": "index.js", "compatibility_date": "2026-10-01", "assets": {"jwt": comp, "config": {"html_handling": "auto-trailing-slash", "not_found_handling": "404-page"}}, "bindings": [{"type": "assets", "name": "ASSETS"}]}
open('/workspace/code2.js', 'w').write('''async () => { const meta=%s; const js=%s; const b="F"+Date.now();
const body=["--"+b,'Content-Disposition: form-data; name="metadata"',"Content-Type: application/json","",JSON.stringify(meta),"--"+b,'Content-Disposition: form-data; name="index.js"; filename="index.js"',"Content-Type: application/javascript+module","",js,"--"+b+"--"].join("\\r\\n");
const r=await cloudflare.request({method:"PUT",path:`/accounts/${accountId}/workers/scripts/pickaplugin`,body,contentType:"multipart/form-data; boundary="+b,rawBody:true}); return {ok:r.success}; }''' % (json.dumps(meta), json.dumps(js)))
print("uploaded", len(r['buckets']), "buckets; wrote /workspace/code2.js")
