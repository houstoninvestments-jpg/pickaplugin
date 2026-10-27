# Black Friday page — pickaplugin.com/black-friday

Live since Oct 27, 2026. Data lives in `data/black_friday.json`; page built by `scripts/build_blackfriday.py`.

## Refresh schedule
Weekly until Dec 2 (Cyber Monday is Nov 30): Nov 3, Nov 10, Nov 17, Nov 24, then daily Nov 25–Dec 2.
Each refresh:
1. Check each "watch" tool's own pricing/blog page and any deals emailed to hello@pickaplugin.com.
2. Only add a deal you saw on the vendor's own page. Add `{"name","what","offer","ends","url","checked"}` to `deals`; bump `checked`.
3. Remove expired deals. After Dec 2, take the deals down and leave a "back next year" note.
4. Build, deploy, `python3 scripts/indexnow.py`.

Status Oct 27: 0 verified 2026 deals. (Codeanywhere's /blackfriday page is an old 2024 offer, so it's not listed.)

## X drafts
1. black friday is a month out and people are already asking which AI coding tools go on sale. honest answer right now: none have announced anything yet. we're keeping a list that only adds real deals, with a link and the date we checked. pickaplugin.com/black-friday

2. if you make a Codex/ChatGPT plugin or an MCP tool and you're running a black friday deal, send it over. free to list, we just check it's real first. no countdown timers, no fake "70% off" stuff. pickaplugin.com/black-friday
