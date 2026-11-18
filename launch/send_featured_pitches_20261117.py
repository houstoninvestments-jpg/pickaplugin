import json, urllib.request, datetime, time, sys
R='/workspace/pickaplugin'
sys.path.insert(0, f'{R}/launch')
from outreach_cooldown import recent_send, skip_message
KEY=open(f'{R}/.secrets/resend_api_key').read().strip()
TODAY='2026-11-17'
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

To be upfront, we're a young directory (about 590 plugins so far) and traffic is still small but growing, so this is an early bet, not a big audience yet.

If you want it, you can start the free week here: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06
Or just reply with any questions.

{FOOT}"""
P=[
 dict(to='support@okara.ai',name='Okara team',tool='Okara MCP',slug='okara-mcp',cat='Docs, Content & SEO',subject='Okara MCP featured spot on PickAPlugin?',
  greet='Hey Okara team,',comp="Saw the MCP launch yesterday and added Okara MCP to PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Running an AI CMO from inside ChatGPT, Claude or Codex, with anything public waiting for a yes before it goes out, is a really nice setup."),
 dict(to='team@paper.design',name='Paper team',tool='Paper MCP',slug='paper-mcp',cat='Design & Frontend',subject='Paper MCP featured spot on PickAPlugin?',
  greet='Hi Paper team,',comp="Congrats on Remote MCP. Letting cloud agents and CI work in Paper files with the desktop app closed is a big step, so I listed Paper MCP on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers."),
 dict(to='help@enhancv.com',name='Enhancv team',tool='Enhancv MCP',slug='enhancv-mcp',cat='Industry Tools',subject='Enhancv MCP featured spot on PickAPlugin?',
  greet='Hi Enhancv team,',comp="Saw the official remote MCP go up this week and added it to PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Editing a resume, writing a cover letter and tracking applications right from Claude or ChatGPT fits how people actually job-hunt now."),
 dict(to='contact@aileron-tech.fr',name='Aileron Tech team',tool='Wingbox',slug='wingbox',cat='Memory & Context',subject='Wingbox featured spot on PickAPlugin?',
  greet='Hi Aileron Tech team,',comp="Wingbox is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Giving a coding agent a local map of the codebase (blast radius, find usages, architecture layers) with no model and nothing leaving the machine is a smart way to cut cost and missed files."),
 dict(to='info@komuta.io',name='Komuta team',tool='Komuta MCP',slug='komuta-mcp',cat='Deploy & DevOps',subject='Komuta MCP featured spot on PickAPlugin?',
  greet='Hi Komuta team,',comp="The Komuta MCP server is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Deploying repos and Postgres, debugging from live traces and doing a one-sentence rollback from Claude Code or Codex is exactly the loop people want from a PaaS."),
 dict(to='support@vaartix.com',name='Vaartix team',tool='Vaartix MCP',slug='vaartix-mcp',cat='Messaging & Remote',subject='Vaartix MCP featured spot on PickAPlugin?',
  greet='Hi Vaartix team,',comp="The Vaartix hosted MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Making it read-only by default, with every send needing approval and a pause switch, is the right call for letting an agent near a transactional email account."),
 dict(to='chats.rishishah@yahoo.com',name='Rishi',tool='Punchcutter',slug='punchcutter',cat='Design & Frontend',subject='Punchcutter featured spot on PickAPlugin?',
  greet='Hi Rishi,',comp="Punchcutter is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Turning a photo of your handwriting into a real font family with kerning and OpenType features, right inside Claude, ChatGPT or Codex, is one of the most fun things in the catalog."),
 dict(to='team@nostairsplease.com',name='No Stairs Please team',tool='No Stairs Please MCP',slug='no-stairs-please-mcp',cat='Industry Tools',subject='No Stairs Please MCP featured spot on PickAPlugin?',
  greet='Hi No Stairs Please team,',comp="The No Stairs Please MCP server is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Asking ChatGPT or Claude to route a multi-stop tour across 38,000+ small venues and pull the booking contacts is a genuinely useful thing for touring bands."),
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
    code=urllib.request.urlopen(urllib.request.Request('https://pickaplugin.com/p/'+p['slug'],headers={'User-Agent':'pickaplugin/1.0'}),timeout=20).status
    if code!=200: print('SKIP 404',p['slug']); continue
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
