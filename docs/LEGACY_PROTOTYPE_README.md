# VersionVault — Website Time Machine

**Prototype v0.1 — a working, local-first Chrome/Edge extension.**

Preserve a screenshot of a website's **currently visible browser tab**, automatically stamp its date, and revisit or compare snapshots later. It works for many websites including ChatGPT, Gemini, Claude, blogs, and storefronts. No cloud account, API key, server, or paid service is required.

## Install in Chrome or Edge

1. Download and **extract** the project ZIP.
2. In Chrome, open `chrome://extensions` (or in Edge, `edge://extensions`).
3. Enable **Developer mode**.
4. Click **Load unpacked** and select the extracted `versionvault-extension` folder containing `manifest.json`.
5. Open a webpage and click the **VersionVault toolbar icon**.
6. Optionally enter a version note and click **Capture this version**.
7. Click **View library** to view snapshots, search, select two to compare side by side, download PNG files, or export/import backups.

> If the toolbar icon is not visible, pin it from your browser's extensions menu.

## Working features

- User-initiated screenshots of the visible area of the active browser tab
- Local screenshot and metadata storage using IndexedDB
- Timestamp, site title, site identity, custom version note
- Archive library with search, per-site filter, and saved-date ordering
- Side-by-side comparison of exactly two captures
- Full-size screenshot viewer; individual PNG download
- Delete selected snapshots; export all to JSON; import JSON backups
- No outgoing network requests made by the extension; no telemetry or external servers
- Only `activeTab` permission; the extension is not automatically reading all your browsing
- URL query strings and fragments are excluded from recorded metadata

## Important limits

- **Screenshot only, not interactive website replay.** This MVP captures just the **visible viewport**. To capture the rest of a long page, scroll and make additional captures.
- **Does not save or run an old AI model.** If OpenAI or Google retires an AI model, this extension cannot continue running it; a screenshot, old web UI, or saved API identifier does not preserve its model weights or hosting service.
- Some browser tabs, protected pages, videos, and restricted contexts may fail capture or show blank content.
- Local IndexedDB can be cleared when removing the extension or deleting its site data. **Export backups regularly.**
- Screenshots may contain private conversations, passwords, personal information, or proprietary content. Stored data is local but **not encrypted** in this prototype. Only capture content you have permission to archive, and keep your exported JSON/PNG files private.
- Chrome/Edge desktop only. No mobile browser implementation or hosted web app yet.
- This is a development prototype and is not independently security-audited or tested across every website.

## File structure

- `manifest.json` — Manifest V3 extension configuration
- `popup.html` + `popup.js` — toolbar capture UI
- `library.html` + `library.js` — browsing, comparison, download, backup
- `db.js` — local storage helpers
- `styles.css` — shared design language
- `icons/` — extension icons

## Product roadmap

1. **v0.1 (included):** manual screenshot captures, local archive, basic comparison, backup.
2. **v0.2:** full-page screenshots, richer metadata, local file-based backups, page change highlighting, screenshot redaction.
3. **v0.3:** WARC/WACZ capture and replay through an archiving engine such as Browsertrix; use an isolated replay viewer and explicit permissions.
4. **v0.4:** multi-device sync, end-to-end encryption, user-owned storage, version timelines, shareable public captures with moderation and takedown processes.
5. **AI history mode:** record model ID, provider, release/deprecation metadata, public product features, and user-exported conversations. Offer live inference only through authorized, still-available APIs or legally hostable open-weight models. Label approximations as approximations.

## Site preservation architecture (later stages)

```
User browser / consent
     |
     +--> visual snapshot --> screenshots + metadata --> encrypted private vault
     |
     +--> authorized website capture --> WARC/WACZ --> safe archival replay viewer
     |
     +--> AI model registry --> provider API (while available) OR open-weight model
                                          --> honest retirement status
```

For production, separate private customer data from a public archive, require explicit consent and access controls, apply copyright/TOS checks and takedown handling, sandbox any replayed content, and do not promise functional replication of proprietary backends.

## Reference materials

- OpenAI model retirement documentation: https://developers.openai.com/api/docs/deprecations
- Gemini model retirement documentation: https://ai.google.dev/gemini-api/docs/deprecations
- Browsertrix Crawler: https://crawler.docs.browsertrix.com/
- ReplayWeb.page: https://replayweb.page/docs/user-guide/
- Chrome tab capture API: https://developer.chrome.com/docs/extensions/reference/api/tabs/

This is an independent prototype; it is not affiliated with OpenAI, Google, Anthropic, or the Wayback Machine.