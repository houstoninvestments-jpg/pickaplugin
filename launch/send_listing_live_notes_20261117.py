# 2026-11-17: "you're listed" replies to free-listing requesters (Aaron approved).
# Replies to people who wrote us; still honor do-not-contact.json.
# No sales pitch. Skip anyone who already got a submission-reply for the same listing.
import json, urllib.request, urllib.error, datetime, time, re
R = '/workspace/pickaplugin'
KEY = open(f'{R}/.secrets/resend_api_key').read().strip()
TODAY = '2026-11-17'

def sanitize(err):
    s = str(err)
    s = re.sub(r'Bearer\s+\S+', 'Bearer [redacted]', s)
    s = s.replace(KEY, '[redacted]')
    return s

M = [
    dict(
        to='support@clawcall.dev',
        slug='clawcall',
        subject='Re: ClawCall on PickAPlugin?',
        text=(
            "Hi Nikit,\n\n"
            "ClawCall is live on PickAPlugin: https://pickaplugin.com/p/clawcall\n\n"
            "If you want a free badge for your site or README, it's at https://pickaplugin.com/badge/clawcall.svg. "
            "Reply if anything on the listing needs fixing.\n\n"
            "Aaron, PickAPlugin"
        ),
    ),
    dict(
        to='naman@getlockstep.dev',
        slug='lockstep',
        subject='Re: Your MCP servers for dev teams post',
        text=(
            "Hi Naman,\n\n"
            "Lockstep is live now: https://pickaplugin.com/p/lockstep\n\n"
            "Thanks again, and you're welcome to cite the Codex plugin research "
            "(https://pickaplugin.com/research/state-of-codex-plugins-2026) with a link if you use it. "
            "If you want a free badge, it's at https://pickaplugin.com/badge/lockstep.svg — "
            "reply if anything on the listing needs fixing.\n\n"
            "Aaron, PickAPlugin"
        ),
    ),
    dict(
        to='hariton.mm+pickaplugin@yandex.ru',
        slug='yandex-tools-mcp',
        subject='Re: Seyka AI - free MCP listing consideration',
        text=(
            "Hi Hariton,\n\n"
            "Yandex Tools MCP is live as a free listing: https://pickaplugin.com/p/yandex-tools-mcp\n\n"
            "Have a look and reply if anything needs fixing.\n\n"
            "Aaron, PickAPlugin"
        ),
    ),
    dict(
        to='hello@getgoodfeels.com',
        slug='a-good-sign',
        subject='Re: Free listing submission: A Good Sign Apple Health MCP (Codex integration)',
        text=(
            "Hi Jason,\n\n"
            "A Good Sign is live on PickAPlugin: https://pickaplugin.com/p/a-good-sign\n\n"
            "If you want a free badge, it's at https://pickaplugin.com/badge/a-good-sign.svg. "
            "Reply if anything on the listing needs fixing.\n\n"
            "Aaron, PickAPlugin"
        ),
    ),
]

dnc = json.load(open(f'{R}/launch/do-not-contact.json'))['entries']
dnc_e = {e.lower() for d in dnc for e in d.get('emails', [])}
dnc_d = {x.lower() for d in dnc for x in d.get('domains', [])}
log = json.load(open(f'{R}/launch/resend-send-log.json'))

already = set()
for e in log:
    if str(e.get('type', '')).startswith('submission-reply') or str(e.get('key', '')).startswith('submission-reply'):
        already.add((e.get('to') or '').lower())
        already.add((e.get('email') or '').lower())
        key = e.get('key') or ''
        if key.startswith('submission-reply-'):
            already.add(key[len('submission-reply-'):])

results = []
for m in M:
    domain = m['to'].split('@')[1].lower()
    if m['to'].lower() in dnc_e or domain in dnc_d or m['slug'] in already or m['to'].lower() in already:
        print('SKIP', m['to'], m['slug'])
        results.append(('skip', m['to'], m['slug'], None))
        continue
    payload = json.dumps({
        "from": "PickAPlugin <hello@pickaplugin.com>",
        "to": [m['to']],
        "reply_to": "hello@pickaplugin.com",
        "subject": m['subject'],
        "text": m['text'],
    }).encode()
    rid = None
    err = None
    for _ in range(3):
        try:
            req = urllib.request.Request(
                "https://api.resend.com/emails",
                data=payload,
                headers={
                    "Authorization": "Bearer " + KEY,
                    "Content-Type": "application/json",
                    "User-Agent": "pickaplugin/1.0",
                },
            )
            rid = json.load(urllib.request.urlopen(req, timeout=30))['id']
            break
        except Exception as e:
            err = sanitize(e)
            time.sleep(3)
    now = datetime.datetime.now().isoformat(timespec='seconds')
    if rid:
        print('sent', m['to'], rid)
        log.append(dict(
            key='submission-reply-' + m['slug'],
            to=m['to'],
            email=m['to'],
            subject=m['subject'],
            time=now,
            date=TODAY,
            type='submission-reply',
            status='sent',
            id=rid,
        ))
        results.append(('sent', m['to'], m['slug'], rid))
    else:
        print('FAILED', m['to'], err)
        results.append(('failed', m['to'], m['slug'], err))
    time.sleep(0.7)

json.dump(log, open(f'{R}/launch/resend-send-log.json', 'w'), indent=1)
print('DONE', results)
