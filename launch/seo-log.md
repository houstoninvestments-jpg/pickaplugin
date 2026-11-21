# PickAPlugin SEO log

Rules: dated entries, at most one title change per page (wait for data before changing again), brand query "pickaplugin" filtered out. Judge pages by clicks that lead to /submit or featured checkout, not just impressions.

## 2026-11-02 (Monday review)

**Data:** GSC export launch/gsc-exports/gsc-2026-11-02/ (last 28 days) + Bing (bing-2026-11-02-*.csv). Brand query excluded.

Quick wins seen (non-brand):
- "best backend for openai codex": 16 impressions, position 6.4, 0 clicks. /best/data-backend averages position 4.4.
- /c/agent-workflows: 72 impressions, position ~13, 3 clicks (in the 11–20 refresh band).
- Homepage: 83 impressions, position 6.7, 0 clicks.
- "data product builder" 17 impressions @ 17.7; "codex auto resume" 10 @ 9.5; "devin plugins" 6 @ 9.2.
- /guides/install-codex-plugin: 48 impressions @ ~31.
- Bing: "codex plugins" / "best codex plugins" cluster at positions 5–10; 7 AI citations.

Changes shipped:
- TITLE CHANGE /best/data-backend
  - old: "Best Data & Backend plugins for ChatGPT & Codex (10 ranked) — PickAPlugin"
  - new: "Best backend & database plugins for OpenAI Codex and ChatGPT (10 ranked) — PickAPlugin"
  - why: match "best backend for openai codex" (pos 6.4, 0 CTR). Re-check on 2026-11-16; don't change it again before then.
- NEW PAGE /guides/publish-codex-plugin: buyer-intent page for makers. Targets "publish codex plugin", "submit codex plugin" and "submit chatgpt app" (all in Google autocomplete), plus "codex plugin marketplace github". Covers the OpenAI submission portal (facts from OpenAI docs, checked Nov 2), repo marketplaces and free directories, and links to /submit and /badge. Linked from /submit, /faq and /guides.

Next week: refresh /c/agent-workflows (position 13) and look at the homepage CTR (title/description).

## 2026-11-09 (CEO weekly review)
- NEW LISTING PAGES /p/agent-craft, /p/easi-run, /p/call-grokbot (maker requests via X and email). In sitemap; IndexNow pinged 567 URLs after deploy (200).
- COPY (conversion, not ranking): every non-featured /p/ page's "Is this your plugin?" line now shows the founding featured rate ($29/mo for life, first week free, N of 10 left); /submit gained a "Want it seen first?" block; /claimed thank-you page mentions the founding offer. No title/description changes, so no GSC re-check needed for these.

## 2026-11-09 (Monday GSC meeting)

**Data:** launch/gsc-exports/2026-11-09-Queries.csv + 2026-11-09-Pages.csv (last 28 days: 28 clicks, 1.51K impressions, avg position 16.9). Brand "pickaplugin" excluded. Code: scripts/seo_overrides.py (title overrides + content injections, applied in build_seo.py). Check date for everything below: **2027-02-07** (90 days), first title-CTR glance 2026-11-23.

Not due / left alone:
- /best/data-backend title changed 2026-11-02, too soon to judge. "best backend for openai codex" went 16 impr @ 6.4 → 46 impr @ 7.0, still 0 clicks. No title change; content and links only (below). Re-check 2026-11-16 as planned.
- /blog/best-codex-plugins-november-2026 is the only page with Bing AI citations, so it wasn't touched.

Job 1, quick wins (non-brand, positions 5–20):
- /best/data-backend: CONTENT. Added "What is the best backend for OpenAI Codex?" answer (Cohesivity, host0, crw, Dex, data product builder, VillageSQL), linking to each. New internal link from /c/data-backend with anchor "best backend plugins for OpenAI Codex".
- TITLE CHANGE /p/codex-auto-resume (page 64 impr @ 7.1, 2 clicks; "codex auto resume" 22 @ 8.6, 0 clicks)
  - old: "Codex Auto Resume — PickAPlugin"
  - new: "Codex Auto Resume: continue Codex after usage limits reset (Windows) — PickAPlugin"
  - plus a "How Codex auto resume works" section summarized from the README, and links from /c/usage-quotas and /best/usage-quotas.
