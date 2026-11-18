import json,urllib.request,datetime,sys,re
L='/workspace/pickaplugin/launch/'
key=open('/workspace/pickaplugin/.secrets/resend_api_key').read().strip()
sent=set()
for f in ['backlink-outreach.json','resend-send-log.json']:
    for e in json.load(open(L+f)):
        for k in ('to','email'):
            v=e.get(k); sent.update([v] if isinstance(v,str) else (v or []))
sent|=set(re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+',open(L+'outreach-sent.md').read()))
sent={s.lower().rstrip('.') for s in sent}
bo=json.load(open(L+'backlink-outreach.json')); rl=json.load(open(L+'resend-send-log.json'))
md=['\n## 2026-11-10 backlink outreach']
for m in json.load(open('emails.json')):
    if m['to'].lower() in sent: print('SKIP dup',m['to']); continue
    body=json.dumps({"from":"PickAPlugin <hello@pickaplugin.com>","to":[m['to']],"reply_to":"hello@pickaplugin.com","subject":m['subject'],"text":m['text']}).encode()
    req=urllib.request.Request('https://api.resend.com/emails',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'pickaplugin-outreach/1.0'})
    now=datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    try:
        r=json.loads(urllib.request.urlopen(req,timeout=30).read()); rid=r.get('id'); status='sent'
    except Exception as ex:
        rid=None; status='failed: '+(ex.read().decode()[:300] if hasattr(ex,'read') else str(ex))
    e={"key":m['key'],"site":m['site'],"to":m['to'],"email":m['to'],"subject":m['subject'],"time":now,"date":now[:10],"target_page":m['target_page'],"link":m['link'],"status":status,"id":rid}
    bo.append(e); rl.append(dict(e,type='backlink-outreach'))
    md.append(f"- {now[:10]} {m['site']} -> {m['to']} \"{m['subject']}\" -> {status} {rid or ''}")
    print(m['to'],status,rid)
    if status!='sent': break
json.dump(bo,open(L+'backlink-outreach.json','w'),indent=1); json.dump(rl,open(L+'resend-send-log.json','w'),indent=1)
open(L+'outreach-sent.md','a').write('\n'.join(md)+'\n')
