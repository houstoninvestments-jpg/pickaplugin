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
2026-11-02 09:56 PT: backlink outreach to Agent Skills Index by BranoLabs (skills.branolabs.com) <hello@branolabs.com> "Your Codex plugins page" -> sent 01a19d67-ac18-75b6-b3bf-92e94533e776
2026-11-02 09:56 PT: backlink outreach to TurboAI (turboai.dev) <alex@turboai.dev> "Your Codex CLI plugins reference" -> sent 01a19d67-acb0-7745-87e2-b631e9eac893
2026-11-02 09:56 PT: backlink outreach to MCP.Directory (mcp.directory) <hello@mcp.directory> "Link swap idea: MCP.Directory + PickAPlugin" -> sent 01a19d67-ad14-77e3-8be2-59c320cfba19
2026-11-02 09:56 PT: backlink outreach to DataNorth (datanorth.ai) <info@datanorth.ai> "Your best ChatGPT plugins post" -> sent 01a19d67-adc9-7114-be49-3656c647576d
2026-11-02 09:56 PT: backlink outreach to Swarmnest (swarmnest.ai) <hello@swarmnest.ai> "Swarmnest + PickAPlugin" -> sent 01a19d67-ae6b-77a8-b7b6-262323e5ba28
2026-11-02 09:56 PT: backlink outreach to OpenAgentSkill (openagentskill.com) <qudongqi2023@gmail.com> "Your skills report + our Codex plugin data" -> sent 01a19d67-aefc-7cb4-9d61-3861ea847d52
2026-11-02 09:56 PT: backlink outreach to Best AI Agent Tools (bestaiagenttools.com) <bestaiagenttools@gmail.com> "Research note for your Codex skills guide" -> sent 01a19d67-af8b-7022-a017-ba0c1991d41f
2026-11-02 09:56 PT: backlink outreach to Skiln (skiln.co) <hey@skiln.co> "Skiln + PickAPlugin link swap?" -> sent 01a19d67-afef-76b3-8a48-859522fa3f97
2026-11-03 09:59 PT: backlink outreach to Lukes Lu blog (ilukes.com) <lukes.lu@yahoo.com> "Your 10 essential Codex plugins post" -> sent 01a1a291-5f16-74bc-9c0c-7a5117b15eae
2026-11-03 09:59 PT: backlink outreach to AgentSkillsDir (agentskillsdir.com) <contact@agentskillsdir.com> "Source-checked plugin data you might like" -> sent 01a1a291-5fb0-72da-abfd-ca61d0d6f5a7
2026-11-03 09:59 PT: backlink outreach to VibeCoding Newsletter (vibecodingnewsletter.com) <contact@vibecodingnewsletter.com> "A possible tools item for VibeCoding Newsletter" -> sent 01a1a291-6086-771a-84ee-5146d2fd6628
2026-11-03 09:59 PT: backlink outreach to MCP Newsletter (mcpnewsletter.com) <contact@mcpnewsletter.com> "Codex plugin data for a future issue" -> sent 01a1a291-6107-7137-93c2-f57a89dd0e05
2026-11-03 09:59 PT: backlink outreach to claudecodexplugins (claudecodexplugins.com) <support@claudecodexplugins.com> "claudecodexplugins + PickAPlugin" -> sent 01a1a291-61c4-7efd-a684-aa30d83dc3ec
2026-11-03 10:00 PT: thread reply (thanks) to BranoLabs <hello@branolabs.com> "Re: Your Codex plugins page" -> sent 01a1a291-8c95-7412-83fd-e9e8832d0333
2026-11-04 09:53 PT: backlink outreach to Agent Plugins Directory by Ellelion (agentpluginsdirectory.com) <info@ellelion.com> "Your plugin.json census + our Codex plugin data" -> sent 01a1a7b1-a8de-70da-a7ee-b4145d187944
2026-11-04 09:53 PT: backlink outreach to Agent Plugins Directory by Ronny Badilla (agent-plugins.directory) <info@ronnybadilla.com> "agent-plugins.directory + PickAPlugin" -> sent 01a1a7b1-a975-751d-b67f-97c8706ca1fb
2026-11-04 09:53 PT: backlink outreach to MCPNav (mcpnav.net) <hello@mcpnav.net> "Codex plugin data for your field guides" -> sent 01a1a7b1-aa06-763d-8c2d-76082b340f75
2026-11-04 09:53 PT: backlink outreach to Agent Skills Hub (agentskillshub.dev) <support@agentskillshub.dev> "Security-ish data on 339 Codex plugins" -> sent 01a1a7b1-aab3-7cf8-b4e3-512dcef945b3
2026-11-04 09:53 PT: backlink outreach to agent-toolbox by Yunseo Kim (github.com/yunseo-kim/agent-toolbox) <contact@yunseo.kim> "Free listing for agent-toolbox on PickAPlugin" -> sent 01a1a7b1-ab2b-755b-aa5d-90ed65c13a66
2026-11-05 09:54 PT: backlink outreach to ChatGPT Plugins Directory (chatgptpluginsdirectory.com) <info@chatgptpluginsdirectory.com> "chatgptpluginsdirectory.com + PickAPlugin" -> sent 01a1acd9-62c2-7d13-b947-f46d6660dbdc
2026-11-05 09:54 PT: backlink outreach to Atlas Cloud (atlascloud.ai Codex plugins roundup) <support@atlascloud.ai> "A data source for your Codex plugins roundup" -> sent 01a1acd9-6330-77e8-828c-45f17f0fa406
2026-11-05 09:54 PT: backlink outreach to Awesome Codex Skills by Composio (github.com/composio-community/awesome-codex-skills) <support@composio.dev> "PickAPlugin for the Awesome Codex Skills resources?" -> sent 01a1acd9-648f-781c-84b2-6252f772b143
2026-11-05 09:54 PT: backlink outreach to Glama MCP (glama.ai) <frank@glama.ai> "Codex plugin data that might fit Glama" -> sent 01a1acd9-653d-77b3-8fd4-1fb324e61c4b
2026-11-05 09:54 PT: backlink outreach to GoodSender (blog.goodsender.com) <support@goodsender.com> "Free listing for GoodSender's Codex MCP" -> sent 01a1acd9-65cc-7b21-aa14-cea0ec8e7562
2026-11-05 09:54 PT: backlink outreach to ManyCP (manycp.com) <hello@manycp.com> "PickAPlugin for ManyCP's directory list?" -> sent 01a1acd9-6654-71af-9cb4-16fb9b938ada
2026-11-05 09:54 PT: backlink outreach to awesome-codex-mcp-servers by Kuber Mehta (github.com/Kuberwastaken/awesome-codex-mcp-servers) <kuberhob@gmail.com> "Your awesome-codex-mcp-servers list" -> sent 01a1acd9-66f4-76e9-ae93-858283460d18
2026-11-05 09:54 PT: backlink outreach to MCP Market (mcpmarket.com) <support@mcpmarket.com> "MCP Market + PickAPlugin" -> sent 01a1acd9-6794-7581-9184-ebc5dd38b633
2026-11-05 09:54 PT: backlink outreach to MCPfinder (mcpfinder.org) <hello@mcpfinder.org> "MCPfinder + PickAPlugin" -> sent 01a1acd9-682e-7ef7-b3e1-96f654839186
2026-11-05 09:54 PT: backlink outreach to Manufact (manufact.com MCP blog) <support@manufact.com> "Data tip for your Codex + ChatGPT MCP post" -> sent 01a1acd9-68c3-7cdb-8df5-9be98ac04a51
