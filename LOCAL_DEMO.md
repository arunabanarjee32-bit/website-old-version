# VersionVault local MVP quickstart (restricted fixture only)

This is a **development prototype**, NOT a secure general-public URL archiver. The only capture target is the literal origin `http://127.0.0.1:8766/` (including its paths). No web URL capture beyond that origin can run.

Prerequisites: Python 3.11+, Chromium at `/usr/bin/chromium` (or `VV_CHROMIUM`), Python virtualenv.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
# terminal 1: controlled fixture
python tests/fixture_site.py
# terminal 2: app (localhost-only, NEVER bind 0.0.0.0)
uvicorn versionvault.app:app --app-dir services/api --host 127.0.0.1 --port 8765
# terminal 3: tests
pytest -q
```

Visit http://127.0.0.1:8765/ then capture the default fixture URL. The page lists captures by time, filters by date, compares two images, downloads a verified ZIP, and imports it. The imported HTML is stored only, never executed in the VersionVault origin.

Dependencies are bounded with major-version ranges; a production lockfile and SBOM remain TODO. Capture isolation is not production-grade: a restrictive route policy + numeric localhost target does **not** replace OS/container egress filtering and non-root Chromium sandboxing. The app must not be deployed to a publicly reachable address. ArchiveBox and SolrWayback integration are research targets, **not implemented** in this MVP. Source is original and external packages remain third-party dependencies.