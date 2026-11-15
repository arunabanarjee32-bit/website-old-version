# Developer handoff — VersionVault

**Updated:** 2026-11-15. This file is self-contained for developers and future Codex sessions; read README.md, AGENTS.md, SECURITY.md, ADR-001 and the master checklist as well.

## 1. Project purpose

Build an independent website-history system to save, preserve, compare and eventually replay permitted historical versions. Aim to compete on reliability, modern capture fidelity and user experience, not immediate global Wayback Machine scale. Archiving historical ChatGPT/Gemini/Claude UI **does not** preserve the retired proprietary AI backend or weights.

## 2. Current architecture

Local-only proof: Python FastAPI app (services/api/versionvault/app.py), embedded HTML UI, SQLite metadata/job status, SHA-256-addressed screenshots/HTML on disk, one background ThreadPoolExecutor worker and Playwright Chromium **offline HTML rendering**. No WARC/WACZ, Solr, Docker infrastructure or customer accounts in the MVP. Future target interfaces: ArchiveBox external capture adapter + SolrWayback distinct replay/index service, with Playwright/Warcio as supporting libs (ADR-001; subject to testing).

## 3. Features truly implemented

- POST /api/captures: only literal http://127.0.0.1:8766/ (and paths) permitted.
- GET /api/jobs/{id}: queued/running/ready/failed.
- GET /api/snapshots: dated snapshot history and metadata.
- GET /api/snapshots/{id}/screenshot: image/png.
- GET /api/snapshots/{id}/export: ZIP containing manifest, HTML, PNG and hashes.
- POST /api/import: bounded ZIP input, expected files, checksums and PNG magic check.
- GET /: UI with capture form, date filter, Left/Right screenshot comparison buttons, export and import.

**Limit:** HTML is fetched via Python only from the local fixture, then passed to offline Chromium. JS-heavy public sites, remote resources, historical WARC replay, computed visual diffs and arbitrary URLs are NOT supported.

## 4. Run locally

Prerequisites: Python 3.11+, installed Chromium at /usr/bin/chromium (or set VV_CHROMIUM), ability to install FastAPI/Uvicorn/Playwright/python-multipart.

From repo root in a virtualenv:
1. python -m venv .venv
2. . .venv/bin/activate
3. python -m pip install -e '.[test]'
4. Terminal A: python tests/fixture_site.py
5. Terminal B: uvicorn versionvault.app:app --app-dir services/api --host 127.0.0.1 --port 8765
6. Open http://127.0.0.1:8765/

**Never bind this demo to 0.0.0.0 or expose it to the public Internet.**

## 5. Run tests

From repository root: PYTHONPATH=services/api pytest -q. On 2026-11-15 local host: **12 passed in 1.87s**. Python 3.13.5 / FastAPI 0.128.2 / Chromium 144. GitHub-hosted CI not yet configured; this command may require the correct Chromium binary path on another machine.

## 6. Reproduce the demo

With both terminals running, enter the default fixture URL and click Save snapshot. Wait for ready, select two separate captures as Left and Right, download ZIP, import it. Import increases snapshot count; corrupt ZIP is rejected in integration tests. Direct Chromium navigation to 127.0.0.1 was blocked in the research environment; the offline rendering path is deliberate and is not a real-web crawl.

## 7. Known problems and caveats

- No production-grade network-level SSRF/egress isolation. Public capture is hard-disabled to one numeric loopback origin.
- For local root test only, Chromium may launch with --no-sandbox; production **must** use nonroot sandboxed worker and isolated network.
- No CSS/JS asset recording from live external sites; no WARC, WACZ, SolrWayback integration, live historical replay or true image diff.
- Job statuses survive in SQLite but pending jobs are not recovered after restart; retries unimplemented.
- Upload/archive bounds and hash verification need malicious ZIP fuzzing, validation/memory limit review and independent security testing.
- No authentication, per-user storage, permissions, encryption or deployment. Private archive publication unsafe.
- Browser UX has not passed a real UI E2E test, only API/fixture tests.
- No dependency lockfile, transitive SBOM, automated CI or standalone downloadable product installer.
- Earlier Chrome extension source ZIP from planning has **not been incorporated into GitHub**.
- Repository distribution license is undecided; contributor/commercial rights require maintainer action.

