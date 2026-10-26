# PickAPlugin
Static ChatGPT/Codex plugin directory (no dependencies, Python 3 only).
- Refresh data: `python3 scripts/refresh.py` (also runs daily via .github/workflows/refresh.yml)
- Build: `python3 scripts/build.py` -> dist/
- Cloudflare Pages: build command `python3 scripts/refresh.py && python3 scripts/build.py`, output dir `dist`
- Stripe: paste Payment Links into STRIPE in scripts/build.py (currently TODO, payments not live)
- Feature a plugin: set "featured": true on its entry in data/plugins.json (preserved across refreshes)
