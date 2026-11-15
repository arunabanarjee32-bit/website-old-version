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


## Release-tag source verification and integration decision — 2026-11-15

**Primary selections unchanged.** GitHub's latest non-prerelease release API returned **ArchiveBox v0.9.77** (published 2026-10-27) and **SolrWayback 5.5.0** (published 2026-09-15), checked again during foundation work. The prior dev/master references remain historical research pins, not version-locked deployment recipes. License files fetched from the **stable release tags**: ArchiveBox MIT in `LICENSE`; SolrWayback Apache License 2.0 in `LICENSE.txt`. Third-party runtime dependencies, bundled binaries and transitive legal obligations remain unreviewed.

### ArchiveBox 0.9.77 actual source path

- `archivebox/cli/archivebox_add.py`: `_collect_input_urls` calls `validate_url`; `add` accepts depth, URL limit, crawl time/size budgets, selected plugins and background mode, then creates `Crawl` records. This is **not** proof of network-level SSRF isolation.
- `archivebox/api/v1_crawls.py`: Django-Ninja route `POST /crawls` validates input URLs and creates crawl records. Its schemas/routes are vendor-specific and subject to change; an adapter must map to our stable metadata, not reuse vendor IDs as sole identity.
- `archivebox/crawls/models.py`, `archivebox/core/models.py` and `archivebox/services/runner.py`: Django lifecycle models and an event/bus/plugin runner coordinate asynchronous crawl/snapshot work. More capable than VersionVault's one-thread executor but materially more operationally complex.
- `pyproject.toml` at the release tag says version 0.9.77 and imports Django, django-ninja, `abx-dl`, `abx-plugins`, `abxbus` and `abxpkg`. Exact transitive licenses/vulnerabilities still require SBOM assessment.
- `docker-compose.yml` at tag uses `archivebox/archivebox:latest` by default, has `PUBLIC_ADD_VIEW=False` and `ARCHIVEDOTORG_ENABLED=True` example settings. **Never deploy from unpinned latest or inherit external submission defaults for private captures.**
- **Status: EXPERIMENT FURTHER**, as optional external capture CLI/service adapter. Never replace working Playwright capture without actual controlled artifact comparison. Current pipeline captures only fixture HTML+PNG and is retained as fallback.

### SolrWayback 5.5.0 actual source path

- `src/main/java/dk/kb/netarchivesuite/solrwayback/parsers/WarcParser.java` handles WARC headers and compressed/uncompressed record lookup, including source offsets; this assumes compatible indexed WARC record locations, not VersionVault ZIPs.
- `src/bundle/solr_config/conf/schema.xml` defines Solr document fields; SolrWayback's indexed URL, crawl date, source path/offset metadata must map to validated canonical capture records while VersionVault retains original immutable WARC and hashes.
- `src/bundle/indexing/warc-indexer.sh` invokes a separate UKWA `webarchive-discovery` indexer JAR, with default `THREADS=2` and `INDEXER_MEM=2048M` **per indexer process**. Potential Java heap allocation at default concurrency is therefore significant but actual RAM usage was **not measured**.
- `pom.xml` tag shows version 5.5.0 and Java servlet/JAX-RS/Solr dependencies. Release notes require Java 11 or 17 for v5+, with Solr 9 and Tomcat 9 in the supplied bundle. The 5.5.0 release notes explicitly describe a fix for certain JavaScript navigation **live-resource leaks**; treat this as a replay-security regression category, not evidence that every leak is impossible.
- **Status: DEFER the full service in local MVP; EXPERIMENT FURTHER** with an independent, isolated WARC/index/replay experiment. No Solr index, Tomcat service or WARC fixture was executed in foundation PR.

### Proposed replaceable adapter data contract — not implemented

`CaptureResult`: VersionVault capture ID; submitted and normalized URL; UTC timestamp; engine ID/release; artifact descriptors `{kind, sha256, bytes, mime_type, storage_key}`; status/error; extracted resources and known-missing resources; fidelity class `screenshot+HTML` vs validated resource archive; provenance/rights metadata. Importer must verify bytes and hashes before committing snapshot rows. No backend engine is trusted for authorization or canonical ownership.

`SearchReplayAdapter`: `index(verified_warc)`, `lookup(url, timestamp)`, `resource(reference)`. Replays are isolated on an unrelated origin with restricted network and no app cookies, and all misses explicitly report unavailable resources. Solr remains a derived/rebuildable index. Compatibility and API details must be adapted after actual WARC interoperability tests; these are conceptual methods only.

**Interoperability experiment state: BLOCKED (not run).** Need permissioned WARC created and validated with Warcio, safe SolrWayback 5.5.0 bundle and warc-indexer, indexed URL query, timestamp check, asset coverage, missing-resource behavior, live leak isolation, storage/CPU/RAM measurements, transitive license SBOM and rollback. Do not claim `ArchiveBox -> SolrWayback` proven.
