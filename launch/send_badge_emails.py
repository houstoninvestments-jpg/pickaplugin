#!/usr/bin/env python3
"""Daily 'you're listed, here's your free badge' emails to listed makers.
Usage: python3 launch/send_badge_emails.py [--dry-run] [--max N]
Sources (only emails already in our data, no scraping): launch/leads.json, launch/sales-pitches.json, INBOUND below.
Skips: do-not-contact.json (emails/domains/slugs), leads declined/do_not_contact, pitches lost/replied/won,
anyone already badge-emailed, anyone emailed by us in the last COOLDOWN_DAYS (deferred, not dropped).
State: launch/badge-emails.json. Every send also appended to launch/resend-send-log.json."""
import json, re, sys, time, datetime, urllib.request, os
R='/workspace/pickaplugin'
MAX=50; COOLDOWN_DAYS=14
if '--max' in sys.argv: MAX=int(sys.argv[sys.argv.index('--max')+1])
DRY='--dry-run' in sys.argv
INBOUND=[  # makers who asked us to list them (emails from their own requests)
 dict(email='marceloalejandrovc@gmail.com',name='Marcelo',slug='horizonx'),
 dict(email='contacto@sonnivasquez.com',name='Sonni',slug='gsc-mcp'),
]
HOLD_SLUGS={'rizamo-mcp','postpiper-mcp','pdf-to-einvoice'}  # queued for a featured pitch by the sales routine; badge email waits for COOLDOWN after that pitch
ROLE_SKIP=('security@','abuse@','privacy@','legal@','noreply','no-reply','donotreply','dmca@','billing@')
J=lambda f: json.load(open(f'{R}/{f}'))
cat={p['slug']:p for p in J('data/plugins.json')}
picks=set(re.findall(r'"([a-z0-9-]+)":"', open(f'{R}/scripts/build.py').read().split('PICKS={',1)[1].split('}\n',1)[0]))
dnc=J('launch/do-not-contact.json')['entries']
dnc_e={e.lower() for d in dnc for e in d.get('emails',[])}
dnc_d={x.lower() for d in dnc for x in d.get('domains',[])}
dnc_s={x for d in dnc for x in d.get('slugs',[])}
leads=J('launch/leads.json'); pitches=J('launch/sales-pitches.json')['pitches']; log=J('launch/resend-send-log.json')
stp=f'{R}/launch/badge-emails.json'
state=json.load(open(stp)) if os.path.exists(stp) else {"about":"Badge email state. 'sent' = done (never resend). Opt-outs go to do-not-contact.json.","sent":[],"skipped":[]}
done={s['to'].lower() for s in state['sent']}
bad_status={s['to'].lower() for s in pitches if s.get('status') in ('lost','replied','won')}
bad_status|={l['email'].lower() for l in leads if l.get('email') and (l.get('declined') or l.get('do_not_contact'))}
pitched={s['to'].lower() for s in pitches}
cand={}
def add(email,name,slug):
    if not email or slug not in cat or cat[slug].get('archived'): return
    e=email.strip().lower(); c=cand.setdefault(e,dict(to=email.strip(),name=None,slugs=[]))
    if name and not c['name']: c['name']=name
    if slug not in c['slugs']: c['slugs'].append(slug)
for i in INBOUND: add(i['email'],i['name'],i['slug'])
for s in pitches:
    nm=s.get('name') or ''
    add(s['to'], None if nm.endswith(' team') else nm, s['listing_url'].rstrip('/').rsplit('/',1)[1])
for l in leads: add(l.get('email'),None,l['slug'])
last={}
for x in log:
    e=(x.get('to') or x.get('email') or '').lower(); d=x.get('date')
    if e and d and d>last.get(e,''): last[e]=d
