from __future__ import annotations
import io
import os
import threading
import time
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from versionvault import app as module


class Fixture(BaseHTTPRequestHandler):
    def do_GET(self):
        page = b'<html><head><title>Version 2026</title></head><body><h1>Preserved</h1><p>Fixture only.</p></body></html>'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def log_message(self, *args):
        pass


@pytest.fixture(scope='module')
def fixture_server():
    srv=ThreadingHTTPServer(('127.0.0.1', 8766), Fixture)
    thread=threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()
    thread.join(timeout=2)
    srv.server_close()


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(module, 'DATA_DIR', tmp_path)
    monkeypatch.setattr(module, 'DB_PATH', tmp_path / 'snapshots.sqlite3')
    return TestClient(module.app)


@pytest.mark.parametrize('url', [
    'https://example.com', 'http://127.0.0.1:80/', 'http://localhost:8766/',
    'http://127.0.0.1:8766@evil.com/', 'http://169.254.169.254/',
    'file:///etc/passwd', 'http://127.0.0.1:8766/#fragment',
    'http://127.0.0.1:8766.evil.com', 'javascript:alert(1)',
])
def test_blocks_unsafe_urls(client, url):
    assert not module.is_permitted_url(url)
    assert client.post('/api/captures', json={'url':url}).status_code == 403


def test_home_and_empty_history(client):
    assert 'VersionVault' in client.get('/').text
    assert client.get('/api/snapshots').json() == []


def test_capture_compare_export_import(client, fixture_server):
    response = client.post('/api/captures', json={'url':'http://127.0.0.1:8766/'})
    assert response.status_code == 202
    job_id = response.json()['id']
    deadline = time.monotonic() + 60  # CI browsers can start slowly under load.
    while time.monotonic() < deadline:
        job = client.get('/api/jobs/'+job_id).json()
        if job['state'] in ('failed', 'ready'):
            break
        time.sleep(.25)
    assert job['state'] == 'ready', job
    snaps = client.get('/api/snapshots').json()
    assert len(snaps) == 1
    snap = snaps[0]
    assert snap['title'] == 'Version 2026'
    shot = client.get('/api/snapshots/'+snap['id']+'/screenshot')
    assert shot.status_code == 200 and shot.content.startswith(b'\x89PNG')
    exported = client.get('/api/snapshots/'+snap['id']+'/export')
    assert exported.status_code == 200
    with zipfile.ZipFile(io.BytesIO(exported.content)) as f:
        assert sorted(f.namelist()) == ['manifest.json','page.html','screenshot.png']
    imported = client.post('/api/import', files={'file':('archive.zip', exported.content, 'application/zip')})
    assert imported.status_code == 201, imported.text
    assert len(client.get('/api/snapshots').json()) == 2
    corrupted = bytearray(exported.content)
    corrupted[1] ^= 0xff
    rejected = client.post('/api/import', files={'file':('bad.zip',bytes(corrupted),'application/zip')})
    assert rejected.status_code == 400


def test_unknown_job_and_snapshot(client):
    assert client.get('/api/jobs/unknown').status_code == 404
    assert client.get('/api/snapshots/unknown').status_code == 404
