"""Local-only capture MVP. NEVER expose as a public URL fetcher.

Only explicitly permitted literal 127.0.0.1 fixture URLs can be captured.
This isn't a substitute for process-level production network isolation.
"""
from __future__ import annotations

import hashlib
import io
import ipaddress
import json
import os
import sqlite3
import uuid
import zipfile
import zlib
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response
from pydantic import BaseModel

# Do NOT expand this to general internet hosts without SSRF/egress controls.
FIXTURE_PORT = int(os.environ.get("VV_FIXTURE_PORT", "8766"))
DATA_DIR = Path(os.environ.get("VV_DATA_DIR", "./.versionvault-data")).resolve()
DB_PATH = DATA_DIR / "snapshots.sqlite3"
EXECUTOR = ThreadPoolExecutor(max_workers=1, thread_name_prefix="vv-capture")


@asynccontextmanager
async def lifespan(_application: FastAPI):
    # A process restart cannot resume an in-process ThreadPoolExecutor task.
    # Fail orphaned jobs explicitly instead of leaving them "running" forever.
    with connect() as db:
        db.execute(
            "UPDATE jobs SET state='failed', error='InterruptedByRestart' "
            "WHERE state IN ('queued', 'running')"
        )
    yield


app = FastAPI(title="VersionVault (local fixture demo)", version="0.1.0", lifespan=lifespan)


def is_permitted_url(raw: str) -> bool:
    if not isinstance(raw, str) or len(raw) > 2048:
        return False
    try:
        parsed = urlsplit(raw)
        # Numeric loopback is deliberate: no DNS resolution/rebinding allowed.
        return (
            parsed.scheme == "http"
            and parsed.hostname == "127.0.0.1"
            and parsed.port == FIXTURE_PORT
            and not parsed.username
            and not parsed.password
            and not parsed.fragment
            and ipaddress.ip_address(parsed.hostname).is_loopback
        )
    except (ValueError, TypeError):
        return False


