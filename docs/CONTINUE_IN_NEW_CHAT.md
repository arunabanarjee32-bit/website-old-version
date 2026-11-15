# Continue VersionVault in a new chat or Codex session

**Use this file when an old conversation is too long or fails to load.**

## Where the knowledge lives

- [**Master continuity archive (complete research, links, five diagrams, decisions, tests, tasks)**](PROJECT_CONTINUITY_MASTER.md)
- [Repository README](../README.md) and [agent instructions](../AGENTS.md)
- [Current status](CURRENT_STATUS.md) and [actual code audit](REPOSITORY_AUDIT.md)
- [Master implementation checklist](MASTER_IMPLEMENTATION_CHECKLIST.md)
- [Developer handoff](DEVELOPER_HANDOFF.md)
- [Exactly two upstream systems](TOP_TWO_REPOSITORIES.md) and [full list of 22](../THIRD_PARTY_REPOS_TO_STUDY.txt)
- [Architecture ADR](adr/ADR-001-capture-architecture.md)
- [Open implementation PR #1](https://github.com/arunabanarjee32-bit/website-old-version/pull/1)

## Paste this into a new chat

> Continue developing my existing VersionVault repository:
> https://github.com/arunabanarjee32-bit/website-old-version
>
> First inspect the latest main commit, feature branches, PRs, CI results and source code. Read docs/PROJECT_CONTINUITY_MASTER.md and docs/MASTER_IMPLEMENTATION_CHECKLIST.md, plus AGENTS.md, docs/DEVELOPER_HANDOFF.md, docs/REPOSITORY_AUDIT.md and docs/TOP_TWO_REPOSITORIES.md. If the master file is still on the docs/versionvault-continuity-archive branch / its documentation PR, read that branch directly. The repository is the durable project memory; do not assume access to my older ChatGPT chats.
>
> The current baseline is a restricted local-only Python/FastAPI, SQLite, Playwright/Chromium fixture MVP. **Never remove the numeric 127.0.0.1:8766 fixture-only capture restriction** until an independently tested, nonroot, network-isolated worker exists. Never serve archived HTML/JS in the trusted app origin. Preserve the existing code and SHA-256 object store.
>
> There are exactly **two primary systems to research**: ArchiveBox for optional capture orchestration, and SolrWayback for future WARC search/replay. Playwright and Warcio are supporting libraries. ArchiveBox-to-SolrWayback compatibility is **NOT tested**.
>
> Check PR #1: it contains reliability/CI improvements and 24 successful tests from its recorded GitHub Actions run, but may still be unmerged. Do not confuse PR work with main. Next priorities: dependency lock + SBOM/license audit, SQLite migrations, crash-safe artifact storage, browser UI E2E, then sandboxed worker and standards-based archiving.
>
> Make one small tested change, on a feature branch; run tests and verify results; update docs, master checklist and continuity archive with precise commit/PR/CI links; do not merge to main without my approval. Be accurate about VERIFIED vs IMPLEMENTED BUT UNVERIFIED vs PARTIALLY IMPLEMENTED vs PLANNED vs BLOCKED.

## End-of-session checkpoint format

Before ending another development/research chat, ask the assistant or Codex session to append a dated entry to the master archive or a small change-log file with:

| Required field | Record |
| --- | --- |
| Date and UTC time | Exact timestamp |
| GitHub branch + HEAD SHA | Verified via GitHub |
| PR(s) | URLs and whether open/merged |
| Files changed | Exact relative paths |
| Changes and reason | Real implementation, not promises |
| Commands and test results | Exact command, passing/failing/skipped |
| CI evidence | Latest workflow run URL at actual head |
| Research | Source URLs and pinned tags; benchmarks only if measured |
| Security/limits | Any new risk, public-capture/replay gates |
| Status transitions | VERIFIED / IMPLEMENTED BUT UNVERIFIED / PARTIALLY IMPLEMENTED / PLANNED / BLOCKED |
| Next smallest task | Exact file/test/acceptance criteria |

**Privacy:** GitHub is public. Store technical decisions and source links here; do not post private raw chats, credentials or archived personal content.
