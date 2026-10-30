"""Loopback-only read-only local diagnostics API and dashboard."""

from __future__ import annotations

import platform
import socket
from pathlib import Path
from urllib.parse import urlsplit

import psutil
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI(title="Remote Desktop Commander", version="0.1.0", docs_url=None, redoc_url=None)
_ALLOWED_HOSTS = {"localhost", "127.0.0.1", "::1"}


class SystemSummary(BaseModel):
    hostname: str
    platform: str
    platform_release: str
    python_version: str
    cpu_count: int
    memory_total_bytes: int
    memory_available_bytes: int
    disk_total_bytes: int
    disk_free_bytes: int


def _summary() -> SystemSummary:
    disk_path = Path.home().anchor or "/"
    try:
        disk = psutil.disk_usage(disk_path)
    except (OSError, PermissionError):
        disk = psutil.disk_usage("/")
    memory = psutil.virtual_memory()
    return SystemSummary(
        hostname=socket.gethostname(),
        platform=platform.system(),
        platform_release=platform.release(),
        python_version=platform.python_version(),
        cpu_count=psutil.cpu_count() or 1,
        memory_total_bytes=memory.total,
        memory_available_bytes=memory.available,
        disk_total_bytes=disk.total,
        disk_free_bytes=disk.free,
    )


@app.middleware("http")
async def restrict_browser_origin_and_host(request: Request, call_next):
    """Reject DNS-rebinding Host values and cross-origin browser requests."""
    host = request.url.hostname
    response = None
    if host not in _ALLOWED_HOSTS:
        response = JSONResponse(status_code=403, content={"detail": "Host not allowed"})
    else:
        origin = request.headers.get("origin")
        if origin:
            try:
                parsed = urlsplit(origin)
                origin_host = parsed.hostname
                origin_port = parsed.port
            except ValueError:
                response = JSONResponse(
                    status_code=403,
                    content={"detail": "Origin not allowed"},
                )
            else:
                request_port = request.url.port
                if (
                    parsed.scheme != request.url.scheme
                    or parsed.username is not None
                    or parsed.password is not None
                    or origin_host not in _ALLOWED_HOSTS
                    or origin_host != host
                    or (origin_port or (443 if parsed.scheme == "https" else 80))
                    != (request_port or (443 if request.url.scheme == "https" else 80))
                    or parsed.path not in {"", "/"}
                    or parsed.query
                    or parsed.fragment
                ):
                    response = JSONResponse(
                        status_code=403,
                        content={"detail": "Origin not allowed"},
                    )

        if response is None:
            response = await call_next(request)

    response.headers.setdefault("Cache-Control", "no-store")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()",
    )
    return response


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "chatrdc-agent", "version": "0.1.0"}


@app.get("/api/v1/system", response_model=SystemSummary)
def system_summary() -> SystemSummary:
    """Return a bounded, read-only host summary."""
    try:
        return _summary()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Unable to collect system summary") from exc


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Remote Desktop Commander</title>
<style>
body{font:16px system-ui,sans-serif;max-width:880px;margin:3rem auto;padding:0 1rem;background:#10151d;color:#e8edf4}
.card{border:1px solid #344154;border-radius:12px;padding:1.2rem;margin:1rem 0}
button{padding:.6rem 1rem;border-radius:8px;border:0;cursor:pointer}
pre{white-space:pre-wrap;overflow-wrap:anywhere;color:#b9d8ff}small{color:#a8b4c4}
</style></head><body><h1>Remote Desktop Commander</h1>
<p>Local device status · Read-only preview</p>
<div class="card"><b>Connection</b><p id="status">Checking local agent…</p><button onclick="refresh()">Refresh status</button></div>
<div class="card"><b>System summary</b><pre id="system">Loading…</pre></div>
<small>Local-only development scaffold. Do not expose this service to the network.</small>
<script>
async function refresh(){try{
const h=await fetch('/health');if(!h.ok)throw Error();
document.getElementById('status').textContent='Agent online';
const r=await fetch('/api/v1/system');if(!r.ok)throw Error();
document.getElementById('system').textContent=JSON.stringify(await r.json(),null,2);
}catch(e){document.getElementById('status').textContent='Unavailable';
document.getElementById('system').textContent='Unable to load system summary.'}}
refresh();
</script></body></html>"""
