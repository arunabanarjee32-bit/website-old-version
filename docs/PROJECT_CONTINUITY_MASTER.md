# VersionVault — Master Project Continuity Archive

> **Updated:** 2026-11-16 (Asia/Kolkata). **Purpose:** Let a new human developer, ChatGPT, Codex, or other AI coding session resume VersionVault **without relying on access to a long or unavailable chat**.
>
> **Start here.** This is a curated, public-safe technical record of research, user requirements, project discussions available to the author, implementation, tests, decisions, references, and unfinished work. It is **not a verbatim export of all private conversation messages**, nor does it recover inaccessible earlier chats. Original GitHub source and commits are authoritative; this document is an index and handoff, not a substitute for checking code.

**Repository:** https://github.com/arunabanarjee32-bit/website-old-version  
**Main branch, checked 2026-11-16:** `0513510d035db4dca865300e529ccd6375bf5665`  
**Open implementation PR:** [#1 — Foundation: reproducible CI, restart recovery, and safe archive import](https://github.com/arunabanarjee32-bit/website-old-version/pull/1)  
**Implementation PR head observed:** `4c47a2b1608cea6546d2a439c78a9bafd54e4c86`  
**This documentation branch:** `docs/versionvault-continuity-archive`  
**Status labels everywhere:** **VERIFIED**, **IMPLEMENTED BUT UNVERIFIED**, **PARTIALLY IMPLEMENTED**, **PLANNED**, **BLOCKED**.

## Contents

1. [Executive summary and hard boundaries](#1-executive-summary-and-hard-boundaries)
2. [What the user asked for, distilled faithfully](#2-what-the-user-asked-for-distilled-faithfully)
3. [GitHub branches, PR and implementation chronology](#3-github-branches-pr-and-implementation-chronology)
4. [Repository map and documents to read](#4-repository-map-and-documents-to-read)
5. [Actual MVP, API and file-by-file audit](#5-actual-mvp-api-and-file-by-file-audit)
6. [Testing and implementation evidence](#6-testing-and-implementation-evidence)
7. [The two primary research systems](#7-the-two-primary-research-systems)
8. [All 22 recommended upstream study repositories](#8-all-22-recommended-upstream-study-repositories)
9. [Architecture and data-flow charts](#9-architecture-and-data-flow-charts)
10. [Security, privacy, license and preservation limitations](#10-security-privacy-license-and-preservation-limitations)
11. [Prioritized implementation roadmap and dependency chart](#11-prioritized-implementation-roadmap-and-dependency-chart)
12. [Open ADRs and important decisions](#12-open-adrs-and-important-decisions)
13. [Competitive positioning, fidelity and costs](#13-competitive-positioning-fidelity-and-costs)
14. [Development and reproducibility instructions](#14-development-and-reproducibility-instructions)
15. [Conversation/project chronology and lessons](#15-conversationproject-chronology-and-lessons)
16. [Reference links, source evidence and recovery procedure](#16-reference-links-source-evidence-and-recovery-procedure)
17. [Copy-and-paste prompt for the next AI session](#17-copy-and-paste-prompt-for-the-next-ai-session)
18. [Rules for maintaining this document](#18-rules-for-maintaining-this-document)

---

## 1. Executive summary and hard boundaries

**Product goal.** VersionVault is an independent, owner-controlled **website time machine**: preserve authorized snapshots of websites; browse by URL/date; compare changes; export/import and later securely replay captured resources. Longer-term, add monitoring, private collections, search, browser extension, developer APIs and lawful AI-interface/conversation history.

**Product truthfulness.** A screenshot is not complete site preservation. Static HTML is not complete WARC capture. Archived website frontend assets do not preserve a retired server or proprietary AI model. AI-model substitutions must be labeled simulated or alternative. No competitor parity or comparative superiority should be claimed without reproducible benchmarks.

**Present working foundation on main:** a deliberately *restricted local* Python/FastAPI + SQLite + Playwright/Chromium application using a local SHA-256 object store, fixture HTML and PNG captures, asynchronous jobs through one in-process executor, simple HTML/JS interface, snapshot history/date filtering, screenshot side-by-side view and ZIP import/export. The local baseline reported **12 passing pytest tests** on 2026-11-15.

**Proposed improvement in PR #1, NOT on main until merge:** GitHub Actions CI with Playwright-managed Chromium, exact-version **direct** dependency constraints, startup cleanup of abandoned queued/running jobs, bounded ZIP decompression and manifest checks, PNG structural/CRC checks, and 12 new regression cases. [Successful CI run 43739925177](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43739925177) on the observed PR head: **24 passed, 1 warning**; selected Ruff checks and pip dependency checks passed.

**Non-negotiable security boundary:** public URL capture is **BLOCKED**. Today only HTTP URLs with literal numeric host `127.0.0.1` and fixture port `8766` are accepted. Do **not** relax this policy until separately isolated nonroot capture workers, network-level egress restrictions, redirects/DNS/metadata protections and tests exist. Do not serve untrusted archived scripts from the authenticated application's origin. Do not publish private captures/chats/secrets. Do not deploy the prototype publicly.

**Project ownership:** preserve one original VersionVault repo; prefer libraries/services through replaceable interfaces; never paste all third-party source trees into it. No root project license has been approved; maintainers must decide license, contribution and redistribution terms.

## 2. What the user asked for, distilled faithfully

The November 2026 master engineering directive asks the technical lead to:

- Audit the existing GitHub repository, current code, branches, open PRs, commits, docs, tests and real execution paths **before** changing implementation.
- Read `THIRD_PARTY_REPOS_TO_STUDY.txt` and research **exactly two primary systems**, **ArchiveBox** and **SolrWayback**, in real source code at pinned stable releases, with licenses, dependency chain, tests, APIs, deployment and performance implications. Playwright and Warcio are **supporting libraries**, not a third or fourth primary system.
- Reuse the existing FastAPI MVP instead of replacing it with an unrelated stack. Keep SQLite locally, content-addressed SHA-256 blobs and a stable VersionVault-owned canonical metadata contract.
- Prefer **REUSE → CONFIGURE → ADAPT → EXTEND → BUILD**. Keep external capture/replay engines replaceable; do not couple to upstream private tables or run multiple heavyweight services without proof.
- Establish a priority-ordered, acceptance-test-backed implementation checklist. Actually write code, run tests, document evidence, make logical commits, push a branch and open a PR if permissions allow. No claims of completed work without evidence.
- First milestone: clean setup, locking/SBOM, PR CI, static checks, reliable job restart/state handling, archive import security, regression tests, preserve fixture security boundary. Next: safe worker, WARC, upstream interoperability, isolated replay and website time-machine UX.
- Treat every user URL, ZIP upload, WARC, saved HTML/JS and private archive as untrusted. SSRF and replay isolation are **production launch gates**. Do not rely on regex-only URL validation or browser-only network blocking.
- Preserve accurate notes for the next developer or AI session; explicitly distinguish **VERIFIED** vs **PLANNED** and retain exact commands, logs, checks and PR links.
- No deployment, forced pushes, history rewrites, or merging into main without authorization.
- Include user-friendly history/timeline, two-version comparison, fidelity warnings, portable exports, eventual search, scheduling, collections, private/shared access, extension and authorized AI-history features; these are aspirations, not already implemented features.

**Explicit continuity request, 2026-11-16:** store research, discussion-derived decisions, diagrams, links, implementation history and next steps **in the GitHub repository** because long chat histories can fail to load. This document is that portable technical knowledge base. Sensitive/private raw conversation messages and unavailable transcripts are intentionally not published to the public repository.

## 3. GitHub branches, PR and implementation chronology

| When (UTC, per commit metadata) | Commit/PR | Meaning |
| --- | --- | --- |
| 2026-11-15 11:52 | [`039e0ea`](https://github.com/arunabanarjee32-bit/website-old-version/commit/039e0ea9894aac33f864ea57bea5a2896cc3a05e) | Initial repository |
| 2026-11-15 12:01 | [`e2e7372`](https://github.com/arunabanarjee32-bit/website-old-version/commit/e2e737200085a867d37fda5e3701597df00bd130) | Vision, architecture, contribution guidance and study catalog |
| 2026-11-15 13:33 | [`eceed3b`](https://github.com/arunabanarjee32-bit/website-old-version/commit/eceed3ba2da9572d19f750178ffad71c9ecc8b85) | Complete upstream research inventory |
| 2026-11-15 15:58 | [`1f7a591`](https://github.com/arunabanarjee32-bit/website-old-version/commit/1f7a591e7d42ec8399da16c6aea05e6f83c5a954) | Restricted local MVP, tests, history and export/import |
| 2026-11-15 15:59 | [`1786d0f`](https://github.com/arunabanarjee32-bit/website-old-version/commit/1786d0f997a75be07ccc89404b8248608f3c4244) | Final exact-tested MVP app source ending |
| 2026-11-15 16:01–16:07 | [`2a18c8a`](https://github.com/arunabanarjee32-bit/website-old-version/commit/2a18c8a49e3924b596b019c7e0762e2619714bd0) and later docs commits | Audit, 22-repository matrix, primary two, architecture ADR, checklist and handoff |
| 2026-11-15 16:28 | [`0513510`](https://github.com/arunabanarjee32-bit/website-old-version/commit/0513510d035db4dca865300e529ccd6375bf5665) | Concise index of previously recommended 22 study repositories; checked main head on 2026-11-16 |
| 2026-11-15 later | [PR #1](https://github.com/arunabanarjee32-bit/website-old-version/pull/1), branch `codex/versionvault-foundation` | Reliability tests, CI, ZIP safety and up-to-date research/checklist docs; open at latest inspection |
| 2026-11-16 | This documentation branch | Portable technical continuity archive, not an application change |

**Important:** branches can change after this snapshot. At the start of every new session, check GitHub's live default branch, branch HEAD, PR status, and latest CI. Do not infer a PR was merged just because it is green.

## 4. Repository map and documents to read

Actual main-branch application layout as inspected:

~~~text
README.md
AGENTS.md
CONTRIBUTING.md
LOCAL_DEMO.md
SECURITY.md
THIRD_PARTY_REPOS_TO_STUDY.txt
pyproject.toml
services/api/versionvault/
  __init__.py
  app.py
tests/
  fixture_site.py
  test_app.py
docs/
  START_HERE.md
  PRODUCT_VISION.md
  ORIGINAL_PRODUCT_BLUEPRINT.md
  FEATURES_AND_SCOPE.md
  ARCHITECTURE.md
  DATA_MODEL.md
  ROADMAP.md
  CURRENT_STATUS.md
  DECISIONS.md
  DEVELOPER_HANDOFF.md
  PREVIOUS_REPOSITORIES_TO_STUDY.txt
  REPOSITORY_RESEARCH_MATRIX.md
  TOP_TWO_REPOSITORIES.md
  REUSE_FIRST.md
  COMPETITIVE_LANDSCAPE.md
  COMPETITOR_FEATURE_GAPS.md
  REPOSITORY_AUDIT.md
  MASTER_IMPLEMENTATION_CHECKLIST.md
  QUALITY_AND_BENCHMARKS.md
  SECURITY_PRIVACY.md
  AI_PRESERVATION.md
  LEGACY_PROTOTYPE_README.md
  adr/ADR-001-capture-architecture.md
~~~

On unmerged PR #1 also expect:
- [CI workflow](https://github.com/arunabanarjee32-bit/website-old-version/blob/codex/versionvault-foundation/.github/workflows/ci.yml)
- [Direct dependency constraints](https://github.com/arunabanarjee32-bit/website-old-version/blob/codex/versionvault-foundation/constraints-ci.txt)
- [Regression suite](https://github.com/arunabanarjee32-bit/website-old-version/blob/codex/versionvault-foundation/tests/test_reliability.py)

**Recommended order for a new developer:** [README](../README.md) → [AGENTS](../AGENTS.md) → **this continuity archive** → [CURRENT_STATUS](CURRENT_STATUS.md) → [DEVELOPER_HANDOFF](DEVELOPER_HANDOFF.md) → [MASTER_IMPLEMENTATION_CHECKLIST](MASTER_IMPLEMENTATION_CHECKLIST.md) → [REPOSITORY_AUDIT](REPOSITORY_AUDIT.md) → [ADR-001](adr/ADR-001-capture-architecture.md) → [TOP_TWO_REPOSITORIES](TOP_TWO_REPOSITORIES.md) → actual code and tests.

**Other indispensable sources:** [full 22 candidates](../THIRD_PARTY_REPOS_TO_STUDY.txt), [short 22-link index](PREVIOUS_REPOSITORIES_TO_STUDY.txt), [research matrix](REPOSITORY_RESEARCH_MATRIX.md), [product vision](PRODUCT_VISION.md), [original plan](ORIGINAL_PRODUCT_BLUEPRINT.md), [feature scope](FEATURES_AND_SCOPE.md), [architecture](ARCHITECTURE.md), [data model](DATA_MODEL.md), [roadmap](ROADMAP.md), [security/privacy](SECURITY_PRIVACY.md), [AI preservation](AI_PRESERVATION.md), [quality benchmarks](QUALITY_AND_BENCHMARKS.md), [competition](COMPETITIVE_LANDSCAPE.md), [feature gaps](COMPETITOR_FEATURE_GAPS.md), [reuse-first](REUSE_FIRST.md), [legacy extension README](LEGACY_PROTOTYPE_README.md).

Note: several older docs truthfully describe the **historical planning era**, not current code. Read dated status updates and GitHub implementation evidence before using them as present-tense facts.

## 5. Actual MVP, API and file-by-file audit

| Component/file | Actual function and evidence | Current status |
| --- | --- | --- |
| `pyproject.toml` | Python ≥3.11; FastAPI, Uvicorn, Playwright, multipart; pytest/httpx test extras; version ranges, not original full lock | PARTIALLY IMPLEMENTED |
| `app.py: is_permitted_url` | Numeric-loopback HTTP host `127.0.0.1`, fixture port, 2,048-character limit, rejects fragments/userinfo and other schemes/hosts | VERIFIED for fixture test cases; public URL admission BLOCKED |
| `app.py: connect` | SQLite WAL, timeout, creates jobs and snapshots tables on connect; lacks versioned migrations and robust process lifecycle | PARTIALLY IMPLEMENTED |
| `app.py: begin_capture` | POST creates queued DB job and submits to global one-worker ThreadPoolExecutor | VERIFIED for fixture |
| `app.py: capture_job` | Permitted 200 text/html fixture fetched via Python with redirects forbidden and ~2 MB HTML limit; offline Chromium renders content and screenshots; error recorded as exception class | VERIFIED for fixture; not a general crawler |
| `app.py: store_object/object_path` | SHA-256 content addressing, temporary rename, readback hash validation; no fsync crash-durability proof | PARTIALLY IMPLEMENTED |
| `app.py: snapshots` | SQLite history ordered by captured_at and ID, snapshot metadata and PNG endpoint | VERIFIED for tested API paths |
| `app.py: export_snapshot` | Snapshot ZIP with JSON manifest, HTML and PNG; screenshot and HTML looked up by SHA | VERIFIED for fixture |
| `app.py: import_snapshot` on main | Reads bounded uploaded ZIP; validates expected names, hashes and PNG signature; needs stronger ratio, aggregate and PNG structure checks | PARTIALLY IMPLEMENTED |
| `app.py: INDEX/home` | Embedded HTML/CSS/JS UI, URL form, job status, date filtering, Left/Right image selection, ZIP export/import | IMPLEMENTED BUT UNVERIFIED in actual browser UI E2E |
| `tests/fixture_site.py` | Local controlled fixture on 127.0.0.1:8766 | VERIFIED |
| `tests/test_app.py` | Nine rejected-URL cases; home/empty list; capture/screenshot/history/export/import; corrupted import and unknown resources | VERIFIED on local main baseline |
| `tests/test_reliability.py` | PR #1 only: 12 additional tests, hostile import/restart cases | VERIFIED in PR #1 CI; not on main |
| `.github/workflows/ci.yml` | PR #1 only: Python 3.13, Playwright Chromium, selected Ruff/compileall/pytest/pip check, pip-freeze artifact | VERIFIED in PR #1 CI; not on main |
| WARC/WACZ, ArchiveBox integration | No actual running code | PLANNED |
| SolrWayback/secure replay | No actual running code | BLOCKED pending isolated evaluation |
| Auth, tenant isolation, public sharing/hosting | No actual running code | BLOCKED |
| Browser extension code | Historical prototype README only, source not in this repo | BLOCKED pending review |
| Computed visual/text diff, scheduled monitoring, full-text search | Not built; only side-by-side screenshot UI | PLANNED |

**Actual API inventory:**
- `GET /` local demo UI.
- `POST /api/captures` queue fixture capture; returns 202/job ID.
- `GET /api/jobs/{job_id}` read queued/running/ready/failed state.
- `GET /api/snapshots` list snapshots with ISO UTC capture timestamps.
- `GET /api/snapshots/{snapshot_id}` metadata.
- `GET /api/snapshots/{snapshot_id}/screenshot` PNG with restrictive MIME/CSP headers.
- `GET /api/snapshots/{snapshot_id}/export` ZIP manifest + HTML + PNG.
- `POST /api/import` checked ZIP import, 201 or error.

**Data schema on main:** SQLite `jobs(id, url, state, error, created_at)` and `snapshots(id, url, title, captured_at, screenshot_sha, html_sha)`; content bytes in `.versionvault-data/objects/<sha256>`. Multi-tenant users/collections/resources are *planned* in [DATA_MODEL](DATA_MODEL.md); not present in SQLite.

**PR #1 reliability delta:** startup sets orphaned `queued`/`running` jobs to `failed` with `InterruptedByRestart`; that does **not** resume jobs or implement a durable queue. ZIP budget: input 10 MB, manifest 64 KB, per HTML/image entry 20 MB, aggregate decompressed 25 MB, compression ratio cutoff 200; duplicate/extra/encrypted entries rejected; PNG chunks/CRC checked. This improves negative-case handling but does not constitute complete archive fuzzing, PNG decoding or production hardening.

**Important caveat:** the allowed fixture port is configurable via `VV_FIXTURE_PORT`; that configuration is for controlled tests, **not** permission to broaden target origins.

## 6. Testing and implementation evidence

| Evidence source | Scope | Recorded result | Interpretation |
| --- | --- | --- | --- |
| 2026-11-15 local main prototype run (recorded in audit) | `PYTHONPATH=services/api pytest -q` | **12 passed** | Historical local test, restricted fixture only |
| [CI run 43738724575](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43738724575) | Early PR with Ubuntu Snap Chromium | **1 failed, 11 passed** (capture timed out in old ~17.5s poll window) | Motivated managed Chromium and 60s bounded wait |
| [CI run 43738795969](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43738795969) | PR code/reliability | **24 passed, 1 warning** | Negative cases and fixture flow in hosted CI |
| [CI run 43739119692](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43739119692) | Revised managed Chromium | **24 passed, 1 warning** | Validated revised browser runner |
| [CI run 43739925177](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43739925177) | Final observed implementation PR head `4c47a2b...` | **24 passed, 1 warning in 2.14s**; pip check and selected Ruff passed | Best recorded PR #1 evidence; branch still requires review/merge |

**Not yet run successfully:** true browser UI journey E2E; multi-resource authorized crawl; WARC generation and validation; SolrWayback index/replay; ArchiveBox vs Playwright comparison; high-load CPU/RAM/throughput; process/filesystem crash and fsync testing; DNS rebinding and egress sandbox tests; malicious JavaScript origin isolation; permission/tenant tests; complete license/SBOM/audit.

No test report should turn an untested item into VERIFIED. After changes to code, rerun tests at the **new HEAD**.

## 7. The two primary research systems

### Primary 1 — ArchiveBox, capture and orchestration

- Repository: https://github.com/ArchiveBox/ArchiveBox
- Stable baseline checked 2026-11-15: [v0.9.77](https://github.com/ArchiveBox/ArchiveBox/releases/tag/v0.9.77), published 2026-10-27. Verify latest again before integration.
- Stable tag `LICENSE`: MIT; this **does not** imply every external dependency/binary is MIT.
- Source modules checked at stable tag: [CLI add](https://github.com/ArchiveBox/ArchiveBox/blob/v0.9.77/archivebox/cli/archivebox_add.py), [runner](https://github.com/ArchiveBox/ArchiveBox/blob/v0.9.77/archivebox/services/runner.py), [crawl models](https://github.com/ArchiveBox/ArchiveBox/blob/v0.9.77/archivebox/crawls/models.py), [snapshot/core models](https://github.com/ArchiveBox/ArchiveBox/blob/v0.9.77/archivebox/core/models.py), [crawl API](https://github.com/ArchiveBox/ArchiveBox/blob/v0.9.77/archivebox/api/v1_crawls.py), [pyproject](https://github.com/ArchiveBox/ArchiveBox/blob/v0.9.77/pyproject.toml), [Compose](https://github.com/ArchiveBox/ArchiveBox/blob/v0.9.77/docker-compose.yml), plugins and tests.
- Evidence: CLI validates URL sources and supports crawl depth, URL/time/size and plugin options; Django/Ninja routes accept crawl records; runner coordinates plugin events and snapshot lifecycle. This does **not** prove capture isolation, fidelity, or VersionVault compatibility.
- Deployment considerations: Django, abx plugin infrastructure, browser/external binaries and significant operational complexity. The tag's Compose example uses unpinned `latest` image and has an external archive submission setting—pin immutable images and disable unapproved external publishing in any isolated experiment.
- **Recommendation: EXPERIMENT FURTHER** as an optional, separate capture CLI/service adapter. Keep existing Playwright-only local capture fallback. Never bind VersionVault canonical records to ArchiveBox Django tables.
- **Needed evidence:** pinned environment and dependency/license SBOM; authorized fixture capture; output artifact inventory, original/final URL, HTTP assets and missing assets; hashes, failure signals, CPU/RAM/time/disk, restart, privacy controls, rollback.

### Primary 2 — SolrWayback, WARC indexing, search and replay

- Repository: https://github.com/netarchivesuite/solrwayback
- Stable baseline checked 2026-11-15: [5.5.0](https://github.com/netarchivesuite/solrwayback/releases/tag/5.5.0), published 2026-09-15. Verify latest again before integration.
- Stable tag `LICENSE.txt`: Apache-2.0; bundled WARC indexer and all transitive dependencies still require review.
- Source modules checked at stable tag: [WarcParser.java](https://github.com/netarchivesuite/solrwayback/blob/5.5.0/src/main/java/dk/kb/netarchivesuite/solrwayback/parsers/WarcParser.java), [WARC indexer script](https://github.com/netarchivesuite/solrwayback/blob/5.5.0/src/bundle/indexing/warc-indexer.sh), [Solr schema](https://github.com/netarchivesuite/solrwayback/blob/5.5.0/src/bundle/solr_config/conf/schema.xml), [pom.xml](https://github.com/netarchivesuite/solrwayback/blob/5.5.0/pom.xml), API/webapp code and tests.
- Evidence: WARC parsing and source-offset retrieval; indexer invokes UKWA webarchive-discovery and writes to Solr; schema supports URL/crawl-date/source and search metadata. Configured indexer defaults observed: two threads and 2048 MiB *heap setting per process*—not a measured VersionVault memory benchmark.
- Deployment considerations: WARC data, compatible indexer JAR/config, Java/Solr/web application runtime, derived Solr index, appropriate isolated replay origin. Release notes have addressed some live-resource leakage; do not assume all replay paths are safe.
- **Recommendation: DEFER integration into MVP; EXPERIMENT FURTHER** when there is a controlled, Warcio-validated WARC fixture and a network-isolated test environment.
- **Crucial open question:** Can **our** future WARC be indexed, searched by known URL/time, and replayed with correct assets **without live network fallback**? **NOT TESTED**. Do not assert interoperability.
- Exact experiment: create lawful fixture WARC; validate records with Warcio; index into isolated Solr; query URL and UTC timestamp; retrieve HTML/image/CSS/JS; verify hashes and missing-resource behavior; test zero live third-party requests; log CPU/memory/disk/time; independently review license and deployment; record ADR result.

### Supporting libraries, not additional primary systems

- [Playwright](https://github.com/microsoft/playwright): browser rendering, screenshots, UI E2E; already used by local MVP.
- [Warcio](https://github.com/webrecorder/warcio): future WARC read/write and independent standards validation; **not yet used for a real WARC pipeline**.
- Supporting libraries and research references should not be reclassified as a third primary archival system.

## 8. All 22 recommended upstream study repositories

**Complete inventory source:** [THIRD_PARTY_REPOS_TO_STUDY.txt](../THIRD_PARTY_REPOS_TO_STUDY.txt). Names/license descriptions below reflect the 2026-11-15 repository research and require revalidation at selected release before use. **Only ArchiveBox and SolrWayback are the two primary systems.**

| # | Upstream link | Research role | License caution / decision |
| --- | --- | --- | --- |
| 01 | [ArchiveBox](https://github.com/ArchiveBox/ArchiveBox) | capture/orchestration | MIT at studied tag; **PRIMARY 1** |
| 02 | [Playwright](https://github.com/microsoft/playwright) | browser automation/UI testing | Apache-2.0 metadata; supporting library |
| 03 | [Warcio](https://github.com/webrecorder/warcio) | WARC I/O | Apache-2.0 metadata; supporting library |
| 04 | [ArchiveWeb.page](https://github.com/webrecorder/archiveweb.page) | interactive browser archiving | AGPL-3.0; license gate |
| 05 | [ReplayWeb.page](https://github.com/webrecorder/replayweb.page) | WARC/WACZ playback | AGPL-3.0; license gate |
| 06 | [Browsertrix](https://github.com/webrecorder/browsertrix) | managed capture platform | AGPL-3.0; benchmark alternative only |
| 07 | [Browsertrix Crawler](https://github.com/webrecorder/browsertrix-crawler) | high-fidelity dynamic crawl | AGPL-3.0; study/benchmark |
| 08 | [SolrWayback](https://github.com/netarchivesuite/solrwayback) | WARC search/replay | Apache-2.0 at studied tag; **PRIMARY 2** |
| 09 | [pywb](https://github.com/webrecorder/pywb) | replay/url rewriting | GPL-3.0; license gate |
| 10 | [Heritrix3](https://github.com/internetarchive/heritrix3) | very large crawls | Apache-2.0 source license; defer |
| 11 | [SingleFile](https://github.com/gildas-lormeau/SingleFile) | portable single-page HTML | AGPL-3.0; license gate |
| 12 | [OldWeb.today](https://github.com/oldweb-today/oldweb-today) | historical browser emulation | AGPL-3.0; inspiration |
| 13 | [changedetection.io](https://github.com/dgtlmoon/changedetection.io) | monitoring/notifications | Apache-2.0; future optional |
| 14 | [Celery](https://github.com/celery/celery) | distributed tasks | BSD-3-Clause source license; only if needed |
| 15 | [Meilisearch](https://github.com/meilisearch/meilisearch) | dedicated search | mixed MIT/BUSL-1.1; edition/license check |
| 16 | [Keycloak](https://github.com/keycloak/keycloak) | enterprise OIDC | Apache-2.0; future optional |
| 17 | [SeaweedFS](https://github.com/seaweedfs/seaweedfs) | distributed object storage | Apache-2.0; later |
| 18 | [LibreChat](https://github.com/LibreChat-AI/LibreChat) | AI chat UI reference | MIT; not retired-model preservation |
| 19 | [Gemini Vault Exporter](https://github.com/crytomato529/gemini-vault-exporter) | authorized AI exports | ALL RIGHTS RESERVED at reviewed source; do not copy |
| 20 | [Live Archiver](https://github.com/hexnod/live-archiver) | chat/file archival | Apache-2.0 metadata; reference |
| 21 | [ChatGPT Archive Tools](https://github.com/jamesmoore/chatgpt-archive-tools) | local user export browsing | MIT metadata; reference |
| 22 | [Awesome Web Archiving](https://github.com/iipc/awesome-web-archiving) | ecosystem catalog | CC0-1.0 metadata; reference |

**Do not bulk-integrate all 22.** License metadata is not a grant for VersionVault to republish third-party code. AGPL service separation alone is not a conclusive licensing escape. Actual release-specific dependency/license and vulnerability audit required.

## 9. Architecture and data-flow charts

These GitHub-native **Mermaid diagrams** represent **architectural proposals** unless explicitly labeled IMPLEMENTED.

### 9.1 Implemented local MVP (main)

~~~mermaid
flowchart TD
    U["Local user / embedded HTML UI"] --> API["FastAPI routes"]
    API --> V["Strict numeric loopback fixture URL validation"]
    V --> J["SQLite jobs + one in-process ThreadPoolExecutor"]
    J --> H["Python 200 HTML fetch; redirects denied; 2MB cap"]
    H --> P["Playwright Chromium offline rendering"]
    P --> SH["PNG screenshot"]
    P --> HT["Fetched HTML"]
    SH --> O["SHA-256 object directory"]
    HT --> O
    O --> DB["SQLite snapshot metadata"]
    DB --> UI["History / date / two-image comparison"]
    DB --> ZIP["ZIP manifest + PNG + HTML export/import"]
~~~

### 9.2 Proposed secure target (NOT implemented)

~~~mermaid
flowchart TD
    C["User / future extension / API"] --> A["VersionVault FastAPI: authz, quotas, URL validation"]
    A --> Q["Durable job states and queue"]
    Q --> W["Isolated nonroot capture worker + enforced egress policy"]
    W --> AD{"Replaceable CaptureAdapter"}
    AD --> PW["Playwright fallback"]
    AD --> AB["ArchiveBox external engine (research)"]
    PW --> VAL["Artifact validation / missing-resource & fidelity classification"]
    AB --> VAL
    VAL --> S["Immutable SHA-256 objects and VersionVault SQLite/Postgres metadata"]
    S --> WARC["WARC/WACZ pipeline, Warcio validation (future)"]
    WARC --> IDX["Replaceable SearchReplayAdapter"]
    IDX --> SOLR["SolrWayback + Solr, isolated (research)"]
    IDX --> ALT["Other licensed option if tests justify"]
    SOLR --> R["Separate-origin sandboxed historical viewer"]
    ALT --> R
    S --> UI["Owned history / compare / export UI"]
    R --> UI
~~~

**Never** render archive JavaScript in the trusted FastAPI origin. The default archive viewer must not fetch live third-party resources as an implicit fallback.

### 9.3 Capture lifecycle, including restart semantics

~~~mermaid
stateDiagram-v2
    [*] --> queued: POST capture
    queued --> running: worker claims job
    running --> ready: snapshot and hashes committed
    running --> failed: capture/browser/storage error
    queued --> failed: app startup detects abandoned job (PR #1)
    running --> failed: app startup detects abandoned job (PR #1)
    ready --> [*]
    failed --> [*]
~~~

PR #1 marks abandoned jobs **failed**, not automatically retried. A future proper worker may require explicit leases, bounded retries, crash recovery and idempotency.

### 9.4 Standards-based WARC compatibility experiment (NOT RUN)

~~~mermaid
sequenceDiagram
    participant Fixture as Authorized fixture
    participant Capture as Future capture adapter
    participant Warcio as Warcio validation
    participant Indexer as WARC indexer
    participant Solr as Solr search
    participant Replay as Isolated replay viewer
    Capture->>Fixture: Capture authorized HTTP resources
    Fixture-->>Capture: HTML/CSS/JS/image responses
    Capture->>Warcio: Produce and validate candidate WARC
    Warcio-->>Indexer: Verified file and records
    Indexer->>Solr: Index URL, timestamps, source offsets
    Replay->>Solr: Query archived URL at timestamp
    Solr-->>Replay: Historical records
    Note over Replay: Verify all assets; no live fallback, no app cookies
~~~

## 10. Security, privacy, license and preservation limitations

### Capture / SSRF gate

- Only the controlled numeric loopback fixture currently accepted. Preserve this guard until a nonroot isolated worker with OS/container-enforced egress deny rules exists.
- For future public capture validate redirects and final destinations, all DNS answers, IPv4/IPv6 private/link-local/loopback/metadata endpoints, rebinding, host forms, proxies and transport behavior. Validate with adversarial network tests, not a regex-only check.
- Apply authorization, per-host/request/concurrency/bytes/time/CPU/RAM limits, no secrets or session cookies in workers, sandboxed Chromium, no arbitrary host mounts, and no unsafe service defaults.

### Archive import / storage

- Validate ZIP member whitelist and duplicates, upload/entry/aggregate decompressed sizes, ratios, CRC/image structure/hashes/manifest schema, path/symlink behavior and resource exhaustion.
- Object keys must be immutable SHA-256 content identifiers; publish only after atomic writes, file/dir sync, verification and database commits are safe under failures. Add corruption, disk-full, simultaneous write, restart and restore drills.
- Imported HTML is untrusted data and must not execute in VersionVault origin.

### Replay isolation

- Separate registrable/origin context, no application cookies or privileged API access, restrictive CSP and sandbox policies, no unauthorized live asset requests or service workers, clear warnings for missing assets and no backend restoration claims.
- Replay blockers cannot be bypassed by pointing SolrWayback/ArchiveBox directly at the authenticated app.

### Privacy/legal

- Never publish private website captures, user conversations, tokens or credentials automatically.
- Include consent, ownership, retention, deletion/export, copyright/takedown policies and audit logs before real multi-user hosted use.
- Root license and inbound contribution terms are **open maintainer decisions**. Do not add a root LICENSE without owner approval.
- A public GitHub repository is not a private conversation archive; this document contains only technical summaries and public links.

### Truthful archival fidelity labels

| Type | Can legitimately claim | Cannot legitimately claim |
| --- | --- | --- |
| Screenshot | Saved visual image at observed time | Live functionality or resource-complete replay |
| Static HTML | Saved markup; maybe limited offline rendering | All CSS/images/scripts/server behavior |
| WARC/WACZ resource archive | Recorded HTTP responses included in verified package | Missing backend operations, unrecorded assets or 100% fidelity |
| Historical replay | Recorded resources served in isolated viewer within tested scope | Actual historical provider server restored |
| AI interface/chat history | Historical visible UI and authorized recorded conversation | Continued inference by retired proprietary model |
| Simulation/alternative AI | A different presently accessible model offering a comparable experience | Exact prior model behavior or identity |

## 11. Prioritized implementation roadmap and dependency chart

**Existing complete detailed task list:** [MASTER_IMPLEMENTATION_CHECKLIST](MASTER_IMPLEMENTATION_CHECKLIST.md). The following is an executive priority view; **status reflects PR vs main explicitly.**

| Priority | Task and acceptance target | State at 2026-11-16 inspection |
| --- | --- | --- |
| P0 | Repo baseline and 22-repo study, two primary choice, ADR | VERIFIED as documentation |
| P0 | Fixture capture/screenshot/history/ZIP workflow, 12 baseline tests | VERIFIED within original restricted scope on main |
| P0 | CI on PR with Playwright-managed browser and 24 tests | VERIFIED **only on PR #1** |
| P0 | Orphaned queued/running restart recovery | VERIFIED by **PR #1 test**; no durable retries |
| P0 | More restrictive ZIP/manifest/PNG checks | VERIFIED for **PR #1 synthetic cases**; fuzzing incomplete |
| P0 | Fully hash-locked **transitive** dependencies + license/SBOM inventory | PARTIALLY IMPLEMENTED (direct constraints only in PR #1) |
| P0 | Versioned SQLite schema migration + constraints and recovery tests | PLANNED |
| P0 | fsync/atomic durability, object integrity, restore/fault injection | PARTIALLY IMPLEMENTED |
| P0 | Nonroot process isolation, egress policies, redirect/DNS/rebinding tests | BLOCKED, launch gate |
| P1 | Browser UI E2E capture → history/date → compare → export/import | PLANNED |
| P1 | CaptureAdapter interface and ArchiveBox v0.9.77 isolated fixture test | PLANNED |
| P1 | Warcio-backed WARC creation and independently validated resource fixtures | PLANNED |
| P1 | SolrWayback 5.5.0 WARC index/search/replay/interoperability | BLOCKED pending safe WARC fixture and isolation |
| P1 | Separate replay origin + fidelity/missing-resource report | BLOCKED |
| P2 | Computed visual/text diffs, search and history usability/accessibility | PLANNED |
| P2 | Scheduling, change alerts, collections, tags, extension | PLANNED |
| P2 | AI historical interface/catalog and authorized private exports | PLANNED |
| P0 launch | Auth/authz, per-tenant privacy, quota/takedown, secure deployment/monitoring | BLOCKED |

~~~mermaid
flowchart TD
    CI["P0: fixture CI + tests (PR #1)"] --> LOCK["P0: transitive lock + SBOM"]
    CI --> MIG["P0: SQLite migrations + crash recovery"]
    MIG --> DUR["P0: fsync, object integrity + fault tests"]
    CI --> UI["P1: browser UI E2E"]
    LOCK --> WORKER["P0: isolated worker + egress threat suite"]
    DUR --> WORKER
    WORKER --> ARCH["P1: ArchiveBox isolated adapter trial"]
    WORKER --> WARC["P1: WARC / Warcio fixtures"]
    WARC --> SOLR["P1: SolrWayback index & offline replay trial"]
    SOLR --> REPLAY["P1: safe replay integration decision"]
    WORKER --> PUBLIC["PUBLIC URL capture security gate"]
    REPLAY --> UX["P2: timeline/search/diff/fidelity UX"]
    UI --> UX
    PUBLIC --> MON["P2: opt-in scheduling and change alerts"]
    UX --> PROD["P0 launch: auth, quotas, legal, secure staging"]
    MON --> PROD
~~~

**Recommended next smallest PR:** after PR #1 review, implement a complete locked dependency install + transitive license/SBOM report, without expanding capture/network scope. Next: versioned SQLite migrations, fault-injection storage tests, browser UI E2E. Do not start huge WARC/Solr infrastructure in the same PR.

## 12. Open ADRs and important decisions

| Decision | Current interpretation | Follow-up |
| --- | --- | --- |
| ADR-001 Capture | Keep owned FastAPI/SQLite/local storage; Playwright fixture fallback; evaluate ArchiveBox external adapter | Benchmark pinned release before adoption |
| ADR-002 Replay | SolrWayback primary replay research; interoperability not proven | WARC-index-playback and isolation test |
| ADR-003 Data | SQLite now; PostgreSQL later only when measured workloads justify it | Migrations, schema and ownership |
| ADR-004 Identity | No public auth currently | OIDC/tenant model and tests before launch |
| ADR-005 License and contributions | No root license chosen | Maintainer decision; dependency notices |
| ADR-006 Crawling, copyright, takedown | Public capture disabled | Policy/authorization and legal review |
| ADR-007 Private vs public niche | Private-first, usability emphasis is hypothesis | Demand research |
| ADR-008 Monitoring | Do not import full monitoring stack prematurely | Lightweight scheduling after safe capture |
| ADR-009 AI history | Preserve UI evidence/user-owned exports, not retired inference | Provider source chronology, sensitive import controls |

[ADR-001 text](adr/ADR-001-capture-architecture.md) is accepted **for research/MVP only**, not formal approval of production integration. Older [DECISIONS](DECISIONS.md) entries may still say “pending” historically; use the ADR and tested implementation as current evidence.

## 13. Competitive positioning, fidelity and costs

Relevant ecosystem: [Wayback Machine](https://web.archive.org/), [Archive-It](https://archive-it.org/), [Webrecorder](https://webrecorder.net/), [ArchiveBox](https://archivebox.io/), [changedetection.io](https://changedetection.io/), [Browsertrix Crawler docs](https://crawler.docs.browsertrix.com/), [ReplayWeb.page docs](https://replayweb.page/docs/user-guide/).

**Opportunity hypotheses:** simple authorized capture workflow, transparent per-capture fidelity, approachable historical navigation, side-by-side and later computed diffs, easy export/restore, private-first self-hosting and API. These are hypotheses, **not evidence of market leadership**.

**Benchmark before claims:** 30+ permissioned/owned fixtures across static HTML, modern JS, images/fonts/CSS, SPA routing, inaccessible resources and intentional failure cases. Measure capture completion, expected-resource completeness, replay quality, time, disk bytes, CPU seconds, peak RAM, export/import roundtrip, search quality and privacy isolation. Publish exact environment/version/config, not synthetic benchmark claims.

**Cost model, not measured pricing:**
- Storage = total bytes per capture × capture frequency × retention × replica/backups factor.
- Compute = browser startup and rendering seconds + indexer CPU/RAM demand + background-worker overhead.
- Bandwidth = bytes downloaded from authorized targets + bytes served to viewers/backups.
- Operations = hardware/VM + security monitoring + upgrade, support and abuse/legal processes.
- Local SQLite + filesystem + one worker is the economical default; do not add Kubernetes, Solr production cluster, PostgreSQL, Celery, S3 or always-on managed tools without a measured need.

## 14. Development and reproducibility instructions

### Existing main-branch local MVP

Requirements: Python 3.11+; Chromium at `/usr/bin/chromium` or specify `VV_CHROMIUM`; a test fixture on localhost only.

~~~bash
git clone https://github.com/arunabanarjee32-bit/website-old-version.git
cd website-old-version
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
# Terminal A
python tests/fixture_site.py
# Terminal B
uvicorn versionvault.app:app --app-dir services/api --host 127.0.0.1 --port 8765
# Terminal C
PYTHONPATH=services/api pytest -q
~~~

Open http://127.0.0.1:8765/ and capture the allowed http://127.0.0.1:8766/ fixture. **NEVER bind 0.0.0.0 or deploy publicly.**

### Test proposed PR #1 code (not on main until merged)

~~~bash
git fetch origin
git switch codex/versionvault-foundation
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]' -c constraints-ci.txt
python -m playwright install chromium
python -m pip check
python -m compileall -q services tests
python -m pytest -q
~~~

**Browser path caveat:** app default is `/usr/bin/chromium`. In GitHub Actions, the workflow sets `VV_CHROMIUM` to Playwright-managed Chromium's executable path. Replicate this environment selection locally if needed. On some hosts browser subprocess sandbox behavior differs; CI success is not security validation.

**Smoke path:** permitted POST capture → status poll ready → GET snapshot history → retrieve PNG → ZIP export → ZIP import → second snapshot; malformed archives rejected. UI DOM interactions require a separate future browser E2E suite.

## 15. Conversation/project chronology and lessons

This section intentionally preserves **decision-bearing project context** rather than pretending that full historical chats are retrievable. Known project discussion topics:

- **2026-11-13, original project kickoff:** user asked for a serious VersionVault product, source inspection and deep research. An original blueprint and later documents were committed. Key principle: do not write an unrelated fresh app or inaccurately claim an advanced crawler exists.
- **2026-11-13, AI model and website preservation discussion:** user asked whether previous website versions could preserve backend access and whether “lovely” AI models could be retained. The resulting technical boundary: frontend HTML/screenshot/archive cannot revive a retired proprietary inference backend; preserve interface history, authorized exports and model availability metadata instead.
- **2026-11-15, project access and GitHub state:** user wanted to inspect PRs, merge if appropriate, identify previously suggested repositories and commit a TXT list. The repository's [22-link concise index](PREVIOUS_REPOSITORIES_TO_STUDY.txt) was committed to main; later live check identified PR #1 open. No unauthorized merge should be performed.
- **2026-11-15, master architecture/implementation directive:** user provided extensive requirements for full code audit; exactly two primary upstream systems; reliable local CI, tests, security and documentation; actual implementation and PR; no speculative production claims. The full technical substance is summarized in this archive and cross-linked to the repository's canonical docs.
- **2026-11-15, execution results:** a new implementation branch, regression tests and CI were committed as PR #1; after an early Snap Chromium timeout, managed Playwright Chromium and bounded test wait produced 24 passing tests on hosted CI. Upstream capture/replay compatibility was not run.
- **2026-11-16, project continuity problem:** user explained that long ChatGPT chats may fail to load and asked for all available research, links, diagrams, plans and technical findings to be durable GitHub files. This master Markdown document records that context and gives future sessions a bootstrapping prompt.

**What is not archived here:** inaccessible verbatim older messages, private conversations, hidden model reasoning, credentials, account data, uploaded private source material not in the repository. A new session should read GitHub code/documents, not assume ChatGPT can recover prior chat internals.

**Lessons to retain:** repository evidence beats historical documents; test actual code; document PR vs main; treat security gates as non-negotiable; small tested changes before large services; maintain stable references and update dates.

## 16. Reference links, source evidence and recovery procedure

**Canonical GitHub entry points**
- [Repository](https://github.com/arunabanarjee32-bit/website-old-version)
- [Main README](../README.md), [AGENTS.md](../AGENTS.md), [local demo](../LOCAL_DEMO.md), [security policy](../SECURITY.md)
- [Full research matrix](REPOSITORY_RESEARCH_MATRIX.md), [chosen top two](TOP_TWO_REPOSITORIES.md), [master checklist](MASTER_IMPLEMENTATION_CHECKLIST.md)
- [Status](CURRENT_STATUS.md), [developer handoff](DEVELOPER_HANDOFF.md), [repository audit](REPOSITORY_AUDIT.md)
- [Architecture](ARCHITECTURE.md), [data model](DATA_MODEL.md), [ADR-001](adr/ADR-001-capture-architecture.md)
- [Original user product blueprint](ORIGINAL_PRODUCT_BLUEPRINT.md), [vision](PRODUCT_VISION.md), [features](FEATURES_AND_SCOPE.md)
- [22 repository list](../THIRD_PARTY_REPOS_TO_STUDY.txt), [short repo link index](PREVIOUS_REPOSITORIES_TO_STUDY.txt)
- [Official release ArchiveBox v0.9.77](https://github.com/ArchiveBox/ArchiveBox/releases/tag/v0.9.77), [SolrWayback 5.5.0](https://github.com/netarchivesuite/solrwayback/releases/tag/5.5.0)
- [Foundation PR #1](https://github.com/arunabanarjee32-bit/website-old-version/pull/1), [latest reported successful PR test](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43739925177)
- [OpenAI API deprecation documentation](https://developers.openai.com/api/docs/deprecations), [Google Gemini API deprecation documentation](https://ai.google.dev/gemini-api/docs/deprecations)

**When an old ChatGPT conversation will not load:** open the GitHub repo directly, navigate to this master file and use the prompt below. Confirm branch and PR state. If a file is only on an unmerged branch, open it via its branch-specific URL or fetch that branch, rather than assuming it is on main. Prefer GitHub PR/CI logs as evidence of actions completed.

**Integrity of record:** documents are intentionally human- and AI-readable text; Git history tracks edits. Do not store raw credentials or private chat transcripts in this public repository. For private backups of personal conversations, use a private repository or encrypted export maintained by the owner instead.

## 17. Copy-and-paste prompt for the next AI session

> I am continuing the existing VersionVault project. Repository:
> https://github.com/arunabanarjee32-bit/website-old-version
>
> First read `docs/PROJECT_CONTINUITY_MASTER.md`, `AGENTS.md`, `README.md`, `docs/CURRENT_STATUS.md`, `docs/DEVELOPER_HANDOFF.md`, `docs/MASTER_IMPLEMENTATION_CHECKLIST.md`, `docs/TOP_TWO_REPOSITORIES.md` and `docs/adr/ADR-001-capture-architecture.md`. If the continuity file is not on main yet, find its documentation PR/branch rather than assuming it does not exist.
>
> Inspect the actual latest main commit, all open PRs, feature branches, changed files, checks and current tests. Do not trust dated documents as proof of merged functionality. The currently known baseline is fixture-only FastAPI/SQLite/Playwright with 12 historical main-branch passing tests. Reliability/CI changes with 24 passing PR tests are in PR #1, not necessarily merged. Do **not** allow arbitrary public URLs or run archived HTML/JS on the app origin.
>
> Exactly two primary research systems: ArchiveBox (capture) and SolrWayback (WARC index/replay). Playwright and Warcio are supporting libraries. Source and licensing research is documented; actual upstream interoperability remains untested.
>
> Continue with the smallest high-priority uncompleted task: check PR #1 status, then complete a **fully transitive hash-locked dependency install and license-reviewed SBOM**, with CI proof, followed by SQLite migrations and crash-durability tests. Preserve existing functionality. Create a feature branch/PR, run tests, update checklist and this continuity archive, provide exact commit/CI/PR evidence; do not merge main without permission.
>
> Never claim implementation or benchmark success without code and test evidence. Make the next session resumable.

## 18. Rules for maintaining this document

1. At the end of **every meaningful coding/research session**, append a dated checkpoint **with exact branch, commit, PR link, changed paths, commands, test counts, CI run URLs, failures, risks, next smallest task**.
2. Re-evaluate PR/main status live; a feature branch's success is not merged-main success.
3. Update current status/checklist, source research/version pins/ADR and this file consistently. Preserve old history without representing it as present.
4. Add only **public-safe** summaries. Do not commit user conversations in raw form, screenshots of private pages, tokens, cookie jars, model prompts with personal information, or private WARC content to a public repo.
5. Keep all architecture diagrams labeled implemented/proposed and Mermaid-compatible on GitHub.
6. If a finding was only read or reasoned, label it **source-inspected/research**. If an experiment was not executed, label **NOT TESTED**.
7. New questions: record them as **OPEN** with an owner/acceptance test; do not silently decide licensing, deployment exposure or product scope.
8. Keep a narrow implementation PR separate from large knowledge-base updates when that improves reviewability.

**Document reliability statement:** this file aggregates documented and conversation-visible technical context as of 2026-11-16. It preserves context for continuation, but cannot substitute for live code inspection and cannot reconstruct every message in inaccessible previous chats.
