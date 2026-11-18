import json, urllib.request, datetime, time
KEY=open('/workspace/pickaplugin/.secrets/resend_api_key').read().strip()
TODAY='2026-11-10'
OFFER='founding $29/mo for life + first week free'
FOOT = """Not interested? Just reply "no" and I won't follow up.

Aaron
PickAPlugin"""
def body(greet, compliment, slug, cat, extra_intro=None):
    intro = extra_intro or ""
    return f"""{greet}

{intro}{compliment} Your listing is here: https://pickaplugin.com/p/{slug}

I wanted to offer you a featured spot. That puts it at the top of {cat} and on the front page, plus a mention in our weekly newsletter (pickaplugin.substack.com).

Founding offer: the first 10 makers who sign up get it for $29/mo for life (normally $49), and the first week is free. All 10 founding spots are still open. Details: https://pickaplugin.com/featured

To be upfront, we're a young directory (450+ plugins so far) and traffic is still small but growing, so this is an early bet, not a big audience yet.

If you want it, you can start the free week here: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06\nOr just reply with any questions.

{FOOT}"""
P=[
 dict(to='support@tripsy.app',name='Tripsy team',tool='Tripsy MCP',slug='tripsy-mcp',cat='Industry Tools',subject='Tripsy MCP featured spot on PickAPlugin?',
  greet='Hi Tripsy team,',comp="Tripsy MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting ChatGPT, Claude and Raycast actually read and update real trips is one of the most practical consumer MCP servers I've seen, and it's built on an app people clearly love."),
 dict(to='hello@apidrifter.com',name='API Drifter team',tool='API Drifter',slug='apidrifter',cat='Review & Testing',subject='API Drifter featured spot on PickAPlugin?',
  greet='Hi API Drifter team,',comp="API Drifter is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Checking a live API against its OpenAPI spec and flagging breaking changes in the APIs you depend on is a problem every team hits, and the quick star count shows people noticed."),
 dict(to='info@dataforseo.com',name='DataForSEO team',tool='DataForSEO Codex Plugins',slug='dataforseo-codex-plugins',cat='Docs, Content & SEO',subject='DataForSEO Codex plugins featured on PickAPlugin?',
  greet='Hi DataForSEO team,',comp="Your new Codex plugins are listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Getting live keyword, SERP and backlink data right inside Codex through your hosted MCP server is a great fit for the people browsing our SEO category."),
 dict(to='cip@titi.re',name='Ciprian',tool='Tactile UI',slug='tactile-ui',cat='Design & Frontend',subject='Tactile UI featured spot on PickAPlugin?',
  greet='Hi Ciprian,',comp="Tactile UI is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Components that feel like real hardware are such a fun idea, and having 1,100+ examples available as a Claude connector makes it genuinely usable from an agent."),
 dict(to='hello@githubcard.com',name='GitHubCard team',tool='GitHubCard MCP',slug='githubcard-mcp',cat='Design & Frontend',subject='GitHubCard MCP featured spot on PickAPlugin?',
  greet='Hi GitHubCard team,',comp="GitHubCard MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Making profile and repo cards straight from Claude or Cursor is a nice, simple use of MCP that people get right away."),
 dict(to='hello@refcat.app',name='Refcat team',tool='Refcat MCP',slug='refcat-mcp',cat='Design & Frontend',subject='Refcat MCP featured spot on PickAPlugin?',
  greet='Hi Refcat team,',comp="Refcat MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting Claude Code and Cursor look up 3.3M real app screens before they invent their own UI is a smart fix for generic AI-made interfaces."),
 dict(to='hello@modem.dev',name='Modem team',tool='Boxery',slug='boxery',cat='Deploy & DevOps',subject='Boxery featured spot on PickAPlugin?',
  greet='Hi Modem team,',comp="Boxery is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Giving coding agents their own VMs, locally or in cloud sandboxes, with the MCP server and Claude config already included, is exactly what people running agents unattended want."),
 dict(to='support@workmagic.io',name='WorkMagic team',tool='WorkMagic agent plugin',slug='workmagic-agent-plugin',cat='Data & Backend',subject='WorkMagic agent plugin featured on PickAPlugin?',
  greet='Hi WorkMagic team,',comp="Your agent plugin is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Asking about attribution, lift tests and budget plans from Claude, ChatGPT, Codex or Cursor is a strong pitch, and shipping it across that many clients at once is impressive."),
 dict(to='contact@knownagents.com',name='Known Agents team',tool='Known Agents MCP Server',slug='known-agents-mcp',cat='Docs, Content & SEO',subject='Known Agents MCP featured spot on PickAPlugin?',
  greet='Hi Known Agents team,',comp="Congrats on launching the MCP server. It's listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Asking ChatGPT or Claude which AI crawlers and agents are hitting your site is a really timely idea."),
 dict(to='support@postminion.com',name='Postminion team',tool='Postminion',slug='postminion',cat='Docs, Content & SEO',subject='Postminion featured spot on PickAPlugin?',
  greet='Hi Postminion team,',comp="Congrats on the ChatGPT plugin launch. Postminion is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Uploading once and having an agent publish or schedule across seven networks is a great use of chat."),
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