- TITLE CHANGE /p/data-product-builder-for-dbt (page 35 impr @ 19.6; "data product builder" 33 @ 20.4)
  - old: "Data Product Builder for dbt — PickAPlugin"
  - new: "Data Product Builder for dbt: Codex & Claude Code skills — PickAPlugin"
  - plus a "What this data product builder does" section (7 skills, requirements, Codex install) and links from /best/data-backend and /c/data-backend.
- TITLE CHANGE /p/devin-plugin-cc (page 13 impr @ 15; "devin plugins" 6 @ 9.2, "devin plugin" 2 @ 10.5)
  - old: "Devin Plugin CC — PickAPlugin"
  - new: "Devin Plugin CC: Devin plugins for Codex & Claude Code — PickAPlugin"
  - plus a "Devin plugins for Codex and Claude Code" section (features, requirements, install), and a link from /c/agent-workflows with anchor "Devin plugins for Codex".
- TITLE CHANGE /guides/where-to-submit-mcp-server (page 29 impr @ 15.2; "mcp server directory" 8 @ 23)
  - old: "Where to submit your MCP server (2026): every registry and directory — PickAPlugin"
  - new: "MCP server directory list (2026): where to submit your MCP server — PickAPlugin"
  - plus internal links with anchor "MCP server directory" from /alternatives and /guides/publish-codex-plugin.
  - Small numbers (under 100 impressions a month) on all four of these. Treat them as signals, not verdicts.

Job 2, titles (low CTR for the position):
- TITLE CHANGE / (home: 190 impr @ 7.9, 1 click, 0.53% CTR)
  - old: "PickAPlugin — an independent catalog of ChatGPT & Codex plugins"
  - new: "Codex & ChatGPT Plugin Directory (2026): 450+ plugins — PickAPlugin" (count rounded down to 50 by the build)
  - meta description now: "A free, independent directory of 450+ Codex plugins, ChatGPT apps and the MCP servers they bundle…"
  - why: lead with the search ("plugin directory chatgpt", "mcp directory", "codex plugins" land here), a count promise and the year. Brand moved to the end.

Job 3, page-two giant:
- /c/agent-workflows (122 impr @ 14.5, 4 clicks): LINKS + intro, NO title change. Added a short intro paragraph to the category page, and 5 new internal links with the exact anchor "agent workflow plugins" from /best/agent-workflows, /p/devin-plugin-cc, /guides/install-codex-plugin, /faq (new "Where should I start?") and /guides. Next step if it's still on page two in 4–6 weeks: outside links straight to this URL.

Bing (Webmaster Tools, AI Performance): 16 AI citations, all on /blog/best-codex-plugins-november-2026. None since Nov 2. No grounding queries available. Bing search impressions fell to about 0/day from Nov 4.
- Quick checks on 2026-11-09, no obvious cause found: robots.txt is "Allow: /" with the sitemap line. sitemap.xml returns 200 (567 URLs live). IndexNow key file returns 200. The blog page returns 200 to a bingbot user agent, has a self canonical and no noindex/X-Robots-Tag. Cloudflare bot fight mode, AI-bot blocking and crawler protection are all off (security level medium, managed free ruleset only).
- Possible soft causes to watch: (1) every build stamps lastmod=today on ~566 of 567 sitemap URLs, and (2) indexnow.py resubmits the whole sitemap after every deploy (often daily) even when pages didn't change. Bing asks for changed URLs only. Next step: send only changed URLs to IndexNow and use real lastmod dates; then check Bing's URL Inspection and crawl stats for the blog page.

