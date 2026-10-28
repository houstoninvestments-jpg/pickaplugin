# Outreach email log

2026-10-26 ~2:45 AM PT: NOTHING SENT. Cloudflare Email Sending to arbitrary recipients requires the Workers Paid plan ($5/mo); the user-Cloudflare connector also gets HTTP 401 on all /email/sending endpoints. No test sent.

| # | Maker | To | Status |
|---|---|---|---|
| 1 | Firecrawl | hello@firecrawl.dev | not sent (blocked) |
| 2 | Hashgraph Online | support@hol.org | not sent (blocked) |
| 3 | Dodo Payments | support@dodopayments.com | not sent (blocked) |
| 4 | WaveSpeedAI | support@wavespeed.ai | not sent (blocked) |
| 5 | Droplinked | support@droplinked.com | not sent (blocked) |
| 6 | Tashfeen Ahmed | tashfene@gmail.com | not sent (blocked) |
| 7 | Serge Bulaev | s@bulaev.org | not sent (blocked) |
| 8 | Sealos (labring) | fanux@sealos.io | not sent (blocked) |
| 9 | AgiFlow | vuong@agiflow.io | not sent (blocked) |
| 10 | VOYGR (PlaceCall) | support@voygr.tech | not sent (blocked) |
| 11 | TohmaN233 | postlewildeman113@gmail.com | not sent (blocked) |
| 12 | Valkyr Labs | support@valkyrlabs.com | not sent (blocked) |

## Resend send path (set up 2026-10-27)
Working send path: Resend API, domain pickaplugin.com verified. From "PickAPlugin <hello@pickaplugin.com>", reply-to hello@pickaplugin.com. Key at /workspace/pickaplugin/.secrets/resend_api_key (mode 600, never print). POST https://api.resend.com/emails with Bearer key. Backlink outreach should use this, max 10 a day, check this file + resend-send-log.json for duplicates first.
2026-10-27 8:18 AM PT: research pitches sent to Ars Technica, The New Stack, InfoQ, DevClass, Console.dev (see research-pitches.md).
2026-10-27 10:07 PT: backlink outreach to HOL awesome-codex-plugins (github.com/hashgraph-online/awesome-codex-plugins) <support@hol.org> "PickAPlugin started from your list" -> sent 01a17e55-028f-706c-bf39-bf9fbc6f8951
2026-10-27 10:07 PT: backlink outreach to SkillAudit (skillaudit.dev) <hello@skillaudit.dev> "Your MCP shortlist + our Codex plugin data" -> sent 01a17e55-0424-71f3-8ed2-656551b98275
2026-10-27 10:07 PT: backlink outreach to AgentAtlas Weekly (agentatlas.dev) <hello@agentatlas.dev> "Codex plugin data for a future issue" -> sent 01a17e55-057d-7918-bfca-32d43b0abaf0
2026-10-27 10:07 PT: backlink outreach to Agentic Weekly (theagenticweekly.com) <hello@theagenticweekly.com> "Open data on 339 Codex plugins" -> sent 01a17e55-0622-7cc2-9e98-6f0c47e3f0ad
2026-10-27 10:07 PT: backlink outreach to Mejba Ahmed blog (mejba.me) <mejba.13@gmail.com> "Your Codex plugins review" -> sent 01a17e55-06dd-7c03-b6ed-083c5cacbf90
