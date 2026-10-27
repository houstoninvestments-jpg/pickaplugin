# Research pitches: State of Codex Plugins 2026
Report: https://pickaplugin.com/research/state-of-codex-plugins-2026
CSV (CC BY 4.0): https://pickaplugin.com/research/state-of-codex-plugins-2026.csv
Data pulled Oct 27, 2026 (PT). NOT SENT. Contact routes checked Oct 27, 2026. Send from hello@pickaplugin.com, one outlet per email, plain text, no attachments.
Every number below is from research/stats.json. If you re-run the analysis, re-check the numbers before sending.

## Key numbers (n = 339 GitHub repos from a 346-plugin catalog)
- 329 of 339 (97%) created in 2026; 168 (50%) pushed in the last 7 days
- Median 6 stars; 52 have zero; top 10% of repos hold 94% of all 97,833 stars
- 105 (31%) have no copyable install command in the README
- 28 (8%) have unclear licensing: 6 no license file, 22 a file GitHub can't identify. 268 (79%) are MIT
- 55 (16%) not pushed in 90+ days, 13 in 180+, 7 archived
- 145 (43%) READMEs mention an API key or token; 61 (18%) wire up a remote HTTP/SSE MCP server (keyword heuristics)
- 274 plugin.json files checked: all valid JSON, 3 with hard errors, 23 with at least one warning
- 209 (62%) also ship a Claude Code manifest, so most "Codex plugins" are cross-host
- 50 (15%) have no primary language, meaning they're basically Markdown skills and config

---
## 1. Ars Technica
Route: news@arstechnica.com (general news submissions, per arstechnica.com/features/2003/10/welcome). Story ideas also: Eric Bangeman, eric@arstechnica.com.
Best angle: concentration + "you're installing a stranger's code"
Subject: Data: 339 Codex plugin repos, median 6 stars, 43% want an API key

Hi Ars team,
I run PickAPlugin, a small independent directory of ChatGPT and Codex plugins. We pulled GitHub data on all 339 plugin repos in our catalog this week. A few things stood out: 97% were created this year, the median repo has 6 stars while the top 10% hold 94% of all stars, and 43% of READMEs ask for an API key or token. So most of what people install is a weekend project from one person, often wired to their keys.
Methodology, limits and a CC BY CSV are here: https://pickaplugin.com/research/state-of-codex-plugins-2026
Happy to share the per-repo data if useful.
Aaron, PickAPlugin

## 2. The New Stack
Route: AI senior editor Frederic Lardinois, frederic@thenewstack.io (his announced address); general editorial@thenewstack.org. Guest bylines are paused (contributions page, Jul 17 2026), so pitch this as a news tip, not a byline.
Best angle: cross-host ecosystem forming fast
Subject: Tip: 62% of Codex plugins also ship a Claude Code manifest

Hi Frederic,
Quick data tip for your AI dev tools coverage. We looked at 339 open-source Codex plugin repos. 97% were created in 2026, half got a push in the last week, and 62% also ship a Claude Code manifest, so plugins are turning into a cross-host format pretty fast. The flip side: 31% have no copyable install command, and 16% have already gone quiet for 90+ days.
Full write-up and CSV (CC BY): https://pickaplugin.com/research/state-of-codex-plugins-2026
Aaron, PickAPlugin

## 3. InfoQ
Route: editors@infoq.com (editorial address on infoq.com/guidelines). News is written by InfoQ editors, so this is a tip for them, not an article submission.
Best angle: maturity/quality signals for architects
Subject: News tip: what 339 Codex plugin repos look like (open data)

Hi InfoQ editors,
In case it's useful for a news item on the agent plugin ecosystem: we analyzed 339 open-source ChatGPT/Codex plugin repos. Manifests are in decent shape (274 plugin.json files, all valid JSON, only 3 hard errors), but install docs aren't: 31% have no install command in the README. 28 repos (8%) have no license or one GitHub can't identify. Methodology and limits are on the page, CSV is CC BY.
https://pickaplugin.com/research/state-of-codex-plugins-2026
Aaron, PickAPlugin

