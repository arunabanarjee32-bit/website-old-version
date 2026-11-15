# VersionVault — Product Blueprint

**Working project name:** VersionVault (check availability and trademark before launch).

## Product vision

Give people a trustworthy way to save, revisit, and compare earlier versions of websites and AI products. A saved website's appearance can survive a redesign; a retired proprietary AI model cannot be kept running merely by preserving a page. The product must never confuse those two guarantees.

## Three distinct products under one roof

1. **Visual Vault (build first):** user-initiated screenshot captures, dates, site metadata, browsing timeline, side-by-side comparisons, private backups. The accompanying Chrome/Edge prototype implements the core workflow.
2. **Web Replay Vault (build second):** archived HTML, CSS, JavaScript, and HTTP resources via WARC/WACZ, sandboxed replay, website-specific quality reporting. Not all logged-in/dynamic/cloud-backed functions replay.
3. **AI History Vault (build third):** model release history, examples, user-exported conversations, prompts/evaluation sets, authorized live access to supported model IDs and clearly labeled approximations from available alternative/open-weight models. Only provider permission or lawful possession of runnable weights allows preservation of exact inference after retirement.

## An example user journey

- On November 13, 2026, the user opens ChatGPT or Gemini and clicks the extension to save a screenshot with note `November 2026 UI`.
- Later, the user records additional versions. Their archive sorts records by date, groups websites by host, and allows side-by-side screenshot comparison.
- Years later, the saved screenshots still display locally, assuming the user retained the data or exported backups. Live prompts are routed only to an authorized available API or another model, never secretly represented as the archived proprietary model.

## MVP functionality

| Module | Included in prototype? | Notes |
|---|---|---|
| Capture visible page screenshot | Yes | User clicks; not full page |
| Timestamp/URL/title/user note | Yes | Queries and fragments removed |
| Local persistence | Yes | IndexedDB on user's device |
| Search/filter library | Yes | Site and text filters |
| Compare two versions | Yes | Two screenshots side by side |
| Export/import backup | Yes | JSON containing embedded images |
| Screenshot PNG export/delete | Yes | Direct local actions |
| Whole-page screenshot | No | Future enhancement |
| Interactive replay / WARC | No | Requires dedicated archive engine |
| Background scheduled captures | No | Requires new permissions & controls |
| Live deprecated model support | No | Not possible when unsupported by provider |

## Proposed production architecture

- **Capture clients:** Chromium browser extension first; desktop app later if cross-browser full-page capture is critical.
- **Web app:** Next.js/React version library and archive browser.
- **API:** TypeScript or Python service for authentication, capture jobs, catalog CRUD, and version comparison metadata.
- **Background jobs:** a queue for user-authorized, rate-limited page crawls; Browsertrix for WARC/WACZ archiving.
- **Storage:** PostgreSQL for metadata; object storage for screenshots/WACZ; optional private encrypted user storage.
- **Replay:** isolated archival replay, for example ReplayWeb.page, with active third-party execution restricted and careful content security isolation.
- **AI catalog:** provider/model/release/status tables, tests and output examples; connect to official, active model APIs via users' authorized keys or to hostable open-weight systems when rights allow.

## Suggested metadata schema

`snapshots(id, owner_id, normalized_url, site_name, title, captured_at, snapshot_type, screenshot_object_key, archive_object_key, sha256, visibility, notes, capture_status)`

`ai_models(id, provider, display_name, official_model_id, released_at, retired_at, api_status, access_method, source_url, behavioral_test_set)`

`behavioral_examples(id, model_id, captured_at, input_text, output_text, license_or_user_consent, dataset_reference)`

Use a strongly enforced separation between public reference captures and private user captures. Do not publish private conversations by default.

## Risks and controls

- **False claims:** never advertise that a screenshot means a retired model still works. Mark `visual snapshot`, `archival replay`, `live model`, and `simulation` separately.
- **Privacy:** screenshots may contain names, passwords, chats, and customer data. Add selective redaction, local encryption, consent, retention controls, and an explicit sharing step.
- **Copyright, trademarks, terms:** verify archiving and redistribution rights; maintain takedown process; avoid appearing official or using branding as if endorsed.
- **Security:** sandbox replayed pages; isolate customer data; treat archival HTML/JS as untrusted; restrict crawl endpoints to mitigate SSRF and abuse; rate-limit capture.
- **Reliability:** future websites may be impossible to faithfully reproduce due to missing APIs, DRM, personalization, login requirements, or external content. Store capture quality notes and hashes.
- **Durability:** export open formats, store independent copies, maintain migrations and backups. A web app alone is not enough without durable storage.

## Launch sequence

**Phase A: Validate demand.** Publish open-source local extension and test whether people save more than one version, compare captures, and return to archives.

**Phase B: Make archive quality better.** Full-page capture, diff highlighting, tags, screenshots with redaction, rich metadata and cloud-optional backup.

**Phase C: Add archival replay.** WACZ/WARC capture, replay in an isolated context, archiving quality score, opt-in scheduling.

**Phase D: AI history experience.** Catalog changes to AI products and APIs, model shutdown alerts, archived example answers, and clearly labeled supported inference.

## Business model ideas

Keep local manual capture free. Potential paid tiers can add opt-in automatic version tracking, team workspaces, encrypted backups, larger storage, and visual-diff alerts. For organizations, an audit trail of public website changes may be a more practical first paying use case than claiming historical AI model access.

## Reference projects and official policies

- Browsertrix Crawler: https://crawler.docs.browsertrix.com/
- ReplayWeb.page: https://replayweb.page/docs/user-guide/
- OpenAI model deprecation: https://developers.openai.com/api/docs/deprecations
- Gemini deprecation: https://ai.google.dev/gemini-api/docs/deprecations
- Chrome captureVisibleTab: https://developer.chrome.com/docs/extensions/reference/api/tabs/

**Independent concept; not affiliated with the providers named above.**