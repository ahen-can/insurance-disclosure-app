# Insurance Data Repository Creator — hosted deployment

**Original tool by Asavari Kaushal: https://github.com/asavari-21/Insurance-Data-Repo**
This is a private deployment copy. The extraction logic (`extractor.py`, `prompt.py`,
`config.py`, `excel_writer.py`) is hers, unchanged. What was added here is only what is
needed to run it as a shared hosted service:

| Added | Why |
|---|---|
| `auth.py` | Shared-password gate, and `$PORT` / `0.0.0.0` binding for Render |
| `render.yaml`, `.python-version` | Render build and runtime configuration |
| `.gitignore` with `.env` | The original never ignored `.env`; see the warning below |
| pinned `requirements.txt` | So a rebuild installs the same stack it was tested on |

`app.py` differs from the original by three lines: an `import auth`, an `auth.install()`,
and `**auth.run_kwargs()` passed to `ui.run`.

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

## Known limitation, not yet fixed

Uploads are held in module-level globals, so **two people using the hosted app at the
same time will mix each other's files**. This deployment ships the tool as-is; isolating
state per browser session is the next change.

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
