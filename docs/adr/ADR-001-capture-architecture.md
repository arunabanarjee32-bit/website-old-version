# ADR-001: Capture architecture and two-system research baseline

**Date:** 2026-11-15
**Status:** Accepted for research / MVP prototype; production engine integration PROVISIONAL.
**Context:** VersionVault needs URL capture, permanent snapshots, WARC/WACZ compatibility, timelines, search and safe replay without duplicating mature archive systems or accepting incompatible licenses.

## Options

A. Fork ArchiveBox and treat its Django DB as VersionVault's own core.
B. Keep VersionVault's stable metadata/object interfaces; evaluate ArchiveBox as a capture adapter, SolrWayback as later WARC search/replay adapter.
C. Integrate full Browsertrix/Webrecorder platform (AGPL; cluster complexity).
D. Build Playwright+Warcio capture, custom replay from scratch.
E. Add changedetection.io primarily for monitoring rather than replay.

## Decision

Choose **B as target architecture**, with **D's minimal Playwright-only screenshot/HTML capture** temporarily used for the first secure, local-only proof of concept. The **exact two primary repositories for study** are ArchiveBox and SolrWayback. Playwright and Warcio are supporting packages, not further primary repositories. Formal production integration of both primary systems requires license, security, WARC interchange and cost gates.

VersionVault will own canonical snapshot metadata and content-addressed artifacts; capture and replay services must be replaceable. Do not bind new code to ArchiveBox's database schema or serve SolrWayback replay from the trusted UI origin. Local demo content is never executed as archived HTML.

## Evidence inspected

- ArchiveBox dev 7efbb5184882a06e0b9a8975a1f8b027b171fd92: cli/archivebox_add.py, services/runner.py, crawls/models.py, core/models.py, api/v1_crawls.py, pyproject.toml; MIT LICENSE; release v0.9.77.
- SolrWayback master a34be4593a8f13df89e43300c7a8d60f8564bb68: WarcParser.java, warc-indexer.sh, Solr schema, pom.xml and README; Apache-2.0 LICENSE; release 5.5.0. Source README indicates WARC/Solr/indexer and Dockerfile is version-stale.
- AGPL License in Browsertrix/Crawler/ReplayWeb.page; GPL in pywb; see docs/REPOSITORY_RESEARCH_MATRIX.md.
- No ArchiveBox-to-SolrWayback integration benchmarks executed.

## Consequences

+ Existing archival and replay engineering are candidates for reuse, with durable format boundaries.
+ Independent VersionVault metadata, UI and future proprietary rights remain possible subject to notices.
- Additional runtime/tooling and adapter testing needed.
- External processes create operational and supply-chain security responsibilities.
- SolrWayback is **not** an MVP dependency and must not be deployed before WARC interchange proof.
- Current local-only prototype is constrained to a numeric loopback fixture; PUBLIC URL fetching is blocked pending true worker egress isolation.

## Exit/rollback criteria

Accept adapter after version-pinned interoperability and isolated replay demo with measured data. If incompatible, costly, or unsafe, retain ArchiveBox/SolrWayback as references, switch to lawful Playwright+Warcio and an alternative licensed replay service with a new ADR. Never bypass licensing or network safety to make a benchmark pass.

## Benchmark status

Upstream comparative benchmark: **NOT RUN**. Local Playwright-rendered fixture capture, SQLite storage and export/import tests: 12 passed in the sandbox on 2026-11-15. Chromium **direct navigation was blocked by the environment**, so local demo fetches allowlisted HTML via Python and renders it in an offline browser context. This is not a valid measure of real JS-heavy website capture fidelity.
