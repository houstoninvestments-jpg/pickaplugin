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
2026-10-28 10:18 PT: backlink outreach to Plugins Radar (pluginsradar.com) <hello@pluginsradar.com> "Your ChatGPT directory tracking + GitHub side data" -> sent 01a18384-f3e0-7d2a-924b-341569e23004
2026-10-28 10:18 PT: backlink outreach to Tried AI Tools (triedaitools.com) <hello@triedaitools.com> "Your ChatGPT plugins directory page" -> sent 01a18384-f4a5-78fd-a2c5-4829522978b7
2026-10-28 10:18 PT: backlink outreach to CodexStacks (codexstacks.com) <hello@codexstacks.com> "Codex plugin data you can cite" -> sent 01a18385-2267-7b2f-8dc8-db1e23489fd0
2026-10-28 10:18 PT: backlink outreach to Codex Harness (codex-harness.com) <contact@codex-harness.com> "Data for your Codex plugin marketplace guide" -> sent 01a18385-23c5-7ef8-9c36-3ffb85bda409
2026-10-28 10:18 PT: backlink outreach to AI Coding Weekly (aicodingweekly.datadriftpress.com) <hello@datadriftpress.com> "A possible item for AI Coding Weekly" -> sent 01a18385-24a5-709d-9d71-8137a33fee35
2026-10-28 10:18 PT: backlink outreach to PulseMCP (pulsemcp.com) <hello@pulsemcp.com> "Codex plugin numbers for the newsletter" -> sent 01a18385-2554-7b39-95ea-76ea89b1bbaa
2026-10-28 10:18 PT: backlink outreach to MCP Agents Market (mcpagentsmarket.com) <hello@mcpagentsmarket.com> "Codex plugins for your Plugins section" -> sent 01a18385-25e4-76e3-b440-a0f97f666e12
2026-10-28 10:18 PT: backlink outreach to MCP Find (mcp-find.org) <hello@mcp-find.org> "Codex plugin data, free to use" -> sent 01a18385-26b2-75dc-bdae-1e2cb647f15a
2026-10-28 10:18 PT: backlink outreach to MCP Select (mcpselect.com) <hello@mcpselect.com> "Some data that fits your testing angle" -> sent 01a18385-2752-76a2-8406-45309fca2d4e
2026-10-28 10:18 PT: backlink outreach to MCP Playground (mcpplaygroundonline.com) <hello@mcpplaygroundonline.com> "Your MCP security scanner + our plugin data" -> sent 01a18385-27fa-73b9-9890-3d07f5c8edec
2026-10-29 10:08 PT: backlink outreach to MCP.so (mcp.so) <support@mcp.so> "Your best MCP servers post" -> sent 01a188a2-bec0-77dc-aefc-7820c572103e
2026-10-29 10:08 PT: backlink outreach to ai101.tools (ai101.tools) <info@dijitalpi.com> "Your October MCP download report" -> sent 01a188a2-bf62-7ce8-8dcc-0cc1b50b0389
2026-10-29 10:08 PT: backlink outreach to ProtocolProbe (protocolprobe.com) <hello@protocolprobe.com> "Your registry checks + our Codex plugin data" -> sent 01a188a2-c004-779d-8082-2c8388f5c3ba
2026-10-29 10:08 PT: backlink outreach to SkillAgent (skillagent.dev) <hello@skillagent.dev> "Your best MCP servers page" -> sent 01a188a2-c099-75ec-86c8-a52facafd27b
2026-10-29 10:08 PT: backlink outreach to Mermail (mermail.app) <contact@mermail.app> "Free listing for Mermail on PickAPlugin" -> sent 01a188a2-c103-7e08-b1a8-b494611eac8b
