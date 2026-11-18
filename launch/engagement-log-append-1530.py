#!/usr/bin/env python3
"""Append confirmed 2026-11-05 15:30 engagement posts to engagement-log.json.
Pass a JSON file of results: [{thread_url, author, type, reply_text, reply_url?, ok}]
"""
import json, sys
from pathlib import Path
LOG = Path("/workspace/pickaplugin/launch/engagement-log.json")
results = json.loads(Path(sys.argv[1]).read_text())
data = json.loads(LOG.read_text())
added = 0
existing = {(e.get("thread_url"), e.get("type","reply"), e.get("date")) for e in data["replies"]}
for r in results:
    if not r.get("ok"):
        continue
    entry = {
        "date": "2026-11-05",
        "run": "15:30",
        "type": r.get("type","reply"),
        "thread_url": r["thread_url"],
        "author": r["author"],
        "reply_text": r["reply_text"],
    }
    if r.get("reply_url"):
        entry["reply_url"] = r["reply_url"]
    key = (entry["thread_url"], entry["type"], entry["date"])
    if key in existing:
        print("skip duplicate", key)
        continue
    data["replies"].append(entry)
    existing.add(key)
    added += 1
LOG.write_text(json.dumps(data, indent=2) + "\n")
print("added", added, "total", len(data["replies"]))
