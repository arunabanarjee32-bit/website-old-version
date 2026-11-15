# Architecture decision register

This file records **proposed** decisions; none is approved merely by appearing here.

| ID | Question | Status | Recommended first experiment |
| --- | --- | --- | --- |
| ADR-001 | ArchiveBox external engine vs direct Playwright/Warcio | Pending | compare on 10 permissioned sites |
| ADR-002 | WARC/WACZ replay engine and service isolation | Pending | benchmark SolrWayback/pywb/ReplayWeb.page with license assessment |
| ADR-003 | Local SQLite/file storage vs PostgreSQL/object storage | Pending | MVP local-first then migrate with measurements |
| ADR-004 | Identity provider and multi-tenant isolation | Pending | postpone until multi-user needs |
| ADR-005 | Project license, inbound contributions and rights | Pending | maintainer and legal decision |
| ADR-006 | Crawl, publisher, robots and public takedown policy | Pending | documented compliance policy before launch |
| ADR-007 | Public archive vs private-first product niche | Pending | user interviews and retention data |
| ADR-008 | Scheduling/change detection architecture | Pending | simple scheduler vs changedetection.io integration |
| ADR-009 | AI historical registry data sourcing and imports | Pending | official sources + user-owned export fixtures |

Template for a new ADR: title; context; options considered; evidence/benchmarks; legal/security/license review; decision; reasons; consequences; revisit criteria; date/owner. Store accepted ADRs under docs/adr/ when implementation begins.
