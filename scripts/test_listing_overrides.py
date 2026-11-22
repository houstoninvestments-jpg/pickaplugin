#!/usr/bin/env python3
"""Guards the StalkChain-style preservation of hand-maintained listing fields."""
import json, os, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import listing_overrides as lo

assert os.path.exists(lo.PATH), "data/listing_overrides.json missing"
ovr = lo.load()
assert len(ovr) >= 50, len(ovr)
# Every about/description/install should be non-empty text; no invented-looking keys
for slug, fields in ovr.items():
    assert isinstance(slug, str) and slug
    for k in lo.COPY_FIELDS:
        if k in fields:
            assert isinstance(fields[k], str) and fields[k].strip(), (slug, k)
    # Don't let a stale override pin link_missing (refresh owns that)
    assert "link_missing" not in lo.COPY_FIELDS

# apply_map overwrites a crawled one-liner with the override
sample = next(s for s, f in ovr.items() if f.get("about") or f.get("description"))
fields = ovr[sample]
out = {sample: {"slug": sample, "name": "X", "description": "short crawled line", "source": "awesome-codex-plugins"}}
lo.apply_map(out, ovr)
if fields.get("description"):
    assert out[sample]["description"] == fields["description"]
if fields.get("about"):
    assert out[sample]["about"] == fields["about"]

# plugins.json should already have those fields merged (build also re-applies)
plugins = {p["slug"]: p for p in json.load(open(os.path.join(ROOT, "data", "plugins.json")))}
for slug, fields in ovr.items():
    assert slug in plugins, slug
    for k in lo.COPY_FIELDS:
        if fields.get(k):
            assert plugins[slug].get(k) == fields[k], (slug, k)

print("ok: listing overrides", len(ovr), "fields preserved")
