import json, urllib.request, datetime, time
R='/workspace/pickaplugin'
KEY=open(f'{R}/.secrets/resend_api_key').read().strip()
TODAY='2026-11-16'
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

To be upfront, we're a young directory (about 550 plugins so far) and traffic is still small but growing, so this is an early bet, not a big audience yet.

If you want it, you can start the free week here: https://buy.stripe.com/7sY6oG0A9bUbdX7eW1cQU06
Or just reply with any questions.

{FOOT}"""
P=[
 dict(to='marceloalejandrovc@gmail.com',name='Marcelo',tool='HorizonX',slug='horizonx',cat='Design & Frontend',subject='HorizonX featured spot on PickAPlugin?',
  greet='Hi Marcelo,',comp="Thanks again for sending HorizonX in. Letting an agent find a component, tune it and drop the real code into a project as HTML, Svelte or React is a much better loop than copy-pasting from a gallery, and the per-tool setup steps on horizonx.so/mcp make it easy to get going."),
 dict(to='contacto@sonnivasquez.com',name='Sonni',tool='gsc-mcp',slug='gsc-mcp',cat='Docs, Content & SEO',subject='gsc-mcp featured spot on PickAPlugin?',
  greet='Hi Sonni,',comp="Thanks again for sending gsc-mcp in. Quick Connect without having to set up a Google Cloud project is the part that sold me. That step is where most people give up on Search Console APIs, and keeping it local and read-only by default is the right call."),
 dict(to='hi@rizamo.com',name='Rizamo team',tool='Rizamo MCP',slug='rizamo-mcp',cat='Docs, Content & SEO',subject='Rizamo featured spot on PickAPlugin?',
  greet='Hi Rizamo team,',comp="Rizamo is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Putting the same set of tools behind one MCP URL, a full OpenAPI REST API and an n8n node is a really clean way to let any agent post to every channel."),
 dict(to='support@postpiper.ai',name='Kevin',tool='PostPiper MCP',slug='postpiper-mcp',cat='Docs, Content & SEO',subject='PostPiper featured spot on PickAPlugin?',
  greet='Hi Kevin,',comp="PostPiper's MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Making every scheduled post wait for an explicit approval before it publishes is exactly the guardrail people want before letting an agent near their X or LinkedIn, and including MCP on every plan is a nice touch."),
 dict(to='contact@smart-byte.com',name='Smart-Byte team',tool='PDF to E-Invoice',slug='pdf-to-einvoice',cat='Industry Tools',subject='PDF to E-Invoice featured spot on PickAPlugin?',
  greet='Hi Smart-Byte team,',comp="PDF to E-Invoice is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Adding EN 16931 ZUGFeRD / Factur-X data to the invoice PDF people already have, without changing the layout and without uploading anything, is a very practical answer to the German e-invoicing rules."),
 dict(to='stuczynski.g@gmail.com',name=None,tool='Mumro MCP',slug='mumro-mcp',cat='Docs, Content & SEO',subject='Mumro featured spot on PickAPlugin?',
  greet='Hi there,',comp="Mumro's MCP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. 38+ remote tools built on brand knowledge you save once, with a human confirmation step before anything publishes, is a thoughtful setup for teams that care how their brand sounds."),
 dict(to='conor@firstconcepts.co',name='Conor',tool='First Concepts MCP',slug='first-concepts-mcp',cat='Design & Frontend',subject='First Concepts featured spot on PickAPlugin?',
  greet='Hi Conor,',comp="First Concepts' MCP server is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting someone jump from their AI assistant straight into a project with the brief, references and concepts already there fixes the copy-paste mess that early creative work usually turns into."),
 dict(to='hello@pikastat.com',name='PikaStat team',tool='PikaStat MCP',slug='pikastat-mcp',cat='its category',subject='PikaStat featured spot on PickAPlugin?',
  greet='Hi PikaStat team,',comp="The PikaStat MCP server is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Asking Claude which of your own Pokémon to build for Great League and getting a ready team with IVs, meta ranks and no power-ups needed is one of the most fun MCP demos I've seen."),
 dict(to='support@onehaus.app',name='OneHaus team',tool='OneHaus MCP',slug='onehaus-mcp',cat='its category',subject='OneHaus featured spot on PickAPlugin?',
  greet='Hi OneHaus team,',comp="The OneHaus MCP server is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Adding to the shopping list or checking what chores are due straight from ChatGPT or Claude is one of the few MCP servers a whole household could actually use, not just developers."),
 dict(to='support@riffumi.com',name='Riffumi team',tool='Riffumi skill',slug='riffumi-skill',cat='Design & Frontend',subject='Riffumi featured spot on PickAPlugin?',
  greet='Hi Riffumi team,',comp="The Riffumi skill is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Offering the same video director as a hosted connector or as a free MIT skill that renders locally with ffmpeg is a generous way to do it, and it's one of the few video-editing tools in the catalog."),
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
