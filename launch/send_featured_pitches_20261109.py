import json, urllib.request, datetime, time
KEY=open('/workspace/pickaplugin/.secrets/resend_api_key').read().strip()
TODAY='2026-11-09'
OFFER='founding $29/mo for life + first week free'
FOOT = """Not interested? Just reply "no" and I won't follow up.

Aaron
PickAPlugin"""
def body(greet, compliment, slug, cat, extra_intro=None):
    intro = extra_intro or ""
    return f"""{greet}

{intro}{compliment} Your listing is here: https://pickaplugin.com/p/{slug}

I wanted to offer you a featured spot. That puts it at the top of {cat} and on the front page, plus a mention in our weekly newsletter (pickaplugin.substack.com).

Founding offer: the first 10 makers who sign up get it for $29/mo for life (normally $49), and the first week is free. No spots have been taken yet. Details: https://pickaplugin.com/featured

To be upfront, we're a young directory (450+ plugins so far) and traffic is still small but growing, so this is an early bet, not a big audience yet.

If you want it, just reply "yes" and I'll send the payment link and set it live.

{FOOT}"""
P=[
 dict(to='dvir@jobspipe.dev',name='Dvir',tool='JobsPipe',slug='jobspipe',cat='Industry Tools',subject='JobsPipe featured spot on PickAPlugin?',
  greet='Hi Dvir,',comp="Thanks again for sending JobsPipe our way. Normalizing postings from 30+ ATS feeds into one MCP server is the kind of plumbing nobody wants to build twice."),
 dict(to='mariam.soliman@skycloak.io',name='Mariam',tool='Skycloak MCP',slug='skycloak-mcp',cat='Security & Governance',subject='Skycloak MCP featured spot on PickAPlugin?',
  greet='Hi Mariam,',comp="Thanks for submitting Skycloak MCP. Being able to manage Keycloak realms, SSO and users straight from an MCP client is a really practical one for teams who live in their agents."),
 dict(to='mesmerpercy@gmail.com',name='Mesmer',tool='LurkAPI',slug='lurkapi',cat='Docs, Content & SEO',subject='LurkAPI featured spot on PickAPlugin?',
  greet='Hey,',comp="Thanks again for sending LurkAPI over. Pulling public posts, transcripts and ad library results from 16 platforms through one MCP server, with free credits to try it, is a great deal for researchers."),
 dict(to='zeal@arcmira.com',name='Zeal',tool='Arcmira',slug='arcmira-youtube-transcript-search',cat='Docs, Content & SEO',subject='Arcmira featured spot on PickAPlugin?',
  greet='Hi Zeal,',comp="Hope the updated homepage and API docs links look right on your listing. Searching YouTube transcripts for timestamped quotes and sponsor mentions is genuinely useful, and the 30+ stars on the repo show people agree."),
 dict(to='hello@neverapply.co',name='Mohammed',tool='NeverApply',slug='neverapply',cat='Industry Tools',subject='NeverApply featured spot on PickAPlugin?',
  greet='Hi Mohammed,',comp="Thanks again for submitting NeverApply. Letting people search jobs without signing in and only asking for OAuth when they want help applying is a really thoughtful setup."),
 dict(to='baley@zens.ai',name='Baley',tool='call-grokbot',slug='call-grokbot',cat='Agent Workflows',subject='call-grokbot is live on PickAPlugin',
  greet='Hi Baley,',extra="Sorry this took a while: your call-grokbot submission slipped through for a week, but it's live now. ",
  comp="Letting a coding agent ask your existing Grok Bots and even interrupt a running request is a clever bridge."),
 dict(to='hello@fastcrw.com',name='CRW team',tool='CRW',slug='crw',cat='Data & Backend',subject='CRW featured spot on PickAPlugin?',
  greet='Hey CRW team,',comp="CRW is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. A Rust Firecrawl/Tavily alternative that agents can call directly is a great fit, and 1.2k stars says it's landing."),
 dict(to='hello@callstack.com',name='Callstack team',tool='Mobile Dev',slug='mobile-dev-callstack',cat='Design & Frontend',subject='Mobile Dev featured spot on PickAPlugin?',
  greet='Hey Callstack folks,',comp="Your Mobile Dev plugin is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Streaming live simulators and devices right beside the agent's chat is one of the coolest things I've seen in a Codex plugin."),
 dict(to='info@exza.de',name='EXZA team',tool='EXZA Remote',slug='exza-remote',cat='Messaging & Remote',subject='EXZA Remote featured spot on PickAPlugin?',
  greet='Hi EXZA team,',comp="EXZA Remote is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Connecting ChatGPT and Claude to your own Mac, Windows or Linux machine with proper device pairing solves a real problem cleanly."),
 dict(to='hello@canonry.ai',name='Canonry team',tool='Canonry',slug='canonry',cat='Docs, Content & SEO',subject='Canonry featured spot on PickAPlugin?',
  greet='Hi Canonry team,',comp="Canonry is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Shipping Codex plugins for AI-answer SEO is smart, since the people browsing plugins are exactly the ones thinking about how AI tools see their brand."),
]
sales=json.load(open('/workspace/pickaplugin/launch/sales-pitches.json'))
log=json.load(open('/workspace/pickaplugin/launch/resend-send-log.json'))
for p in P:
    text=body(p['greet'],p['comp'],p['slug'],p['cat'],p.get('extra'))
    payload=json.dumps({"from":"PickAPlugin <hello@pickaplugin.com>","to":[p['to']],"reply_to":"hello@pickaplugin.com","subject":p['subject'],"text":text}).encode()
    rid=None; err=None
    for attempt in range(3):
        try:
            req=urllib.request.Request("https://api.resend.com/emails",data=payload,headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json","User-Agent":"pickaplugin/1.0"})
            rid=json.load(urllib.request.urlopen(req,timeout=30))['id']; break
        except Exception as e:
            err=str(e); time.sleep(3)
    now=datetime.datetime.now().isoformat(timespec='seconds')
    status='sent' if rid else 'failed'
    sales['pitches'].append(dict(to=p['to'],name=p['name'],tool=p['tool'],listing_url='https://pickaplugin.com/p/'+p['slug'],subject=p['subject'],resend_id=rid,date=TODAY,time=now,offer=OFFER,status=status,error=err))
    if rid: log.append(dict(key='featured-'+p['slug'],to=p['to'],email=p['to'],subject=p['subject'],time=now,date=TODAY,type='featured-pitch',offer=OFFER,status='sent',id=rid))
    print(status,p['to'],rid or err)
    time.sleep(0.7)
sales['founding_spots_taken']=0
json.dump(sales,open('/workspace/pickaplugin/launch/sales-pitches.json','w'),indent=2)
json.dump(log,open('/workspace/pickaplugin/launch/resend-send-log.json','w'),indent=1)
