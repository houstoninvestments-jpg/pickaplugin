# Value posts (jab jab jab, right hook) — @PickAPlugin
Ratio: 23 JAB / 7 HOOK, interleaved. Numbers come from data/plugins.json (343 plugins, stars checked on 336, pulled 2026-10-25/26). Opinions are labelled as opinions by tone, never as data.
Threads: parts marked 1/n. Post a thread as a reply chain.

## V1 [JAB]
Hot take: the best agent plugin is the one that stops your agent from doing something.

Blocking secret reads, gating deploys, refusing to touch main. Capabilities are cheap. Guardrails are the scarce thing.

## V2 [JAB]
We pulled GitHub stars for 336 Codex/ChatGPT plugins.

Median: 6 stars.
191 have fewer than 10.
Only 12 have more than 1,000.

Stars measure marketing, not usefulness. Most of the good stuff is sitting at 6.

## V3 [JAB]
Before you install an MCP server, ask 3 questions:

1. What can it read?
2. What can it write or send?
3. Where does the data go?

If the README can't answer all three in one screen, don't install it.

## V4 [HOOK]
That's why we built PickAPlugin: 343 Codex & ChatGPT plugins sorted by what they do, each linked to its source so you can check those 3 answers yourself.

Free, no signup.
pickaplugin.com

_Image: launch/graphics/v-catalog.png_

## V5 [JAB]
43 of our 343 plugins exist to give agents memory. 18 exist to tell you how much of your usage plan is left.

That's the real state of agent tooling: people are fighting forgetfulness and rate limits, not building sci-fi.

_Image: launch/graphics/v-pains.png_

## V6 [JAB]
Mistake I see constantly: installing 15 MCP servers "just in case."

Every tool you add is description text the model reads and another chance to pick the wrong tool. Fewer tools, better choices. Prune monthly.

## V7 [JAB]
1/4 How to pick an agent memory plugin without wasting a weekend:

2/4 Decide where memory lives. Local files you can read and git-diff beat a hosted black box for most solo devs.

3/4 Check if it can forget. Stale memory is worse than none: the agent confidently follows last month's decisions.

4/4 Test it on one repo for a week before you trust it. We list 43 to compare: pickaplugin.com/c/memory-context

## V8 [HOOK]
Built a Codex or ChatGPT plugin? It's probably already in our catalog. Search for it.

Wrong description? We fix it free. Want it in front of more people? Paid spots exist and are always labelled paid: pickaplugin.com/advertise

## V9 [JAB]
Overhyped: "autonomous agent runs for 8 hours."

Underhyped: an agent that leaves a clean log of what it did, what it skipped and what it needs from you. Plugins like Nightshift get this. The morning review is the product.

## V10 [JAB]
The underrated plugin category: read-only.

17 plugins in our catalog describe themselves as read-only. They inspect, summarize, recommend. Zero blast radius. Start there before you hand anything write access.

## V11 [JAB]
Your agent can probably read your .env right now.

Not because it's malicious. Because "read the project" includes it. Mask secrets at the hook level, not with a polite instruction in AGENTS.md.

## V12 [HOOK]
We keep a Security & Governance shelf for exactly this. 11 plugins: secret masking, policy hooks, security tooling.

Short shelf, high stakes.
pickaplugin.com/c/security-governance

## V13 [JAB]
109 of 343 plugins in our catalog mention MCP.

MCP won the plumbing war quietly. The interesting fight now is above it: discovery, trust, and which tool the model actually picks.

## V14 [JAB]
60 plugins in our "Codex & ChatGPT" catalog also mention Claude.

Builders aren't picking a side. They're building for whichever agent you already use. If your plugin only works in one, you're leaving users on the table.

## V15 [JAB]
How to write a plugin description an agent (and a human) will actually pick:

- First line: the verb. "Blocks", "searches", "deploys".
- Second: what it touches. Files, network, accounts.
- Third: what it never does.

"AI-powered productivity layer" tells nobody anything.

## V16 [HOOK]
We hand-wrote one-line descriptions for all 343 plugins so you don't have to read 343 READMEs.

12 shelves. One page per plugin. Every page links the repo.
pickaplugin.com

## V17 [JAB]
Hot take: "agent orchestration" plugins are the new todo apps.

Agent Workflows is our biggest shelf at 85 plugins. Everyone builds one, few get used. If you're building in AI tooling, the emptier shelves (Data & Backend has 8) are the opportunity.

_Image: launch/graphics/v-shelves.png_

## V18 [JAB]
The most useful thing an agent can do when stuck is stop and ask you.

Not retry 40 times. Not hallucinate a workaround. Ping you on Telegram or your phone, wait, continue. Plugins for this exist (Agentgram, /call-me). Use one.

## V19 [JAB]
52 plugins in our catalog have zero GitHub stars. Some of them are good.

If you only browse "awesome" lists sorted by stars, you're seeing the best marketers, not the best tools.

## V20 [HOOK]
That's the whole point of PickAPlugin: sorted by what a plugin does, not how loud its launch was. Editor's picks are never for sale.

pickaplugin.com

## V21 [JAB]
Rate limit mid-task is the most expensive moment in agent coding. You lose the context, not just the time.

Fix: track usage pace, not usage total. "At this pace I run out Thursday" is actionable. "62% used" isn't.

## V22 [JAB]
1/3 Mistakes we see in plugin READMEs, ranked:

2/3 No install command above the fold. No list of what it can access. Demo GIF of a todo app.

3/3 And the worst: no "when NOT to use this." The best READMEs tell you when to walk away. That's when we trust them.

## V23 [JAB]
Agent handoff is the next big category and nobody has nailed it.

Pasting context from Codex into another window is how most people do it today. A few plugins (Magents, Agent Message Queue) are trying shared buses. Watch this space.

## V24 [HOOK]
Makers: if your plugin is in our catalog, a $9/mo Verified badge says you claimed the listing and keep it current. That's it. No ranking boost.

Free listings stay free.
pickaplugin.com/advertise

## V25 [JAB]
Opinion: local-first is the default for dev tools now.

59 of 343 plugins in our catalog mention running locally. If your tool ships my code to your server, the README should say why in the first paragraph.

## V26 [JAB]
The cheapest code review upgrade: make the agent write the spec before the code.

Requirements → design → tasks, each one approved by you. It feels slow. It's faster than reviewing 600 lines that solved the wrong problem.

## V27 [JAB]
Underrated plugin type: the ones that write your standup.

Your agent history plus git log already knows what you did this week. Let it draft the recap. Edit, don't write.

## V28 [HOOK]
New here? Start with the shelf that matches your pain:

Secrets → /c/security-governance
Forgetful agent → /c/memory-context
Hitting limits → /c/usage-quotas
Shipping → /c/deploy-devops

All on pickaplugin.com, free.

## V29 [JAB]
7 plugins in our catalog are already archived on GitHub. The ecosystem is months old.

Before you build your workflow around a plugin, check last commit date and open issues. Abandonware moves fast in AI tooling.

## V30 [JAB]
What's the one plugin or MCP server you'd actually miss tomorrow?

Not the one you starred. The one you use. Best answers go in our next roundup (with credit).
