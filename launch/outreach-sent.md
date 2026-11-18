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
2026-11-09 09:53 PT: backlink outreach to The MCP Census (mcpcensus.com) <info@mcpcensus.com> "Codex plugin data for your registries page" -> sent 01a1c171-ffbf-71a0-9884-20b4e950761e
2026-11-09 09:53 PT: backlink outreach to MCPifex (mcpifex.com) <support@amdose.com> "Your best MCP marketplaces page" -> sent 01a1c172-004a-7555-a69f-c1d215d7b352
2026-11-09 09:53 PT: backlink outreach to Codex Skills (codexskills.dev) <hello@codexskills.dev> "Codex Skills + PickAPlugin" -> sent 01a1c172-00c6-751f-af7f-401e978a3933
2026-11-09 09:53 PT: backlink outreach to MCP360 (mcp360.ai) <support@mcp360.ai> "Data for your Codex plugins guide" -> sent 01a1c172-0171-764d-ae6c-47e113a8f5d7
2026-11-09 09:53 PT: backlink outreach to VibeIDE (vibeide.dev) <info@vibeide.dev> "A free tool for your Codex guides" -> sent 01a1c172-01ec-7b16-8dce-9173362d7243

## 2026-11-09 featured-spot sales pitches (founding $29/mo for life + first week free)
- 2026-11-09 JobsPipe -> dvir@jobspipe.dev | JobsPipe featured spot on PickAPlugin? | Resend 01a1c17f-3754-7de2-b2a6-780c8a3be74a
- 2026-11-09 Skycloak MCP -> mariam.soliman@skycloak.io | Skycloak MCP featured spot on PickAPlugin? | Resend 01a1c17f-3ab6-70c7-b21f-bfc7eda9fec0
- 2026-11-09 LurkAPI -> mesmerpercy@gmail.com | LurkAPI featured spot on PickAPlugin? | Resend 01a1c17f-3de2-7c63-9883-2dc1ad73a73f
- 2026-11-09 Arcmira -> zeal@arcmira.com | Arcmira featured spot on PickAPlugin? | Resend 01a1c17f-40ea-7bfc-a223-c13271a13cfc
- 2026-11-09 NeverApply -> hello@neverapply.co | NeverApply featured spot on PickAPlugin? | Resend 01a1c17f-4436-7d65-a153-9adca34c1c1a
- 2026-11-09 call-grokbot -> baley@zens.ai | call-grokbot is live on PickAPlugin | Resend 01a1c17f-475a-7098-9452-2522594c29c6
- 2026-11-09 CRW -> hello@fastcrw.com | CRW featured spot on PickAPlugin? | Resend 01a1c17f-4a82-7612-949c-faaeea8b2e3f
- 2026-11-09 Mobile Dev -> hello@callstack.com | Mobile Dev featured spot on PickAPlugin? | Resend 01a1c17f-4da0-7621-9a0e-a9ba8f901fdb
- 2026-11-09 EXZA Remote -> info@exza.de | EXZA Remote featured spot on PickAPlugin? | Resend 01a1c17f-50cb-7567-bc4f-2e255b2791b4
- 2026-11-09 Canonry -> hello@canonry.ai | Canonry featured spot on PickAPlugin? | Resend 01a1c17f-53c3-7a9a-85a4-3dd34fc7e33a

