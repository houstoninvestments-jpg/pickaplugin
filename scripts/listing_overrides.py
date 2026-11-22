"""Hand-maintained listing fields: about text, install, homepage, docs, improved descriptions.

Applied at the end of refresh.py (after a source crawl) and when build.py loads
plugins.json, so the daily 7 AM refresh cannot wipe editor improvements. Same
idea as the StalkChain category pin and multi-line install preservation.

Source of truth: data/listing_overrides.json (keyed by slug). Do not invent
features or stats; every override should come from the project's README or homepage.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "data", "listing_overrides.json")
# Copy fields only. link_missing is owned by refresh.py's GitHub check so a
# repo that comes back isn't stuck as dead because of a stale override.
COPY_FIELDS = ("about", "description", "install", "homepage", "docs")

def load():
    if not os.path.exists(PATH):
        return {}
    return json.load(open(PATH))

def apply_map(out, overrides=None):
    """out: slug -> plugin dict (refresh.py). Overrides win over crawled values."""
    ovr = load() if overrides is None else overrides
    n = 0
    for slug, fields in ovr.items():
        p = out.get(slug)
        if not p:
            continue
        for k in COPY_FIELDS:
            if fields.get(k):
                p[k] = fields[k]
                n += 1
    return n

def apply_list(plugins, overrides=None):
    """plugins: list of dicts (build.py). Returns the same list."""
    ovr = load() if overrides is None else overrides
    by = {p["slug"]: p for p in plugins}
    apply_map(by, ovr)
    return plugins
