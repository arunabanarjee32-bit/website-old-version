# Competitor feature gaps (public documentation reviewed 2026-11-15)

This is a **product strategy hypothesis**, not a claim of market leadership, pricing equivalence, product parity, or measured competitor weaknesses.

| Product | Core strengths | Audience / model | Export and replay notes | VersionVault opportunity |
| --- | --- | --- | --- | --- |
| Wayback Machine https://web.archive.org | huge public crawl history, URL/time navigation, Save Page Now | public preservation/research | Save Page Now is a single-page capture, subject to exclusions; captures can lack resources | private history + modern visual diff + transparent fidelity grades |
| Archive-It https://archive-it.org | scoped institutional collections, crawl schedules, metadata, full-text search | paid institutions | archive management and Wayback-based browsing; downloadable partner WARC data | simpler entry for individuals/developers, local self-host option |
| ArchiveBox https://archivebox.io | self-hosted multi-format extraction and archives, CLI/admin | self-hosters | captures many formats; replay fidelity depends on method/external tools | polished date/version navigation, fidelity reporting and private sync |
| Browsertrix / Webrecorder https://webrecorder.net | browser crawling, QA, WACZ, collaboration, ReplayWeb integration | professional archive operators | replay WACZ; modern dynamic capture options; usage/ops complexity | approachable individual UX + integrated comparisons |
| changedetection.io https://changedetection.io | monitoring schedules, text/visual changes and alerts | site monitors | not intended as full WARC historian | change alerts *plus* preserved version evidence |
| ReplayWeb.page https://replayweb.page | browser/PWA offline WACZ/WARC playback and archive browsing | local archive users | local files not uploaded when opened through PWA | native personal version timeline, capture and privacy flow |
| OldWeb.today https://oldweb.today | legacy browser emulation and historical experience | web historians/nostalgia | depends on accessible historical content and emulated browsers | modern responsive interface, history search and own captures |

## Prioritized feature-gap matrix

| Feature | Phase | Current VersionVault status (after local MVP work) | Competitor context / requirement |
| --- | --- | --- | --- |
| Save screenshot of a controlled site | Essential MVP | local fixture demo implemented/tested | baseline not competitor parity |
| URL history, timestamp, side-by-side view | Essential MVP | local fixture demo implemented/tested | key usability foundation |
| Export/import with hashes | Essential MVP | local demo ZIP tested; not WARC | interoperability baseline |
| General public URL capture | Essential MVP **security-gated** | **blocked** pending egress-isolated worker | no arbitrary public fetch in dev |
| Durable WARC/WACZ | Competitive next | planned | format and replay interoperability |
| Secure isolated historical replay | Competitive next | planned | SolrWayback or licensed alternative |
| Visual/text diff, search, alerting | Competitive next | only screenshot side-by-side demo | compare change monitoring leaders |
| Better JS-heavy fidelity / QA | Strategic differentiator | planned | Browsertrix shows useful QA design |
| Private local-first AI product history | Strategic differentiator | planned | imported exports are not original model inference |
| Team collaboration, RBAC, retention | Advanced future | planned | Archive-It/Browsertrix institutional use cases |
| Large-scale crawling & global public collections | Advanced future | planned, unfunded | cannot match Wayback scale immediately |
| Continue original retired proprietary AI backend | Not currently feasible | not achievable by UI capture | requires provider access or lawful original model weights |

## Competitor documentation used

- https://archivesupport.zendesk.com/hc/en-us/articles/360001513491-Save-Pages-in-the-Wayback-Machine
- https://support.archive-it.org/hc/en-us/articles/209783963-What-s-the-difference-between-the-General-Archive-and-Archive-It
- https://support.archive-it.org/hc/en-us/articles/208002236-How-to-access-web-archives-from-inside-your-Archive-It-account
- https://docs.archivebox.io/latest/ArchiveBox-Architecture-Diagrams.html
- https://crawler.docs.browsertrix.com/
- https://docs.browsertrix.com/user-guide/concepts/
- https://replayweb.page/docs/user-guide/
- https://github.com/oldweb-today/oldweb-today

Next action: define an owned/permissioned 30-site benchmark before publishing comparative claims.
