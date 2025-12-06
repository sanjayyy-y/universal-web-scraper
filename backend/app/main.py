
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from .models import ScrapeRequest
from .scraper.static_scraper import fetch_static_and_parse
from .scraper.js_scraper import scrape_with_js
from .scraper.utils import init_interactions, total_text_length, classify_error

app = FastAPI(title="Lyftr Universal Website Scraper")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.post("/scrape")
async def scrape(req: ScrapeRequest):
    """
    Core endpoint as per assignment:
    - Accepts JSON: { "url": "https://example.com" }
      plus optional:
      - mode: "auto" | "static" | "js"
      - deep: bool
    - Returns JSON with `result` key.
    """
    url = str(req.url)

    if not (url.startswith("http://") or url.startswith("https://")):
        raise HTTPException(
            status_code=400,
            detail="Only http(s) URLs are supported",
        )

    interactions = init_interactions(url)
    errors = []

    result = None

    try:
        if req.mode in ("auto", "static"):
            # 1) Static scrape
            static_result = await fetch_static_and_parse(url, errors, interactions)
            text_len = total_text_length(static_result["sections"])

            result = static_result

            # 2) Conditional JS fallback in auto mode
            if req.mode == "auto" and text_len < 500:
                js_result = await scrape_with_js(url, interactions, errors, deep=req.deep)
                if js_result is not None:
                    result = js_result

        elif req.mode == "js":
            js_result = await scrape_with_js(url, interactions, errors, deep=req.deep)
            if js_result is None:
                # If JS fails completely, fall back to static to avoid empty data
                static_result = await fetch_static_and_parse(url, errors, interactions)
                result = static_result
            else:
                result = js_result

    except Exception as exc:
        errors.append(classify_error(exc, phase="fetch"))
        if result is None:
            # Last-resort fallback if nothing parsed
            result = {
                "url": url,
                "scrapedAt": "",
                "meta": {
                    "title": "",
                    "description": "",
                    "language": "",
                    "canonical": None,
                    "strategy": "error",
                },
                "sections": [],
            }

    result["interactions"] = {
        "clicks": interactions.get("clicks", []),
        "scrolls": interactions.get("scrolls", 0),
        "pages": interactions.get("pages", []),

        "timeline": interactions.get("timeline", []),
    }
    result["errors"] = errors

    return JSONResponse({"result": result})


app.mount(
    "/", StaticFiles(directory="frontend/dist", html=True), name="frontend"
)