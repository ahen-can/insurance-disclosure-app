from nicegui import ui, run
from extractor import extract_from_pdf
from excel_writer import update_excel
import auth

import tempfile
import os

ui.colors(
    primary="#D97B36",
    secondary="#F9E9E2",
    accent="#BF6525"
)

ui.query("body").style(
    "background:linear-gradient(135deg,#F9E9E2,#F8D9C8);"
)

uploaded_pdfs = []
uploaded_excel_data = None

async def upload_pdfs(e):
    global uploaded_pdfs
    content_bytes = await e.file.read()
    uploaded_pdfs.append({
        "name": e.file.name,
        "content": content_bytes
    })
    ui.notify(f"PDF added: {e.file.name}", color="positive")

async def upload_excel(e):
    global uploaded_excel_data
    content_bytes = await e.file.read()
    uploaded_excel_data = {
        "name": e.file.name,
        "content": content_bytes
    }
    ui.notify(f"Excel template added: {e.file.name}", color="positive")

progress = ui.linear_progress(value=0, show_value=False).classes("w-full")
progress.visible = False

status = ui.label().style(
    "font-size:16px;color:#5A3A1A;"
)

download_container = ui.column()

async def run_extraction():
    global uploaded_excel_data

    if len(uploaded_pdfs) == 0:
        ui.notify("Please upload PDFs", color="negative")
        return

    if uploaded_excel_data is None:
        ui.notify("Please upload the Excel template", color="negative")
        return

    progress.visible = True
    progress.value = 0

    tmpdir = tempfile.mkdtemp()

    excel_path = os.path.join(
        tmpdir,
        uploaded_excel_data["name"]
    )

    def save_template():
        with open(excel_path, "wb") as f:
            f.write(uploaded_excel_data["content"])

    await run.io_bound(save_template)

    results = {}
    total = len(uploaded_pdfs)

    for i, pdf in enumerate(uploaded_pdfs):
        percentage = round(((i + 1) / total) * 100)
        status.text = f"Processing {pdf['name']}..."

        try:
            data = await run.io_bound(extract_from_pdf, pdf["content"])
            insurer = data.get(
                "company_name",
                pdf["name"].replace(".pdf", "")
            )

            results[insurer] = {
                "status": "success",
                "data": data
            }

            ui.notify(
                f"Extracted {insurer}",
                color="positive"
            )

        except Exception as e:
            results[pdf["name"]] = {
                "status": "error",
                "error": str(e)
            }

        progress.value = (i + 1) / total

    status.text = "Writing to Excel template..."
    progress.value = 0
    progress.props('indeterminate')

    await run.io_bound(update_excel, results, excel_path)

    progress.props(remove='indeterminate')
    progress.value = 1.0
    status.text = "Excel compiled successfully !!"

    download_container.clear()

    with download_container:
        ui.download(
            excel_path,
            filename=uploaded_excel_data["name"]
        )

        ui.notify(
            "Done!",
            color="positive"
        )

        ui.separator()

        for insurer, result in results.items():
            if result["status"] == "success":
                with ui.expansion(insurer).classes('w-full'):
                    ui.json_editor({"content": {"json": result["data"]}})
            else:
                ui.label(f"{insurer}: {result['error']}").style("color:red;")

    status.text = "Completed"

    uploaded_pdfs.clear()
    uploaded_excel_data = None
    progress.visible = False

with ui.column().classes("w-full items-center"):

    ui.label(
        "Insurance Data Repository Creator"
    ).style("""
        font-size:40px;
        font-family:Georgia;
        font-weight:bold;
        color:#B35A1F;
    """)

    with ui.card().classes("w-3/4"):
        ui.markdown("""
### Instructions

1. Upload ONLY Public Disclosure PDFs in the required order.

2. Upload one Financial Year at a time.

3. Upload the Excel template containing sheets L2,3,4,5,6,7,9,22,37,38,39,41,45.

4. Only one user can use the tool at any given time.
                    
5. Keep in mind AI token usage.
""").style("""
        font-size:15px;
        font-family:Arial;
        font-weight:bold;
        color:#B35A1F;
    """)

    ui.upload(
        label="Upload Public Disclosure PDFs",
        multiple=True,
        auto_upload=True,
        on_upload=upload_pdfs
    ).classes("w-3/4")

    ui.upload(
        label="Upload Excel Template",
        multiple=False,
        auto_upload=True,
        on_upload=upload_excel
    ).classes("w-3/4")

    ui.button(
        "Extract & Generate Excel",
        on_click=run_extraction
    ).props("color=primary")

auth.install()

ui.run(
    title="Insurance Data Repository Creator",
    reload=False,
    **auth.run_kwargs(),
)
