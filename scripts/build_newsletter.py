# Executed by build.py (shares its namespace: D, layout, e, nlform, ROOT). Builds /newsletter and /newsletter/<date>
# from data/newsletter/*.json (written by scripts/newsletter.py). Unsent drafts get a preview page marked noindex
# and are left out of the archive list and sitemap.
import importlib.util as _ilu, glob as _gn
_spec=_ilu.spec_from_file_location("pap_newsletter",os.path.join(ROOT,"scripts","newsletter.py")); _NL=_ilu.module_from_spec(_spec); _spec.loader.exec_module(_NL)
os.makedirs(D+"/newsletter",exist_ok=True)
_issues=[json.load(open(f)) for f in sorted(_gn.glob(os.path.join(ROOT,"data","newsletter","*.json")),reverse=True)]
for _I in _issues:
  _sent=_I.get("status")=="sent"
  _ban="" if _sent else '<p class=box style="border-color:var(--acc)"><b>Preview.</b> This issue hasn\'t been emailed yet. It may change before it goes out.</p>'
  _h=layout(f'{_I["subject"]} ({_NL.nice(_I["date"])}) — PickAPlugin weekly',f'''<div class=prose><span class=mono style="color:var(--acc)">PickAPlugin weekly · {e(_NL.nice(_I["date"]))}</span><h1>{e(_I["subject"])}</h1>{_ban}
{_NL.body_html(_I,web=True)}<p style="margin-top:26px"><a href="../newsletter.html">← All issues</a></p></div>''',1,f'New MCP servers and ChatGPT, Codex & Claude plugins added to PickAPlugin in the week ending {_NL.nice(_I["date"])}, plus the fastest-growing projects by GitHub stars.')
  if not _sent: _h=_h.replace("<meta charset=utf-8>",'<meta charset=utf-8><meta name=robots content="noindex">',1)
  open(f'{D}/newsletter/{_I["date"]}.html',"w").write(_h)
_list="".join(f'<li><span class=mono>{e(_NL.nice(I["date"]))}</span> <a href="newsletter/{I["date"]}.html">{e(I["subject"])}</a></li>' for I in _issues if I.get("status")=="sent")
open(D+"/newsletter.html","w").write(layout("Newsletter: new MCP servers & plugins, once a week — PickAPlugin",f'''<div class=prose><span class=mono style="color:var(--acc)">Free · weekly</span><h1>New MCP servers &amp; plugins, once a week</h1>
<p style="font-size:19px">One short email: the MCP servers and ChatGPT, Codex &amp; Claude plugins that joined the catalog that week, and the projects gaining GitHub stars fastest. It's built from our catalog data, not press releases. Any paid slot is labelled <b>Sponsored</b>.</p>
<p>You'll get a confirmation email first, and every issue has a one-click unsubscribe link.</p></div>{nlform("newsletter-page","Subscribe")}
<div class=prose><h3>Past issues</h3>{f'<ul class=log>{_list}</ul>' if _list else '<p>The first issue hasn\'t gone out yet. Subscribe above to get it.</p>'}</div>''',0,"A free weekly email of new MCP servers and ChatGPT, Codex & Claude plugins, plus the fastest-growing projects by GitHub stars."))
print("newsletter:",len(_issues),"issue pages,",sum(1 for I in _issues if I.get("status")=="sent"),"sent")
