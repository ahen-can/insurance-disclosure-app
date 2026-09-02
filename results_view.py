"""Rendering extraction results for on-screen copying.

Built from the written workbook rather than the extracted JSON, so what you copy
is exactly what the download contains: same sheets, same column order, same
values. Separate from app.py so it can be rendered without an API call.
"""

from nicegui import ui

import sheets
import summary
import theme

VERDICT_COLOURS = {
    "OK": "#E2EFDA",
    "Review": "#FFF2CC",
    "Check": "#F8CBAD",
}


def render(excel_path, results, kind="life", sheet_data=None):
    """Draw the results into the current container.

    `sheet_data` is the output of sheets.read_workbook(). It is passed in rather
    than read here so the caller can do the reading off the event loop: parsing
    a twenty-sheet workbook with openpyxl blocks long enough on a small instance
    to trip the websocket reconnect, which reloads the page and empties the
    upload queue.
    """
    failures = {k: v for k, v in results.items() if v["status"] == "error"}
    successes = [k for k, v in results.items() if v["status"] == "success"]

    with ui.row().classes("items-center justify-between w-full"):
        ui.label("Results").classes("brand-title text-xl")
        ui.button("Download workbook", icon="download",
                  on_click=lambda: ui.download.file(str(excel_path),
                                                    excel_path.name)) \
            .props("outline dense color=primary")

    if successes:
        ui.label(f"Extracted: {', '.join(successes)}").classes("note")

    _usage_panel(results)

    for name, failure in failures.items():
        with ui.card().classes("panel w-full p-3") \
                .style(f"border-left:4px solid {theme.ORANGE}"):
            ui.label(f"{name} could not be extracted").classes("sheet-name")
            ui.label(failure["error"]).classes("muted")

    if not successes:
        return

    _summary_panel(results, kind)

    ui.label("Click Copy, then paste into your workbook. Values only, tab "
             "separated, in template column order.").classes("note")

    if sheet_data is None:
        sheet_data = sheets.read_workbook(excel_path)
    for sheet_name, headers, rows in sheet_data:
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
            ui.html(_table_html(headers, rows)).classes("scroll-x w-full")


def _usage_panel(results):
    """Gemini token counts for this run, in the same shape as the sheet's.

    Shown up top as a running receipt of what the extraction cost, next to the
    insurer list rather than buried below the correctness summary -- it does
    not bear on whether the data is right, just on what it took to get it.
    """
    rows = summary.collect_usage(results)
    if not rows:
        return
    *insurer_rows, total_row = rows
    with ui.row().classes("items-center gap-4 w-full"):
        ui.label(
            f"Tokens used: {_fmt(total_row[1])} in / {_fmt(total_row[2])} out "
            f"/ {_fmt(total_row[3])} total"
        ).classes("muted")
        if len(insurer_rows) > 1:
            with ui.expansion("Per PDF").classes("w-full").props("dense"):
                ui.html(_table_html(summary.USAGE_HEADERS, rows)) \
                    .classes("scroll-x w-full")


def _fmt(value):
    return f"{value:,}" if isinstance(value, (int, float)) else "-"


def _summary_panel(results, kind):
    """The same figures the '00 Summary' sheet carries, shown up front.

    Put above the data because it is what decides whether the data below can be
    trusted; the sheet itself is easy to scroll past in a 20-sheet workbook.
    """
    form_rows, review_rows = summary.collect(results, kind)
    needs_work = [r for r in form_rows if r[8] in ("Review", "Check")]

    with ui.card().classes("panel w-full p-3 gap-2"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label("Summary and confidence").classes("sheet-name")
            ui.label(f"{len(needs_work)} of {len(form_rows)} forms need a look") \
                .classes("muted")

        if review_rows:
            ui.label(f"{len(review_rows)} fields flagged for re-checking - "
                     "cross-check failures are recomputed arithmetic, model "
                     "flags are the model's own doubts.").classes("note")
        else:
            ui.label("Nothing flagged. Cross-checks all passed and the model "
                     "reported no doubts.").classes("muted")

        ui.html(_verdict_table(summary.FORM_HEADERS, form_rows)) \
            .classes("scroll-x w-full")
        if review_rows:
            ui.html(_table_html(summary.REVIEW_HEADERS, review_rows)) \
                .classes("scroll-x w-full")


def _verdict_table(headers, rows):
    """Like _table_html, but tints the verdict cell so the eye finds it."""
    head = "".join(f"<th>{_escape(h)}</th>" for h in headers)
    body = ""
    for row in rows:
        cells = ""
        for i, value in enumerate(row):
            colour = VERDICT_COLOURS.get(value) if i == 8 else None
            style = f' style="background:{colour};font-weight:600"' if colour else ""
            cells += f"<td{style}>{_escape(value)}</td>"
        body += f"<tr>{cells}</tr>"
    return f'<table class="datagrid"><tr>{head}</tr>{body}</table>'


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
