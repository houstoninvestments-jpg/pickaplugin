import json, urllib.request, datetime, time
KEY=open('/workspace/pickaplugin/.secrets/resend_api_key').read().strip()
TODAY='2026-11-13'
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
 dict(to='support@hronaut.dev',name='Hronaut team',tool='Hronaut for Codex',slug='hronaut-codex',cat='Agent Workflows',subject='Hronaut for Codex featured spot on PickAPlugin?',
  greet='Hi Hronaut team,',comp="Hronaut for Codex is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Giving coding agents a visible desktop browser with a separate workspace per project is a smart answer to agents trampling each other's sessions, and bundling the MCP server with a skill makes setup painless."),
 dict(to='hello@anoma.ly',name='Anomaly team',tool='browse',slug='anomaly-browse',cat='Agent Workflows',subject='browse featured spot on PickAPlugin?',
  greet='Hi Anomaly team,',comp="Your browse tool is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Letting agents use your real, logged-in browser through an MCP server and a Chromium extension skips the whole headless-login mess, which is exactly where most browser agents fall over."),
 dict(to='info@zipline.li',name='Zipline team',tool='Zipline',slug='zipline-mcp',cat='Agent Workflows',subject='Zipline featured spot on PickAPlugin?',
  greet='Hi Zipline team,',comp="Zipline is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Having Claude, ChatGPT, Grok and Gemini share one conversation and hand tasks off to each other is a genuinely different idea from the usual single-model MCP server."),
 dict(to='georgesm.petrov@gmail.com',name='Georges',tool='Screenplay',slug='agent-screenplay',cat='Docs, Content & SEO',subject='Screenplay featured spot on PickAPlugin?',
  greet='Hi Georges,',comp="Screenplay is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Getting a polished screen recording of a site or desktop app from one prompt in Claude Code, Codex or Cursor is a great time-saver, and it's no surprise it picked up stars so quickly."),
 dict(to='jean@je4ndev.com',name='Jean',tool='Elozi',slug='elozi',cat='Messaging & Remote',subject='Elozi featured spot on PickAPlugin?',
  greet='Hi Jean,',comp="Elozi is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. An open-source support inbox for WhatsApp, Telegram, web chat and email where agents draft and act only inside human-approved limits is the right balance for letting AI near customers."),
 dict(to='hello@formsmtp.com',name='FormSMTP team',tool='FormSMTP',slug='formsmtp',cat='Messaging & Remote',subject='FormSMTP featured spot on PickAPlugin?',
  greet='Hi FormSMTP team,',comp="FormSMTP is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Sending contact forms through your own SMTP (Gmail, Zoho, SES) instead of yet another third-party mail service is a nice, simple pitch, and the MCP server means agents can wire up forms without hand-holding."),
 dict(to='aj@intuicodigital.com',name='Calorie Cub team',tool='Calorie Cub',slug='calorie-cub',cat='Industry Tools',subject='Calorie Cub featured spot on PickAPlugin?',
  greet='Hi Calorie Cub team,',comp="Calorie Cub is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Building calorie tracking agent-first, so you just tell Claude or ChatGPT what you ate, is one of the friendliest consumer uses of MCP I've seen."),
 dict(to='hey@kadirhan.dev',name='Kadirhan',tool='Ramback',slug='ramback',cat='Deploy & DevOps',subject='Ramback featured spot on PickAPlugin?',
  greet='Hi Kadirhan,',comp="Ramback is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Finding the dev servers Claude Code, Codex and Cursor left running (plus forgotten simulators and Gradle daemons) from the menu bar solves a very real annoyance for anyone running agents all day."),
 dict(to='deanjyool@gmail.com',name='Dean',tool='LoreVault',slug='lorevault',cat='Memory & Context',subject='LoreVault featured spot on PickAPlugin?',
  greet='Hi Dean,',comp="LoreVault is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Turning agent chat history into an Obsidian or Logseq graph of decisions, rules and gotchas, each linked back to its source, is a really clever way to stop re-explaining the same things to your agent."),
 dict(to='hey@warenmail.com',name='Waren',tool='Suno Music Producer',slug='suno-music-producer',cat='Docs, Content & SEO',subject='Suno Music Producer featured spot on PickAPlugin?',
  greet='Hi Waren,',comp="Suno Music Producer is listed on PickAPlugin, a directory of ChatGPT and Codex plugins and MCP servers. Bundling the Suno MCP server with a reusable skill for producing songs and covers is a fun one, and it's one of the very few music tools in the catalog."),
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

