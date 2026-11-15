> **Update 2026-11-15:** A locally tested fixture-only MVP exists, but the planned *public website* workflow is not complete and remains security-gated. See [MASTER_IMPLEMENTATION_CHECKLIST.md](MASTER_IMPLEMENTATION_CHECKLIST.md) for per-feature verified status. The milestones below are the earlier planning baseline.

---

# Roadmap with milestones, not promises

## Milestone 0 — Responsible foundation (CURRENT PRIORITY)

- [ ] Confirm working product name, ownership, distribution and repository license decision.
- [ ] Audit legacy browser-extension prototype and decide how to import it without misleading claims.
- [ ] Complete license/maintenance/security evaluation of ArchiveBox, Playwright, Warcio, replay candidates.
- [ ] Choose capture architecture in ADR-001.
- [ ] Create reproducible dev environment, CI, issue labels, contributor terms.
- [ ] Draft SSRF + replay threat model and legal/takedown policy.

**Exit:** maintainer accepts a one-page architecture decision, dependency list and first working-slice plan.

## Milestone 1 — Real usable local MVP

- [ ] Submit allowed URL and see a capture job with success/failure.
- [ ] Capture screenshot + supported HTML metadata using Playwright and tested storage.
- [ ] Retrieve a dated snapshot by website/time from a local library.
- [ ] Compare two screenshots and export a backup.
- [ ] Unit, integration, browser and security tests for this vertical slice.
- [ ] Document local run and restore steps with verified output.

**Exit:** new developer can clone and complete capture -> view -> compare -> export offline on a clean machine. No unverifiable claims.

## Milestone 2 — Standards-based web archive

- [ ] Capture/validate WARC or WACZ with integrity metadata.
- [ ] Evaluate SolrWayback, pywb, ReplayWeb.page and Browsertrix licensing/compatibility.
- [ ] Isolated historical playback with clear partial-replay warnings.
- [ ] Replay acceptance fixtures and export/import round-trip tests.

## Milestone 3 — Differentiated product

- [ ] Browser extension integrated with backend under explicit consent.
- [ ] Scheduled public-page capture + change detection and notifications.
- [ ] Search, collections, tags, visual/text diff, retention and audit features.
- [ ] AI history catalog + privacy-preserving conversation export importer.

## Milestone 4 — Multi-user and scale

- [ ] Production-grade identity, tenant isolation, object storage, worker queue.
- [ ] Billing/teams only after demand, support process and legal readiness.
- [ ] Evaluate Heritrix-scale crawling and advanced search if metrics justify it.
- [ ] Public collection workflows only with copyright/privacy/takedown policy.

## Backlog prioritization rule

Prioritize by real user value x replay fidelity x reliability divided by effort, operating cost and legal/security risk. *Do not* integrate a large tool merely because it is open source. Close each phase with measured results, demo and honest limitations.
