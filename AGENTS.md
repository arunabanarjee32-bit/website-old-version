# Instructions for Codex and coding agents

You are working on **VersionVault**, an independent long-term web preservation platform. Read README.md and docs/START_HERE.md before touching implementation. There is no confirmed production system in this repository as of the initial documentation import.

## Required chat-independent continuity

Before starting substantive work, read [docs/PROJECT_CONTINUITY_MASTER.md](docs/PROJECT_CONTINUITY_MASTER.md) and [docs/PROJECT_CHAT_CONTEXT_RECOVERED.md](docs/PROJECT_CHAT_CONTEXT_RECOVERED.md), which records the accessible earlier project-chat excerpts and explicit coverage limitations. It retains public-safe technical research, 22 upstream links, exactly two primary systems, architecture charts, branch/PR status, CI evidence, security gates, and a ready-to-reuse next-session prompt. Do not assume previous ChatGPT conversations can be loaded or that a green unmerged PR exists on main. After each session, add a checkpoint with commit SHA, tested results, links, known failures and next task. Never publish raw private conversation data in this public repository.

## Non-negotiable task workflow

1. Inspect the actual working tree, tests, environment and current state. Never assume features exist because they are on the roadmap.
2. Write a short feature-to-existing-solution comparison for any significant task. See THIRD_PARTY_REPOS_TO_STUDY.txt and docs/REUSE_FIRST.md.
3. Prefer maintained, permissively licensed dependencies where appropriate. Never copy code from AGPL/GPL repositories into proprietary application modules without an explicit approved licensing decision. A service boundary does not magically eliminate network-copyleft obligations.
4. Plan the smallest complete vertical slice, then code, test, document, and report evidence.
5. Protect existing files; do not rewrite working components just to standardize stacks. Avoid new services until necessary.
6. Do not introduce secrets, customer captures, private conversation exports, provider session cookies, or API keys into commits, logs or fixtures.
7. Before claiming success, execute appropriate tests or plainly state which tests could not run in Codex Cloud.
8. No auto-deployment of public crawlers or public archive releases without maintainer approval.

## Product truthfulness

- Screenshot capture != static HTML preservation != complete archived-resource replay != original live website.
- Preserving the ChatGPT/Gemini/Claude UI and user-owned exports != preserving provider-hosted proprietary AI model inference.
- Model substitutions must be labeled as **simulated/alternative**, not as the original retired model.
- No bypassing authentication, anti-abuse controls, paid content, DRM or private endpoints.

## Security requirements

Treat submitted URLs and all downloaded content as hostile. Prevent SSRF (including DNS rebinding, redirect-to-private, cloud metadata, and private network exposure); isolate capture workers and replay origins; disallow unsafe outbound access; redact cookies and tokens; secure import/export paths; use per-user authorization; resource limits and crawl rate limits; never trust HTML/JS from archives.

## Proposed build order

- ADR + dependency/rights inventory + threat model
- Local runnable workflow: submit permitted public URL -> create job -> capture screenshot/HTML -> persist metadata and content -> browse history -> export
- WARC/WACZ support and isolated replay using evaluated and license-compatible engine
- Diff/timeline/search, extension, monitoring
- AI export/history features, teams and scale

## Definition of done

- Reproducible local startup documented and verified
- Unit/integration/e2e tests relevant to change, with results
- API/schema/migration and usage docs updated
- Licensing/security checks updated
- Clear limitations and follow-on tasks

Start every large task by auditing existing code and writing what can be reused. When uncertain, stop at a research/ADR deliverable instead of speculative infrastructure code.
