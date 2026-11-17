"""Global 7-day cooldown for outbound PickAPlugin marketing email.

Before sending a sales pitch, badge email, or backlink outreach, call
recent_send(email) (or skip_message(email)). If it returns a log entry /
reason string, skip that recipient.

A recipient is on cooldown if launch/resend-send-log.json has any successful
PickAPlugin email to that address in the last COOLDOWN_DAYS days.

Replies to people who wrote us are exempt: pass reply=True, or simply do not
call these helpers (see send_submission_replies_*.py).
"""
import datetime, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(ROOT, "launch", "resend-send-log.json")
COOLDOWN_DAYS = 7

def _addr(entry):
    return (entry.get("to") or entry.get("email") or "").strip().lower()

def _when(entry):
    raw = str(entry.get("time") or entry.get("date") or entry.get("at") or "").strip()
    if not raw:
        return None
    for cand in (raw[:19].replace("Z", ""), raw[:10]):
        try:
            return datetime.datetime.fromisoformat(cand)
        except ValueError:
            pass
    return None

def recent_send(email, days=COOLDOWN_DAYS, log=None, reply=False):
    """Return the most recent successful log entry for email within `days`, or None.

    reply=True (responses to inbound mail) is always exempt and returns None.
    Failed/error sends do not start a cooldown, so a retry is allowed.
    """
    if reply or not email:
        return None
    want = email.strip().lower()
    if log is None:
        if not os.path.exists(LOG):
            return None
        log = json.load(open(LOG))
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
    best = None
    best_t = None
    for e in log:
        if _addr(e) != want:
            continue
        if str(e.get("status") or "").lower() in ("error", "failed"):
            continue
        t = _when(e)
        if t is None or t < cutoff:
            continue
        if best_t is None or t > best_t:
            best, best_t = e, t
    return best

def skip_message(email, days=COOLDOWN_DAYS, log=None, reply=False):
    e = recent_send(email, days=days, log=log, reply=reply)
    if not e:
        return None
    when = e.get("time") or e.get("date") or e.get("at")
    kind = e.get("type") or e.get("key") or "email"
    return f"SKIP cooldown ({days}d) {email} last={when} ({kind})"
