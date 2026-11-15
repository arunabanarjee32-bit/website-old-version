# Repository audit — actual tree and verified status (2026-11-15)

## Evidence and chronology

**Before implementation:** GitHub main @ eceed3ba2da9572d19f750178ffad71c9ecc8b85 contained 20 text/Markdown documentation files, one main branch, 3 commits, zero open PRs, no application code, migrations, tests, CI, backend or deployable release. All 20 documents from the research instruction were read. Original project ideas were and remain ambitious, but not implemented by their documentation alone.

**After this engineering session:** Python FastAPI local demo, SQLite tables, tests, controlled HTTP fixture and pyproject are committed. GitHub app file SHA 75ad01d7666fbf6935df6d0d70f4370fb2dfca86 and tests SHA 2c7037eaadaac6752544a8224a6b48f9180ed96c were compared to hashes of exact locally tested files. **12 local tests passed** on 2026-11-15, with Python 3.13.5 / FastAPI 0.128.2 / /usr/bin/chromium 144. This is a local development run, NOT GitHub CI or a real-world capture benchmark.

Status vocabulary: Implemented and verified (in explicitly limited test), Implemented but unverified, Partially implemented, Planned only, Blocked.

| Component | Responsibility | Actual files | Status | Reusable implementation | Missing | Priority | Dependencies | Next action |
|---|---|---|---|---|---|---|---|---|
| Scope/governance | Project purpose and requirements | README.md, docs/*, AGENTS.md | Implemented and verified (documentation exists) | Contributor and roadmap docs | Licensing/trademark owner decision | P0 | Maintainer | decide license and inbound terms |
| URL admission | prevent unsafe fetch requests | services/api/versionvault/app.py | Implemented and verified for exact 127.0.0.1 fixture only | is_permitted_url | real public URLs, DNS/redirect policy, network egress | P0 | Isolated worker | security architecture review |
| Capture | local fixture screenshot/HTML | services/api/versionvault/app.py | Implemented and verified for simple HTML fixture | Playwright offline renderer | network resources, SPAs, WARC, safe public fetch | P0 | Chromium | adapter benchmark |
| Jobs | queued/running/ready/failed | app.py | Partially implemented | SQLite and single executor | retries/cancellation/restart recovery | P0 | database | restart-safe job mechanism |
| Object storage | hash and retain files | app.py | Implemented and verified locally | SHA256 storage | quotas, encrypted backups, cross-user control | P0 | filesystem | storage contract and import hardening |
| Snapshot metadata | site/date/title history | app.py | Implemented and verified locally | SQLite snapshot rows | migration, users, full text indexes | P0 | SQLite | migrations and schema constraints |
| Frontend | capture/history/date filter/compare/import | app.py embedded INDEX | Implemented but unverified in browser interaction | HTML/JS UI | UI e2e tests, accessibility, responsive QA | P1 | API | browser acceptance test |
| Backup | ZIP export/import + integrity | app.py | Implemented and verified locally | ZIP manifest, hashes | fuzzing, WARC/WACZ interchange | P0 | zipfile | negative archive fixtures |
| WARC/WACZ | standardized resource archive | docs/ARCHITECTURE.md | Planned only | none | format recording/validation | P1 | Warcio/ArchiveBox research | test WARC pipeline |
| Replay/search | historical playback | docs/adr/ADR-001-capture-architecture.md | Planned only | none | SolrWayback indexer, origin sandbox | P1 | WARC/Solr | interop proof |
| Comparison algorithm | text/pixel diffs | app.py shows two images | Partially implemented | side-by-side view | actual computed diff | P2 | two snapshots | golden image/text fixture |
| Monitoring | schedules and alerts | docs/ROADMAP.md | Planned only | none | scheduler/alerts | P2 | safe capture | defer until capture secure |
| Browser extension | permissioned user-side capture | docs/LEGACY_PROTOTYPE_README.md | Blocked (source not in GitHub) | historical README only | source import/audit | P2 | browser API | audit earlier prototype |
| AI preservation | model history and user imports | docs/AI_PRESERVATION.md | Planned only | design only | importer, privacy and catalog | P2 | secure user storage | fake data import design |
| Auth and tenancy | private user accounts | docs/SECURITY_PRIVACY.md | Blocked for public hosting | none | OIDC, RBAC, tenant tests | P0 launch gate | secure identity | keep app localhost |
| CI/deployment | reproducible builds | pyproject.toml, LOCAL_DEMO.md | Partially implemented | local instructions | lockfile, GitHub CI, Docker, monitoring | P0 | pinned browser/tools | CI |
| Public crawler | permissioned real-web capture | none | Blocked | none | SSRF egress isolation, abuse/copyright controls | P0 launch gate | operations | do NOT expose current demo |

## Source inspection versus desired architecture

- The original specification suggested a Next.js UI, FastAPI backend, worker, WARC/WACZ, PostgreSQL and optional Solr. Actual MVP uses one FastAPI process and embedded HTML, SQLite and local disk: this is an intentional lean implementation, **not a finalized production architecture**.
- GitHub documents originally stated no application existed. The appended README/CURRENT_STATUS updates now supersede that historical claim.
- Old local extension is not merged or security-audited; its README being committed does not make it a working in-repo extension.
- ArchiveBox and SolrWayback have been chosen for research but **neither is linked to the running demo**. The primary systems and supporting libraries are distinct.
- The repository has no root LICENSE; publicly viewable code is not automatically openly licensed for reuse.

## Verified tests and explicit limitations

Run: PYTHONPATH=services/api pytest -q. Local output was **12 passed in 1.87s**. A real Chromium direct navigation request to local fixture failed with ERR_BLOCKED_BY_ADMINISTRATOR in this environment. The working demo uses Python fetching an **exact, numeric, loopback-origin** 200 HTML fixture with redirects denied, then offline browser set_content screenshot. Browser network routing remains blocked. This proves only a tightly scoped local workflow, **not a safe general URL-capture service**. The UI's Left/Right DOM buttons were not tested in real browser interaction; the API returned images successfully.

No upstream comparative benchmarks, cloud runtime, production dependency audit or comprehensive security penetration tests have been performed.

See [developer handoff](DEVELOPER_HANDOFF.md), [feature checklist](MASTER_IMPLEMENTATION_CHECKLIST.md), [upstream research](REPOSITORY_RESEARCH_MATRIX.md) and [architecture decision](adr/ADR-001-capture-architecture.md).


## Foundation PR audit delta (2026-11-15; not yet merged)

Baseline main commit: `0513510d035db4dca865300e529ccd6375bf5665`; `main` contained 0 open PRs at inspection. Feature branch `codex/versionvault-foundation`, PR [#1](https://github.com/arunabanarjee32-bit/website-old-version/pull/1).

| Code path | Verified behavior and remaining issue | Status after PR CI |
| --- | --- | --- |
| `is_permitted_url` and `begin_capture` | Exact numeric HTTP loopback fixture only, no userinfo/fragments, reject other ports/schemes/hosts; no production network isolation | **VERIFIED** for tested admission cases, public use **BLOCKED** |
| `capture_job` / `EXECUTOR` | One in-process worker; Python HTML fetch rejects redirects and caps bytes, Chromium renders with offline networking. Browser subprocess is not a hardened separate worker | **VERIFIED** fixture; production worker **BLOCKED** |
| `lifespan` / `connect` | New startup query marks stale `queued` and `running` rows `failed` with `InterruptedByRestart`, preserves `ready`/`failed`. SQLite uses WAL and per-connect `CREATE TABLE IF NOT EXISTS`; versioned migrations not present | **VERIFIED** startup-state regression test; migration **PLANNED** |
| `store_object` / `object_path` | SHA-256 object key, staging temp and atomic rename, read-time hash verification. No fsync or crash-consistency drill; no encryption/quota | **PARTIALLY IMPLEMENTED** |
| `import_snapshot` / `read_zip_entry` | Added bounded decompression reads, 10MB upload, 64KB manifest, 20MB per artifact, 25MB aggregate, compression ratio <=200, duplicate/extra entry rejection, digest typing and PNG chunk CRC/framing. ZIPs not extracted into filesystem | **VERIFIED** for new synthetic positive and nine malformed fixtures; fuzzing **PLANNED** |
| `INDEX` + `home` | Embedded frontend has date, side-by-side comparison, import/export UI; no browser interaction tests | **IMPLEMENTED BUT UNVERIFIED** |
| `.github/workflows/ci.yml` + `constraints-ci.txt` | GitHub Actions runs Python 3.13, installs Playwright-managed Chromium, checks `pip check`, compileall, selective Ruff and pytest; pins direct application/test packages, uploads installed dependency inventory. No hashed transitive lock, license SBOM or vulnerability scan | CI **VERIFIED**; full lock/SBOM **PARTIALLY IMPLEMENTED** |

**New evidence:** [successful run 43739119692](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43739119692), commit `bbd136235a50d9248d34a7e12f1f5397940f0d74`: **24 passed, 1 warning in 5.11 seconds**, selected Ruff checks and pip dependency consistency passed. Earlier [run 43738724575](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43738724575) failed 1/12 when snap Chromium took longer than the previous 17.5-second polling window; runner then moved to Playwright-managed Chromium with a 60-second bounded test deadline. This is a CI regression signal and mitigation, not proof of all future runner stability.

**Security limitations:** ZIP validation can reject malformed PNG chunk structures but is not a full image decoding or malware scan. `lifespan` recovery is not a durable job processor or retry queue. Missing CI evidence for public capture, isolation, external assets, WARC search/replay, data migrations, crash durability, authenticated access and actual UI E2E.
