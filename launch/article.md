# X Article #1 for @PickAPlugin

## Packaging (planned first)
- **Title, sells the dream:** "How I tell if a ChatGPT or Codex plugin is worth installing in about 2 minutes"
- **Banner, answers "why should I trust these guys?":** `launch/article-banner.png` (1500x600). A real crop of our /call-me page with hand circles on Checked on, Last push and License, plus the note "we check these on every single plugin". It shows the receipts and doesn't promise anything.
- **Intro, answers "isn't it just the one with the most stars?":** it opens on the stars numbers.
- None of the three overlap: title = speed/outcome, banner = proof we actually check, intro = stars aren't enough.

All numbers are from data/plugins.json (345 plugins, pulled Oct 27, 2026).

---

## Title
How I tell if a ChatGPT or Codex plugin is worth installing in about 2 minutes

## Body

Most people pick a plugin by stars. I get it, I did too.

But out of the 337 plugins in our directory that we could check stars for, 191 have fewer than 10. Only 12 have over 1,000. So if stars are your filter you're basically picking from 12 things and ignoring a ton of stuff that works fine.

I've been going through these one by one for pickaplugin.com, so here's what I actually look at now. Nothing fancy.

**First, when was it last touched**

This is the first thing I check, before I even read what it does. Plugins break when ChatGPT or Codex changes something, and if nobody's around to fix it you're stuck.

Good news here honestly. 243 of the 337 had a push to GitHub in the last 30 days. Only 13 hadn't been touched in over 6 months. This whole space is new so most stuff is fresh, but that also means a plugin that went quiet for 6 months is kind of a big deal.

And 7 of them are flat out archived. The author put up the "I'm done" sign. Skip those unless you plan on forking it.

**Then the license**

Boring but it matters if you're using this at work. 267 are MIT, 38 are Apache 2.0, a few are GPL or AGPL.

35 have no license at all. People think no license means free for anyone, it's actually the opposite. Technically you don't have the right to use it. Usually the author just forgot, so I'll open an issue and ask, but I won't put it in anything for a client until they answer.

AGPL is the other one to notice. Only 2 in our list, but if you're building something you sell, read up first.

**Can I actually install it**

You'd be surprised. 111 out of 345 don't have an install command anywhere we could copy from the readme. Sometimes that's fine, it's a template or a pack of prompts. Sometimes it means "clone this, figure it out."

When there is a command I read it before pasting it. A lot of these are something like

claude mcp add --transport http call-me https://callmemcp.com/mcp

which means you're talking to someone else's server. That's not bad. It just means your stuff goes to them, so I look at who runs it. Plugins that run locally I worry about less.

**The red flags that make me close the tab**

A readme that's mostly hype and no screenshots or examples.
Asks for way more access than it needs for what it does.
Hosted server with no privacy note and no idea who's behind it.
A paid app hiding behind a "free" plugin and you only find out at step 4. (Not always a dealbreaker. The /call-me one is upfront about its paid iPhone app, which I respect.)
No license plus no activity. One of those is fine, both is a no.

**Stars last**

I do look at stars, just last. Under 10 stars plus a recent push plus a clear license is usually just new, not bad. Plenty of the best ones we found are tiny.

**That's it**

Last push, license, install command, red flags, then stars. Takes me about 2 minutes per plugin once you get used to it.

We do this for every plugin on pickaplugin.com and put the results right on the page, so you can see last push, license, stars and the install command without opening GitHub. It's hand sorted, no algorithm ranking things, and we're not affiliated with OpenAI. Go poke around: pickaplugin.com

If you made one of these plugins, you can list it free, or if it's already on there, claim your listing and fix anything we got wrong. Takes a minute.

---

## Quote-tweet angles (post on later days, quote the article)

**QT 1 (dream: stop wasting an afternoon on a dead plugin)**
7 of the plugins we track are archived. their authors literally gave up on them and they still show up in lists.
here's how to spot that stuff before you install

**QT 2 (objection: "this sounds like a lot of work")**
ok it's not actually a process, it's 4 things you check in order. last push, license, install command, red flags. 2 minutes.
we already did it for 345 of them if you'd rather skip it

**QT 3 (objection: "is it safe to use at work?")**
35 ChatGPT/Codex plugins in our list have no license at all. which means you technically can't use them, at work or anywhere.
wrote up what I check before anything goes near a real project
