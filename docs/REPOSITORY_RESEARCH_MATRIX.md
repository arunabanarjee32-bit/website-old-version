# Repository research matrix — evidence collected 2026-11-15

## Research scope and method

All 22 repos from THIRD_PARTY_REPOS_TO_STUDY.txt were inspected using GitHub repository metadata and complete recursive source-tree listings. For the ten most relevant tools, specific source modules and official documentation were examined; selected licenses and build manifests were fetched. The latest non-prerelease GitHub release endpoint was queried for all 22. An absent release below means **no latest published release returned**, not necessarily no tags. Last-push dates are GitHub metadata and **do not prove reliability or security**. All versions below are research reference points, not dependency pins in the VersionVault app.

No upstream service was installed, no upstream performance benchmark was executed, and no transitive dependency SBOM was completed. Deployment/CPU/RAM descriptions are **qualitative engineering estimates**, unless an official requirement is stated. GitHub license API metadata is not sufficient where stated; exact HEAD license file was inspected for the two selected projects and several flagged alternatives.

**Weighted screening heuristic (subjective, not empirical performance measurements):**
0–5 on requirement alignment (25%), capture/preservation (20%), integration (15%), license/security compatibility (15%), extensibility (10%), maintenance (10%), and runtime efficiency (5%). Multiply by weights, divide by 5. A legal/security blocker VETOES integration regardless of score. Libraries may score well technically but are not eligible as a *primary system* if they do not independently solve a major subsystem. Score uncertainty approximately ±10 points. Do NOT treat differences of a few points as demonstrated.

## All 22 audited candidates

