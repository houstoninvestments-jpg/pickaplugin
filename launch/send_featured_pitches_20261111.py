import json, urllib.request, datetime, time
KEY=open('/workspace/pickaplugin/.secrets/resend_api_key').read().strip()
TODAY='2026-11-11'
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

To be upfront, we're a young directory (500+ plugins so far) and traffic is still small but growing, so this is an early bet, not a big audience yet.

If you want it, you can start the free week here: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06\nOr just reply with any questions.

{FOOT}"""
P=[
 dict(to='devs@pidgeon.ai',name='Pidgeon team',tool='Pidgeon',slug='pidgeon',cat='Messaging & Remote',subject='Pidgeon featured spot on PickAPlugin?',
  greet='Hi Pidgeon team,',comp="Pidgeon is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Giving agents their own email inboxes through one plugin that works in Claude Code, Codex, Cursor and Gemini CLI is a really clean idea, and it solves something people building agents keep hacking around."),
 dict(to='support@clypmint.com',name='Clypmint team',tool='Clypmint B-Roll',slug='clypmint-b-roll',cat='Design & Frontend',subject='Clypmint B-Roll featured spot on PickAPlugin?',
  greet='Hi Clypmint team,',comp="Clypmint B-Roll is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Pulling real footage for whatever a script names, checked by a vision model and with usage rights sorted, is a genuinely useful thing to hand an agent."),
 dict(to='docx-editor@eigenpal.com',name='EigenPal team',tool='docx-editor MCP App',slug='docx-editor-mcp-app',cat='Docs, Content & SEO',subject='docx-editor MCP App featured spot on PickAPlugin?',
  greet='Hi EigenPal team,',comp="The docx-editor MCP App is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Previewing and editing a real Word file inside ChatGPT, with live updates to the local document, is one of the more practical MCP apps I've come across."),
 dict(to='hello@spronta.com',name='Spronta team',tool='Crawlie',slug='crawlie',cat='Docs, Content & SEO',subject='Crawlie featured spot on PickAPlugin?',
  greet='Hi Spronta team,',comp="Crawlie is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. A fast, open-source SEO and GEO crawler that installs as a Codex plugin marketplace is a great fit for our SEO category, and the star count shows people like it."),
 dict(to='contact@mitigant.io',name='Mitigant team',tool='Mitigant MCP Server',slug='mitigant-mcp',cat='Security & Governance',subject='Mitigant MCP featured spot on PickAPlugin?',
  greet='Hi Mitigant team,',comp="The Mitigant MCP Server is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting an agent run curated, reversible cloud attacks mapped to MITRE ATT&CK is a bold and very concrete use of MCP for security teams."),
 dict(to='me@ricardodantas.me',name='Ricardo',tool='Loam',slug='loam',cat='Memory & Context',subject='Loam featured spot on PickAPlugin?',
  greet='Hi Ricardo,',comp="Loam is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. A local-first Markdown notes app with live co-editing and backlinks, where agents can work right in your notes over MCP, is a lovely combination."),
 dict(to='kye@swarms.world',name='Kye',tool='Swarms Skills',slug='swarms-skills',cat='Agent Workflows',subject='Swarms Skills featured spot on PickAPlugin?',
  greet='Hi Kye,',comp="Swarms Skills is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Connecting Claude Code and Codex straight to the Swarms Marketplace through skills and your MCP server is a smart move, and the launch clearly landed with your audience."),
 dict(to='support@buildcord.dev',name='Buildcord team',tool='Buildcord MCP Server',slug='buildcord-mcp',cat='Messaging & Remote',subject='Buildcord MCP featured spot on PickAPlugin?',
  greet='Hi Buildcord team,',comp="Congrats on shipping the MCP server. Buildcord is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Building and changing Discord bots just by asking ChatGPT, Claude or Cursor is a really fun way to use a no-code builder."),
 dict(to='support@webtwizz.com',name='WebTwizz team',tool='WebTwizz',slug='webtwizz',cat='Design & Frontend',subject='WebTwizz featured spot on PickAPlugin?',
  greet='Hi WebTwizz team,',comp="WebTwizz is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Building and publishing a site from ChatGPT, Claude, Codex or Gemini CLI and then carrying on in your own editor is a nice handoff that most AI builders skip."),
 dict(to='support@hoplix.com',name='Hoplix team',tool='Hoplix Print-on-Demand MCP',slug='hoplix-mcp',cat='Industry Tools',subject='Hoplix MCP featured spot on PickAPlugin?',
  greet='Hi Hoplix team,',comp="The Hoplix Print-on-Demand MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. A remote OAuth MCP server that lets shop owners run print-on-demand from Claude or ChatGPT is a great example of a real business going agent-ready."),
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
