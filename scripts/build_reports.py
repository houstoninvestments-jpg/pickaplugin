# Executed by build.py before build_compare/build_seo. Renders every data/reports/<yyyy-mm>.json (made by
# scripts/make_report.py) to /reports/<yyyy-mm> plus standalone SVG charts and a CSV, and /reports (index).
import json as _rj2, glob as _rg2, csv as _rc2, io as _rio2, calendar as _cal
_RS=sorted(_rg2.glob(os.path.join(ROOT,"data","reports","*.json")))
os.makedirs(D+"/reports",exist_ok=True)
def _svgbars(title,items,total=None,note="",w=680):
  items=[(str(k),v) for k,v in items]; mx=max([v for _,v in items] or [1]) or 1; h=34*len(items)+70; y=50; out=[]
  for lab,v in items:
    bw=round(330*v/mx); pct=f" · {100*v/total:.0f}%" if total else ""
    out.append(f'<text x="0" y="{y+16}" font-family="Martian Mono,ui-monospace,monospace" font-size="12" fill="#14171f">{e(lab[:30])}</text><rect x="230" y="{y}" width="{max(bw,2)}" height="22" fill="#1f3a8a" opacity=".85"/><text x="{238+bw}" y="{y+16}" font-family="Martian Mono,ui-monospace,monospace" font-size="12" fill="#1f3a8a">{v:,}{pct}</text>'); y+=34
  return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{e(title)}"><rect width="{w}" height="{h}" fill="#fbf8f0"/>'
    f'<text x="0" y="24" font-family="Newsreader,Georgia,serif" font-size="20" font-weight="700" fill="#14171f">{e(title)}</text><line x1="230" y1="40" x2="230" y2="{h-22}" stroke="#14171f"/>{"".join(out)}'
    f'<text x="0" y="{h-6}" font-family="Martian Mono,ui-monospace,monospace" font-size="11" fill="#6b6658">{e(note)}</text></svg>')