## 2026-11-10 backlink outreach
- 2026-11-10 Codex Design (codexdesign.io) -> info@codexdesign.io "Codex Design on PickAPlugin" -> sent 01a1c697-ef70-7d6a-9c20-9f3737964bbf
- 2026-11-10 Xtrusio (xtrusio.com) -> hello@xtrusio.com "Your Codex plugins install guide" -> sent 01a1c697-efda-7bac-b10d-41b8dc8b97b2
- 2026-11-10 Blastra (blastra.io) -> ceo@blastra.io "One more for your MCP directories list" -> sent 01a1c697-f047-7ac2-9b88-1bcf6815bf11
- 2026-11-10 Plug and Ship (plugandship.dev) -> hello@plugandship.dev "Your where to submit an MCP server guide" -> sent 01a1c697-f0ea-7eb1-99a6-d9dd433a104a
- 2026-11-10 PlugMCP (plugmcp.ai) -> contact@plugmcp.ai "Your best MCP directories field guide" -> sent 01a1c697-f160-7749-8596-936b0d333899
- 2026-11-10 The Anthropic Stack (theanthropicstack.com) -> theanthropicstack@proton.me "A link for The Queue maybe" -> sent 01a1c697-f19e-717e-8a8f-9ae7fa38995a
2026-11-11 09:57 PT: backlink outreach to Apideck (apideck.com) <hello@apideck.com> "Your MCP directories post" -> sent 01a1cbc2-35e5-7ee8-a422-96a4c9fb4e04
2026-11-11 09:57 PT: backlink outreach to SaaSCity (saascity.io) <support@saascity.io> "MCP server directories page" -> sent 01a1cbc2-3637-7f08-8022-21191b9ca2e9
2026-11-11 09:57 PT: backlink outreach to Left Hook (lefthook.com) <hello@lefthook.com> "Your hosted MCP server listing post" -> sent 01a1cbc2-36a3-7c6d-9eab-059681a26e23
2026-11-11 09:57 PT: backlink outreach to Linkly (linklyhq.com) <support@linklyhq.com> "Your MCP directories roundup" -> sent 01a1cbc2-372d-770b-834b-3c5201e00e63
2026-11-11 09:57 PT: backlink outreach to REVERB (reverbico.com) <david@reverbico.com> "Your MCP directories and registries list" -> sent 01a1cbc2-37a0-7713-8d40-2d082957185c
2026-11-11 09:57 PT: backlink outreach to Gaintage (gaintage.com) <hello@gaintage.com> "Your ChatGPT plugins explainer" -> sent 01a1cbc2-37ef-7cda-a1d3-2b77ed732781
2026-11-11 09:57 PT: backlink outreach to Essen Industries (essenindustries.com) <sales@essenindustries.com> "Your plugins vs apps vs connectors post" -> sent 01a1cbc2-3877-7b3c-9f26-929b2b050543
2026-11-12 09:57 PT: backlink outreach to Frank Spin (frankspin.com) <info@frankspin.com> "Your MCP app store map" -> sent 01a1d0e8-b465-7739-b085-ddbab46c3f07
2026-11-12 09:57 PT: backlink outreach to Yep Soso (yepsoso.com) <support@yepsoso.com> "Your Codex plugins walkthrough" -> sent 01a1d0e8-b4d9-7971-b241-06851acd0fe5
2026-11-12 09:57 PT: backlink outreach to Viraloop (viraloop.io) <hello@viraloop.io> "Your AI plugin directories guide" -> sent 01a1d0e8-b549-799a-99f2-2fdd2098ccb6
2026-11-12 09:57 PT: backlink outreach to SkillMaxx (skillmaxx.gilventures.ai) <skillmaxx@gilventures.ai> "SkillMaxx + PickAPlugin" -> sent 01a1d0e8-b591-7ee7-a6d0-bb0d3b6702e8
2026-11-13 09:55 PT: backlink outreach to Scrape.ly (scrape.ly) <hello@scrape.ly> "Scrape.ly is listed on PickAPlugin" -> sent 01a1d60c-f5c8-79c4-af91-729b540b88f9
2026-11-13 09:55 PT: backlink outreach to AgentShortlist (agentshortlist.dev) <hi@agentshortlist.dev> "Your MCP servers ranking + a data source" -> sent 01a1d60c-f616-7771-8860-2b58cd961c2a
2026-11-13 09:55 PT: backlink outreach to GearPicked (gearpicked.com) <hello@gearpicked.com> "One more route for your MCP submission checklist" -> sent 01a1d60c-f69a-7239-abe3-5f62870fb694
2026-11-13 09:55 PT: backlink outreach to Flaq AI (flaq.ai) <contact@flaq.ai> "Your awesome_codex_skills list" -> sent 01a1d60c-f70d-7c3c-9bd7-6cba3455c9cb
2026-11-13 09:55 PT: backlink outreach to ChatGPT Apps Rank (chatgptappsrank.com) <hello@chatgptappsrank.com> "Your apps vs plugins explainer" -> sent 01a1d60c-f764-7cbb-be20-420c86e7e98b
2026-11-13 09:55 PT: backlink outreach to Big Hat Group Codex Weekly (bighatgroup.com) <info@bighatgroup.com> "Something for Codex Weekly maybe" -> sent 01a1d60c-f7d7-7252-b057-b1f8db9d2bb3
2026-11-16 08:15 PT: confirmed link swap with SkillMaxx <skillmaxx@gilventures.ai> "Re: SkillMaxx + PickAPlugin" (our link live on /alternatives; they add 'Related directories' on /how-we-test/) -> sent 01a1e524-7ec5-704f-a8a4-f7d157270d36
2026-11-16 10:24 PT: backlink outreach to Lockstep (getlockstep.dev) <naman@getlockstep.dev> "Your MCP servers for dev teams post" -> sent 01a1e59a-c359-754e-b22d-1b8801958817
2026-11-16 10:24 PT: backlink outreach to OpenApps (theopenapps.com) <hello@theopenapps.com> "Plugin Stack is listed on PickAPlugin" -> sent 01a1e59a-c3d3-7e34-bf05-8758d9edd2a4
2026-11-16 10:24 PT: backlink outreach to ClawCall (clawcall.dev) <support@clawcall.dev> "ClawCall on PickAPlugin?" -> sent 01a1e59a-e8a7-74b4-b132-864ba7c77943
2026-11-16 10:24 PT: backlink outreach to Best GitHub Repos (bestgithubrepositories.com) <partnership@bestgithubrepositories.com> "Your Claude Code plugins list" -> sent 01a1e59a-e91d-742a-b50b-8f71bcef6723
2026-11-16 10:24 PT: backlink outreach to MCP Hunter (mcp-hunter.com) <hello@mcp-hunter.com> "PickAPlugin + MCP Hunter" -> sent 01a1e59a-e9a4-72a5-91b9-b033d3fb577f
2026-11-16 10:24 PT: backlink outreach to Kipt (kipt.me) <hello@kipt.me> "Your Codex plugins guide" -> sent 01a1e59a-ea23-764a-8030-8f2a7b04f545
2026-11-16 10:24 PT: backlink outreach to Claude Marketplaces (claudemarketplaces.com) <hi@claudemarketplaces.com> "Link swap with a Codex-side directory?" -> sent 01a1e59a-ea9a-78dd-851a-52262dfb4c6a
2026-11-17 10:24 PT: backlink outreach to Corsair (corsair.dev) <dev@corsair.dev> "Your MCP context cost post" -> sent 01a1eac0-6682-7291-9cf9-4ed1d2488118
2026-11-17 10:24 PT: backlink outreach to MCPSkillHub (mcpskillhub.com) <admin@mcpskillhub.com> "Your MCP context tax report" -> sent 01a1eac0-66f0-7bc4-902a-963cbeea608b
2026-11-17 10:24 PT: backlink outreach to AI Toolbox (ai-toolbox.co) <team@ai-toolbox.co> "Your best ChatGPT plugins list" -> sent 01a1eac0-6760-7af6-a274-86e1f54a9fba
2026-11-17 10:24 PT: backlink outreach to Agent Ready (agentready.co) <hello@agentready.co> "Your ChatGPT plugins are back post" -> sent 01a1eac0-67d6-798c-98d9-11a9903dc9a5
2026-11-17 10:24 PT: backlink outreach to LaunchList (getlaunchlist.com) <contact@getlaunchlist.com> "One more for your MCP directories list" -> sent 01a1eac0-6845-7ca1-8d31-2b1c4e7287b3
2026-11-17 10:24 PT: backlink outreach to SkillsLLM (skillsllm.com) <hello@skillsllm.com> "Link swap with a Codex plugin directory?" -> sent 01a1eac0-68b6-79a0-b0ec-a85c40cad7dc
2026-11-17 10:24 PT: backlink outreach to Arantic Documentation (docs.arantic.com) <contact@arantic.com> "Your Codex plugins docs page" -> sent 01a1eac0-6929-7733-92ca-96c4f8f6ccb1
2026-11-17 10:24 PT: backlink outreach to Arvind Verma (techiarvind.com) <connect@techiarvind.com> "Your Claude Code and Codex plugins list" -> sent 01a1eac0-699b-74f4-9ef6-2154a9e40265
2026-11-17 10:24 PT: backlink outreach to Chen Media MCP Weekly (chen.media) <alex@chen.media> "MCP Weekly + PickAPlugin" -> sent 01a1eac0-69e2-7bd9-b29f-6264cee6a01a
2026-11-17 10:24 PT: backlink outreach to Implicator.ai (implicator.ai) <editor@implicator.ai> "Your coding-agent plugins piece" -> sent 01a1eac0-6a4d-7af8-830d-3a42ecbfc37f
2026-11-18 10:28 PT: backlink outreach to ChatCut (chatcut.io) <alima@chatcut.io> "Your Codex plugins for creators post" -> sent 01a1efeb-4723-71fb-8212-78b30fed234d
2026-11-18 10:28 PT: backlink outreach to LaunchDistro (launchdistro.com) <contact@launchdistro.com> "One more for your MCP registries page" -> sent 01a1efeb-47a6-7d47-8f7a-fa498e1afca7
2026-11-18 10:28 PT: backlink outreach to Another Directory (another.directory) <hello@another.directory> "Where to launch: plugin directories" -> sent 01a1efeb-4817-7341-accf-a7bf6aeddbbb
2026-11-18 10:28 PT: backlink outreach to OpusClip (opus.pro) <contact@opus.pro> "AI Producer on PickAPlugin?" -> sent 01a1efeb-486e-747e-a7b0-8ae3d1bc8756
2026-11-18 10:28 PT: backlink outreach to Satelo (satelo.io) <info@satelo.io> "Satelo MCP on PickAPlugin?" -> sent 01a1efeb-48e4-79a2-b983-a4c463a19621
2026-11-18 10:28 PT: backlink outreach to LogNorm (lognorm.com) <hello@lognorm.com> "Your MCP servers for SEO and marketing post" -> sent 01a1efeb-4958-73bb-86ea-0e2b2e541ba9
2026-11-18 10:28 PT: backlink outreach to Agent Skills (agentskills.codes) <agentskillscodes@gmail.com> "Link swap between skill and plugin directories?" -> sent 01a1efeb-49d2-7de7-8edf-f412072b040c
2026-11-18 10:28 PT: backlink outreach to Starpop (starpop.ai) <alex@starpop.ai> "Starpop MCP on PickAPlugin?" -> sent 01a1efeb-4a4e-7163-b3c7-b24759b03dd1
