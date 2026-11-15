# Quality, benchmarking and definition of done

The product goal is to compete on **measurable fidelity and usability**, not copied marketing claims.

## Benchmark corpus

Create 30+ legal-to-archive test targets, including sites we operate or explicitly permissioned fixtures:
- static HTML, complex CSS, fonts/images
- SPAs with client-side routing and delayed rendering
- dynamically loaded lists, embedded media (where permitted)
- redirects, error responses, canonical URL variants
- pages with robots/publisher limits and controlled authentication fixtures
- accessibility and mobile/responsive viewports
- intentionally malicious URLs/redirects for SSRF tests
- archives with missing resources, malicious JS and decompression edge cases

Do not run a public internet crawler as a test by default.

## Core metrics

| Metric | Measurement |
| --- | --- |
| Capture completion | passed captures / attempted captures (with reason codes) |
| Screenshot similarity | pinned viewport and deterministic fixture image comparison |
| Resource completeness | recorded expected resources / observed expected resources |
| Replay success | scripted interactions supported in offline isolated viewer |
| Timeline correctness | timestamp ordering and version identity |
| Search coverage/quality | retrieval precision/recall on deterministic corpus |
| Export/import fidelity | archive hash/manifest equivalence after round trip |
| Security | passed egress/SSRF, isolation and cross-user access tests |
| Reliability | failed/timeout/retry rates and crash-free tasks |
| Unit economics | CPU time, memory and storage bytes per capture |
| Accessibility | automated checks + keyboard/screen-reader manual audits |

## MVP acceptance scenario

On a clean machine with documented startup:
1. Submit a permitted demo URL.
2. Observe queued -> completed job and bounded failure handling.
3. Confirm screenshot and metadata persisted and timestamp shown.
4. Reopen by site and date and compare two snapshots.
5. Export and re-import data with hashes/identity intact.
6. Confirm SSRF fixtures and malicious archived content cannot reach protected resources.
7. Confirm README setup and CI tests match actual behavior.

If a step is unavailable, mark it **not implemented**, not passed. Later write and publish reproducible comparative measurements against third-party tools.
