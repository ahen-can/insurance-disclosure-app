# Insurance Data Repository Creator — hosted deployment

**Original tool by Asavari Kaushal: https://github.com/asavari-21/Insurance-Data-Repo**
This is a private deployment copy. The extraction logic (`extractor.py`, `prompt.py`,
`config.py`, `excel_writer.py`) is hers, unchanged. What was added here is only what is
needed to run it as a shared hosted service:

| Added | Why |
|---|---|
| `auth.py` | Password-gated login page, and `$PORT` / `0.0.0.0` binding for Render |
| `theme.py` | Shared palette and styles |
| `results_view.py`, `sheets.py` | On-screen results with copy-to-clipboard |
| `templates/` | Built-in output templates, so none has to be uploaded |
| `render.yaml`, `.python-version` | Render build and runtime configuration |
| `.gitignore` with `.env` | The original never ignored `.env`; see the warning below |
| pinned `requirements.txt` | So a rebuild installs the same stack it was tested on |

`app.py` has been reworked into a `@ui.page` layout: a fixed left panel for
instructions, uploads and template choice, and a results pane on the right. The
extraction itself (`extractor.py`, `prompt.py`, `config.py`, `excel_writer.py`) is
untouched apart from how the PDF reaches Gemini.

## Getting data out without downloading

Each sheet in the result is shown as a card with a **Copy** button that puts the data
row on the clipboard as tab-separated values, in template column order. Click a cell in
your own workbook and paste: it fills across the columns under your existing headers.
Useful where downloading a spreadsheet triggers device policy. The full workbook is
still downloadable from the button at the top of the results.

> **Security note.** In the upstream repo `.gitignore` never listed `.env`, and the file
> was committed in the first commit and deleted later (commit "Deleted .env"). Deleting a
> file does not remove it from git history, so that key is still readable by anyone who
> clones the public repo. It should be revoked. This copy ignores `.env` from its first
> commit and keeps all secrets in Render's dashboard.

## Deploying to Render

1. Push this repo (private) to GitHub.
2. Render → New → Web Service → connect the repo. `render.yaml` supplies the build and
   start commands; the free instance type is fine to begin with.
3. Set these in the Render dashboard (never in the repo):
   - `GEMINI_API_KEY` — your own key from https://aistudio.google.com/apikey
   - `APP_PASSWORD` — the password you share with colleagues
   - `STORAGE_SECRET` — any long random string (Render can generate it)
4. Free instances sleep after 15 minutes idle, so the first load after a quiet spell
   takes 30–60 seconds. That is expected, not a failure.

If `APP_PASSWORD` is unset the gate is disabled and the app is open to anyone with the
URL — fine locally, not fine on Render.

## Notes

- Upload state is per browser session, so two people can use the app at once.
- PDFs are streamed to disk and uploaded to Gemini's Files API rather than held in
  memory; inlining a 25 MB disclosure exhausted the 512 MB Render instance.
- Transient Gemini failures (503 and friends) are retried with backoff and then
  attempted against a fallback model. Set `GEMINI_MODEL`, `GEMINI_FALLBACK_MODELS` or
  `GEMINI_MAX_ATTEMPTS` to change that.
- The built-in template has no L-25 sheets: the upstream prompt drops L-25, so those
  sheets stay empty.

---

_Everything below is the original README._

A NiceGUI web app that extracts key financial and operational data from Indian life insurance companies' Public Disclosure PDFs using the Gemini API, and compiles the results into a structured Excel workbook (sheets L2–L45).

Upload one or more Public Disclosure PDFs along with an Excel template, and the app will extract the relevant figures from each PDF, write them into the appropriate sheets, and give you a download link for the completed workbook.

## Prerequisites

- Python 3.9+
- A Google Gemini API key ([Google AI Studio](https://aistudio.google.com/))

## Setup

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd Insurance-Data-Repo-main
   ```

2. **Create and activate a virtual environment**

   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Create a `.env` file in the project root with your Gemini API key:

   ```
   GEMINI_API_KEY=your_api_key_here
   ```

5. **(Optional) Generate a fresh Excel template**

   If you don't already have an Excel template with sheets L2–L45, generate one:

   ```bash
   python3 create_template.py
   ```

   This creates `insurance_data.xlsx` in the project root, which you can upload in the app.

## Running the App

```bash
python3 app.py
```

NiceGUI will start a local web server (by default at `http://localhost:8080`) and should open automatically in your browser.

## Usage

1. Upload one or more Public Disclosure PDFs (one financial year at a time).
2. Upload the Excel template (sheets L2–L45).
3. Click **Extract & Generate Excel**.
4. Once processing completes, download the compiled Excel workbook and review the extracted data for each company.

## Important Points:

1. No 2 users are to use the app simultaneously.
2. Keep in mind AI token availability while using the app.

## Notes

- Deactivate the virtual environment when you're done: `deactivate`
- Do not commit your `.env` file — it contains your API key.
