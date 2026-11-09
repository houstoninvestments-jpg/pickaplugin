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
