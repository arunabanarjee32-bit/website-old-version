# MASTER IMPLEMENTATION CHECKLIST

As of 2026-11-15. [x] means acceptance evidence exists **only for the stated scope** (some API tests do not prove browser UX or production security). No feature is complete simply because a design document names it. Local test command: PYTHONPATH=services/api pytest -q; verified 12 passed using the controlled fixture in this session. GitHub Actions CI and upstream benchmarks have **not run**.

Statuses: Verified, Partial UI, Planned, Blocked. P0 critical, P1 high, P2 next, P3 future. See docs/REPOSITORY_AUDIT.md for status detail, docs/adr/ADR-001-capture-architecture.md for architecture, and LOCAL_DEMO.md for demo instructions.


## Milestone 0 — Foundation

- [x] **M0-01: Repository audit + baseline** — P0; status **Verified**.
  - **Dependencies:** GitHub access. **Tasks:** Inspect every file/tree/branch/commit.
  - **Acceptance:** No planned feature claimed shipped. **Tests:** Cross-check GitHub tree.
  - **Reuse:** GitHub API. **Docs:** REPOSITORY_AUDIT.md. **Evidence:** Existing audit.
- [x] **M0-02: Exactly two upstream systems + ADR** — P0; status **Verified**.
  - **Dependencies:** 22-repo inspection. **Tasks:** Select capture and replay bases.
  - **Acceptance:** Two decisions with constraints. **Tests:** Source/license trace.
  - **Reuse:** ArchiveBox; SolrWayback. **Docs:** TOP_TWO_REPOSITORIES.md, ADR-001. **Evidence:** Research matrix + ADR.
- [x] **M0-03: Local fixture app and tests** — P0; status **Verified locally**.
  - **Dependencies:** Python, Chromium. **Tasks:** API/UI, local store and pytest.
  - **Acceptance:** Controlled fixture capture succeeds. **Tests:** pytest 12 passing.
  - **Reuse:** Playwright, FastAPI. **Docs:** LOCAL_DEMO.md. **Evidence:** Commit 1786d0f.
- [ ] **M0-04: Lock dependencies and SBOM** — P0; status **Planned**.
  - **Dependencies:** Chosen versions. **Tasks:** Generate lock + transitive license file.
  - **Acceptance:** Clean deterministic install. **Tests:** Cold install and license scanner.
  - **Reuse:** pip/uv. **Docs:** REUSE_FIRST.md. **Evidence:** No lockfile yet.
- [ ] **M0-05: Threat model and network worker isolation** — P0; status **Blocked for public capture**.
  - **Dependencies:** Capture design. **Tasks:** Nonroot, no secrets, egress deny.
  - **Acceptance:** Private ranges unreachable. **Tests:** SSRF/redirect/rebinding tests.
  - **Reuse:** OS sandbox. **Docs:** SECURITY_PRIVACY.md. **Evidence:** Only loopback guard tested.
- [ ] **M0-06: CI and test harness** — P0; status **Planned**.
  - **Dependencies:** Locked Chromium/Python. **Tasks:** Run unit/integration/security/UI tests on PR.
  - **Acceptance:** Green reproducible workflow. **Tests:** GitHub Actions run.
  - **Reuse:** pytest/Playwright. **Docs:** QUALITY_AND_BENCHMARKS.md. **Evidence:** No CI yet.
- [ ] **M0-07: Database migrations** — P0; status **Partial**.
  - **Dependencies:** Schema approval. **Tasks:** Versioned SQLite migration/restart recovery.
  - **Acceptance:** Upgrade preserves stored snapshots. **Tests:** Migration/restart tests.
  - **Reuse:** SQLite. **Docs:** DATA_MODEL.md. **Evidence:** CREATE TABLE in app only.
- [ ] **M0-08: Project/license/contributor terms** — P0; status **Blocked**.
  - **Dependencies:** Maintainer approval. **Tasks:** Choose root license and contribution agreement.
  - **Acceptance:** Signed-off public terms. **Tests:** Manual legal check.
  - **Reuse:** None. **Docs:** CONTRIBUTING.md. **Evidence:** No root LICENSE.

## Milestone 1 — Working website time machine

- [x] **M1-01: Capture URL submission** — P0; status **Verified fixture**.
  - **Dependencies:** Fixture guard. **Tasks:** Validate URL, create job.
  - **Acceptance:** Allowed fixture accepted, unsafe URL rejected. **Tests:** 9 rejection cases + API test.
  - **Reuse:** FastAPI. **Docs:** LOCAL_DEMO.md. **Evidence:** pytest pass.
