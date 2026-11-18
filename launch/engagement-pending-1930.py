
import json
from datetime import datetime
from zoneinfo import ZoneInfo
path = "/workspace/pickaplugin/launch/engagement-log.json"
with open(path) as f:
    data = json.load(f)
# RESULTS_PLACEHOLDER will be replaced
results = RESULTS
now = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%dT%H:%M:%S%z")
# fix tz format
now = datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="seconds")
for r in results:
    entry = {
        "date": "2026-11-04",
        "run": "19:30",
        "thread_url": r["thread_url"],
        "author": r["author"],
        "reply_text": r["reply_text"],
        "reply_url": r.get("reply_url"),
        "status": r.get("status", "posted"),
        "posted_at": r.get("posted_at", now),
        "mentions_site": r.get("mentions_site", False),
        "priority_thread": r.get("priority_thread", False),
    }
    if r.get("kind") == "quote_tweet":
        entry["type"] = "quote_tweet"
    data["replies"].append(entry)
with open(path, "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")
print("logged", len(results))