_rep_index=[]
for _rf in _RS:
  R=_rj2.load(open(_rf)); M=R["month"]; _y,_m=map(int,M.split("-")); MN=f"{_cal.month_name[_m]} {_y}"
  _dir=f"{D}/reports/{M}"; os.makedirs(_dir,exist_ok=True)
  _URL=f"{SITE_URL}/reports/{M}"; _src=f"PickAPlugin, State of MCP & Codex Plugins, {MN} (data through {R['as_of']})"
  _thru="" if R["complete"] else f" (month to date, through {R['as_of']})"
  charts={
   "new-by-category":_svgbars(f"New plugins by category, {MN}{' to date' if not R['complete'] else ''}",R["new_by_category"],R["new_count"],f"n = {R['new_count']} new listings · {_src} · CC BY 4.0"),
   "new-by-packaging":_svgbars(f"How new plugins install, {MN}",R["new_by_packaging"],R["new_count"],f"n = {R['new_count']} · from each README's install command · PickAPlugin · CC BY 4.0"),
   "fastest-growing":_svgbars(f"Most GitHub stars gained, {MN}",[(g["name"],g["gain"]) for g in R["fastest_abs"]],None,f"stars gained since {R['baseline_date']} · {R['stars_tracked']} repos tracked · PickAPlugin · CC BY 4.0"),
   "catalog-by-category":_svgbars(f"Whole catalog by category, {R['as_of']}",R["catalog_by_category"],R["catalog_now"],f"n = {R['catalog_now']} listings · PickAPlugin · CC BY 4.0"),
  }
  for k,v in charts.items(): open(f"{_dir}/{k}.svg","w").write(v)
  def _fig(k,cap): return f'<figure style="margin:24px 0;border-top:3px double var(--ink);padding-top:10px">{charts[k]}<figcaption class=mono style="font-size:12px;color:var(--mute)">{cap} · <a href="{M}/{k}.svg">SVG</a></figcaption></figure>'
  _rows=[("metric","value","notes")]
  for k in ("catalog_start","catalog_now","new_count","new_median_stars","pushed_7d","pushed_30d","live_with_push_data","archived","stars_tracked","stars_total_start","stars_total_now","gained_any","lost_any"): _rows.append((k,R[k],""))
  for grp in ("new_by_category","new_by_packaging","new_by_license","new_by_language","catalog_by_category","license_share_catalog"):
    for k,v in R[grp]: _rows.append((grp+":"+k,v,""))
  for g in R["fastest_abs"]: _rows.append(("stars_gained:"+g["slug"],g["gain"],f'{g["from"]}->{g["to"]}'))
  for g in R["fastest_pct"]: _rows.append(("stars_pct:"+g["slug"],g["pct"],f'{g["from"]}->{g["to"]}'))
  _b=_rio2.StringIO(); _rc2.writer(_b).writerows(_rows)
  open(f"{_dir}/data.csv","w").write(f"# {_src}. {_URL}. License: CC BY 4.0, credit PickAPlugin with a link.\n"+_b.getvalue())
  _pct=lambda a,b:f"{100*a/max(1,b):.0f}%"
  _gt=R["stars_total_now"]-R["stars_total_start"]
  top_new=R["notable_new"][:8]; fa=R["fastest_abs"]; fp=R["fastest_pct"]
  _cite=f'{_src}. {_URL}'
  _embed=f'<a href="{_URL}"><img src="{_URL}/new-by-category.svg" alt="New MCP and Codex plugins by category, {MN} (PickAPlugin)" width="680"></a>'
  _tbl=lambda xs,cols:'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;border-top:3px solid var(--ink)"><tr>'+"".join(f'<th class=mono style="text-align:left;padding:8px;border-bottom:1px solid var(--rule)">{c}</th>' for c in cols)+'</tr>'+"".join('<tr>'+"".join(f'<td style="padding:8px;border-bottom:1px solid var(--rule);vertical-align:top">{c}</td>' for c in r)+'</tr>' for r in xs)+'</table></div>'
  body=f'''<div class=prose style="max-width:900px"><span class=mono style="color:var(--acc)">Report · {MN}{_thru} · CC BY 4.0</span>
<h1>State of MCP &amp; Codex Plugins: {MN}</h1>
<p style="font-size:19px">Every month we count what changed in the PickAPlugin catalog of open-source Codex plugins, Claude Code plugins and MCP servers. All numbers below come from our own catalog and public GitHub data. Nothing is surveyed or estimated.</p>
<div style="border:1px solid var(--ink);background:#fffdf8;padding:14px 18px;margin:18px 0"><b>The numbers</b><ul class=where>
<li><b>{R["new_count"]}</b> new plugins joined the catalog in {MN}{_thru}, taking it from {R["catalog_start"]} to <b>{R["catalog_now"]}</b> listings.</li>
<li>The busiest category for new plugins was <b>{e(R["new_by_category"][0][0])}</b> ({R["new_by_category"][0][1]} new, {_pct(R["new_by_category"][0][1],R["new_count"])}), then {e(R["new_by_category"][1][0])} ({R["new_by_category"][1][1]}).</li>
<li>The {R["stars_tracked"]} repos we tracked since {R["baseline_date"]} gained <b>{_gt:,} GitHub stars</b> combined ({R["stars_total_start"]:,} → {R["stars_total_now"]:,}). {R["gained_any"]} of them gained at least one.</li>
<li>Most stars gained: <b>{e(fa[0]["name"])}</b> (+{fa[0]["gain"]:,}). Fastest growth among repos that started with 25+ stars: <b>{e(fp[0]["name"])}</b> ({fp[0]["from"]:,} → {fp[0]["to"]:,}, +{fp[0]["pct"]:.0f}%).</li>
<li>New plugins start small: the median new listing had <b>{R["new_median_stars"]} stars</b>. {dict(R["new_by_packaging"]).get("No install command in README",0)} of {R["new_count"]} ({_pct(dict(R["new_by_packaging"]).get("No install command in README",0),R["new_count"])}) had no copyable install command in their README.</li>
<li>The ecosystem is busy: {R["pushed_7d"]} of {R["live_with_push_data"]} non-archived repos ({_pct(R["pushed_7d"],R["live_with_push_data"])}) got a push in the 7 days to {R["as_of"]}, and {_pct(R["pushed_30d"],R["live_with_push_data"])} in the last 30.</li></ul></div>
<h2>New plugins by category</h2>{_fig("new-by-category","Share of this month's new listings")}
<h2>Notable launches</h2><p>The most-starred plugins that joined the catalog this month.</p>
{_tbl([(f'<a href="../p/{x["slug"]}.html"><b>{e(x["name"])}</b></a><br><span style="font-size:14px">{e(x["description"][:160])}</span>',e(x["category"]),f'{x["stars"]:,}' if x["stars"] is not None else "n/a",e(x["license"] or "none"),x["first_seen"]) for x in top_new],["Plugin","Category","Stars","License","Added"])}
<h2>Fastest-growing by GitHub stars</h2>{_fig("fastest-growing","Absolute stars gained this month")}
<h3>Biggest percentage jumps (repos that started with 25+ stars)</h3>
{_tbl([(f'<a href="../p/{g["slug"]}.html">{e(g["name"])}</a>',e(g["category"]),f'{g["from"]:,} → {g["to"]:,}',f'+{g["pct"]:.0f}%') for g in fp[:8]],["Plugin","Category","Stars","Change"])}
<h2>How new plugins install</h2><p>Read from the install command in each README. A plugin with no copyable command takes more work to try.</p>{_fig("new-by-packaging","Install method of new listings")}
<h2>Licenses on new plugins</h2><p>{", ".join(f"{e(k)}: {v}" for k,v in R["new_by_license"])}. Across the whole catalog: {", ".join(f"{e(k)} {v}" for k,v in R["license_share_catalog"])}.</p>
<h2>The whole catalog</h2>{_fig("catalog-by-category","All listings by category")}
<h2>Use these numbers</h2><p>Everything here is CC BY 4.0. Quote it, chart it, put it in a newsletter. Just credit PickAPlugin with a link.</p>
<p class=mono>Cite</p><pre class=code>{e(_cite)}</pre>
<p class=mono>Embed the chart</p><pre class=code>{e(_embed)}</pre>
<p>Raw numbers: <a href="{M}/data.csv">data.csv</a> · charts: {" · ".join(f'<a href="{M}/{k}.svg">{k}.svg</a>' for k in charts)}</p>
<h2>Methodology</h2><ul class=where>
<li><b>Catalog:</b> PickAPlugin collects open-source Codex plugins, Claude Code plugins, skills packs and MCP servers daily from public lists (like awesome-codex-plugins) and maker submissions. It isn't every plugin in existence, just the ones we've found and listed.</li>
<li><b>"New"</b> means the listing's first-seen date in our catalog falls in {MN}. That's when we found it, not necessarily when the repo was created. The catalog count on {R["baseline_date"]} ({R["catalog_start"]}) comes from our git history; 9 hand-added listings dated Oct 29 joined after that snapshot, which is why start + new doesn't add up exactly to {R["catalog_now"]}.</li>
<li><b>Stars</b> come from the GitHub API at each daily refresh. Growth compares the catalog committed on {R["baseline_date"]} (commit {R["baseline_commit"]}) with the latest refresh on {R["as_of"]}, for the {R["stars_tracked"]} repos that have a star count in both. Stars measure attention, not quality.</li>
<li><b>Activity</b> uses each repo's last push date, for listings that aren't archived and have GitHub data.</li>
<li><b>Install method</b> is read from the first install command in the README (mcp add, /plugin, codex plugin, npx skills add).</li>
<li>Regenerated by script (<code>scripts/make_report.py</code>) from the catalog. {"This is a month-to-date edition; the final numbers land at the start of next month." if not R["complete"] else "This is the final edition for the month."}</li></ul>
<p>Browse the data behind it: <a href="../compare.html">comparisons and alternatives</a> · <a href="../research/state-of-codex-plugins-2026.html">State of Codex Plugins 2026 (deep dive)</a> · <a href="../index.html">the full catalog</a></p>
<p style="color:var(--mute);font-size:14px">Corrections: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div>'''
  open(f"{D}/reports/{M}.html","w").write(layout(f"State of MCP & Codex Plugins, {MN}: {R['new_count']} new plugins, {_gt:,} stars gained — PickAPlugin",body,1,
    f"{MN} report: {R['new_count']} new Codex/Claude Code plugins and MCP servers, by category; fastest-growing repos by GitHub stars; install and license data. CC BY 4.0."))
  _rep_index.append((M,MN,R))
if _rep_index:
  open(D+"/reports.html","w").write(layout("State of MCP & Codex Plugins: monthly reports — PickAPlugin",'<div class=prose><span class=mono style="color:var(--acc)">Monthly · CC BY 4.0</span><h1>State of MCP &amp; Codex Plugins</h1><p style="font-size:19px">A monthly count of new plugins, fastest-growing repos and how the ecosystem is shifting, built from the PickAPlugin catalog.</p><ul class=where>'+"".join(f'<li><a href="reports/{M}.html"><b>{MN}</b></a>: {R["new_count"]} new plugins, catalog at {R["catalog_now"]}{"" if R["complete"] else " (month to date)"}</li>' for M,MN,R in reversed(_rep_index))+'</ul></div>',0,"Monthly reports on the Codex plugin and MCP server ecosystem: new plugins, categories, fastest-growing repos. Free to cite."))
print("reports:",len(_rep_index))