- [x] **M1-02: Capture job progress** — P0; status **Verified fixture**.
  - **Dependencies:** SQLite + executor. **Tasks:** Queued/running/ready/failed.
  - **Acceptance:** Job polled to completed. **Tests:** Integration status test.
  - **Reuse:** ThreadPoolExecutor. **Docs:** app.py. **Evidence:** pytest pass; restart untested.
- [x] **M1-03: Screenshot + HTML metadata** — P0; status **Verified fixture**.
  - **Dependencies:** Offline Chromium. **Tasks:** Render and hash/store files.
  - **Acceptance:** PNG and timestamp persisted. **Tests:** Capture/persistence test.
  - **Reuse:** Playwright. **Docs:** LOCAL_DEMO.md. **Evidence:** pytest pass.
- [ ] **M1-04: Historical dates and list** — P0; status **Partial UI**.
  - **Dependencies:** Snapshot metadata. **Tasks:** List sorted captures, filter by date.
  - **Acceptance:** Date selector and snapshot IDs work. **Tests:** API test; UI e2e pending.
  - **Reuse:** SQLite/DOM. **Docs:** app.py. **Evidence:** API passed; UI not browser tested.
- [ ] **M1-05: Compare two versions** — P0; status **Partial UI**.
  - **Dependencies:** Two screenshots. **Tasks:** Left/right panels.
  - **Acceptance:** Two selected PNGs display. **Tests:** Playwright UI test needed.
  - **Reuse:** DOM + screenshots. **Docs:** app.py. **Evidence:** Source/UI exists, unverified interaction.
- [x] **M1-06: Export + reimport snapshot** — P0; status **Verified fixture**.
  - **Dependencies:** Hashed object store. **Tasks:** Manifest, ZIP and checked reimport.
  - **Acceptance:** Round-trip makes valid second snapshot. **Tests:** Positive + corrupted ZIP test.
  - **Reuse:** zipfile. **Docs:** app.py. **Evidence:** pytest pass.
- [ ] **M1-07: Permitted real public URL captures** — P0; status **Blocked**.
  - **Dependencies:** M0-05 egress isolation. **Tasks:** DNS+redirect+network containment.
  - **Acceptance:** External permitted site works, private blocked. **Tests:** SSRF and isolation test.
  - **Reuse:** ArchiveBox/Playwright. **Docs:** SECURITY_PRIVACY.md. **Evidence:** Not implemented.
- [ ] **M1-08: Full browser user journey E2E** — P0; status **Planned**.
  - **Dependencies:** CI/browser. **Tasks:** Visit, submit, wait, date, compare, export/import.
  - **Acceptance:** End-to-end headless browser works. **Tests:** Playwright UI suite.
  - **Reuse:** Playwright. **Docs:** QUALITY_AND_BENCHMARKS.md. **Evidence:** Not run.

## Milestone 2 — Advanced archival preservation

- [ ] **M2-01: Standards-based WARC capture** — P1; status **Planned**.
  - **Dependencies:** Safe capture worker. **Tasks:** Record HTTP transactions.
  - **Acceptance:** Warcio parses expected responses. **Tests:** WARC fixture tests.
  - **Reuse:** ArchiveBox/Warcio. **Docs:** ADR-001. **Evidence:** Not implemented.
- [ ] **M2-02: WACZ packaging and integrity** — P1; status **Planned**.
  - **Dependencies:** M2-01. **Tasks:** Index/manifest resource hashes.
  - **Acceptance:** Archive opens in independent viewer. **Tests:** WACZ cross-tool tests.
  - **Reuse:** WACZ library. **Docs:** ARCHITECTURE.md. **Evidence:** Not implemented.
- [ ] **M2-03: Isolated historical replay** — P1; status **Blocked**.
  - **Dependencies:** M2-01, M0-05. **Tasks:** Evaluate SolrWayback indexing.
  - **Acceptance:** Safe offline WARC replay. **Tests:** Replay and origin isolation tests.
  - **Reuse:** SolrWayback. **Docs:** TOP_TWO_REPOSITORIES.md. **Evidence:** No interop test.
- [ ] **M2-04: Missing-resource/fidelity report** — P1; status **Planned**.
  - **Dependencies:** M2-03. **Tasks:** Detect absent resources.
  - **Acceptance:** Clearly list missing URLs. **Tests:** Purposely incomplete WARC fixture.
  - **Reuse:** Archive metadata. **Docs:** QUALITY_AND_BENCHMARKS.md. **Evidence:** Not implemented.
