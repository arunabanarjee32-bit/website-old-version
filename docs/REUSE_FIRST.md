# Reuse-first engineering and Codex credit budget

## Policy

Before Codex writes a subsystem, verify a maintained third-party solution does not already solve it. **Integrate -> configure -> add adapters -> extend -> build last.** Reuse is not automatically free: check license, deployment, upgrades, security, APIs, costs and long-term maintenance.

## Decision table

| Need | First candidate | Backup / research | Early decision |
| --- | --- | --- | --- |
| Basic capture workflow | ArchiveBox external CLI/service | custom Playwright pipeline | benchmark both; choose ONE |
| JavaScript screenshots | Playwright | browser extension tab capture | adopt Playwright for server jobs |
| WARC read/write | Warcio | native WARC helpers | adopt library, not custom parser |
| High-fidelity dynamic crawling | Browsertrix Crawler | ArchiveWeb.page | research; AGPL review |
| Historical replay | SolrWayback | pywb, ReplayWeb.page | research/license gate |
| Scheduled changes | built-in minimal schedule | changedetection.io | defer external service until real demand |
| Background queue | Celery | simpler queue / in-process for local | only after jobs justify it |
| Search | database indexing | Meilisearch, Solr | defer dedicated engine until measured |
| Identity | established auth library/OIDC | Keycloak | no homegrown password service |
| Object storage | filesystem | S3/SeaweedFS | local first |
| Large-scale crawl | Heritrix | Browsertrix stack | much later |
| Static single-page saving | SingleFile | custom HTML packer | study its behavior, AGPL gate |
| AI chat UX/export | LibreChat, other exporters | original importer | import only owned data with permission |

## Candidate gates

For any dependency record: canonical URL, primary use case, exact version/commit, **license at that version including transitive dependencies**, maintenance/last release, reproducible build, upstream support, integration method, security isolation, API stability, failure recovery, removal strategy, performance comparison, and fallback.

### Copyleft warning

ArchiveWeb.page, ReplayWeb.page, Browsertrix and SingleFile have AGPL license obligations; pywb uses GPL. Do not copy their code into a presumed proprietary app without deliberate legal review. Running as a separate service does **not automatically** remove AGPL obligations—review the exact form of deployment and modifications. Licenses listed in the study TXT file reflect repository metadata as of Nov 15, 2026, not a legal determination.

## Codex savings discipline

- Start tasks with audit of current code and public tools.
- One bounded issue/PR at a time.
- Do not create a new backend framework, queue, auth system, parser, crawler or search engine merely for practice.
- Require a reproducible benchmark before replacing a working dependency.
- Preserve existing implementation until replacement passes equal or stronger tests.
- Pin dependencies/lockfiles; maintain a software bill of materials (SBOM).
- Maintain small docs and tests alongside each change.

Full list of suggested repositories: [THIRD_PARTY_REPOS_TO_STUDY.txt](../THIRD_PARTY_REPOS_TO_STUDY.txt).