def connect():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA busy_timeout=10000")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""CREATE TABLE IF NOT EXISTS jobs
        (id TEXT PRIMARY KEY, url TEXT NOT NULL, state TEXT NOT NULL,
         error TEXT, created_at TEXT NOT NULL)""")
    conn.execute("""CREATE TABLE IF NOT EXISTS snapshots
        (id TEXT PRIMARY KEY, url TEXT NOT NULL, title TEXT NOT NULL,
         captured_at TEXT NOT NULL, screenshot_sha TEXT NOT NULL,
         html_sha TEXT NOT NULL)""")
    conn.commit()
    return conn


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def store_object(data: bytes) -> str:
    digest = sha256(data)
    base = DATA_DIR / "objects"
    base.mkdir(parents=True, exist_ok=True)
    target = base / digest
    if not target.exists():
        temp = base / (digest + "." + uuid.uuid4().hex + ".tmp")
        temp.write_bytes(data)
        temp.replace(target)
    return digest


def object_path(digest: str) -> Path:
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise HTTPException(status_code=400, detail="Invalid digest")
    target = DATA_DIR / "objects" / digest
    if not target.exists():
        raise HTTPException(status_code=404, detail="Archive object missing")
    if sha256(target.read_bytes()) != digest:
        raise HTTPException(status_code=409, detail="Archive object failed integrity check")
    return target


def capture_job(job_id: str, url: str):
    try:
        with connect() as db:
            db.execute("UPDATE jobs SET state='running' WHERE id=?", (job_id,))
        class DenyRedirect(HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                raise ValueError("Redirects are disabled in the local fixture prototype")

        # Browser navigation is restricted by this execution environment.
        # Fetch a strictly allowlisted numeric loopback origin without redirects,
        # then render the downloaded HTML in an offline browser context.
        opener = build_opener(DenyRedirect)
        with opener.open(Request(url, headers={"User-Agent": "VersionVault-local-fixture/0.1"}), timeout=5) as resp:
            if resp.status != 200 or not resp.headers.get_content_type() == "text/html":
                raise ValueError("Fixture must return HTML 200")
            html = resp.read(2_000_001)
        if len(html) > 2_000_000:
            raise ValueError("Fixture HTML too large")
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            args = []
            # Local demo runs as root in some CI containers. NEVER use this
            # no-sandbox fallback for a production worker.
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                args.append("--no-sandbox")
            browser = pw.chromium.launch(
                headless=True,
                executable_path=os.environ.get("VV_CHROMIUM", "/usr/bin/chromium"),
                args=args,
            )
            try:
                context = browser.new_context(service_workers="block", viewport={"width": 1120, "height": 760})
                page = context.new_page()
                context.set_offline(True)  # No live scripts/assets/network in demo preview.
                page.route("**/*", lambda route: route.abort())
                page.set_content(html.decode("utf-8", errors="replace"), wait_until="load", timeout=12000)
                title = page.title()[:200]
                screenshot = page.screenshot(full_page=True, type="png")
                context.close()
            finally:
                browser.close()
        screenshot_sha = store_object(screenshot)
        html_sha = store_object(html)
        with connect() as db:
            db.execute("INSERT INTO snapshots VALUES (?, ?, ?, ?, ?, ?)",
                       (uuid.uuid4().hex, url, title,
                        datetime.now(timezone.utc).isoformat(), screenshot_sha, html_sha))
            db.execute("UPDATE jobs SET state='ready' WHERE id=?", (job_id,))
    except Exception as exc:
        # Avoid logging raw content or credentials.
        with connect() as db:
            db.execute("UPDATE jobs SET state='failed', error=? WHERE id=?", (type(exc).__name__, job_id))


class CaptureRequest(BaseModel):
    url: str


@app.post("/api/captures", status_code=202)
def begin_capture(payload: CaptureRequest):
    if not is_permitted_url(payload.url):
        raise HTTPException(status_code=403, detail="Local demo only: use http://127.0.0.1:8766/ fixture")
    job = uuid.uuid4().hex
    with connect() as db:
        db.execute("INSERT INTO jobs VALUES (?, ?, 'queued', NULL, ?)",
                   (job, payload.url, datetime.now(timezone.utc).isoformat()))
    EXECUTOR.submit(capture_job, job, payload.url)
    return {"id": job, "state": "queued"}


@app.get("/api/jobs/{job_id}")
def job_status(job_id: str):
    with connect() as db:
        row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Unknown job")
    return dict(row)


@app.get("/api/snapshots")
def list_snapshots():
    with connect() as db:
        return [dict(row) for row in db.execute("SELECT * FROM snapshots ORDER BY captured_at DESC, id DESC").fetchall()]


def get_snapshot(snapshot_id: str):
    with connect() as db:
        row = db.execute("SELECT * FROM snapshots WHERE id=?", (snapshot_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    return dict(row)


@app.get("/api/snapshots/{snapshot_id}")
def snapshot_metadata(snapshot_id: str):
    return get_snapshot(snapshot_id)


@app.get("/api/snapshots/{snapshot_id}/screenshot")
def screenshot(snapshot_id: str):
    snap = get_snapshot(snapshot_id)
    return FileResponse(object_path(snap["screenshot_sha"]), media_type="image/png",
                        headers={"X-Content-Type-Options": "nosniff", "Content-Security-Policy": "default-src 'none'"})


@app.get("/api/snapshots/{snapshot_id}/export")
def export_snapshot(snapshot_id: str):
    snap = get_snapshot(snapshot_id)
    screenshot_bytes = object_path(snap["screenshot_sha"]).read_bytes()
    html_bytes = object_path(snap["html_sha"]).read_bytes()
    manifest = {"format": "versionvault-local-demo-v1", "snapshot": snap}
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr("manifest.json", json.dumps(manifest))
        zipf.writestr("screenshot.png", screenshot_bytes)
        zipf.writestr("page.html", html_bytes)
    return Response(output.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": f'attachment; filename="{snapshot_id}.zip"',
                             "X-Content-Type-Options": "nosniff"})


# Bound decompression independently of upload bytes and ZIP metadata.
MAX_IMPORT_BYTES = 10_000_000
MAX_MANIFEST_BYTES = 64_000
MAX_ENTRY_BYTES = 20_000_000
MAX_TOTAL_UNCOMPRESSED = 25_000_000
MAX_COMPRESSION_RATIO = 200
EXPECTED_ENTRIES = {"manifest.json", "page.html", "screenshot.png"}


def read_zip_entry(zipf: zipfile.ZipFile, name: str, limit: int) -> bytes:
    # A bounded stream read protects against dishonest entry size metadata.
    with zipf.open(name) as source:
        content = source.read(limit + 1)
    if len(content) > limit:
        raise ValueError("Decompressed archive entry too large")
    return content


def validate_png(data: bytes) -> None:
    """Check PNG chunk framing/CRC; does not guarantee semantic image decode."""
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("Not a PNG")
    offset = 8
    chunks = 0
    saw_image_data = False
    while offset + 12 <= len(data):
        length = int.from_bytes(data[offset:offset + 4], "big")
        kind = data[offset + 4:offset + 8]
        end = offset + 8 + length
        if end + 4 > len(data):
            raise ValueError("Truncated PNG chunk")
        actual_crc = zlib.crc32(kind + data[offset + 8:end])
        expected_crc = int.from_bytes(data[end:end + 4], "big")
        if actual_crc != expected_crc:
            raise ValueError("Corrupt PNG CRC")
        if chunks == 0:
            if kind != b"IHDR" or length != 13:
                raise ValueError("Missing PNG header")
            width = int.from_bytes(data[offset + 8:offset + 12], "big")
            height = int.from_bytes(data[offset + 12:offset + 16], "big")
            if not 1 <= width <= 16_384 or not 1 <= height <= 16_384:
                raise ValueError("Invalid PNG dimensions")
        if kind == b"IDAT":
            saw_image_data = True
        if kind == b"IEND":
            if length != 0 or not saw_image_data or end + 4 != len(data):
                raise ValueError("Invalid PNG ending")
            return
        offset = end + 4
        chunks += 1
    raise ValueError("Incomplete PNG")


@app.post("/api/import", status_code=201)
async def import_snapshot(file: UploadFile = File(...)):
    data = await file.read(MAX_IMPORT_BYTES + 1)
    if len(data) > MAX_IMPORT_BYTES:
        raise HTTPException(status_code=413, detail="Archive too large")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zipf:
            infos = zipf.infolist()
            if len(infos) != 3 or {entry.filename for entry in infos} != EXPECTED_ENTRIES:
                raise ValueError("Unexpected or duplicate archive entries")
            if sum(entry.file_size for entry in infos) > MAX_TOTAL_UNCOMPRESSED:
                raise ValueError("Archive expands beyond total size limit")
            for entry in infos:
                limit = MAX_MANIFEST_BYTES if entry.filename == "manifest.json" else MAX_ENTRY_BYTES
                if (
                    entry.is_dir()
                    or entry.flag_bits & 1  # encrypted entries unsupported
                    or entry.file_size > limit
                    or entry.compress_size > MAX_IMPORT_BYTES
                    or entry.file_size > MAX_COMPRESSION_RATIO * max(entry.compress_size, 1)
                ):
                    raise ValueError("Unsafe archive entry")
            manifest = json.loads(read_zip_entry(zipf, "manifest.json", MAX_MANIFEST_BYTES))
            if not isinstance(manifest, dict) or manifest.get("format") != "versionvault-local-demo-v1":
                raise ValueError("Unrecognized format")
            snap = manifest["snapshot"]
            if not isinstance(snap, dict):
                raise ValueError("Invalid snapshot metadata")
            if not isinstance(snap["url"], str) or len(snap["url"]) > 2048:
                raise ValueError("Bad snapshot URL")
            if not isinstance(snap["title"], str) or len(snap["title"]) > 200:
                raise ValueError("Bad snapshot title")
            if not isinstance(snap["captured_at"], str) or len(snap["captured_at"]) > 64:
                raise ValueError("Bad capture date")
            for digest_name in ("html_sha", "screenshot_sha"):
                value = snap[digest_name]
                if not isinstance(value, str) or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
                    raise ValueError("Bad artifact hash")
            html = read_zip_entry(zipf, "page.html", MAX_ENTRY_BYTES)
            image = read_zip_entry(zipf, "screenshot.png", MAX_ENTRY_BYTES)
            validate_png(image)
            if sha256(html) != snap["html_sha"] or sha256(image) != snap["screenshot_sha"]:
                raise ValueError("Digest mismatch")
    except (ValueError, TypeError, KeyError, AssertionError, zipfile.BadZipFile,
            json.JSONDecodeError, RuntimeError, EOFError, OSError, zlib.error) as exc:
        raise HTTPException(status_code=400, detail="Invalid or corrupt VersionVault archive") from exc
    ss, hs = store_object(image), store_object(html)
    new_id = uuid.uuid4().hex
    with connect() as db:
        db.execute("INSERT INTO snapshots VALUES (?, ?, ?, ?, ?, ?)",
                   (new_id, snap["url"], snap["title"], snap["captured_at"], ss, hs))
    return {"id": new_id, "imported": True}


INDEX = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VersionVault • Local demo</title><style>body{background:#f5f7fc;color:#1b2742;max-width:1150px;margin:auto;font:16px system-ui;padding:28px}header{display:flex;align-items:center;justify-content:space-between}h1{font-size:32px;margin:0 0 4px}small,.muted{color:#596476}.panel{background:white;border:1px solid #dfe3eb;border-radius:12px;padding:18px;margin:18px 0}input,button{font:inherit;padding:10px;border:1px solid #b6bfd0;border-radius:6px}input{min-width:320px}button{cursor:pointer;background:#243b70;color:white;border:0}a{color:#2349a1}table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #e4e7eb;text-align:left}#compare{display:grid;grid-template-columns:1fr 1fr;gap:12px}#compare img{max-width:100%;border:1px solid #ddd}#compare>section{overflow:hidden}@media(max-width:650px){#compare{grid-template-columns:1fr}input{min-width:0;width:85%}}</style></head><body>
<header><div><h1>VersionVault</h1><small>Local fixture proof of concept — no public crawling or live AI model preservation</small></div></header>
<div class="panel"><h2>Capture a permitted local page</h2><form id="form"><input id="url" aria-label="Capture URL" value="http://127.0.0.1:8766/" required><button>Save snapshot</button></form><p id="status" role="status" class="muted"></p></div>
<div class="panel"><h2>History</h2><label>Filter by date <input type="date" id="date"></label><button id="refresh">Refresh</button><table><thead><tr><th>Capture</th><th>Time (UTC)</th><th>Compare</th><th>Export</th></tr></thead><tbody id="entries"></tbody></table></div>
<div class="panel"><h2>Side-by-side comparison</h2><div id="compare"><section><h3>Earlier</h3><img id="left" alt="Earlier screenshot"></section><section><h3>Later</h3><img id="right" alt="Later screenshot"></section></div></div>
<div class="panel"><h2>Import an exported snapshot</h2><input id="archive" type="file" accept=".zip"><button id="import">Import</button><p id="import-status" role="status"></p></div>
<script>
const $=id=>document.getElementById(id);let records=[];
async function load(){const r=await fetch('/api/snapshots');records=await r.json();render()}
function render(){const body=$('entries');body.replaceChildren();for(const s of records){if($('date').value&&!s.captured_at.startsWith($('date').value))continue;const tr=document.createElement('tr');const td=document.createElement('td');td.textContent=s.title+' — '+s.url;tr.append(td);const time=document.createElement('td');time.textContent=s.captured_at;tr.append(time);const pair=document.createElement('td');for(const [label,id] of [['Left','left'],['Right','right']]){const b=document.createElement('button');b.textContent=label;b.onclick=()=>{$(id).src='/api/snapshots/'+encodeURIComponent(s.id)+'/screenshot'};pair.append(b,document.createTextNode(' '))}tr.append(pair);const ex=document.createElement('td');const a=document.createElement('a');a.href='/api/snapshots/'+encodeURIComponent(s.id)+'/export';a.textContent='ZIP';ex.append(a);tr.append(ex);body.append(tr)}}
$('form').onsubmit=async ev=>{ev.preventDefault();$('status').textContent='Submitting…';const r=await fetch('/api/captures',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:$('url').value})});const j=await r.json();if(!r.ok){$('status').textContent=j.detail;return}for(let n=0;n<40;n++){await new Promise(resolve=>setTimeout(resolve,400));const result=await(await fetch('/api/jobs/'+j.id)).json();$('status').textContent='Job: '+result.state;if(result.state==='ready'||result.state==='failed'){await load();return}}$('status').textContent='Job still running; refresh later'};
$('refresh').onclick=load;$('date').onchange=render;$('import').onclick=async()=>{const f=$('archive').files[0];if(!f){$('import-status').textContent='Choose a ZIP';return}const form=new FormData();form.append('file',f);const r=await fetch('/api/import',{method:'POST',body:form});$('import-status').textContent=r.ok?'Imported successfully':'Import rejected';if(r.ok)await load()};load();
</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse(INDEX, headers={"Content-Security-Policy": "default-src 'self'; script-src 'unsafe-inline' 'self'; style-src 'unsafe-inline' 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'", "X-Content-Type-Options": "nosniff"})
