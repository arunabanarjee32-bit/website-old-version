> **FOUNDATION PR UPDATE — 2026-11-15 (branch `codex/versionvault-foundation`, NOT merged to `main`):** Pull request [#1](https://github.com/arunabanarjee32-bit/website-old-version/pull/1) proposes GitHub Actions CI, pinned **direct** test dependencies, restart recovery for interrupted jobs, bounded ZIP decompression/metadata validation, PNG chunk checks, and 12 new regression tests. [GitHub Actions run 43739119692](https://github.com/arunabanarjee32-bit/website-old-version/actions/runs/43739119692) at `bbd136235a50d9248d34a7e12f1f5397940f0d74`: **24 passed, 1 warning**, selected Ruff checks and `pip check` passed, Python 3.13 and Playwright-managed Chromium. A full hash-locked dependency graph, SBOM, worker isolation, browser UI E2E, WARC, replay and production readiness remain UNVERIFIED or PLANNED. Earlier direct-system-Chromium CI intermittently timed out; the revised browser installation succeeded. **The status below describes historical main-branch baselines and remains retained for context.**

---

> **STATUS UPDATE — 2026-11-15:** The historical audit below describes the original documentation-only tree. A restricted local fixture **FastAPI + SQLite + Playwright** MVP is now committed (services/api/versionvault/app.py). Local test run: **12 passed**; code commit 1f7a591e7d42ec8399da16c6aea05e6f83c5a954, exact-tested source follow-up 1786d0f997a75be07ccc89404b8248608f3c4244. Features: queued job, allowed local HTML fetch, offline Chromium rendering/screenshot, snapshot dates, two-pane comparison UI, checked ZIP import/export. Chromium direct network navigation was blocked in the research environment. No public URL capture, WARC/WACZ, replay, auth, hosted CI, or deployment. Primary repo study selection: ArchiveBox + SolrWayback (NEITHER INTEGRATED). See [audit](REPOSITORY_AUDIT.md), [checklist](MASTER_IMPLEMENTATION_CHECKLIST.md), [handoff](DEVELOPER_HANDOFF.md). This update supersedes earlier statements that no application code exists.

---

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
