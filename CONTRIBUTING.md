# Contributing to VersionVault

Welcome! You do not need access to any prior conversations to work on this project.

## Read before doing anything

1. [README.md](README.md)
2. [docs/START_HERE.md](docs/START_HERE.md)
3. [docs/CURRENT_STATUS.md](docs/CURRENT_STATUS.md)
4. [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
5. [docs/REUSE_FIRST.md](docs/REUSE_FIRST.md)
6. [SECURITY.md](SECURITY.md) and [docs/SECURITY_PRIVACY.md](docs/SECURITY_PRIVACY.md)

## Current contribution status

This repo is **planning-first**. The maintainer has **not yet selected a repository-wide license or formal inbound-contribution terms**. Opening an issue or discussing designs is encouraged. Do not submit substantial external code until licensing/contributor terms are clarified and you are comfortable with them. An automatically generated README is not evidence that any code is already released.

## High-value first contributions

- Review and verify references and licenses in THIRD_PARTY_REPOS_TO_STUDY.txt.
- Produce architecture decision records (ADRs) comparing mature archiving engines.
- Establish test fixtures using sites you control or have consent to archive.
- Design a local proof of concept with screenshot + metadata + deterministic export.
- Define WARC/WACZ replay benchmarks and a sandboxing threat model.

## Suggested issue/PR structure

**Problem:** describe a specific user problem and impacted workflow.
**Existing solution research:** alternatives checked, versions/URLs, license and maintenance.
**Proposal:** smallest integration or implementation path.
**Risks:** privacy, threat model, accessibility, storage, copyright and cost.
**Acceptance criteria:** objective reproducible tests.
**Out of scope:** explicitly list postponed work.

Keep PRs narrowly scoped, update docs when changing decisions, do not commit secrets or personal captures, and report which tests were actually executed.

## Conduct and ownership

Be respectful and collaborative; no harassment, doxxing or abusive scraping. Third-party contributors retain whatever rights applicable law and agreed terms provide; maintainers should not assume ownership without explicit licensing. Repo visibility does not automatically license its contents. The maintainer will document definitive code and contribution terms before external-code acceptance.
