# backend/app/scraper/static_scraper.py
import httpx
from typing import Dict, List

from ..config import settings
from .parser import parse_document
from .utils import classify_error, record_event


async def fetch_static_and_parse(
    url: str,
    errors: List[Dict[str, str]],
    interactions: Dict,
) -> Dict:
    try:
        async with httpx.AsyncClient(
            timeout=settings.static_timeout, follow_redirects=True
        ) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            html = resp.text
    except Exception as exc:
        err = classify_error(exc, phase="fetch")
        errors.append(err)
        raise

    record_event(interactions, "static_fetch", "Fetched static HTML", url=url)

    # Parse
    result = parse_document(
        input_url=url,
        html=html,
        base_url=url,
        strategy="static",
    )
    return result