today=datetime.date.today()
queue=[];deferred=[];excluded=[]
for e,c in cand.items():
    dom=e.split('@')[1]
    if e in done: continue
    if e in dnc_e or dom in dnc_d or any(s in dnc_s for s in c['slugs']) or e in bad_status: excluded.append(e); continue
    if e.startswith(ROLE_SKIP) or 'noreply' in e: excluded.append(e); continue
    if any(x in HOLD_SLUGS for x in c['slugs']) and e not in pitched: deferred.append((e,'after featured pitch + %dd'%COOLDOWN_DAYS)); continue
    if e in last and (today-datetime.date.fromisoformat(last[e])).days<COOLDOWN_DAYS:
        deferred.append((e,str(datetime.date.fromisoformat(last[e])+datetime.timedelta(days=COOLDOWN_DAYS)))); continue
    queue.append(c)
def label(s): return "Editor's pick on" if s in picks else "Listed on"
def body(c,featured_line):
    names=[cat[s]['name'] for s in c['slugs']]; tool=' and '.join(names)
    greet=f"Hi {c['name']}," if c['name'] else "Hi there,"
    pages='\n'.join(f"https://pickaplugin.com/p/{s}" for s in c['slugs'])
    snips='\n\n'.join(f"[![{label(s)} PickAPlugin](https://pickaplugin.com/badge/{s}.svg)](https://pickaplugin.com/p/{s})" for s in c['slugs'])
    one=len(c['slugs'])==1
    t=f"""{greet}

Quick heads up: {tool} {'is' if one else 'are'} listed on PickAPlugin, a free directory of ChatGPT, Codex and Claude plugins and MCP servers. {'Your page' if one else 'Your pages'}:
{pages}

If you want it, there's a free "{label(c['slugs'][0])} PickAPlugin" badge for your README. It just links back to your listing. Paste this in:

{snips}

Totally optional. And if anything on the listing is wrong or out of date, reply and I'll fix it.
"""
    if featured_line: t+="\n(There's also a paid featured spot at pickaplugin.com/featured if you ever want more visibility, but the listing and badge are free either way.)\n"
    t+="""
Reply "stop" and I won't email again.

Aaron
PickAPlugin"""
    return t
print(f"candidates={len(cand)} queue={len(queue)} deferred={len(deferred)} excluded={len(excluded)} already_sent={len(done)}")
KEY=None if DRY else open(f'{R}/.secrets/resend_api_key').read().strip()
sent=0;errors=[]
for c in queue[:MAX]:
    tool=cat[c['slugs'][0]]['name']
    subj=f"Free badge for {tool} on PickAPlugin"
    text=body(c, c['to'].lower() not in pitched and c['to'].lower() not in {i['email'].lower() for i in INBOUND})
    if DRY: print('---',c['to'],subj); print(text); continue
    payload=json.dumps({"from":"PickAPlugin <hello@pickaplugin.com>","to":[c['to']],"reply_to":"hello@pickaplugin.com","subject":subj,"text":text}).encode()
    rid=None;err=None
    for a in range(3):
        try:
            req=urllib.request.Request("https://api.resend.com/emails",data=payload,headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json","User-Agent":"pickaplugin/1.0"})
            rid=json.load(urllib.request.urlopen(req,timeout=30))['id'];break
        except Exception as ex:
            err=str(ex);time.sleep(3)
    now=datetime.datetime.now().isoformat(timespec='seconds')
    if rid:
        sent+=1
        state['sent'].append(dict(to=c['to'],slugs=c['slugs'],subject=subj,date=str(today),time=now,id=rid))
        log.append(dict(key='badge-'+c['slugs'][0],to=c['to'],email=c['to'],subject=subj,time=now,date=str(today),type='badge-email',status='sent',id=rid))
    else: errors.append((c['to'],err))
    print('sent' if rid else 'FAILED',c['to'],rid or err)
    time.sleep(0.7)
if not DRY:
    state['last_run']=dict(date=str(today),sent=sent,errors=errors,remaining_ready=len(queue)-sent,deferred=[dict(to=e,eligible=d) for e,d in deferred])
    json.dump(state,open(stp,'w'),indent=1)
    json.dump(log,open(f'{R}/launch/resend-send-log.json','w'),indent=1)
    print(f"SENT={sent} ERRORS={len(errors)} READY_LEFT={len(queue)-sent} DEFERRED={len(deferred)}")
