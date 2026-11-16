# 2026-11-16: replies to maker submissions received Nov 14-16 (listing live + free badge; founding offer only where appropriate).
import json, urllib.request, datetime, time
R='/workspace/pickaplugin'
KEY=open(f'{R}/.secrets/resend_api_key').read().strip()
TODAY='2026-11-16'
OFFER='founding $29/mo for life + first week free (or $79 launch package)'
def badge(slug,name): return f"[![Listed on PickAPlugin](https://pickaplugin.com/badge/{slug}.svg)](https://pickaplugin.com/p/{slug})"
OFFER_TXT="""If you ever want more visibility: a featured spot puts it at the top of its category and on the front page. The first 10 makers get it for $29/mo for life (normally $49), with the first week free, and all 10 founding spots are still open: https://pickaplugin.com/featured . There's also a one-time $79 launch package if you'd rather not subscribe. To be upfront, we're a young directory and traffic is still small, so that's an early bet, not a big audience yet. The free listing stays either way.
"""
def body(greet,tool,slug,note,offer):
    t=f"""{greet}

Thanks for sending {tool} over. It's live now: https://pickaplugin.com/p/{slug}

{note}If you want it, here's a free badge for your README. It just links back to your listing:

{badge(slug,tool)}

If anything on the listing is wrong or out of date, reply and I'll fix it.
"""
    if offer: t+="\n"+OFFER_TXT
    t+="""
Reply "stop" and I won't email again.

Aaron
PickAPlugin"""
    return t
M=[
 dict(to='jan@inhotel.io',name='Jan',tool='GoVisit Toolkit',slug='govisit-toolkit',cat='Industry Tools',subject='Re: GoVisit Toolkit — Codex/ChatGPT plugin listing',greet='Hi Jan,',note="It's in Industry Tools, with the npx skills install line from your README. ",offer=True),
 dict(to='wlain.cwb@gmail.com',name=None,tool='the Kling AI plugin',slug='kling-ai',cat='Design & Frontend',subject='Re: Free listing suggestion: Kling AI ChatGPT and Codex plugin',greet='Hi,',note="It's in Design & Frontend, with the codex plugin marketplace install line, and the listing notes that a Kling account and paid credits are needed. ",offer=False),
 dict(to='support@juzpost.com',name='Jeeva',tool='JuzPost',slug='juzpost',cat='Docs, Content & SEO',subject='Re: Plugin submission: JuzPost for ChatGPT',greet='Hi Jeeva,',note="It's in Docs, Content & SEO, with the hosted MCP install line. ",offer=True),
 dict(to='hello@applysent.com',name='ApplySent team',tool='ApplySent',slug='applysent',cat='Industry Tools',subject='Re: Plugin submission: ApplySent',greet='Hi ApplySent team,',note="It's in Industry Tools, with the remote MCP endpoint as the install line. ",offer=True),
 dict(to='team@agentseo.dev',name='AgentSEO team',tool='AgentSEO Clients',slug='agentseo',cat='Docs, Content & SEO',subject='Re: Free listing request: AgentSEO Clients (MCP + SEO/AEO API)',greet='Hi AgentSEO team,',note="It's in Docs, Content & SEO, with the npx MCP server install line and your pricing note (100 starter credits, plans from $9/month). This also covers the earlier request from wildsummitgear@gmail.com for the same repo. ",offer=True),
 dict(to='nic@sequenzy.com',name='Nic',tool='Sequenzy',slug='sequenzy',cat='Messaging & Remote',subject='Re: Free listing submission: Sequenzy email marketing plugin',greet='Hi Nic,',note="It went through the free editorial queue as you asked. It's in Messaging & Remote, with the Codex skills install line. ",offer=False),
 dict(to='ai@artarasov.com',name='Artem',tool='Kismet',slug='kismet',cat='Industry Tools',subject='Re: Submit Kismet — open-source Unreal Engine MCP server',greet='Hi Artem,',note="It's in Industry Tools as an MCP server (not a native Codex plugin, as you said), with the local MCP install line. ",offer=True),
]
dnc=json.load(open(f'{R}/launch/do-not-contact.json'))['entries']
dnc_e={e.lower() for d in dnc for e in d.get('emails',[])}; dnc_d={x.lower() for d in dnc for x in d.get('domains',[])}
sales=json.load(open(f'{R}/launch/sales-pitches.json')); log=json.load(open(f'{R}/launch/resend-send-log.json'))
bst=json.load(open(f'{R}/launch/badge-emails.json'))
for m in M:
    if m['to'].lower() in dnc_e or m['to'].split('@')[1].lower() in dnc_d: print('SKIP dnc',m['to']); continue
    text=body(m['greet'],m['tool'],m['slug'],m['note'],m['offer'])
    payload=json.dumps({"from":"PickAPlugin <hello@pickaplugin.com>","to":[m['to']],"reply_to":"hello@pickaplugin.com","subject":m['subject'],"text":text}).encode()
    rid=None; err=None
    for a in range(3):
        try:
            req=urllib.request.Request("https://api.resend.com/emails",data=payload,headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json","User-Agent":"pickaplugin/1.0"})
            rid=json.load(urllib.request.urlopen(req,timeout=30))['id']; break
        except Exception as e: err=str(e); time.sleep(3)
    now=datetime.datetime.now().isoformat(timespec='seconds')
    print('sent' if rid else 'FAILED', m['to'], rid or err)
    if not rid: continue
    log.append(dict(key='submission-reply-'+m['slug'],to=m['to'],email=m['to'],subject=m['subject'],time=now,date=TODAY,type='submission-reply'+('+featured-offer' if m['offer'] else ''),status='sent',id=rid))
    bst['sent'].append(dict(to=m['to'],slugs=[m['slug']],subject=m['subject'],date=TODAY,time=now,id=rid))
    if m['offer']:
        sales['pitches'].append(dict(to=m['to'],name=m['name'],tool=m['tool'],listing_url='https://pickaplugin.com/p/'+m['slug'],subject=m['subject'],resend_id=rid,date=TODAY,time=now,offer=OFFER,status='sent',error=None,kind='submission-reply'))
    time.sleep(0.7)
json.dump(sales,open(f'{R}/launch/sales-pitches.json','w'),indent=2)
json.dump(log,open(f'{R}/launch/resend-send-log.json','w'),indent=1)
json.dump(bst,open(f'{R}/launch/badge-emails.json','w'),indent=1)
