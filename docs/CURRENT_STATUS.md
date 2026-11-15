# Current status and decisions (as of 2026-11-15)

## Confirmed in this GitHub repository

- The repository started with only a 21-byte README: `# website-old-version`.
- This documentation import establishes product goals, contribution guidance, research list, proposed architecture, testing/security baseline and roadmap.
- There is currently **no verified app/build/deployment** in this GitHub tree. Work listed in roadmap remains planned until merged and tested.

## Prior planning artifact (outside repository implementation)

A separate **VersionVault v0.1 local-first Chrome/Edge screenshot extension prototype** and a product-plan Markdown file were generated during the concept stage. They are not proof of a functional server-side archive and are not yet the production architecture. The original prototype's README is mirrored as docs/LEGACY_PROTOTYPE_README.md for historical context. Source import and security review are tracked as an initial task; do not advertise functionality as currently deployed.

## Important open decisions

- Working product name and trademark/domain clearance
- Code distribution license and contribution/ownership terms
- Decide archive architecture (ArchiveBox service versus direct Playwright pipeline)
- Official replay engine and copyleft compliance strategy
- Local-first-only versus hosted multi-user launch sequence
- Authentication/privacy/retention/copyright/takedown policies
- Budget limits and hosting/operating assumptions
- Define competitor benchmark methodology and first user niche

## Immediate next task for a developer/Codex

Do **not** start by building a giant distributed crawler. Produce ADR-001 and a reproducible local demo that captures a site we control, stores an immutable snapshot, and displays it in a dated timeline. Run real tests. See docs/ROADMAP.md.