## 8. External dependencies and research systems

Current pip project depends on FastAPI, Uvicorn, Playwright, python-multipart; test extras pytest/httpx; SQLite from stdlib and system Chromium. Repository-study primary systems are **exactly ArchiveBox and SolrWayback**, both still evaluation targets. ArchiveBox MIT; SolrWayback Apache-2.0 on inspected source. See matrix for sources, versions and other licensing warnings.

## 9. Next task to implement

First establish reproducible pinned dependencies and GitHub CI for 12 fixture tests, with a controlled Chromium runner and no public web access. Then design an egress-isolated nonroot capture worker before enabling user-submitted real websites.

## 10. Architecture decisions and five next tasks

Read docs/adr/ADR-001-capture-architecture.md and docs/TOP_TWO_REPOSITORIES.md. Metadata/object hashes are canonical in VersionVault; external capture and replay engines must be replaceable. The five immediate tasks (in priority order):

1. **Dependency lock/SBOM and CI:** clean runner executes all 12 tests; publish test/lock evidence.
2. **Worker security architecture:** demonstrate no access to private IP/cloud metadata, no DNS rebinding, no unsafe replay origins.
3. **ArchiveBox adapter evaluation:** run pinned v0.9.77 only against owned fixture under egress isolation; record CLI/API artifacts.
4. **SolrWayback WARC interoperability:** index one lawful WARC via 5.5.0 bundle and replay in isolated origin; record CPU/RAM/disk.
5. **Browser E2E + job restart robustness:** click through capture/date/compare/export/import and verify retry/restart behavior.

Use docs/MASTER_IMPLEMENTATION_CHECKLIST.md for per-feature acceptance and evidence. Do not change 'planned' to 'done' without real tests.


## 11. Foundation PR handoff — 2026-11-15 (subsequent session)

**GitHub state:** `main` baseline `0513510d035db4dca865300e529ccd6375bf5665`. Branch `codex/versionvault-foundation`; [PR #1](https://github.com/arunabanarjee32-bit/website-old-version/pull/1), not merged. Test-evidenced source commit `bbd136235a50d9248d34a7e12f1f5397940f0d74`. Follow-up documentation commits add only descriptions (inspect current PR head before changing files). Do not force-push or merge without approval.

**Changed code/files:** `services/api/versionvault/app.py` (lifespan marks orphaned jobs failed on startup, bounded import read and PNG framing/CRC checks); `tests/test_reliability.py` (12 new cases); `tests/test_app.py` (capture poll deadline 60s); `.github/workflows/ci.yml` (Ubuntu 24.04, Python 3.13, Playwright-managed Chromium, pip check, compileall, selected Ruff, pytest, installed dependency list artifact); `constraints-ci.txt` (direct dependency versions). Existing fixture policy untouched.

**Reproduce:** from repository root with Python 3.13:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]' -c constraints-ci.txt
python -m playwright install chromium
# In CI, VV_CHROMIUM is set to Playwright's chromium.executable_path.
# Locally, use VV_CHROMIUM if /usr/bin/chromium is absent or mismatched.
python -m pip check
python -m compileall -q services tests
python -m pytest -q
```

**Evidence:** [GitHub Actions 43739119692](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43739119692) on `bbd1362`: **24 passed, 1 warning in 5.11s**; static checks pass. The one warning is from third-party Starlette/AnyIO deprecation. [Earlier run 43738724575](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43738724575) had 1 timeout waiting for a Snap Chromium capture; subsequent CI changed to library-managed browser and bounded wait. No local checkout/test was completed by this session because the execution container could not resolve github.com; do not treat this as local test evidence.

**Next smallest task:** establish **full transitive hash-locked dependency resolution + SBOM/license inventory**, using the now-green CI as a baseline; then SQLite migrations, fsync/fault-injection recovery and UI browser E2E. Keep the exact fixture origin and no live replay. Dependency constraints alone do not constitute a complete reproducible lock. New external service experiments need owner permission and separate isolation evidence.
