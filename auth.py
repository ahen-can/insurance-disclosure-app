"""Shared-password gate and Render-compatible server settings.

Kept apart from app.py so the original tool's code stays as Asavari wrote it.
The app sits at a public URL and spends our own Gemini quota on every run, so it
must not be reachable without the password.

HTTP Basic Auth rather than a NiceGUI login page: NiceGUI 3.x refuses to mix
`@ui.page` with UI defined at global scope, and app.py defines its UI globally.
A login page would mean restructuring the tool before we have ever seen it run.
Basic auth needs no page at all, so app.py keeps her code intact.
"""

import base64
import os
import secrets

from nicegui import app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
REALM = 'Basic realm="Insurance Data Repository Creator", charset="UTF-8"'


def _password_matches(header: str) -> bool:
    if not header.lower().startswith("basic "):
        return False
    try:
        decoded = base64.b64decode(header[6:]).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return False
    _username, separator, password = decoded.partition(":")
    if not separator:
        return False
    # Any username is accepted; only the shared password is checked.
    return secrets.compare_digest(password, APP_PASSWORD)


class BasicAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if _password_matches(request.headers.get("authorization", "")):
            return await call_next(request)
        return Response(status_code=401, headers={"WWW-Authenticate": REALM})


_INSTALLED = False


def install() -> bool:
    """Enable the password gate. Returns False when no password is configured.

    Idempotent on purpose: with the UI defined at global scope, NiceGUI re-runs
    app.py on every page request to rebuild it, so this is called repeatedly, and
    Starlette refuses to add middleware once the server is running.
    """
    global _INSTALLED
    if _INSTALLED or not APP_PASSWORD:
        return False
    app.add_middleware(BasicAuthMiddleware)
    _INSTALLED = True
    return True


def run_kwargs() -> dict:
    """Server settings that differ between local use and Render.

    Render routes traffic to $PORT (10000 by default) and requires binding to
    0.0.0.0; ui.run() otherwise picks its own defaults and the deploy fails
    health checks.
    """
    return {
        "host": "0.0.0.0",
        "port": int(os.environ.get("PORT", 8080)),
        "storage_secret": os.environ.get("STORAGE_SECRET", "local-dev-secret"),
        "show": False,          # no browser to open on a server
    }