## 2026-11-14 (comparison pages at scale + monthly report)
- NEW scripts/build_compare.py (run by build.py): 118 /compare/<a>-vs-<b> (incl. the 10 old URLs, now richer), 105 /alternatives/<slug>, 32 /best-for/<use-case>, hub /compare. TF-IDF description overlap picks pairs; thin-page guards (4+ real alternatives, 5+ matches per use case, max 3 comparisons per plugin). Each page: stars, last push, license, language, packaging, hosts, install command, "who it suits", links to /p, /c, /best. Plugin pages, /c and /best pages link to them. New plugins get pages on the next build.
- Keywords: scripts/fetch_keywords.py (free Google suggestqueries + Bing qsonhs autocomplete) -> data/keywords.json (225 plugins, 216 use-case seeds). Use-case pages come from "best mcp server for …"/"codex plugin for …" suggestions. GSC page-two plugins get priority for alternatives pages when they have 4+ real alternatives.
- NEW /reports/2026-11 (State of MCP & Codex Plugins, month to date through Nov 14) + /reports index. `python3 scripts/make_report.py 2026-11` regenerates data/reports/2026-11.json; re-run on Dec 1 for the final November numbers, then `make_report.py 2026-12` through December.
- IndexNow: indexnow.py now takes path prefixes (`python3 scripts/indexnow.py /compare /alternatives ...`); pinged 285 changed URLs (200).
- Check on 2026-12-14: impressions on /compare, /alternatives, /best-for in GSC; prune any page with 0 impressions after 60 days.

## 2026-11-16 (Monday GSC meeting + traffic-drop diagnosis)

**Data:** launch/gsc-exports/2026-11-16-*.csv (last 28 days Oct 26–Nov 14, Web: 30 clicks, 1.63K impressions, avg pos 16.7). No brand ("pickaplugin") rows in the export. Bing Webmaster Tools was signed out in the box browser, so there's no Bing data this week (no AI Performance or Topic Portfolio review).

**The cliff:** daily impressions were 80–169/day Oct 27–Nov 8, then Nov 9: 12, Nov 10: 2, Nov 11: 3, Nov 12–13: 0, Nov 14: 3. It hits every page at once, so it's site-wide, not a page or title problem. The non-brand query table is almost identical to the Nov 9 export: nothing new was earned this week. Bing went to about 0/day from Nov 4.

