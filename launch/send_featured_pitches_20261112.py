import json, urllib.request, datetime, time
KEY=open('/workspace/pickaplugin/.secrets/resend_api_key').read().strip()
TODAY='2026-11-12'
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
 dict(to='brady@agentgrown.com',name='Brady',tool='AgentGrown',slug='agentgrown',cat='Docs, Content & SEO',subject='AgentGrown is live on PickAPlugin',
  greet='Hi Brady,',comp="Thanks for sending AgentGrown over. It's now live on PickAPlugin, the directory of ChatGPT and Codex plugins and MCP servers. Giving coding agents a site's real Search Console, GA4 and keyword data instead of guesses is exactly what SEO work with agents has been missing, and the one-line remote install makes it easy to try."),
 dict(to='team@showtake.app',name='ShowTake team',tool='ShowTake',slug='showtake',cat='Design & Frontend',subject='ShowTake featured spot on PickAPlugin?',
  greet='Hi ShowTake team,',comp="ShowTake is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Having the coding agent film the demo video and App Store screenshots of the app it just built is a genuinely clever way to kill one of the most tedious parts of shipping iOS and Mac apps."),
 dict(to='support@snap-render.com',name='SnapRender team',tool='SnapRender',slug='snaprender',cat='Review & Testing',subject='SnapRender featured spot on PickAPlugin?',
  greet='Hi SnapRender team,',comp="SnapRender is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Shipping it as a Claude Code and Codex plugin plus an MCP server for Cursor and the rest is a smart way to make screenshots and page reads available wherever people's agents already live."),
 dict(to='contact@mvrks.co',name='NoLang team',tool='NoLang',slug='nolang',cat='Docs, Content & SEO',subject='NoLang featured spot on PickAPlugin?',
  greet='Hi NoLang team,',comp="NoLang is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting agents generate videos through a plugin, CLI and MCP connector all at once is a great move, and it's one of the few real video-generation tools in the catalog."),
 dict(to='vinayak@apavin.com',name='Vinayak',tool='Apavin MCP',slug='apavin-mcp',cat='Messaging & Remote',subject='Apavin MCP featured spot on PickAPlugin?',
  greet='Hi Vinayak,',comp="Apavin MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Putting business email, WhatsApp and LinkedIn behind one hosted MCP server that works in Claude, ChatGPT, Cursor and VS Code is a really practical setup for anyone doing outreach from their agent."),
 dict(to='commerce@netdigitaltech.com',name='Wapliss team',tool='Wapliss for ChatGPT',slug='wapliss-chatgpt',cat='Messaging & Remote',subject='Wapliss for ChatGPT featured spot on PickAPlugin?',
  greet='Hi Wapliss team,',comp="Wapliss for ChatGPT is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Being able to have ChatGPT summarize busy WhatsApp groups and send replies is something a lot of people want and very few tools do cleanly."),
 dict(to='team@firstblood.io',name='Vast team',tool='Vast Agentic Giveaway',slug='vast-agentic-giveaway',cat='Docs, Content & SEO',subject='Vast Agentic Giveaway featured spot on PickAPlugin?',
  greet='Hi Vast team,',comp="Vast Agentic Giveaway is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Running a whole giveaway from your AI agent, with a plugin, skill and MCP server covering every major client, is a fun and very concrete use case for marketers."),
 dict(to='hello@twring.com',name='Twring team',tool='Twring',slug='twring',cat='Messaging & Remote',subject='Twring featured spot on PickAPlugin?',
  greet='Hi Twring team,',comp="Twring is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Calling your coding agent from a phone, and having it call you back when it needs you, is one of the most fun ideas I've seen this month, and making it self-hostable is a nice touch."),
 dict(to='info@websensepro.com',name='Bilal',tool='Google Search Console MCP',slug='google-search-console-mcp',cat='Docs, Content & SEO',subject='Google Search Console MCP featured spot on PickAPlugin?',
  greet='Hi Bilal,',comp="Your Google Search Console MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Asking Claude or Cursor about keywords, indexing and period-over-period changes in plain English beats exporting CSVs from Search Console every time."),
 dict(to='contato@erathos.com',name='Erathos team',tool='Erathos MCP',slug='erathos-mcp',cat='Data & Backend',subject='Erathos MCP featured spot on PickAPlugin?',
  greet='Hi Erathos team,',comp="The Erathos MCP server is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting agents work with a data-ingestion platform that connects 100+ sources to the warehouse is a strong fit for our Data & Backend category."),
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
