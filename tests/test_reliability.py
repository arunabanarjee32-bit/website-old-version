"""Reliability and hostile-import tests for the strictly local MVP."""
from __future__ import annotations

import io
import json
import uuid
import warnings
import zipfile
import zlib

import pytest
from fastapi.testclient import TestClient
from versionvault import app as module


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "DATA_DIR", tmp_path)
    monkeypatch.setattr(module, "DB_PATH", tmp_path / "snapshots.sqlite3")
    with TestClient(module.app) as api:
        yield api


def _chunk(kind: bytes, body: bytes) -> bytes:
    return (
        len(body).to_bytes(4, "big") + kind + body
        + zlib.crc32(kind + body).to_bytes(4, "big")
    )


def png() -> bytes:
    ihdr = (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + bytes([8, 6, 0, 0, 0])
    raw_pixel = b"\x00\xff\x00\x00\xff"
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", ihdr)
        + _chunk(b"IDAT", zlib.compress(raw_pixel))
        + _chunk(b"IEND", b"")
    )


def create_archive(case: str = "valid") -> bytes:
    html = b"<html><title>local fixture</title></html>"
    image = png()
    if case == "compression_bomb":
        html = b"x" * 1_000_000
    if case == "invalid_png_crc":
        image = image[:-1] + bytes([image[-1] ^ 1])  # Invalidate IEND chunk CRC.
    snap = {
        "url": "http://127.0.0.1:8766/",
        "title": "Local fixture",
        "captured_at": "2026-11-15T12:00:00+00:00",
        "html_sha": module.sha256(html),
        "screenshot_sha": module.sha256(image),
    }
    if case == "invalid_metadata":
        snap["title"] = {"object": "not a string"}
    if case == "wrong_hash":
        snap["html_sha"] = "0" * 64
    manifest = json.dumps({"format": "versionvault-local-demo-v1", "snapshot": snap}).encode()
    if case == "oversize_manifest":
        manifest = b" " * 65_000 + manifest
    if case == "invalid_json":
        manifest = b"not-json"
    contents = {"manifest.json": manifest, "page.html": html, "screenshot.png": image}
    if case == "missing_entry":
        del contents["page.html"]
    if case == "extra_entry":
        contents["../evil"] = b"do not extract"
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in contents.items():
            archive.writestr(name, payload)
        if case == "duplicate_entry":
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                archive.writestr("page.html", html)
    return buffer.getvalue()


def test_valid_minimal_png_roundtrip(client):
    result = client.post(
        "/api/import",
        files={"file": ("fixture.zip", create_archive(), "application/zip")},
    )
    assert result.status_code == 201, result.text
    screenshot = client.get("/api/snapshots/" + result.json()["id"] + "/screenshot")
    assert screenshot.status_code == 200
    assert screenshot.content == png()


@pytest.mark.parametrize("case", [
    "compression_bomb", "invalid_png_crc", "invalid_metadata", "wrong_hash",
    "oversize_manifest", "invalid_json", "missing_entry", "extra_entry",
    "duplicate_entry",
])
def test_rejects_unsafe_archive_without_mutating_history(client, case):
    response = client.post(
        "/api/import",
        files={"file": ("untrusted.zip", create_archive(case), "application/zip")},
    )
    assert response.status_code == 400, (case, response.text)
    assert client.get("/api/snapshots").json() == []


def test_import_upload_limit(client):
    response = client.post(
        "/api/import",
        files={"file": ("large.zip", b"x" * 10_000_001, "application/zip")},
    )
    assert response.status_code == 413
    assert client.get("/api/snapshots").json() == []


def test_interrupted_jobs_are_failed_on_startup(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "DATA_DIR", tmp_path)
    monkeypatch.setattr(module, "DB_PATH", tmp_path / "snapshots.sqlite3")
    ids = {state: uuid.uuid4().hex for state in ("queued", "running", "ready", "failed")}
    with module.connect() as db:
        for state, job_id in ids.items():
            db.execute(
                "INSERT INTO jobs VALUES (?, ?, ?, NULL, ?)",
                (job_id, "http://127.0.0.1:8766/", state, "2026-11-15T12:00:00Z"),
            )
    with TestClient(module.app) as api:
        for state in ("queued", "running"):
            job = api.get("/api/jobs/" + ids[state]).json()
            assert job["state"] == "failed"
            assert job["error"] == "InterruptedByRestart"
        assert api.get("/api/jobs/" + ids["ready"]).json()["state"] == "ready"
        assert api.get("/api/jobs/" + ids["failed"]).json()["state"] == "failed"
