# Feature inventory and scope

Legend: **MVP** = first runnable vertical slice; **Next** = after MVP evidence; **Later** = strategic expansion; **Research** = feasibility/legal/licensing gate. These are PLANNED features, not shipped functionality.

| Feature | Phase | Acceptance intent |
| --- | --- | --- |
| User submits public URL | MVP | strict URL validation + SSRF protection; clear error states |
| Asynchronous capture job | MVP | progress/status, retries and bounded resources |
| Screenshot of rendered page | MVP | timestamp, viewport, provenance, hash and downloadable image |
| HTML/response capture | MVP | preserve retrievable content, identify missing resources |
| Metadata and history by URL/date | MVP | list and retrieve any saved capture |
| Local export + import | MVP | round-trip preserves data/hash and privacy |
| Basic version comparison | MVP | two captures, accessible side-by-side UI |
| WARC/WACZ durable archives | Next | standards-oriented archive with verification |
| Isolated historical replay | Next / Research | replay without trusting saved scripts or leaking sessions |
| Textual/visual differences | Next | stable comparison with exclusions and test fixtures |
| Browser extension | Next | explicit per-site user gesture and clear permissions |
| Scheduled capture, alerts | Next | rate limits, retry behavior, user-owned monitoring |
| Search across sites and capture text | Next | transparent indexing and permission enforcement |
| AI chat export/import and provider history | Next | explicit user-owned sources; private by default |
| Historical AI model inference | Research | only lawful weights or provider APIs still available |
| Team roles, private workspaces, audit logs | Later | security, recovery, policy controls |
| Heritrix/crawler cluster, large-scale crawling | Later | justified by quality/cost/throughput metrics |
| Public archive service, community collections | Later | copyright, takedown, abuse and moderation processes |
| Desktop apps, cloud sync, billing | Later | evidence of demand and operational readiness |

## Capture type labels in product

- **Screenshot:** image only. No functionality implied.
- **Static page:** HTML/assets may display, but live server actions can be absent.
- **Resource archive:** WARC/WACZ of observed requests/responses.
- **Replay:** browser/viewer reconstructs recorded interactions *as supported*.
- **Live:** currently running original service; not a saved version.
- **AI alternative/simulation:** third-party or open-weight replacement, NEVER labeled the retired proprietary original.

## Out of scope for early releases

No global internet crawler, no unapproved use of user cookies or API keys, no bypassing robots/authorization/access control, no claims of permanent historic AI-model availability, no storing secrets by default, no direct execution of archived JS in trusted application origin.
