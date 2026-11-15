# Exactly two primary repositories — architecture study selection

**Decision date:** 2026-11-15. Exactly TWO substantial systems selected for primary engineering evaluation, **not automatic embedding**. Playwright and Warcio are supporting libraries, not additional primary platforms.

## Primary Repository 1: ArchiveBox
**GitHub:** https://github.com/ArchiveBox/ArchiveBox
**Latest published release checked:** v0.9.77 (2026-10-27)
**Inspected source pin:** dev @ 7efbb5184882a06e0b9a8975a1f8b027b171fd92 (dev pyproject identifies 0.9.78rc215; pin release tag separately before deploying)
**Verified license:** MIT in repository LICENSE at inspected dev source; retain notices and audit dependency chain.

**Why:** Already offers URL ingestion, extraction methods, crawl/snapshot lifecycle, CLI, Django UI, REST endpoints, scheduling, multi-format outputs, tests and Docker workflow. Reimplementing that entire orchestration layer is poor use of Codex credits.

**Source modules to inspect:** archivebox/cli/archivebox_add.py, archivebox/services/runner.py, archivebox/crawls/models.py, archivebox/core/models.py, archivebox/api/v1_crawls.py, archivebox/plugins and abx plugin packages, pyproject.toml, Dockerfile, docker-compose.yml, tests/workflows.

**What VersionVault can reuse (after benchmark):** container/CLI as external capture adapter, captured artifacts, crawler outcomes, metadata and job status. Adapt by importing verified outputs, not by coupling our database to ArchiveBox's internal Django model tables.

**What not to reuse directly:** third-party admin UI/branding, customer accounts without a product-specific auth review, all default plugins, cookies/session capture, Archive.org submission defaults, unverified background scheduler, unneeded dependencies.

**Evaluate locally:** in a disposable, no-external-egress environment, install stable v0.9.77 following its pinned release instructions; disable external submissions and all unnecessary collectors; capture a permissioned controlled fixture, inspect output manifest/hash and API/CLI results. Capture workers must not have access to host secrets. Do not run arbitrary internet crawls.

**Engineering savings:** qualitative HIGH for orchestration and capture formats; not quantified by hours. Limitations: heavyweight Python/Django/abx + Chromium dependencies, changing plugin interfaces, resource use, complex deployment. Security: SSRF, authenticated content leakage, command/extractor subprocess isolation, outbound archive publishing. **Replacement strategy:** implement VersionVault CaptureAdapter contract and immutable archive object interface so Playwright-only, Browsertrix (if licensed), or future native workers can replace it.

## Primary Repository 2: SolrWayback
**GitHub:** https://github.com/netarchivesuite/solrwayback
**Latest published release checked:** 5.5.0 (2026-09-15)
**Inspected source pin:** master @ a34be4593a8f13df89e43300c7a8d60f8564bb68; pom.xml says 5.5.1-SNAPSHOT
**Verified license:** Apache-2.0 from LICENSE.txt; audit bundled WARC indexer and transitive dependencies separately.

**Why:** Existing full-text archive search, WARC indexing integration, Wayback-style historical replay, visualizations and archive export. It is complementary to capture, not a second capture engine.

**Source modules to inspect:** src/main/java/.../parsers/WarcParser.java, src/bundle/indexing/warc-indexer.sh, src/bundle/solr_config/conf/schema.xml, src/main/webapp/api.jsp, pom.xml, src/test and official 5.5.0 bundled deployment.

**What VersionVault can reuse (after benchmark):** separate indexing-and-replay service for standards-based WARC captures, possibly link-based search/query API and export. Its Solr index is derived data; WARC objects in VersionVault remain the immutable source of truth.

**What not to reuse directly:** its public-facing UI as our sole frontend, legacy/default Dockerfile (still points at 5.1.2), user account/session assumptions, Solr as VersionVault's primary metadata DB.

**Evaluate locally:** use the released 5.5.0 bundle and a small, lawful WARC fixture, run warc-indexer into an isolated Solr instance, then request a historical URL through its documented frontend service. Verify no external resource fallback or application-origin scripting. Do NOT enable this service for untrusted public users without replay isolation.

**Engineering savings:** qualitative HIGH for WARC indexing/replay/search versus inventing a URL rewriting engine; **not yet measured**. Limitations: Java/Solr/Tomcat footprint, index pipeline and schema coupling, resource pressure, Dockerfile/version drift. Security: replayed JavaScript, SSRF-like URL rewriting, cross-origin leaks, archive/file permission boundaries. **Replacement strategy:** implement SearchReplayAdapter, retain canonical WARC/WACZ, treat Solr index as rebuildable; replace service with compatible replay engine after future legal and performance evidence.

## Complementarity and selection logic

**ArchiveBox produces captured artifacts; SolrWayback indexes and presents standards-based archived resources.** The integration must be proved by a WARC contract and migration test. There is not yet evidence ArchiveBox output can be fed unchanged into the SolrWayback indexer; that compatibility is a milestone-2 gate.

**Neither project was integrated into the 2026-11-15 local demo.** That demo uses Playwright as an ordinary supporting dependency to establish a safe working vertical slice. We deliberately did not provision Docker/Solr or run ArchiveBox in this environment.

**Five alternatives and tradeoffs:**
1. Browsertrix: richer web-archiving operations, but high integration/ops cost and AGPL terms.
2. Browsertrix Crawler: attractive browser capture/WACZ but AGPL and overlapping capture responsibility.
3. ReplayWeb.page: lighter browser-based offline playback than SolrWayback, but AGPL review and origin isolation.
4. pywb: capable replay, but GPL licensing and deployment compatibility need legal analysis.
5. changedetection.io: excellent alerts but doesn't fulfill archival replay/search foundation.
Additional: Playwright and Warcio are essential *libraries*, not comprehensive independently managed archive platforms. Heritrix is too operationally large for earliest release.

## Selection gates — must pass before embedding or publicly deploying

- Stable release binary/container hash and license inventory including transitive components.
- Benchmarked controlled WARC interchange (capture->index->offline replay), with resource completeness and failure cases.
- Confirm storage authorization, no resource leaks, no external fallback in replay and full egress isolation in capture.
- Run CPU/memory tests on modest hardware, determine support/upgrades and failure-handling.
- Obtain maintainer decision on VersionVault license and external service deployment.

**If these gates fail:** keep the same two repositories as *study selections* but do NOT integrate them. Instead continue with a minimal Playwright+Warcio pipeline and reopen the ADR. No fictitious compatibility claims.
