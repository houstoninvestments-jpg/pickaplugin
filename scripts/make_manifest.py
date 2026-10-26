"""Build the Workers static-assets manifest for dist/ -> /workspace/manifest.json and /workspace/code1.js."""
import os, hashlib, base64, json
m = {}
for r, _, fs in os.walk('dist'):
    for f in fs:
        p = os.path.join(r, f); b = open(p, 'rb').read(); ext = os.path.splitext(f)[1][1:]
        m['/' + os.path.relpath(p, 'dist')] = {"hash": hashlib.sha256((base64.b64encode(b).decode() + ext).encode()).hexdigest()[:32], "size": len(b)}
json.dump(m, open('/workspace/manifest.json', 'w'))
open('/workspace/code1.js', 'w').write('async () => (await cloudflare.request({method:"POST",path:`/accounts/${accountId}/workers/scripts/pickaplugin/assets-upload-session`,body:{manifest:' + json.dumps(m) + '}})).result')
print(len(m), "files")
