"""Shared-password gate and Render-compatible server settings.

Kept apart from app.py so the extraction code stays as Asavari wrote it.
The app sits at a public URL and spends our own Gemini quota on every run, so
it must not be reachable without the password.
"""

import os
import secrets

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from starlette.middleware.base import BaseHTTPMiddleware

import theme

APP_PASSWORD = os.environ.get("APP_PASSWORD", "")

# NiceGUI's own endpoints serve the page's JS, the websocket handshake and the
# upload POSTs; redirecting those would break the page for a signed-in user too.
UNRESTRICTED_PREFIXES = ("/login", "/_nicegui", "/favicon", "/socket.io")


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith(UNRESTRICTED_PREFIXES) or is_signed_in():
            return await call_next(request)
        return RedirectResponse("/login")


def is_signed_in() -> bool:
    try:
        return bool(app.storage.user.get("authenticated", False))
    except RuntimeError:      # no request context, e.g. during startup
        return False


def sign_out() -> None:
    app.storage.user["authenticated"] = False
    ui.navigate.to("/login")


@ui.page("/login")
def login_page():
    theme.apply()

    def attempt():
        if APP_PASSWORD and secrets.compare_digest(password.value or "", APP_PASSWORD):
            app.storage.user["authenticated"] = True
            ui.navigate.to("/")
        else:
            password.value = ""
            ui.notify("Incorrect password", color="negative")

    with ui.column().classes("absolute-center items-center gap-4"):
        ui.label("Insurance Data Repository").classes("brand-title text-3xl")
        ui.label("Public disclosure extractor").classes("brand-sub")
        with ui.card().classes("panel p-6 items-stretch").style("width: 340px"):
            password = ui.input("Password", password=True,
                                password_toggle_button=True) \
                .props("outlined dense").classes("w-full")
            password.on("keydown.enter", attempt)
            ui.button("Sign in", on_click=attempt) \
                .props("unelevated color=primary").classes("w-full mt-2")


_INSTALLED = False


def install() -> bool:
    """Enable the password gate. Returns False when no password is configured."""
    global _INSTALLED
    if _INSTALLED or not APP_PASSWORD:
        return False
    app.add_middleware(AuthMiddleware)
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
        "show": False,
        # NiceGUI defaults to 3 seconds, after which the browser gives up on the
        # websocket and reloads the page. A reload re-runs the page function,
        # which builds a fresh workspace and state -- so the queued PDFs vanish
        # and "Run extraction" then does nothing but show a toast. Three seconds
        # is far too tight on a free instance sharing a tenth of a CPU, where a
        # single openpyxl load can stall the loop for longer than that.
        "reconnect_timeout": float(os.environ.get("RECONNECT_TIMEOUT", 60)),
    }