Checked on 2026-11-16, nothing blocking found:
- robots.txt: `Allow: /`, `Disallow: /go/` (click redirects only), sitemap line present.
- /, /c/agent-workflows, /p/lurkapi, /sitemap.xml return 200 to Googlebot, bingbot and curl user agents. Self canonical on the apex host, no meta robots noindex, no X-Robots-Tag (only /go/* redirects carry noindex). The only noindex page in dist is the unsent newsletter preview, which is intended.
- Cloudflare: bot fight mode, AI-bot blocking, crawler protection and JS detections are all off. Security level medium, managed free ruleset only. Redirect rules are just www→apex and strip-trailing-slash, unchanged since Oct 27.
- Cloudflare logs, last 24h: real Googlebot (desktop and smartphone) fetched /, robots.txt, /c/*, /p/*, guides and sitemap and got 200s (plus expected 301s from www/trailing slash and two 404s for /ads.txt and /favicon.ico). Not challenged or blocked. Daily edge 403s were normal except Nov 9 (171), which was a one-day blip.
- No deploy Nov 8–10 touched robots, canonicals or headers. The Nov 9 commits were founding-offer copy, five title overrides and internal links.
- Sitemap: 913 valid apex URLs, no duplicates. But 912 of 913 had lastmod = build day, and IndexNow got the whole sitemap after every deploy (913 URLs this morning). That's the Nov 9 Bing follow-up, which had **not** been done until today (fixed below).
- Context: Google's November 2026 core update started Nov 10 (a day after our drop began) and runs to about Nov 24. No spam update in November.

**Most likely cause:** Google has stopped showing the site almost everywhere, either through a site-level quality reassessment of a young domain with about 900 mostly programmatic pages, or through something only Search Console can show (a manual action, a security issue, or "crawled/discovered – not indexed" for most URLs). It isn't a technical block we can see from outside. **Next step (needs the GSC UI):** check Security & Manual actions, the Indexing → Pages trend since Nov 8, and URL Inspection (live test) on / and /c/agent-workflows. Until then, and until the core update finishes (~Nov 24): **no new title changes and no new programmatic page batches.** Per the guide, don't undo work without a named mistake.

**Fixes shipped today:**
- REAL LASTMOD: build_seo.py now gives each page a content signature (text without scripts, digits and whitespace, so star counts and dates don't count as edits), kept in data/lastmod.json. lastmod moves only when a page really changes. Seeded today: /p pages use their first_seen date, compare/alternatives/best-for use 2026-11-14 (when they were created), the rest use today.
- INDEXNOW CHANGED-ONLY: indexnow.py now sends only data/changed_urls.json (URLs whose signature changed today). `--all` is the escape hatch. Today it sent nothing, because the morning redeploy had already sent everything.
- DETERMINISTIC COMPARE PAGES: build_compare.py picked head-to-head pairs and "shared terms" by Python set order, so every build added or dropped a few /compare URLs and rewrote others (7 pages differed between two identical builds). Pairs and terms are now sorted. There are now 120 stable head-to-heads; pages that dropped out 404 as before.

**Job 1/2/3 this week:** not run as changes. With about 0 impressions since Nov 9, there's no fresh signal, and the guide says not to touch titles during a drop or a core update. Nov 9 title changes (home, codex-auto-resume, data-product-builder, devin-plugin-cc, where-to-submit-mcp-server): not due, first glance 2026-11-23. /best/data-backend (changed Nov 2): "best backend for openai codex" 48 impr @ 7.0, 0 clicks, which is the same data as last week, so no verdict.

**Other:** /alternatives gained a SkillMaxx install-test results entry (a link swap SkillMaxx agreed to on Nov 13; they're adding a "Related directories" link to us on their How we test page).
### 2026-11-16 GSC health check (browser, read-only)
- Manual actions: none. Security issues: none.
- Page indexing (report updated 2026-11-12): 86 indexed, 467 not indexed (273 "Crawled - currently not indexed", 191 "Discovered - currently not indexed", 3 redirects).
- URL Inspection of / : "URL is not on Google" — Crawled - currently not indexed (last crawl 2026-11-10, fetch OK, indexing allowed, canonical self).
- Read: Google is dropping the site on quality, not a technical block (likely thin, auto-generated pages plus the Nov core update). Hold off on new generated-page batches; next step is consolidating or noindexing thin /p, /compare and /alternatives pages and making the home page and key hubs more substantial. Re-check on 2026-11-23.
## 2026-11-21 (thin-page cleanup)

**Why:** GSC (reviewed 2026-11-16) showed no manual action, but the homepage and most URLs were "Crawled / Discovered - currently not indexed." Impressions fell to about 0 from Nov 9. Likely cause: a large batch of thin, auto-generated pages (compare, alternatives, best-for, /best duplicates of /c, MCP converter pairs, plus thank-you pages in the sitemap).

**Audit of the then-current build (1,032 sitemap URLs):**
- /p/ listing pages: 659. Keep indexable (they are the catalog). Median ~88 unique non-template words; descriptions are short, but each page has unique project facts.
- /compare/<a>-vs-<b>: 123 pages, ~79% template, median 47 unique non-template words. Thin. 301 to /compare.
- /alternatives/<slug>: 120 pages, ~66% template, median 90 unique non-template words. Thin. 301 to /p/<slug>; similar-plugin lists now sit on the listing page.
- /best-for/<use>: 37 generated use-case pages. 301 to /compare; a few shortlists were inlined on that hub.
- /best/<cat>: 12 pages, near-duplicates of /c/<cat> (almost the same word counts). 301 to /c/<cat>, and the ranked intro moved onto the category hubs.
- /tools/mcp-config-converter/<pair>: 14 near-duplicate converter pages (~90% template). 301 to /tools/mcp-config-converter; pair notes folded into the hub.
- /language/* with fewer than 10 plugins (C#, PowerShell, Swift): dropped; 308 already sent below-gate URLs to /languages. License pages all stayed (min 5).
- Thank-you/form pages (claimed, confirm, confirmed, subscribed, unsubscribed, form-error): noindex, dropped from the sitemap.
- Kept and enriched: homepage (new "How to use this catalog" section), all /c/ hubs (original intro, start-here shortlists, links to guides and sibling shelves), /compare hub, guides, tools, research, blog article.

**Rules now in the build** (refresh.py does not undo them; lastmod still uses _sig from 78f80ca):
- Do not generate new /compare/*, /alternatives/*, /best-for/*, /best/* or converter-pair URL batches.
- Sitemap omits noindex pages. Worker 301s the retired URL patterns (run_worker_first updated).

**Titles:** no homepage or Nov 9 listing-title changes (those are not due). Category pages absorbed the old /best titles so the 301s have a matching heading.

Re-check indexing on 2026-11-23 as planned, then again in early 2027.
