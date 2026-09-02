# extractor.py
# import google.generativeai as genai
import json
import os
import random
import time
from dotenv import load_dotenv
from prompt import build_general_prompt, build_prompt
from google import genai
from google.genai import errors

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# gemini-2.5-flash, which this tool was written against, is closed to new API
# keys ("no longer available to new users"), so the model has to be named
# explicitly and is worth keeping configurable — swapping it on Render is then
# an env var change rather than a code change.
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

# Google returns 503 UNAVAILABLE when a model is busy, which happens to the
# newest models in particular and has nothing to do with the request. Without a
# retry the whole PDF is lost to a momentary spike, so transient failures are
# retried with backoff and then tried against a second model.
FALLBACK_MODELS = [m.strip() for m in
                   os.getenv("GEMINI_FALLBACK_MODELS", "gemini-3.5-flash").split(",")
                   if m.strip()]
MAX_ATTEMPTS = int(os.getenv("GEMINI_MAX_ATTEMPTS", "4"))
TRANSIENT_CODES = {429, 500, 502, 503, 504}


def _generate(contents):
    """Call Gemini, retrying transient failures and falling back to another model."""
    models = [MODEL] + [m for m in FALLBACK_MODELS if m != MODEL]
    last_error = None
    for model in models:
        for attempt in range(MAX_ATTEMPTS):
            try:
                return client.models.generate_content(model=model, contents=contents)
            except errors.APIError as exc:
                if getattr(exc, "code", None) not in TRANSIENT_CODES:
                    raise
                last_error = exc
                if attempt < MAX_ATTEMPTS - 1:
                    time.sleep(2 ** attempt + random.random())
    tried = ", ".join(models)
    raise RuntimeError(
        f"Gemini was unavailable after retrying {tried}. This is a temporary "
        f"capacity problem on Google's side, not a problem with the PDF or the "
        f"API key — try again shortly, or set GEMINI_MODEL to another model. "
        f"Last error: {last_error}"
    ) from last_error

#genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
#model = genai.GenerativeModel("gemini-2.5-flash")

def _wait_active(uploaded, timeout=120):
    """Wait for an uploaded file to finish processing before it is referenced."""
    deadline = time.time() + timeout
    while uploaded.state and uploaded.state.name == "PROCESSING":
        if time.time() > deadline:
            raise RuntimeError(f"Gemini did not finish processing {uploaded.name} in time")
        time.sleep(1)
        uploaded = client.files.get(name=uploaded.name)
    if uploaded.state and uploaded.state.name == "FAILED":
        raise RuntimeError(f"Gemini could not process the uploaded PDF ({uploaded.name})")
    return uploaded


def extract_from_pdf(pdf_path, kind: str = "life") -> dict:
    """Extract one disclosure PDF, given a path on disk.

    `kind` picks the form family: "life" for the L forms, "general" for the NL
    forms. Everything below is shared - only the prompt differs.

    The PDF is uploaded to Gemini's Files API and referenced by name rather than
    inlined in the request. Inlining base64-encodes the whole file into every
    request — about 100 MB of copies for a 25 MB disclosure, repeated on each
    retry — which is what exhausted the 512 MB instance.
    """
    prompt = build_general_prompt() if kind == "general" else build_prompt()

    uploaded = client.files.upload(
        file=str(pdf_path),
        config={"mime_type": "application/pdf"},
    )
    try:
        uploaded = _wait_active(uploaded)
        response = _generate([uploaded, prompt])
        usage = getattr(response, "usage_metadata", None)
    finally:
        # Uploaded files expire on their own after 48h; removing them keeps the
        # account's file list clean when many PDFs are processed in a batch.
        try:
            client.files.delete(name=uploaded.name)
        except Exception:
            pass
    
    raw = response.text.strip()
    
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()
    
    data = json.loads(raw)
    # Piggy-backed onto the same dict as "confidence" and "review", so it
    # travels through app.py and excel_writer.py without either needing to
    # know it exists -- both already pass the whole dict through untouched.
    if usage is not None:
        data["usage"] = {
            "input_tokens": usage.prompt_token_count,
            "output_tokens": usage.candidates_token_count,
            "total_tokens": usage.total_token_count,
        }
    return data
