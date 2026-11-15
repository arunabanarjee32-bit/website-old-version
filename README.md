# VersionVault — Website Old Version Preservation

> **Project status (2026-11-15):** A **locally tested, restricted fixture-only MVP** is now committed in services/api/versionvault. It includes capture jobs, screenshot, metadata, dated history, two-pane comparison and hashed ZIP import/export. **General public crawling, WARC/WACZ replay, production security, accounts and deployment are NOT implemented.** The earlier extension prototype remains separate.

## Recover project context without an old ChatGPT chat

**[Read the complete VersionVault continuity archive](docs/PROJECT_CONTINUITY_MASTER.md)** · **[Copy the new-chat starter prompt](docs/CONTINUE_IN_NEW_CHAT.md)** — the persistent, public-safe project brief: verified code status, research findings, all 22 study links, five Mermaid architecture/workflow charts, decisions, PR/CI history, security gates, exact commands, and a prompt for the next developer or AI session. Read this **before** relying on long chat history. The archive is a curated technical record, **not a raw private chat export**.

**Branch caveat:** foundation CI and 24-test reliability improvements are proposed in [PR #1](https://github.com/arunabanarjee32-bit/website-old-version/pull/1); they do not exist on main until merged. New sessions must inspect live PR/CI state.

## Mission

Build an independent, trustworthy, self-hostable and eventually cloud-hosted **website time machine** that lets people capture, preserve, search, replay where possible, compare, and export earlier versions of websites. Treat the preservation of AI product interfaces and users' authorized conversation exports as a special use case.

**Long-term aspiration:** compete on usability, modern-site fidelity, privacy, transparency and developer experience with the strongest web-archiving products (Internet Archive's Wayback Machine, Archive-It, ArchiveBox, Browsertrix/Webrecorder, and change-monitoring tools). This is an aspiration, **not** a claim that VersionVault currently matches those platforms.

**Hard boundary:** saving ChatGPT/Gemini/Claude interfaces or transcripts **does not preserve** discontinued proprietary AI models, provider servers or private APIs. Never imply otherwise.

## Runnable local demo and new engineering documentation

See [LOCAL_DEMO.md](LOCAL_DEMO.md) for setup and hard restrictions: the only allowed capture target is http://127.0.0.1:8766/ and its paths. On the local research host, PYTHONPATH=services/api pytest -q reported **12 passing tests**; hosted CI and real-world website benchmarks have not run.

- [Repo audit](docs/REPOSITORY_AUDIT.md)
- [Engineering comparison of all 22 public repos](docs/REPOSITORY_RESEARCH_MATRIX.md)
- [Exactly two primary systems selected](docs/TOP_TWO_REPOSITORIES.md)
- [ADR-001 architecture decision](docs/adr/ADR-001-capture-architecture.md)
- [Master implementation checklist](docs/MASTER_IMPLEMENTATION_CHECKLIST.md)
- [Competitor feature gaps](docs/COMPETITOR_FEATURE_GAPS.md)
- [Developer handoff](docs/DEVELOPER_HANDOFF.md)

## Start here

- [New contributor orientation](docs/START_HERE.md) — complete onboarding without prior chat context.
- [Product vision and who it serves](docs/PRODUCT_VISION.md)
- [Feature specification and boundaries](docs/FEATURES_AND_SCOPE.md)
- [System architecture](docs/ARCHITECTURE.md) and [data model](docs/DATA_MODEL.md)
- [Competitive landscape](docs/COMPETITIVE_LANDSCAPE.md)
- [Reuse-first technical decisions](docs/REUSE_FIRST.md)
- **[Every suggested GitHub project to study (TXT)](THIRD_PARTY_REPOS_TO_STUDY.txt)**
- [Roadmap and first milestone](docs/ROADMAP.md)
- [Acceptance tests and benchmarks](docs/QUALITY_AND_BENCHMARKS.md)
- [Security, privacy, legal risks](docs/SECURITY_PRIVACY.md)
- [AI product preservation limitations](docs/AI_PRESERVATION.md)
- [Current status and open decisions](docs/CURRENT_STATUS.md)
- [Codex instructions](AGENTS.md), [contributing](CONTRIBUTING.md), [reporting security issues](SECURITY.md)

The [original planning blueprint](docs/ORIGINAL_PRODUCT_BLUEPRINT.md) is retained for context, but where it differs from newer docs, treat the newer docs as proposed guidance—not as code already implemented.

## Why one repository?

VersionVault is intended to have **one owner-controlled monorepo for our original application code**, integrating stable, appropriately licensed libraries and separate engines as dependencies/services. Do **not** simply copy whole unrelated open-source repositories into this tree. A hosted service or container can be integrated without importing its entire source, subject to its license and deployment requirements.

Proposed future structure (NOT yet implemented):

```text
apps/web/                 # browser-facing version library
apps/extension/           # consent-based capture extension
services/api/             # user/archive/catalog API
services/worker/          # capture jobs, indexing and QA
packages/contracts/       # shared schemas and types
infra/                    # local Compose and deployment manifests
docs/                     # architecture and contributor handbook
tests/                    # capture, replay, security, e2e benchmarks
```

## Guiding principles

1. **Reuse before rebuilding.** Research existing solutions before requesting new Codex code.
2. **Truthful archival fidelity.** Label screenshots, static copies, WARC/WACZ replay, live apps, and AI simulations distinctly.
3. **Security first.** Arbitrary URLs, archived scripts and private captures are untrusted.
4. **Privacy by default.** Never publish authenticated pages, private conversations or sensitive captures automatically.
5. **Interoperability.** Prefer portable WARC/WACZ and documented export formats.
6. **Measurable quality.** Reliability, fidelity, cost/capture, restoreability and usability matter more than lines of code.
7. **No license shortcuts.** All third-party dependencies require individual license and security review.

## Contributing and usage

Read [CONTRIBUTING.md](CONTRIBUTING.md) and [AGENTS.md](AGENTS.md). There is **no project-wide open-source license committed yet**. Public visibility does not grant permission to copy/redistribute repository content. The maintainer must choose and publish a license or explicit contributor terms before accepting substantial outside contributions. All brand and trademark decisions remain open.

This project is independent; it is not affiliated with OpenAI, Google, Anthropic, Internet Archive or the third-party software projects listed here.
