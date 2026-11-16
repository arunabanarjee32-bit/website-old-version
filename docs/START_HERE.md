# Start here: the complete VersionVault briefing

**Audience:** any developer, designer, researcher or AI coding agent arriving without the original planning conversation.

## First read: persistent project continuity

[**Master continuity archive — PROJECT_CONTINUITY_MASTER.md**](PROJECT_CONTINUITY_MASTER.md) and [**recovered earlier project chat context**](PROJECT_CHAT_CONTEXT_RECOVERED.md) should both be read. The master archive contains the GitHub-source-backed research, implementation/test history, diagrams, upstream study links, safety boundaries and exact next-session prompt. It supersedes the historical *planning-only* statements below where dated evidence shows working code or a new open PR. Always verify the current main branch and PRs rather than assuming plans were merged.

## The idea in one sentence

Create an independent website preservation system where a user selects a site and a date, saves a reliable record, and can later **find, view, compare, replay (where technically possible) and export** that historical version.

## Why this project exists

Websites and AI interfaces change constantly. Screenshots lose functionality and metadata; browser bookmarks point to the latest site; online services may remove past versions entirely. Existing systems solve parts of the problem, but the intended differentiator is a **single clear experience** combining personal capture, proper archives, historical comparison, and transparent quality reporting.

## Ambition vs reality

Our ambition is to compete with major web-archiving and site-change services. The repository is **not currently a competitor in production**. At documentation kickoff, the repo contained only a minimal README. No working backend, production capture pipeline, deployment or archive service has been verified here. A local-first screenshot extension prototype was created separately during planning and is described in docs/LEGACY_PROTOTYPE_README.md; integrating/auditing its source is a future issue.

## Intended product areas

1. **Personal time machine:** manual/scheduled website captures, collections, tagging, history calendar, side-by-side comparisons, privacy and export.
2. **Capture/replay infrastructure:** browser/HTTP capture, WARC/WACZ, resource integrity, isolated historical playback, fidelity notes.
3. **Website change intelligence:** visual/text changes, schedules, alerts, diffs and shareable reports with appropriate permissions.
4. **AI product preservation:** dated UI snapshots, historical feature/model registry, imported user-owned chats, documented examples, and live links to models that are still legitimately available.
5. **Developer/team platform:** APIs, backups, access control, self-hosting, collaboration, governance and observability.

## A representative user story

A user captures a publicly accessible page in 2026. In 2028 they open VersionVault, search by URL or site, choose the 2026 snapshot, inspect its archived content and screenshot, compare with later dates, and export a standards-based archive. When replay needs a missing server/API, the viewer clearly warns rather than pretending the page still works.

## The central technical rule

A webpage's screenshot/HTML/assets can be stored independently; a server-side service behind it cannot automatically be preserved. Saving a ChatGPT page **never** guarantees future access to OpenAI's retired model. A runnable model requires lawful access to the original weights/hosted service and compatible infrastructure.

## How we build

- Keep one owner-controlled monorepo for **original** VersionVault code.
- Integrate established libraries and services; don't paste whole unrelated repos together.
- Evaluate ArchiveBox, Playwright and Warcio first, with alternative engines as research.
- Verify licenses and AGPL/GPL obligations *before* integration.
- Start with one local end-to-end workflow; only scale after objective benchmarks.
- Use Codex Cloud as a development/test tool, not as permanent production hosting.

## Jump to the right document

| Question | Document |
| --- | --- |
| What's in/out? | [FEATURES_AND_SCOPE](FEATURES_AND_SCOPE.md) |
| How is it designed? | [ARCHITECTURE](ARCHITECTURE.md), [DATA_MODEL](DATA_MODEL.md) |
| What exists right now? | [CURRENT_STATUS](CURRENT_STATUS.md) |
| What should be built first? | [ROADMAP](ROADMAP.md) |
| What can we reuse? | [REUSE_FIRST](REUSE_FIRST.md), [third-party list](../THIRD_PARTY_REPOS_TO_STUDY.txt) |
| How to measure success? | [QUALITY_AND_BENCHMARKS](QUALITY_AND_BENCHMARKS.md) |
| What are the legal/security constraints? | [SECURITY_PRIVACY](SECURITY_PRIVACY.md) |
| How should Codex work? | [AGENTS](../AGENTS.md) |

This is an **independent** project; third-party names are used for comparison, not affiliation or endorsement.