| # | Repository (GitHub) | Language / latest release / last pushed (UTC) | Evidence in source tree | License / integration and primary role | Screening score |
|---|---|---|---|---|---:|
| 1 | [ArchiveBox](https://github.com/ArchiveBox/ArchiveBox) | Python; v0.9.77; 2026-11-15 | archivebox/services/runner.py, crawls/models.py, core/models.py, api/v1_crawls.py, cli/archivebox_add.py, pyproject.toml, tests | MIT in LICENSE; CLI/API/separate service; **primary candidate** capture/orchestration; heavy Django/plugin dependency chain | **89** |
| 2 | [Playwright](https://github.com/microsoft/playwright) | TypeScript; v1.65.1; 2026-11-14 | packages/playwright-core, packages/playwright, tests, browser_patches | Apache-2.0 metadata; **supporting library**, browser control/screenshots/tests; not standalone archivist | 77 |
| 3 | [Warcio](https://github.com/webrecorder/warcio) | Python; v1.8.2; 2026-10-28 | warcio/archiveiterator.py, warcio/warcwriter.py, test/test_writer.py, test/test_archiveiterator.py | Apache-2.0 metadata; **supporting library** for WARC IO, not capture UI/replay | 74 |
| 4 | [ArchiveWeb.page](https://github.com/webrecorder/archiveweb.page) | TypeScript; v0.17.1; 2026-11-09 | src/ext/bg.ts, src/ext/browser-recorder.ts, src/electron, package.json | AGPL-3.0; high fidelity extension capture, **license gate** | 69 |
| 5 | [ReplayWeb.page](https://github.com/webrecorder/replayweb.page) | TypeScript; v2.5.4; 2026-11-14 | src/replay.ts, build, embedding assets, tests/embed | AGPL-3.0; WACZ/WARC playback via service worker, **license gate** | 77 |
| 6 | [Browsertrix](https://github.com/webrecorder/browsertrix) | TypeScript+Python; v1.26.6; 2026-11-14 | backend/pyproject.toml, backend/test, frontend, chart, btrix | AGPL-3.0; managed high-fidelity platform, Kubernetes/ops burden, **license gate** | 75 |
| 7 | [Browsertrix Crawler](https://github.com/webrecorder/browsertrix-crawler) | TypeScript; v1.15.4; 2026-11-14 | src/crawler.ts, util/recorder.ts, warcwriter.ts, wacz.ts, tests | AGPL-3.0; Docker Puppeteer capture/WACZ; **license gate**, inspect separate-service terms | 74 |
| 8 | [SolrWayback](https://github.com/netarchivesuite/solrwayback) | Java+JS; 5.5.0; 2026-11-10 | src/main/.../parsers/WarcParser.java, src/bundle/indexing/warc-indexer.sh, solr_config/conf/schema.xml, pom.xml, src/test | Apache-2.0 in LICENSE.txt; **primary candidate** archival index/search/replay; requires Solr, warc-indexer and servlet host | **82** |
| 9 | [pywb](https://github.com/webrecorder/pywb) | Python; v-2.11.1; 2026-11-14 | pywb/rewrite, pywb/indexer, pywb/recorder, tests | GPL-3.0 in LICENSE; replay/URL rewriting; licensing/distribution gate | 74 |
| 10 | [Heritrix3](https://github.com/internetarchive/heritrix3) | Java; 3.18.0; 2026-11-14 | engine, modules, commons, docker, pom.xml | LICENSE text states Apache-2.0 (GitHub NOASSERTION); robust large crawls but excessive MVP operations | 73 |
| 11 | [SingleFile](https://github.com/gildas-lormeau/SingleFile) | JavaScript; v1.37.0; 2026-11-13 | src/core/content, src/core/bg, manifest.json, tests | AGPL-3.0; browser save-as-HTML, **license gate**, not full interactive replay | 64 |
| 12 | [OldWeb.today](https://github.com/oldweb-today/oldweb-today) | JavaScript; no latest release returned; 2024-10-31 | src/main.js, site, extra | AGPL-3.0; browser emulation inspiration, not core new-site capture | 50 |
| 13 | [changedetection.io](https://github.com/dgtlmoon/changedetection.io) | Python; 0.70.3; 2026-11-15 | changedetection.py, changedetectionio/tests/fetchers, plugin examples, Dockerfile | Apache-2.0; separate monitoring service/alerts, not WARC replay; add when justified | 72 |
| 14 | [Celery](https://github.com/celery/celery) | Python; v5.7.0; 2026-11-11 | celery/app/task.py, celery/app/base.py, tests | **BSD-3-Clause in LICENSE** (GitHub NOASSERTION); background queue, needs broker; defer | 61 |
| 15 | [Meilisearch](https://github.com/meilisearch/meilisearch) | Rust; v1.56.2; 2026-11-12 | crates, Cargo.toml, LICENSE, LICENSE-MIT, LICENSE-EE | **Mixed MIT + BUSL-1.1**, not blanket MIT; edition/feature commercial review; defer dedicated search | 57 |
| 16 | [Keycloak](https://github.com/keycloak/keycloak) | Java; 26.8.2; 2026-11-15 | services, authz, adapters, pom.xml | Apache-2.0; mature identity **separate service**, too heavy for local MVP | 55 |
| 17 | [SeaweedFS](https://github.com/seaweedfs/seaweedfs) | Go; 4.53; 2026-11-15 | weed, cmd, docker, k8s, go.mod | Apache-2.0; object/S3 store, distributed ops unnecessary for MVP | 45 |
| 18 | [LibreChat](https://github.com/LibreChat-AI/LibreChat) | TypeScript; no latest release returned; 2026-11-15 | api/app/clients, client, packages, Dockerfile | MIT in LICENSE; AI chat frontend/backend reference; does NOT preserve retired provider models | 54 |
| 19 | [Gemini Vault Exporter](https://github.com/crytomato529/gemini-vault-exporter) | JavaScript; v0.4.1; 2026-07-24 | content.js, background.js, manifest.json, options.js | **All rights reserved in LICENSE**, NOT generally reusable code; study behavior only | 35 |
| 20 | [Live Archiver](https://github.com/hexnod/live-archiver) | JavaScript; v1.2.10; 2026-11-05 | background.js, content, panel, manifest.json | Apache-2.0 metadata; small chat archive extension, not full web historian | 48 |
| 21 | [ChatGPT Archive Tools](https://github.com/jamesmoore/chatgpt-archive-tools) | C#+TypeScript; v0.0.40; 2026-10-13 | ChatGpt.Archive.Api, ChatGpt.Exporter.Cli, front-react, tests | MIT metadata; local imported export viewer; auxiliary AI-history reference | 44 |
| 22 | [Awesome Web Archiving](https://github.com/iipc/awesome-web-archiving) | Curated list; no latest release returned; 2026-11-06 | README.md, deprecated.md, CONTRIBUTING.md | CC0-1.0 metadata; reference collection, not runnable subsystem | 33 |

## Deep findings from code and official docs

### ArchiveBox
- Entrypoints: CLI including archivebox/cli/archivebox_add.py; REST/Django Ninja routes via archivebox/api/v1_crawls.py; orchestration archivebox/services/runner.py; Crawl and Snapshot model/queue transitions in archivebox/crawls/models.py and archivebox/core/models.py; tests/workflows and Docker Compose present.
- Current dev pyproject declares version 0.9.78rc215, Python >=3.13, Django >=6.1.3, abx plugin infrastructure and PostgreSQL support. Latest stable GitHub release returned v0.9.77. The checked dev branch is not automatically the stable release.
- Multiple external tools/browser processes; operational memory overhead higher than the minimal local demo. ArchiveBox's own install docs state 1 GB minimum / 2 GB+ recommended (environment-dependent).
- Default Docker Compose example enables Archive.org submission; set ARCHIVEDOTORG_ENABLED=False for privacy-sensitive/local workflows. Do not blindly inherit defaults or cookie capture settings.
- Research pin: 7efbb5184882a06e0b9a8975a1f8b027b171fd92 (dev HEAD observed). MIT license inspected at source LICENSE. Full dependency/license/security audit still pending.

### SolrWayback
- Entrypoints: Java webapp/WAR and frontend REST endpoints; parsed WARC records in parsers/WarcParser.java; Solr schema at src/bundle/solr_config/conf/schema.xml; indexing shell at src/bundle/indexing/warc-indexer.sh calls external warc-indexer JAR.
- Requires **accessible WARC files, compatible Solr index, indexer, and a servlet container**. Cannot simply point it at a screenshot ZIP or SQLite database and obtain replay.
- Source README describes 5.5.0 bundle, full-text and media search, link graphs, export and Wayback-style views. pom.xml at master is 5.5.1-SNAPSHOT; Dockerfile still refers to old 5.1.2 bundle. Validate current recommended bundle deployment rather than trusting stale Dockerfile.
- Indexer script default per-process heap 2048M and notes 20 threads can require ~20 GB memory; this is a **configuration example**, not a measured VersionVault cost.
- Research pin: a34be4593a8f13df89e43300c7a8d60f8564bb68 (master). LICENSE.txt Apache-2.0 verified. warc-indexer/transitive licenses and safe replay deployment need separate audit.

### Playwright and Warcio: important supporting libraries, not primary systems
- Playwright packages/playwright-core and tests supply a tested browser-control layer, not WARC catalog/replay/storage. Current v1.65.1; license metadata Apache-2.0; browser binaries are a runtime dependency.
- Warcio warcio/archiveiterator.py and writer utilities provide WARC streaming and test fixtures. Current v1.8.2; Apache-2.0 metadata. Do not confuse WARC writing with browser-based recording of all JS network interactions.

### Five strongest alternatives considered
- Browsertrix platform: browser-based capture plus scheduling, user management and collections, but AGPL network-copyleft review, Docker/Kubernetes deployments and major scope overlap with our own product.
- Browsertrix Crawler: dedicated Docker high-fidelity WACZ output and QA; stronger dynamic fidelity reference than basic HTML capture, but AGPL and operational browser pressure.
- ReplayWeb.page: portable WACZ/offline replay via service worker; excellent lightweight UX, but AGPL and archived-content isolation require legal/security architecture.
- pywb: Python WARC playback and URL rewriting; excellent mature replay capability, but GPL-3.0 distribution compatibility requires explicit review.
- changedetection.io: useful scheduled monitoring and alerts with Apache-2.0 license, but not a replacement for WARC historical replay.

### Supplemental feasibility notes
- SingleFile preserves some static pages with assets as a single HTML; it is not a reliable backup of dynamic server behavior.
- Heritrix has strong web-scale crawl machinery but does not solve modern browser DOM reconstruction and is costly to operate in an MVP.
- SolrWayback's external warc-indexer must be evaluated in conjunction with storage layout and permissioned benchmark WARC corpus.
- Background queues, search services, external identity and distributed storage are **later choices**; adding them today would raise cost with little MVP benefit.

## Critical research still missing

1. Reproducible upstream Docker/CLI evaluation and comparative capture/replay of real WARC fixtures.
2. Transitive license/SBOM reviews at exact installed versions for ArchiveBox, SolrWayback and warc-indexer.
3. Vulnerability scan, runtime memory/CPU benchmarks and secure deployment validation.
4. Third-party API compatibility tests and WARC/WACZ interchange.
5. Formal maintainer legal approval for product license, public crawling and replay exposure.

**Source pointers:** official repositories linked in the table; also https://docs.archivebox.io/latest/ArchiveBox-Architecture-Diagrams.html , https://crawler.docs.browsertrix.com/ , https://replayweb.page/docs/user-guide/ and https://github.com/netarchivesuite/solrwayback/blob/master/README.md .


## Stable release code recheck (2026-11-15 foundation session)

Exactly **two** primary system repositories remain ArchiveBox and SolrWayback. GitHub release API still returned ArchiveBox `v0.9.77` and SolrWayback `5.5.0`. Actual source at both release tags was rechecked: ArchiveBox `cli/archivebox_add.py`, `api/v1_crawls.py`, `crawls/models.py`, `core/models.py`, `services/runner.py`, `pyproject.toml`, `docker-compose.yml`, MIT `LICENSE`; SolrWayback `parsers/WarcParser.java`, `warc-indexer.sh`, `solr_config/conf/schema.xml`, `pom.xml`, Apache-2.0 `LICENSE.txt`. Notably ArchiveBox's compose example references an unpinned latest image and external Archive.org submission setting, while SolrWayback's indexer defaults to two 2048M Java-heap processes. Treat both as review points, not measured product requirements. See detailed evidence and adapters in [TOP_TWO_REPOSITORIES.md](TOP_TWO_REPOSITORIES.md).

**Actual experiments performed:** GitHub source/release inspection and VersionVault CI fixture tests only. No ArchiveBox binary was installed and no SolrWayback WARC index/replay experiment was run. No new unverified compatibility, capture-success, CPU/RAM, or performance claims are made; 22-repo inventory remains a *screening* record, not approval to combine or distribute any source code.
