# Security, privacy, legal and operational safeguards

This is a threat-model starter, not security certification. Public website capture and replay have exceptionally high risk due to attacker-controlled URLs and JavaScript.

## Crawl security

- SSRF prevention: allow only approved HTTP(S) schemes; resolve and validate every DNS answer, response redirect, proxy and network hop; block loopback, RFC1918, link-local, metadata endpoints, internal DNS and IPv6 private ranges.
- Network-level egress filtering and isolated ephemeral worker containers; URL validation alone is insufficient because of DNS rebinding.
- Hard limits: crawl depth, allowed domains, bytes, CPU, memory, duration, concurrency, redirects and requests per host.
- Do not archive passwords, auth tokens, cookies or other sensitive state by default; require explicit consent and granular scope for any private capture.
- No credential forwarding to arbitrary user-submitted hosts.

## Replay security

- Replayed HTML, scripts, embeds and uploads are hostile. Serve on a separate sandboxed origin with strong isolation, CSP, restricted capabilities and no session cookies.
- Avoid live network fallback without clear user consent; no execution in the main app origin.
- Prevent malicious archives, decompression bombs, path traversal and MIME sniffing attacks.
- Explicit warnings for incomplete replay; never claim the original website still works when server-side functionality is gone.

## Privacy and rights

- Default all personal collections and AI chat exports to PRIVATE.
- Explicit publish/share workflow with preview, sensitive-content redaction and rights checks.
- Implement export/delete/retention and secure backups before multi-user launch.
- Respect applicable copyright, privacy, access control, publisher policies and takedown obligations; obtain permission for restricted/private material.
- Keep provenance (URL, date, tool/version, hashes, known capture errors).
- Avoid publishing others' personal data through crawl-derived archives.

## Operational requirements

Rate limiting, logs without secrets, audit trails, encryption in transit/at rest as warranted, scoped keys, automated vulnerability scans, backup and restore tests, service abuse detection, incident response and independent review before internet-wide deployment.

## AI-specific limitations

- Imported chat history must be user-authorized and treated as sensitive personal data.
- Model release dates/status need cited primary sources and last-verified timestamps.
- An old frontend cannot revive a deprecated provider backend or inaccessible model weights.
- Alternative models/approximate replay must be clearly labeled.

## Legal/licensing

See docs/REUSE_FIRST.md. Do not publish proprietary rebrands of unreviewed copyleft software. The product's own license, contributor terms and brand/trademark clearance are open maintainer decisions.
