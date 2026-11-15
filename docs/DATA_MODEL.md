# Proposed data model (not migrations yet)

The minimum model should support versions, provenance and private access control without overfitting to any one archiving engine.

```text
users(id, email_or_external_subject, created_at)
collections(id, owner_id, name, visibility, created_at)
sites(id, normalized_origin, display_name)
snapshots(
  id, collection_id, site_id, submitted_url, normalized_url,
  captured_at, capture_mode, status, title, viewport,
  screenshot_key, archive_key, content_hash_sha256, byte_size,
  recorder_name, recorder_version, warning_json, owner_id, visibility
)
capture_jobs(
  id, owner_id, requested_url, capture_options_json, state,
  submitted_at, started_at, finished_at, error_code, attempt
)
snapshot_resources(id, snapshot_id, resource_url, status, mime_type, sha256)
comparison_reports(id, left_snapshot_id, right_snapshot_id, report_key, created_at)
ai_providers(id, name, website)
ai_models(
  id, provider_id, official_model_id, display_name, released_at,
  retired_at, current_api_status, source_url, last_verified_at
)
ai_conversation_imports(
  id, owner_id, provider_id, source_type, imported_at,
  encrypted_object_key, visibility, consent_record
)
audit_events(id, actor_id, action, resource_type, resource_id, timestamp)
```

## Critical invariants

- Every private resource query is scoped by owner/team authorization, NOT just by guessed object ID.
- Snapshots are immutable after finalization; corrections create new metadata version/audit trail.
- URLs used as crawl targets are validated after DNS resolution and every redirect; submitted URL and final observed URL are both recorded.
- Archive/screenshot blobs are separately hashed and can be exported with integrity manifest.
- User data and imported AI conversations are private by default, deletable, exportable and excluded from public indexing.
- Time is stored in UTC with explicit capture source and display timezone.
- Distinguish unsuccessful capture, successful screenshot, partial resources and verified playable archive.
- Avoid retaining authenticated cookies and credentials in archives unless a separately designed, explicit and secured workflow exists.

Use migrations and enforce relational constraints before introducing multi-user production behavior.
