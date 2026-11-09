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
