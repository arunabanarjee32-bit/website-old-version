# Security policy (initial)

VersionVault is an **early-stage project**; no production security claims, responsible-disclosure program, or supported release versions have been established.

**Please do not publish exploit details, credentials, private archived pages, session cookies or personal data in public issues.** Contact the repository owner privately via GitHub profile/contact options to coordinate a confidential report; a dedicated security contact address and advisory workflow should be configured before public launch.

Priority threat classes:
- Server-side request forgery (SSRF), DNS rebinding, redirects to private IPs and metadata services
- Malicious HTML/JS replay, same-origin confusion and cross-site access
- Authenticated capture leaking cookies, tokens, chats or internal pages
- Archive upload/path traversal, zip bombs and oversized captures
- Cross-user access to private snapshots and weak signed URLs
- Supply-chain vulnerabilities, license and retention compliance

See [docs/SECURITY_PRIVACY.md](docs/SECURITY_PRIVACY.md) for the baseline threat model. Do not launch a public fetch-by-URL service without isolation, rate limits, egress controls and penetration testing.