- [ ] **M2-05: Interoperability import/export** — P1; status **Planned**.
  - **Dependencies:** M2-02. **Tasks:** Validate standard archive imports.
  - **Acceptance:** Round trip with external viewer. **Tests:** WARC/WACZ conformance.
  - **Reuse:** Warcio. **Docs:** ARCHITECTURE.md. **Evidence:** Not implemented.

## Milestone 3 — Monitoring and search

- [ ] **M3-01: Scheduled captures** — P2; status **Planned**.
  - **Dependencies:** Safe queue, M1-07. **Tasks:** Cron, dedupe, retries.
  - **Acceptance:** No duplicate jobs; bounded crawl. **Tests:** Fake clock/retry tests.
  - **Reuse:** changedetection.io optional. **Docs:** REUSE_FIRST.md. **Evidence:** Not implemented.
- [ ] **M3-02: Computed text/visual diffs** — P2; status **Planned**.
  - **Dependencies:** Two captures. **Tasks:** Image/text algorithms and ignore regions.
  - **Acceptance:** Golden cases match. **Tests:** Golden screenshot/text tests.
  - **Reuse:** Open image diff libs. **Docs:** QUALITY_AND_BENCHMARKS.md. **Evidence:** Side-by-side only.
- [ ] **M3-03: Opt-in alerts** — P2; status **Planned**.
  - **Dependencies:** M3-02. **Tasks:** Rate-limited notifications.
  - **Acceptance:** No duplicate alert. **Tests:** Mock sender test.
  - **Reuse:** Existing alert service. **Docs:** PRODUCT_VISION.md. **Evidence:** Not implemented.
- [ ] **M3-04: Full-text search and filters** — P2; status **Planned**.
  - **Dependencies:** SQLite metadata. **Tasks:** Index content and permissions.
  - **Acceptance:** Known documents found. **Tests:** Precision/tenant tests.
  - **Reuse:** SQLite FTS then Solr. **Docs:** DATA_MODEL.md. **Evidence:** Date filter only.

## Milestone 4 — Browser extension

- [ ] **M4-01: Manual click to capture** — P2; status **Blocked**.
  - **Dependencies:** Legacy source audit. **Tasks:** Review/import MV3 prototype.
  - **Acceptance:** Minimal permissions and working capture. **Tests:** Extension E2E tests.
  - **Reuse:** Browser APIs. **Docs:** LEGACY_PROTOTYPE_README.md. **Evidence:** Source not in repo.
- [ ] **M4-02: Private storage and consent sync** — P2; status **Planned**.
  - **Dependencies:** M4-01, auth. **Tasks:** Explicit grants, deletion, sync.
  - **Acceptance:** Private by default. **Tests:** Leak/cookie tests.
  - **Reuse:** Browser storage. **Docs:** SECURITY_PRIVACY.md. **Evidence:** Not implemented.
- [ ] **M4-03: Browser/version compatibility** — P2; status **Planned**.
  - **Dependencies:** M4-01. **Tasks:** Chrome/Edge fixture regression.
  - **Acceptance:** Pass test matrix. **Tests:** Automated extension tests.
  - **Reuse:** Playwright/browser APIs. **Docs:** QUALITY_AND_BENCHMARKS.md. **Evidence:** Not implemented.

## Milestone 5 — AI website history

- [ ] **M5-01: Dated AI interface snapshots** — P2; status **Planned**.
  - **Dependencies:** Safe capture. **Tasks:** Snapshot model/catalog.
  - **Acceptance:** Historical labeling + timestamps. **Tests:** Static controlled fixtures.
  - **Reuse:** Capture engine. **Docs:** AI_PRESERVATION.md. **Evidence:** Not implemented.
- [ ] **M5-02: Historical model availability catalog** — P2; status **Planned**.
  - **Dependencies:** Official primary sources. **Tasks:** IDs, release/deprecation status.
  - **Acceptance:** Source and verified date stored. **Tests:** Catalog schema tests.
  - **Reuse:** Provider public docs. **Docs:** AI_PRESERVATION.md. **Evidence:** Not implemented.
- [ ] **M5-03: Authorized chat export import** — P2; status **Planned**.
  - **Dependencies:** Privacy+auth. **Tasks:** Validate exports, encrypt/private defaults.
  - **Acceptance:** No unauthorized imports. **Tests:** Synthetic exporter fixtures.
  - **Reuse:** Chat export research. **Docs:** AI_PRESERVATION.md. **Evidence:** Not implemented.
