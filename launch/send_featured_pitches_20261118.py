import json, urllib.request, datetime, time, sys
R='/workspace/pickaplugin'
sys.path.insert(0, f'{R}/launch')
from outreach_cooldown import recent_send, skip_message
KEY=open(f'{R}/.secrets/resend_api_key').read().strip()
TODAY='2026-11-18'
OFFER='founding $29/mo for life + first week free'
founding=json.load(open(f'{R}/data/founding.json'))
left=founding['spots_total']-len(founding['claimed'])
assert left>0
left_txt="All 10 founding spots are still open." if left==10 else f"{left} of the 10 founding spots are still open."
FOOT = """Not interested? Just reply "no" and I won't follow up.

Aaron
PickAPlugin"""
def body(greet, compliment, slug, cat):
    return f"""{greet}

{compliment} Your listing is here: https://pickaplugin.com/p/{slug}

I wanted to offer you a featured spot. That puts it at the top of {cat} and on the front page, plus a mention in our weekly newsletter (pickaplugin.substack.com).

Founding offer: the first 10 makers who sign up get it for $29/mo for life (normally $49), and the first week is free. {left_txt} Details: https://pickaplugin.com/featured

To be upfront, we're a young directory (600+ plugins so far) and traffic is still small but growing, so this is an early bet, not a big audience yet.

If you want it, you can start the free week here: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06
Or just reply with any questions.

{FOOT}"""
P=[
 dict(to='contact@coinotag.com',name='COINOTAG team',tool='COINOTAG MCP',slug='coinotag-mcp',cat='Industry Tools',subject='COINOTAG MCP featured spot on PickAPlugin?',
  greet='Hi COINOTAG team,',comp="Saw the MCP server go live this week and added it to PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Support and resistance levels for about 750 markets plus news in 6 languages, with a free tier that needs no key, is an easy thing for agents to pick up."),
 dict(to='contact@bugrecon.me',name='BugRecon team',tool='BugRecon MCP',slug='bugrecon-mcp',cat='Security & Governance',subject='BugRecon MCP featured spot on PickAPlugin?',
  greet='Hey BugRecon team,',comp="Congrats on shipping the MCP server. I listed BugRecon MCP on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting an assistant work with your projects, scopes and scans on the same permissions and quotas as the API is a clean setup for hunters."),
 dict(to='support@deployxa.com',name='Deployxa team',tool='Deployxa MCP',slug='deployxa-mcp',cat='Deploy & DevOps',subject='Deployxa MCP featured spot on PickAPlugin?',
  greet='Hi Deployxa team,',comp="Saw your post about deploying straight from Claude Code, Codex and ChatGPT, and added Deployxa MCP to PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. One hosted MCP URL with OAuth is about as low-friction as it gets."),
 dict(to='team@get-tau.com',name='Tau team',tool='Tau Scout',slug='tau-scout',cat='Industry Tools',subject='Tau Scout featured spot on PickAPlugin?',
  greet='Hi Tau team,',comp="Tau Scout is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Building and refining a LinkedIn job shortlist from your AI chat, with a CV-evidence fit check and no LinkedIn login needed, is a really practical take on job search."),
]
# safety checks
dnc=json.load(open(f'{R}/launch/do-not-contact.json'))['entries']
dnc_e={e.lower() for d in dnc for e in d.get('emails',[])}; dnc_d={x.lower() for d in dnc for x in d.get('domains',[])}; dnc_s={x for d in dnc for x in d.get('slugs',[])}
sales=json.load(open(f'{R}/launch/sales-pitches.json')); log=json.load(open(f'{R}/launch/resend-send-log.json'))
pitched={p['to'].lower() for p in sales['pitches']}
assert len(P)<=10
for p in P:
    e=p['to'].lower()
    if e in dnc_e or e.split('@')[1] in dnc_d or p['slug'] in dnc_s or e in pitched or 'codexstacks' in e:
        print('SKIP',p['to']); continue
    hit = skip_message(e, log=log)
    if hit:
        print(hit); continue
    try: code=urllib.request.urlopen(urllib.request.Request('https://pickaplugin.com/p/'+p['slug'],headers={'User-Agent':'pickaplugin/1.0'}),timeout=20).status
    except Exception as ex: code=str(ex)
    if code!=200: print('SKIP listing not live',p['slug'],code); continue
    text=body(p['greet'],p['comp'],p['slug'],p['cat'])
    payload=json.dumps({"from":"PickAPlugin <hello@pickaplugin.com>","to":[p['to']],"reply_to":"hello@pickaplugin.com","subject":p['subject'],"text":text}).encode()
    rid=None; err=None
    for attempt in range(2):  # one try + at most one retry
        try:
            req=urllib.request.Request("https://api.resend.com/emails",data=payload,headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json","User-Agent":"pickaplugin/1.0"})
            rid=json.load(urllib.request.urlopen(req,timeout=30))['id']; break
        except Exception as ex:
            err=str(ex); time.sleep(3)
    now=datetime.datetime.now().isoformat(timespec='seconds')
    status='sent' if rid else 'failed'
    sales['pitches'].append(dict(to=p['to'],name=p['name'],tool=p['tool'],listing_url='https://pickaplugin.com/p/'+p['slug'],subject=p['subject'],resend_id=rid,date=TODAY,time=now,offer=OFFER,status=status,error=None if rid else err))
    if rid: log.append(dict(key='featured-'+p['slug'],to=p['to'],email=p['to'],subject=p['subject'],time=now,date=TODAY,type='featured-pitch',offer=OFFER,status='sent',id=rid))
    print(status,p['to'],rid or err)
    time.sleep(0.7)
sales['founding_spots_taken']=len(founding['claimed'])
json.dump(sales,open(f'{R}/launch/sales-pitches.json','w'),indent=2)
json.dump(log,open(f'{R}/launch/resend-send-log.json','w'),indent=1)
