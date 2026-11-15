# Proposed architecture (design, NOT implemented)

## Style

An owner-controlled **monorepo** for original code; clear interfaces to third-party libraries and separate services/containers. A monorepo does not mean a single process and does not mean copy-pasting entire foreign repositories.

```text
Browser extension / Web UI / API clients
                 |
       Public application API
      authz + rate limits + input validation
                 |
         Job queue + scheduler
                 |
  isolated capture workers (egress policy)
    |         |          |
 Playwright   ArchiveBox  alternative crawler (gated)
    |         |          |
      standard snapshot metadata
     screenshots / HTML / WARC/WACZ
          |              |
    object store     PostgreSQL
          |              |
    validation -> indexing/search
          |
      isolated replay origin
          |
    timeline / compare / export
```

## Default proposals, open to ADR

- UI: Next.js + React + TypeScript
- API: Python FastAPI (or TypeScript if proven simpler; decide once)
- Jobs: Celery or similarly mature queue; no queue in tiny local prototype if unnecessary
- Browser rendering: Playwright
- Capture engine: evaluate ArchiveBox as an **independent service** or CLI; do not fork immediately
- Archive formats: Warcio/WARC, evaluate WACZ packagers and validation
- Metadata: SQLite local MVP, PostgreSQL once multi-user/concurrency warrants
- Binary storage: local filesystem with content hashes first, S3-compatible later
- Search: Postgres basic full-text first, Meilisearch/Solr only when benchmarks justify
- Replay: benchmark compatible isolated engines (SolrWayback, pywb, ReplayWeb.page); do not build custom WARC URL-rewriting from scratch prematurely
- Monitoring: simple scheduling first; changedetection.io as a possible service integration
- Identity: no self-invented auth; start with reputable maintained solutions; evaluate Keycloak only when enterprise requirements warrant
- Web-scale crawling: Heritrix later, not in MVP

## Key boundaries

1. **Ingest/crawl boundary:** untrusted URL, network access and content; isolate process, user, time and resources.
2. **Storage boundary:** metadata records must reference immutable content-addressed objects; enforce user ownership.
3. **Replay boundary:** untrusted archived HTML/JS from a dedicated sandboxed origin, strong CSP, no access to authenticated app origin or secrets.
4. **Public/private boundary:** sharing is an explicit user action with redaction, rights checks and removal mechanisms.
5. **AI boundary:** imported transcripts and metadata are not proof of original model execution.

## Capture lifecycle

requested -> validating -> queued -> fetching -> packaging -> integrity_check -> indexed -> ready OR failed.

For each capture retain original URL, normalized URL, timestamp, actor (where appropriate), archive type, recorder/version, source/rights status, content hash, sizes, success/errors, replay warnings and visibility.

## Scale later

One small worker and local storage first. After measurements: PostgreSQL, object storage, worker pools, metrics, isolated queue and private tenant separation. Versioned schema, retention settings, backups and restore drills are required before production.

## Needed ADRs

- ADR-001: ArchiveBox embedded/forked vs external service vs direct Playwright/Warcio
- ADR-002: replay engine legal/technical compatibility
- ADR-003: storage, retention, schema and public/private tenancy
- ADR-004: auth provider and key-management strategy
- ADR-005: license/brand/company IP strategy
- ADR-006: crawl permissions, robots/copyright/takedown policy