- [ ] **M5-04: Historical AI UI comparison** — P2; status **Planned**.
  - **Dependencies:** M5-01, M3-02. **Tasks:** Timeline differences.
  - **Acceptance:** Clear difference from actual inference. **Tests:** UI snapshot tests.
  - **Reuse:** Version compare. **Docs:** AI_PRESERVATION.md. **Evidence:** Not implemented.

## Milestone 6 — Production platform

- [ ] **M6-01: Identity + authorization + tenant isolation** — P0 before launch; status **Blocked**.
  - **Dependencies:** Maintainer security decision. **Tasks:** OIDC, RBAC and explicit sharing.
  - **Acceptance:** No cross-tenant access. **Tests:** Negative authorization tests.
  - **Reuse:** Established auth provider. **Docs:** SECURITY_PRIVACY.md. **Evidence:** Not implemented.
- [ ] **M6-02: Backups + restore + retention** — P1; status **Planned**.
  - **Dependencies:** Schema. **Tasks:** Encrypted backups, restore drill.
  - **Acceptance:** Restore identical hashes. **Tests:** Disaster recovery drill.
  - **Reuse:** Standard backup tools. **Docs:** DATA_MODEL.md. **Evidence:** Per-snapshot ZIP only.
- [ ] **M6-03: Object storage + observability** — P1; status **Planned**.
  - **Dependencies:** Measured scale. **Tasks:** Optional S3, logs, metrics.
  - **Acceptance:** Outage/quotas measured. **Tests:** Failure injections.
  - **Reuse:** S3, telemetry. **Docs:** ARCHITECTURE.md. **Evidence:** Not implemented.
- [ ] **M6-04: Rate limits/abuse response** — P0 before launch; status **Blocked**.
  - **Dependencies:** Egress isolation. **Tasks:** Quotas, timeouts, takedowns.
  - **Acceptance:** Security review signed off. **Tests:** Threat suite and pen test.
  - **Reuse:** OS gateway. **Docs:** SECURITY_PRIVACY.md. **Evidence:** Not implemented.
- [ ] **M6-05: Production deployment and capacity** — P2; status **Blocked**.
  - **Dependencies:** M6-01..04. **Tasks:** Hardened container and CI.
  - **Acceptance:** Reproducible secure staging. **Tests:** Load + restore tests.
  - **Reuse:** Docker. **Docs:** DEVELOPER_HANDOFF.md. **Evidence:** Not implemented.

## Milestone 7 — Competitive improvements

- [ ] **M7-01: Dynamic-page high-fidelity capture** — P2; status **Planned**.
  - **Dependencies:** WARC + safe worker. **Tasks:** SPA and network capture QA.
  - **Acceptance:** Measure on consented 30 fixtures. **Tests:** Fidelity benchmark.
  - **Reuse:** Browsertrix for research. **Docs:** QUALITY_AND_BENCHMARKS.md. **Evidence:** Not measured.
- [ ] **M7-02: Better search and visual diff** — P2; status **Planned**.
  - **Dependencies:** M2/M3. **Tasks:** Fast indexes, relevant results.
  - **Acceptance:** Quality/cost gains demonstrated. **Tests:** Benchmarks.
  - **Reuse:** SolrWayback, SQLite. **Docs:** COMPETITOR_FEATURE_GAPS.md. **Evidence:** Not implemented.
- [ ] **M7-03: Bulk capture + collaboration + API/self-host** — P3; status **Planned**.
  - **Dependencies:** Multi-user platform. **Tasks:** Permissioned collections and stable API.
  - **Acceptance:** Safe bulk jobs and client contracts. **Tests:** E2E/contract/load tests.
  - **Reuse:** ArchiveBox adapter. **Docs:** ARCHITECTURE.md. **Evidence:** Not implemented.
- [ ] **M7-04: Public collections and moderation** — P3; status **Blocked**.
  - **Dependencies:** Legal/privacy signoff. **Tasks:** Takedown workflow + rights review.
  - **Acceptance:** Approved publication and removal. **Tests:** Moderation/redaction tests.
  - **Reuse:** None. **Docs:** SECURITY_PRIVACY.md. **Evidence:** Not implemented.

## Completion and security policy

Always attach exact commit/test logs, dependency and license inventory, and reproduction steps before checking off a feature. Never claim that saving a ChatGPT/Gemini/Claude frontend resurrects a retired proprietary AI model. No public URL capture until OS-level egress isolation and SSRF threat suite pass. Benchmark only owned or explicitly permissioned sites. This list is a living plan, not a claim of release readiness.
