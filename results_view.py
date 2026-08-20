"""Rendering extraction results for on-screen copying.

Built from the written workbook rather than the extracted JSON, so what you copy
is exactly what the download contains: same sheets, same column order, same
values. Separate from app.py so it can be rendered without an API call.
"""

from nicegui import ui

import sheets
import theme


def render(excel_path, results):
    """Draw the results into the current container."""
    failures = {k: v for k, v in results.items() if v["status"] == "error"}
    successes = [k for k, v in results.items() if v["status"] == "success"]

    with ui.row().classes("items-center justify-between w-full"):
        ui.label("Results").classes("brand-title text-xl")
        ui.button("Download workbook", icon="download",
                  on_click=lambda: ui.download.file(str(excel_path),
                                                    excel_path.name)) \
            .props("outline dense color=primary")

    if successes:
        ui.label(f"Extracted: {', '.join(successes)}").classes("muted")

    for name, failure in failures.items():
        with ui.card().classes("panel w-full p-3") \
                .style(f"border-left:4px solid {theme.ORANGE}"):
            ui.label(f"{name} could not be extracted").classes("sheet-name")
            ui.label(failure["error"]).classes("muted")

    if not successes:
        return

    ui.label("Click Copy, then paste into your workbook. Values only, tab "
             "separated, in template column order.").classes("muted")

    for sheet_name, headers, rows in sheets.read_workbook(excel_path):
        with ui.card().classes("panel w-full p-3 gap-2"):
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(sheet_name).classes("sheet-name")
                ui.label(f"{len(headers)} columns").classes("muted")
            for row in rows:
                with ui.row().classes("items-center justify-between w-full no-wrap"):
                    ui.label(str(row[0]) if row and row[0] else "(row)") \
                        .classes("step ellipsis").style("min-width:0")
                    ui.button("Copy", icon="content_copy",
                              on_click=lambda r=row, s=sheet_name: _copy(r, s)) \
                        .props("flat dense color=primary")
            with ui.expansion("Preview").classes("w-full").props("dense"):
                ui.html(_table_html(headers, rows)).classes("scroll-x")


def _copy(row, sheet_name):
    ui.clipboard.write(sheets.to_tsv(row))
    ui.notify(f"{sheet_name} row copied - paste into your workbook",
              color="positive")


def _table_html(headers, rows):
    head = "".join(f"<th>{_escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{_escape(c)}</td>" for c in row) + "</tr>"
                   for row in rows)
    return f'<table class="datagrid"><tr>{head}</tr>{body}</table>'


def _escape(value):
    text = "" if value is None else str(value)
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