## 4. DevClass
Route: devclass@sitpub.com (devclass.com/contact-us)
Best angle: maintenance decay in a brand new ecosystem
Subject: Data: 16% of Codex plugins already quiet for 90+ days

Hi DevClass team,
We track ChatGPT and Codex plugins and just pulled GitHub data on 339 of them. Nearly all were created this year, yet 55 (16%) haven't had a push in 90+ days and 7 are archived. Median stars is 6. 43% of READMEs mention an API key or token, and 18% point your agent at a remote MCP server. Free to use with credit:
https://pickaplugin.com/research/state-of-codex-plugins-2026
Aaron, PickAPlugin

## 5. Simon Willison (simonwillison.net)
Route: no email listed. His about page lists @simonw on X, simonwillison.net on Bluesky, @simon@simonwillison.net on Mastodon. Best is a public post that tags him, not a DM. Only send if it's genuinely interesting to him; don't follow up.
Best angle: the data itself + skills-as-Markdown
Draft (Bluesky/X reply-style post):
Pulled GitHub data on 339 Codex plugin repos. 15% have no primary language at all, they're just Markdown skills and config. Median 6 stars, top 10% hold 94% of stars, 43% of READMEs ask for an API key. CSV is CC BY if you want to poke at it: https://pickaplugin.com/research/state-of-codex-plugins-2026 @simonw

## 6. TLDR (TLDR AI / TLDR Dev)
Route: editor-curated, no public form. A TLDR staffer said on the DevRel Roundtable podcast (developerrelations.com) that you can email submissions@tldr.tech. That address isn't on tldr.tech itself, so treat it as unconfirmed. Ads are separate (advertise.tldr.tech), don't go there.
Subject: Submission: State of Codex Plugins 2026 (open data, 339 repos)
Hi TLDR team, possibly useful for TLDR AI or Dev: open data on 339 ChatGPT/Codex plugin repos. Median 6 stars, top 10% hold 94% of stars, 31% have no install command, 43% ask for an API key. https://pickaplugin.com/research/state-of-codex-plugins-2026 Thanks, Aaron

## 7. Changelog News
Route: changelog.com/news/submit (form; they welcome submitting your own work, no commercial pitches). Form submission = an external submission, needs the same OK as an email.
Best angle: open data for devs
Title: State of Codex Plugins 2026: open data on 339 plugin repos
Why it's newsworthy: First data pass on the new ChatGPT/Codex plugin ecosystem. 97% of repos created this year, median 6 stars, 31% with no install command, 62% also shipping a Claude Code manifest. Methodology and limits documented, CSV under CC BY.

## 8. Console.dev (weak fit, optional)
Route: hello@console.dev (console.dev/selection-criteria). They review dev tools, not reports, so pitch the free plugin.json validator and mention the report as context.
Subject: Free plugin.json validator for Codex plugins
Hi David, we built a free, no-signup plugin.json checker for ChatGPT/Codex plugins (https://pickaplugin.com/tools/plugin-json-validator). We ran it against 274 real manifests for our State of Codex Plugins report: only 3 had hard errors, but 23 had warnings like a missing $schema or version. Might fit Console if you cover agent tooling. Aaron, PickAPlugin

---
## X post drafts (@PickAPlugin, standalone, no hashtags)
1. We pulled GitHub data on 339 ChatGPT and Codex plugins. The median one has 6 stars. The top 10% have 94% of all the stars. Most of what you install is one person's side project, so read the repo first.
https://pickaplugin.com/research/state-of-codex-plugins-2026

2. 97% of the Codex plugins we track were created this year. 16% have already gone 90+ days without a push. The ecosystem is brand new and already has ghost towns.
https://pickaplugin.com/research/state-of-codex-plugins-2026

3. Checked 339 plugin repos for an install command in the README. 105 don't have one. If you make a plugin, one copy-paste line in a code block is the cheapest win you've got. Full data (free CSV): https://pickaplugin.com/research/state-of-codex-plugins-2026
