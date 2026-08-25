import os
import shutil
import tempfile
from pathlib import Path

from nicegui import app, run, ui

import auth
import results_view
import sheets
import theme
from excel_writer import update_excel
from extractor import extract_from_pdf

# Output templates shipped with the app, each paired with the form family it
# holds. Add a life v2 here once the L-25 sheets and the other known gaps are
# filled in.
TEMPLATE_DIR = Path(__file__).parent / "templates"
LIFE_TEMPLATE = "Life - Template v1 (built in)"
BUILT_IN_TEMPLATES = {
    LIFE_TEMPLATE: (TEMPLATE_DIR / "template_v1.xlsx", "life"),
    "General - Template v1 (built in)": (TEMPLATE_DIR / "template_general_v1.xlsx",
                                         "general"),
}
UPLOAD_OWN = "Upload my own..."

INSTRUCTIONS = [
    "Upload one or more Public Disclosure PDFs. One financial year at a time.",
    "Pick the output template: life (L forms) or general (NL forms).",
    "Run the extraction. Each PDF takes roughly 20-30 seconds.",
    "Check the summary first, then copy rows into your own workbook.",
]


@ui.page("/")
def main_page():
    theme.apply()

    # Per-browser-session state. Holding this in the page function rather than in
    # module globals is what lets two people use the app at once without mixing
    # each other's uploads.
    workspace = Path(tempfile.mkdtemp(prefix="idr-"))
    state = {
        "pdfs": [],
        "template": BUILT_IN_TEMPLATES[LIFE_TEMPLATE][0],
        "template_label": LIFE_TEMPLATE,
        "kind": BUILT_IN_TEMPLATES[LIFE_TEMPLATE][1],
    }

    async def on_pdf_upload(event):
        path = workspace / event.file.name
        await event.file.save(path)
        state["pdfs"].append({"name": event.file.name, "path": path})
        refresh_queue()
        ui.notify(f"Added {event.file.name}", color="positive")

    async def on_template_upload(event):
        path = workspace / f"template-{event.file.name}"
        await event.file.save(path)
        # Which form family an uploaded template is for is read off its sheet
        # names rather than asked for: it is answerable from the file, and one
        # more question in front of a run is one more thing to get wrong.
        try:
            kind = await run.io_bound(sheets.detect_kind, str(path))
        except Exception as exc:
            ui.notify(f"Could not read {event.file.name}: {exc}", color="negative")
            return
        state["template"] = path
        state["template_label"] = event.file.name
        state["kind"] = kind
        family = "general (NL forms)" if kind == "general" else "life (L forms)"
        ui.notify(f"Using {event.file.name} - read as {family}", color="positive")

    def on_template_change(event):
        if event.value == UPLOAD_OWN:
            template_upload.set_visibility(True)
            state["template"] = None
            state["template_label"] = None
            state["kind"] = None
        else:
            template_upload.set_visibility(False)
            state["template"], state["kind"] = BUILT_IN_TEMPLATES[event.value]
            state["template_label"] = event.value

    def refresh_queue():
        queue.clear()
        with queue:
            if not state["pdfs"]:
                ui.label("No PDFs added yet").classes("muted")
                return
            for item in state["pdfs"]:
                with ui.row().classes("items-center justify-between w-full no-wrap"):
                    ui.label(item["name"]).classes("step ellipsis").style("min-width:0")
                    ui.button(icon="close", on_click=lambda i=item: remove_pdf(i)) \
                        .props("flat dense round size=sm color=grey")

    def remove_pdf(item):
        state["pdfs"] = [p for p in state["pdfs"] if p is not item]
        item["path"].unlink(missing_ok=True)
        refresh_queue()

    # ---------------------------------------------------------------- extraction
    async def run_extraction():
        if not state["pdfs"]:
            ui.notify("Add at least one PDF first", color="negative")
            return
        if not state["template"]:
            ui.notify("Choose or upload an output template", color="negative")
            return

        run_button.disable()
        progress.visible = True
        progress.value = 0
        output.clear()
        with output:
            with ui.column().classes("items-center w-full gap-2") \
                    .style("margin-top:16vh"):
                ui.spinner(size="42px", color="primary")
                ui.label("Extracting...").classes("muted")

        excel_path = workspace / f"output-{Path(state['template']).name}"
        await run.io_bound(shutil.copyfile, state["template"], excel_path)

        results = {}
        total = len(state["pdfs"])
        for index, pdf in enumerate(state["pdfs"]):
            status.text = f"Extracting {pdf['name']}"
            try:
                data = await run.io_bound(extract_from_pdf, str(pdf["path"]),
                                          state["kind"])
                insurer = data.get("company_name", pdf["name"].removesuffix(".pdf"))
                results[insurer] = {"status": "success", "data": data}
            except Exception as exc:
                results[pdf["name"]] = {"status": "error", "error": str(exc)}
            progress.value = (index + 1) / total

        status.text = "Writing workbook"
        progress.props("indeterminate")
        await run.io_bound(update_excel, results, str(excel_path), state["kind"])
        progress.props(remove="indeterminate")
        progress.value = 1.0
        progress.visible = False
        status.text = ""

        output.clear()
        with output:
            results_view.render(excel_path, results, state["kind"])
        for pdf in state["pdfs"]:
            pdf["path"].unlink(missing_ok=True)
        state["pdfs"] = []
        refresh_queue()
        run_button.enable()

    # --------------------------------------------------------------------- layout
    # value=True rather than the default None: None makes NiceGUI ask the
    # browser whether the drawer should start open, and there is no toggle
    # button in this layout, so an auto-hidden panel would be unreachable.
    with ui.left_drawer(value=True, fixed=True, bordered=True).props("width=340") \
            .classes("p-4 gap-3").style(f"background:{theme.PAPER}"):
        ui.label("Insurance Data").classes("brand-title text-xl")
        ui.label("Public disclosure extractor").classes("brand-sub")
        ui.separator()

        for number, text in enumerate(INSTRUCTIONS, 1):
            with ui.row().classes("items-start gap-2 no-wrap"):
                ui.label(str(number)).classes("step-num")
                ui.label(text).classes("step").style("min-width:0")

        ui.separator()
        ui.label("DISCLOSURE PDFs").classes("muted")
        # Quasar colours the uploader header with `color`; left as primary it is a
        # slab of orange with a byte counter, which fights the rest of the panel.
        ui.upload(multiple=True, auto_upload=True, on_upload=on_pdf_upload) \
            .props('flat bordered color=grey-2 text-color=grey-8 accept=".pdf" '
                   'label="Drop or choose PDFs"') \
            .classes("w-full").style("min-height:92px")
        queue = ui.column().classes("w-full gap-1")

        ui.label("OUTPUT TEMPLATE").classes("muted")
        ui.select(list(BUILT_IN_TEMPLATES) + [UPLOAD_OWN],
                  value=LIFE_TEMPLATE, on_change=on_template_change) \
            .props("outlined dense").classes("w-full")
        template_upload = ui.upload(multiple=False, auto_upload=True,
                                    on_upload=on_template_upload) \
            .props('flat bordered color=grey-2 text-color=grey-8 accept=".xlsx" '
                   'label="Choose .xlsx"') \
            .classes("w-full").style("min-height:92px")
        template_upload.set_visibility(False)

        run_button = ui.button("Run extraction", icon="play_arrow",
                               on_click=run_extraction) \
            .props("unelevated color=primary").classes("w-full mt-1")
        progress = ui.linear_progress(value=0, show_value=False).classes("w-full")
        progress.visible = False
        status = ui.label().classes("muted")

        ui.space()
        ui.button("Sign out", icon="logout", on_click=auth.sign_out) \
            .props("flat dense color=grey").classes("w-full")

    with ui.column().classes("w-full p-6 gap-3").style("max-width:1400px"):
        output = ui.column().classes("w-full gap-3")
        with output:
            empty_state()

    refresh_queue()


def empty_state():
    with ui.column().classes("items-center w-full gap-2").style("margin-top:16vh"):
        ui.icon("description", size="56px").style(f"color:{theme.GREY}")
        ui.label("Results appear here").classes("brand-title text-xl")
        ui.label("Add a disclosure PDF on the left, then run the extraction.") \
            .classes("muted")


auth.install()

ui.run(
    title="Insurance Data Repository Creator",
    reload=False,
    **auth.run_kwargs(),
)
