# Executed by build.py after the main pages exist. Adds the "Launch package" offer to /advertise and /featured
# and swaps the old "no traffic numbers" line for the real, caveated ones in data/launch_package.json.
# Keeps every existing featured/founding link as is.
import json as _lj
_LP=_lj.load(open(os.path.join(ROOT,"data","launch_package.json")))
if _LP.get("enabled"):
  _T=_LP["traffic"]
  _traffic=(f'Honest numbers: Cloudflare counted {_T["cf_uniques_week"]} unique visitors for {_T["cf_week"]} (that count includes some bots), '
            f'and Google search sent {_T["gsc_clicks_28d"]} clicks from {_T["gsc_impressions_28d"]} impressions in the 28 days to {_T["gsc_export"]}. Small, but growing week over week.')
  _price=_LP.get("price_note") or "$79 one-time (intro price)"
  _link=_LP.get("stripe_payment_link") or ""
  if _link:
    _cta=(f'<p><a class=btn href="{_link}">Book a launch day — {_price}</a> '
          f'<span class=mono style="color:var(--mute);font-size:12px">· we\'ll email within 1 business day to schedule</span></p>')
  else:
    _subj="Launch%20package%20for%20my%20plugin"
    _bodyq="Plugin%20link%3A%20%0ALaunch%20date%20I%27d%20like%3A%20%0AOne%20line%20on%20what%20it%20does%3A%20"
    _cta=(f'<p><a class=btn href="mailto:{EMAIL}?subject={_subj}&body={_bodyq}">Email us to book a launch day</a> '
          f'<span class=mono style="color:var(--mute);font-size:12px">· we\'ll reply with the price and open dates</span></p>')
  def _launch_box(r):
    return f'''<div class=box id=launch style="margin:22px 0"><span class="mono" style="color:var(--acc)">New · Launch package</span>
<h3 style="margin-top:6px">Launching a plugin or MCP server? We'll give it a proper launch day.</h3>
<ul class=where>
<li><b>Launch-day homepage spotlight:</b> your plugin in a labelled “Launching today” spot at the top of the homepage for 24 hours.</li>
<li><b>Newsletter mention:</b> a short write-up in our next newsletter roundup. The list is new and small, so think of this as a bonus, not the main event.</li>
<li><b>Cross-posts:</b> a launch post on our Bluesky, dev.to and Hashnode accounts, linking to your repo and your listing.</li>
<li><b>Badge:</b> a “Launched on PickAPlugin” README badge that links to your listing.</li>
<li>Your listing gets checked and tidied (description, category, install command) before the day.</li></ul>
<p>{_traffic} We won't promise installs. What you get is a clearly labelled launch on a site built for people choosing plugins, plus posts that keep linking to you after the day ends.</p>
<p>We run {_LP.get("slots_per_week",2)} launches a week at most, so each one gets the spotlight to itself. Every launch is labelled as paid, and it never changes editor's picks or the catalog order.</p>
{_cta}
<p style="font-size:14px;color:var(--mute)">Just want the ongoing spot? The <a href="{r}featured.html">featured founding offer</a> ($29/mo for life, first week free) is still open and works well alongside a launch.</p></div>'''
  for _pg,_r,_anchor in (("advertise.html","","<div class=ladder>"),("featured.html","",'<h3>Where you appear</h3>')):
    _f=os.path.join(D,_pg)
    if not os.path.exists(_f): continue
    _h=open(_f).read()
    if 'id=launch' in _h: continue
    if _anchor in _h: _h=_h.replace(_anchor,_launch_box(_r)+_anchor,1)
    _h=_h.replace("We don't publish traffic numbers yet and won't invent any. You're buying a clearly labelled spot, not a guaranteed number of installs.",
                  _traffic+" We'll never invent numbers. You're buying a clearly labelled spot, not a guaranteed number of installs.")
    _h=_h.replace("<a href=\"advertise.html\">advertise</a> page.)</p>","<a href=\"advertise.html\">advertise</a> page. Launching something new? See the <a href=\"#launch\">launch package</a>.)</p>",1)
    open(_f,"w").write(_h)
  print("launch package: on /advertise and /featured")
